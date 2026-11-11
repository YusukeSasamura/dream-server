import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
R={'index.html':[('<h2>残すほど、夢の読み解きは深くなる</h2>','<h2>あなたの夢をフロイトと深める</h2>'),
 ('<h2>人と場所を登録すると、さらに深まる</h2>','<h2>あなたの夢が現実世界のストーリーに</h2>'),
 ('<span class="pc">夢には、身近な人や場所がよく現れます。','<span class="pc">毎日あなたが見た夢が映像化されます。<br>夢には、身近な人や場所がよく現れます。'),
 ('<span class="sp">夢には、身近な人や場所がよく現れます。','<span class="sp">毎日あなたが見た夢が映像化されます。<br>夢には、身近な人や場所がよく現れます。')],
 'en.html':[('<h2>The more you leave, the deeper the reading</h2>','<h2>Go deeper into your dreams with Freud</h2>'),
 ('<h2>Add your people and places, and it goes deeper</h2>','<h2>Your dreams, as stories of your real world</h2>'),
 ('<p>The people and places closest to you often appear in dreams.','<p>Every dream you have becomes a film.<br>The people and places closest to you often appear in dreams.')]}
for fn,rs in R.items():
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    for a,b in rs:
        if b not in s: s=s.replace(a,b,1)
    open(p,'w',encoding='utf-8').write(s)
print('v20 patched')
