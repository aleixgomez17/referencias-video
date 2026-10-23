import sys, cv2, numpy as np
hd, sub, out_path, dbg = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
Y0, Y1 = 1300, 1700
a = cv2.VideoCapture(hd); b = cv2.VideoCapture(sub)
w, h, fps = int(a.get(3)), int(a.get(4)), a.get(5)
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)); n = 0; last = None
while True:
    ok, fa = a.read()
    if not ok: break
    ok2, fb = b.read()
    if not ok2: fb = last
    last = fb
    band = fb[Y0:Y1]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    white = (hsv[..., 2] > 215) & (hsv[..., 1] < 45)
    yellow = (hsv[..., 0] > 18) & (hsv[..., 0] < 38) & (hsv[..., 1] > 120) & (hsv[..., 2] > 170)
    dark = (hsv[..., 2] < 50).astype(np.uint8)
    neardark = cv2.dilate(dark, np.ones((17, 17), np.uint8)) > 0
    cand = ((white | yellow) & neardark).astype(np.uint8)
    num, lab, st, _ = cv2.connectedComponentsWithStats(cand, 8)
    keep = np.zeros_like(cand)
    for i in range(1, num):
        x, y, ww, hh, area = st[i]
        if 8 <= hh <= 110 and area >= 15 and ww <= 200: keep[lab == i] = 1
    # agrupar letras en lineas: quedarse con componentes que tienen vecinas en la misma altura
    m = cv2.dilate(keep, np.ones((9, 9), np.uint8))
    m = cv2.GaussianBlur(m.astype(np.float32), (3, 3), 0)[..., None]
    reg = fa[Y0:Y1].astype(np.float32)
    fa[Y0:Y1] = (band * m + reg * (1 - m)).astype(np.uint8)
    out.write(fa)
    if n in (24, 300, 500): cv2.imwrite(dbg + '_%d.png' % n, fa[Y0 - 200:Y1 + 100])
    n += 1
out.release(); print('frames', n)
