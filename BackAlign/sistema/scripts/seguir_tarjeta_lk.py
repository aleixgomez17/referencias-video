import cv2,numpy as np,json
def g(i): return cv2.cvtColor(cv2.imread(f'fr/{i:04d}.png'),cv2.COLOR_BGR2GRAY)
tr={int(k):v for k,v in json.load(open('track.json')).items()}
def chain(i0,Q0,i1,step,mask_scale=0.88,minpts=12):
    """sigue Q0 (4 esquinas) desde i0 hasta i1 con LK + homografía"""
    Q=np.float32(Q0); out={i0:Q.copy()}; i=i0
    lk=dict(winSize=(31,31),maxLevel=4,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,30,0.01))
    while i!=i1:
        j=i+step; a,b=g(i),g(j)
        c=Q.mean(0); m=np.zeros(a.shape,np.uint8); cv2.fillPoly(m,[(c+(Q-c)*mask_scale).astype(np.int32)],255)
        p=cv2.goodFeaturesToTrack(a,300,0.005,5,mask=m)
        if p is None or len(p)<minpts: print('pocos puntos',i); break
        q,st,_=cv2.calcOpticalFlowPyrLK(a,b,p,None,**lk)
        # comprobación hacia atrás
        p2,st2,_=cv2.calcOpticalFlowPyrLK(b,a,q,None,**lk)
        ok=(st.ravel()==1)&(st2.ravel()==1)&(np.linalg.norm(p-p2,axis=2).ravel()<1.0)
        if ok.sum()<minpts: print('pocos buenos',i,ok.sum()); break
        H,inl=cv2.findHomography(p[ok],q[ok],cv2.RANSAC,3.0)
        if H is None or inl.sum()<minpts: print('sin H',i); break
        Q=cv2.perspectiveTransform(Q.reshape(-1,1,2),H).reshape(-1,2); i=j; out[i]=Q.copy()
    return out
if __name__=='__main__':
    Q99=tr[99][1]
    fr=chain(99,Q99,60,-1)
    ks=sorted(fr); print(ks[0],ks[-1])
    json.dump({k:fr[k].tolist() for k in ks},open('front_chain.json','w'))
    from PIL import Image,ImageDraw
    ims=[]
    for i in range(ks[0],100,2):
        if i not in fr: continue
        im=Image.open(f'fr/{i:04d}.png').convert('RGB'); d=ImageDraw.Draw(im)
        d.polygon([tuple(p) for p in fr[i]],outline=(0,255,0),width=5); d.text((340,600),str(i),fill=(255,255,0))
        ims.append(im.crop((250,550,850,1250)).resize((300,350)))
    c=8;r=(len(ims)+c-1)//c;S=Image.new('RGB',(300*c,350*r))
    for k,im in enumerate(ims):S.paste(im,((k%c)*300,(k//c)*350))
    S.save('/tmp/lk.jpg')
