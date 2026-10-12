# Referencias y vídeos con IA

Repositorio del equipo para crear vídeos de producto (UGC) con IA a partir de vídeos de referencia.

## 📁 Cómo está organizado

```
aprendizajes/        ← LEER ANTES DE GENERAR. Qué funciona y qué no.
  lecciones.md               reglas aprendidas (modelos, prompts, trucos)
  prompts-que-funcionan.md   plantillas listas para copiar
  registro-generaciones.md   cada generación: modelo, coste, resultado, lección

productos/           ← fotos de referencia de cada producto (frente y espalda)
  top-espalda/

avatares/            ← caras de nuestros avatares de IA
  es40/       española ~40 años (usar solo_cara.png para vídeo)
  rubia/

proyectos/           ← un vídeo = una carpeta
  01-top-negro-chica-rubia/
  02-leopardo-avatar-rubia-top-beige/
  03-salon-avatar-es40-top-negro/
  04-jardin-avatar-es40/
    referencia/      vídeo original
    trozos/          cortes que se mandan a la IA
    generaciones/    lo que devuelve la IA (en bruto)
    final/           ✅ vídeos terminados

sistema/             ← automático, no tocar
  pedidos/           enlaces que se mandan a descargar
  descargas/         lo que descarga GitHub automáticamente
```

## 🔁 Flujo de trabajo

1. Subir el vídeo de referencia y las fotos (o mandárselos a Claude en el chat).
2. Claude los prepara (recorta, baja a 720p, trocea por planos) y los sube aquí.
3. Claude lanza la generación en APIMart (necesita Claude Desktop abierto en el ordenador de Aleix).
4. GitHub descarga el resultado automáticamente en `sistema/descargas/`.
5. Claude lo revisa fotograma a fotograma, lo monta con el audio original y lo deja en `proyectos/…/final/`.
6. Se apunta en `aprendizajes/registro-generaciones.md` lo que ha salido bien o mal.

## ⚠️ Importante

- El repositorio es **público**: APIMart necesita leer los archivos desde un enlace público. No subir nada privado.
- Las fotos de producto deben estar **limpias** (sin flechas, textos ni gráficos).
- Nombres de archivo: en minúsculas, sin espacios ni tildes (`beige_espalda.png`).
