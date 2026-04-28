# Claude Code · Token Optimization Playbook

> Guía operativa para reducir el consumo de tokens en Claude Code en 90%+
> sin perder calidad de respuesta. Aplicable a Claude Code en CLI, IDE
> (VS Code / Cursor / Windsurf), Cloud Desktop y la web.

---

## 0. Fundamentos: cómo te cobra Claude

| Concepto | Detalle |
|---|---|
| **Token** | Unidad mínima que el modelo lee y procesa (≈ 1 palabra en español, menos en inglés) |
| **Contexto acumulativo** | Cada mensaje **relee TODA** la conversación previa. No es lineal — crece con cada turno |
| **Cache de prompts** | Anthropic guarda contexto **5 min**. Después de 5 min ocioso → re-procesa todo |
| **Costo del contexto invisible** | `CLAUDE.md`, MCPs conectados, system prompts, archivos adjuntos: **todos cuentan** aunque no los veas |

> **Regla mental:** Mensaje 1 ≈ 500 tokens. Mensaje 30 ≈ 15,000+ tokens. La curva es **multiplicativa**, no lineal.

---

## 1. Elegir el modelo correcto (impacto: 40-70% de ahorro)

| Modelo  | Cuándo usarlo                                                   |
| ------- | ---------------------------------------------------------------- |
| **Opus** | Planificación, decisiones críticas, arquitectura, "no errors allowed" |
| **Sonnet** | Coding general, refactor, análisis. Default polivalente |
| **Haiku** | Formateo, respuestas cortas, tareas mecánicas |

**Setup óptimo (Plan-mode con Opus, todo lo demás Sonnet):**
```bash
# Dentro del IDE / terminal de Claude Code:
/model opus plan
# Output: "set model to opus in plan mode, sonnet otherwise"
```

**Setup en Claude Desktop:** dropdown abajo a la derecha → cambia según la tarea.

---

## 2. Planear antes de implementar (impacto: 30-50% en proyectos largos)

**Anti-patrón:** "Hazme un e-commerce con MRP y dashboard." → Claude implementa, te das cuenta a la mitad que algo está mal, re-prompts, gastas 5x más.

**Patrón correcto:**
1. `/create-plan <objetivo>` — Claude escribe `plan.md` con stack, orden, dependencias
2. **Tú lees el plan, iteras** sobre el `.md` hasta que esté perfecto
3. `/implement` — sólo entonces escribe código

Estructura típica del workspace:
```
project/
├── plans/
│   ├── feature-A.md   # plan iterado antes de implementar
│   └── feature-B.md
├── CLAUDE.md
└── src/
```

---

## 3. Limpiar contexto entre tareas (impacto: 50-80% al cambiar de tema)

```bash
/clear   # comienza sesión nueva con contexto vacío
```

**Cuándo:**
- Terminaste feature A y empiezas feature B sin relación
- La conversación pasó de 50 mensajes y vas a hacer algo nuevo
- Sentís que las respuestas empiezan a degradar

**Casi nadie lo hace.** Ejecutarlo a tiempo te ahorra cantidades absurdas de tokens.

---

## 4. Un prompt bien armado > 5 separados (impacto: 30%)

**Anti-patrón:**
```
> Investiga sobre X
[espera respuesta - 2k tokens]
> Guarda eso en la base de datos
[espera respuesta - 4k tokens, recargó el primero]
> Mándame un mensaje de Slack al terminar
[respuesta - 7k tokens, recargó los anteriores]
```
Total: ~13k tokens por contexto compuesto.

**Patrón correcto:**
```
> 1) Investiga sobre X.
  2) Guarda los datos relevantes en la tabla `research`.
  3) Dispara un mensaje en #notifs cuando termines.
```
Total: ~5k tokens. Un solo turno, un solo cargado de contexto.

**Caveat:** algunas tareas se benefician de separarlas (cuando una depende del output exacto de la anterior). Usa juicio — pero **por defecto, agrupa**.

---

## 5. Medir lo que gastas (impacto: te da claridad para optimizar)

```bash
/context   # muestra desglose: system prompt, herramientas, MCPs, memoria, mensajes
/usage     # uso acumulado de la sesión actual
```

Output típico de `/context`:
```
Total session:        11%
  System prompt        3.5%
  Tools (built-in)     3.9%
  Memory files         2.6%
  Skills               XX%
  MCP servers          XX%
  Messages             XX%
```

Si ves que **MCP servers** o **Memory files** está alto sin usarse → optimiza esos primero.

---

## 6. Desconectar MCPs que no usas (impacto: 5-30% según cuántos tengas)

Cada MCP server conectado **carga su lista de tools en el system prompt** aunque no lo uses. Si tienes 8 MCPs y sólo usas 2 en este proyecto → estás pagando por 6 que no necesitas.

**En Claude Desktop:** Settings → Connectors → desactiva los que no uses.

**En Claude Code (CLI):**
```bash
claude mcp list                   # ve qué tienes
claude mcp remove <name> -s user  # quita user-scope
# o usa enabledMcpjsonServers en settings.json para filtrar por proyecto
```

**Estrategia:** mantén user-scope sólo lo "siempre útil" (ej: codebase-memory, context7).
MCPs específicos (Firecrawl, Playwright, Taskmaster) → activa por proyecto via `.mcp.json`.

---

## 7. CLAUDE.md preciso (impacto: 10-25% en cada turno)

`CLAUDE.md` se **inyecta en cada turno**. Si tiene 800 líneas, son 800 líneas multiplicadas por todos tus mensajes.

**Anti-patrón:** dump de toda la doc del proyecto + ejemplos + historial.

**Patrón correcto:**
```markdown
# Project XYZ

## Stack
- Next.js 14 + Tailwind + Supabase

## Estructura
- `src/app/` — App Router
- `src/components/` — UI
- `src/lib/` — utilidades + clientes Supabase

## Convenciones
- Server actions en `src/actions/`
- Tipo `Database` generado en `src/lib/database.types.ts`

## Comandos
- `pnpm dev`, `pnpm build`, `pnpm test`

## Cuando necesites contexto profundo de X
Lee `docs/X.md` o búscalo via codebase-memory.
```

**Regla:** si dudas si una línea pertenece, **fuera**. Pon detalles en archivos separados que Claude lea bajo demanda.

---

## 8. La cache es de 5 minutos (impacto: enorme si trabajas en bursts)

Anthropic cachea tu contexto durante **5 min de inactividad**. Si trabajas, paras 7 min, vuelves → re-paga todo el contexto desde cero.

**Mitigación:**
```bash
/compact   # resume la conversación, libera contexto sin perder hilo
/clear     # corta limpio si vas a parar mucho
```

**Patrón "voy a almorzar":**
```bash
/compact   # comprime antes de irte
# (vuelves 1h después)
# La conversación sigue, pero el contexto ahora es 1/5 del tamaño
```

---

## 9. Skills que comprimen output (impacto: 30-65%)

Algunas skills modifican **cómo responde** Claude para usar menos palabras manteniendo el sentido.

**Ejemplo: `caveman` skill** — Claude responde como cavernícola: "skill = file. carga sesion. front cloud carga." Reduce ~65% de tokens en respuestas largas.

```bash
# Activar en sesión:
> activate caveman skill
```

**Cuándo usar:** sesiones de exploración rápida, prototipo, debugging cuando no necesitas prosa pulida.

**Cuándo NO:** documentación, comunicación con stakeholders, código que va a producción (los comentarios quedan raros).

---

## 10. Bonus: stack de tooling extra

| Tool | Para qué |
|---|---|
| `/context` + `/usage` (built-in) | Saber dónde se va el contexto |
| **Token cost auditor skill** | Audita tu workspace y lista qué optimizar (Nexum Academy gratis) |
| **`disabledMcpjsonServers`** en `settings.json` | Apaga MCPs específicos por proyecto sin desinstalar |
| **Archivos `.cursorignore` / `.claudeignore`** | Excluye carpetas del contexto auto-leído (node_modules, dist, etc.) |
| **`/rewind`** | Vuelve atrás N turnos sin perder el plan, libera contexto futuro |

---

## 📊 Tabla de prioridad (esfuerzo vs impacto)

| # | Método | Esfuerzo | Impacto |
| - | ------ | -------- | ------- |
| 1 | `/clear` entre tareas no relacionadas | Cero | Alto |
| 2 | Fusionar prompts relacionados | Bajo | Medio |
| 3 | CLAUDE.md mínimo (≤100 líneas) | Medio | Alto |
| 4 | `/model opus plan` (Opus solo plan-mode) | Cero | Alto |
| 5 | Planificar antes de implementar | Medio | Alto |
| 6 | Desconectar MCPs no usados | Bajo | Medio |
| 7 | `/compact` antes de pausas | Cero | Medio |
| 8 | `/context` y `/cost` regulares | Cero | Medio (detección) |
| 9 | Skills compactadoras (Caveman) | Bajo | Medio |
| ★ | Skill de auditoría de uso (Nexum) | Cero | Alto |

> **Empezar por:** 1 + 4 (cero esfuerzo, alto impacto). Después 3 + 5.
> Estas reglas viven en `~/.claude/CLAUDE.md` para que apliquen a TODA sesión global.

---

## ✅ Checklist diario

Antes de empezar:
- [ ] `/model opus plan` (Opus solo en plan-mode)
- [ ] CLAUDE.md ≤ 100 líneas, sin dumps
- [ ] Sólo MCPs necesarios para este proyecto

Durante la sesión:
- [ ] Plan antes de implementar (`plan.md` → review → `/implement`)
- [ ] Prompts agrupados, no ráfaga de mensajes cortos
- [ ] `/context` cada ~30 turnos para ver dónde se va

Al cambiar de tarea:
- [ ] `/clear` (no acumules contexto irrelevante)
- [ ] Si pausas >5 min: `/compact` antes de irte

Mensual:
- [ ] Audit del CLAUDE.md → quita lo que ya no aplica
- [ ] Audit de MCPs → desconecta los que no usaste

---

> Stack referenciado por este doc: Anthropic Claude Sonnet 4.6 + Opus 4.7 (cutoff Jan 2026), Claude Code CLI 2.x, MCP protocol v2.0+.
