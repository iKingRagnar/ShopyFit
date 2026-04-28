# ShopyFit · KÖRE v5 — Storefront + Ops AI

Plataforma fashion-tech estática para **KÖRE — Built Different**. Incluye:

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
| **Automation Flows** | Calendario 12 meses · Carrito abandonado 3-toques (email → WA → cupón) · Loyalty (Bronze/Silver/Gold) · workflows propios en FastAPI |
| **Suppliers**        | Score 0–100 (precio + lead + defectos + cumplimiento), alerta proveedor único, auto-recotización |

### 📐 Sistema de diseño KÖRE v4
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

## Backend (FastAPI en Railway)

El backend vive en [`api/`](./api/) — FastAPI + Anthropic SDK, deployable como
**segundo servicio en Railway** (root directory `api/`). El sitio estático
queda intacto.

### Endpoints

| Función JS (`dashboard.html`) | Endpoint                              |
| ----------------------------- | ------------------------------------- |
| `applyRec(id)`                | `POST /api/recommendations/apply`     |
| `askAI()`                     | `POST /api/ai-advisor` → Claude       |
| `suggestReorder(sku)`         | `POST /api/fifo/suggest-reorder`      |
| `runAutoRequote()`            | `POST /api/suppliers/requote`         |
| (futuro) precios              | `POST /api/pricing/apply`             |
| (futuro) PO MRP               | `POST /api/po/send`                   |

### Activar el backend desde el front

En `dashboard.html`, al inicio del `<script>`:

```js
const API_BASE = 'https://shopyfit-api-production.up.railway.app';
const USE_API  = true;
```

Mientras `USE_API=false` los handlers usan respuestas mock locales (útil para
demo sin backend desplegado).

### Detalles de deploy

Pasos completos (Railway → segundo servicio → root `api/` → env vars
`ANTHROPIC_API_KEY` y `ALLOWED_ORIGINS`) en [`api/README.md`](./api/README.md).

> El doc histórico [`tomasq-sourcing-backend.md`](./tomasq-sourcing-backend.md)
> describe la arquitectura original con n8n. Se mantiene como referencia,
> pero la implementación vigente es la de `api/` (FastAPI directo).
