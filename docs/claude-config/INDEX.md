# INDEX — Claude Code knowledge base (LLM Wiki)

> **Mini-wiki estilo Karpathy.** Cada nodo es un markdown que se enlaza con los demás.
> Cuando un LLM lee este índice, sabe a qué archivo navegar para cada tema.
> Reemplaza RAG para bases de hasta ~500 docs. Portable: funciona en Claude Code, OpenCode, Manus, etc.

## 🗺️ Mapa de la wiki

```
INDEX.md (estás aquí)
  │
  ├─► [SETUP.md] — qué hay instalado en mi Claude
  │     • plugins (7) · MCPs (5) · skills (66) · marketplaces (3)
  │     • script reproducible para máquina nueva
  │     enlaza con → CLAUDE_GLOBAL_RULES.md, AI_PATTERNS.md
  │
  ├─► [CLAUDE_GLOBAL_RULES.md] — reglas que sigo en TODA sesión
  │     • token discipline · model selection · anti-patterns
  │     • copia del ~/.claude/CLAUDE.md auto-cargado
  │     enlaza con → CLAUDE_OPTIMIZATION.md
  │
  ├─► [CLAUDE_OPTIMIZATION.md] — playbook de los 9 métodos para reducir tokens 90%+
  │     • /clear, /compact, /context, /usage, /model
  │     • CLAUDE.md mínimo, MCPs justos, skills compactadoras
  │     enlaza con → CLAUDE_GLOBAL_RULES.md, LLM_WIKI.md
  │
  ├─► [AI_PATTERNS.md] — 17 patrones reusables de sistemas multi-agente
  │     • #1 Multi-agent router · #2 Message buffering · #3 Follow-ups
  │     • #4 Payment intent · #5 Working hours · #6 Human handoff
  │     • #7-#15 Misc patterns · #16 Scroll-morph videos
  │     • #17 LLM Wiki (Karpathy) ← este sistema
  │     enlaza con → MORPH_VIDEOS.md, LLM_WIKI.md
  │
  ├─► [LLM_WIKI.md] — guía para construir tu propia wiki estilo Karpathy
  │     • 3 capas: raw → wiki → schema (CLAUDE.md)
  │     • 4 operaciones: ingest, query, lint, bulk-ingest
  │     • cuándo usar wiki vs RAG
  │     enlaza con → AI_PATTERNS.md (pattern #17)
  │
  └─► [MORPH_VIDEOS.md] — prompts para los 4 scroll-morph videos del sitio
        • Hero (bull → atleta) · Drop (raw → BUILT DIFFERENT)
        • Fabric → Garment · TORO → 改善 → JUNTOS
        • Stack: Nano Banana 2 + Veo 3.1
        enlaza con → AI_PATTERNS.md (pattern #16)
```

## 🔍 Navegación por uso

### "Voy a empezar en una máquina nueva"
→ [SETUP.md](./SETUP.md) sección "Quick install"

### "Estoy quemando muchos tokens"
→ [CLAUDE_OPTIMIZATION.md](./CLAUDE_OPTIMIZATION.md) tabla de prioridad
→ [CLAUDE_GLOBAL_RULES.md](./CLAUDE_GLOBAL_RULES.md) reglas a aplicar

### "Quiero construir un sistema multi-agente"
→ [AI_PATTERNS.md](./AI_PATTERNS.md) pattern #1 (router) y #3 (follow-ups)

### "Quiero un knowledge base que no use RAG"
→ [LLM_WIKI.md](./LLM_WIKI.md) (este sistema mismo es el ejemplo)
→ [AI_PATTERNS.md](./AI_PATTERNS.md) pattern #17

### "Quiero hacer animaciones premium en una landing"
→ [MORPH_VIDEOS.md](./MORPH_VIDEOS.md)
→ [AI_PATTERNS.md](./AI_PATTERNS.md) pattern #16

### "Necesito decisiones de marca para Toro Kaizen"
→ [`docs/propuestas.md`](../propuestas.md) (no está en este wiki, es proyecto-específico)

## 📐 Tags / categorías

| Tag | Archivos |
|-----|---------|
| `#token-optimization` | CLAUDE_OPTIMIZATION, CLAUDE_GLOBAL_RULES |
| `#multi-agent` | AI_PATTERNS (#1-#15) |
| `#frontend-effects` | AI_PATTERNS (#16), MORPH_VIDEOS |
| `#knowledge-management` | LLM_WIKI, AI_PATTERNS (#17), INDEX |
| `#claude-config` | SETUP, CLAUDE_GLOBAL_RULES |
| `#brand-strategy` | `../propuestas.md` |

## 🔄 Actualizar este índice

Cuando agregues un nuevo doc a `docs/claude-config/`:
1. Añade su nodo al mapa de arriba con su descripción + enlaces
2. Añade entrada en "Navegación por uso" si aplica
3. Etiqueta con tags relevantes
4. Si el doc reemplaza otro, marca el viejo `[deprecated]`

> Última actualización: 2026-04-28 · 6 nodos activos.
