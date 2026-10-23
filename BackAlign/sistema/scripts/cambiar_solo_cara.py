import sys, cv2, insightface, numpy as np
from insightface.app import FaceAnalysis
src_img, vin, vout, model = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
sw = insightface.model_zoo.get_model(model, providers=['CPUExecutionProvider'])
src = app.get(cv2.imread(src_img)); src = max(src, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
cap = cv2.VideoCapture(vin); fps = cap.get(5); w = int(cap.get(3)); h = int(cap.get(4))
out = cv2.VideoWriter(vout, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)); n = 0; miss = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    faces = app.get(fr)
    if faces:
        f = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
        fr = sw.get(fr, f, src, paste_back=True)
    else: miss += 1
    out.write(fr); n += 1
out.release(); print('frames', n, 'sin cara', miss)
