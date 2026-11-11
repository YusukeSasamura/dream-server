import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
p=os.path.join(D,'index.html'); s=open(p,encoding='utf-8').read()
s=s.replace('<p class="kicker">For you<small>あなたのために</small></p>','<p class="sub-h">あなたのために</p>')
s=s.replace('<p class="kicker">For everyone<small>みんなのために</small></p>','<p class="sub-h">みんなのために</p>')
s=s.replace('それはやがて、人の夢についての大きな共有の記録になります。</p>\n    <p class="body">人類はなぜ','それはやがて、人の夢についての大きな共有の記録になります。<br>人類はなぜ')
open(p,'w',encoding='utf-8').write(s)
p=os.path.join(D,'style.css'); c=open(p,encoding='utf-8').read()
if '/*ja*/' not in c:
    c+='/*ja*/.essay>.sub-h{margin:0}.essay>.sub-h+p.body{margin-top:26px}.sub .sub-h,.essay>.sub-h{font-size:clamp(18px,1.8vw,21px);font-weight:500;letter-spacing:.08em}\n.how-track .phone{box-shadow:none}.how-track{background:none}\n'
    open(p,'w',encoding='utf-8').write(c)
print('ja patched')
