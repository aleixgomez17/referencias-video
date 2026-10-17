import cv2, numpy as np, sys, glob, os
src, dst, dbg = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst, exist_ok=True); os.makedirs(dbg, exist_ok=True)
Y0, Y1 = 700, 1100          # vertical band where the loops hang
K = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27))
stats = []
for f in sorted(glob.glob(src + '/*.png')):
    n = int(os.path.basename(f)[:4])
    img = cv2.imread(f)
    out = img.copy()
    if n <= int(sys.argv[4]):
        roi = img[Y0:Y1]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        dark = (hsv[..., 2] < 75).astype(np.uint8)
        body = cv2.morphologyEx(dark, cv2.MORPH_OPEN, K)          # big black fabric
        thin = cv2.subtract(dark, body)
        thin = cv2.morphologyEx(thin, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        near = cv2.dilate(body, np.ones((9, 9), np.uint8))
        cnt, lab, st, _ = cv2.connectedComponentsWithStats(thin)
        mask = np.zeros_like(thin)
        for i in range(1, cnt):
            comp = (lab == i)
            if st[i, cv2.CC_STAT_AREA] < 25: continue
            if not (comp & (near > 0)).any(): continue            # must touch the top
            if st[i, cv2.CC_STAT_HEIGHT] < 12: continue            # loops are tall-ish
            cx = st[i, cv2.CC_STAT_LEFT] + st[i, cv2.CC_STAT_WIDTH] / 2
            if 230 < cx < 490: continue                            # skip cleavage / centre
            mask[comp] = 1
        mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
        mask[body > 0] = 0                                        # never paint over the top itself
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
        stats.append((n, int(mask.sum())))
        if mask.any():
            out[Y0:Y1] = cv2.inpaint(roi, mask * 255, 6, cv2.INPAINT_TELEA)
        if n % 6 == 0 or n < 8:
            d = roi.copy(); d[mask > 0] = (0, 0, 255)
            cv2.imwrite(f'{dbg}/{n:04d}.png', np.hstack([d, out[Y0:Y1]]))
    cv2.imwrite(f'{dst}/{os.path.basename(f)}', out)
print([s for s in stats if s[0] % 12 == 0])
