import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
def ed(fn,pairs):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return
    s=open(p,encoding='utf-8').read()
    if '<!--v31-->' in s: return
    for a,b in pairs: s=s.replace(a,b,1)
    s=s.replace('</body>','<!--v31-->\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
ed('terms.html',[
 ('2026年11月13日</p>','2026年11月17日</p>'),
 ('<li>13歳以上の方を対象にしています。',
  '<li>フロイトとの会話や夢の絵は、iPhoneの中のAIだけでつくります。Apple Intelligenceに対応していないiPhoneでは、アプリに入っているAI（会話：Sarashina2.2（MITライセンス）、絵：Stable Diffusion 2.1（CreativeML Open RAIL++-Mライセンス）のApple公開のCore ML版）を使います。夢の内容が外部のAIに送られることはありません。</li>\n    <li>13歳以上の方を対象にしています。'),
 ('<li>アプリの仕組みを不正に使ったり、壊したりしないでください。</li>',
  '<li>アプリの仕組みを不正に使ったり、壊したりしないでください。</li>\n    <li>アプリに入っている絵のAIは、そのライセンス（CreativeML Open RAIL++-M）が定める使い方の制限に従って使ってください。法律に反すること、人を傷つけたり差別したりすること、他人になりすますこと、未成年者を害すること、同意のない個人の情報や画像を扱うこと、誤った情報で人をだますことなどに使うことはできません。AIが描いた絵の利用はあなたの責任となり、同じ制限はその絵を他の人に渡す場合にも及びます。</li>'),
 ('Readings and films are made on your iPhone (Apple Intelligence).',
  'Readings, conversations and pictures are made only by AI on your iPhone: Apple Intelligence where available, otherwise AI models built into the app (Sarashina2.2, MIT license; Stable Diffusion 2.1 Core ML by Apple, CreativeML Open RAIL++-M license). Your use of the picture model and its outputs must follow that license\'s use-based restrictions (e.g. no unlawful, harmful, discriminatory, impersonating or deceptive uses, no harm to minors, no processing of personal data or images without consent).'),
])
ed('index.html',[('対応していないiPhoneでも夢の記録はでき、映像はあらかじめ用意した場面からつくられます。',
  '対応していないiPhoneでも、アプリに入っているAIがiPhoneの中だけで絵を描き、フロイトと話せます（絵はメモリ6GB以上のiPhone）。')])
ed('en.html',[('On other iPhones you can still record dreams; films are made from prepared scenes.',
  'On other iPhones, AI built into the app draws the pictures and talks as Freud, entirely on your iPhone (pictures need 6 GB of memory or more).')])
print('v31 patched')
