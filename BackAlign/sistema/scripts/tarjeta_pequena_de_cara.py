import cv2,numpy as np,json,os,sys
S_=0.78
tr={int(k):v[1] for k,v in json.load(open('track.json')).items()}
ch={int(k):v for k,v in json.load(open('front_chain.json')).items()}
src=cv2.imread('/mnt/user-data/uploads/cd4658f8-image.png').astype(np.float32)
H0,W0=src.shape[:2]; SRC=np.float32([[0,0],[W0,0],[W0,H0],[0,H0]])
# alfa de tarjeta con esquinas redondeadas
al=np.zeros((H0,W0),np.float32); r=18
cv2.rectangle(al,(r,0),(W0-1-r,H0-1),1,-1); cv2.rectangle(al,(0,r),(W0-1,H0-1-r),1,-1)
for cx,cy in ((r,r),(W0-1-r,r),(r,H0-1-r),(W0-1-r,H0-1-r)): cv2.circle(al,(cx,cy),r,1,-1)
al=cv2.erode(al,np.ones((3,3),np.uint8))
plate=cv2.imread('fr/0008.png').astype(np.float32)
plate[1062:1112,:]=plate[1012:1062,:][::-1]
plate[1020:1112,360:478]=plate[1020:1112,478:596][:,::-1]   # evitar la tapa roja de la caja en el fondo limpio
def Qf(i):
    if i>=99: return np.float32(tr[i])
    return np.float32(ch[i])
def shrink(Q,s=S_):
    a=Q[3]        # ancla: esquina inferior izquierda (donde la agarra la niña)
    return (a+(Q-a)*s).astype(np.float32)
CAN=np.float32([[0,0],[268*S_,0],[268*S_,257*S_],[0,257*S_]])
def rigid(cx,cy,ang,sc=1.0):
    c=(CAN-CAN.mean(0))*(sc/S_); t=np.deg2rad(ang); R=np.float32([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
    return (c@R.T+[cx,cy]).astype(np.float32)
def top_ang(Q): d=Q[1]-Q[0]; return np.degrees(np.arctan2(d[1],d[0]))
P90=shrink(Qf(90)); a90=top_ang(P90); c90=P90.mean(0)
ytop={68:1075,70:1050,74:985,78:890,80:850,82:800,84:760}
def Pquad(i):
    if i>=90: return shrink(Qf(i))
    ks=sorted(ytop)
    def sm(t): t=min(max(t,0),1); return t*t*(3-2*t)
    def rig(j):
        sc=0.66+(S_-0.66)*sm((j-72)/18)
        yt=np.interp(j,ks,[ytop[k] for k in ks]); cy=yt+CAN[2,1]*(sc/S_)/2
        cx=np.interp(j,[68,84],[503,480]); ang=a90*sm((j-70)/20)
        return rigid(cx,cy,ang,sc)
    if i<=84: return rig(i)
    t=(i-84)/6.0; return (rig(84)*(1-t)+P90*t).astype(np.float32)
def redmask(im):
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); h,s,v=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
    m=(((h<6)|(h>172))&(s>110)&(v>60)).astype(np.uint8)*255
    roi=np.zeros_like(m); roi[560:1112,370:660]=255; m&=roi
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); m=cv2.dilate(m,np.ones((5,5),np.uint8))
    return m
def skin(im,x0,x1,y0,y1,early=False):
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); h,s,v=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
    hlo=8 if early else 3
    m=((h>=hlo)&(h<=20)&(s>=(122 if early else 85))&(v<=(178 if early else 192))&(v>=(105 if early else 70))).astype(np.uint8)*255
    roi=np.zeros_like(m); roi[max(y0,0):y1,max(x0,0):x1]=255; m&=roi
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((9,9) if early else (7,7),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m); out=np.zeros_like(m)
    for k in range(1,n):
        if st[k,cv2.CC_STAT_AREA]>(900 if early else 500): out[lab==k]=255
    return cv2.dilate(out,np.ones((5,5),np.uint8))
def poly(shape,Q,d):
    m=np.zeros(shape[:2],np.uint8); cv2.fillPoly(m,[Q.astype(np.int32)],255)
    return cv2.dilate(m,np.ones((2*d+1,2*d+1),np.uint8)) if d else m
def frame(i):
    im0=cv2.imread(f'fr/{i:04d}.png'); im=im0.astype(np.float32)
    if i<68: return im0
    # 1) borrar tarjeta original
    if i<83:
        er=redmask(im0); er=cv2.dilate(er,np.ones((15,15),np.uint8))
    else:
        er=np.zeros(im0.shape[:2],np.uint8)
        if i<98: er[690:1100,395:650]=255
        else: er[690:1102,410:690]=255
        for j in range(max(i-2,86),min(i+2,169)+1):
            if j in ch or j in tr: er|=poly(im0.shape,Qf(j),38)
        er[1104:]=0
        if i>=88:
            Q3=Qf(i)[3]; er[int(Q3[1])-110:,:int(Q3[0])+70]=0
        else: er[:,:450]=0
        v0=cv2.cvtColor(im0,cv2.COLOR_BGR2HSV)[:,:,2]; er[(v0<85)&(np.arange(1080)[None,:]<396)]=0
    m=cv2.GaussianBlur(er.astype(np.float32)/255,(0,0),3)[...,None]
    out=im*(1-m)+plate*m
    if 84<=i<=94:
        hsv=cv2.cvtColor(im0,cv2.COLOR_BGR2HSV); hh,ss,vv=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
        pk=(((hh<14)|(hh>160))&(ss>40)&(vv>150)&(ss<130)).astype(np.uint8)*255
        roi=np.zeros_like(pk); roi[1084:1170,400:640]=255; pk&=roi; pk=cv2.dilate(pk,np.ones((9,9),np.uint8))
        ob=out.astype(np.uint8); ob=cv2.inpaint(ob,pk,7,cv2.INPAINT_TELEA); out=ob.astype(np.float32)
    if 78<=i<=92:
        hsv=cv2.cvtColor(im0,cv2.COLOR_BGR2HSV); hh,ss,vv=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
        tip=((((hh<8)|(hh>170))&(ss>90)&(vv>50))).astype(np.uint8)*255
        roi=np.zeros_like(tip); roi[1080:1162,400:640]=255; tip&=roi; tip=cv2.dilate(tip,np.ones((9,9),np.uint8))
        ob=out.astype(np.uint8); ob=cv2.inpaint(ob,tip,7,cv2.INPAINT_TELEA); out=ob.astype(np.float32)
    # 2) pegar tarjeta real, más pequeña y de cara
    Pq=Pquad(i); H=cv2.getPerspectiveTransform(SRC,Pq.astype(np.float32))
    w=cv2.warpPerspective(src,H,(1080,1920),flags=cv2.INTER_CUBIC)
    a=cv2.warpPerspective(al,H,(1080,1920),flags=cv2.INTER_LINEAR)
    if i<=86: a[1190:]=0
    a=cv2.GaussianBlur(a,(0,0),0.7)
    # color: igualar brillo medio con el de la tarjeta original en este fotograma
    
    out=out*(1-a[...,None])+w*a[...,None]
    # 3) dedos por encima de la tarjeta nueva (solo lo que se ha borrado)
    if i<86: sk=np.zeros(im0.shape[:2],np.uint8)
    else:
        Q=Qf(i); xl=int(min(Q[0,0],Q[3,0])); yb=int(max(Q[2,1],Q[3,1]))
        sk=np.zeros(im0.shape[:2],np.uint8)
        if i>=100: sk|=skin(im0,Q[1,0].astype(int)-30 if False else int(Q[1,0])-30,int(Q[1,0])+150,960,1120)
    if i>=86:
        Q=Qf(i).astype(np.int32); E=np.zeros(im0.shape[:2],np.uint8)
        cv2.polylines(E,[Q[[1,2,3]]],False,255,17)
        if i>=99: E[1004:1016,:]=0
        sk&=~E
    sk&=er
    sk=cv2.GaussianBlur(sk.astype(np.float32)/255,(0,0),1.2)[...,None]
    out=out*(1-sk)+im*sk
    return np.clip(out,0,255).astype(np.uint8)
if __name__=='__main__':
    os.makedirs('fix',exist_ok=True)
    idx=[int(x) for x in sys.argv[1:]] or range(1,170)
    for i in idx: cv2.imwrite(f'fix/{i:04d}.png',frame(i))
