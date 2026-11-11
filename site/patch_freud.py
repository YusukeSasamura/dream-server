import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
T={'ja':('フロイトと話す','見た夢をフロイトが読み解きます。問いかけに答えながら話すうちに、夢が伝えようとしていることへの理解が、少しずつ深まっていきます。'),
'en':('Talk with Freud','Freud reads your dream, then talks it through with you. Answering his questions, you come a little closer to what the dream is trying to say.')}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="sub"' in s: continue
    a=s.index('id="about"'); b=s.index('</p>',s.index('class="body"',a))+4
    h,t=T[lang]
    s=s[:b]+'\n    <div class="sub"><p class="sub-h">'+h+'</p><p>'+t+'</p></div>'+s[b:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.sub-h' not in c:
    c+='''.sub{margin:56px auto 0;max-width:520px}
.sub-h{font-size:clamp(17px,1.7vw,20px);font-weight:500;letter-spacing:.08em;margin:0}
.sub p:not(.sub-h){font-size:16px;line-height:2;margin:14px 0 0;color:#333;text-wrap:pretty}
'''
    open(p,'w',encoding='utf-8').write(c)
print('freud patched')
