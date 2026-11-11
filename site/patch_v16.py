import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'shelf-top' in s: continue
    m=re.search(r'\s*<figure class="shelf-shot">.*?</figure>',s,re.S)
    if not m: continue
    fig=re.sub(r'<figcaption>.*?</figcaption>','',m.group(0).strip()).replace('class="shelf-shot"','class="shelf-shot shelf-top"',1)
    s=s[:m.start()]+s[m.end():]
    a=s.index('<section class="note pad note2">'); h=s.index('</h2>',a)+5
    s=s[:h]+'\n    '+fig+s[h:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v16*/' not in c:
    open(p,'w',encoding='utf-8').write(c+'/*v16*/.shelf-top{margin:36px auto 8px}\n')
print('v16 patched')
