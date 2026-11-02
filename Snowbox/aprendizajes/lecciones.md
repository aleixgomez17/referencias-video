# Lecciones aprendidas (vídeos con IA) — Snowbox

Reglas sacadas de pruebas reales del equipo. Antes de lanzar una generación, repasa esta lista.

Las secciones 1 a 8 son las **lecciones comunes** a todos los proyectos, copiadas de `../../BackAlign/aprendizajes/lecciones.md` y `../../NailCheck/aprendizajes/lecciones.md` el 2026-11-02 (se han dejado fuera las que solo sirven para sujetadores o pegatinas). Los originales siguen allí y pueden tener lecciones nuevas: échales un vistazo también. La sección 9 es solo de Snowbox.

**Cómo aportar:**
- Lección nueva → añadirla en la sección que toque con `(nombre, fecha, proyecto)` al final.
- Si tu prueba **contradice** una lección de otro, no la borres: añade debajo `⚠️ (nombre, fecha): en mi prueba pasó X` con el proyecto. Cuando haya 2 pruebas que lo confirmen, se corrige la regla.
- Si tu prueba **confirma** una lección, añade `✔️ confirmado (nombre, fecha)`.
- Si una lección de Snowbox sirve para todos, añádela también en BackAlign.

---

## 1. Qué modelo usar

| Para qué | Modelo | Resultado real |
|---|---|---|
| **Editar un vídeo real** (cambiar objeto, color, fondo) | `seedance-2.0` (normal) | ✅ Mantiene la persona y la escena reales. Es el que mejor ha funcionado. |
| Cambiar la **cara** por un avatar | `seedance-2.0-face` | ✅ Acepta caras realistas de avatar (el `seedance-2.0` normal las bloquea). |
| Editar con mejor calidad o vídeos largos | `seedance-2.5` | ✅ `size: "adaptive"`, `duration: -1` (4–30 s de una vez). Calidad superior; ≈ 0,25–0,26 $/s. Probarlo cuando 2.0-face devuelve el vídeo sin cambios. *(Aleix 2026-10-24, Xavi 2026-10-26)* |
| Pruebas baratas | `seedance-2.0-fast` | ❌ Con vídeo de referencia **copia el original casi sin cambios**. No usar para editar. |
| Editar con Kling | `kling-video-o1` | ❌ A través de la conexión de APIMart **ignora el vídeo** y genera uno nuevo desde cero. |
| Editar con Wan | `wan2.7-videoedit` | ❌ No consigue descargar los archivos de GitHub. No usar. |
| Crear avatar / imágenes / editar un fotograma | `gpt-image-2` | ✅ Muy realista. ~0,01–0,014 $ por imagen. |

## 2. Cómo escribir el prompt

- **Corto y en forma de orden de edición** ("Replace the … in video 1 with … from image 1"). Si describes segundo a segundo el vídeo original, el modelo entiende "cópialo". *(Aleix, top-negro)*
- **No digas "exactamente igual, fotograma a fotograma"** cuando quieres cambiar algo grande: lo toma literal y no cambia nada. Mejor: "Replace X with Y" y luego "same movements, same place". *(Aleix, jardín: 1,63 $ perdidos)*
- **Di las diferencias concretas** entre el original y lo que quieres ("she is NOT the young woman from video 1"). *(Aleix, jardín)*
- **Describe el producto tal como se ve en uso** y **el color en cada momento** ("… in every shot"). *(Aleix, top-negro / leopardo)*
- **Tono de piel:** si no lo dices puede salir muy bronceada → "fair, light natural skin, NOT tanned, real skin texture, no airbrushed look". *(Aleix, leopardo)*
- **Las órdenes en negativo no quitan lo que está en el vídeo de referencia** (detalles pequeños y gestos de boca se heredan). Describir en positivo. *(Xavi, 2026-10-13)*
- **Si la IA se salta o resume una acción larga**, describir las acciones en orden con "at the same moments" y hacerlo en una sola pasada. *(Aleix, 2026-10-17, a51)*
- Pide siempre: "No watermarks, no logos, no on-screen text". **Los textos los ponemos después en el montaje** (la IA los deforma).
- **Para que no parezca falso** (referencia de estudio/decorado): "Re-film the scene as real, candid smartphone footage shot on an iPhone in a real [lugar]" + fondo real + "natural realistic skin with pores, slight handheld movement, slight grain, not a studio, no plastic skin". *(Aleix, 2026-10-18, viref1)*
- **Filtro de contenido** (`OutputVideoSensitiveContentDetected`): falla sin coste; reintentar con otra `seed` y "casual everyday video". *(Aleix, 2026-10-16)*

## 3. Vídeos con varios planos

- En un vídeo con varios cortes, **la IA aplica bien el cambio en el primer plano y en los siguientes se relaja**. Solución: trocear por cambios de plano, que cada trozo empiece con el plano importante, y describir igual en todos los prompts lo que debe mantenerse. *(Aleix, top-negro / jardín; Xavi, 2026-10-18, el-problema-amigos)*
- Con `seedance-2.0-face` insistir en "in EVERY shot of the video, from the first frame to the last" puede bastar para hacerlo en una pasada. *(Victor 2026-10-12, Xavi 2026-10-13)*
- **Si el vídeo tiene voz, generarlo de UNA sola pasada** (≤ 16–17 s acelerado a 15 s exactos, `duration: 15`, devolverle la velocidad en el montaje). Al trocear, la boca deja de ir con la voz. *(Aleix, 2026-10-15; Xavi, 2026-10-13/14)*
- **Vídeos sin voz de más de 15 s:** 2 partes lanzadas a la vez con **la misma foto de cara** como imagen 1. *(Aleix, 2026-10-16)*
- **Trozos consecutivos que hablan:** cortar en el segundo exacto, `duration: 15` cada uno, unir con corte seco + audio original; img1 del 2º trozo = fotograma de la cara del 1º ya generado. *(Xavi, 2026-10-25)*
- **Textos relámpago:** algunos vídeos de TikTok tienen un texto que aparece 2–3 fotogramas; si no se borra, la IA lo copia. Revisar el original a 10 fps alrededor de cada cambio de texto. *(Aleix, 2026-10-18)*

## 4. Límites técnicos de Seedance y APIMart

- Vídeo de referencia: **más de 1,8 s y menos de 15,2 s** (2.0), **máx. 720p**.
- Duración de salida: **4 a 15 s** enteros (2.5: hasta 30 s con `duration: -1`).
- Trozo < 1,8 s → alargarlo congelando el último fotograma (`tpad`) hasta 4 s y luego quedarse con la parte buena. *(Aleix, jardín)*
- La salida casi nunca dura lo mismo que la referencia: reajustar velocidad en el montaje. Acelerar la referencia (`setpts=PTS*15/16`) y devolverla después sincroniza bien. *(Xavi, 2026-10-13/14)*
- `generate_audio: false` y **poner el audio original nosotros** en el montaje.
- Imágenes de referencia: **≥ 300 px de ancho** (máx. 6000) y proporción ancho/alto **entre 0,4 y 2,5**; si no, falla sin coste. *(Xavi, 2026-10-14 / 2026-10-18)*
- Seedance lee las imágenes desde la URL `raw.githubusercontent.com` del repo: **tiene que ser público**. Fotos de personas reales → subirlas con `upload_image` de APIMart, no al repo. *(Xavi, 2026-10-13 / 2026-10-18)*
- **Tiempo de espera:** una tarea de 15 s puede tardar ~10–12 min y quedarse en "50 %". No relanzar mientras siga en "processing": se cobra dos veces. *(Xavi, 2026-10-25)*
- **Error 402 por saldo:** al reintentar con la MISMA `idempotency_key` devuelve el error guardado; reenviar con una key nueva (el fallo no cobra). *(Xavi, 2026-10-26)*
- **Una segunda pasada sobre un vídeo ya generado empeora la calidad** (piel y fondo "pintados") y tiende a copiarlo tal cual. Hacer cada cambio sobre el ORIGINAL. *(Aleix, 2026-10-18 / 2026-10-24)*

## 5. Avatares y caras

- **Foto solo de la cara** (sin fondo ni cuerpo): si das una foto con habitación, la IA copia esa habitación. Si tiene fondo, recortarla muy ajustada y ampliar a ≥ 500 px. *(Aleix, salón; Xavi, 2026-10-25)*
- **Misma cara en todos los trozos:** imagen 1 = fotograma de la cara del primer trozo generado, imagen 2 = foto del avatar. *(Aleix, jardín)*
- **Avatar con foto pequeña o mala:** rehacerla con `gpt-image-2` pasándola en `image_urls` ("Keep the exact identity… sharp head-and-shoulders portrait… plain light grey wall"), 0,009 $. *(Xavi, 2026-10-25)*
- **Cara "cuidada":** retocar la foto con `gpt-image-2` ("keep her exact identity… healthy smooth even skin, natural glow, well-rested, not plastic"). *(Aleix, 2026-10-16)*
- **Que el avatar NO hable:** img1 = foto de cara con labios cerrados y el prompt **empezando** por "A silent woman with her mouth closed the entire video: her lips stay together in a soft closed-lip smile in every single frame, exactly like the face in image 1". Solo funciona partiendo del vídeo ORIGINAL (otra persona). Alternativa sin vídeo: fotograma con boca cerrada como "Image 1 is the first frame of the video" + acción en positivo. *(Aleix 2026-10-18/23, Xavi 2026-10-25/26)*
- **Cuanto más distinto el pelo del avatar respecto al original, más fiable es el cambio.** *(Aleix, 2026-10-23)*
- **Dos personas en el mismo vídeo:** a veces solo cambia a una. Mejor cada persona en una pasada sobre el original y unir. *(Aleix, 2026-10-18)*
- Quitar tatuajes, piercings o pulseras: "Smooth arms with NO tattoos, no nose ring, no … bracelet" funcionó. *(Xavi, 2026-10-25)*

## 6. Referencias de producto

- **Quitar flechas, textos o gráficos** de las fotos de referencia: la IA los pega en el vídeo tal cual. *(Aleix, top-negro)*
- **Recortar las fotos para que solo se vea el producto:** si hay habitación u otra ropa, la IA la mete en el vídeo. *(Aleix, 2026-10-13)*
- **Detalles diminutos del producto** (dibujos pequeños, letras): editando vídeo con seedance la IA mantiene lo del original aunque des la foto; los objetos grandes sí se cambian bien. *(Aleix, 2026-10-18, nightnail)*
- **Solución para detalles pequeños:** editar el 1er fotograma con `gpt-image-2` (imagen 1 = fotograma, imagen 2 = producto, 0,01 $) y animarlo con seedance imagen→vídeo ("Image 1 is the first frame of the video" + acción descrita), sin vídeo de referencia. Se pierde la sincronía exacta con el original. *(Aleix, 2026-10-18, nightnail)*
- **Cambiar solo el color de algo:** no pasar foto de otro modelo distinto (mezcla los dos); pedir "the SAME … as in video 1… the only change is its color". Con foto del MISMO modelo sí ayuda. *(Aleix 2026-10-24, Xavi 2026-10-25)*

## 7. Retoques gratis (sin IA) — probar antes de gastar

- Quitar un plano malo y reajustar la velocidad; textos, audio original, recorte a 9:16, quitar la pantalla final de TikTok: todo con ffmpeg.
- **Borrar texto incrustado de la referencia** antes de generar (script `BackAlign/proyectos/2026-10-14_xavi_sujetador-definitivo-avatar-morena/trozos/quitar_texto.py`) y volver a poner el texto encima en el montaje para tapar la mancha. *(Xavi, 2026-10-14)*
- **Transcribir:** mp3 en `BackAlign/sistema/transcribir/<persona>_<nombre>.mp3` → push → ~1 min → pull. Cortar frases dejando ~0,08 s tras la palabra anterior. *(Aleix, 2026-10-13)*
- **Vídeo torcido:** medir el ángulo (OpenCV, Hough) y girar con ffmpeg `rotate`; ojo, gira al revés que OpenCV. *(Xavi, 2026-10-18)*
- **Solo cambiar la cara:** `BackAlign/sistema/scripts/cambiar_solo_cara.py` (inswapper), gratis y con boca sincronizada; no cambia pelo ni cuerpo. *(Xavi, 2026-10-25)*
- **Solo cambiar el fondo (cámara fija):** fondo nuevo por plano con `gpt-image-2` + `BackAlign/sistema/scripts/cambiar_fondo.py` (RobustVideoMatting). Persona, boca y audio 100 % originales. *(Xavi, 2026-10-28)*
- **Mejorar calidad al final:** `BackAlign/sistema/scripts/mejorar_caras.py` (GFPGAN al 70 %) + `scale=1080:1920:flags=lanczos,unsharp=5:5:0.4`, CRF 14. Lento (~5 s/fotograma). *(Aleix, 2026-10-23)*
- **Pasar subtítulos de un vídeo a otro:** `BackAlign/sistema/scripts/copiar_subtitulos.py`. *(Aleix, 2026-10-23)*

## 8. Antes de entregar un vídeo

1. Sacar fotogramas cada ~0,5 s (o 1 fps) y compararlos con el original.
2. Comparar de cerca caras del principio, del final y del avatar.
3. Revisar los cortes entre trozos (fotogramas sueltos del original, cambios de color).
4. Decir el coste y lo que no ha salido bien, y apuntarlo en `registro-generaciones.md`.

---

## 9. Lecciones propias de Snowbox (calendarios, planners, juegos)

- **Cambiar los productos de una estantería de tienda por el calendario** con `seedance-2.0` (img1 = foto del calendario recortada, sin el salón) funciona en una pasada: las estanterías salen llenas de cajitas numeradas con los colores y el estilo del calendario. Pero salen **cajas sueltas** (no la estantería de madera entera) y **los números se repiten o se deforman** (13, 23 dos veces, un "5" raro). Si se ve de cerca, tapar los números en el montaje o probar con imagen→vídeo (plantilla G). *(Xavi, 2026-11-02, tienda-calendario: 0,69 $ por 4 s)*
- **Con `seedance-2.0` normal, pedir "remove every store logo" no quitó los logos grandes de la tienda** (las dianas rojas de Target) ni "slightly different facial features" cambió a la mujer: el vídeo de referencia manda. ✔️ confirma la lección 2 (las órdenes de quitar algo del vídeo no funcionan). Para la cara usar `seedance-2.0-face` o `cambiar_solo_cara.py` (gratis). *(Xavi, 2026-11-02, tienda-calendario)*
- Parámetros que aceptó `seedance-2.0` para vídeo vertical: `video_urls`, `image_urls`, `duration: 4`, `size: "9:16"`, `resolution: "720p"`, `generate_audio: false`. Tardó ~4 min y devolvió 4,04 s a 24 fps; se estiró a 4,13 s y se subió a 1080×1920 gratis con ffmpeg (lanczos + unsharp). *(Xavi, 2026-11-02, tienda-calendario)*
- **Imagen→vídeo: NO usar `first_frame_image` ni `last_frame_image` en seedance-2.0 vía APIMart.** Las ignoró por completo: salió otra familia y otro calendario inventado (0,71 $ perdidos). Ya le pasó a Xavi el 24-10 en BackAlign (cambió persona y fondo). Lo que sí funcionó en NailCheck: pasar la imagen en `image_urls` y empezar el prompt con "Image 1 is the first frame of the video". *(Xavi, 2026-11-02, familia-abre-caja1)*
- **GPT Image con estanterías numeradas:** a la primera puso 5 filas con números repetidos. Arreglo: editar esa imagen pasando también la foto del calendario recortada y escribir la distribución fila a fila ("Row 1: 2, 3, 4, 5, 6… Every number appears only once"). Salió perfecta. Si una caja sobra, quitarla gratis rellenando el hueco con el color del fondo (OpenCV). *(Xavi, 2026-11-02, familia-abre-caja1)*
- ✅ **Imagen→vídeo con inicio y final que SÍ funciona:** `image_urls` = [fotograma de inicio, fotograma final] y el prompt empieza por "Image 1 is the first frame of the video. Image 2 shows the same family and the same calendar at the end of the video." Mantuvo personas, ropa, salón y calendario (números correctos) y la acción descrita salió bien a la primera. El encuadre final queda algo más abierto que la imagen 2. *(Xavi, 2026-11-02, familia-abre-caja1: 0,71 $ por 5 s)*
