import cv2, numpy as np, sys
vin, vout = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(vin); fps = cap.get(5); w, h = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter(vout, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)); i = 0
X0, X1, Y0, Y1 = 360, 620, 950, 1075
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps
    if 4.8 <= t <= 6.4:
        r = f[Y0:Y1, X0:X1]
        lab = cv2.cvtColor(r, cv2.COLOR_BGR2LAB); L = lab[..., 0].astype(np.float32)
        hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
        skin = (hsv[..., 0] < 25) & (hsv[..., 1] > 50) & (L > 90)
        med = cv2.medianBlur(lab[..., 0], 81).astype(np.float32)
        m = ((med - L) > 14) & (L > 45)
        # solo dentro de zonas rodeadas de piel
        sk = cv2.dilate(skin.astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
        er = cv2.erode(skin.astype(np.uint8), np.ones((5, 5), np.uint8))
        m = (m & sk).astype(np.uint8)
        num, lab2, st, _ = cv2.connectedComponentsWithStats(m, 8)
        keep = np.zeros_like(m)
        for k in range(1, num):
            x, y, ww, hh, a = st[k]
            if a >= 12 and ww < 120 and hh < 80: keep[lab2 == k] = 1
        keep = cv2.dilate(keep, np.ones((13, 13), np.uint8))
        full = np.zeros((h, w), np.uint8); full[Y0:Y1, X0:X1] = keep
        f = cv2.inpaint(f, full * 255, 7, cv2.INPAINT_TELEA)
    out.write(f); i += 1
out.release(); print('ok', i)
