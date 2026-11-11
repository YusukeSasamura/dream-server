import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    s=re.sub(r'<title>.*?</title>','<title>Dream — I Wake Up Every Morning in Order to Dream</title>',s,count=1)
    open(p,'w',encoding='utf-8').write(s)
print('title patched')
