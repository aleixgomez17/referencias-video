# Configuración para cada miembro del equipo

Cada uno trabaja con su propio Claude y su propia cuenta de APIMart, sobre este mismo repositorio.
Hay que hacerlo **una sola vez** por persona (unos 15 minutos).

## 1. GitHub
1. Crear cuenta gratis en github.com (si no tienes).
2. Pasarle tu usuario a Aleix para que te añada como colaborador (Settings → Collaborators → Add people).
3. Aceptar la invitación que llega por email.
4. (Opcional) Instalar **GitHub Desktop** y clonar `aleixgomez17/referencias-video` para tener la carpeta en tu ordenador. Antes de mirar nada: **Fetch → Pull**.

## 2. Conectar GitHub con tu Claude
1. En Claude: **Settings → Connectors → GitHub → Connect** e inicia sesión con tu cuenta.
2. En la misma pantalla, en **Claude GitHub App**, si sale "No instalado" pulsa **Corregir** y da acceso al repositorio `referencias-video`. Si no te deja (porque el repositorio es de Aleix), pídele a Aleix que lo apruebe desde su GitHub.
3. En un chat nuevo dile a tu Claude: *"Conecta el repositorio aleixgomez17/referencias-video y lee CLAUDE.md"*.

## 3. APIMart en tu Claude Desktop (para generar vídeos)
1. Crea tu cuenta en apimart.ai y recarga saldo. Crea una API key en **Keys**. **No la pegues nunca en un chat.**
2. Instala **Node.js** (versión LTS) desde nodejs.org.
3. En Claude Desktop: **Settings → Developer → Edit Config**. Abre el archivo `claude_desktop_config.json`.
4. Justo **después de la primera llave `{`** pega esto (con la coma final) y cambia `TU_KEY` por tu key:

```json
  "mcpServers": {
    "apimart": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.apimart.ai/mcp", "--header", "Authorization:${APIMART_AUTH}"],
      "env": {
        "APIMART_AUTH": "Bearer TU_KEY"
      }
    }
  },
```

5. Guarda, **cierra Claude del todo** (clic derecho en el icono junto al reloj → Quit) y vuelve a abrirlo.
6. Prueba en un chat nuevo: *"Usa list_models de APIMart con limit 5, sin generar nada"*.

Si el archivo ya tenía un bloque `"mcpServers"`, no pegues otro: añade solo `"apimart": {…}` dentro del existente.

## 4. Mientras tu Claude genera
- Ten **Claude Desktop abierto** en tu ordenador (la conexión con APIMart pasa por él).
- Si el ordenador entra en reposo, la generación sigue; al volver escríbele "ya" a tu Claude y la recoge.
