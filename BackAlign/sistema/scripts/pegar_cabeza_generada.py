"""Pega la cabeza y el pelo del vídeo generado sobre el vídeo original (cuerpo y prenda originales).
uso: python3 cabeza.py <original> <generado_misma_duracion_y_fps> <salida> [factor_bajo_barbilla]"""
import sys, cv2, numpy as np
from insightface.app import FaceAnalysis
orig, gen, outp = sys.argv[1], sys.argv[2], sys.argv[3]
k = float(sys.argv[4]) if len(sys.argv) > 4 else 0.45
app = FaceAnalysis(name='buffalo_l', allowed_modules=['detection'], providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
a = cv2.VideoCapture(orig); b = cv2.VideoCapture(gen)
w, h, fps = int(a.get(3)), int(a.get(4)), a.get(5)
out = cv2.VideoWriter(outp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
cut = None; n = 0
while True:
    ok1, fo = a.read(); ok2, fg = b.read()
    if not (ok1 and ok2): break
    faces = app.get(fg) or app.get(fo)
    if faces:
        f = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
        x1, y1, x2, y2 = f.bbox; fh = y2 - y1
        c = int(y2 + k * fh)
        cut = c if cut is None else int(0.6 * cut + 0.4 * c)
    if cut is None: cut = h // 3
    ys = np.arange(h, dtype=np.float32)[:, None]
    m = np.clip((cut + 25 - ys) / 50.0, 0, 1)[..., None]
    fr = (fg.astype(np.float32) * m + fo.astype(np.float32) * (1 - m)).astype(np.uint8)
    out.write(fr); n += 1
out.release(); print('frames', n)
