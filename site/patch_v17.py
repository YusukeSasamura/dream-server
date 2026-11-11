import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
NAV={'ja':('前へ','次へ'),'en':('Previous','Next')}
JS='<script>/*v17*/document.querySelectorAll(".films").forEach(f=>{const r=f.querySelector(".film-row"),p=f.querySelector(".film-nav .prev"),n=f.querySelector(".film-nav .next");if(!r||!p)return;const st=()=>{const c=r.querySelector(".film");return c?c.getBoundingClientRect().width+parseFloat(getComputedStyle(r).columnGap||0):r.clientWidth};const upd=()=>{p.disabled=r.scrollLeft<4;n.disabled=r.scrollLeft+r.clientWidth>=r.scrollWidth-4};p.onclick=()=>r.scrollBy({left:-st(),behavior:"smooth"});n.onclick=()=>r.scrollBy({left:st(),behavior:"smooth"});r.addEventListener("scroll",upd,{passive:true});addEventListener("resize",upd);upd()})</script>'
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if '/*v17*/' in s: continue
    # 1. pull Freud slide out of How to
    m=re.search(r'\s*<div class="how-row how-freud">.*?(?=\s*<div class="how-row how-report">)',s,re.S)
    row=m.group(0); s=s[:m.start()]+s[m.end():]
    s=s.replace('<span class="how-count">1 / 6</span>','<span class="how-count">1 / 5</span>',1)
    ph=re.search(r'<div class="phone">.*</div></div></div>(?=</div><div class="how-tx">)',row,re.S).group(0)
    fig='\n    <figure class="note-shot">'+ph+'</figure>'
    a=s.index('<section class="note pad">'); h=s.index('</h2>',a)+5
    s=s[:h]+fig+s[h:]
    # 2. move Film after note2
    fa=s.index('<section class="films pad"'); fe=s.index('</section>',fa)+10
    films=s[fa:fe]; s=s[:fa]+s[fe:].lstrip('\n ')
    s=s.replace('\n  ','\n  ',1)
    pv,nx=NAV[lang]
    films=films.replace('    </div>\n  </section>','    </div>\n    <div class="film-nav"><button class="prev" type="button" aria-label="'+pv+'">←</button><button class="next" type="button" aria-label="'+nx+'">→</button></div>\n  </section>')
    b=s.index('<section class="note pad note2">'); be=s.index('</section>',b)+10
    s=s[:be]+'\n\n  '+films+s[be:]
    s=s.replace('</body>',JS+'\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v17*/' not in c:
    c+='''/*v17*/.note-shot{margin:48px auto 0;width:220px}
.note-shot .phone{margin:0 auto}
.films .film-row{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:max(14px,1.8vw);scrollbar-width:none;grid-template-columns:none}
.films .film-row::-webkit-scrollbar{display:none}
.films .film-row .film{flex:0 0 calc((100% - 4*max(14px,1.8vw))/4.5);scroll-snap-align:start}
.film-nav{display:flex;justify-content:center;gap:26px;margin-top:28px}
.film-nav button{width:46px;height:46px;border-radius:50%;border:1px solid var(--ink);background:none;color:var(--ink);font-size:18px;cursor:pointer;font-family:var(--sans)}
.film-nav button:hover:not(:disabled){background:var(--ink);color:var(--paper)}
.film-nav button:disabled{opacity:.25;cursor:default}
@media (max-width:900px){.films .film-row .film{flex:0 0 36%}}
@media (max-width:600px){.films .film-row .film{flex:0 0 62%;scroll-snap-align:center}}
'''
    open(p,'w',encoding='utf-8').write(c)
print('v17 patched')
