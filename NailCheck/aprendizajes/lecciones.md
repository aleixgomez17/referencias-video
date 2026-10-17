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
