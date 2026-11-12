import sys,os,re,html
D=sys.argv[1] if len(sys.argv)>1 else '.'
BASE='https://iwakeupeverymorninginordertodream.com/'
for fn,lang,url in (('index.html','ja_JP',BASE),('en.html','en_US',BASE+'en.html')):
    p=os.path.join(D,fn)
    if not os.path.exists(p): continue
    s=open(p,encoding='utf-8').read()
    if '<!--v25-->' in s: continue
    t=re.search(r'<title>(.*?)</title>',s,re.S); t=t.group(1).strip() if t else 'Dream'
    d=re.search(r'<meta\s+name="description"\s+content="([^"]*)"',s); d=d.group(1) if d else t
    tags=('<!--v25-->\n<meta property="og:type" content="website">\n'
      f'<meta property="og:site_name" content="Dream">\n<meta property="og:title" content="{t}">\n'
      f'<meta property="og:description" content="{d}">\n<meta property="og:url" content="{url}">\n'
      f'<meta property="og:image" content="{BASE}og.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
      f'<meta property="og:locale" content="{lang}">\n<meta name="twitter:card" content="summary_large_image">\n'
      f'<meta name="twitter:image" content="{BASE}og.png">\n')
    s=s.replace('</head>',tags+'</head>',1)
    open(p,'w',encoding='utf-8').write(s)
print('v25 patched')
