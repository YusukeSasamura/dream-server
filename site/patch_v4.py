import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
PH={'ja':'<div class="phone"><div class="island"></div><div class="screen"><div class="pad-s"><div class="who"><div class="av">F</div>フロイト</div><div class="b in">駅は、何かを待つ場所だね。海の音は、遠くにある懐かしさかもしれない。</div><div class="b in">最近、誰かからの知らせを待っていないかね？</div><div class="b out">来週、昔の友だちに会います。</div><div class="b in">それなら、夢はその再会を少し先に旅していたのかもしれないね。</div></div></div></div>',
'en':'<div class="phone"><div class="island"></div><div class="screen"><div class="pad-s"><div class="who"><div class="av">F</div>Freud</div><div class="b in">A station is a place of waiting. The sea may be a longing for something far away.</div><div class="b in">Have you been waiting to hear from someone lately?</div><div class="b out">I am seeing an old friend next week.</div><div class="b in">Then perhaps the dream travelled a little ahead, to that meeting.</div></div></div></div>'}
TX={'ja':('Freud','フロイトと話す','「Freud」を開くと、フロイトがあなたの夢を読み解きます。気になったことを問い返したり、思い当たることを話したりするうちに、対話が少しずつ深まっていきます。声でも文字でも話せます。答えを決めつけず、あなた自身が気づくための問いを返してくれます。'),
'en':('Freud','Talk with Freud','Open Freud and he reads your dream. Ask him back about what puzzles you, or tell him what comes to mind, and the talk slowly goes deeper. You can speak or type. He doesn’t hand you answers; he asks the questions that help you notice for yourself.')}
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'how-freud' in s: continue
    rows=[m.start() for m in re.finditer(r'<div class="how-row">',s)]
    if len(rows)<5: continue
    k,t,x=TX[lang]
    new='<div class="how-row how-freud"><div class="how-ph">'+PH[lang]+'</div><div class="how-tx"><p class="how-n">00 — '+k+'</p><h3>'+t+'</h3><p>'+x+'</p></div></div>\n    '
    s=s[:rows[4]]+new+s[rows[4]:]
    n=[0]
    def num(m):
        n[0]+=1; return '<p class="how-n">%02d — '%n[0]
    s=re.sub(r'<p class="how-n">\d\d — ',num,s)
    s=s.replace('<span class="how-count">1 / 5</span>','<span class="how-count">1 / 6</span>')
    open(p,'w',encoding='utf-8').write(s)
print('v4 patched')
