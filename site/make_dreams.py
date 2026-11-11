import numpy as np, sys, os, math
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
os.chdir(OUT)
from PIL import Image, ImageFilter
W,H=270,480; FPS=24; T=8; N=FPS*T
rng=np.random.default_rng(3)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); X=xx/W; Y=yy/H
def noise_field(seed,sc=6):
    r=np.random.default_rng(seed).random((sc,sc,3)).astype(np.float32)
    return r
def smooth_noise(r,ox,oy,scale):
    # bilinear sample of a small periodic grid -> soft clouds
    sc=r.shape[0]
    u=(X*scale+ox)%sc; v=(Y*scale+oy)%sc
    i0=np.floor(u).astype(int); j0=np.floor(v).astype(int); fu=u-i0; fv=v-j0
    fu=fu*fu*(3-2*fu); fv=fv*fv*(3-2*fv)
    i1=(i0+1)%sc; j1=(j0+1)%sc
    a=r[j0,i0,0]; b=r[j0,i1,0]; c=r[j1,i0,0]; d=r[j1,i1,0]
    return (a*(1-fu)+b*fu)*(1-fv)+(c*(1-fu)+d*fu)*fv
def mix(a,b,t): return a+(b-a)*t[...,None]
def col(h): return np.array([int(h[i:i+2],16)/255 for i in (1,3,5)],np.float32)
def save(img,path,blur):
    im=Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).resize((540,960),Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
    im.save(path)

def station(f,t):
    # dusk sea seen from a station: horizon, slow swell, drifting lights
    sky=mix(col('#9fb2c8')[None,None,:]*np.ones((H,W,1)),col('#e9e3dc')[None,None,:]*np.ones((H,W,1)),np.clip(Y/0.55,0,1))
    sea=mix(col('#7d93a8')[None,None,:]*np.ones((H,W,1)),col('#3f5266')[None,None,:]*np.ones((H,W,1)),np.clip((Y-.55)/.45,0,1))
    wave=.03*np.sin(X*9+t*2*math.pi/T*2)+.02*np.sin(X*17-t*2*math.pi/T*3)
    img=np.where((Y>.55+wave*.3)[...,None],sea,sky)
    img+= (smooth_noise(noise_field(1),t/T*6,0,4)-.5)[...,None]*.08
    # platform edge
    img=np.where(((Y>.78)&(Y<.80))[...,None],img*0.55,img)
    for i in range(3):
        cx=(i/3+t/T)%1; cy=.42+.03*math.sin(i*2+t*.8)
        d=np.hypot(X-cx,(Y-cy)*H/W)
        img+=np.exp(-(d/.10)**2)[...,None]*col('#fff1dc')*.16
    return img,5

def corridor(f,t):
    z=(t/T)  # slow push
    img=np.ones((H,W,3),np.float32)*col('#efe9e1')
    cx,cy=.5,.45
    for k in range(7):
        s=((k/7+z)%1); s=.05+s**2*1.6
        x0,x1=cx-s*.45,cx+s*.45; y0,y1=cy-s*.75,cy+s*.75
        edge=((np.abs(X-x0)<.006)|(np.abs(X-x1)<.006))&(Y>y0)&(Y<y1)
        a=min(1,s*1.5)*(1-min(1,s/1.6))
        img=np.where(edge[...,None],img*(1-.25*a),img)
    d=np.hypot(X-cx,(Y-cy)*H/W); img+=np.exp(-(d/.12)**2)[...,None]*.25
    img*=(1-.35*np.clip(d*1.6,0,1))[...,None]
    img+=(smooth_noise(noise_field(2),0,t/T*6,3)-.5)[...,None]*.05
    return img,6

def sky(f,t):
    top=col('#6b5c8f'); mid=col('#d9a6b8'); low=col('#f3d9c4')
    a=np.clip(Y/0.6,0,1); b=np.clip((Y-.6)/.4,0,1)
    img=mix(mix(top*np.ones((H,W,1)),mid*np.ones((H,W,1)),a),low*np.ones((H,W,1)),b)
    cl=smooth_noise(noise_field(5),t/T*6,0,3)*.6+smooth_noise(noise_field(7),t/T*6*2,1.3,6)*.4
    img=mix(img,np.ones((H,W,3),np.float32)*col('#fbefe9'),np.clip((cl-.55)*2.2,0,1)*.7)
    for i in range(5):  # floating figures (fish-like soft ellipses)
        px=((i*.23+t/T*(.6+i*.1))%1.2)-.1; py=.25+.1*i+.02*math.sin(t*2+i)
        e=((X-px)/.05)**2+((Y-py)/.012)**2
        img=mix(img,np.ones((H,W,3),np.float32)*col('#3b3350'),np.exp(-e)*.55)
    return img,5

for name,fn in [('station',station),('corridor',corridor),('sky',sky)]:
    os.makedirs(name,exist_ok=True)
    for f in range(N):
        t=f/FPS; img,b=fn(f,t)
        save(img,f'{name}/f{f:04d}.png',b)
    os.system(f'ffmpeg -v error -y -framerate {FPS} -i {name}/f%04d.png -vf "noise=alls=6:allf=t,eq=saturation=0.85" -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart {name}.mp4')
    os.system(f'ffmpeg -v error -y -ss 3 -i {name}.mp4 -frames:v 1 -vf scale=270:-1 {name}_poster.jpg')
print('done')
