import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
I={'partner':'<path d="M12 20s-7.5-4.6-7.5-10.2A4.1 4.1 0 0 1 12 7.4a4.1 4.1 0 0 1 7.5 2.4C19.5 15.4 12 20 12 20z"/>',
'family':'<circle cx="7" cy="8" r="2.6"/><circle cx="17" cy="8" r="2.6"/><circle cx="12" cy="12.5" r="2"/><path d="M2.5 19c.6-3 2.3-4.6 4.5-4.6M21.5 19c-.6-3-2.3-4.6-4.5-4.6M8.5 20c.5-2.2 1.8-3.4 3.5-3.4s3 1.2 3.5 3.4"/>',
'friend':'<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2.5 20c.7-3.6 2.8-5.5 5.5-5.5 1.6 0 3 .7 4 2 1-1.3 2.4-2 4-2 2.7 0 4.8 1.9 5.5 5.5"/>',
'work':'<circle cx="12" cy="7.5" r="3.2"/><path d="M5 20.5c.9-4.3 3.6-6.5 7-6.5s6.1 2.2 7 6.5M12 14l-1.2 2.4L12 20l1.2-3.6z"/>',
'home':'<path d="M4 11l8-6.5 8 6.5M6 9.5V20h12V9.5M10 20v-5h4v5"/>',
'place':'<path d="M12 21s-6-5.5-6-10a6 6 0 0 1 12 0c0 4.5-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>'}
SEC={'ja':('人と場所を登録すると、さらに深まる',
 [('partner','パートナー'),('family','家族'),('friend','友人'),('work','職場の人'),('home','自宅'),('place','よく行く場所')],
 '夢には、身近な人や場所がよく現れます。パートナーや家族、友人、<br>そして自宅やよく行く場所をDreamに登録しておくと、<br>夢に出てきた人や場所が、日々の誰と、どこと重なるのかが見えてきます。',
 '登録は、設定の「よく会う人」「よく行く場所」からいつでもできます。<br>名前や場所はiPhoneの中だけで扱い、外には送りません。'),
'en':('Add your people and places, and it goes deeper',
 [('partner','Partner'),('family','Family'),('friend','Friends'),('work','Colleagues'),('home','Home'),('place','Places')],
 'The people and places closest to you often appear in dreams. Add your partner, family and friends,<br>and your home and the places you often go, and Dream can show<br>who and where in your days the figures in your dreams connect to.',
 'Add them anytime under “People you often see” and “Places you often go” in Settings.<br>Names and places stay on your iPhone and are never sent out.')}
FILMS={'ja':[('shore','波打ちぎわのふたり','10月30日の朝'),('door','光る扉の向こう','10月27日の朝'),('crowd','顔のない人ごみ','10月24日の朝'),('rain','雨のなかで待つ人','10月20日の朝'),('woods','森の奥の人影','10月16日の朝'),('wheel','夜の観覧車','10月12日の朝'),('town','水に沈んだ町','10月8日の朝')],
'en':[('shore','Two by the Shore','Morning of Oct 30'),('door','Beyond the Bright Door','Morning of Oct 27'),('crowd','A Crowd Without Faces','Morning of Oct 24'),('rain','Waiting in the Rain','Morning of Oct 20'),('woods','A Figure in the Woods','Morning of Oct 16'),('wheel','The Night Wheel','Morning of Oct 12'),('town','The Drowned Town','Morning of Oct 8')]}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'class="film-row"' in s: continue
    s=re.sub(r'(<p class="kicker[^"]*">[^<]*)<small>.*?</small>',r'\1',s)
    a=s.index('<section class="films pad"'); e=s.index('</section>',a)
    sec=s[a:e]
    h=sec.index('<figure class="film"'); body=sec[h:].rstrip()
    extra=''.join('\n    <figure class="film" style="margin:0"><div class="frame"><video src="'+k+'.mp4" poster="'+k+'_poster.jpg" autoplay muted loop playsinline preload="metadata" aria-label="'+t+'"></video></div><h3>'+t+'</h3><p>'+d+'</p></figure>' for k,t,d in FILMS[lang])
    sec=sec[:h]+'<div class="film-row">'+body+extra+'\n    </div>\n  '
    s=s[:a]+sec+s[e:]
    e=s.index('</section>',a)+10
    hd,items,p1,p2=SEC[lang]
    ul='<ul class="give">'+''.join('<li><svg viewBox="0 0 24 24" aria-hidden="true">'+I[k]+'</svg><span>'+t+'</span></li>' for k,t in items)+'</ul>'
    s=s[:e]+'\n\n  <section class="note pad note2">\n    <h2>'+hd+'</h2>\n    '+ul+'\n    <p>'+p1+'</p>\n    <p>'+p2+'</p>\n  </section>'+s[e:]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.film-row' not in c:
    c+='''.kicker{font-size:20px;letter-spacing:0}
.films{display:block}
.film-row{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:36px max(14px,1.8vw)}
.film-row .film{display:block}
.film-row .film h3{font-size:clamp(15px,1.3vw,18px)}
.film-row .film p{font-size:13px}
@media (max-width:900px){.film-row{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin-inline:calc(-1*max(16px,4vw));padding-inline:max(16px,4vw);scrollbar-width:none}.film-row::-webkit-scrollbar{display:none}.film-row .film{flex:0 0 62%;scroll-snap-align:center}}
@media (min-width:600px) and (max-width:900px){.film-row .film{flex-basis:36%}}
.note2 h2{white-space:normal}
html[lang=ja] .note2 h2{white-space:nowrap}
'''
    open(p,'w',encoding='utf-8').write(c)
print('v3 patched')
