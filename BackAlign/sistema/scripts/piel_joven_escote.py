"""Even out sun spots on the neck/chest below a detected face, keeping fine grain.

Usage: python3 piel_joven_escote.py in.mp4 out.mp4 [strength 0-1] [--frames t1,t2 out_prefix]
Works per frame: insightface face box -> region below chin -> skin mask (excludes the
beige garment, hair, jewellery) -> remove medium-frequency blotches (spots) while
re-adding the fine high-frequency texture so the skin does not look plastic.
"""
import sys, subprocess, numpy as np, cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", allowed_modules=["detection"], providers=["CPUExecutionProvider"])
app.prepare(ctx_id=-1, det_size=(640, 640))


def skin_mask(img, region):
    x0, y0, x1, y1 = region
    roi = img[y0:y1, x0:x1]
    lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, a, b = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
    ycc = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycc[..., 1].astype(np.float32), ycc[..., 2].astype(np.float32)
    skin = (cr > 135) & (cr < 180) & (cb > 80) & (cb < 128) & (L > 40)
    # beige garment: lighter and less red than tanned skin
    garment = (L > 175) & (a < 14)
    m = (skin & ~garment).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 6)
    full = np.zeros(img.shape[:2], np.float32)
    full[y0:y1, x0:x1] = m
    return full


def fix(img, strength):
    faces = app.get(img)
    if not faces:
        return img
    f = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    fx0, fy0, fx1, fy1 = f.bbox
    fw, fh = fx1 - fx0, fy1 - fy0
    if fw < 60:
        return img
    h, w = img.shape[:2]
    cx = (fx0 + fx1) / 2
    region = (int(max(0, cx - 2.0 * fw)), int(min(h - 1, fy1 + 0.05 * fh)),
              int(min(w, cx + 2.0 * fw)), int(min(h, fy1 + 3.2 * fh)))
    if region[3] - region[1] < 20:
        return img
    m = skin_mask(img, region)
    # fade in below the chin so the face is untouched
    ramp = np.clip((np.arange(h) - (fy1 + 0.05 * fh)) / (0.35 * fh), 0, 1).astype(np.float32)
    m *= ramp[:, None]
    imf = img.astype(np.float32)
    fine = imf - cv2.GaussianBlur(imf, (0, 0), 1.2)           # pores / grain
    base = cv2.bilateralFilter(img, 0, 22, 9).astype(np.float32)
    base = cv2.GaussianBlur(base, (0, 0), 3.5)                   # kill blotches
    smooth = np.clip(base + 0.9 * fine, 0, 255)
    a = (m * strength)[..., None]
    return np.clip(imf * (1 - a) + smooth * a, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    vin, vout = sys.argv[1], sys.argv[2]
    strength = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
    if "--frames" in sys.argv:
        i = sys.argv.index("--frames")
        times, prefix = sys.argv[i + 1].split(","), sys.argv[i + 2]
        for t in times:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", vin, "-frames:v", "1",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite(f"{prefix}_{t}.png", fix(img, strength))
        sys.exit(0)
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,r_frame_rate", "-of", "csv=p=0", vin],
                           capture_output=True, text=True).stdout.strip().split(",")
    W, H, fps = int(probe[0]), int(probe[1]), probe[2]
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", vin, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                          stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", fps, "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
                           "-pix_fmt", "yuv420p", vout], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        wr.stdin.write(fix(np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy(), strength).tobytes())
        n += 1
    wr.stdin.close(); wr.wait()
    print("frames", n)
