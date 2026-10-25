# Lecciones aprendidas (vídeos con IA)

Reglas sacadas de pruebas reales del equipo. Antes de lanzar una generación, repasa esta lista.

**Cómo aportar:**
- Lección nueva → añadirla en la sección que toque con `(nombre, fecha, proyecto)` al final.
- Si tu prueba **contradice** una lección de otro, no la borres: añade debajo `⚠️ (nombre, fecha): en mi prueba pasó X` con el proyecto. Cuando haya 2 pruebas que lo confirmen, se corrige la regla.
- Si tu prueba **confirma** una lección, añade `✔️ confirmado (nombre, fecha)`.
- Las lecciones sin autor son de Aleix (10–12 oct 2026), proyectos de la carpeta `proyectos/`.

---

## 1. Qué modelo usar

| Para qué | Modelo | Resultado real |
|---|---|---|
| **Editar un vídeo real** (cambiar prenda, color, cara) | `seedance-2.0` (normal) | ✅ Mantiene la persona y la escena reales. Es el que mejor ha funcionado. |
| Cambiar la **cara** por un avatar | `seedance-2.0-face` | ✅ Acepta caras realistas de avatar (el `seedance-2.0` normal las bloquea). |
| Pruebas baratas | `seedance-2.0-fast` | ❌ Con vídeo de referencia **copia el original casi sin cambios**. No usar para editar. |
| Editar con Kling | `kling-video-o1` | ❌ A través de la conexión de APIMart **ignora el vídeo** y genera uno nuevo desde cero (otra chica, otra escena). Solo sirve desde la web de APIMart en modo edición. |
| Editar con Wan | `wan2.7-videoedit` | ❌ No consigue descargar los archivos de GitHub (servidores de Alibaba). No usar. |
| Crear avatar / imágenes | `gpt-image-2` | ✅ Muy realista. Cuesta ~0,014 $ por imagen. |

*(proyectos top-negro y jardín)*

## 2. Cómo escribir el prompt

- **Corto y en forma de orden de edición.** "Replace the bra in video 1 with the top from image 1…". Si describes segundo a segundo lo que pasa en el vídeo original, el modelo entiende "cópialo" y lo copia. *(top-negro)*
- **No digas "exactamente igual, fotograma a fotograma"** cuando quieres cambiar algo grande (la cara): el modelo lo toma literal y no cambia nada. En vez de eso: "Replace the woman in video 1 with the woman from image 1" y luego "same movements, same clothes, same place". *(jardín: 1,63 $ perdidos)*
- **Di las diferencias concretas** entre el original y lo que quieres, sobre todo si se parecen: "40 years old, fine lines, NO fringe/bangs; she is NOT the young woman from video 1". *(jardín)*
- **Describe el producto tal como se ve PUESTO**, no mientras se lo ponen. Error que tuvimos: escribimos "banda cruzada en X" y el top abrochado en realidad es una banda recta con corchetes en el centro. *(top-negro)*
- **Indica el color en cada prenda y en cada momento**: "the top is BLACK in every shot", "loose light grey trousers, the same light grey in every shot". *(leopardo)*
- **Tono de piel**: si no lo dices, puede salir muy bronceada → "fair, light natural skin, NOT tanned, real skin texture, no airbrushed look". *(leopardo)*
- **Las órdenes en negativo no quitan lo que está en el vídeo de referencia.** Con `seedance-2.0-face` pedimos "the top has NO loops or cords at the sides" y "mouth closed, she does NOT talk": salió idéntico (anillas y boca hablando copiadas del original). Los gestos de boca y los detalles pequeños del producto se heredan del vídeo. *(Xavi, 2026-10-13, morena-avatar-rubia45: 2,58 $ perdidos)*
- Pide siempre: "No watermarks, no logos, no on-screen text". Los textos los ponemos después en edición (la IA los deforma).

## 3. Vídeos con varios planos → trocear

- En un vídeo con varios cortes, **la IA aplica bien el cambio en el primer plano y en los siguientes se relaja** (vuelve el sujetador original, vuelve la cara original). *(top-negro, jardín)*
- **Solución que funciona:** cortar el vídeo en trozos por cambios de plano y **que cada trozo empiece con el plano importante** (el de frente, el que enseña la cara o el producto).
- Para cada trozo, dar las referencias que le tocan: foto de frente para planos de frente, foto de espalda para planos de espalda.
- **Inconveniente:** entre trozos puede cambiar algo (color del pantalón, la habitación, la cara). Se evita describiendo esos elementos igual en todos los prompts y, para la cara, ver el punto 5.
  ⚠️ (Victor, 2026-10-12, tanga-avatar-rubia): con `seedance-2.0-face` un vídeo de 14 s y 9 planos salió bien **en una sola pasada** (2,40 $) usando una foto solo de cara y un prompt que dice "Replace the woman… in EVERY shot of the video, from the first frame to the last, including the back views" + "her hair is BLONDE in every shot, also when seen from behind" + "She is NOT the dark-haired woman from video 1". Puede que la clave sea insistir en *cada plano*. Falta otra prueba que lo confirme.
  ✔️ confirmado en parte (Xavi, 2026-10-13, morena-avatar-rubia45): con el mismo enfoque ("in EVERY frame, from the first frame to the last, including when the top covers part of her face and when her face is partly out of frame") el avatar aguantó los 15 s de una pasada (2,58 $), incluso cambiando de pelo corto castaño a largo rubio. Pero mi vídeo era **un solo plano sin cortes**, así que no confirma del todo el caso de varios planos.

- **Si el vídeo tiene voz, generarlo de UNA sola pasada.** Al dividirlo en trozos, cada generación pone una cara algo distinta y, como Seedance devuelve segundos enteros (p. ej. 13 s para una referencia de 12,6 s), al reajustar la duración la boca deja de ir con la voz. Solución: dejar la referencia en ≤ 16–17 s (quitando alguna frase si hace falta), acelerarla a **15 s exactos**, pedir `duration: 15` y devolverle la velocidad en el montaje. ✔️ confirma la técnica de Xavi. (Aleix, 2026-10-15, tiktok-pecho-caido)

- **Cara "cuidada":** si la cara sale cansada o con mucha textura, retocar antes la foto del avatar con `gpt-image-2` pasándola en `image_urls` ("keep her exact identity… healthy smooth even skin, natural glow, well-rested, soft natural makeup, not plastic") y usar esa foto recortada solo a la cara como imagen 1. Ejemplo: `avatares/rubia/cara_cuidada_solo.png`. (Aleix, 2026-10-16, postura-avatar-rubia)
- **Vídeos sin voz de más de 15 s:** se pueden hacer en 2 partes lanzadas a la vez si las dos usan **la misma foto de cara** como imagen 1 (no un fotograma generado). Las caras salieron iguales. Cortar en un cambio de plano y ajustar cada parte a una duración entera (12 s, 13 s). (Aleix, 2026-10-16, postura-avatar-rubia)
- **Filtro de contenido de Seedance** (`OutputVideoSensitiveContentDetected`): falla sin coste. Reintentar con otra `seed` y añadiendo "fully covered, casual everyday try-on video" funcionó a la segunda. (Aleix, 2026-10-16, postura-avatar-rubia)

## 4. Límites técnicos de Seedance (vía APIMart)

- Vídeo de referencia: **más de 1,8 s y menos de 15,2 s**, resolución **máx. 720p** (bajar los vídeos 1080p).
- Duración de salida: **4 a 15 s** (número entero).
- Si un trozo dura menos de 1,8 s: **alargarlo congelando el último fotograma** (`tpad`) hasta 4 s, generar, y luego quedarnos solo con la parte buena. *(jardín)*
- La salida casi nunca dura exactamente lo mismo que la referencia: se reajusta la velocidad en el montaje.
- `generate_audio: false` y **poner el audio original nosotros** en el montaje. (La opción de conservar audio da error en la conexión.)
- Si la referencia dura un poco más de 15 s (p. ej. 16 s), **acelerarla un poco** (`setpts=PTS*15/16`) en vez de cortar, generar 15 s y en el montaje **devolverla a su velocidad** (`setpts=PTS*16/15`) con el audio original: quedó perfectamente sincronizado y no se pierde nada. *(Xavi, 2026-10-13, morena-avatar-rubia45)*
- Las imágenes de referencia deben medir **al menos 300 px de ancho** (y como máximo 6000). Si un recorte de cara sale más pequeño, ampliarlo (p. ej. a 500 px) antes de subirlo; si no, la tarea falla (sin coste). *(Xavi, 2026-10-14, sujetador-definitivo)*
- Acelerar ×1,19 (17,8 s → 15 s) y devolver la velocidad en el montaje también sincronizó bien. *(Xavi, 2026-10-14, sujetador-definitivo)*
- Seedance lee las imágenes directamente desde la URL `raw.githubusercontent.com` del repo, sin pasar por `upload_image`. **El repo tiene que ser público**: si está en privado, APIMart no puede leer nada. *(Xavi, 2026-10-13, morena-avatar-rubia45)*

## 5. Avatares y caras

- **Foto solo de la cara** (sin fondo ni cuerpo): si das una foto con habitación, **la IA copia esa habitación** como fondo. *(salón)*
- **Para que la cara sea la misma en todos los trozos:** usar como imagen 1 **un fotograma de la cara tal como salió en el primer trozo generado**, y la foto del avatar como imagen 2. *(jardín: arreglado así)*
- Los primeros fotogramas de un vídeo con planos muy cortos (< 0,5 s) a veces se quedan con la cara original → revisarlos y recortarlos. *(salón)*
- GPT Image 2 **bloquea la palabra "sujetador/bra"** → pedir "beige fitted tank top" y el producto ya lo pone el vídeo. *(salón)*

## 6. Referencias de producto

- Siempre **una foto de frente y una de espalda**, del producto puesto, en el color que queremos.
- **Quitar flechas, textos o gráficos** de las fotos: la IA los pega en el vídeo tal cual. *(top-negro: salió la imagen con flechas incrustada)*
- Que en la foto se vea el detalle que importa (p. ej. el cierre de la espalda).
- **Recortar las fotos de producto para que solo se vea la prenda.** Si en la foto la modelo lleva vaqueros o hay una habitación de fondo, la IA mete esos vaqueros y esa habitación en el vídeo. Usar `beige_frente_recorte.png` / `beige_espalda_recorte.png`. (Aleix, 2026-10-13, tiktok-pecho-caido)

## 7. Retoques que se hacen sin IA (gratis)

- Quitar un plano malo y reajustar la velocidad para no cortar el audio.
- Borrar una franja o borde pixelado en la tela de un plano concreto.
- Poner textos, el audio original, recortar a 9:16, quitar la pantalla final de TikTok.
- **Vídeos con texto incrustado (TikTok):** borrar el texto y las flechas de la referencia antes de generar (script `proyectos/2026-10-14_xavi_sujetador-definitivo-avatar-morena/trozos/quitar_texto.py`). La flecha desapareció del todo, pero **la IA copia la mancha borrosa** donde estaba el texto. Solución gratis: volver a poner el mismo texto encima en el montaje (fuente Inter SemiBold, blanco con contorno negro, misma posición) y la mancha queda tapada. *(Xavi, 2026-10-14, sujetador-definitivo)*
- **Borrar detalles pequeños oscuros del producto** (p. ej. anillas o cordones laterales sobre fondo claro): detectar las líneas negras finas pegadas al top y rellenarlas con *inpainting* de OpenCV fotograma a fotograma. Quedó limpio y sin parpadeo; solo quedan los puntos de enganche, muy pequeños. Script: `proyectos/2026-10-13_xavi_morena-avatar-rubia45/trozos/quitar_anillas.py`. *(Xavi, 2026-10-13, morena-avatar-rubia45)*

- **Transcribir lo que dice un vídeo** (para saber dónde cortar): subir el audio en mp3 a `sistema/transcribir/<persona>_<nombre>.mp3` y hacer push. GitHub lo transcribe solo con Whisper en ~1 min y deja `<nombre>.txt` (frases con tiempos) y `<nombre>_palabras.json` (cada palabra con su tiempo). Después mover todo a `sistema/transcribir/archivo/`. (Aleix, 2026-10-13, tiktok-pecho-caido)
- **Cortar frases de un vídeo:** cortar con los tiempos de palabra y dejar ~0,08 s de margen después del final de la palabra anterior; si no, se cuela una sílaba ("si no se te va…"). Volver a transcribir el corte para comprobar que se entiende. (Aleix, 2026-10-13, tiktok-pecho-caido)

## 8. Antes de entregar un vídeo

1. Sacar fotogramas cada ~0,5 s y compararlos con el original.
2. Comparar de cerca la cara del principio, la del final y la del avatar.
3. Revisar los cortes entre trozos (fotogramas sueltos del original, cambios de color).
4. Decir el coste y lo que no ha salido bien.

- **Si la IA se salta o resume una acción larga (p. ej. girarse y pasarse la banda por detrás), describir en el prompt las acciones en orden con "at the same moments" y hacerlo en una sola pasada de 15 s.** En A51 (2 partes, sin describir acciones) la parte 1 se adelantó 3 s e inventó un plano; en el mismo guion con otra chica, una pasada + acciones descritas salió clavado. Comparar siempre original vs generado a 1 fps antes de montar. (Aleix, 2026-10-17, a51-avatar-rubia / mujer-mayor-avatar-rubia)
- **Para que la IA no cambie la prenda del vídeo al cambiar la cara:** recortar la prenda de un fotograma del propio vídeo original (sin cara) y pasarla como imagen 2, con "Replace only the woman's face and hair… everything below her neck stays exactly as in video 1… the garment looks exactly like image 2". Sin esto, seedance convirtió el top con tiras en un palabra de honor normal. *(Aleix, 2026-10-23, rubia-tetona2-avatar)*
- **Avatar rubia → otra rubia no cambia; rubia → morena sí.** Cuanto más distinto el pelo del avatar respecto al original, más fiable es el cambio. *(Aleix, 2026-10-23, rubia-tetona2-avatar)*
- **Que el avatar no hable manteniendo el vídeo de referencia:** funcionó poner como imagen 1 un fotograma del avatar con la boca cerrada y empezar el prompt con "A silent woman with her mouth closed the entire video: her lips stay together in a soft closed-lip smile in every single frame, exactly like the face in image 1". Con la orden al final del prompt seguía hablando. ⚠️ matiza la lección de Xavi (2026-10-13): en negativo no funciona, pero así sí. *(Aleix, 2026-10-23, rubia-tetona2-avatar)*
- **Mejorar la calidad gratis al final:** `sistema/scripts/mejorar_caras.py` restaura las caras fotograma a fotograma con GFPGAN (modelo gfpgan_1.4.onnx de las releases de GitHub de facefusion-assets, models-3.0.0; detector buffalo_l de insightface) mezclado al 70 %, y después `scale=1080:1920:flags=lanczos,unsharp=5:5:0.4` + CRF 14. Ojos y piel mucho más definidos sin efecto plástico. Tarda ~5 s por fotograma con 2 núcleos (22 s de vídeo ≈ 1 h). *(Aleix, 2026-10-23, rubia-tetona2-avatar)*
- **Pasar subtítulos de un vídeo a otro:** si nos dan el vídeo original con subtítulos incrustados (estilo karaoke blanco/amarillo con contorno negro), `sistema/scripts/copiar_subtitulos.py` los aísla por color en la franja inferior (y 1300-1700 en 1080×1920), se queda con las letras que tienen contorno negro y las pega sobre nuestro vídeo final, sincronizado por tiempo (convertir antes el vídeo de subtítulos a 30 fps). Funciona aunque el vídeo con subtítulos esté algo ampliado. *(Aleix, 2026-10-23, rubia-tetona2-avatar)*
- **Cambiar solo el color de la prenda del vídeo:** NO pasar fotos del producto (si la foto es de otro modelo o la prenda está en otra posición, la IA mezcla las dos y parece que lleva dos sujetadores). Pedir "the SAME single garment as in video 1, with exactly the same shape, cut, straps and band; the only change is its color: the leopard print becomes plain solid BLACK". *(Aleix, 2026-10-24, leopardo-rubia-negro)*
- **La IA añade una prenda color carne bajo tops con mucho escote** (para "tapar"), aunque no se le dé foto de producto. Solución gratis: generar igualmente y luego pegar SOLO la cabeza y el pelo generados sobre el vídeo original con `sistema/scripts/pegar_cabeza_generada.py` (fundido a la altura de las clavículas). Funciona porque seedance mantiene casi exactas las posiciones del cuerpo. *(Aleix, 2026-10-24, morena-a-rubia)*
- **Foto del avatar con la boca cerrada:** si la foto de cara enseña los dientes, el avatar sale sonriendo con la boca entreabierta y parece que habla. Usar `avatares/rubia/cara_cuidada_boca_cerrada.png` (o hacer la versión con GPT Image, 0,01 $). *(Aleix, 2026-10-24, morena-a-rubia)*
- **Receta para cambiar solo la persona cuando la IA estropea la prenda:** (1) generar con seedance-face con la cara del avatar; (2) pegar cara y pelo generados sobre el vídeo original con `sistema/scripts/pegar_cabeza_generada.py`; (3) pasar ese montaje otra vez por seedance-face pidiendo "re-render clean… keep everything the same… fix only the skin tone continuity and the hair". Sale limpio, con el top original. Cuesta 2 pasadas por parte. *(Aleix, 2026-10-24, morena-a-rubia)*
  ⚠️ (Aleix, 2026-10-24): la receta de arriba NO funcionó al revisarla con calma: la pasada de limpieza copió el montaje con sus defectos (lección de 2026-10-11: pedir "todo igual" hace que copie). No usar esa receta. *(morena-a-rubia)*
- **Seedance 2.5 (nuevo):** para editar un vídeo hay que pasar `size: "adaptive"` y `duration: -1` (mismo formato y duración que el vídeo de referencia, entre 4 y 30 s, ¡30 s de una vez!). En la primera prueba (cambiar morena por rubia) la calidad y la prenda fueron muy superiores a 2.0-face y NO añadió la prenda color carne con escote, pero ignoró "boca cerrada" y la avatar habla. Coste ≈ 0,26 $/s. *(Aleix, 2026-10-24, morena-a-rubia)*
- **UGC hablando a cámara + avatar que sí debe hablar:** con `seedance-2.0-face`, plantilla E, img1 = cara del avatar sonriendo con dientes y img2 = recorte del sujetador sacado del propio vídeo, salió bien a la primera en 15 s: labios sincronizados con el audio original sin reajustar velocidad, prenda idéntica y sin prenda color carne en un escote en V profundo. ✔️ confirma la lección de Aleix (2026-10-23) de pasar el recorte de la prenda del propio vídeo. *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
- **Cambiar el tamaño del pecho funciona con una frase en el prompt:** "Her bust is noticeably fuller than in video 1, naturally filling the same bra" + "Casual everyday try-on video" → más pecho, mismo sujetador y sin saltar el filtro de contenido. *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
- **Foto del avatar con fondo (piscina, árboles):** recortarla muy ajustada a cara y pelo (y ampliar a ≥ 500 px) fue suficiente: la habitación del vídeo se mantuvo y no apareció nada del fondo de la foto. *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
- **Opción gratis antes de gastar:** si solo hay que cambiar la cara (mismo pelo y cuerpo), `sistema/scripts/cambiar_solo_cara.py` (inswapper_128 de facefusion-assets models-3.0.0 + buffalo_l) lo hace sin coste y mantiene la boca sincronizada; ~1,8 s por fotograma con 2 núcleos. No cambia pelo ni cuerpo. *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
- **Tiempo de espera de APIMart:** una tarea de 15 s se quedó ~10 min en "50 %" y terminó bien (11,5 min en total). No relanzar mientras siga en "processing": se cobraría dos veces. *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
- **Trozos consecutivos de un vídeo que habla (15 s + 15 s):** cortar el original en el segundo exacto, generar cada trozo con `duration: 15` y unirlos con corte seco + audio original: la pose encaja en el corte y la boca sigue sincronizada. Para que sea la misma mujer, img1 = fotograma de la cara del trozo anterior ya generado. No hizo falta `first_frame_image` (que en mi prueba del 24-10 cambió persona y fondo). ✔️ confirma la lección de la cara de "jardín". *(Xavi, 2026-10-25, morena-avatar-rubia-piscina)*
