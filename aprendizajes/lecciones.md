# Lecciones aprendidas (vídeos con IA)

Reglas sacadas de pruebas reales, con su coste. Antes de lanzar una generación, repasa esta lista.
Cuando aprendamos algo nuevo, se añade aquí con la fecha y el proyecto donde lo vimos.

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

*(01-top-negro, 04-jardín)*

## 2. Cómo escribir el prompt

- **Corto y en forma de orden de edición.** "Replace the bra in video 1 with the top from image 1…". Si describes segundo a segundo lo que pasa en el vídeo original, el modelo entiende "cópialo" y lo copia. *(01)*
- **No digas "exactamente igual, fotograma a fotograma"** cuando quieres cambiar algo grande (la cara): el modelo lo toma literal y no cambia nada. En vez de eso: "Replace the woman in video 1 with the woman from image 1" y luego "same movements, same clothes, same place". *(04: 1,63 $ perdidos)*
- **Di las diferencias concretas** entre el original y lo que quieres, sobre todo si se parecen: "40 years old, fine lines, NO fringe/bangs; she is NOT the young woman from video 1". *(04)*
- **Describe el producto tal como se ve PUESTO**, no mientras se lo ponen. Error que tuvimos: escribimos "banda cruzada en X" y el top abrochado en realidad es una banda recta con corchetes en el centro. *(01)*
- **Indica el color en cada prenda y en cada momento**: "the top is BLACK in every shot", "loose light grey trousers, the same light grey in every shot". *(02)*
- **Tono de piel**: si no lo dices, puede salir muy bronceada → "fair, light natural skin, NOT tanned, real skin texture, no airbrushed look". *(02)*
- Pide siempre: "No watermarks, no logos, no on-screen text". Los textos los ponemos después en edición (la IA los deforma).

## 3. Vídeos con varios planos → trocear

- En un vídeo con varios cortes, **la IA aplica bien el cambio en el primer plano y en los siguientes se relaja** (vuelve el sujetador original, vuelve la cara original). *(01, 04)*
- **Solución que funciona:** cortar el vídeo en trozos por cambios de plano y **que cada trozo empiece con el plano importante** (el de frente, el que enseña la cara o el producto).
- Para cada trozo, dar las referencias que le tocan: foto de frente para planos de frente, foto de espalda para planos de espalda.
- **Inconveniente:** entre trozos puede cambiar algo (color del pantalón, la habitación, la cara). Se evita describiendo esos elementos igual en todos los prompts y, para la cara, ver el punto 5.

## 4. Límites técnicos de Seedance (vía APIMart)

- Vídeo de referencia: **más de 1,8 s y menos de 15,2 s**, resolución **máx. 720p** (bajar los vídeos 1080p).
- Duración de salida: **4 a 15 s** (número entero).
- Si un trozo dura menos de 1,8 s: **alargarlo congelando el último fotograma** (`tpad`) hasta 4 s, generar, y luego quedarnos solo con la parte buena. *(04)*
- La salida casi nunca dura exactamente lo mismo que la referencia: se reajusta la velocidad en el montaje.
- `generate_audio: false` y **poner el audio original nosotros** en el montaje. (La opción de conservar audio da error en la conexión.)

## 5. Avatares y caras

- **Foto solo de la cara** (sin fondo ni cuerpo): si das una foto con habitación, **la IA copia esa habitación** como fondo. *(03)*
- **Para que la cara sea la misma en todos los trozos:** usar como imagen 1 **un fotograma de la cara tal como salió en el primer trozo generado**, y la foto del avatar como imagen 2. *(04: arreglado así)*
- Los primeros fotogramas de un vídeo con planos muy cortos (< 0,5 s) a veces se quedan con la cara original → revisarlos y recortarlos. *(03)*
- GPT Image 2 **bloquea la palabra "sujetador/bra"** → pedir "beige fitted tank top" y el producto ya lo pone el vídeo. *(03)*

## 6. Referencias de producto

- Siempre **una foto de frente y una de espalda**, del producto puesto, en el color que queremos.
- **Quitar flechas, textos o gráficos** de las fotos: la IA los pega en el vídeo tal cual. *(01: salió la imagen con flechas incrustada)*
- Que en la foto se vea el detalle que importa (p. ej. el cierre de la espalda).

## 7. Retoques que se hacen sin IA (gratis)

- Quitar un plano malo y reajustar la velocidad para no cortar el audio.
- Borrar una franja o borde pixelado en la tela de un plano concreto.
- Poner textos, el audio original, recortar a 9:16, quitar la pantalla final de TikTok.

## 8. Antes de entregar un vídeo

1. Sacar fotogramas cada ~0,5 s y compararlos con el original.
2. Comparar de cerca la cara del principio, la del final y la del avatar.
3. Revisar los cortes entre trozos (fotogramas sueltos del original, cambios de color).
4. Decir el coste y lo que no ha salido bien.
