# Registro de generaciones — NailCheck

Cada generación que lanza cualquiera del equipo, con su coste y lo que aprendimos.

**Cómo añadir:** una fila nueva AL FINAL de la tabla (no editar filas de otros). Hacer `pull` justo antes y `push` justo después.

| Fecha | Quién | Proyecto | Modelo | Qué se pidió | Resultado | Coste ($) | Lección |
|---|---|---|---|---|---|---|---|
| 2026-10-18 | Xavi | 2026-10-18_xavi_el-problema-amigos | seedance-2.0-face | Cambiar chico y chica por dos amigos (chico con gorra beige y camiseta roja de Marruecos) en vídeo de 8 s con 2 planos (barra + pasillo), una pasada | ⚠️ Barra perfecta (caras, gorra, camiseta 5); el pasillo salió igual que el original | 1,37 | En 2 planos el 2º se relaja: generarlo aparte |
| 2026-10-18 | Xavi | 2026-10-18_xavi_el-problema-amigos | seedance-2.0-face | Solo el pasillo (4 s) con fotos de espalda | ❌ Falló sin coste: "Aspect ratio must be between 0.4 and 2.5" | 0 | Fotos de cuerpo entero demasiado alargadas: recortar a ≥ 0,4 de ancho/alto |
| 2026-10-18 | Xavi | 2026-10-18_xavi_el-problema-amigos | seedance-2.0-face | Solo el pasillo (4 s), fotos busto+cara de él y cara de ella, describiendo la espalda y la acción ("he carries her…") | ✅ Camiseta roja, gorra, chica rubia, él la lleva cargada | 0,69 | Plano lejano y oscuro: basta con ropa y pelo bien descritos |
