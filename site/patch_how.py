import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
NOW={'ja':('ちょっと疲れたけど、<br>海がきれいだった。','開けば聞いています'),'en':('A little tired,<br>but the sea was lovely.','Open it and it’s listening')}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="how-row' in s: continue
    tr=s[s.index('<div class="track">'):s.index('<div class="links">')]
    ph=re.findall(r'<figure class="shot">(<div class="phone">.*?)<figcaption>',tr,re.S)
    now=ph[0].replace('<span>Now</span><span class="on">Dream</span>','<span class="on">Now</span><span>Dream</span>')
    now=re.sub(r'<div class="said">.*?</div>','<div class="said">'+NOW[lang][0]+'</div>',now,flags=re.S)
    now=re.sub(r'<div class="hint">.*?</div>','<div class="hint">'+NOW[lang][1]+'</div>',now,flags=re.S)
    phones=[ph[0],now,ph[1],ph[2],ph[4]]
    a=s.index('<section class="steps pad" id="how">'); b=s.index('</section>',a)+10
    sec=s[a:b]
    kick=re.search(r'<p class="kicker">.*?</p>',sec,re.S).group(0)
    st=re.findall(r'<div class="when">(.*?)<small>(.*?)</small></div><p>(.*?)</p>',sec,re.S)
    rows=''.join('\n    <div class="how-row"><div class="how-ph">'+phones[i]+'</div><div class="how-tx"><p class="how-n">'+'%02d'%(i+1)+' — '+st[i][1]+'</p><h3>'+st[i][0]+'</h3><p>'+st[i][2]+'</p></div></div>' for i in range(len(st)))
    s=s[:a]+'<section class="steps pad" id="how">\n    '+kick+rows+'\n  </section>'+s[b:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.how-row' not in c:
    c+='''.steps{max-width:900px}
.how-row{display:grid;grid-template-columns:220px minmax(0,1fr);gap:clamp(28px,6vw,90px);align-items:center;margin-top:90px}
.how-row:first-of-type{margin-top:56px}
.how-row:nth-of-type(even){grid-template-columns:minmax(0,1fr) 220px}
.how-row:nth-of-type(even) .how-ph{order:2}
.how-ph .phone{width:220px}
.how-n{margin:0;font-size:12px;letter-spacing:.18em;color:var(--mute);text-transform:uppercase}
.how-tx h3{margin:10px 0 0;font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:.04em}
.how-tx p:last-child{margin:14px 0 0;font-size:16px;line-height:2;max-width:420px}
@media (max-width:640px){.how-row,.how-row:nth-of-type(even){grid-template-columns:1fr;gap:26px;text-align:center;margin-top:70px}.how-row:nth-of-type(even) .how-ph{order:0}.how-ph .phone{margin:0 auto}.how-tx p:last-child{margin-inline:auto}}
'''
    open(p,'w',encoding='utf-8').write(c)
print('how patched')
