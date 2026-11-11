import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
BAR='<div class="home-bar"><i class="cal"></i><svg class="kb" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M6 10h1M9.5 10h1M13 10h1M16.5 10h1M6 13.5h1M17 13.5h1M9 13.5h6"/></svg></div>'
for fn in ('index.html','en.html'):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'home-bar' in s: continue
    s=re.sub(r'(<div class="home">.*?)<div class="hint">.*?</div>',lambda m:m.group(1)+BAR,s,flags=re.S)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v22*/' not in c:
    c+='''/*v22*/.home .pills{padding:3px;gap:0}.home .pills span{padding:5px 15px;font-size:10px}
.home .orb{margin:auto -12px 0;width:calc(100% + 24px);height:auto;border-radius:0;background:none;box-shadow:none;display:block}
.home .orb svg{display:block;width:100%;height:64px}
.home .said{margin-top:18px;font-size:12.5px;line-height:1.7;color:#1d1d1f}
.home-bar{margin-top:auto;width:100%;position:relative;height:22px;display:flex;justify-content:center;align-items:center}
.home-bar .cal{position:relative;width:11px;height:11px;border:.8px solid rgba(0,0,0,.55);border-radius:2.5px;box-sizing:border-box}
.home-bar .cal:before{content:"";position:absolute;left:-1px;right:-1px;top:3px;height:.8px;background:rgba(0,0,0,.55)}
.home-bar .cal:after{content:"";position:absolute;left:5.5px;top:5.5px;width:2.4px;height:2.4px;border-radius:50%;background:#1d1d1f}
.home-bar .kb{position:absolute;right:6px;top:4px;width:14px;height:14px;fill:none;stroke:rgba(0,0,0,.55);stroke-width:1.2;stroke-linecap:round}
'''
    open(p,'w',encoding='utf-8').write(c)
print('v22 patched')
