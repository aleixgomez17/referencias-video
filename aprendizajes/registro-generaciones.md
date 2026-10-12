# Registro de generaciones

Cada generación que lanza cualquiera del equipo, con su coste y lo que aprendimos.

**Cómo añadir:** una fila nueva AL FINAL de la tabla (no editar filas de otros). Hacer `pull` justo antes y `push` justo después.

| Fecha | Quién | Proyecto | Modelo | Qué se pidió | Resultado | Coste ($) | Lección |
|---|---|---|---|---|---|---|---|
| 2026-10-10 | Aleix | 2026-10-10_aleix_top-negro-chica-rubia | seedance-2.0-fast | Cambiar sujetador del vídeo entero (prompt largo) | ❌ Casi igual al original + plano con la foto de flechas pegada | 0,92 | Fast copia; prompt largo = copia; quitar gráficos de las referencias |
| 2026-10-10 | Aleix | 2026-10-10_aleix_top-negro-chica-rubia | wan2.7-videoedit | Editar vídeo (2 intentos) | ❌ No pudo descargar los archivos | 0 | Wan no lee GitHub |
| 2026-10-10 | Aleix | 2026-10-10_aleix_top-negro-chica-rubia | kling-video-o1 | Editar vídeo | ❌ Ignoró el vídeo, chica y escena nuevas | 0,34 | Kling vía conexión no edita |
| 2026-10-10 | Aleix | 2026-10-10_aleix_top-negro-chica-rubia | seedance-2.0 | Prueba trozo puesto, prompt corto | ⚠️ Edita de verdad, pero solo cambió el 1er plano | 0,77 | Prompt corto funciona; el cambio se pierde en los planos siguientes |
| 2026-10-10 | Aleix | 2026-10-10_aleix_top-negro-chica-rubia | seedance-2.0 | Trozo A (en la mano) + trozo B (puesto), foto frente + espalda | ✅ Top correcto delante y detrás | 1,55 | Trocear + referencias de frente y espalda |
| 2026-10-10 | Aleix | 2026-10-10_aleix_leopardo-avatar-rubia-top-beige | seedance-2.0-face | Avatar rubia + top beige, 2 trozos | ⚠️ Funciona, pero piel muy morena, pantalón cambia de color entre trozos, movimiento raro al inicio | 2,66 | Especificar tono de piel y color de cada prenda en todos los trozos |
| 2026-10-10 | Aleix | 2026-10-10_aleix_leopardo-avatar-rubia-top-beige | seedance-2.0-face | Igual + dormitorio + piel clara + pantalón gris | ⚠️ Mejor; aún algo bronceada; habitación cambia un poco entre trozos | 2,66 | — |
| 2026-10-10 | Aleix | 2026-10-10_aleix_salon-avatar-es40-top-negro | gpt-image-2 | Avatar española 40 años (cara + cuerpo) | ✅ Muy realista; la de cuerpo con "sujetador" fue bloqueada (0 $) | 0,03 | No usar "bra" en GPT Image |
| 2026-10-10 | Aleix | 2026-10-10_aleix_salon-avatar-es40-top-negro | seedance-2.0-face | Avatar es40 + leopardo→negro (13 s, 1 trozo) | ✅ Avatar y top negro; ⚠️ fondo = salón de la foto del avatar; primeros 0,75 s con cara original | 2,23 | Usar foto solo de cara si se quiere el fondo original |
| 2026-10-11 | Aleix | 2026-10-11_aleix_jardin-avatar-es40 | seedance-2.0-face | Solo cara, "todo igual fotograma a fotograma" | ❌ No cambió la cara | 1,63 | No pedir "exactamente igual" al cambiar la cara |
| 2026-10-11 | Aleix | 2026-10-11_aleix_jardin-avatar-es40 | seedance-2.0-face | "Sustituye a la mujer" + diferencias (edad, sin flequillo) | ⚠️ Solo el 1er plano con avatar | 1,63 | El cambio solo aguanta el primer plano |
| 2026-10-11 | Aleix | 2026-10-11_aleix_jardin-avatar-es40 | seedance-2.0-face | Trozos B y C que empiezan con la cara | ⚠️ C bien; B se saltó el plano de frente | 1,37 | Trozos cortos alargados con fotograma congelado funcionan |
| 2026-10-11 | Aleix | 2026-10-11_aleix_jardin-avatar-es40 | seedance-2.0-face | Trozo C con fotograma de la cara del inicio como imagen 1 | ✅ Misma cara que al principio | 0,69 | Usar fotograma generado para mantener la cara entre trozos |
| 2026-10-12 | Victor | 2026-10-12_victor_tanga-avatar-rubia | seedance-2.0-face | Avatar rubia en vídeo entero de 14 s y 9 planos (sin trocear), imagen 1 = cara recortada sin fondo, imagen 2 = cara.png; prompt "in EVERY shot… also when seen from behind" | ✅ Rubia en todos los planos, también de espalda y desde el 1er fotograma; misma cara; top y braguita negros correctos. ⚠️ Vaqueros algo más claros que el original | 2,40 | Con un prompt que insiste en "cada plano, también de espalda" el cambio aguantó todo el vídeo de una pasada |

**Gastado por Aleix hasta 2026-10-12:** ~16,5 $ (cada uno paga con su propia cuenta de APIMart)
