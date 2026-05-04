# Inversión mensual · TORO KAIZEN

> Documento de trabajo para socios. Estimaciones en MXN, basadas en mercado mexicano DTC (Direct-to-Consumer) athletic apparel a abril 2026. Editar libre — esto es la base, no el evangelio.

---

## TL;DR — los 3 escenarios

| Escenario | Inversión inicial (one-time) | Operación mensual | Cuando usar |
|---|---|---|---|
| **🌱 Bootstrap** | ~$30,000 MXN | **~$15,000 MXN/mes** | Probar producto/mercado con riesgo mínimo |
| **🚀 Realista** | ~$60,000 MXN | **~$45,000 MXN/mes** | Lanzar serio con ramp-up controlado (recomendado) |
| **⚡ Agresivo** | ~$120,000 MXN | **~$110,000 MXN/mes** | Escalar rápido, ya hay validación |

**Inversión inicial en partes iguales (50/50 socios):**
- Bootstrap: $15,000 c/u
- Realista: $30,000 c/u ← *recomendado para arrancar*
- Agresivo: $60,000 c/u

---

## 1. Tech / infraestructura digital

### Lo que ya está cubierto (gratis o ya pagado)
| Item | Estado | Ahorro vs alternativa |
|---|---|---|
| **Diseño web completo** | ✅ Hecho con Claude (~12 PRs merged) | $40,000-80,000 MXN one-time |
| **Branding** (logo, paleta, sistema visual) | ✅ Hecho | $15,000-30,000 MXN |
| **Hosting Railway tier hobby** | ✅ Activo | — |
| **Dominio actual** `shopyfit-production.up.railway.app` | ✅ subdominio gratis | — |
| **Skills + plugins de Claude Code** | ✅ Sin costo extra | — |

### Costos mensuales recurrentes

| Item | Bootstrap | Realista | Agresivo | Notas |
|---|---|---|---|---|
| Railway hosting | $0 (free) | $400 ($20 USD pro) | $400 | Free funciona hasta ~10K visitas/mes |
| Dominio `.mx` | $30 | $30 | $30 | $300 MXN/año amortizado |
| Email business (Google Workspace) | $0 | $280 (2 users × $140) | $280 | Solo si quieren `@torokaizen.mx` |
| Email transaccional (Resend) | $0 (3K free) | $0 | $400 | Para confirmaciones de orden |
| WhatsApp Business API | $0 | $0 | $200 | Negligible al inicio |
| Mailchimp / lista email | $0 | $200 | $400 | Hasta 500 contactos free |
| AI APIs (Gemini, OpenAI) | $0 | $200 | $800 | Para gen imágenes, copy auto |
| Analytics (Plausible) | $0 (GA4 free) | $180 | $180 | Plausible es premium pero privacy-friendly |
| Cloudflare CDN | $0 | $0 | $0 | Free tier alcanza |
| Stripe / MercadoPago | comisión por venta (~3.6% + $3 MXN) | — | — | No fijo |
| **Subtotal tech** | **$30** | **$1,290** | **$2,690** | |

---

## 2. Producción / inventory

### Costo unitario por prenda (proveedores MX)

| Prenda | Costo producción | PVP sugerido | Margen unitario |
|---|---|---|---|
| Tee oversize 240gsm + bull print | $180-260 MXN | $699 MXN | ~$440 MXN |
| Tank stringer | $140-200 MXN | $549 MXN | ~$370 MXN |
| Hoodie 380gsm fleece | $380-480 MXN | $899 MXN | ~$460 MXN |
| Jogger french terry | $280-380 MXN | $849 MXN | ~$510 MXN |
| Shorts performance | $180-260 MXN | $649 MXN | ~$420 MXN |
| Set completo | $580-720 MXN | $1,199 MXN | ~$540 MXN |
| Cap | $90-150 MXN | $399 MXN | ~$270 MXN |

**Margen promedio mezclado:** ~$430 MXN/unidad (~55%)

### Producción mensual

| | Bootstrap | Realista | Agresivo |
|---|---|---|---|
| Unidades nueva producción | 30 piezas | 100 piezas | 250 piezas |
| Costo prom × $300 MXN | $9,000 | $30,000 | $75,000 |
| Hangtag + bolsa polibag | +$500 | +$1,800 | +$4,500 |
| **Subtotal producción** | **$9,500** | **$31,800** | **$79,500** |

---

## 3. Marketing / paid acquisition

### Distribución mensual

| Canal | Bootstrap | Realista | Agresivo |
|---|---|---|---|
| Meta Ads (FB/IG) | $3,000 | $8,000 | $25,000 |
| TikTok Ads | $0 | $4,000 | $15,000 |
| Google Ads (search brand) | $0 | $1,500 | $5,000 |
| Influencer micro (1-2 colabs/mes) | $0 | $3,000 | $10,000 |
| Content creator UGC | $0 | $1,500 | $5,000 |
| **Subtotal marketing** | **$3,000** | **$18,000** | **$60,000** |

**ROAS objetivo:** 3.5× (por cada $1 en ads, $3.50 en ventas). Significa que $18K marketing realista debería generar ~$63K en ventas → ~140 unidades vendidas → $60K margen.

---

## 4. Operativo / logística

| Item | Bootstrap | Realista | Agresivo |
|---|---|---|---|
| Empaque custom (sticker, tarjeta thank-you) | $300 | $1,500 | $4,500 |
| Subsidio envío (free shipping +$799) | $1,000 | $5,000 | $15,000 |
| Fulfillment (si no en casa) | $0 | $0 | $4,500 |
| Customer service (asistente part-time) | $0 | $3,500 | $8,000 |
| **Subtotal operativo** | **$1,300** | **$10,000** | **$32,000** |

---

## 5. Legal / fiscal MX

| Item | Costo | Frecuencia |
|---|---|---|
| RFC personal o SAS | $0 | One-time |
| Acta constitutiva SAS de RL de CV | $5,000-15,000 | One-time |
| Registro marca IMPI (1 clase ropa) | $2,800 | One-time |
| Registro marca IMPI (clase 35 retail) | $2,800 | One-time |
| Cuenta business (BBVA, Banamex, Mercado Pago Empresa) | $0-500 | One-time |
| Contador / contabilidad básica | $1,500-3,000 | **Mensual** |

| | Bootstrap | Realista | Agresivo |
|---|---|---|---|
| Contador mensual | $1,500 | $2,500 | $4,500 |
| Otros (servicios pro) | $0 | $0 | $1,500 |
| **Subtotal legal** | **$1,500** | **$2,500** | **$6,000** |

---

## Resumen mensual

| Categoría | Bootstrap | Realista | Agresivo |
|---|---|---|---|
| 1. Tech / infra | $30 | $1,290 | $2,690 |
| 2. Producción | $9,500 | $31,800 | $79,500 |
| 3. Marketing | $3,000 | $18,000 | $60,000 |
| 4. Operativo | $1,300 | $10,000 | $32,000 |
| 5. Legal / fiscal | $1,500 | $2,500 | $6,000 |
| **Total mensual** | **$15,330** | **$63,590** | **$180,190** |
| **Por socio (50/50)** | **$7,665** | **$31,795** | **$90,095** |

> Nota: el **realista** tiene producción cargada porque incluye restock para crecer. Si arrancan con la producción inicial cubierta del one-time, los meses 2-4 son más cerca de $40K/mes y suben con la demanda.

---

## Inversión inicial (one-time)

### Lo crítico antes de lanzar

| Item | Bootstrap | Realista | Agresivo | Notas |
|---|---|---|---|---|
| Producción inicial (sample + 1ª tanda) | $15,000 | $30,000 | $60,000 | 50-200 unidades |
| Photoshoot (modelo + foto + edición) | $0 (DIY) | $12,000 | $30,000 | Esencial para Meta Ads |
| Registro marca IMPI (2 clases) | $5,600 | $5,600 | $5,600 | Crítico legal |
| Acta constitutiva SAS | $0 (RFC personal) | $8,000 | $15,000 | Recomendable mes 3-6 |
| Diseño packaging (cajas, hangtags físicos) | $1,000 | $3,000 | $8,000 | |
| Imprevistos / buffer | $5,000 | $10,000 | $20,000 | |
| **Total one-time** | **$26,600** | **$68,600** | **$138,600** |
| **Por socio (50/50)** | **$13,300** | **$34,300** | **$69,300** |

---

## Proyección de ventas — punto de equilibrio

### Realista escenario, mes a mes

| Mes | Inversión acum. socios c/u | Unidades vendidas | Ventas brutas | Margen bruto | Net (margen − ops) |
|---|---|---|---|---|---|
| 1 | $34,300 + $32,000 = $66K | 30 | $21,000 | $13,000 | -$50,000 (lanzamiento) |
| 2 | $32,000 | 70 | $50,000 | $30,000 | -$33,000 |
| 3 | $32,000 | 130 | $90,000 | $56,000 | -$7,000 |
| 4 | $32,000 | 180 | $125,000 | $77,000 | **+$14,000** ← break-even mensual |
| 5 | $32,000 | 240 | $165,000 | $103,000 | +$40,000 |
| 6 | $32,000 | 300 | $210,000 | $130,000 | +$67,000 |

**Break-even del proyecto completo (recuperar inversión inicial):** ~mes 9-12 con escenario realista bien ejecutado.

---

## Recomendaciones operativas

### Empezar **Bootstrap** o **Realista**

- **Bootstrap** ($7,665/mes c/u): para validar mercado con riesgo controlado. 30 piezas iniciales, $3K MXN ads/mes, casi todo manual. Si vende: escalas a Realista. Si no vende en 60 días: pausan sin perder mucho.
- **Realista** ($31,795/mes c/u): si ya tienen confianza en el producto y quieren ramp-up serio. Producción de 100 piezas/mes, $18K ads, photoshoot pro. Es la curva sana.
- **Agresivo**: solo si validan tracción en mes 1-2 con bootstrap. NO arrancar aquí — quema capital sin data.

### Lo que pueden cubrir con tiempo en vez de plata

- **Customer service** los primeros 3 meses: ustedes mismos por WhatsApp Business
- **Fulfillment**: empacar en casa hasta 100+ órdenes/mes
- **Content creation**: foto con celular bien iluminado + reels propios = $0 vs contratar
- **Comunidad / orgánico**: Instagram + TikTok + WhatsApp groups gratis pero brutalmente time-intensive
- **Email copy + ads copy**: con AI ya cubierto (Claude/ChatGPT)

### Reglas del 50/50

1. **Aporte inicial** parejo (one-time)
2. **Mensualidad operativa** parejo OR ajuste por hours-worked si uno mete más tiempo
3. **Utilidades a repartir** después de cubrir todos los costs + reservar 20% para crecimiento
4. **Reserva de inventory:** mínimo 2x ventas mensuales en stock

---

## Lo que YO ya cubrí en este proyecto (sin costo extra)

Para que tu socio entienda qué se ahorraron:

| Trabajo | Valor mercado MX | Estado |
|---|---|---|
| Diseño UX/UI completo (e-commerce + landing) | $30K-60K | ✅ Hecho |
| Sistema de marca (logo bull, kanji 改善, paleta) | $15K-25K | ✅ Hecho |
| Carrito real con persistencia + free-ship bar | $8K-15K | ✅ Hecho |
| Mobile responsive completo | $5K-12K | ✅ Hecho |
| SEO técnico + schema + PWA + a11y | $10K-20K | ✅ Hecho |
| 7 SVG silhouettes apparel + sistema fallback | $4K-8K | ✅ Hecho |
| Pipeline de generación de imágenes IA | $3K-6K | ✅ Listo (necesita billing $0.60) |
| Manifesto + página de marcas + chatbot | $5K-10K | ✅ Hecho |
| **Total ahorrado en desarrollo** | **$80,000-156,000 MXN** | |

Ese ahorro es la mejor "inversión inicial" que ya hicieron sin saberlo.

---

## Próximos pasos sugeridos

1. **Reunión de socios** con este doc abierto + decidir tier (Bootstrap o Realista)
2. **Cotización formal de proveedor** de producción (3 maquilas en Aguascalientes/MTY/CDMX)
3. **Registro IMPI** de marca esta semana ($5,600 inversión protege todo)
4. **Apertura de cuenta business** + contador → semana 2
5. **Primera tanda producción** → semana 3-4
6. **Photoshoot + lanzamiento ads** → semana 5-6
7. **Open for orders** → semana 7-8

Total tiempo desde "go" hasta primera venta: ~8 semanas.

---

> Última actualización: 2026-04-29 · Editar libre. Esto es base para conversar, no para tatuarse.
