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

*(Todavía ninguna. Cuando un prompt funcione, añadirlo aquí con modelo, imágenes, coste y proyecto.)*
