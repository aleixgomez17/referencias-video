# Lecciones aprendidas (vídeos con IA) — NailCheck

Reglas sacadas de pruebas reales del equipo. Antes de lanzar una generación, repasa esta lista (y también `../../BackAlign/aprendizajes/lecciones.md`, que tiene lo aprendido sobre modelos y prompts en general).

**Cómo aportar:**
- Lección nueva → añadirla con `(nombre, fecha, proyecto)` al final.
- Si tu prueba **contradice** una lección de otro, no la borres: añade debajo `⚠️ (nombre, fecha): en mi prueba pasó X` con el proyecto.
- Si tu prueba **confirma** una lección, añade `✔️ confirmado (nombre, fecha)`.

---

## Seedance

- **Vídeo de 2 planos en una pasada:** el primer plano cambia bien, pero el segundo (pasillo oscuro y lejano) salió idéntico al original. Generar el segundo plano aparte (4 s) y unirlo en el montaje. ✔️ confirma la lección 3 de BackAlign. *(Xavi, 2026-10-18, el-problema-amigos)*
- **Proporción de las imágenes de referencia:** ancho/alto entre **0,4 y 2,5**. Una foto de cuerpo entero (p. ej. 300×770) falla con "Aspect ratio must be between 0.4 and 2.5" (sin coste). Recortarla (hasta las rodillas) antes de subirla. *(Xavi, 2026-10-18, el-problema-amigos)*
- **Fotos de personas reales:** subirlas con `upload_image` de APIMart en vez de al repo (que es público). *(Xavi, 2026-10-18, el-problema-amigos)*
- **Que el avatar no hable con la boca:** con vídeo de referencia, seedance-face copia los movimientos de boca del original (también le pasó a Xavi en BackAlign). Solución que funcionó: tomar un fotograma ya generado con la boca cerrada como imagen 1 ("Image 1 is the first frame of the video"), añadir el producto como imagen 2, NO pasar vídeo, y describir la acción en positivo ("lips gently closed in a soft smile for the whole video"). Boca cerrada los 5 s. Coste 0,71 $ por 5 s (no es más barato que con vídeo de 5 s). *(Aleix, 2026-10-18, nightnail-clips)*
- **Pegatinas y detalles diminutos (uña, hoja de pegatinas):** editando el vídeo con seedance-2.0, la IA mantiene lo que había en el original (estrellas/mariposas en la hoja, uña sin pegatina) aunque le des la foto del producto. En cambio, objetos grandes como el sobre se cambian perfectamente. *(Aleix, 2026-10-18, nightnail-clips)*
- **Solución para detalles pequeños del producto:** editar el 1er fotograma del clip con GPT Image (0,01 $, imagen 1 = fotograma, imagen 2 = foto del producto) y animarlo con seedance imagen→vídeo ("Image 1 is the first frame of the video" + la acción descrita), sin vídeo de referencia. Los corazones se mantuvieron en la hoja y aparecieron en las uñas. Se pierde la sincronía exacta con el original. *(Aleix, 2026-10-18, nightnail-clips)*
- **Dos personas en el mismo vídeo:** a veces seedance-face solo cambia a una (viref1: cambió a la mujer y dejó al hombre). Arreglo fiable: segunda pasada usando el vídeo ya generado como referencia y pidiendo cambiar solo a la otra persona ("the woman … stays exactly as she is"). Cuesta otra pasada completa. *(Aleix, 2026-10-18, viref1-avatares)*
- **Textos relámpago:** algunos vídeos de TikTok tienen un texto que aparece solo 2-3 fotogramas; si no se borra, la IA lo copia. Revisar el original a 10 fps alrededor de cada cambio de texto. *(Aleix, 2026-10-18, viref1-avatares)*
- **Hacer una segunda pasada sobre un vídeo ya generado empeora la calidad:** en viref1 la 2ª pasada (para cambiar al hombre) dejó piel y fondo con textura "pintada"/granulosa y Aleix lo vio falso. Un retoque gratis (quitar ruido, subir a 1080 y añadir grano) apenas lo mejora. Mejor: cada persona en una pasada sobre el ORIGINAL y unirlas después. *(Aleix, 2026-10-18, viref1-avatares)*
- **Para que no parezca falso:** si el vídeo de referencia es de estudio/decorado, pedir en una pasada "Re-film the scene as real, candid smartphone footage shot on an iPhone in a real [lugar]" + describir el fondo real + "natural realistic skin with pores, slight handheld movement, slight grain, not a studio, no plastic skin". En viref1 el resultado ganó mucho realismo manteniendo personas y gestos. *(Aleix, 2026-10-18, viref1-avatares)*

## Retoques gratis (sin IA)

- **Vídeo torcido (móvil girado):** no usar Seedance. Medir el ángulo de las líneas verticales del fondo (OpenCV, Hough) y girar con ffmpeg: `rotate=ÁNGULO*PI/180:ow=iw:oh=ih:c=black,crop=…,scale=720:1280`. Con 10° en vertical hace falta un zoom de ×1,3 para que no queden esquinas negras. Coste 0 y no deforma los textos del producto. ⚠️ El `rotate` de ffmpeg gira al revés que `getRotationMatrix2D` de OpenCV: comprobar el resultado midiendo de nuevo. *(Xavi, 2026-10-18, video2toma1)*
