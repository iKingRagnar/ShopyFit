# Claude Code Setup — Plugins, Skills & MCP Servers

> Snapshot del entorno `~/.claude/` para replicarlo en otra sesión / máquina.
> Todo está configurado a **nivel user**, así aplica en cualquier proyecto, chat, cowork y code que abras con tu cuenta.

---

## ⚙️ Quick install (script todo-en-uno)

Si llegas a una máquina nueva y tienes `claude` CLI + `npm`/`npx` + `git` + `curl`, esto reproduce todo el setup en ~5 minutos:

```bash
# ──────────── 1. ENV vars globales ────────────
mkdir -p ~/.claude
SETTINGS=~/.claude/settings.json
[ -f "$SETTINGS" ] || echo '{"$schema":"https://json.schemastore.org/claude-code-settings.json"}' > "$SETTINGS"

# Sube el timeout para que Write/Edit grandes no se corten (bug "Stream idle timeout")
jq '.env.API_TIMEOUT_MS = "1800000"' "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"

# Tus API keys (REEMPLAZA con las tuyas)
jq '.env.ANTHROPIC_API_KEY = "sk-ant-api03-XXXXXXXXXX"'   "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"
jq '.env.FIRECRAWL_API_KEY = "fc-XXXXXXXXXX"'             "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"

# ──────────── 2. Marketplaces (3) ────────────
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin marketplace add obra/superpowers-marketplace
claude plugin marketplace add AgriciDaniel/claude-seo

# ──────────── 3. Plugins (7) ────────────
claude plugin install frontend-design@claude-plugins-official
claude plugin install superpowers@superpowers-marketplace
claude plugin install context7@claude-plugins-official
claude plugin install firecrawl@claude-plugins-official
claude plugin install playwright@claude-plugins-official
claude plugin install serena@claude-plugins-official
claude plugin install claude-seo@agricidaniel-seo

# ──────────── 4. MCP Servers (5) ────────────
# Reemplaza la API key real cuando ejecutes esto
claude mcp add --scope user task-master-ai \
  -e ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXX \
  -- npx -y task-master-ai

claude mcp add --scope user gpt-researcher  -- npx -y @assafelovic/gptr-mcp
claude mcp add --scope user obsidian        -- npx -y mcp-remote http://localhost:22360/sse
claude mcp add --scope user promptfoo       -- npx -y promptfoo@latest mcp --transport stdio

# Codebase Memory MCP (binary)
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# ──────────── 5. Skills sueltas (a ~/.claude/skills/) ────────────
mkdir -p /tmp/sk && cd /tmp/sk

# 5a) 10 skills oficiales de Anthropic
git clone --depth 1 https://github.com/anthropics/skills.git anthropic-skills
for s in pdf xlsx pptx docx canvas-design web-artifacts-builder brand-guidelines skill-creator frontend-design; do
  cp -r anthropic-skills/skills/$s ~/.claude/skills/
done

# 5b) 40 marketing skills de Corey Haines
git clone --depth 1 https://github.com/coreyhaines31/marketingskills.git marketing
cp -r marketing/skills/* ~/.claude/skills/

# 5c) Deep Research (2 variantes)
git clone --depth 1 https://github.com/Weizhena/Deep-Research-skills.git deep-research
cp -r deep-research/skills/research-en       ~/.claude/skills/deep-research
cp -r deep-research/skills/research-codex-en ~/.claude/skills/deep-research-codex

# 5d) Remotion
git clone --depth 1 --filter=blob:none --no-checkout https://github.com/remotion-dev/remotion.git remotion
cd remotion && git sparse-checkout init --cone && git sparse-checkout set "packages/skills" && git checkout
cp -r packages/skills/skills/remotion ~/.claude/skills/
cd /tmp/sk

# 5e) Firecrawl CLI + 18 sub-skills (con tu API key)
npx -y firecrawl-cli@latest init --all -k fc-XXXXXXXXXX

# Limpieza
rm -rf /tmp/sk

# ──────────── 6. Reinicia Claude Code ────────────
# (los MCP servers se levantan en el siguiente arranque)
```

---

## 📋 Inventario completo

### 🔑 Variables de entorno globales (`~/.claude/settings.json` → `env`)

| Variable             | Valor / Propósito                                                |
| -------------------- | ---------------------------------------------------------------- |
| `API_TIMEOUT_MS`     | `1800000` (30 min) — evita "Stream idle timeout" en Edit grandes |
| `ANTHROPIC_API_KEY`  | Tu key real — la usan task-master-ai, MCPs y subagentes          |
| `FIRECRAWL_API_KEY`  | Tu key real — Firecrawl CLI y skills la leen automáticamente     |

### 🛒 Marketplaces (3) — `~/.claude/settings.json` → `extraKnownMarketplaces`

| Nombre                       | Repo GitHub                          |
| ---------------------------- | ------------------------------------ |
| `claude-plugins-official`    | `anthropics/claude-plugins-official` |
| `superpowers-marketplace`    | `obra/superpowers-marketplace`       |
| `agricidaniel-seo`           | `AgriciDaniel/claude-seo`            |

### 🔌 Plugins (7 enabled)

| # | Plugin                       | Marketplace               | Uso                                               |
| - | ---------------------------- | ------------------------- | ------------------------------------------------- |
| 1 | **frontend-design**          | claude-plugins-official   | Diseño UI con buen criterio (anti AI-slop)        |
| 2 | **superpowers**              | superpowers-marketplace   | TDD estricto + brainstorming socrático + 20 skills (Jesse Vincent) |
| 3 | **context7**                 | claude-plugins-official   | Docs version-específica de cualquier lib (Upstash) |
| 4 | **firecrawl**                | claude-plugins-official   | Web scraping + search + interact (Y Combinator)   |
| 5 | **playwright**               | claude-plugins-official   | Browser automation (Microsoft)                    |
| 6 | **serena**                   | claude-plugins-official   | Análisis semántico de código vía LSP              |
| 7 | **claude-seo**               | agricidaniel-seo          | SEO audit · 21 sub-skills + 12 subagentes         |

### ⚡ MCP Servers (5, scope `user`) — `~/.claude.json` → `mcpServers`

| Server                  | Comando                                                  | Notas                                                 |
| ----------------------- | -------------------------------------------------------- | ----------------------------------------------------- |
| **task-master-ai**      | `npx -y task-master-ai`                                  | Parsea PRDs en tareas estructuradas. Necesita Anthropic key |
| **codebase-memory-mcp** | `~/.local/bin/codebase-memory-mcp`                       | Tree-sitter index 66 lenguajes · 120x menos tokens. Single binary |
| **gpt-researcher**      | `npx -y @assafelovic/gptr-mcp`                           | Deep research planner+executors paralelos             |
| **obsidian**            | `npx -y mcp-remote http://localhost:22360/sse`           | ⚠️ Requiere Obsidian app + plugin oficial corriendo  |
| **promptfoo**           | `npx -y promptfoo@latest mcp --transport stdio`          | Tests unitarios para prompts + 50+ vulnerability detectors |

### 🧠 Skills (66 totales en `~/.claude/skills/`)

#### Anthropic oficiales (10)
`brand-guidelines` · `canvas-design` · `docx` · `frontend-design` · `pdf` · `pptx` · `session-start-hook` · `skill-creator` · `web-artifacts-builder` · `xlsx`

#### Investigación / Memoria (3)
`codebase-memory` · `deep-research` · `deep-research-codex`

#### Video (1)
`remotion`

#### Marketing (40 — Corey Haines / Conversion Factory)
SEO/Content: `ai-seo` · `content-strategy` · `programmatic-seo` · `schema-markup` · `seo-audit` · `site-architecture`

CRO: `ab-test-setup` · `analytics-tracking` · `form-cro` · `onboarding-cro` · `page-cro` · `paywall-upgrade-cro` · `popup-cro` · `signup-flow-cro`

Copy: `ad-creative` · `cold-email` · `copy-editing` · `copywriting` · `email-sequence`

Growth: `community-marketing` · `competitor-alternatives` · `competitor-profiling` · `customer-research` · `directory-submissions` · `free-tool-strategy` · `launch-strategy` · `lead-magnets` · `marketing-ideas` · `marketing-psychology` · `paid-ads` · `referral-program` · `social-content`

Sales/Ops: `aso-audit` · `churn-prevention` · `pricing-strategy` · `product-marketing-context` · `revops` · `sales-enablement`

Misc: `image` · `video`

#### Firecrawl (12 — instaladas por `firecrawl-cli init`)
`firecrawl` (CLI top-level) · `firecrawl-agent` · `firecrawl-search` · `firecrawl-scrape` · `firecrawl-crawl` · `firecrawl-map` · `firecrawl-interact` · `firecrawl-parse` · `firecrawl-download` · `firecrawl-build-onboarding` · `firecrawl-build-search` · `firecrawl-build-scrape` · `firecrawl-build-interact`

---

## 🩹 Troubleshooting

| Problema                                       | Solución                                                                                     |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------- |
| "Stream idle timeout - partial response"       | `API_TIMEOUT_MS=1800000` ya configurado. Si vuelve, sube a `2700000` (45 min)                |
| `obsidian` MCP marca rojo                      | Normal sin Obsidian app corriendo. Abre Obsidian + plugin que escuche en `:22360`            |
| `task-master-ai` falla auth                    | Key real en `~/.claude.json` → mcpServers → task-master-ai → env → ANTHROPIC_API_KEY        |
| Plugin no aparece en `claude plugin list`      | `claude plugin marketplace update <nombre>` y reintenta install                              |
| Skill no se activa por sí sola                 | Su `description` decide cuándo se invoca. Forza con `/<skill-name>` o pídela explícitamente  |

---

## 📂 Archivos clave

- **Global rules / habits:** `~/.claude/CLAUDE.md` (auto-loaded en cada sesión)
- **Settings (env, plugins, marketplaces):** `~/.claude/settings.json`
- **MCP servers (user scope):** `~/.claude.json` → key `mcpServers`
- **Skills:** `~/.claude/skills/<nombre>/SKILL.md` cada una
- **Plugins instalados:** `~/.claude/plugins/marketplaces/<marketplace>/<plugin>/`
- **Codebase Memory binary:** `~/.local/bin/codebase-memory-mcp`

## 🧠 Global rules cheatsheet (de `CLAUDE.md`)

| # | Método | Esfuerzo | Impacto |
| - | ------ | -------- | ------- |
| 1 | `/clear` entre tareas no relacionadas | Cero | Alto |
| 2 | Fusionar prompts relacionados | Bajo | Medio |
| 3 | CLAUDE.md mínimo (≤100 líneas) | Medio | Alto |
| 4 | `/model opus plan` | Cero | Alto |
| 5 | Planificar antes de implementar | Medio | Alto |
| 6 | Desconectar MCPs no usados | Bajo | Medio |
| 7 | `/compact` antes de pausas | Cero | Medio |
| 8 | `/context` + `/cost` regulares | Cero | Medio |
| 9 | Skills compactadoras (Caveman) | Bajo | Medio |
| ★ | Skill auditoría de uso (Nexum) | Cero | Alto |

Detalles completos en `docs/claude-config/CLAUDE_OPTIMIZATION.md` (en cada repo) o en este SETUP.md hermano.

---

## 🔒 Seguridad — claves API

Las API keys viven en plaintext en `~/.claude/settings.json` (env block) y `~/.claude.json` (mcpServers env). Si compartes esta máquina o haces backup público:

```bash
chmod 600 ~/.claude/settings.json ~/.claude.json
# o usa apiKeyHelper en lugar de hardcodear (ver schema oficial)
```

**Nunca** commitees estos archivos en repos públicos.

---

## 🔄 Para llevar este setup a otra máquina

1. Copia este `SETUP.md` a la nueva máquina.
2. Edita el bloque "Quick install" reemplazando `XXXXXXXXXX` por tus API keys reales.
3. Ejecuta el script.
4. Reinicia Claude Code.
5. Verifica con: `claude plugin list && claude mcp list && ls ~/.claude/skills | wc -l`
   Esperas ver: 7 plugins · 5 MCP servers · 66+ skills.

> Última actualización: 2026-04-28 · Generado automáticamente del entorno vivo.
