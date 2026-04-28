# LLM Wiki — guía para construirla

> Sistema de "memoria infinita" estilo Andrej Karpathy. Reemplaza RAG con
> archivos markdown interconectados que el LLM navega como Wikipedia.
> 95% menos tokens que un RAG tradicional para bases de hasta ~500 docs.

Tags: `#knowledge-management` `#llm-wiki` `#karpathy` `#obsidian`

---

## 🎯 Cuándo usar esto vs RAG tradicional

| Tu caso | Recomendación |
|---|---|
| <500 documentos, knowledge en evolución, equipo chico | **LLM Wiki** ← este sistema |
| 100k+ documentos, multi-tenant, búsqueda semántica obligada | RAG tradicional (Pinecone, Weaviate, pgvector) |
| Knowledge base personal/equipo, quieres portabilidad | LLM Wiki |
| Live chat con miles de queries/min | RAG (latencia menor) |
| Creator de contenido organizando lo propio | LLM Wiki |

**Test rápido:** ¿caben todos tus docs en una carpeta y los puede leer un humano? → Wiki. ¿Tienes que indexar mensualmente porque cambia todo? → RAG.

---

## 🏗️ Arquitectura — 3 capas

```
┌─────────────────────────────────────────┐
│  Capa 1: RAW                            │
│  Archivos crudos sin clasificar         │
│  • PDFs, transcripts, capturas, etc.    │
└──────────────┬──────────────────────────┘
               │ ingest
               ▼
┌─────────────────────────────────────────┐
│  Capa 2: WIKI                           │
│  Markdown interconectados (lo navegable)│
│  • conceptos/  · entidades/  · síntesis/│
│  • cada archivo enlaza con [[otros]]    │
└──────────────┬──────────────────────────┘
               │ esquema
               ▼
┌─────────────────────────────────────────┐
│  Capa 3: SCHEMA                         │
│  CLAUDE.md / AGENTS.md / GEMINI.md      │
│  • reglas para el LLM                   │
│  • cómo ingest, cómo navegar, cómo escribir│
└─────────────────────────────────────────┘
```

**El INDEX.md vive en la capa 2** y es el punto de entrada de todo.

---

## 🔧 4 operaciones

| Operación | Qué hace | Cuándo |
|-----------|----------|--------|
| **ingest** | Toma 1 archivo raw, lo clasifica, lo etiqueta, lo conecta a wiki existente | Agregaste 1 cosa nueva |
| **query** | Pregunta cualquier cosa; el LLM navega desde INDEX → archivos relevantes | Diario, en chat |
| **lint** | Encuentra archivos huérfanos (sin links) y los conecta o margina | Mensual / mantenimiento |
| **bulk-ingest** | Procesa 100s de raw files en una sola pasada | Setup inicial / migración |

Cada operación es un prompt al LLM con instrucciones del CLAUDE.md.

---

## 📦 Stack mínimo

| Tool | Para qué | Costo |
|------|----------|-------|
| **Obsidian** | Visualizar la wiki + grafo de conexiones | Gratis |
| **Claude Code** (o cualquier agente) | Operaciones (ingest, query, lint) | Tu plan Claude |
| **Markdown files** | El medio | Gratis |
| **Git** | Versionado | Gratis |
| Obsidian Clipper plugin | Mandar webpages al raw desde el navegador | Gratis |

> Total: $0 + tu suscripción de Claude. Sin Pinecone, sin OpenAI embeddings, sin servidores.

---

## 🚀 Setup paso a paso

### 1. Estructura de carpetas
```bash
mkdir -p mi-wiki/{raw,wiki,log}
cd mi-wiki
touch INDEX.md CLAUDE.md
echo '# INDEX' > INDEX.md
echo '# Reglas del agente' > CLAUDE.md
```

### 2. Abrir como Obsidian Vault
- Descarga Obsidian (gratis, no necesitas cuenta)
- File → Open Folder as Vault → selecciona `mi-wiki/`
- Listo: ya navegas con grafo y enlaces

### 3. CLAUDE.md mínimo (esquema)

```markdown
# LLM Wiki — Reglas del agente

Eres el mantenedor de esta wiki. Tu trabajo:

## ingest <file>
1. Lee el archivo en raw/
2. Decide su categoría (concepto, entidad, síntesis)
3. Crea/actualiza un .md en wiki/<categoría>/
4. Conecta con archivos existentes via [[wikilinks]]
5. Actualiza INDEX.md si introduce un tema nuevo
6. Mueve el raw a raw/processed/

## query <pregunta>
1. Lee INDEX.md primero (siempre)
2. Sigue los wikilinks relevantes
3. NO leas archivos raw a menos que el wiki te lleve allí explícitamente
4. Si no encuentras la respuesta en wiki, di "no está documentado"

## lint
1. Busca archivos en wiki/ sin wikilinks entrantes
2. Por cada huérfano: conecta con un archivo relevante o sugiere borrarlo
3. Reporta resumen al final

## bulk-ingest <dir>
1. Por cada archivo en raw/<dir>/: ejecuta ingest
2. Al final corre lint automático
3. Actualiza INDEX.md con todas las nuevas categorías

## Reglas generales
- Cada wiki/*.md MUST tener al menos 1 wikilink saliente
- INDEX.md es la fuente de la verdad de la estructura
- Nunca borres archivos sin pedir confirmación
- Logs van a log/YYYY-MM-DD.md
```

### 4. Primera ingesta

```bash
# En Claude Code, dentro del vault:
> bulk-ingest raw/
```

El LLM lee todo, clasifica, conecta y popula el wiki/. Demora minutos.

### 5. Empieza a usarlo

```bash
> query: ¿qué patrones se repiten en mis videos de YouTube exitosos?
> ingest raw/nueva-transcripcion.txt
> lint
```

---

## 💡 Ejemplos de uso

### Creator de contenido
- raw/ → transcripts de YouTube, tweets, ideas sueltas
- wiki/ → conceptos clave del canal, series, audiences
- query → "qué hooks me funcionan mejor", "ya toqué este tema"

### E-commerce
- raw/ → reviews, support tickets, product specs
- wiki/ → SKUs, FAQs por categoría, supplier profiles
- query → "qué problema resuelve este producto", "cuál es nuestro mejor seller"

### Equipo de software
- raw/ → ADRs, post-mortems, RFCs
- wiki/ → decisiones técnicas, sistemas, equipos
- query → "por qué elegimos Postgres en 2024", "quién dueño de auth"

### Personal knowledge management
- raw/ → highlights de libros, podcasts, conversaciones
- wiki/ → conceptos, mentores, frameworks personales
- query → "qué dijo X sobre liderazgo", "patrones de decisión"

---

## ⚖️ Pros y cons honestos

### Pros
- ✅ **Portable** — la misma carpeta funciona en Claude Code, OpenCode, Manus, Cursor, etc.
- ✅ **Versionable con git** — todo es texto
- ✅ **Sin costo de infraestructura** — sin vector DB, sin embeddings API
- ✅ **Editable a mano** — cuando el LLM se equivoca, lo arreglas vos
- ✅ **Revisable** — abres el .md y lees lo que el LLM "sabe"
- ✅ **Mejora con el tiempo** — más operaciones → wiki más rica

### Cons
- ❌ **Mantenimiento** — necesita lint regular, sino se vuelve grafo de espagueti
- ❌ **No es búsqueda semántica** — depende de calidad del INDEX y nombres de archivo
- ❌ **Sets gigantes** — 10k+ archivos se vuelven lentos de procesar en operations
- ❌ **Multi-tenant** complicado — cada usuario necesita su vault separado
- ❌ **No real-time** — query es síncrono y respuesta tarda mientras navega

---

## 🛠️ Tips operativos

1. **Naming convention estricta:** `concepto-X.md`, `persona-X.md`, `evento-YYYY-MM.md`. El LLM clasifica mejor con prefijos.
2. **INDEX corto:** ≤200 líneas. Si crece más, divide en INDEX-cat1.md, INDEX-cat2.md.
3. **Wikilinks > tags:** `[[Otra-página]]` es más navegable que `#tag`.
4. **Log diario:** corre `lint` al final del día y guarda el resumen en `log/YYYY-MM-DD.md`.
5. **Plugin Obsidian Clipper:** instálalo en Chrome para mandar artículos web directamente a `raw/` con un click.
6. **MCP Obsidian:** existe MCP server para Obsidian que permite que Claude lea/escriba en el vault remotamente.

---

## 🔗 Referencias

- **Karpathy original tweet:** https://twitter.com/karpathy/status/... (LLM-Wiki concept)
- **Repo de plantilla:** `karpathy/llm-wiki` (GitHub)
- **Obsidian:** https://obsidian.md
- **Obsidian Clipper:** Chrome Web Store
- **Pattern #17 en este repo:** [`AI_PATTERNS.md`](./AI_PATTERNS.md#17-llm-wiki-conocimiento-interconectado-vs-rag)

---

## 🎯 Esta misma wiki es un ejemplo

Mira `docs/claude-config/` en este repo: tiene INDEX.md (entrada), 6 nodos especializados (SETUP, CLAUDE_GLOBAL_RULES, CLAUDE_OPTIMIZATION, AI_PATTERNS, MORPH_VIDEOS, LLM_WIKI) y enlaces cruzados. Cuando me preguntas algo de Claude Code, leo INDEX primero, navego al doc relevante, no necesito releer todo cada vez.

> Última actualización: 2026-04-28
