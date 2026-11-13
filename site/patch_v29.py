import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
def ed(fn,pairs):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return
    s=open(p,encoding='utf-8').read()
    if '<!--v29-->' in s: return
    for a,b in pairs: s=s.replace(a,b)
    s=s.replace('</body>','<!--v29-->\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
ed('privacy.html',[
 ('<li>年代・性別（あなたが選んだ場合のみ）</li>','<li>年代・性別・国籍（あなたが選んだ場合のみ）、iPhoneの言語設定</li>'),
 ('(if chosen) age band and gender,','(if chosen) age band, gender and nationality, your iPhone language,'),
])
ed('terms.html',[('日付、国、年代・性別、','日付、国、言語、年代・性別・国籍、')])
ed('admin.html',[("<button onclick=\"dl('countries')\">国</button>","<button onclick=\"dl('countries')\">国</button><button onclick=\"dl('nationalities')\">国籍</button><button onclick=\"dl('languages')\">言語</button>")])
print('v29 patched')
