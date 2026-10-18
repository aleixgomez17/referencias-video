"""Clip 2: el texto cambia ("The problem"+emoji -> "Vs..."). Máscara por fotograma.
uso: python3 quitar_texto_clip2.py <in_dir> <out_dir>"""
import cv2, numpy as np, sys, glob, os
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
TX = (120, 180, 600, 265); EM = (505, 182, 592, 262); THE = (130, 190, 280, 255)
fases = []
for f in sorted(glob.glob(src + '/*.png')):
    img = cv2.imread(f)
    r = img[TX[1]:TX[3], TX[0]:TX[2]]
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    w = ((hsv[..., 2] > 210) & (hsv[..., 1] < 50)).astype(np.uint8)
    m = np.zeros(img.shape[:2], np.uint8)
    m[TX[1]:TX[3], TX[0]:TX[2]] = cv2.dilate(w, np.ones((11, 11), np.uint8))
    t = img[THE[1]:THE[3], THE[0]:THE[2]]
    th = cv2.cvtColor(t, cv2.COLOR_BGR2HSV)
    problem = int(((th[..., 2] > 210) & (th[..., 1] < 50)).sum()) > 900
    if problem: m[EM[1]:EM[3], EM[0]:EM[2]] = 1
    fases.append('P' if problem else 'V')
    cv2.imwrite(os.path.join(dst, os.path.basename(f)), cv2.inpaint(img, m * 255, 9, cv2.INPAINT_TELEA))
print(''.join(fases))
