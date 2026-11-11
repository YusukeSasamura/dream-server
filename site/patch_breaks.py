import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
R=[('毎晩、誰にも見えない数時間があります。Dreamはそれを残します。話した夢と過ごした一日が重なるうちに、心にかかっているもの、望んでいるもの、まだ言葉になっていないものが、少しずつ形をあらわします。',
'毎晩、誰にも見えない数時間があります。<br>Dreamはそれを残します。<br>話した夢と過ごした一日が重なるうちに、<br>心にかかっているもの、望んでいるもの、<br>まだ言葉になっていないものが、少しずつ形をあらわします。'),
('見た夢をフロイトが読み解きます。問いかけに答えながら話すうちに、夢が伝えようとしていることへの理解が、少しずつ深まっていきます。',
'見た夢をフロイトが読み解きます。<br>問いかけに答えながら話すうちに、<br>夢が伝えようとしていることへの理解が、少しずつ深まっていきます。'),
('名前を伏せて共有した夢は、Dreamを使うすべての人の記録に加わります。それはやがて、人の夢についての大きな共有の記録になります。夢とは何か。古くからの問いに、もう一度、一緒に向き合うために。</p>',
'名前を伏せて共有した夢は、<br>Dreamを使うすべての人の記録に加わります。<br>それはやがて、人の夢についての大きな共有の記録になります。</p>\n    <p class="body">夢とは何か？<br>古くからの問いに、もう一度、一緒に向き合うために。</p>')]
p=os.path.join(D,'index.html'); s=open(p,encoding='utf-8').read()
for a,b in R:
    if a in s: s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*br*/' not in c:
    c+='/*br*/.essay{max-width:760px}.sub{max-width:640px}\n@media (max-width:640px){.essay br,.sub br{display:none}}\n'
    open(p,'w',encoding='utf-8').write(c)
print('breaks patched', s.count('<br>'))
