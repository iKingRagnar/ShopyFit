#!/usr/bin/env python3
"""
Generate brand-coherent product mockups for TORO KAIZEN via Gemini Flash Image API.

Usage:
  GOOGLE_AI_API_KEY=... python3 gen_product_images.py [sku-slug | all]

The catalog mirrors the 8 product cards in index.html. Each entry declares
its garment shape + colorways. We render one PNG per (product, color) pair
into assets/products/{sku}-{color}.png.

The prompts encode:
  - clean studio photography (no model, white/cream background)
  - chest-area bull logo print
  - editorial fashion photography aesthetic
  - garment-specific cut details (tapered jogger, oversized tee, etc.)

Cost: ~$0.02/image on gemini-3.1-flash-image-preview. Full batch (~30 images)
~$0.60. Cheap insurance vs paying for a real photoshoot.
"""
from __future__ import annotations
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

API_KEY = os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    sys.exit("GOOGLE_AI_API_KEY env var required")

MODEL = "gemini-3.1-flash-image-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "products"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ───── Color → photoreal description ─────
COLOR_DESC = {
    "black": "deep matte black",
    "white": "off-white cream tone",
    "gray": "heather gray melange",
    "navy": "deep navy blue",
    "olive": "muted olive green",
    "red": "burgundy red",
    "purple": "deep aubergine purple",
    "lime": "neon lime green accent",
}

# ───── Garment-specific cut + framing ─────
GARMENT_DESC = {
    "tee": (
        "an oversized boxy short-sleeve t-shirt with crew neckline, drop-shoulder seams, "
        "and slightly extended hem. Heavyweight 240 gsm combed cotton fabric, visible texture. "
        "Garment is laid flat from a slight overhead angle, gently arranged with no folds, "
        "sleeves spread naturally"
    ),
    "tank": (
        "an athletic stringer tank top with deep armholes, sleek racing back, ribbed crew neckline. "
        "Performance fabric with subtle sheen. Shown from the front, laid flat on a clean surface"
    ),
    "hoodie": (
        "an oversized pullover hoodie with kangaroo front pouch pocket, adjustable drawstring hood "
        "with metal-tipped cords, ribbed cuffs and hem. Heavyweight 380 gsm fleece-lined cotton. "
        "Shown three-quarter view with the hood gently structured"
    ),
    "jogger": (
        "tapered-fit jogger pants with elasticated drawstring waistband, side seam pockets, "
        "elastic ankle cuffs. French terry cotton fabric with visible texture. "
        "Shown in a flat-lay overhead view, legs arranged side-by-side, drawstring loosely tied"
    ),
    "shorts": (
        "athletic 5-inch inseam shorts with elasticated drawstring waistband, side mesh pockets. "
        "Lightweight performance polyester. Shown laid flat from above"
    ),
    "cap": (
        "a low-profile baseball cap with structured 6-panel crown, pre-curved brim, "
        "self-fabric strap with metal closure. Subtle washed cotton twill texture. "
        "Shown from a slight three-quarter front angle"
    ),
    "set": (
        "a matching two-piece athletic co-ord set: cropped pullover hoodie on top + tapered "
        "joggers below, both in the same fabric and color. Shown together as a flat-lay outfit, "
        "hoodie above joggers, like a complete outfit composition"
    ),
}

# ───── Catalog: mirrors the 8 cards in index.html ─────
CATALOG = [
    {"sku": "TQ-TEE-GBLK",  "name": "Tee Gothic Black",       "shape": "tee",    "colors": ["black", "white", "gray", "navy"]},
    {"sku": "TQ-TANK-STR",  "name": "Tank Stringer Bravio",   "shape": "tank",   "colors": ["black", "white", "lime"]},
    {"sku": "TQ-SHORT-OBS", "name": "Short Obsidian 5in",     "shape": "shorts", "colors": ["black", "navy", "olive", "gray", "red"]},
    {"sku": "TQ-SET-TITAN", "name": "Set Titan Edition",      "shape": "set",    "colors": ["black", "navy"]},
    {"sku": "TQ-TEE-GWHT",  "name": "Tee Gothic White",       "shape": "tee",    "colors": ["black", "white", "gray"]},
    {"sku": "TQ-JOG-PHN",   "name": "Jogger Phantom Toro",    "shape": "jogger", "colors": ["black", "gray", "olive"]},
    {"sku": "TQ-HOOD-VOID", "name": "Hoodie Void Mortal",     "shape": "hoodie", "colors": ["black", "gray", "purple"]},
    {"sku": "TQ-SET-VENOM", "name": "Set Venom Compresion",   "shape": "set",    "colors": ["black", "purple", "lime"]},
]

PROMPT_TEMPLATE = (
    "Editorial product photography for premium athletic apparel brand TORO KAIZEN "
    "(Mexican strength + Japanese kaizen aesthetic, dark minimalist brand identity). "
    "Subject: {color_desc} {garment_desc}. "
    "The chest / front of the garment shows a small subtle bull-head silhouette logo print, "
    "discreet and contrast-toned, no text. "
    "Photographic style: high-end studio lighting, soft directional shadows, clean off-white "
    "seamless paper background, no model, no human, just the garment. "
    "Composition: garment is the only subject, centered, fills 75% of frame, "
    "tasteful negative space around. Sharp focus, natural fabric texture and weave visible, "
    "neutral color grading. 4:5 vertical aspect ratio. "
    "Aesthetic references: Aimé Leon Dore lookbook, Kith product page, Patta editorial. "
    "No watermark, no text overlay, no price tag visible."
)


def build_prompt(shape: str, color: str) -> str:
    return PROMPT_TEMPLATE.format(
        color_desc=COLOR_DESC[color],
        garment_desc=GARMENT_DESC[shape],
    )


def gen_one(prompt: str) -> bytes | None:
    """POST to Gemini, return PNG bytes or None on failure."""
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"  ERR: {e}")
        return None
    # Extract first inlineData (PNG/JPEG bytes) from the response
    cands = data.get("candidates") or []
    for c in cands:
        for p in c.get("content", {}).get("parts", []):
            inline = p.get("inlineData") or p.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    print(f"  no image in response: {json.dumps(data)[:300]}")
    return None


def gen_for_sku(entry, only_color: str | None = None) -> int:
    n = 0
    for color in entry["colors"]:
        if only_color and color != only_color:
            continue
        out = OUT_DIR / f"{entry['sku']}-{color}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"  ✓ {out.name} (already exists, skip)")
            continue
        prompt = build_prompt(entry["shape"], color)
        print(f"  → generating {out.name} …", end=" ", flush=True)
        img = gen_one(prompt)
        if img:
            out.write_bytes(img)
            print(f"saved ({len(img):,} bytes)")
            n += 1
        else:
            print("FAILED")
        time.sleep(0.4)  # be nice to the API
    return n


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    only_color = sys.argv[2] if len(sys.argv) > 2 else None
    if target == "all":
        total = 0
        for entry in CATALOG:
            print(f"\n[{entry['sku']}] {entry['name']} — {entry['shape']}")
            total += gen_for_sku(entry, only_color)
        print(f"\n=== Done. {total} new images generated. ===")
    elif target == "smoke":
        # Single sanity check
        entry = CATALOG[0]
        print(f"Smoke test: {entry['sku']} (black)")
        gen_for_sku(entry, only_color="black")
    else:
        entry = next((e for e in CATALOG if e["sku"] == target), None)
        if not entry:
            sys.exit(f"unknown sku {target}; valid: {[e['sku'] for e in CATALOG]}")
        gen_for_sku(entry, only_color)


if __name__ == "__main__":
    main()
