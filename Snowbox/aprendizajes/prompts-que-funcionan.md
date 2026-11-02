# Prompts que han funcionado — Snowbox

Plantillas reales que dieron buen resultado. Copiar, cambiar lo que va entre [corchetes] y lanzar.

Las de cambiar persona, cara o prenda en un vídeo real están en `../../BackAlign/aprendizajes/prompts-que-funcionan.md` (plantillas A–F). Aquí van las que sirven en general y las nuevas de Snowbox.

---

## D. Avatar realista con GPT Image 2 (común)

**Modelo:** `gpt-image-2` · `size: 9:16`, `resolution: 2k` · **Coste:** ~0,014 $
**Origen:** BackAlign (Aleix)

```
Candid smartphone photo of a real [40]-year-old [Spanish] woman from [Madrid], head-and-shoulders portrait looking at the camera with a soft natural half smile. [Mediterranean features], skin with real texture: visible pores, a few freckles, subtle fine lines around the eyes and mouth, no makeup except a little mascara. [Shoulder-length wavy dark brown hair], slightly messy, natural. Wearing a plain [beige fitted cotton tank top]. Shot on an iPhone front camera, soft natural window daylight, slightly blurred home background. Realistic UGC look, unretouched, natural colors, no beauty filter, no studio lighting, no glamour, not a model.
```

## G. Producto pequeño o con detalle impreso: fotograma editado + imagen→vídeo (común)

**Modelos:** `gpt-image-2` (editar el 1er fotograma) + `seedance-2.0` sin vídeo de referencia
**Origen:** NailCheck, nightnail-clips (Aleix, 2026-10-18) · **Coste:** ~0,01 $ + ~0,71 $ por 5 s

Paso 1 — `gpt-image-2`, imagen 1 = primer fotograma del clip, imagen 2 = foto limpia del producto:
```
Edit image 1: replace the [objeto que sostiene / que está sobre la mesa] with the product from image 2, keeping its exact design, colors and printed details. Everything else in image 1 stays the same: same person, hands, pose, room, lighting and framing.
```

Paso 2 — `seedance-2.0`, imagen 1 = fotograma editado, sin vídeo:
```
Image 1 is the first frame of the video. [Describe la acción en positivo y en orden: she slowly opens the first door of the calendar and smiles]. Same person, same room, same lighting, natural handheld smartphone footage. No watermarks, no logos, no on-screen text.
```

*(Las indicaciones entre corchetes son de ejemplo; el método es el que funcionó, el texto exacto de NailCheck no quedó guardado.)*

---

## Plantillas de Snowbox

## S1. Escena nueva con el calendario: imagen→vídeo con inicio y final

**Modelos:** `gpt-image-2` (fotogramas, ~0,015 $ cada uno) + `seedance-2.0` · **Imágenes:** 1 = fotograma de inicio, 2 = fotograma final · **Sin vídeo** · `duration: 5`, `size: 9:16`, `resolution: 720p`, `generate_audio: false`
**Usado en:** familia-abre-caja1 (Xavi, 2026-11-02) · **Coste:** 0,71 $ por 5 s

Fotogramas: crear el final con GPT Image pasando la foto del calendario y dando la distribución fila a fila ("EXACTLY FOUR rows of SIX… Row 1: …"); luego el de inicio editando el final ("Change only this: …").

```
Image 1 is the first frame of the video. Image 2 shows the same family and the same calendar at the end of the video. Warm family home video at Christmas, filmed on a smartphone, same people, same room and same advent calendar shelf as image 1. [The girl in red reindeer pajamas takes red box number 1 off the top-left of the white calendar shelf, brings it down to her chest with both hands and lifts its lid to peek inside, like in image 2. Her brother leans in excitedly, the mother and father lean closer behind them, and all four smile and laugh together with genuine joy.] All the other numbered boxes [2 to 24] stay in their places on the shelf, unchanged. Same warm lighting, gentle slight handheld movement, natural realistic skin. No watermarks, no logos, no on-screen text.
```
