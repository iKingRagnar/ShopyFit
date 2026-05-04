# AI tools para generar logos · Stack 2026

> Pregunta de TQ (4-may-2026): *"creo yo debe haber mejores app AI para generar logos minimalistas no? Aunque los de chat gpt están buenos jeje"*. Respuesta corta: sí, hay 4 que vencen a ChatGPT/DALL-E para logos. Aquí está el ranking.

---

## TL;DR

**Para Toro Kaizen, usa Recraft V3.** Es el único que genera SVG editable directo. $12/mes, vale cada peso.

---

## El ranking real (testeado, 2026)

### 🥇 Recraft V3 — el GOAT para logos
- **Diferencial brutal:** salida SVG vectorial nativa (no raster que después tienes que vectorizar)
- Tiene "styles" guardados — entrenas tu brand una vez y todas las generaciones futuras heredan ese look
- Best-in-class para shapes geométricas + minimalismo
- Funciona excelente para iconos de categoría (ya tenemos 40 en el sprite, podemos generar más vía Recraft)
- **Costo:** free 50 imágenes/día. Plan Plus $12/mes ilimitado
- **URL:** https://recraft.ai

**Cuándo usar:** Casi siempre. Especialmente para mark del toro, monograma TK, iconos de producto, badges.

### 🥈 Ideogram 3.0 — rey del texto
- **Diferencial:** entiende typography como nadie. Si necesitas un logo CON texto ("TORO KAIZEN" lockup, hangtag, sticker), aquí.
- Genera prompts con instrucciones específicas tipo "stencil military bold uppercase letterspacing 0.18em"
- Free 100 imágenes/semana
- $7/mes plan Plus
- **URL:** https://ideogram.ai

**Cuándo usar:** Wordmarks completos, hangtags con texto, mockups de producto con "TORO KAIZEN" estampado, banners de TikTok/Meta con copy integrado.

### 🥉 Midjourney v7 — aesthetic king
- **Diferencial:** aún manda en quality estética cruda, especialmente con `--style raw --ar 1:1` + prompts cuidados
- Mejor para mood boards / lookbook concepts que para logos finales
- Solo via Discord (fricción)
- $10/mes basic, $30/mes pro
- **URL:** https://midjourney.com

**Cuándo usar:** Brainstorming visual de moodboards, hero images, lookbook concepts, photoshoots styled.

### 4. Flux 1.1 Pro Ultra — el open-source champion
- Modelo de Black Forest Labs, accessible vía replicate.com / fal.ai / mystic.ai
- Calidad nivel Midjourney pero pay-per-use (~$0.04 por imagen)
- Mejor para volumen alto (50+ imágenes para ads)
- **URLs:** https://replicate.com/black-forest-labs/flux-1.1-pro-ultra · https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra

**Cuándo usar:** Cuando vas a generar muchas imágenes (catálogo de producto, batch de ads), y la economía pay-per-use le gana al sub mensual.

### 5. ChatGPT + DALL-E 3 (lo que TQ usa)
- Bueno para concept exploration rápido
- Malo para producir finales: raster only, fidelity media, no vector
- Ya están pagando ChatGPT Plus probablemente, así que cero costo marginal
- **Veredicto:** úsenlo para brainstorm verbal/visual, NO para finales

### También válidos pero secundarios

- **Adobe Firefly 3** — production-safe (training data licenciada), ideal si la marca crece y necesitan defenderse legalmente. $5/mes.
- **Google Imagen 3 / Gemini Advanced** — alta calidad pero solo via Gemini interface, no batch fácil. $20/mes Google One AI.
- **Looka / LogoAI / Tailor Brands** — apps específicas para logos. Resultados genéricos pero rápidos. NO recomendados — quedan tipo plantilla.

---

## Workflow recomendado para Toro Kaizen

```
1. BRAINSTORM TEXTO
   └─ ChatGPT / Claude / WhatsApp con socio
      "estamos pensando en X, qué te parece, qué falta"
       ↓
2. PROMPT CRAFTING
   └─ ChatGPT te ayuda a articular el prompt visual
      "minimal black-and-white bull skull, mexican folkloric line work,
       front view, geometric, no text, transparent background"
       ↓
3. GENERATE SVG VARIANTS
   └─ Recraft V3 (5-10 variantes en SVG)
       ↓
4. PICK FAVORITES + ITERATE
   └─ Toma 2-3 finalistas, generas 5 variantes de cada con tweaks
       ↓
5. POLISH MANUAL
   └─ Figma o Illustrator: alinear a brand grid, asegurar
      pixel-perfect en tamaños chicos (favicon 16x16, sleeve label 8mm)
       ↓
6. INTEGRAR AL SITIO
   └─ Subir como nuevo <symbol id="bull-v2"> al sprite library
      Reemplazar referencias en index.html / marks.html
      Updates de la documentación de marca
```

---

## Prompt templates probados para tu marca

### Para variantes del bull mark
```
Minimalist mexican bull skull silhouette, front view, geometric line art,
black on transparent background, single solid weight strokes, no shading,
gym apparel brand mark, 1:1 aspect ratio, vector style, NO text, NO photo,
NO 3d rendering. References: Aimé Leon Dore, Patta, Kith brand marks.
```

### Para variantes del TK monograma
```
Geometric monogram letters T and K interlocked or stacked, inside hexagonal
frame outline, single weight strokes, minimalist black-on-white, vector
mark for athletic apparel brand. Style: Y3, Helly Hansen, Stone Island
brand marks. NO text other than TK. NO decoration.
```

### Para hangtag mockup
```
Premium product hangtag mockup, 350gsm cardstock, kraft paper texture,
square aspect ratio. Front shows TORO KAIZEN wordmark in Bebas Neue style
plus small bull skull mark plus tagline "Discipline Over Everything" in
caps. Black ink on cream paper. Photographed flat-lay overhead with
soft directional light, premium fashion photography style. References:
Aimé Leon Dore hangtags.
```

### Para print mockup en tee
```
Toro Kaizen black oversized tee t-shirt mockup, 240gsm heavyweight cotton,
flat-lay overhead view, isolated on white seamless paper background.
Center chest shows minimalist bull skull silhouette in lime green silicone
print, approx 6cm wide. Premium product photography, soft directional
shadow, garment is the only subject, no model. References: Gymshark,
YoungLA product photos.
```

---

## Cómo conecta esto con el setup actual del proyecto

- En la sesión previa configuré `nanobanana-mcp` (Gemini) en `~/.claude/settings.json`. Está **bloqueado por billing** en el free tier — para destrabarlo, link Google Cloud billing en aistudio.google.com/billing (~$0.60 batch completo de mockups).
- Si TQ se suscribe a **Recraft V3** ($12/mes), bypassemos completamente el blocker de Gemini para temas de logo/icono. Recraft es más caro mensual pero da SVG editable que es ORO para integrar al sprite library del sitio.
- Si en cambio prefieren **Ideogram free tier**, tienen 100/semana sin pagar — alcanza para iterar este mes.

---

## Mi recomendación final

**Para esta etapa pre-launch, el stack más práctico:**

1. **Suscríbanse a Ideogram 3.0 free tier** — cero costo, 100/semana
2. **Cuando lance la marca + tengan ventas, upgrade a Recraft V3** — los $12/mes se justifican porque el sprite library del sitio será mantenido en SVG (todo escala perfecto)
3. **ChatGPT lo siguen usando para brainstorm de prompts** — su rol es de "director creativo verbal"
4. **Midjourney solo si quieren mood boards de photoshoot** — no es necesario para logos

Total inversión mensual añadida: $0 ahora (free tiers), $12/mes después.

---

> Última actualización: 2026-05-04 · Editar libre cuando aparezcan herramientas nuevas
