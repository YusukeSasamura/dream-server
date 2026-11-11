import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
TX={'ja':['「Dream」をタップして、覚えている夢をそのまま話してください。断片でも、順番がばらばらでもかまいません。話し終えて少し黙ると、自動で記録されます。思い出せない朝は、そのときの気分だけでも残しておけます。',
'アプリを開くと、すぐに聞きはじめます。今の気持ちや、ふと気になったことを、ひとことつぶやくだけ。声を出しにくい場所では、文字でも書けます。こうした小さなつぶやきが、夜に見る夢を読み解く手がかりになります。',
'予定・行った場所・撮った写真・睡眠の記録は、許可するだけで自動で集まります。何もしなくても、その日のできごとがタイムラインに並びます。集めた情報はiPhoneの中だけで扱われ、外には送られません。',
'その夜の夢を開くと、Storyでは話した夢が読みやすい物語に整えられ、夢から生まれた映像と、前日のできごととのつながりが見られます。Freudでは、フロイトが夢を読み解き、問いかけながら一緒に考えます。',
'夢一覧で、これまでの夢をふり返れます。月ごとのレポートでは、夢によく出てくることばや、夢の中の気持ちの移り変わりが見えてきます。くり返し現れるものに、あなた自身の関心や願いが映っているかもしれません。'],
'en':['Tap Dream and tell what you remember, just as it comes. Fragments are fine, and so is telling it out of order. Pause for a moment when you finish and it’s saved on its own. On mornings you can’t recall anything, you can keep just the mood.',
'Open the app and it starts listening right away. Murmur how you feel, or something that caught your attention — a single line is enough. Where you can’t speak, type instead. These small notes become clues for reading the dreams that come at night.',
'Once you allow it, your plans, places, photos and sleep gather on their own. Without doing anything, the day lines up in your timeline. Everything stays on your iPhone and is never sent out.',
'Open the night’s dream. Story turns what you said into a readable tale, with a film made from the dream and the links to the day before. In Freud, he reads the dream and thinks it through with you, asking questions as he goes.',
'The dream shelf lets you look back over every dream. Monthly reports show the words that keep appearing and how the feelings in your dreams shift. What returns again and again may reflect what you care about and long for.']}
NAV={'ja':('前へ','次へ'),'en':('Previous','Next')}
JS='<script>document.querySelectorAll(".how-car").forEach(c=>{const t=c.querySelector(".how-track"),n=t.children.length,o=c.querySelector(".how-count");let i=0;const go=k=>{i=(k+n)%n;t.scrollTo({left:t.clientWidth*i,behavior:"smooth"})};c.querySelector(".prev").onclick=()=>go(i-1);c.querySelector(".next").onclick=()=>go(i+1);t.addEventListener("scroll",()=>{i=Math.round(t.scrollLeft/t.clientWidth);o.textContent=(i+1)+" / "+n},{passive:true})})</script>'
for fn,lang in (('index.html','ja'),('en.html','en')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if 'how-car' in s: continue
    k=[0]
    def rep(m):
        t=TX[lang][k[0]]; k[0]+=1
        return m.group(1)+'<p>'+t+'</p></div></div>'
    s=re.sub(r'(<div class="how-tx">.*?</h3>)<p>.*?</p></div></div>',rep,s,flags=re.S)
    a=s.index('<div class="how-row">'); e=s.index('</section>',a)
    rows=s[a:e].rstrip()
    pv,nx=NAV[lang]
    car='<div class="how-car"><div class="how-track">'+rows+'</div>\n    <div class="how-nav"><button class="prev" type="button" aria-label="'+pv+'">←</button><span class="how-count">1 / 5</span><button class="next" type="button" aria-label="'+nx+'">→</button></div></div>\n  '
    s=s[:a]+car+s[e:]
    s=s.replace('</body>',JS+'\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '.how-car' not in c:
    c+='''.how-car{margin-top:56px}
.how-track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.how-track::-webkit-scrollbar{display:none}
.how-track .how-row,.how-track .how-row:nth-of-type(even){flex:0 0 100%;scroll-snap-align:start;margin:0;grid-template-columns:220px minmax(0,1fr);padding:10px 4px 30px}
.how-track .how-row:nth-of-type(even) .how-ph{order:0}
.how-tx p:last-child{max-width:460px}
.how-nav{display:flex;justify-content:center;align-items:center;gap:26px;margin-top:20px}
.how-nav button{width:46px;height:46px;border-radius:50%;border:1px solid var(--ink);background:none;color:var(--ink);font-size:18px;cursor:pointer;font-family:var(--sans)}
.how-nav button:hover{background:var(--ink);color:var(--paper)}
.how-count{font-size:13px;letter-spacing:.14em;color:var(--mute);min-width:50px;text-align:center;font-variant-numeric:tabular-nums}
@media (max-width:640px){.how-track .how-row,.how-track .how-row:nth-of-type(even){grid-template-columns:1fr;text-align:center}}
'''
    open(p,'w',encoding='utf-8').write(c)
print('howslide patched')
