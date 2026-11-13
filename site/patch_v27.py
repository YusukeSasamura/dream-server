import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
def ed(fn,pairs):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return
    s=open(p,encoding='utf-8').read()
    if '<!--v27-->' in s: return
    for a,b in pairs: s=s.replace(a,b)
    s=s.replace('</body>','<!--v27-->\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
ed('privacy.html',[
 ('改定日 2026年11月11日','改定日 2026年11月13日'),
 ('<li>このiPhoneで作るランダムなID（アカウントやお名前とは結びつけません）</li>',
  '<li>夢と日々のつながり（バージョン1.2以降、同意した場合）：夢とつながった記録の種類（予定・行った場所・写真・気持ちなど）と何日前の出来事か。夢の前日の記録の量（0・1〜2・3以上）、移動距離の幅（例：1〜5km）と初めての場所に行ったかどうか、予定の種類（仕事・旅行・人と会うなど。予定のタイトルは送りません）、記録した気持ちの種類、睡眠時間の目安（6時間未満・6〜8時間・8時間以上）、起きた時間帯（例：6〜8時）、曜日、夢に出てきた登録済みの人の関係（パートナー・家族・友人など。名前は送りません）</li>\n    <li>このiPhoneで作るランダムなID（アカウントやお名前とは結びつけません）</li>'),
 ('<p>夢の本文、写真、場所、ヘルスケアのデータ、アカウント情報は送りません。',
  '<p>夢の本文、予定のタイトル、人や場所の名前、いた場所（座標・住所）、写真、正確な時刻、ヘルスケアの数値、アカウント情報は送りません。睡眠は上の3段階の目安だけを送ります。'),
 ('夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータは提供しません。',
  '夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータ（睡眠の目安を含む）は提供しません。'),
 ('it sends only theme words, feelings, date, country and (if chosen) age band and gender under a random ID',
  'it sends theme words, feelings, date, country, (if chosen) age band and gender, and — from version 1.2 with your consent — how the dream links to the days before, only as kinds and rough ranges (kinds of linked records and how many days earlier; for the day before: amount of records, distance-moved range, whether you went somewhere new, kinds of plans, feelings noted, a sleep range, wake-time range, weekday, and the relationship of registered people who appear) under a random ID; never titles, names, coordinates, exact times or health figures. Sleep ranges are never shared with third parties'),
])
ed('terms.html',[
 ('（夢のテーマを表す言葉、夢の中の気持ち、日付、国、年代・性別など）',
  '（夢のテーマを表す言葉、夢の中の気持ち、日付、国、年代・性別、夢とつながった出来事の種類と何日前か、前日の記録の量・移動距離の幅・予定の種類などのおおまかな様子）'),
 ('夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータを提供することはありません。',
  '夢の本文、声、写真、名前、メールアドレス、場所、ヘルスケアのデータ（睡眠の目安を含む）を提供することはありません。'),
 ('2026年11月13日','2026年11月13日'),
])
ed('admin.html',[
 ("<button onclick=\"dl('demographics')\">年代・性別</button>",
  "<button onclick=\"dl('demographics')\">年代・性別</button><br><button onclick=\"dl('days')\">前日の様子 × 夢</button><button onclick=\"dl('links')\">夢とつながった記録</button>"),
])
print('v27 patched')
