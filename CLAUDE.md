# CLAUDE.md · TORO KAIZEN project rules

> Reglas operativas para Claude Code en este repo. **Override de cualquier comportamiento default**.

---

## Anti stream-idle-timeout (CRÍTICO)

El error `Stream idle timeout - partial response received` ocurre cuando una sola respuesta intenta emitir demasiado texto de golpe. **Para que NO vuelva a pasar:**

### Reglas de output en chat

1. **Cap respuestas a 250 palabras máximo** salvo que el usuario pida explícitamente "explícame en detalle".
2. **Nunca pegar tablas de >8 filas en chat** — escribirlas a un `.md` en `docs/` y mandar el link.
3. **Nunca pegar bloques de código de >40 líneas en chat** — escribirlos al archivo correspondiente y mostrar solo el `Edit` summary.
4. **Resúmenes de PR**: máximo 5 bullets por sección. El detalle completo va en el PR body via `mcp__github__create_pull_request`, no en la respuesta de chat.
5. **No re-imprimir contenido recién creado**. Si escribiste algo a un archivo, mandar el path, no el contenido.
6. **Cierres de PR**: 2-3 frases máximo. "PR #X mergeado, commit Y. CI Z." Nada de mega-resúmenes después.

### Reglas de tool-use

7. **Bash output trimming**: usar `| head -N`, `| tail -N`, o `tee` para acotar. Evitar `cat archivo_grande` sin cap.
8. **Nunca leer archivos completos solo para verificar 5 líneas** — usar `grep -n` con contexto chico.
9. **Sanity check bloques**: una sola línea `echo "OK"` después de batches, no 20 líneas de validación.

### Reglas de autoría

10. **Documentos largos van a archivos**. Si la respuesta natural >500 palabras → es un doc.
11. **Multi-turno > una respuesta gigante**. Si hay 5 mejoras propuestas, ofrecer las 5 en una lista corta y aplicar en PRs separados, no todas en uno.

---

## Operación del proyecto

### Branch & PR flow
- Toda feature en branch `claude/<descriptor-corto>`.
- Commit messages descriptivos pero secos.
- PR body conciso (≤300 palabras) con secciones: Summary · Cambios · Files · Test plan.
- Squash-merge default. Nunca force-push a main.

### Hosting
- Producción: Netlify (`netlify.toml` define redirects + security headers).
- `/docs/*` y `/scripts/*` están bloqueados públicamente (404 force) — solo accesibles vía GitHub URL.
- Costo info NUNCA debe leak al sitio público (`docs/INVERSION_*` son interno).

### Tema visual
- **Hero, lookbook, footer**: dark canvas (`--bg-1: #141416`).
- **Productos, reviews, UGC**: cream band (`.cream-band` class).
- **Acento universal**: lime `#D4FF00`.
- Sprite SVG inline (40+ symbols) en `index.html` end-of-body.
- Type stack: `Bebas Neue` (display) + `Barlow Condensed` (eyebrow/btn) + `Barlow` (body) + `JetBrains Mono` (code/numbers) + `Noto Serif JP` (kanji).

### Estado del catálogo
- 3 SKUs hero (con `data-mto="1"`): Tee Gothic Black ($649), Jogger Phantom ($849), Hoodie Void ($899).
- 5 SKUs Coming Soon (con `data-status="coming-soon"`): Tank Stringer, Short Obsidian, Set Titan, Tee Gothic White, Set Venom.
- Modelo: Pre-order Drop / Made-to-Order (7-14 días lead time).

### Stack de inversión confirmado
- Costo unitario target: $150-200 MXN (TQ confirma).
- PVP: tee $649, jogger $849, hoodie $899, cargo $799.
- Posicionamiento: 50-65% más barato que YoungLA/Gymshark/Vuori/Lululemon con misma calidad de tela.
- Target demo: 15-26 años, TikTok-first marketing.

### Codes activos
- `BIENVENIDO10` (-10%)
- `SQUAD15` (-15%)
- `TORO20` (-20%)
- `ENVIO0` (envío gratis sin mínimo)

---

## Comandos útiles

```bash
# Ver últimos PRs
git log origin/main --oneline -10

# Sanity check del index.html
grep -c '<symbol id=' index.html  # debería ser 40+
grep -c 'class="pc rv"' index.html  # debería ser 8

# Verificar que docs estén bloqueados públicamente
curl -sI https://torokaizen.mx/docs/INVERSION_LIGERA_POD.md | head -3
# Debería responder 404

# Buscar texto en el sitio
grep -in '<keyword>' index.html | head -10
```

---

## Anti-patterns (NUNCA)

- ❌ Imprimir un markdown completo en chat después de escribirlo a archivo
- ❌ Tablas comparativas con 10+ columnas en chat (van a `.md`)
- ❌ Repetir contenido del PR body en el chat post-merge
- ❌ Generar respuestas con 50+ líneas de explicación cuando 10 líneas + un link al doc alcanzan
- ❌ Dump de `cat archivo` sin head/tail cap
- ❌ Múltiples `grep` en serie cuando uno solo con `-A` o `-B` alcanza

---

> Última actualización: 2026-05-04 después del primer Stream idle timeout. Si vuelve a pasar, revisar este archivo y endurecerlo.
