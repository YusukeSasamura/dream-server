import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
R={'index.html':[('<h3>起きたら</h3>','<h3>夢の内容を伝える</h3>'),('<h3>日中は</h3>','<h3>今の気持ちを伝える</h3>'),('<h3>自動で残る</h3>','<h3>予定は自動で伝わる</h3>'),('<h3>翌朝</h3>','<h3>夢を深く理解する</h3>'),('<h3>レポート</h3>','<h3>夢のレポートを見る</h3>'),('06 — Report','05 — Report')],
'en.html':[('<h3>When you wake</h3>','<h3>Tell your dream</h3>'),('<h3>During the day</h3>','<h3>Tell how you feel now</h3>'),('<h3>Kept for you</h3>','<h3>Your plans come in on their own</h3>'),('<h3>The next morning</h3>','<h3>Understand your dream deeply</h3>'),('<h3>Reports</h3>','<h3>See your dream reports</h3>'),('06 — Report','05 — Report')]}
for fn,rs in R.items():
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    for a,b in rs: s=s.replace(a,b,1)
    open(p,'w',encoding='utf-8').write(s)
print('v24 patched')
