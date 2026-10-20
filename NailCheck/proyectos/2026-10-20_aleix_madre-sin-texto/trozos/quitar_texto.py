"""Borra un texto fijo blanco (con contorno) y opcionalmente un emoji, por fotogramas.
uso: python3 quitar_texto.py <in_dir> <out_dir> x0,y0,x1,y1 [ex0,ey0,ex1,ey1]"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]
TX = [int(v) for v in sys.argv[3].split(',')]
EM = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else None
os.makedirs(dst, exist_ok=True)
files = sorted(glob.glob(src + '/*.png'))
acc = None
for f in files:
    r = cv2.imread(f)[TX[1]:TX[3], TX[0]:TX[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    w = ((hsv[..., 2] > 215) & (hsv[..., 1] < 45)).astype(np.float32)
    acc = w if acc is None else acc + w
m = (acc / len(files) > 0.85).astype(np.uint8)
m = cv2.dilate(m, np.ones((11, 11), np.uint8))
mask = np.zeros(cv2.imread(files[0]).shape[:2], np.uint8)
mask[TX[1]:TX[3], TX[0]:TX[2]] = m
if EM: mask[EM[1]:EM[3], EM[0]:EM[2]] = 1
for f in files:
    cv2.imwrite(os.path.join(dst, os.path.basename(f)), cv2.inpaint(cv2.imread(f), mask * 255, 9, cv2.INPAINT_TELEA))
print('px mascara:', int(mask.sum()))
