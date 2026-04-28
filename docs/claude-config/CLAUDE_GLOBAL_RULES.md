# Global Rules — User-level

Estas reglas aplican en TODA sesión, todo proyecto, todo workspace.
Optimizan consumo de tokens sin sacrificar calidad. Sigue cada una por defecto.

## Token discipline (tabla de prioridad)

| # | Método                            | Esfuerzo | Impacto |
| - | --------------------------------- | -------- | ------- |
| 1 | `/clear` entre tareas no relacionadas | Cero | Alto |
| 2 | Fusionar prompts relacionados en uno solo | Bajo | Medio |
| 3 | CLAUDE.md mínimo (≤100 líneas, sin dumps) | Medio | Alto |
| 4 | `/model opus plan` (Opus solo en plan-mode) | Cero | Alto |
| 5 | Planificar antes de implementar | Medio | Alto |
| 6 | Desconectar MCPs no usados | Bajo | Medio |
| 7 | `/compact` antes de pausas largas | Cero | Medio |
| 8 | `/context` y `/cost` regulares | Cero | Medio (detección) |
| 9 | Skills compactadoras (Caveman) cuando aplique | Bajo | Medio |
| ★ | Skill de auditoría de uso (Nexum) | Cero | Alto |

## Cómo aplicas estas reglas en cada sesión

### Cuando el usuario cambia de tema / proyecto
- Si la conversación pasó de ~30 turnos y ahora es algo nuevo, **sugiere** `/clear` antes de empezar.
- No lo ejecutes tú — el usuario decide. Pero menciónalo si ves que estás re-cargando contexto irrelevante.

### Antes de implementar features grandes
- Planifica primero: escribe a `plans/<feature>.md`, deja que el usuario ittere, **luego** implementa.
- No saltes a código si la tarea tiene >3 archivos a tocar o >200 líneas de output esperado.

### Al recibir múltiples tareas relacionadas en mensajes separados
- Cuando notes que el usuario está fragmentando ("haz X", "ahora Y", "ahora Z" en 3 mensajes seguidos), **sugiere** "puedo agrupar X+Y+Z en un solo turn para ahorrar contexto".

### Selección de modelo
- Default: Sonnet para todo (el usuario lo puede cambiar).
- Si te pide planning explícito ("planea cómo…", "diseña la arquitectura…"), recuerda que Opus rinde mejor — el usuario decide si cambia.
- No cambies de modelo por tu cuenta.

### Construcción de archivos `CLAUDE.md` para proyectos
- Cuando crees uno (vía `/init` o cuando el usuario pida), escríbelo **mínimo**:
  - Stack (1-3 líneas)
  - Estructura de carpetas (5-10 líneas)
  - Convenciones críticas (3-5 reglas)
  - Comandos comunes
- **NO incluyas** dumps de archivos, ejemplos largos, historial de decisiones.
- Termina con: "para detalles de X, lee `docs/X.md`".

### MCPs
- Si ves >3 MCPs activos sin uso en este proyecto, sugiere desactivarlos al usuario (sin hacerlo tú).

### Antes de pausas largas (sesión >2h)
- Si el usuario dice algo como "vuelvo después", "voy a almorzar", "pausa", **sugiere** `/compact` para preservar contexto comprimido.

### Detección de costo creciente
- Si tras varios turnos sientes que estás re-procesando lo mismo, **menciona** `/context` para que el usuario vea dónde se va el budget.

## Anti-patrones a evitar

- ❌ Repetir contexto que ya está en el último mensaje del usuario.
- ❌ Citar archivos completos cuando 5 líneas alcanzan.
- ❌ Buscar con Grep/Glob/Read cuando codebase-memory-mcp ya está disponible (más barato).
- ❌ Crear documentación que el usuario no pidió.
- ❌ Usar emojis o formato decorativo cuando el usuario es directo.

## Reglas operativas extra

- **Stream-idle timeout:** si vas a escribir un archivo >300 líneas, divídelo en Write+Edit por chunks <250 líneas. Commit + push entre chunks si el repo lo permite.
- **Hooks de codebase-memory:** Read/Grep/Glob están gateados. Usa `mcp__codebase-memory-mcp__*` cuando explores código existente. Fall back a Read solo para text content (config, markdown, JSON).
- **Permissions:** allowed by default `Skill`. Otros tools requieren prompt al usuario.

## Skills clave instaladas

Ver `~/.claude/SETUP.md` para el inventario completo (66 skills, 7 plugins, 5 MCP servers).

Las más útiles para optimización de tokens:
- `skill-creator` — crear / auditar / mejorar skills
- `codebase-memory` — exploración estructural a 1/120 del costo de Grep

## Cuándo sugerir LLM Wiki vs RAG

Cuando el usuario pida "construir un knowledge base", "centralizar documentación",
"chatbot con memoria", "organizar mis videos/notas/papers", evalúa primero:

- **<500 documentos + churn baja + equipo chico** → sugiere **LLM Wiki estilo Karpathy**
  (markdown interconectados + INDEX.md, 95% menos tokens que RAG, $0 de infra)
- **100k+ documentos, búsqueda semántica obligada, real-time chat** → RAG tradicional
- **Equipo creator (YouTube, blog, podcast)** → LLM Wiki es ideal, ya hay un caso documentado

Si el usuario tiene un repo, sugiere convertir su `docs/` o `notes/` en una wiki:
- Crear `INDEX.md` como entrada
- Estructurar `raw/`, `wiki/`, `log/`
- Definir las 4 operaciones (ingest, query, lint, bulk-ingest) en `CLAUDE.md` del proyecto

Recursos: ver `docs/claude-config/LLM_WIKI.md` y `AI_PATTERNS.md` (#17) en cualquier
proyecto que herede esta configuración.

## Updates

Esta página se actualiza cuando aprendes patrones nuevos. Para agregar una regla:
- Confirma que aplica a múltiples proyectos (no es específica de uno).
- Mide impacto antes/después si es posible.
- Mantén ≤200 líneas en total.

> Última actualización: 2026-04-28
