# ShopyFit · TOMASQ v5 — Storefront + Ops AI

Plataforma fashion-tech estática para **TOMASQ — Built Different**. Incluye:

### 🛍️ Storefront público (`index.html`)
- Catálogo segmentado por **nicho deportivo** (🏃 Running · 🏋 Gym · ⚡ Crossfit · 🧘 Yoga · 🏙 Streetwear)
- Filtro secundario por **rango de edad** (18–24 · 25–34 · 35–44 · 45+)
- Hero, ticker, drops, **B2B Sourcing** comparador y **Fulfillment MRP** con BOM auto-consolidado y acciones WhatsApp / email / PO PDF.

### 🤖 Ops AI Dashboard (`dashboard.html`) — nivel "más allá de Shopify"
Panel de operación para que la marca corra sola. 6 módulos:

| Módulo               | Qué hace                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| **Overview**         | KPIs (ventas, margen, stock muerto), sparkline 14d, feed de decisiones automáticas que la IA ejecutó hoy |
| **AI Advisor**       | Recomendación destacada del día + grid de acciones (descuento, envío gratis dinámico, giveaway, bundle, recovery, restock, loyalty) + chat con Claude |
| **Inventario FIFO**  | Tabla de lotes ordenada por antigüedad, alertas de stock muerto (>60d), reorden sugerido (velocidad × lead time) |
| **Pricing Engine**   | 3 tiers (Value/Mid/Premium) calculados desde BOM real, A/B test continuo, reglas dinámicas por rotación |
| **Automation Flows** | Calendario 12 meses · Carrito abandonado 3-toques (email → WA → cupón) · Loyalty (Bronze/Silver/Gold) · 8 workflows n8n live |
| **Suppliers**        | Score 0–100 (precio + lead + defectos + cumplimiento), alerta proveedor único, auto-recotización |

### 📐 Sistema de diseño TOMASQ v4
Lime `#D4FF00`, fondos `#141416 / #1c1c1f / #26262a`, texto `#f5f5f2 / #c8c8c2`. Bebas Neue / Barlow Condensed / Barlow / JetBrains Mono.

El sitio es **100% estático** (HTML + CSS y JS inline) — cero build step.

---

## Estructura

```
.
├── index.html                   # Storefront v5 (con filtros nicho + edad)
├── dashboard.html               # Ops AI Dashboard (6 módulos)
├── tomasq-v4.html               # Snapshot v4 storefront (sin filtros nuevos)
├── tomasq-v3.html               # Versión anterior (accesible en /v3)
├── tomasq-sourcing-backend.md   # Arquitectura backend para scraping real
├── vercel.json                  # Config Vercel (headers + cache)
├── netlify.toml                 # Config Netlify (headers + redirects)
└── filesfit.zip                 # Bundle original subido
```

---

## Cómo levantarlo

### Opción 1 — Vercel (recomendado)

```bash
# Una sola vez
npm i -g vercel

# Deploy
vercel --prod
```

O conecta el repo en https://vercel.com/new — Vercel detecta `vercel.json` y publica sin build command.

### Opción 2 — Netlify

```bash
npm i -g netlify-cli
netlify deploy --prod --dir .
```

O arrastra la carpeta entera a https://app.netlify.com/drop.

### Opción 3 — GitHub Pages

1. Repo → **Settings** → **Pages**
2. Source: `Deploy from a branch`
3. Branch: `main` / folder: `/ (root)`
4. Guarda — la URL queda en `https://ikingragnar.github.io/ShopyFit/`

### Opción 4 — Cloudflare Pages

1. Conecta el repo en https://pages.cloudflare.com
2. Build command: *(vacío)*
3. Build output directory: `/`

### Opción 5 — Local (desarrollo)

```bash
# Cualquiera de estos:
python3 -m http.server 8000
# o
npx serve .
```

Abre http://localhost:8000.

---

## Rutas

| Ruta               | Sirve                                |
| ------------------ | ------------------------------------ |
| `/`                | `index.html` — storefront v5         |
| `/dashboard.html`  | Ops AI Dashboard (6 módulos)         |
| `/v4`              | `tomasq-v4.html` — storefront v4     |
| `/v3`              | `tomasq-v3.html` — storefront v3     |

---

## Conectar con backend real

Todos los handlers JS del dashboard tienen un `// TODO:` que apunta al fetch a
implementar. Resumen de endpoints / webhooks pendientes:

| Acción                     | Función JS              | Endpoint sugerido                                                |
| -------------------------- | ----------------------- | ---------------------------------------------------------------- |
| Aplicar recomendación IA   | `applyRec(id)`          | `POST /api/ai-advisor/apply` o `https://…n8n.cloud/webhook/apply-rec` |
| Chat con AI Advisor        | `askAI()`               | `POST /api/ai-advisor` → Anthropic Claude / OpenAI               |
| Sugerir reorden            | `suggestReorder(sku)`   | `POST /api/fifo-suggest` (Postgres + lógica velocidad)           |
| Auto-recotizar proveedores | `runAutoRequote()`      | `POST https://…n8n.cloud/webhook/requote`                        |
| Enviar PO consolidada      | `sendAllPO(orderId)`    | `POST https://…n8n.cloud/webhook/po-send`                        |
| Refresh scraping           | `refreshScrap(btn)`     | `POST /api/refresh` (FastAPI)                                    |

Ejemplo de migración:

```js
async function applyRec(id) {
  const r = await fetch('https://guillermocantuu.app.n8n.cloud/webhook/apply-rec', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ rec_id: id }),
  });
  const { ok, message } = await r.json();
  toast(message, ok ? 'success' : 'error');
}
```

Arquitectura completa (Postgres schema, scrapers Python, workflow n8n,
endpoints FastAPI) en [`tomasq-sourcing-backend.md`](./tomasq-sourcing-backend.md).
