import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    s=s.replace('href="index.html"','href="/"').replace('href="./index.html"','href="/"')
    s=s.replace('<head>','<head>\n<script>if(location.pathname.endsWith("/index.html"))history.replaceState(null,"",location.pathname.slice(0,-10)+location.search+location.hash)</script>',1) if 'endsWith("/index.html")' not in s else s
    open(p,'w',encoding='utf-8').write(s)
print('v6 patched')
