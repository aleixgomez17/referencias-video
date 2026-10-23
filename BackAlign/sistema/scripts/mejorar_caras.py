import sys, cv2, numpy as np, onnxruntime as ort
from insightface.app import FaceAnalysis
vin, vout, model = sys.argv[1], sys.argv[2], sys.argv[3]
blend = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
app = FaceAnalysis(name='buffalo_l', allowed_modules=['detection'], providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
so = ort.SessionOptions(); so.intra_op_num_threads = 2
sess = ort.InferenceSession(model, so, providers=['CPUExecutionProvider']); iname = sess.get_inputs()[0].name
T = np.array([[0.37691676,0.46864664],[0.62285697,0.46912813],[0.50123859,0.61331904],[0.39308822,0.72541100],[0.61150205,0.72490465]], np.float32) * 512
mask = np.zeros((512, 512), np.float32); cv2.rectangle(mask, (40, 40), (472, 472), 1, -1); mask = cv2.GaussianBlur(mask, (101, 101), 0)
cap = cv2.VideoCapture(vin); fps = cap.get(5); w = int(cap.get(3)); h = int(cap.get(4))
out = cv2.VideoWriter(vout, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)); n = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    for f in app.get(fr):
        M, _ = cv2.estimateAffinePartial2D(f.kps.astype(np.float32), T, method=cv2.LMEDS)
        crop = cv2.warpAffine(fr, M, (512, 512), borderMode=cv2.BORDER_REPLICATE)
        x = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        x = ((x - 0.5) / 0.5).transpose(2, 0, 1)[None]
        y = sess.run(None, {iname: x})[0][0].transpose(1, 2, 0)
        y = np.clip((y + 1) / 2, 0, 1); y = cv2.cvtColor((y * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        y = cv2.addWeighted(y, blend, crop, 1 - blend, 0)
        IM = cv2.invertAffineTransform(M)
        back = cv2.warpAffine(y, IM, (w, h), borderMode=cv2.BORDER_REPLICATE)
        m = cv2.warpAffine(mask, IM, (w, h))[..., None]
        fr = (back * m + fr * (1 - m)).astype(np.uint8)
    out.write(fr); n += 1
out.release(); print('frames', n)
