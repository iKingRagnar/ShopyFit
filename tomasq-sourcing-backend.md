# TOMASQ Sourcing — Arquitectura Backend

> Cómo conectar el dashboard del HTML con scraping real de precios.

---

## Stack recomendado

```
┌─────────────────────────────────────────────────────────┐
│  n8n (cron diario 6 AM)                                 │
│    ├─ HTTP Request → Telas Parisina                     │
│    ├─ HTTP Request → Modatelas                          │
│    ├─ Playwright/Puppeteer node → Casa Cervantes (JS)   │
│    └─ Python Code node → BeautifulSoup parsing          │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Supabase / Neon PostgreSQL                             │
│    ├─ tabla: suppliers                                  │
│    ├─ tabla: materials                                  │
│    ├─ tabla: price_snapshots (histórico)                │
│    └─ tabla: products_bom (Bill of Materials)           │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  FastAPI / n8n webhook → JSON endpoint                  │
│    GET /api/sourcing/best-price?product=tee             │
│    GET /api/sourcing/suppliers/:material_id             │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
              [TOMASQ B2B Dashboard HTML]
```

---

## 1. Schema PostgreSQL

```sql
CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  location VARCHAR(80),
  type VARCHAR(20) CHECK (type IN ('nacional','importacion')),
  website TEXT,
  scraping_url TEXT,
  scraping_method VARCHAR(20), -- 'http','playwright','api'
  rating DECIMAL(2,1),
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE materials (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  category VARCHAR(50), -- 'tela_principal','hilo','etiqueta','empaque'
  unit VARCHAR(10), -- 'm','kg','u'
  spec JSONB -- {gsm:240,composition:'95% algodón 5% spandex'}
);

CREATE TABLE price_snapshots (
  id BIGSERIAL PRIMARY KEY,
  supplier_id INT REFERENCES suppliers(id),
  material_id INT REFERENCES materials(id),
  price DECIMAL(10,2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'MXN',
  stock_qty INT,
  stock_status VARCHAR(20), -- 'ok','low','out'
  delivery_days_min INT,
  delivery_days_max INT,
  scraped_at TIMESTAMP DEFAULT NOW(),
  source_url TEXT,
  raw_html TEXT -- backup
);

CREATE INDEX idx_price_latest ON price_snapshots(material_id, supplier_id, scraped_at DESC);

CREATE TABLE products_bom (
  id SERIAL PRIMARY KEY,
  product_sku VARCHAR(40) NOT NULL,
  product_name VARCHAR(120),
  material_id INT REFERENCES materials(id),
  qty_per_unit DECIMAL(10,3) NOT NULL,
  notes TEXT
);

-- Vista: mejor precio por material
CREATE VIEW v_best_prices AS
SELECT DISTINCT ON (material_id)
  material_id,
  supplier_id,
  price,
  stock_status,
  delivery_days_min,
  scraped_at
FROM price_snapshots
WHERE scraped_at > NOW() - INTERVAL '7 days'
  AND stock_status != 'out'
ORDER BY material_id, price ASC;
```

---

## 2. Scraper Python (módulo base)

```python
# scraper_textil.py
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import psycopg2
from datetime import datetime

class TextilScraper:
    def __init__(self, db_conn_str):
        self.conn = psycopg2.connect(db_conn_str)
    
    def scrape_modatelas(self, material_query="algodon pima 240"):
        """HTTP simple - sitio renderizado server-side"""
        url = f"https://www.modatelas.com.mx/buscar?q={material_query}"
        r = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; TomasqBot/1.0)'
        })
        soup = BeautifulSoup(r.text, 'lxml')
        results = []
        for card in soup.select('.product-card'):
            results.append({
                'name': card.select_one('.product-name').text.strip(),
                'price': float(card.select_one('.price').text.replace('$','').replace(',','')),
                'stock': 'ok' if card.select_one('.in-stock') else 'low',
                'url': card.select_one('a')['href']
            })
        return results
    
    def scrape_casa_cervantes(self, material_query):
        """Playwright - sitio con JS dinámico"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://casacervantes.mx/search?q={material_query}")
            page.wait_for_selector('.product-grid', timeout=10000)
            
            products = page.query_selector_all('.product-item')
            results = []
            for prod in products:
                results.append({
                    'name': prod.query_selector('.title').inner_text(),
                    'price': float(prod.query_selector('.price-now').inner_text().replace('$','').replace(',','')),
                    'stock': prod.query_selector('.stock-status').inner_text(),
                })
            browser.close()
            return results
    
    def save_snapshot(self, supplier_id, material_id, data):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO price_snapshots 
            (supplier_id, material_id, price, stock_status, scraped_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (supplier_id, material_id, data['price'], data['stock']))
        self.conn.commit()

# Uso
if __name__ == "__main__":
    scraper = TextilScraper("postgresql://user:pass@host/tomasq")
    
    # Scrape 14 proveedores en paralelo (asyncio)
    suppliers = [
        ('modatelas', 1, scraper.scrape_modatelas),
        ('casa_cervantes', 2, scraper.scrape_casa_cervantes),
        # ... más
    ]
    
    for name, sup_id, fn in suppliers:
        try:
            data = fn("algodon pima 240")
            scraper.save_snapshot(sup_id, material_id=1, data=data[0])
            print(f"✓ {name}: ${data[0]['price']}")
        except Exception as e:
            print(f"✗ {name}: {e}")
```

---

## 3. n8n Workflow

```json
{
  "name": "TOMASQ — Daily Sourcing Scrape",
  "nodes": [
    {
      "name": "Cron Daily 6AM",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "triggerTimes": {
          "item": [{"hour": 6, "minute": 0}]
        }
      }
    },
    {
      "name": "Get Active Suppliers",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT id, name, scraping_url, scraping_method FROM suppliers WHERE active = true"
      }
    },
    {
      "name": "Split In Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": {"batchSize": 1}
    },
    {
      "name": "Switch Method",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": {
          "rules": [
            {"value2": "http"},
            {"value2": "playwright"},
            {"value2": "api"}
          ]
        }
      }
    },
    {
      "name": "HTTP Scrape",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "={{ $json.scraping_url }}",
        "method": "GET"
      }
    },
    {
      "name": "Code: Parse HTML",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const cheerio = require('cheerio');\nconst $ = cheerio.load($input.item.json.data);\nconst price = parseFloat($('.price-now').text().replace('$','').replace(',',''));\nreturn [{json: {price, scraped_at: new Date()}}];"
      }
    },
    {
      "name": "Insert Snapshot",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "price_snapshots"
      }
    },
    {
      "name": "Webhook → Dashboard",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "tomasq-prices-updated",
        "responseMode": "lastNode"
      }
    }
  ]
}
```

---

## 4. FastAPI endpoint para el dashboard HTML

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2.extras

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/api/sourcing/comparator")
def get_comparator(product_sku: str = "tee"):
    conn = psycopg2.connect(DSN)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT 
            s.name,
            s.location,
            s.rating,
            ps.price,
            ps.stock_status,
            ps.delivery_days_min,
            ps.delivery_days_max,
            ps.scraped_at,
            CASE WHEN ps.price = MIN(ps.price) OVER () 
                 THEN true ELSE false END AS is_best
        FROM price_snapshots ps
        JOIN suppliers s ON s.id = ps.supplier_id
        JOIN products_bom bom ON bom.material_id = ps.material_id
        WHERE bom.product_sku = %s
          AND ps.scraped_at > NOW() - INTERVAL '7 days'
        ORDER BY ps.price ASC
    """, (product_sku,))
    return {"suppliers": cur.fetchall()}

@app.get("/api/sourcing/calc")
def calculate_cost(product_sku: str, qty: int = 1, margin_pct: float = 79):
    """Calcula costo total, PV sugerido, utilidad"""
    # ... query BOM + best prices + multiply by qty
    pass

@app.post("/api/sourcing/refresh")
def trigger_scrape():
    """Triggers el workflow n8n manualmente"""
    requests.post("https://guillermocantuu.app.n8n.cloud/webhook/scrape-now")
    return {"status": "triggered"}
```

---

## 5. Conectar dashboard HTML a backend

En el HTML actual, reemplazar la función `refreshScrap()` y los datos mock:

```javascript
async function refreshScrap(btn) {
  btn.classList.add('spin');
  showToast('Ejecutando scrapers...');
  
  // Trigger n8n workflow
  await fetch('https://api.tomasq.mx/api/sourcing/refresh', {method: 'POST'});
  
  // Wait for scrape to complete (poll or websocket)
  setTimeout(async () => {
    const data = await fetch('https://api.tomasq.mx/api/sourcing/comparator?product_sku=tee')
      .then(r => r.json());
    
    // Re-render supplier table
    renderSuppliers(data.suppliers);
    btn.classList.remove('spin');
    showToast('✓ ' + data.suppliers.length + ' proveedores actualizados');
  }, 1800);
}

async function selProd(btn, prod) {
  document.querySelectorAll('.bp-tab').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  
  const data = await fetch(`https://api.tomasq.mx/api/sourcing/comparator?product_sku=${prod}`)
    .then(r => r.json());
  
  renderSuppliers(data.suppliers);
  
  const calc = await fetch(`https://api.tomasq.mx/api/sourcing/calc?product_sku=${prod}&qty=500&margin_pct=79`)
    .then(r => r.json());
  
  updateCalculator(calc);
}
```

---

## 6. Proveedores reales para arrancar (México)

| Proveedor | URL | Método | Producto target |
|-----------|-----|--------|----------------|
| Telas Parisina | parisina.com | HTTP + Cheerio | Algodón, jersey, French Terry |
| Modatelas | modatelas.com.mx | HTTP simple | Telas técnicas, mesh |
| Casa Cervantes | casacervantes.mx | Playwright (JS) | Algodón Pima premium |
| Telas París | telasparis.com | HTTP | Lycra, spandex |
| Telas El Tejedor | teleltejedor.com | HTTP | Hilo industrial |
| Mercado Libre | api.mercadolibre.com | API oficial | Multi-vendor |
| Alibaba | alibaba.com | Playwright + login | Importación en volumen |
| Made-in-China | made-in-china.com | Playwright | Importación |

---

## 7. Compliance & rate limiting

```python
# Respetar robots.txt
from urllib.robotparser import RobotFileParser

def can_scrape(url):
    rp = RobotFileParser()
    rp.set_url(f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt")
    rp.read()
    return rp.can_fetch("TomasqBot/1.0", url)

# Rate limit: max 1 req/3s por proveedor
import time
from functools import wraps

def rate_limit(seconds=3):
    last_call = {}
    def decorator(func):
        @wraps(func)
        def wrapper(supplier, *args, **kwargs):
            now = time.time()
            if supplier in last_call and now - last_call[supplier] < seconds:
                time.sleep(seconds - (now - last_call[supplier]))
            last_call[supplier] = time.time()
            return func(supplier, *args, **kwargs)
        return wrapper
    return decorator
```

---

## 8. Deploy

- **n8n**: ya lo tienes en `guillermocantuu.app.n8n.cloud`. Crear workflow.
- **PostgreSQL**: Neon (ya lo usas en ARIA) o Supabase. Crear las 4 tablas.
- **Scrapers Python**: Railway o Render. `requirements.txt`: `playwright, beautifulsoup4, psycopg2-binary, fastapi, uvicorn`
- **Dashboard HTML**: GitHub Pages + dominio `b2b.tomasq.mx`

---

## Quick wins primera semana

1. **Día 1-2**: Schema SQL + 3 scrapers básicos (Modatelas, Parisina, Casa Cervantes)
2. **Día 3**: n8n workflow con cron diario
3. **Día 4**: FastAPI con 2 endpoints (`/comparator`, `/refresh`)
4. **Día 5**: Conectar HTML al backend, deploy
5. **Día 6-7**: Agregar 5 proveedores más + alertas de cambio de precio (>5% delta)
