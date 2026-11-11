import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.'
T=[('<li><b>広告に使いません。売りません。</b>あなたの記録やヘルスケアのデータを、広告に使ったり第三者に売ったりすることはありません。</li>',
'<li><b>広告に使いません。</b>あなたの記録やヘルスケアのデータを、広告に使うことはありません。</li>\n    <li><b>個人がわからない形で、第三者に提供することがあります。</b>「みんなの夢」で集まった情報（夢のテーマを表す言葉、夢の中の気持ち、日付、国、年代・性別など）を、個人を特定できない統計情報に加工したうえで、研究・調査・サービス改善などのために第三者に提供することがあります。夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータを提供することはありません。くわしくは<a href="/privacy.html">プライバシーポリシー</a>に書いています。</li>'),
('その後は月額480円（予定）です。','その後は月額480円です。'),
('    <li>いまはテスト版です。テスト中は無料で使え、内容は改善のため変わることがあります。</li>\n',''),
('We never use your data for ads or sell it, and you can delete','We never use your data for ads. Data from “Everyone’s dreams” may be shared with third parties only as de-identified statistics (never your dream text, voice, photos, name, email, places or health data). You can delete'),
('then ¥480/month (planned).','then ¥480/month.')]
P=[('<p>広告やマーケティングには使いません。ヘルスケアのデータを広告目的で使ったり、第三者に販売したりすることはありません。</p>',
'<p>広告やマーケティングには使いません。ヘルスケアのデータを広告目的で使ったり、第三者に提供・販売したりすることはありません。</p>'),
('参加をやめると、このiPhoneから送った情報はすべて削除されます。</p>',
'参加をやめると、このiPhoneから送った情報はすべて削除されます。</p>\n  <h2>統計情報の第三者提供</h2>\n  <p>「みんなの夢」で集まった情報は、個人を特定できない統計情報（たとえば「ある月に、ある国の20代で多かった夢のテーマと気持ち」のような集計）に加工したうえで、研究・調査・サービス改善などのために第三者に提供することがあります。提供するのは集計した結果だけで、ひとりひとりの記録や、このiPhoneのランダムなIDは提供しません。夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータは提供しません。</p>'),
('Data is never used for advertising or sold.','Data is never used for advertising. Data from “Everyone’s dreams” may be shared with third parties only as de-identified, aggregated statistics; individual records, IDs, dream text, voice, photos, names, email, places and health data are never shared.')]
for fn,R,mark in (('terms.html',T,'個人がわからない形で'),('privacy.html',P,'統計情報の第三者提供')):
    p=os.path.join(D,fn); s=open(p,encoding='utf-8').read()
    if mark in s: continue
    for a,b in R:
        if a not in s: print('miss',fn,a[:30])
        s=s.replace(a,b,1)
    open(p,'w',encoding='utf-8').write(s)
print('v23 patched')
