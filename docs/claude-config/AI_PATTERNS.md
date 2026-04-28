# AI Agent Patterns — Catálogo reusable

> Patrones extraídos de sistemas multi-agente complejos en producción
> (e-commerce con 400-500 mensajes/día, ventas automatizadas, multi-canal).
> Aplica en n8n, Make, FastAPI, Cloud Functions, Agent SDK, etc.

---

## 1. Multi-agent router (1 cerebro + N especialistas)

**Problema:** un solo prompt gigante con todas las instrucciones de venta termina mal. Los modelos pierden foco, alucinan, mezclan etapas.

**Solución:**
```
Webhook
  ↓
Router agent (GPT5-mini / Haiku)  ← 1 sola decisión: "step1|step2|step3|step4"
  ↓ structured output (JSON)
  ├──► Specialist agent A (etapa: descubrimiento)
  ├──► Specialist agent B (etapa: catálogo)
  ├──► Specialist agent C (etapa: cotización)
  └──► Specialist agent D (etapa: cierre)
```

**Reglas:**
- El router **no responde al usuario**, solo enruta. Output mínimo posible (`step2`).
- Cada specialist tiene **un solo trabajo**, prompt corto, herramientas mínimas.
- Modelo del router puede ser barato (Haiku/GPT5-mini). Los specialists usan modelos más fuertes solo donde aplica.
- **Memoria compartida** (Postgres) entre todos los agentes vía `memory_id` (ej: número de teléfono).

**Cuándo no hacerlo:** ≤ 3 estados / preguntas simples. Aquí sobra.

---

## 2. Message buffering — agrupar ráfagas (Redis ventana 50s)

**Problema:** los usuarios envían 4 mensajes seguidos: "Hola", "¿cuánto?", "el rojo", "envío?". Sin buffer respondes 4 veces, gastas 4x tokens y respondes mal a contexto roto.

**Solución:**
```
Mensaje entrante
  ↓
Push a Redis list (ttl 50s) ← acumula bajo memory_id
  ↓
Wait 50s (timer único por usuario)
  ↓
Pop todos los mensajes de Redis  →  unirlos por ", "  →  enviar al agente
```

**Implementación clave:**
- Cada mensaje resetea el timer (debounce, no throttle)
- TTL de la list 50s para que no acumule basura si el usuario abandonó
- Borrar la list **después** del pop para no duplicar en la próxima ráfaga

**Resultado:** 4 mensajes → 1 turno → 1 respuesta coherente.

---

## 3. Cadena de seguimientos escalonados (1h → 3h → 5h → 24h)

**Problema:** usuario deja de responder a media venta. Sin follow-up pierdes la venta. Con follow-up demasiado pronto, espantas.

**Solución (un sub-flow por etapa del funnel):**
```
Trigger (cuando agente responde algo "anclable")
  ↓
Wait 1h  →  ¿última msg en memoria es la del agente? → SI: send follow-up #1
  ↓
Wait 3h  →  misma pregunta sobre follow-up #1 → SI: send #2
  ↓
Wait 5h  →  misma pregunta → SI: send #3
  ↓
Wait 24h →  marcar como "perdido" + activar template-flow del CRM (cold cadence)
```

**Pieza clave:** después de enviar cada follow-up, **insertar manualmente ese mensaje en la memoria** para que el siguiente check (¿la última msg es la mía?) funcione.

**Variantes por etapa:**
- Etapa 1 (descubrimiento): mensajes amistosos, "sigues por aquí?"
- Etapa 4 (cotización lista): mensajes con descuento progresivo, urgencia ("te quedan 7 días de promo")

---

## 4. Detección de intent de pago (PDF + imagen)

**Problema:** distinguir entre "captura de pago" vs "stickers / fotos random / catálogos enviados por curiosidad".

**Solución 2-stage:**
```
Imagen entrante
  ↓
¿Es PDF?  →  SÍ:
  - asume pago (95%+ accuracy en e-commerce real)
  - notifica humano (Telegram)
  - mueve lead a etapa "pendiente confirmar pago"
  - manda mensaje según horario laboral
  
  →  NO (es imagen):
  ├─► Stage 1: ¿es captura de transferencia? (Vision API)
  │     SÍ → mismo flow del PDF
  │     NO → continúa
  └─► Stage 2: ¿identificas un producto del catálogo? (Vision API)
        SÍ → guarda producto detectado, agente comenta el diseño
        NO → eleva a humano (sticker, foto random, no parseable)
```

**Por qué no usar IA para todos los PDFs:** costo. 1 de cada 50 PDFs es no-pago. No vale la pena gastar API por todos cuando el FP es bajo y barato (humano confirma).

---

## 5. Working hours awareness

**Problema:** mandar "muchas gracias por tu pago, lo verifico ahora" a las 3am genera desconfianza ("¿es estafa? no hay nadie revisando").

**Solución:**
```js
// Code node simple, no IA
const now = new Date().toLocaleString("en-US", {timeZone: "America/Mexico_City"});
const hour = new Date(now).getHours();
const inHours = hour >= 9 && hour < 19;  // 9am-7pm

// Mensaje A: "Estamos verificando tu pago" (in hours)
// Mensaje B: "Recibimos tu pago, revisamos en horario 9-19" (out of hours)
```

**Aplica también para:** sugerir esperar al hablar con humano, calibrar urgencia de respuesta, ajustar tono.

---

## 6. Human handoff (Telegram group)

**Cuándo escalar a humano:**
- Imagen no reconocible (ni pago ni producto)
- Pregunta fuera del scope ("¿pueden adelantar el pedido 1 semana?")
- Quejas / amenazas / lenguaje agresivo
- Petición especial fuera del flow (descuento custom, cambio de logística)

**Implementación mínima:**
```
Trigger (uno de los casos arriba)
  ↓
1. Mover lead a etapa "atención humana" (CRM stops automation)
2. Notify Telegram group con: customer_name, last_msg, image_url, link_al_chat
3. Send a customer: "Una compa te contesta en breve" (in hours)
   o: "Te respondemos mañana en horario" (out of hours)
```

**Group de Telegram con bot incluido** = todo el equipo ve el caso, cualquiera responde.

---

## 7. División de respuesta en 3 partes (humanización)

**Problema:** una IA respondiendo todo en un párrafo gigante se siente robot.

**Solución:** prompt al agente: "tu respuesta DEBE estar dividida en 3 mensajes separados por `|||`. Cada mensaje debe sentirse natural si lo leo solo."

```
Agent output:
"Hola María! 👋 Qué padre que estés organizando tu boda 🎉|||Para que veamos los productos, necesito saber: ¿es para 50, 100 o 200 invitados?|||También cuéntame qué fecha tienes pensada y el código postal donde lo enviaríamos."
```

Después en el flow:
```
Split por "|||"  →  for each:
  send_message(part)
  wait 1.5s
```

**Resultado:** conversación se siente humana sin escribir 3 prompts ni 3 turnos del agente.

---

## 8. Detection of "extra question" tras catálogo

**Problema:** usuario dice "muéstrame sandalias y short, y por cierto ¿dónde están ubicados?". Si tu agent solo está preparado para mostrar imágenes, ignora la pregunta.

**Solución:**
```
Agent A (catálogo): genera array de productos a mostrar
  ↓
Loop: para cada producto, send images + PDFs + dynamic text
  ↓
[al terminar el loop]
Agent B (intent classifier): "¿quedó alguna pregunta sin responder en el msg original?"
  - SÍ → redirige al Agent D (preguntas generales) con contexto del msg original
  - NO → fin del turn
```

---

## 9. Calculadora deterministica (NO IA)

**Problema:** cotización con 12 productos, cada uno con peso, divididos en cajas con límite de peso, costo de envío variable. Si lo hace IA, alucina números.

**Solución:** código puro en un Code node con todas las restricciones embebidas.

```js
// pseudo-código
const PRODUCTS = {sandalias:{peso:120, max_per_box:50}, ...};
const BOX_LIMIT_KG = 25;

function calcShipping(items) {
  let totalKg = items.reduce((a,b) => a + (PRODUCTS[b.sku].peso * b.qty), 0);
  let boxes = Math.ceil(totalKg / 1000 / BOX_LIMIT_KG);
  let cost = boxes * 300;  // $300 MXN por caja
  return { boxes, cost };
}
```

**El agente solo invoca la función como tool**, no calcula. 100% determinístico, 0 errores.

**Aplica para:** cotizaciones, cálculo de impuestos, conversión de unidades, scoring de leads, descuentos por volumen.

---

## 10. Markers especiales para acciones del flow

**Problema:** quieres que el agente envíe un PDF en ciertos momentos sin sumar otro agente.

**Solución low-tech:**
- Prompt al agente: "cuando el usuario pida métodos de pago, termina tu respuesta con `.com 1 2 3`."
- En el flow: `if response contains ".com 1 2 3" → send_attachment(payment_methods.pdf)`.

Otro ejemplo: `Facebook reviews` keyword → manda screenshot de FB. `Show calendar` → manda imagen del calendario.

**Por qué funciona:** el agente queda con su prompt limpio. La complejidad la maneja el flow. Cero llamadas extra al modelo.

---

## 11. Scoping vars across alternate paths (n8n / DAG-based platforms)

**Problema (específico de n8n / Make / cualquier DAG):** tienes un nodo que toma var de "nodo X". Si la ejecución pasó por un branch alternativo donde X **no se ejecutó**, la var falla.

**Solución pragmática:** **duplicar la rama** del DAG. Tienes los mismos nodos finales 2 veces, uno por cada path posible. Las vars **siempre** existen porque cada copia tiene sus propios precedentes.

```
   ┌── path A → [setupA] ──┐
in ─┤                       ├── (NO conviene unir aquí)
   └── path B → [setupB] ──┘
                            
   ┌── path A → [setupA] → [respondA] (copia)
in ─┤                                         
   └── path B → [setupB] → [respondB] (copia)
```

Sí, es feo. Sí, funciona el 100% de las veces sin sorpresas con vars rotas.

**No aplica en:** SDK code (TypeScript/Python) donde tienes control de scopes vía variables explícitas.

---

## 12. Tag executions para debugging post-hoc

**Problema:** flow corre miles de veces al día. Algo falla. Buscar la ejecución correcta entre miles es infierno.

**Solución:** asigna **tags** a las ejecuciones desde dentro del flow.

```js
// n8n / SDK equivalente
$execution.metadata.tags = [
  "atencion", "etapa-3", "phone-+5215512345678", "lead-id-9821"
];
```

Después puedes filtrar:
```
GET /executions?tags=etapa-3,phone-+5215512345678
```

Ver: por qué este lead no avanzó, qué prompt vio el agente, qué decidió.

**Da un valor extra al cliente:** sus operadores también filtran por tags para casos puntuales.

---

## 13. "Desinterés detector" para parar follow-ups

**Problema:** usuario respondió "no me interesa, está caro". Si sigue tu cadena de follow-ups quedas como spammer.

**Solución:**
```
Tras enviar cotización + 24h sin compra:
  Lee últimos 7 mensajes del usuario.
  Pasa a un agente clasificador (Haiku / cheap):
    Q: "¿hay desinterés explícito? (caro / no me gusta / lo descarté / no insistan)"
    A: yes / no
  
  yes → marca lead como "perdido" + para todos los follow-ups
  no  → continúa con cadence normal
```

**Por qué 7:** suficiente contexto para detectar el shift, no tanto como para gastar tokens en mensajes irrelevantes viejos.

---

## 14. Stripe-like sales notification

**UX win:** cada venta detectada → notificación instantánea al dueño/equipo:

```
🟢 NUEVA VENTA — $4,950 MXN
👤 María González — +5215512345678
📦 50 sandalias + 30 cilindros + envío MX
🕐 hace 2 min · ver chat
```

Vía Telegram bot, Slack webhook, o push notification. Da la dopamina del "Shopify ka-ching" pero conectado a tu pipeline custom.

---

## 15. CRM event hygiene

**Anti-pattern:** dejar el agente respondiendo después de que ya cerró la venta o se elevó a humano.

**Pattern:**
- Cada cambio de etapa **bloquea/desbloquea** el agente.
- Etapas habilitadas para IA → un IF al inicio del flow filtra antes de cualquier API call.
- Etapas no-IA → solo notify humano, no procesa.

```
Webhook
  ↓
Get current stage of lead
  ↓
IF stage in [discovery, catalog, quoted, follow-up]:
  → continue with AI flow
ELSE:
  → notify human, drop execution
```

---

## ✅ Cuándo importa cada patrón

| Tu sistema… | Patrones críticos |
|---|---|
| Pequeño (1-2 agentes, baja escala) | 2 (buffering), 4 (payment intent), 6 (handoff) |
| E-commerce / ventas multi-etapa | TODOS — especialmente 1, 3, 4, 8, 13 |
| Soporte técnico | 1 (router), 6 (handoff), 12 (tags) |
| Reservas / agendamiento | 9 (calculadora deterministica), 5 (working hours), 7 (humanización) |
| Contenido / creative | 1 (router por estilo), 11 (scoping), 14 (notifications) |

---

## 16. Scroll-morph videos (frontend AI showcase)

**Problema:** páginas web genéricas se reconocen al instante como AI-slop. Para verse "premium agency" necesitas algo que llame la atención sin ser cringe.

**Solución:** efecto donde el `currentTime` de un `<video>` se ata al progreso de scroll del usuario. El usuario "controla" la animación con el mouse-wheel/dedo. Combinado con videos AI-generados que muestran un estado A → estado B (ej: bull mark → atleta usando la prenda), el efecto se siente high-budget.

**Stack de generación:**
1. **Frame inicial** — imagen real o generada con Nano Banana 2 (Google AI Studio)
2. **Frame final** — ChatGPT genera prompt para Nano Banana 2 que crea el end frame
3. **Veo 3.1 prompt** — ChatGPT genera prompt segundo-a-segundo para el morph 8s, vertical, 4K
4. **Generar video** en Google AI Studio
5. **Embed** con HTML5 `<video>` + JS scroll listener

**JS pattern (vanilla):**
```js
function initScrollMorph(section){
  const video = section.querySelector('video');
  video.muted = true; video.playsInline = true; video.preload = 'auto';
  let ticking = false;
  function onScroll(){
    if(ticking)return; ticking=true;
    requestAnimationFrame(()=>{
      const rect = section.getBoundingClientRect();
      const total = rect.height - window.innerHeight;
      const progress = Math.max(0, Math.min(1, -rect.top / total));
      if(video.duration) video.currentTime = progress * video.duration;
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
}
```

**HTML structure:**
```html
<section class="scroll-morph"><!-- height: 240vh -->
  <div class="scroll-morph-sticky"><!-- position: sticky; top:0; height:100vh -->
    <h2>Tu copy</h2>
    <video muted playsinline preload="auto">
      <source src="/morphs/hero.mp4" type="video/mp4">
    </video>
  </div>
</section>
```

**Costo aprox por video:** ~$3 USD (1 imagen Nano Banana + 1 video Veo). Total página de 4 morphs: ~$15.

**Cuándo NO hacerlo:**
- Audiencia tiene conexión lenta (videos pesan 10-30MB cada uno)
- Mobile-first crítico con rendimiento estricto (la decode de video frames cuesta CPU)
- Sitios institucionales serios (banks, gov) — el efecto se siente pop

**Cuándo SÍ:**
- E-commerce premium (apparel, beauty, design)
- Landing pages de SaaS con producto visual
- Brand storytelling pages (manifesto, drop announcement)
- Portfolios creativos

**Pitfalls comunes:**
- Olvidar `muted` y `playsinline` → mobile no autoplay
- No usar `requestAnimationFrame` → scroll choca con jank
- Videos con frame rate bajo (24fps) se ven "saltados" cuando scrolleas rápido — exporta 30fps+
- No `+faststart` en metadata → video tarda en empezar a render

**Aplicación en TORO KAIZEN:** 4 morphs ya cableados en index.html (hero, drop, fabric→garment) + manifesto.html (toro→改善→juntos). Ver `docs/claude-config/MORPH_VIDEOS.md` para los prompts exactos.

---

> Inspirado en sistemas reales de e-commerce mexicano con n8n + WhatsApp Business API + Postgres + Telegram.
> Aplica en cualquier orquestador (n8n, Make, Pipedream, Temporal, Inngest, Cloudflare Workflows, Anthropic Agent SDK).
