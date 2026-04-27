# ShopyFit · TOMASQ v3 / v4

Sitio estático single-page de **TOMASQ — Built Different**. Incluye:

- 🛍️ Página principal de marca + catálogo
- ⚡ **Fulfillment MRP** — pedidos pendientes, BOM consolidado, plan por proveedor, acciones (WhatsApp / email / PO PDF)
- 🔍 **B2B Sourcing** — comparador en vivo de 7 proveedores mexicanos + calculadora unitaria
- 📐 Sistema de diseño TOMASQ v4: lime `#D4FF00`, fondos `#141416 / #1c1c1f / #26262a`, texto `#f5f5f2 / #c8c8c2`

El sitio es **100% estático** (HTML + CSS y JS inline) — cero build step.

---

## Estructura

```
.
├── index.html                   # Versión vigente (TOMASQ v4)
├── tomasq-v4.html               # Copia idéntica a index.html (referencia)
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

| Ruta              | Sirve                  |
| ----------------- | ---------------------- |
| `/`               | `index.html` (v4)      |
| `/v4`             | `index.html` (v4)      |
| `/v3`             | `tomasq-v3.html`       |

---

## Conectar con backend real (scraping + n8n)

La UI tiene `mock data`. Para conectar a producción reemplaza los handlers
(`sendWhatsApp`, `generatePO`, `sendAllPO`) con llamadas a tu webhook de n8n:

```js
async function sendAllPO(orderId) {
  await fetch('https://guillermocantuu.app.n8n.cloud/webhook/po-send', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ orderId, plan: currentPlan }),
  });
}
```

Arquitectura completa (Postgres schema, scrapers Python, workflow n8n,
endpoints FastAPI) en [`tomasq-sourcing-backend.md`](./tomasq-sourcing-backend.md).
