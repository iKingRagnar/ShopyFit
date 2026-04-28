"""ShopyFit · Ops AI backend (FastAPI).

Deploy as a separate Railway service pointing at the `api/` directory.
Frontend (root /) stays as a static site; this service serves /api/* and is
called from `dashboard.html` via fetch.
"""
from __future__ import annotations

import os
from typing import Any

from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ALLOWED_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if o.strip()
]

app = FastAPI(title="ShopyFit Ops AI", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

claude = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


# ───────── schemas ─────────

class ChatBody(BaseModel):
    prompt: str
    context: dict[str, Any] | None = None


class ApplyRecBody(BaseModel):
    rec_id: str


class ReorderBody(BaseModel):
    sku: str


class PriceBody(BaseModel):
    sku: str
    price: float


# ───────── health ─────────

@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "claude_configured": claude is not None,
        "allowed_origins": ALLOWED_ORIGINS,
    }


# ───────── AI Advisor ─────────

SYSTEM_PROMPT = """Eres el AI Advisor de TOMASQ, una marca mexicana de ropa
deportiva premium. Hablas español natural, das recomendaciones accionables
y concretas (con números cuando aplique). Eres directo, no hagas listas
largas: 2-4 frases por respuesta. No inventes métricas que no te dieron."""


@app.post("/api/ai-advisor")
def ai_advisor(body: ChatBody) -> dict[str, Any]:
    if claude is None:
        raise HTTPException(503, "ANTHROPIC_API_KEY not configured")

    ctx = ""
    if body.context:
        ctx = f"\n\nContexto del negocio (JSON):\n{body.context}"

    msg = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": body.prompt + ctx}],
    )
    reply = "".join(b.text for b in msg.content if b.type == "text")
    return {"reply": reply, "model": msg.model, "usage": msg.usage.model_dump()}


# ───────── Recommendations / actions ─────────
# Stubs: replace with real DB queries when Postgres is wired.

REC_RESPONSES = {
    "tank-15": "Descuento 15% Tank Tops · activo martes 18-22h",
    "shipping-799": "Envío gratis subido a $799",
    "giveaway-titan": "Giveaway Set Titan lanzado en IG",
    "bundle-tee-short": "Bundle Tee+Short $999 activo",
    "recovery-38": "Recovery flow disparado · 38 carritos",
    "reorder-hoodie": "PO Hoodie Void enviada · Maquila GZ · 60u",
    "reactivate-gold": "142 cupones Gold enviados (-15%, 7d)",
}


@app.post("/api/recommendations/apply")
def apply_recommendation(body: ApplyRecBody) -> dict[str, Any]:
    msg = REC_RESPONSES.get(body.rec_id, "Recomendación aplicada")
    # TODO: persist apply event in Postgres (audit log)
    return {"ok": True, "message": msg, "rec_id": body.rec_id}


# ───────── FIFO inventory ─────────

@app.post("/api/fifo/suggest-reorder")
def suggest_reorder(body: ReorderBody) -> dict[str, Any]:
    # TODO: read sales velocity + lead time from Postgres
    velocity_per_day = 4.1
    lead_time_days = 12
    safety_stock_days = 7
    suggested = round(velocity_per_day * (lead_time_days + safety_stock_days))
    return {
        "sku": body.sku,
        "suggested_qty": suggested,
        "supplier": "Maquila GZ",
        "eta_days": lead_time_days,
        "rationale": (
            f"Velocidad {velocity_per_day}/d × ({lead_time_days}+{safety_stock_days})d "
            f"= {suggested}u"
        ),
    }


# ───────── Pricing ─────────

@app.post("/api/pricing/apply")
def apply_price(body: PriceBody) -> dict[str, Any]:
    # TODO: write to products table + emit price-change event
    return {"ok": True, "sku": body.sku, "new_price": body.price}


# ───────── Suppliers ─────────

@app.post("/api/suppliers/requote")
def requote_suppliers() -> dict[str, Any]:
    # TODO: loop active suppliers and trigger your scraper / cotización flow
    return {
        "ok": True,
        "in_queue": 14,
        "improvements_detected": 3,
        "summary": "14/14 cotizaciones recibidas · 3 mejoras detectadas",
    }
