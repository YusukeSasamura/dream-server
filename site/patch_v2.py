import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
FR={'ja':'<p class="body">見た夢をフロイトが読み解き、<br>問いかけに答えながら話すうちに、<br>夢が伝えようとしていることへの理解が、さらに深まっていきます。</p>',
'en':'<p class="body">Freud reads your dream and talks it through with you.<br>Answering his questions, you come closer to what the dream is trying to say.</p>'}
BD={'ja':('ダウンロード','1か月無料'),'en':('Download on the','1 month free')}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="badge"' in s: continue
    url=re.search(r'href="(https://apps\.apple\.com[^"]*)"',s).group(1)
    badge='<a class="badge" href="'+url+'" target="_blank" rel="noopener"><small>'+BD[lang][0]+'</small>App Store</a>'
    s=s.replace('夢を見るために、毎朝私は目覚めるのです</p>','夢を見るために、毎朝私は目覚めるのです。</p>')
    s=re.sub(r'<div class="links">.*?</div>','<div class="links">'+badge+'<a class="free" href="#price">'+BD[lang][1]+'</a></div>',s,count=1,flags=re.S)
    s=re.sub(r'<a class="store"[^>]*>.*?</a>',badge,s,count=1,flags=re.S)
    if lang=='en':
        s=s.replace('<p class="kicker">For you</p>','<p class="sub-h">For you</p>').replace('<p class="kicker">For everyone</p>','<p class="sub-h">For everyone</p>')
    s=re.sub(r'<div class="sub">.*?</div>',FR[lang],s,count=1,flags=re.S)
    a=s.index('id="about">')+len('id="about">')
    s=s[:a]+'\n    <p class="kicker sec-k">About Dream App</p>'+s[a:]
    n0=s.index('<section class="note pad">'); n1=s.index('</section>',n0)+10
    note=s[n0:n1]; s=s[:n0]+s[n1:]
    f0=s.index('<section class="films pad"')
    s=s[:f0]+note+'\n\n  '+s[f0:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.badge' not in c:
    c+='''.badge{display:inline-flex;flex-direction:column;align-items:flex-start;background:#000;color:#fff;border-radius:11px;padding:7px 20px 9px;line-height:1.05;font-size:20px;font-weight:600;letter-spacing:-.01em;text-align:left}
.badge small{font-size:10px;font-weight:400;letter-spacing:.03em;margin-bottom:2px}
.badge:hover{opacity:.82}
.links{align-items:center;gap:24px}
.links .free{font-size:14px;border-bottom:1px solid currentColor;padding-bottom:1px}
.offer .badge{margin-top:30px}
.sec-k{margin-bottom:56px}
.essay p.body+p.body{margin-top:1.6em}
.note{padding-block:130px 0}
.phone{position:relative}
.mark{font-weight:700;letter-spacing:-.005em;margin-right:0;text-transform:uppercase}
header .mark{font-size:22px}
.kicker{font-weight:700;letter-spacing:.01em;font-size:15px}
.kicker small{font-weight:400;letter-spacing:.2em}
'''
    open(p,'w',encoding='utf-8').write(c)
print('v2 patched')
