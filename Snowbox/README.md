# Snowbox

Vídeos y publicidad con IA para Snowbox (calendarios, planners y juegos de Navidad imprimibles). Misma forma de trabajar que `BackAlign/` y `NailCheck/`.

```
aprendizajes/        ← LEER ANTES DE GENERAR
  lecciones.md               lecciones comunes (modelos, prompts, APIMart, retoques gratis) + las propias de Snowbox
  prompts-que-funcionan.md   plantillas listas para copiar
  registro-generaciones.md   cada generación: modelo, coste, resultado, lección
productos/           ← imágenes de cada producto (portada, páginas interiores, mockups), limpias: <producto>_<vista>.png
  p. ej. calendario-adviento-familia/  calendario-adviento-parejas/  planner-navidad/  juegos-familia/
avatares/            ← caras de los avatares de IA (para vídeo, foto de solo cara)
proyectos/           ← un vídeo = una carpeta: AAAA-MM-DD_persona_nombre
    referencia/  trozos/  generaciones/  final/
```

Las descargas y transcripciones automáticas usan `BackAlign/sistema/` (compartido), igual que NailCheck.

## Ojo con los productos de papel

Los calendarios y planners tienen **mucho texto y detalle impreso**. La IA de vídeo deforma las letras y suele mantener lo que había en el vídeo original (ver lecciones de detalles pequeños). Mejor: editar un fotograma con GPT Image metiendo el producto real y animarlo después, o poner el producto/textos en el montaje.
