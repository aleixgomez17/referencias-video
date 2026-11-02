"""Pegar un papel/tarjeta REAL encima del que sale en un vídeo de IA (texto deformado).
Uso: 1) extraer fotogramas: ffmpeg -i video.mp4 -vf scale=1080:1920:flags=lanczos fr/%04d.png
2) poner en Q las 4 esquinas del papel en el ÚLTIMO fotograma (orden: sup-izq, sup-der, inf-der, inf-izq) y en REF ese número
3) python3 pegar_tarjeta_real.py tarjeta.png  -> out/%04d.png  -> ffmpeg -framerate 24 -i out/%04d.png ...
Sigue la tarjeta hacia atrás con ECC (homografía) y solo pega la franja de texto (BAND) con fundido, igualando el color.
Origen: Snowbox ninos-abren-casilla (Aleix con Claude, 2026-11-02)."""
# ---- seguimiento ----
import cv2,numpy as np,json
Q=np.float32([[238,937],[521,943],[510,1194],[236,1190]])
def gray(i): return cv2.cvtColor(cv2.imread(f'fr/{i:04d}.png'),cv2.COLOR_BGR2GRAY).astype(np.float32)
ref=gray(169)
x0,y0,x1,y1=200,880,580,1260
T=ref[y0:y1,x0:x1]
mask=np.zeros(T.shape,np.uint8); cv2.fillPoly(mask,[(Q-[x0,y0]).astype(np.int32)],255)
mask[:, :60]=0  # exclude fingers on left
W=np.eye(3,dtype=np.float32); out={}
crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,100,1e-5)
for i in range(169,60,-1):
    I=gray(i)[y0:y1,x0:x1]
    try:
        cc,W=cv2.findTransformECC(T,I,W,cv2.MOTION_HOMOGRAPHY,crit,mask,5)
    except cv2.error: print('fail',i); break
    p=cv2.perspectiveTransform((Q-[x0,y0]).reshape(-1,1,2),W).reshape(-1,2)+[x0,y0]
    out[i]=[float(cc),p.tolist()]
    if cc<0.6: print('low',i,cc); break
json.dump(out,open('track.json','w'))
for i in sorted(out)[::8]: print(i,round(out[i][0],3),np.round(out[i][1][0]),np.round(out[i][1][2]))

# ---- composición ----
import cv2,numpy as np,json,os
tr={int(k):v for k,v in json.load(open('track.json')).items()}
src=cv2.imread('/mnt/user-data/uploads/cd4658f8-image.png').astype(np.float32)
H0,W0=src.shape[:2]
S=np.float32([[0,0],[W0,0],[W0,H0],[0,H0]])
# band mask in source coords (text lines), feathered
m=np.zeros((H0,W0),np.float32); m[112:176,30:342]=1; m=cv2.GaussianBlur(m,(0,0),4)
os.makedirs('out',exist_ok=True)
for f in sorted(os.listdir('fr')):
    i=int(f[:4]); im=cv2.imread('fr/'+f).astype(np.float32)
    if i>=120 and i in tr:
        a=min(1,(i-119)/6)
        Q=np.float32(tr[i][1]); H=cv2.getPerspectiveTransform(S,Q)
        w=cv2.warpPerspective(src,H,(1080,1920),flags=cv2.INTER_CUBIC)
        mm=cv2.warpPerspective(m,H,(1080,1920))
        # color match: video card background near text vs white
        ys,xs=np.where(mm>0.9)
        vb=np.median(im[ys,xs],axis=0); sb=np.median(w[ys,xs],axis=0)
        bright=(im[ys,xs].sum(1)>np.percentile(im[ys,xs].sum(1),60))
        vb=np.median(im[ys[bright],xs[bright]],axis=0)
        w=w*(vb/sb)
        w=cv2.GaussianBlur(w,(0,0),0.8)
        al=(mm*a)[...,None]
        im=im*(1-al)+w*al
    cv2.imwrite('out/'+f,np.clip(im,0,255).astype(np.uint8))
