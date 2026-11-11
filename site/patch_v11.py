import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
PH={'ja':('あなた','みんな','直近7日間 · 1,240人','みんなの夢の中の気持ち',[('不安',34),('なつかしい',22),('おだやか',18),('うれしい',15)],'今週の夢のことば','「遅れる」'),
'en':('You','Everyone','Last 7 days · 1,240 people','Feelings in everyone’s dreams',[('uneasy',34),('nostalgic',22),('calm',18),('happy',15)],'Word of the week','“Late”')}
TX={'ja':('レポート','あなたのレポートでは、ひと月の夢をふり返り、よく出てくることばや夢の中の気持ち、日々とのつながりが見えてきます。みんなのレポートでは、世界中の人がどんな夢を見ているのかを、国や年代ごとに見られます。参加は任意で、名前を伏せたテーマと気持ちだけが集まります。'),
'en':('Reports','Your report looks back on your month: the words that keep returning, the feelings in your dreams and how they link to your days. Everyone’s report shows what people around the world are dreaming, by country and age. Joining is optional, and only themes and feelings are shared, without names.')}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'how-report' in s: continue
    m=re.search(r'<div class="how-row">(?:(?!<div class="how-row).)*?— Look back</p>.*?</p></div></div>',s,re.S)
    if not m: continue
    a,b,sub,head,bars,wl,w=PH[lang]
    bar=''.join('<div class="bar"><span>%s</span><i style="width:%d%%"></i><em>%d%%</em></div>'%(k,v*2.4,v) for k,v in bars)
    phone='<div class="phone"><div class="island"></div><div class="screen"><div class="pad-s"><div class="seg"><span>'+a+'</span><span class="on">'+b+'</span></div><div style="font-size:9px;color:#86868b">'+sub+'</div><div style="font-size:14px;font-weight:600;margin-bottom:6px">'+head+'</div>'+bar+'<div style="font-size:9px;color:#86868b;margin-top:14px">'+wl+'</div><div style="font-size:24px;font-weight:300">'+w+'</div></div></div></div>'
    num=re.search(r'<p class="how-n">(\d\d) — ',m.group(0)).group(1)
    t,x=TX[lang]
    row='<div class="how-row how-report"><div class="how-ph">'+phone+'</div><div class="how-tx"><p class="how-n">'+num+' — Report</p><h3>'+t+'</h3><p>'+x+'</p></div></div>'
    s=s[:m.start()]+row+s[m.end():]
    open(p,'w',encoding='utf-8').write(s)
print('v11 patched')
