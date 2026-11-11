import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
SP=[('毎晩、誰にも見えない','毎晩、誰にも見えない数時間があります。<br>Dreamはそれを残します。<br>話した夢と過ごした一日が重なるうちに、<br>あなたの心に本当にあるもの、<br>望んでいるもの、まだ言葉になっていないものが、<br>少しずつ形をあらわします。'),
('見た夢をフロイトが読み解き、','見た夢をフロイトが読み解き、<br>問いかけに答えながら話すうちに、<br>夢が伝えようとしていることへの理解が、<br>さらに深まっていきます。'),
('世界中の誰がどんな夢','世界中の誰がどんな夢をみているのか？<br>名前を伏せて共有した夢は、<br>Dreamを使うすべての人の記録に加わります。<br>それはやがて、<br>人の夢についての大きな共有の記録になります。<br><br>人類はなぜ夢をみるのか？<br>そもそも夢とはなんなのか？<br>古くからの問いに、もう一度、一緒に向き合うために。'),
('夢は、日々のできごとから','夢は、日々のできごとから編まれています。<br>Nowでつぶやくほど、そして会う人・行く場所・<br>予定・写真・睡眠をDreamに見せるほど、<br>つながりが多く見つかり、<br>フロイトの読み解きも確かになります。'),
('許可した情報は、','許可した情報は、夢を読むためだけに使い、<br>iPhoneの外には送りません。<br>何を共有するかは、いつでもあなたが決めます。'),
('夢には、身近な人や場所','夢には、身近な人や場所がよく現れます。<br>パートナーや家族、友人、<br>そして自宅やよく行く場所をDreamに登録しておくと、<br>夢に出てきた人や場所が、日々の誰と、<br>どこと重なるのかが見えてきます。'),
('登録は、設定の','登録は、設定の「よく会う人」「よく行く場所」から<br>いつでもできます。<br>名前や場所はiPhoneの中だけで扱い、外には送りません。')]
p=os.path.join(D,'index.html'); s=open(p,encoding='utf-8').read()
if 'class="sp"' not in s:
    for mark,sp in SP:
        m=re.search(r'(<p(?: class="body")?>)('+re.escape(mark)+r'.*?)</p>',s,re.S)
        if not m: print('miss',mark); continue
        s=s[:m.start()]+m.group(1)+'<span class="pc">'+m.group(2)+'</span><span class="sp">'+sp+'</span></p>'+s[m.end():]
    open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*v14*/' not in c:
    c+='/*v14*/.sp{display:none}\n@media (max-width:640px){.pc{display:none}.sp{display:inline}.essay p.body,.note p{font-size:min(15px,3.5vw);line-height:2;letter-spacing:-.01em}.sp br{display:inline}}\n'
    open(p,'w',encoding='utf-8').write(c)
print('v14 patched')
