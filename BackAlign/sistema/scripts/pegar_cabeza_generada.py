"""Pega del vídeo generado la cabeza (hasta un poco bajo la barbilla) y el pelo a los lados,
pero el pelo solo donde en el ORIGINAL no hay piel (hombros, cuello y prenda salen siempre del original).
uso: python3 cabeza4.py <original> <generado> <salida>"""
import sys, cv2, numpy as np
from insightface.app import FaceAnalysis
orig, gen, outp = sys.argv[1], sys.argv[2], sys.argv[3]
app = FaceAnalysis(name='buffalo_l', allowed_modules=['detection'], providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
a = cv2.VideoCapture(orig); b = cv2.VideoCapture(gen)
w, h, fps = int(a.get(3)), int(a.get(4)), a.get(5)
out = cv2.VideoWriter(outp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
st = None; n = 0
Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
while True:
    ok1, fo = a.read(); ok2, fg = b.read()
    if not (ok1 and ok2): break
    faces = app.get(fg) or app.get(fo)
    if faces:
        f = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
        x1, y1, x2, y2 = f.bbox; cur = np.array([(x1 + x2) / 2, y2, x2 - x1, y2 - y1], np.float32)
        st = cur if st is None else 0.6 * st + 0.4 * cur
    if st is None: st = np.array([w / 2, h / 4, 200, 250], np.float32)
    cx, chin, fw, fh = st
    head = np.clip((chin + 0.2 * fh - Y) / 30.0, 0, 1) * np.clip((0.75 * fw - np.abs(X - cx)) / 30.0, 0, 1)
    upper = np.clip((chin - 0.1 * fh - Y) / 30.0, 0, 1)                   # todo lo que está por encima de la barbilla
    side = np.clip((chin + 0.7 * fh - Y) / 40.0, 0, 1)
    ho = cv2.cvtColor(fo, cv2.COLOR_BGR2HSV)
    skin = (((ho[..., 0] < 25) | (ho[..., 0] > 165)) & (ho[..., 1] > 35) & (ho[..., 2] > 70)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    skin = cv2.GaussianBlur(cv2.dilate(skin, np.ones((9, 9), np.uint8)).astype(np.float32), (21, 21), 0)
    lower = side * (1 - skin)
    m = np.clip(np.maximum(np.maximum(head, upper), lower), 0, 1)[..., None]
    fr = (fg.astype(np.float32) * m + fo.astype(np.float32) * (1 - m)).astype(np.uint8)
    out.write(fr); n += 1
out.release(); print('frames', n)
