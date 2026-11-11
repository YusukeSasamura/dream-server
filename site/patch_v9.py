import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    s=s.replace('https://yusukesasamura.github.io/dream-privacy/terms.html','/terms.html').replace('https://yusukesasamura.github.io/dream-privacy/','/privacy.html')
    open(p,'w',encoding='utf-8').write(s)
print('v9 patched')
