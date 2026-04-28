# ShopyFit · Ops AI Backend (FastAPI)

Servicio Python que respalda al `dashboard.html` del front. Se despliega como
**un segundo servicio en Railway**, dejando el sitio estático intacto.

## Endpoints

| Método | Ruta                          | Qué hace                                                                |
| ------ | ----------------------------- | ----------------------------------------------------------------------- |
| GET    | `/health`                     | Health check + estado de la API key                                     |
| POST   | `/api/ai-advisor`             | Chat con Claude (`claude-sonnet-4-6`)                                   |
| POST   | `/api/recommendations/apply`  | Marca una recomendación como aplicada                                   |
| POST   | `/api/fifo/suggest-reorder`   | Calcula cantidad de reorden (velocidad × lead time + safety)            |
| POST   | `/api/pricing/apply`          | Actualiza precio de un SKU                                              |
| POST   | `/api/suppliers/requote`      | Lanza el flujo de auto-recotización                                     |

## Local (desarrollo)

```bash
cd api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # y edita ANTHROPIC_API_KEY
export $(grep -v '^#' .env | xargs)
uvicorn main:app --reload --port 8001
```

Health check:
```bash
curl http://localhost:8001/health
```

Probar Claude:
```bash
curl -X POST http://localhost:8001/api/ai-advisor \
  -H 'content-type: application/json' \
  -d '{"prompt":"¿Qué SKU está perdiendo dinero esta semana?"}'
```

## Deploy en Railway (segundo servicio)

1. **Railway dashboard** → tu proyecto → **+ New** → **GitHub Repo** → selecciona `ShopyFit` (el mismo repo).
2. En el servicio nuevo, **Settings** → **Source** → **Root Directory**: `api`.
3. **Variables**:
   - `ANTHROPIC_API_KEY` (obligatoria)
   - `ALLOWED_ORIGINS` = la URL pública de tu front (ej. `https://shopyfit-production.up.railway.app`). Se aceptan varias separadas por coma.
4. **Networking** → **Generate Domain** (puerto auto = `$PORT`).
5. Railpack detecta `requirements.txt` + `Procfile` y arranca con `uvicorn`.

Cuando ya tengas la URL pública, ponla en el `dashboard.html` (constante `API_BASE` al inicio del `<script>`).

## Migrar mocks → real

Por ahora los endpoints `recommendations/apply`, `fifo/suggest-reorder`,
`pricing/apply` y `suppliers/requote` devuelven respuestas hardcoded.
Sustituye los `# TODO:` cuando conectes Postgres (Neon/Railway/Supabase).

## Stack

- **FastAPI 0.115** — async-friendly, validación Pydantic
- **Anthropic SDK 0.39** — Claude Sonnet 4.6 (modelo más reciente disponible)
- **Uvicorn** — server ASGI
