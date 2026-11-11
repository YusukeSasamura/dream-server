import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'note2-kicker' in s: continue
    h='<div class="films-head"><p class="kicker">Film</p></div>'
    s=s.replace('\n    '+h,'',1).replace(h,'',1)
    s=s.replace('<section class="note pad note2">\n    <h2>','<section class="note pad note2">\n    <p class="kicker note2-kicker">Film</p>\n    <h2>',1)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v18*/' not in c:
    c+='/*v18*/.note2-kicker{text-align:center;margin:0 0 28px}\n.films{padding-block:56px 0}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v18 patched')
