"""Borra un texto fijo blanco con contorno negro y una flecha roja de un vídeo (por fotogramas).
uso: python3 quitar_texto.py <carpeta_fotogramas_in> <carpeta_out>"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
files = sorted(glob.glob(src + '/*.png'))
TX = (40, 545, 690, 635)        # caja del texto: x0, y0, x1, y1
AR = (25, 680, 160, 950)        # caja de la flecha
# máscara fija del texto: píxeles blancos en casi todos los fotogramas
acc = None
for f in files[::6]:
    r = cv2.imread(f)[TX[1]:TX[3], TX[0]:TX[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    w = ((hsv[..., 2] > 215) & (hsv[..., 1] < 50)).astype(np.float32)
    acc = w if acc is None else acc + w
textmask = (acc / len(files[::6]) > 0.8).astype(np.uint8)
textmask = cv2.dilate(textmask, np.ones((17, 17), np.uint8))   # cubre el contorno negro
full_text = np.zeros(cv2.imread(files[0]).shape[:2], np.uint8)
full_text[TX[1]:TX[3], TX[0]:TX[2]] = textmask
arrow_frames = 0
for f in files:
    img = cv2.imread(f)
    mask = full_text.copy()
    r = img[AR[1]:AR[3], AR[0]:AR[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    red = (((hsv[..., 0] < 8) | (hsv[..., 0] > 172)) & (hsv[..., 1] > 150) & (hsv[..., 2] > 120)).astype(np.uint8)
    if red.sum() > 800:                                     # la flecha está en este fotograma
        arrow_frames += 1
        ys, xs = np.where(red)
        m = np.zeros_like(red)
        m[max(ys.min() - 14, 0):ys.max() + 18, max(xs.min() - 14, 0):xs.max() + 14] = 1
        mask[AR[1]:AR[3], AR[0]:AR[2]] |= m
    out = cv2.inpaint(img, mask * 255, 9, cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join(dst, os.path.basename(f)), out)
print('fotogramas con flecha:', arrow_frames, 'px texto:', int(textmask.sum()))
