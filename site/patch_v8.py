import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    s=s.replace('  <span>© 2026 nanou inc.</span>\n','').replace('<span>© 2026 nanou inc.</span>','')
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v8*/' not in c:
    c+='/*v8*/footer{grid-template-columns:repeat(3,minmax(0,1fr))}\n@media (max-width:760px){footer{grid-template-columns:1fr}}\n'; open(p,'w',encoding='utf-8').write(c)
print('v8 patched')
