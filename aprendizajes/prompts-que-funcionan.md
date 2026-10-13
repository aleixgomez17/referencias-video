# Prompts que han funcionado

Plantillas reales que dieron buen resultado. Copiar, cambiar lo que va entre [corchetes] y lanzar.

---

## A. Cambiar el producto en un vídeo real (misma persona)

**Modelo:** `seedance-2.0` · **Imágenes:** 1 = producto de frente, 2 = producto de espalda · **Vídeo:** trozo de ≤ 8 s
**Usado en:** top-negro (trozo B) · **Coste:** ~0,86 $ por 5 s

```
Replace the bra the woman is wearing in video 1 with the top from image 1 and image 2, in [BLACK]. Front view must look like image 1: [seamless smooth scoop V-neck, wide straps, and a straight wide band under the bust with a small hook-and-eye panel in the center front]. Back view must look like image 2: [racerback with a large U-shaped cutout above a wide lower band with a small hook closure]. The top is [black] in every shot. Keep everything else from video 1 unchanged: the same woman, face, hair, movements, hands, camera, room, lighting and timing.
```

## B. Cambiar a la persona por un avatar + cambiar color del producto

**Modelo:** `seedance-2.0-face` · **Imágenes:** 1 = cara del avatar (solo cara), 2 = foto extra del avatar · **Vídeo:** ≤ 15 s
**Usado en:** salón · **Coste:** ~2,23 $ por 13 s

```
Replace the woman in video 1 with the woman from image 1 and image 2. She performs EXACTLY the same movements as the woman in video 1: same body motion, same hand and arm movements, same head turns, same timing. Her face, hair and body are from image 1 and image 2: [a 40-year-old Spanish woman with shoulder-length wavy dark brown hair, brown eyes, natural light olive skin with real texture]. Change only one more thing: every time the [leopard-print top] appears, it becomes a plain solid [BLACK] top with exactly the same shape as in video 1. Everything else stays exactly as in video 1: [trousers], the room, the lighting, the camera framing and the timing. No watermarks, no logos, no on-screen text.
```

## C. Cambiar la cara cuando el avatar se parece a la chica original

**Modelo:** `seedance-2.0-face` · **Imágenes:** 1 = fotograma de la cara ya generada (para mantener la misma cara), 2 = foto del avatar
**Usado en:** jardín (trozo C v2) · **Coste:** ~0,69 $ por 4 s

```
Replace the woman in video 1 with the woman from image 1 and image 2. Image 1 shows exactly the face she must have: copy this exact face, same facial features, same eyes, eyebrows, nose, smile and skin, so she looks like the same person. Image 2 is extra reference of the same woman. She is about [40] years old, [Spanish, brown eyes, NO fringe and NO bangs]. Do not keep the young woman's face from video 1. Her hair is [tied up with a white claw clip], exactly as in video 1. She performs the same movements as in video 1: [describe brevemente el gesto]. Same [clothes], [place] and camera framing. No watermarks, no logos, no on-screen text.
```

## D. Avatar realista con GPT Image 2

**Modelo:** `gpt-image-2` · `size: 9:16`, `resolution: 2k` · **Coste:** ~0,014 $

```
Candid smartphone photo of a real [40]-year-old [Spanish] woman from [Madrid], head-and-shoulders portrait looking at the camera with a soft natural half smile. [Mediterranean features], skin with real texture: visible pores, a few freckles, subtle fine lines around the eyes and mouth, no makeup except a little mascara. [Shoulder-length wavy dark brown hair], slightly messy, natural. Wearing a plain beige fitted cotton tank top. Shot on an iPhone front camera, soft natural window daylight, slightly blurred home background. Realistic UGC look, unretouched, natural colors, no beauty filter, no studio lighting, no glamour, not a model.
```

## E. Cambiar a la persona por un avatar en un vídeo de un solo plano (incluye cambio de pelo)

**Modelo:** `seedance-2.0-face` · **Imágenes:** 1 = cara del avatar recortada sin fondo, 2 = foto entera del avatar · **Vídeo:** ≤ 15 s, un plano
**Usado en:** morena-avatar-rubia45 (Xavi) · **Coste:** ~2,58 $ por 15 s

```
Replace the woman in video 1 with the woman from image 1 and image 2, in EVERY frame of the video, from the first frame to the last, including when [the top covers part of her face] and when her face is partly out of frame. She is about [45] years old, with [long straight dark-blonde hair with lighter highlights falling past her shoulders, hazel-green eyes], light natural skin with real texture and fine lines, NOT tanned. She is NOT [the young woman with the short brown bob] from video 1: her hair is [LONG and BLONDE] in every frame. She performs the same movements as in video 1, [puts on the same black top in the same way], and has the same hands, jewellery and [jeans]. Same room, lighting, camera framing and timing. The top is [BLACK] in every frame. No watermarks, no logos, no on-screen text.
```
