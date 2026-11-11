import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v21*/' not in c:
    c+='/*v21*/.note p.note2-kicker{font-family:var(--sans);font-size:20px;font-weight:700;color:var(--ink);letter-spacing:0;line-height:36px;text-transform:uppercase;margin:0 0 28px}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v21 patched')
