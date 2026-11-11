import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'offer-links' in s: continue
    links=re.search(r'<div class="links">(.*?)</div>',s,re.S).group(1)
    free=re.sub(r'<a class="free" href="#price">(.*?)</a>',r'<span class="free">\1</span>',links)
    a=s.index('<section class="offer pad"'); e=s.index('</section>',a)
    sec=s[a:e]
    sec=re.sub(r'\s*<p class="price">.*?</p>','',sec,flags=re.S)
    note=re.search(r'\s*<p>(.*?)</p>',sec,re.S)
    notetxt=note.group(1) if note else ''
    if note: sec=sec[:note.start()]+sec[note.end():]
    sec=re.sub(r'\s*<a class="badge".*?</a>','',sec,flags=re.S)
    sec=sec.rstrip()+'\n    <div class="links offer-links">'+free+'</div>\n    <p class="offer-note">'+notetxt+'</p>\n  '
    s=s[:a]+sec+s[e:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v12*/' not in c:
    c+='/*v12*/.links{flex-direction:column;align-items:center;gap:12px}\n.offer-links{margin-top:8px}\n.offer .offer-links .badge{margin-top:0}\n.offer .free{font-size:12px;color:var(--ink)}\n.offer p.offer-note{font-size:12px;margin-top:14px}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v12 patched')
