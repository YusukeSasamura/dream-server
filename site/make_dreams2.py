import numpy as np, sys, os, math
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
ONLY=sys.argv[2].split(',') if len(sys.argv)>2 else None
NF=int(os.environ.get('NF','0')) or None
os.chdir(OUT)
from PIL import Image, ImageFilter
W,H=270,480; FPS=24; T=8; N=NF or FPS*T
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); X=xx/W; Y=yy/H; PX=xx; PY=yy
def col(h): return np.array([int(h[i:i+2],16)/255 for i in (1,3,5)],np.float32)
def grad(a,b,t): return col(a)*(1-t[...,None])+col(b)*t[...,None]
def mixc(img,c,m): return img*(1-m[...,None])+col(c)*m[...,None]
def blob(cx,cy,rx,ry,soft=1.0):
    e=((PX-cx)/rx)**2+((PY-cy)/ry)**2
    return np.clip(np.exp(-np.maximum(e-1,0)*3/soft),0,1)*(e<9)
def figure(cx,cy,s=1.0,soft=1.0):
    # cx,cy in px = feet position; s=scale (1 ≈ 150px tall)
    h=150*s
    head=blob(cx,cy-h*.86,h*.075,h*.085,soft)
    body=blob(cx,cy-h*.5,h*.14,h*.3,soft)
    legs=blob(cx,cy-h*.16,h*.09,h*.17,soft)
    return np.clip(head+body+legs,0,1)
def nz(seed,ox,oy,sc):
    r=np.random.default_rng(seed).random((6,6)).astype(np.float32); n=6
    u=(X*sc+ox)%n; v=(Y*sc+oy)%n; i0=np.floor(u).astype(int); j0=np.floor(v).astype(int); fu=u-i0; fv=v-j0
    fu=fu*fu*(3-2*fu); fv=fv*fv*(3-2*fv); i1=(i0+1)%n; j1=(j0+1)%n
    return (r[j0,i0]*(1-fu)+r[j0,i1]*fu)*(1-fv)+(r[j1,i0]*(1-fu)+r[j1,i1]*fu)*fv
def save(img,path,blur):
    Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).resize((540,960),Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur)).save(path)
P=2*math.pi/T

def shore(t):  # two figures at the waterline
    img=grad('#c9d3dc','#efe6dc',np.clip(Y/.5,0,1))
    sea=grad('#8fa3b4','#5d7286',np.clip((Y-.5)/.25,0,1))
    sand=grad('#d8cbb8','#b8a68e',np.clip((Y-.72)/.28,0,1))
    wl=.72+.012*np.sin(X*8+t*P*2)
    img=np.where((Y>.5)[...,None],sea,img); img=np.where((Y>wl)[...,None],sand,img)
    foam=np.exp(-((Y-wl)*90)**2); img=mixc(img,'#f4f1ec',foam*.7)
    sw=3*math.sin(t*P)
    f=figure(112+sw,355,1.0,1.3)+figure(160-sw,358,.93,1.3)
    img=mixc(img,'#3c3f48',np.clip(f,0,1)*.75)
    img+=(nz(3,t/T*6,0,3)-.5)[...,None]*.05
    return img,5

def door(t):  # a figure inside a glowing doorway
    img=np.ones((H,W,3),np.float32)*col('#2b2a30')
    img=grad('#26252b','#3a3840',np.clip(Y,0,1))
    pulse=.85+.15*math.sin(t*P)
    d=((np.abs(PX-135)<48)&(PY>110)&(PY<400)).astype(np.float32)
    glow=np.exp(-(((PX-135)/70)**2+((PY-255)/170)**2))
    img=mixc(img,'#fff4e0',np.clip(d*pulse+glow*.45*pulse,0,1))
    f=figure(135+4*math.sin(t*P*.5),395,1.25-.05*math.sin(t*P),1.6)
    img=mixc(img,'#4a4550',f*.8)
    floor=np.exp(-((PY-420)/40)**2)*np.exp(-((PX-135)/60)**2)
    img=mixc(img,'#e9dcc6',floor*.35*pulse)
    return img,6

def crowd(t):  # blurred commuters drifting on a platform
    img=grad('#dfe2e5','#b9bec4',np.clip(Y,0,1))
    img=mixc(img,'#f2f2ee',np.exp(-((PY-120)/60)**2)*.6)
    rng=np.random.default_rng(7)
    for i in range(14):
        sp=rng.uniform(.3,1.0)*(1 if i%2 else -1); x0=rng.uniform(0,W)
        cx=(x0+sp*t*30)%(W+80)-40; dep=rng.uniform(.6,1.15); cy=300+dep*90
        img=mixc(img,['#5b5f68','#6d6a70','#4c5560'][i%3],figure(cx,cy,dep*.95,1.8)*(.35+.4*dep))
    img=mixc(img,'#9aa0a6',((PY>395)&(PY<400)).astype(np.float32)*.5)
    return img,6

def rain(t):  # a person with an umbrella under falling rain
    img=grad('#7f8b98','#a9b2bb',np.clip(Y,0,1))
    rng=np.random.default_rng(11)
    for i in range(70):
        x=rng.uniform(0,W); y0=rng.uniform(0,H); y=(y0+t*260)%H
        img=mixc(img,'#dde3ea',blob(x,y,.6,9,1.0)*.5)
    um=np.exp(-np.maximum(((PX-140)/52)**2+((PY-238)/26)**2-1,0)*4)*(PY<246)
    img=mixc(img,'#2f3540',np.clip(um,0,1)*.85)
    img=mixc(img,'#2f3540',blob(140,300,1.5,58,1)*.6)
    f=figure(140,392,.95,1.5)*(PY>245)
    img=mixc(img,'#3a3f49',f*.8)
    pud=np.exp(-((PY-405)/8)**2)*np.exp(-((PX-140)/80)**2)
    img=mixc(img,'#c8d0d8',pud*(.4+.1*math.sin(t*P*4)))
    return img,5

def woods(t):  # a figure between trees in mist
    img=grad('#d5ddd2','#9fae9a',np.clip(Y,0,1))
    for i,(x,w,c) in enumerate([(30,16,'#55624f'),(95,10,'#6f7d68'),(210,20,'#4d5947'),(250,9,'#7a8873'),(165,7,'#83907d')]):
        img=mixc(img,c,np.clip(1-np.abs(PX-x)/w,0,1)**.5*.85)
    img=mixc(img,'#e9eee6',np.clip(nz(5,t/T*6,0,2)*1.2-.3,0,1)*.55)
    f=figure(128+6*math.sin(t*P),370,.8,1.8)
    img=mixc(img,'#3f463c',f*(.45+.15*math.sin(t*P)))
    return img,6

def wheel(t):  # a ferris wheel turning at night
    img=grad('#1d2236','#3d3550',np.clip(Y,0,1))
    cx,cy,R=150,250,105
    a=t*P/4
    r=np.hypot(PX-cx,PY-cy)
    img=mixc(img,'#c9c0d6',np.exp(-((r-R)/2.2)**2)*.6)
    for k in range(12):
        th=a+k*math.pi/6; x=cx+R*math.cos(th); y=cy+R*math.sin(th)
        img=mixc(img,['#ffd9a8','#ffc2c9','#cfe3ff'][k%3],blob(x,y,5,5,1.5)*.95)
        sp=np.abs((PX-cx)*math.sin(th)-(PY-cy)*math.cos(th))<1.0
        img=mixc(img,'#8d86a0',(sp&(r<R)).astype(np.float32)*.35)
    img=mixc(img,'#16192a',(PY>400).astype(np.float32)*.9)
    img=mixc(img,'#ffe1b5',np.exp(-((PY-402)/3)**2)*.3)
    return img,4

def town(t):  # a quiet town under water, light from above
    img=grad('#6fa3b3','#1f4b5c',np.clip(Y,0,1))
    rng=np.random.default_rng(4)
    for i in range(7):
        x=i*40+rng.uniform(-6,6); w=rng.uniform(14,22); h=rng.uniform(70,150)
        b=((np.abs(PX-x)<w)&(PY>440-h)).astype(np.float32)
        roof=((PY>440-h-w*.8)&(PY<440-h)&(np.abs(PX-x)<(PY-(440-h-w*.8))/.8)).astype(np.float32)
        img=mixc(img,'#2c5868',np.clip(b+roof,0,1)*.75)
    rays=np.clip(np.sin(X*18+np.sin(Y*3+t*P)*1.5+t*P*.5),0,1)**6*np.clip(1-Y,0,1)
    img=mixc(img,'#cfeaf0',rays*.35)
    for i in range(18):
        x=rng.uniform(0,W); y=(rng.uniform(0,H)-t*40)%H
        img=mixc(img,'#e6f6fa',blob(x,y,2,2,1)*.5)
    return img,5

SC=[('shore',shore),('door',door),('crowd',crowd),('rain',rain),('woods',woods),('wheel',wheel),('town',town)]
for name,fn in SC:
    if ONLY and name not in ONLY: continue
    os.makedirs(name,exist_ok=True)
    for f in range(N):
        t=f/FPS*(FPS*T/N); img,b=fn(t); save(img,f'{name}/f{f:04d}.png',b)
    os.system(f'ffmpeg -v error -y -framerate {FPS if not NF else max(1,NF//T)} -i {name}/f%04d.png -vf "noise=alls=6:allf=t,eq=saturation=0.85" -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart {name}.mp4')
    os.system(f'ffmpeg -v error -y -ss 3 -i {name}.mp4 -frames:v 1 -vf scale=270:-1 {name}_poster.jpg')
    os.system(f'rm -rf {name}')
print('done')
