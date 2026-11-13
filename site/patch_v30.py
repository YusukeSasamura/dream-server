import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
JA='<p class="offer-note">おすすめ：Apple Intelligence（Image Playground）に対応したiPhone（iPhone 15 Pro以降）。夢の文ごとに絵が描かれ、フロイトとも話せます。対応していないiPhoneでも夢の記録はでき、映像はあらかじめ用意した場面からつくられます。</p>'
EN='<p class="offer-note">Recommended: an iPhone with Apple Intelligence and Image Playground (iPhone 15 Pro or later). Each sentence of your dream is drawn as its own picture, and you can talk with Freud. On other iPhones you can still record dreams; films are made from prepared scenes.</p>'
for fn,anchor,note in (('index.html','登録や課金はありません。すべての機能を無料で使えます。</p>',JA),('en.html','No subscription, no in-app purchases. Every feature is free.</p>',EN)):
    p=os.path.join(D,fn)
    if not os.path.exists(p): continue
    s=open(p,encoding='utf-8').read()
    if '<!--v30-->' in s: continue
    s=s.replace(anchor,anchor+'\n    '+note,1)
    s=s.replace('</body>','<!--v30-->\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
print('v30 patched')
