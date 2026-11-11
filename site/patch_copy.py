import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
p=os.path.join(D,'index.html'); s=open(p,encoding='utf-8').read()
def sub(pat,rep):
    global s
    s,n=re.subn(pat,lambda m:rep,s,count=1,flags=re.S)
    if not n: print('miss',pat[:40])
sub(r'<p class="body">毎晩.*?</p>','<p class="body">毎晩、誰にも見えない数時間があります。<br>Dreamはそれを残します。<br>話した夢と過ごした一日が重なるうちに、<br>あなたの心に本当にあるもの、望んでいるもの、<br>まだ言葉になっていないものが、少しずつ形をあらわします。</p>')
sub(r'(<p class="sub-h">フロイトと話す</p>)<p>.*?</p>','<p class="sub-h">フロイトと話す</p><p>見た夢をフロイトが読み解きます。<br>問いかけに答えながら話すうちに、<br>夢が伝えようとしていることへの理解が、さらに深まっていきます。</p>')
sub(r'(<small>みんなのために</small></p>).*?(\s*</section>)','<small>みんなのために</small></p>\n    <p class="body">世界中の誰がどんな夢をみているのか？<br>名前を伏せて共有した夢は、<br>Dreamを使うすべての人の記録に加わります。<br>それはやがて、人の夢についての大きな共有の記録になります。</p>\n    <p class="body">人類はなぜ夢をみるのか？<br>そもそも夢とはなんなのか？<br>古くからの問いに、もう一度、一緒に向き合うために。</p>\n  </section>')
sub(r'(<section class="note pad">.*?</ul>).*?</section>',None) if False else None
a=s.index('<section class="note pad">'); u=s.index('</ul>',a)+5; e=s.index('</section>',a)
s=s[:u]+'\n    <p>夢は、日々のできごとから編まれています。Nowでつぶやくほど、<br>そして会う人・行く場所・予定・写真・睡眠をDreamに見せるほど、<br>つながりが多く見つかり、フロイトの読み解きも確かになります。</p>\n    <p>許可した情報は、夢を読むためだけに使い、iPhoneの外には送りません。<br>何を共有するかは、いつでもあなたが決めます。</p>\n  '+s[e:]
open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*copy*/' not in c:
    c+='/*copy*/.note{max-width:760px}.essay p.body+p.body{margin-top:2em}\n@media (max-width:640px){.note br{display:none}}\n'
    open(p,'w',encoding='utf-8').write(c)
print('copy patched')
