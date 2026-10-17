# Referencias y vídeos con IA

Repositorio del equipo (4 personas, cada una con su Claude) para crear vídeos de producto (UGC) con IA a partir de vídeos de referencia, e ir guardando lo que aprendemos.

👉 **Nuevo en el equipo:** sigue `CONFIGURACION-EQUIPO.md` (una sola vez).

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

proyectos/           ← un vídeo = una carpeta: AAAA-MM-DD_persona_nombre
  2026-10-10_aleix_top-negro-chica-rubia/
  2026-10-11_aleix_jardin-avatar-es40/
  …
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
3. Claude lanza la generación en APIMart con **tu** cuenta (necesita tu Claude Desktop abierto).
4. GitHub descarga el resultado automáticamente en `sistema/descargas/`.
5. Claude lo revisa fotograma a fotograma, lo monta con el audio original y lo deja en `proyectos/…/final/`.
6. Se apunta en `aprendizajes/registro-generaciones.md` lo que ha salido bien o mal.

## 🤝 Normas del equipo

- **Antes de empezar:** Fetch → Pull (o tu Claude hace `git pull`).
- **Aprendizajes:** solo se añade, nunca se borra lo de otro. Lección nueva con `(nombre, fecha, proyecto)`. Si tu prueba contradice algo, añade una nota ⚠️ debajo.
- **Registro:** cada generación es una fila nueva al final, con tu nombre y el coste.
- **Proyectos:** cada uno en su carpeta con fecha y nombre; no tocar las de otros.

## ⚠️ Importante

- El repositorio es **público**: APIMart necesita leer los archivos desde un enlace público. No subir nada privado.
- Las fotos de producto deben estar **limpias** (sin flechas, textos ni gráficos).
- Nombres de archivo: en minúsculas, sin espacios ni tildes (`beige_espalda.png`).
