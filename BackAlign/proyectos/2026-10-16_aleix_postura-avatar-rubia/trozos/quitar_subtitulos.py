"""Borra subtítulos blancos que cambian en cada plano (franja inferior) y el texto grande final.
uso: python3 -I quitar_subtitulos.py <entrada.mp4> <salida.mp4>"""
import cv2, numpy as np, sys
src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
BANDS = [((940, 1045), 0.0, 9), ((740, 930), 23.0, 17)]   # (y0,y1), desde segundo, dilatación
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps; i += 1
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    mask = np.zeros(f.shape[:2], np.uint8)
    for (y0, y1), t0, dil in BANDS:
        if t < t0: continue
        w = ((hsv[y0:y1, ..., 2] > 200) & (hsv[y0:y1, ..., 1] < 60)).astype(np.uint8)
        if w.sum() < 150: continue
        mask[y0:y1] |= cv2.dilate(w, np.ones((dil, dil), np.uint8))
    if mask.any():
        f = cv2.inpaint(f, mask * 255, 7, cv2.INPAINT_TELEA)
    out.write(f)
out.release()
