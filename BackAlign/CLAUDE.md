# Instrucciones para Claude en este repositorio

Repositorio **compartido por un equipo de 4 personas**, cada una con su propio Claude y su propia cuenta de APIMart. Aquí se guardan referencias, resultados y, sobre todo, **lo que vamos aprendiendo** para hacer mejores vídeos de producto con IA (Seedance, GPT Image vía APIMart).

## Al empezar cada sesión
1. `git pull --rebase` para tener lo último de todos.
2. Si no sabes el nombre de la persona con la que trabajas, pregúntaselo una vez (se usa en nombres de proyecto, registro y commits).
3. Lee `aprendizajes/lecciones.md` y `aprendizajes/prompts-que-funcionan.md` antes de proponer cualquier generación, y aplícalos. Lee también las últimas filas de `aprendizajes/registro-generaciones.md`: puede haber pruebas recientes de otros compañeros.

## Antes de gastar
- Explica el plan, el modelo y el coste estimado, y espera el OK de la persona.

## Dónde va cada cosa
- Fotos de producto: `productos/<producto>/` (nombres `<color>_<vista>.png`, limpias, sin flechas ni textos).
- Avatares: `avatares/<nombre>/` (para vídeo usar la foto de solo cara).
- Cada vídeo es un proyecto: `proyectos/AAAA-MM-DD_<persona>_<nombre-corto>/` con `referencia/`, `trozos/`, `generaciones/`, `final/`. La fecha y el nombre evitan que dos personas creen la misma carpeta.
- No modificar ni borrar proyectos de otras personas.
- Descargas de APIMart: escribir la URL en `sistema/pedidos/<persona>_<nombre>.txt`, push, esperar ~50 s, pull; el archivo aparece en `sistema/descargas/`. Moverlo después a `proyectos/…/generaciones/` y mover el `.txt` a `sistema/pedidos/archivo/`.

## Para no pisar el trabajo de otros
- Commits pequeños y `git pull --rebase` justo antes de cada `git push`. Si hay conflicto en un archivo de `aprendizajes/`, conserva las líneas de ambos.
- En `aprendizajes/` solo se **añade**: filas nuevas al final del registro, lecciones nuevas con `(persona, fecha, proyecto)`. Nunca borrar lo que escribió otro; si una prueba lo contradice, añadir una nota `⚠️` debajo (ver cabecera de `lecciones.md`).
- Mensajes de commit que empiecen por el nombre de la persona: `"[Aleix] Añade trozo B del proyecto jardín"`.

## Transcribir audio
- Para saber qué dice un vídeo: subir el mp3 a `sistema/transcribir/<persona>_<nombre>.mp3`, push, esperar ~1 min, pull. Aparecen `.txt` y `_palabras.json` con tiempos. Luego mover a `sistema/transcribir/archivo/`.

## Después de cada generación
- Revisar fotograma a fotograma antes de entregar (caras, cortes entre trozos, colores).
- Añadir una fila a `aprendizajes/registro-generaciones.md`.
- Si se aprende algo nuevo, añadirlo a `aprendizajes/lecciones.md`; si un prompt funciona bien, a `prompts-que-funcionan.md`.

## Configuración
- Cómo conecta cada miembro su Claude con GitHub y APIMart: `CONFIGURACION-EQUIPO.md`.
