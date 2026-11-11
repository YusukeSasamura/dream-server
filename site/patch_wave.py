import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
JS='<script>(()=>{const c=document.querySelector(".wave canvas");if(!c)return;const x=c.getContext("2d");let w,h,dpr;const rs=()=>{dpr=devicePixelRatio||1;w=c.clientWidth;h=c.clientHeight;c.width=w*dpr;c.height=h*dpr;x.setTransform(dpr,0,0,dpr,0,0)};rs();addEventListener("resize",rs);const still=matchMedia("(prefers-reduced-motion:reduce)").matches;const L=[[1,1.6,0],[.55,1.1,1.7],[.3,.9,3.1]];const f=t=>{x.clearRect(0,0,w,h);const env=.75+.25*Math.sin(t*.0011)*Math.sin(t*.0023+1);L.forEach(([a,lw,ph],k)=>{x.beginPath();for(let i=0;i<=w;i+=2){const u=i/w,fade=Math.sin(Math.PI*u)**1.4,y=h/2+fade*env*h*.46*a*(Math.sin(u*14+t*.0024+ph)*.6+Math.sin(u*31-t*.0037+ph*2)*.3+Math.sin(u*5+t*.0012)*.25);i?x.lineTo(i,y):x.moveTo(i,y)}x.strokeStyle="rgba(17,17,17,"+(k?.32/k:1)+")";x.lineWidth=lw;x.stroke()});if(!still)requestAnimationFrame(f)};requestAnimationFrame(f)})()</script>'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="wave"' in s: continue
    a=s.index('<div class="slider"'); b=s.index('<div class="links">',a)
    s=s[:a]+'<div class="wave" aria-hidden="true"><canvas></canvas></div>\n    '+s[b:]
    s=s.replace('</body>',JS+'\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.wave{' not in c:
    c+='.wave{width:100vw;margin:56px 0 0 calc(50% - 50vw);height:clamp(140px,20vw,260px)}\n.wave canvas{display:block;width:100%;height:100%}\nhtml,body{overflow-x:clip}\n'
    open(p,'w',encoding='utf-8').write(c)
print('wave patched')
