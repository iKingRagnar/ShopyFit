# Scroll-Morph Videos — Prompt Templates

> 4 videos AI-generados que producen el efecto "scroll-morph" en TORO KAIZEN.
> Stack: ChatGPT (refinar prompts) → Nano Banana 2 (frames start/end) → Veo 3.1 (morph 8s).
> Costo total estimado: ~$15 USD · ~40 min de tu tiempo.

## Workflow general (mismo para los 4)

1. **Frame inicial:** busca/genera la imagen de inicio (Nano Banana 2 si necesitas algo custom).
2. **Frame final:** pásale a ChatGPT la imagen inicial + descripción del estado final → ChatGPT te devuelve un prompt para Nano Banana 2 → en Google AI Studio (modelo `nano-banana-2`, 2K resolution, thinking máximo) generas la imagen final.
3. **Veo prompt:** dale las 2 imágenes a ChatGPT pidiéndole un prompt segundo a segundo para Veo 3.1.
4. **Generar video:** Google AI Studio modelo `veo-3.1`, formato vertical, 8s, 4K, sube SOLO la imagen inicial, pega prompt, run.
5. **Drop el .mp4** en `assets/morphs/<id>.mp4` (los nombres están en cada sección abajo).
6. Commit + push → Railway redeploya → el video aparece live.

---

## 1️⃣ Hero · `assets/morphs/hero-bull-to-athlete.mp4`

**Frame inicial:** Logo del toro de TORO KAIZEN (silueta lime sobre fondo cream o negro liso, centrado, vista frontal).

**Frame final:** Atleta hombre 25-30 años, complexión atlética, estampa Tee Gothic Black con el logo del toro al pecho, fondo gym crudo (concrete + iluminación dramática lateral), pose lateral, mirando al frente.

**Prompt para ChatGPT (start → end):**
```
Tengo una imagen de un logo de toro (cabeza frontal, lime sobre fondo neutro) y necesito una imagen final del mismo símbolo TRANSFORMADO en un atleta vistiendo una camiseta oversize negra con ese exact logo del toro estampado en lime al pecho. El atleta debe estar en un gimnasio con paredes de concreto, iluminación lateral dramática (key light derecha, fill suave izquierda), pose lateral 3/4, mirando hacia la cámara. Mismo encuadre vertical, mismo centro, misma proporción. Calidad fotorrealista 4K, grano filmico sutil, paleta cream + lime + carbón.
```

**Prompt Veo 3.1:**
```
Vertical 9:16, 8 seconds, 4K. Cinematic morph between two states.

0.0-1.5s: Bull head logo (lime on cream/black bg) breathes subtly, slight pulse.
1.5-3.0s: Logo's outline starts dissolving into particle dust that swirls upward.
3.0-5.0s: Particles reform into the silhouette of a male athlete, pose locking in 3/4 lateral.
5.0-6.5s: Detail materializes — oversized black tee with lime bull logo at chest, concrete gym wall fades in behind.
6.5-8.0s: Final beat — athlete fully formed, dramatic side lighting kicks on, slight camera push-in. Subtle bull-mark watermark glints lime in bottom-right corner.

Mood: powerful, premium, "Built Different". No text overlays. No music — let the visual breathe.
```

---

## 2️⃣ Drop · `assets/morphs/drop-stamp.mp4`

**Frame inicial:** Tela de algodón cruda blanca/cream, doblada de manera minimalista sobre superficie de madera oscura, vista cenital.

**Frame final:** Misma tela, ahora estampada con el logo del toro lime + texto "BUILT DIFFERENT" debajo, ahora visible plano y colocada como prenda terminada (camiseta extendida).

**Prompt ChatGPT (start → end):**
```
Tengo una imagen de tela cruda de algodón blanco doblada minimalista sobre madera oscura, vista cenital. Necesito generar la imagen final donde esa tela ya es una camiseta oversize extendida plana, color black, con el logo del toro TORO KAIZEN estampado en lime al centro del pecho y el texto "BUILT DIFFERENT" en Bebas Neue debajo. Mismo encuadre cenital, misma luz, misma superficie de madera. Fotorrealista, 4K, paleta cream + lime + carbón.
```

**Prompt Veo 3.1:**
```
Vertical 9:16, 8 seconds, 4K. Top-down product transformation.

0.0-1.0s: Raw white cotton fabric, folded minimally, soft side light from camera-left.
1.0-2.5s: Fabric unfolds itself in stop-motion choreography, edges crisp into oversized tee shape.
2.5-4.0s: Tee turns from raw white to black via a "dye dip" effect that ripples across the surface.
4.0-5.5s: Lime bull-mark stamp drops from above, lands at chest center with a subtle dust burst.
5.5-7.0s: "BUILT DIFFERENT" text materializes letter-by-letter in Bebas Neue below the bull.
7.0-8.0s: Final hold — tee perfectly flat, cinematic top-down shot, single golden-hour highlight on the lime stamp.

No people. No text overlays beyond the BUILT DIFFERENT print itself. Stay top-down throughout.
```

---

## 3️⃣ Fabric → Garment · `assets/morphs/fabric-to-garment.mp4`

**Frame inicial:** Bobina de algodón peinado 30/1 industrial, hilo crudo enrollado en spool de madera, vista lateral, taller textil mexicano de fondo (fuera de foco).

**Frame final:** Camiseta Tee Gothic terminada, colgada en perchero de madera, etiqueta TORO KAIZEN visible en cuello, mismo taller de fondo (ahora con producto terminado).

**Prompt ChatGPT (start → end):**
```
Tengo una imagen de bobina de hilo de algodón peinado 30/1 sobre spool de madera, vista lateral, taller textil mexicano fuera de foco al fondo (Aguascalientes vibe — paredes ladrillo, máquinas vintage). Necesito la imagen final donde esa bobina ya se transformó en una camiseta oversize negra Tee Gothic colgada en perchero de madera, con etiqueta tejida TORO KAIZEN en el cuello visible. Mismo taller de fondo pero ahora con producto terminado en primer plano. Fotorrealista, 4K, iluminación cálida tarde mexicana.
```

**Prompt Veo 3.1:**
```
Vertical 9:16, 8 seconds, 4K. Documentary "from raw to ready" transformation.

0.0-1.5s: Cotton spool spinning slowly, single thread feeding off the side. Mexican textile workshop in soft bokeh background.
1.5-3.0s: Thread accelerates, weaving itself in mid-air into a fabric panel that drops down.
3.0-4.5s: Fabric is "cut" by invisible scissors leaving a clean tee silhouette outline. The piece flips and rotates 90° to face camera.
4.5-6.0s: Tee dyes black via wave from left to right, crisp not muddy.
6.0-7.0s: Tee rises onto a wooden hanger that materializes. Woven label "TORO KAIZEN" stitches itself onto the inner collar.
7.0-8.0s: Final hold — finished tee on hanger, warm Mexican afternoon sun raking from camera-left, dust motes in air.

Hands-free transformation (no humans visible). Workshop ambient stays soft-focus throughout.
```

---

## 4️⃣ Manifesto · `assets/morphs/toro-kaizen-juntos.mp4`

**Frame inicial:** Toro embistiendo (silueta lime contra fondo negro absoluto), pose 3/4 dinámica, polvo lime suspendido alrededor sugiriendo movimiento.

**Frame final:** Atleta unisex de pie en pose serena, frente a kanji 改善 enorme detrás (lime sobre negro), una mano sobre el pecho donde lleva el logo del toro estampado, mirando al frente.

**Prompt ChatGPT (start → end):**
```
Tengo una imagen de un toro embistiendo, silueta lime sobre fondo negro absoluto, polvo lime alrededor sugiriendo carga. Necesito la imagen final donde la energía del toro se "asienta" en un atleta unisex de pie, pose serena con mano sobre el pecho, mirando al frente. Detrás de la persona el kanji 改善 (Kaizen) gigante en lime contra el mismo negro absoluto. Mismo encuadre vertical, mismo centro, misma paleta lime + negro. Fotorrealista cinematográfico, mood premium meditativo.
```

**Prompt Veo 3.1:**
```
Vertical 9:16, 8 seconds, 4K. Philosophical 3-state morph.

0.0-2.0s: TORO STATE — Bull silhouette in mid-charge, lime particles streaking off the horns, raw kinetic energy. Black void background.
2.0-3.5s: Bull form deconstructs into floating lime particles that swirl in a controlled spiral. The kanji 改善 begins materializing from the dust, large and centered.
3.5-5.0s: KAIZEN STATE — Particles fully resolve into the kanji 改善 in lime. Gentle pulse, like breathing. Background stays pure black.
5.0-6.5s: Kanji's bottom strokes extend downward, becoming the silhouette of an athlete standing in front of it.
6.5-8.0s: JUNTOS STATE — Athlete fully formed, hand on chest where bull mark glows lime, kanji 改善 huge behind. Single rim light from above. Dust settles. Hold.

Reverent, slow, ceremonial. No text overlays. No music suggestions — pure visual.
```

---

## ✅ Checklist post-generación

Por cada video:
- [ ] Descargar el `.mp4` desde Google AI Studio
- [ ] Renombrar al filename exacto (ej: `hero-bull-to-athlete.mp4`)
- [ ] Mover a `assets/morphs/` en el repo
- [ ] Verificar que pesa <30MB (si pesa más, comprime con `ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4`)
- [ ] `git add assets/morphs/<file>.mp4 && git commit -m "morph: add <name>" && git push`
- [ ] Railway redeploya → live

## 🔍 Si algo no se ve bien

| Problema | Solución |
|---|---|
| Video carga pero no morph al scroll | El placeholder se queda — revisa que el `.mp4` tenga duración válida (`ffprobe -i video.mp4`) |
| Video se ve estirado en mobile | Asegúrate de exportar 9:16 vertical (1080x1920 o 2160x3840) |
| Carga lento | Comprime con CRF 28-30, o usa `-preset slow` para mejor compresión |
| Salta entre frames bruscamente | El video tiene frame rate bajo. Re-render a 30fps mínimo |
| Cache del navegador no toma el nuevo video | Versiona el filename: `drop-stamp-v2.mp4` y actualiza el `<source>` |

## 📦 Compresión recomendada

```bash
# Calidad alta (~12MB para 8s 4K vertical):
ffmpeg -i raw.mp4 -vcodec libx264 -crf 23 -preset slow -movflags +faststart morphs/hero-bull-to-athlete.mp4

# Si pesa demasiado:
ffmpeg -i raw.mp4 -vcodec libx264 -crf 28 -preset slow -vf "scale=1080:1920" -movflags +faststart morphs/hero-bull-to-athlete.mp4
```

`-movflags +faststart` mueve los metadatos al inicio → el video puede empezar a reproducirse antes de descargar todo.

---

> Última actualización: 2026-04-28 · Pattern aplicado en `index.html` (3 morphs) + `manifesto.html` (1 morph).
