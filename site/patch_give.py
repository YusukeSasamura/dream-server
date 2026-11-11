import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
I={'person':'<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-4 4-6 7-6s6 2 7 6"/>',
'place':'<path d="M12 21s-6-5.5-6-10a6 6 0 0 1 12 0c0 4.5-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>',
'plan':'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
'photo':'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="M21 16l-5-5-8 8"/>',
'sleep':'<path d="M19.5 14.5A7.5 7.5 0 1 1 9.5 4.5a6 6 0 0 0 10 10z"/>',
'now':'<path d="M4 12v0M8 9v6M12 6v12M16 9v6M20 12v0"/>'}
L={'ja':[('person','会う人'),('place','行く場所'),('plan','予定'),('photo','写真'),('sleep','睡眠'),('now','つぶやき')],
'en':[('person','People'),('place','Places'),('plan','Plans'),('photo','Photos'),('sleep','Sleep'),('now','Murmurs')]}
def ul(lang):
    return '\n    <ul class="give">'+''.join('<li><svg viewBox="0 0 24 24" aria-hidden="true">'+I[k]+'</svg><span>'+t+'</span></li>' for k,t in L[lang])+'</ul>'
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="give"' in s: continue
    a=s.index('<section class="note pad">'); b=s.index('</h2>',a)+5
    s=s[:b]+ul(lang)+s[b:]; open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.give' not in c:
    c+='''html[lang=ja] .note h2{white-space:nowrap;font-size:clamp(16px,4.3vw,30px)}
.give{list-style:none;padding:0;margin:40px auto 10px;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px 8px;max-width:600px}
.give li{display:flex;flex-direction:column;align-items:center;gap:10px;font-size:13px;color:var(--ink);letter-spacing:.04em}
.give svg{width:30px;height:30px;fill:none;stroke:var(--ink);stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round}
@media (max-width:520px){.give{grid-template-columns:repeat(3,minmax(0,1fr))}}
'''
    open(p,'w',encoding='utf-8').write(c)
print('patched')
