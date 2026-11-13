import sys,os,re
D=sys.argv[1] if len(sys.argv)>1 else '.'
def ed(fn,pairs):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return
    s=open(p,encoding='utf-8').read()
    if '<!--v26-->' in s: return
    for a,b in pairs: s=re.sub(a,b,s)
    s=s.replace('</body>','<!--v26-->\n</body>',1)
    open(p,'w',encoding='utf-8').write(s)
ed('index.html',[
 (r'最初の1か月は無料（月額480円(（予定）)?）','すべての機能が無料'),
 (r'(<section class="offer pad" id="price">\s*<p class="kicker">)Subscription(</p>)',r'\1Free\2'),
 (r'すべての機能が使えます。App Storeでいつでも解約できます。','登録や課金はありません。すべての機能を無料で使えます。'),
 (r'最初の1か月は無料、?その後 ?月額480円(（予定）)?','すべての機能が無料'),
])
ed('en.html',[
 (r'First month free \(¥480/month\)','Free — every feature'),
 (r'(<section class="offer pad" id="price">\s*<p class="kicker">)Subscription(</p>)',r'\1Free\2'),
 (r'Every feature included\. Cancel anytime in the App Store\.','No subscription, no in-app purchases. Every feature is free.'),
 (r'1 month free, then ¥480 ?/ ?month( \(planned\))?','Free — every feature'),
])
ed('terms.html',[
 (r'Dreamは、すべての機能をひとつのプランで使えます。最初の1か月は無料で、その後は月額480円(（予定）)?です。','Dreamは無料です。すべての機能を、料金なしで使えます。'),
 (r'<li>お支払い・更新・解約はApp Storeで行います。[^<]*</li>','<li>アプリ内課金や広告はありません。以前に購読を始めた方は、iPhoneの「設定 › Apple ID › サブスクリプション」から解約できます。解約すれば、以後の料金はかかりません。</li>'),
 (r'購入には、おうちの人の同意が必要です。',''),
 (r'Every feature is in one plan: the first month is free, then ¥480/month( \(planned\))?\.','Dream is free: every feature, no charge.'),
 (r'You subscribe and cancel through the App Store\.','There are no in-app purchases; if you subscribed earlier, you can cancel in Settings › Apple ID › Subscriptions.'),
 (r'2026年11月11日','2026年11月13日'),
])
print('v26 patched')
