# Plan de video · ropa en modelo

> TQ pidió videos de cómo se vería la ropa puesta. Aquí lo honesto + el camino real.

## La verdad sin adornos

**No puedo generar video fotorrealista de ropa en un modelo desde aquí.** Eso requiere un API de video-gen, todos de pago, ninguno con free tier que sirva:

| Plataforma | Calidad | Costo | API |
|---|---|---|---|
| **Runway Gen-4** | Top tier | ~$0.05/seg (~$0.50 por clip 10s) | Sí, requiere key |
| **Kling AI 2.0** | Excelente, barato | ~$0.30/clip | Sí (PiAPI/fal.ai) |
| **Google Veo 3** | Top, audio incluido | ~$0.40/clip | Vía Gemini (mismo billing bloqueado) |
| **Pika 2.0** | Bueno | ~$0.25/clip | Sí |
| **Sora (OpenAI)** | Top | Plan ChatGPT Pro $200/mes | Limitado |
| **Hailuo / MiniMax** | Bueno, barato | ~$0.20/clip | Sí (fal.ai) |

## El flujo realista (cuando tengan budget)

1. **Generar imagen base** del producto en modelo (Pollinations free, o Midjourney/Recraft)
2. **Image-to-video** con Kling o Runway: subes la foto, prompt "model walking, subtle camera movement, gym lighting" → clip 5-10s
3. **Costo real:** ~$0.30-0.50 por clip. 10 clips de producto = ~$3-5 USD total
4. **Mejor relación calidad/precio 2026:** Kling 2.0 vía fal.ai (~$0.30/clip, calidad casi Runway)

## Lo que SÍ está activo ahora (gratis)

- **Pollinations.ai** (FLUX) genera imágenes de producto brand-perfect en el navegador del cliente. Ya wireado en los 3 hero SKUs con prompts dark+red. Cero costo, cero key.
- Cuando carguen el sitio, las imágenes se generan client-side (~3-5s primera vez, luego cache).

## Recomendación

**Fase 1 (ahora):** Pollinations para imágenes estáticas. Suficiente para validar.

**Fase 2 (cuando vendan):** Suscripción Kling AI o fal.ai (~$10-20 USD/mes) → generan 30-50 clips de producto en movimiento. Yo armo el script de generación batch (como gen_product_images.py pero para video) cuando tengan la key.

**Fase 3 (con tracción real):** Photoshoot/videoshoot real con modelo. Nada le gana a producto real en cuerpo real. ~$8-15K MXN una sesión cubre todo el catálogo.

## Lo que necesito de TQ/ustedes para Fase 2

1. Cuenta en fal.ai o Kling (free signup, después pay-as-you-go)
2. API key
3. Yo escribo `scripts/gen_product_videos.py` que toma las imágenes de producto y las anima

> Sin API key de video, lo máximo es imagen estática (que ya está). No hay forma gratis de video AI fotorrealista en 2026.
