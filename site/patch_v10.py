import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
p=os.path.join(D,'index.html'); s=open(p,encoding='utf-8').read()
s=s.replace('大きな共有の記録になります。<br>人類はなぜ','大きな共有の記録になります。<br><br>人類はなぜ',1)
open(p,'w',encoding='utf-8').write(s)
print('v10 patched')
