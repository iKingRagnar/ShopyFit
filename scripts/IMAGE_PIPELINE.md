# Image generation pipeline — Toro Kaizen

Brand-coherent product mockups via Google Gemini Flash Image (a.k.a. nano-banana).
Replaces / augments the CSS-filter color preview that ships today (PR #14).

## Status (2026-04-29)

| Component | State | Notes |
|---|---|---|
| `~/.claude/settings.json` MCP entry | ✅ configured | `nanobanana-mcp` registered with the user's Google AI key |
| `@ycse/nanobanana-mcp` npm package | ✅ pre-cached | Verified arrives in `~/.npm/_npx/` |
| `~/.claude/skills/seo-image-gen/SKILL.md` | ✅ installed | Skill is callable as `claude-seo:seo-image-gen` |
| `scripts/gen_product_images.py` | ✅ committed | Direct REST script, bypasses MCP |
| Image generation | ⛔ **blocked: needs billing** | Free tier does not include `gemini-3.1-flash-image-preview` |

## The blocker

Running `gen_product_images.py` returns:

```
HTTP 429
"Quota exceeded for metric: generate_content_free_tier_requests,
 limit: 0, model: gemini-3.1-flash-image"
```

`limit: 0` is the smoking gun — the model is **not in the free tier at all**.

## Fix (one-time, ~3 minutes)

1. Open <https://aistudio.google.com/billing>
2. Either link an existing Google Cloud billing account, or create one (Google offers $300 free credit on first signup)
3. Make sure your existing API key (the one already in `settings.json`) is associated with the billed project
4. Re-run:

```bash
cd ~/ShopyFit
GOOGLE_AI_API_KEY="$(jq -r '.mcpServers["nanobanana-mcp"].env.GOOGLE_AI_API_KEY' ~/.claude/settings.json)" \
  python3 scripts/gen_product_images.py smoke
```

Expected: a single PNG saved to `assets/products/TQ-TEE-GBLK-black.png`.

If the smoke test succeeds, generate the full batch:

```bash
GOOGLE_AI_API_KEY="$(jq -r '.mcpServers["nanobanana-mcp"].env.GOOGLE_AI_API_KEY' ~/.claude/settings.json)" \
  python3 scripts/gen_product_images.py all
```

## Cost estimate

| Model | Per-image | Full batch (~32 images) |
|---|---|---|
| `gemini-3.1-flash-image-preview` | ≈ $0.020 | **≈ $0.64** |
| `imagen-4.0-generate-001` (alternative) | ≈ $0.040 | ≈ $1.28 |

Sub-coffee territory. Don't overthink it.

## What the script does

1. Iterates the `CATALOG` list (8 SKUs mirroring `index.html`)
2. For each SKU × color in its colorways, builds a brand-coherent prompt:
   - `PROMPT_TEMPLATE` — references Aimé Leon Dore / Kith / Patta editorial photography
   - `GARMENT_DESC[shape]` — cut and framing per garment type (jogger / hoodie / tee / tank / shorts / cap / set)
   - `COLOR_DESC[color]` — descriptive name (e.g. "deep matte black", "muted olive green")
3. POSTs to `models/gemini-3.1-flash-image-preview:generateContent` with `responseModalities: ["TEXT","IMAGE"]`
4. Decodes the `inlineData.data` base64 → writes PNG to `assets/products/{sku}-{color}.png`
5. Skips files that already exist (idempotent — safe to rerun)
6. Sleeps 0.4s between calls to be a polite API citizen

## Wiring images into the storefront

After generation, each `.pc` card in `index.html` should declare per-color attributes:

```html
<div class="pc"
     data-sku="TQ-JOG-PHN"
     data-shape="jogger"
     data-img="assets/products/TQ-JOG-PHN-black.png"
     data-img-black="assets/products/TQ-JOG-PHN-black.png"
     data-img-gray="assets/products/TQ-JOG-PHN-gray.png"
     data-img-olive="assets/products/TQ-JOG-PHN-olive.png">
```

`applyPcColor()` (already shipped in PR #14) reads `data-img-{c}` first and only falls back to the CSS filter if the attribute is missing. Drop the URLs in and the swatch click swaps to a real photo automatically — zero new code.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 429 with `limit: 0` | Free tier blocker | Enable billing (above) |
| 429 with `limit: N` | Hit per-minute rate cap | Increase `time.sleep` in the script |
| 400 BadRequest | Prompt rejected by safety filter | Check the failing entry, soften wording |
| Empty `inlineData` | Model returned text only | Re-run; if persistent, switch to `imagen-4.0` |
| Style is off-brand | Prompt drift across runs | Pin a single seed garment description, regenerate as set |

## Catalog reference

Hardcoded in `scripts/gen_product_images.py`:

| SKU | Garment | Colorways |
|---|---|---|
| `TQ-TEE-GBLK` | tee | black · white · gray · navy |
| `TQ-TANK-STR` | tank | black · white · lime |
| `TQ-SHORT-OBS` | shorts | black · navy · olive · gray · red |
| `TQ-SET-TITAN` | set | black · navy |
| `TQ-TEE-GWHT` | tee | black · white · gray |
| `TQ-JOG-PHN` | jogger | black · gray · olive |
| `TQ-HOOD-VOID` | hoodie | black · gray · purple |
| `TQ-SET-VENOM` | set | black · purple · lime |

**Total: 30 images.** Adjust the catalog in the script to match catalog growth.

## Path back to "free"

If billing is a hard no, alternatives:

1. **Manually source Unsplash photos per color** — same `data-img-{color}` wiring, just hand-picked URLs. Less consistent visually.
2. **Stick with CSS filters (PR #14)** — the recolor-on-click already works without any photos at all. It's a solid 80% solution.
3. **Wait for a real photoshoot** — when the brand has model + garments, drop URLs into the same attribute slots.

The infrastructure is identical for all three paths — `applyPcColor()` only cares whether `data-img-{color}` exists.
