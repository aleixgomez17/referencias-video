"""Borra el texto fijo blanco (con contorno) y el emoji de arriba del clip 1.
uso: python3 quitar_texto_clip1.py <carpeta_fotogramas_in> <carpeta_out>"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
files = sorted(glob.glob(src + '/*.png'))
TX = (150, 190, 570, 315)       # caja del texto
EM = (422, 240, 495, 310)       # caja del emoji
acc = None
for f in files[::4]:
    r = cv2.imread(f)[TX[1]:TX[3], TX[0]:TX[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    w = ((hsv[..., 2] > 220) & (hsv[..., 1] < 40)).astype(np.float32)
    acc = w if acc is None else acc + w
m = (acc / len(files[::4]) > 0.8).astype(np.uint8)
m = cv2.dilate(m, np.ones((11, 11), np.uint8))
mask = np.zeros(cv2.imread(files[0]).shape[:2], np.uint8)
mask[TX[1]:TX[3], TX[0]:TX[2]] = m
mask[EM[1]:EM[3], EM[0]:EM[2]] = 1
for f in files:
    img = cv2.imread(f)
    cv2.imwrite(os.path.join(dst, os.path.basename(f)), cv2.inpaint(img, mask * 255, 9, cv2.INPAINT_TELEA))
print('px mascara:', int(mask.sum()))
