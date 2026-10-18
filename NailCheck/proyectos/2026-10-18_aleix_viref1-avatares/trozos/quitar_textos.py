"""Borra "The Problem"+emojis (hasta 4,03 s) y "Comment Safe..."+emoji (después). Máscara por fotograma.
uso: python3 quitar_textos.py <in_dir> <out_dir>"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
TX = (80, 232, 625, 322)
for i, f in enumerate(sorted(glob.glob(src + '/*.png'))):
    img = cv2.imread(f); t = i / 30.0
    r = img[TX[1]:TX[3], TX[0]:TX[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    w = ((hsv[..., 2] > 200) & (hsv[..., 1] < 60)).astype(np.uint8)
    m = np.zeros(img.shape[:2], np.uint8)
    m[TX[1]:TX[3], TX[0]:TX[2]] = cv2.dilate(w, np.ones((21, 21), np.uint8))
    if t < 4.03: m[238:322, 478:612] = 1
    else: m[262:308, 555:608] = 1
    cv2.imwrite(os.path.join(dst, os.path.basename(f)), cv2.inpaint(img, m * 255, 9, cv2.INPAINT_TELEA))
