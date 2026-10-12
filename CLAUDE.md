# Instrucciones para Claude en este repositorio

Este repositorio guarda referencias y resultados de vídeos de producto generados con IA (APIMart: Seedance, GPT Image).

## Antes de lanzar cualquier generación
1. Lee `aprendizajes/lecciones.md` y `aprendizajes/prompts-que-funcionan.md` y aplica lo que dicen.
2. Di al usuario el plan, el modelo y el coste estimado, y espera su OK antes de gastar.

## Dónde va cada cosa
- Fotos de producto: `productos/<producto>/` (nombres: `<color>_<vista>.png`).
- Avatares: `avatares/<nombre>/` (para vídeo usar la foto de solo cara).
- Cada vídeo es un proyecto: `proyectos/NN-nombre/{referencia,trozos,generaciones,final}/`.
- Para descargar un resultado de APIMart: escribir la URL en `sistema/pedidos/<nombre>.txt`, hacer push, esperar ~50 s y hacer pull; el archivo aparece en `sistema/descargas/`. Después moverlo a `proyectos/…/generaciones/`.
- Los pedidos ya descargados se mueven a `sistema/pedidos/archivo/`.

## Después de cada generación
- Revisar fotograma a fotograma antes de entregar (caras, cortes entre trozos, colores).
- Añadir una fila a `aprendizajes/registro-generaciones.md` (fecha, proyecto, modelo, qué se pidió, resultado, coste, lección).
- Si se aprende algo nuevo, añadirlo a `aprendizajes/lecciones.md`; si un prompt funciona bien, añadirlo a `prompts-que-funcionan.md`.
