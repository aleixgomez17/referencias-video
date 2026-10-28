"""Fix matting failures in a short window of a fixed-camera clip with colour rules.

Usage: python3 fondo_por_diferencia.py orig.mp4 alpha_rvm.mp4 comp_in.mp4 bg.png win_start win_end out.mp4 [x0 x1]
Inside [win_start, win_end]:
  alpha = max(RVM alpha, very dark pixels in the central columns x0..x1  -> black garment)
  alpha = 0 where the pixel is neutral grey/white (original wall, also when seen through gaps)
then small islands are removed and the frame is recomposited over bg.png.
Outside the window the frames of comp_in are copied unchanged.
"""
import sys, subprocess, numpy as np, cv2

orig, alpha_v, comp_in, bgp, w0, w1, out = sys.argv[1:8]
w0, w1 = float(w0), float(w1)
cap = cv2.VideoCapture(orig); fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
cx0, cx1 = (int(sys.argv[8]), int(sys.argv[9])) if len(sys.argv) > 9 else (int(W * 0.18), int(W * 0.82))
ca = cv2.VideoCapture(alpha_v); cc = cv2.VideoCapture(comp_in)

bg = cv2.imread(bgp)
sc = max(W / bg.shape[1], H / bg.shape[0])
bg = cv2.resize(bg, (int(round(bg.shape[1] * sc)), int(round(bg.shape[0] * sc))))
y0 = (bg.shape[0] - H) // 2; x0 = (bg.shape[1] - W) // 2
bg = bg[y0:y0 + H, x0:x0 + W].astype(np.float32)
rng = np.random.default_rng(1)
central = np.zeros((H, W), bool); central[:, cx0:cx1] = True

wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
                       "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
i = 0
while True:
    ok1, o = cap.read(); ok2, al = ca.read(); ok3, c = cc.read()
    if not (ok1 and ok2 and ok3):
        break
    t = i / fps; i += 1
    if not (w0 <= t < w1):
        wr.stdin.write(c.tobytes()); continue
    a = al[..., 0].astype(np.float32) / 255.0
    lab = cv2.cvtColor(o, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0]; chroma = np.hypot(lab[..., 1] - 128, lab[..., 2] - 128)
    dark = central & (L < 60)
    dark = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
    a = np.maximum(a, dark.astype(np.float32))
    wall = (chroma < 8) & (L > 95)
    wall = cv2.morphologyEx(wall.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
    a[wall] = 0
    m = (a > 0.5).astype(np.uint8)
    k, lbl, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for j in range(1, k):
        if st[j, cv2.CC_STAT_AREA] > 2500: keep[lbl == j] = 1
    keep = cv2.dilate(keep, np.ones((5, 5), np.uint8))
    a = cv2.GaussianBlur(a * keep, (0, 0), 1.0)[..., None]
    grain = rng.normal(0, 2.0, bg.shape).astype(np.float32)
    res = o.astype(np.float32) * a + np.clip(bg + grain, 0, 255) * (1 - a)
    wr.stdin.write(np.clip(res, 0, 255).astype(np.uint8).tobytes())
wr.stdin.close(); wr.wait()
print("frames", i)
