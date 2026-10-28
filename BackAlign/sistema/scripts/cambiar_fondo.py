"""Replace the background of a fixed-camera video, free, with RobustVideoMatting (ONNX, CPU).

Usage: python3 cambiar_fondo.py rvm.onnx in.mp4 out.mp4 "t_start:t_end=bg.png" [...] [--alpha alpha.mp4]
Each segment of the video (by shot) gets its own background image (resized/cropped to fill).
The person keeps her original pixels; only the background changes. Light colour-match of the
background to the original wall brightness and a soft grain so it does not look pasted.
"""
import sys, subprocess, numpy as np, cv2, onnxruntime as ort

model, vin, vout = sys.argv[1], sys.argv[2], sys.argv[3]
segs = []
alpha_out = None
args = sys.argv[4:]
if "--alpha" in args:
    i = args.index("--alpha"); alpha_out = args[i + 1]; args = args[:i] + args[i + 2:]
for s in args:
    rng, bg = s.split("=")
    a, b = rng.split(":")
    segs.append((float(a), float(b), bg))

probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate", "-of", "csv=p=0", vin],
                       capture_output=True, text=True).stdout.strip().split(",")
W, H = int(probe[0]), int(probe[1]); num, den = map(int, probe[2].split("/")); fps = num / den


def fill(img):
    h, w = img.shape[:2]
    sc = max(W / w, H / h)
    img = cv2.resize(img, (int(round(w * sc)), int(round(h * sc))), interpolation=cv2.INTER_LANCZOS4)
    y0 = (img.shape[0] - H) // 2; x0 = (img.shape[1] - W) // 2
    return img[y0:y0 + H, x0:x0 + W]


bgs = [(a, b, fill(cv2.imread(p)).astype(np.float32)) for a, b, p in segs]
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
ratio = np.array([float(__import__("os").environ.get("RVM_RATIO","0.5"))], np.float32)

rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", vin, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                      stdout=subprocess.PIPE)
enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p"]
wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", probe[2], "-i", "-"] + enc + [vout], stdin=subprocess.PIPE)
wa = None
if alpha_out:
    wa = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
                           "-r", probe[2], "-i", "-"] + enc + [alpha_out], stdin=subprocess.PIPE)
n = 0; cur_seg = None
rng = np.random.default_rng(0)
while True:
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    t = n / fps
    seg = next((i for i, (a, b, _) in enumerate(bgs) if a <= t < b), len(bgs) - 1)
    if seg != cur_seg:  # new shot -> reset the recurrent state
        rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4; cur_seg = seg
    src = (fr.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
    fgr, pha, *rec = sess.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                     "downsample_ratio": ratio})
    a = pha[0, 0]
    a = np.clip((a - 0.12) / 0.66, 0, 1)  # no half-transparent ghosts
    a = cv2.GaussianBlur(a, (0, 0), 0.8)[..., None]
    bg = bgs[seg][2][..., ::-1]  # BGR->RGB
    grain = rng.normal(0, 2.0, bg.shape).astype(np.float32)
    out = fr.astype(np.float32) * a + np.clip(bg + grain, 0, 255) * (1 - a)
    wr.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
    if wa:
        wa.stdin.write((a[..., 0] * 255).astype(np.uint8).tobytes())
    n += 1
wr.stdin.close(); wr.wait()
if wa:
    wa.stdin.close(); wa.wait()
print("frames", n)
