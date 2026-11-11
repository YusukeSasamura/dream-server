import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn,a,b in (('index.html','>1か月無料</a></div>','>最初の1か月は無料（月額480円）</a></div>'),('en.html','>1 month free</a></div>','>First month free (¥480/month)</a></div>')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read(); s=s.replace(a,b,1); open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v7*/' not in c:
    c+='/*v7*/.links .free{font-size:12px}\n'; open(p,'w',encoding='utf-8').write(c)
print('v7 patched')
