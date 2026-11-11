import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
SUB={'ja':'夢を見るために、毎朝私は目覚めるのです。','en':'A dream diary for iPhone'}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'offer-mast' in s: continue
    s=re.sub(r'(<section class="offer pad" id="price">\s*<p class="kicker">Subscription</p>)',
      r'\1\n    <div class="offer-mast"><img class="app-icon" src="icon.svg" alt="Dream"><div class="issue">I Wake Up Every Morning<br>in Order to Dream</div><div class="ja-title">'+SUB[lang]+'</div></div>',s,count=1)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.offer-mast' not in c:
    c+='.offer p.kicker{font-size:20px;color:var(--ink);margin:0;letter-spacing:0}\n.offer-mast{margin:56px 0 40px}\n.offer-mast .issue{font-size:clamp(26px,3.6vw,44px)}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v5 patched')
