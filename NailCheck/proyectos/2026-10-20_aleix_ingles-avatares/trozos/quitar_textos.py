"""Borra "The problem"+emojis (plano 1, fotogramas 0-107) y "Comment Safe to Get yours"+emoji (plano 2, 108-fin).
Texto fijo blanco: se detecta acumulando píxeles blancos que no se mueven en cada plano.
uso: python3 quitar_textos.py <in_dir> <out_dir>"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
fs = sorted(glob.glob(src + '/*.png'))
FASES = [((0, 108), (105, 232, 610, 305), (468, 232, 605, 305)),
         ((108, len(fs)), (85, 205, 645, 335), (455, 272, 540, 335))]
for (a, b), TX, EM in FASES:
    sub = fs[a:b]; acc = None
    for f in sub:
        r = cv2.imread(f)[TX[1]:TX[3], TX[0]:TX[2]]
        hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
        w = ((hsv[..., 2] > 210) & (hsv[..., 1] < 50)).astype(np.float32)
        acc = w if acc is None else acc + w
    m = (acc / len(sub) > 0.8).astype(np.uint8)
    m = cv2.dilate(m, np.ones((17, 17), np.uint8))
    mask = np.zeros(cv2.imread(sub[0]).shape[:2], np.uint8)
    mask[TX[1]:TX[3], TX[0]:TX[2]] = m
    mask[EM[1]:EM[3], EM[0]:EM[2]] = 1
    for f in sub:
        cv2.imwrite(os.path.join(dst, os.path.basename(f)), cv2.inpaint(cv2.imread(f), mask * 255, 9, cv2.INPAINT_TELEA))
    print('plano', a, b, 'px', int(mask.sum()))
