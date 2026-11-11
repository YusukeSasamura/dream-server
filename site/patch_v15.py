import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
SHELF='''<figure class="shelf-shot"><div class="phone shelf-phone"><div class="island"></div><div class="screen shelf">
<div class="sh-hero" style="background-image:url(shore_poster.jpg)"><div class="sh-grad"></div><div class="sh-back">‹</div>
<div class="sh-hero-in"><span class="sh-pill">The night’s dream</span><div class="sh-title">Two by the Shore</div><div class="sh-meta">Oct 30, 2026 · Sea · Mother</div><div class="sh-btn">▶&nbsp; Watch the story</div></div></div>
<div class="sh-dots"><i class="on"></i><i></i><i></i><i></i><i></i></div>
<div class="sh-row"><div class="sh-h">Looking back <b>›</b></div><div class="sh-cards">
<div class="sh-tall" style="background-image:url(station_poster.jpg)"><span>Week</span><em>Nov 3 – 9</em></div>
<div class="sh-tall" style="background-image:url(sky_poster.jpg)"><span>Month</span><em>October 2026</em></div></div></div>
<div class="sh-row"><div class="sh-h">Recent dreams <b>›</b></div><div class="sh-cards">
<div class="sh-wide" style="background-image:url(door_poster.jpg)"><em>Beyond the Bright Door</em><small>Oct 27, 2026 ▸</small></div>
<div class="sh-wide" style="background-image:url(rain_poster.jpg)"><em>Waiting in the Rain</em><small>Oct 20, 2026 ▸</small></div></div></div>
<div class="sh-row"><div class="sh-h">Most talked about with Freud <b>›</b></div><div class="sh-cards">
<div class="sh-post" style="background-image:url(woods_poster.jpg)"><b>1</b><em>A Figure in the Woods</em></div>
<div class="sh-post" style="background-image:url(crowd_poster.jpg)"><b>2</b><em>A Crowd Without Faces</em></div>
<div class="sh-post" style="background-image:url(wheel_poster.jpg)"><b>3</b><em>The Night Wheel</em></div></div></div>
</div></div><figcaption>CAP</figcaption></figure>'''
CAP={'ja':'夢一覧','en':'Your dream shelf'}
CSS='''/*v15*/.shelf-shot{margin:56px auto 0;width:260px;text-align:center}
.shelf-shot figcaption{margin-top:14px;font-size:12px;color:var(--mute);letter-spacing:.06em}
.shelf-phone .screen.shelf{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Inter",sans-serif;overflow:hidden}
.sh-hero{position:relative;height:270px;background-size:cover;background-position:center}
.sh-grad{position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.2),rgba(0,0,0,0) 35%,rgba(0,0,0,.95))}
.sh-back{position:absolute;top:30px;left:10px;width:22px;height:22px;border-radius:50%;background:rgba(0,0,0,.35);font-size:15px;line-height:20px;text-align:center}
.sh-hero-in{position:absolute;left:0;right:0;bottom:12px;display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center}
.sh-pill{font-size:7.5px;font-weight:500;border:1px solid rgba(255,255,255,.5);border-radius:99px;padding:2px 7px}
.sh-title{font-size:19px;font-weight:800;letter-spacing:-.01em;line-height:1.05;padding:0 10px}
.sh-meta{font-size:8px;color:rgba(255,255,255,.75)}
.sh-btn{margin-top:3px;background:#fff;color:#000;font-size:9px;font-weight:600;border-radius:99px;padding:6px 14px}
.sh-dots{display:flex;justify-content:center;gap:4px;margin:8px 0 2px}
.sh-dots i{width:4px;height:4px;border-radius:2px;background:rgba(255,255,255,.35)}
.sh-dots i.on{width:12px;background:rgba(255,255,255,.9)}
.sh-row{padding:10px 0 0 10px}
.sh-h{font-size:11px;font-weight:700;margin-bottom:6px}
.sh-h b{color:#8e8e93;font-weight:700}
.sh-cards{display:flex;gap:6px;overflow:hidden}
.sh-tall,.sh-wide,.sh-post{flex:none;position:relative;background-size:cover;background-position:center;border-radius:7px;overflow:hidden}
.sh-tall{width:72px;height:118px}
.sh-tall:after,.sh-wide:after,.sh-post:after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 40%,rgba(0,0,0,.8))}
.sh-tall span{position:absolute;left:5px;bottom:20px;z-index:1;font-size:6.5px;color:rgba(255,255,255,.65)}
.sh-tall em,.sh-wide em,.sh-post em{position:absolute;left:5px;right:5px;bottom:6px;z-index:1;font-style:normal;font-size:7.5px;font-weight:600;line-height:1.2;text-align:left}
.sh-wide{width:150px;height:84px;border-radius:8px}
.sh-wide em{bottom:15px;font-size:9.5px}
.sh-wide small{position:absolute;left:5px;bottom:5px;z-index:1;font-size:6.5px;color:rgba(255,255,255,.75)}
.sh-post{width:64px;height:94px;border:1px solid rgba(255,255,255,.12)}
.sh-post b{position:absolute;left:5px;top:3px;z-index:1;font-size:18px;font-weight:700}
.sh-post em{text-align:center;font-size:6.5px;font-weight:700}
'''
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'shelf-shot' in s: continue
    a=s.index('<section class="note pad note2">'); e=s.index('</section>',a)
    s=s[:e]+'  '+SHELF.replace('CAP',CAP[lang])+'\n  '+s[e:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v15*/' not in c:
    open(p,'w',encoding='utf-8').write(c+CSS)
print('v15 patched')
