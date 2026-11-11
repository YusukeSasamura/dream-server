import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v13*/' not in c:
    c+='/*v13*/@media (max-width:640px){.essay br,.sub br,.note br{display:inline}.essay p.body{font-size:15px;line-height:1.95}.note p{font-size:14px}}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v13 patched')
