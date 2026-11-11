# Pulls the site from GitHub, applies patch_*.py, copies changed files into /out
import urllib.request as U, os, sys, tempfile, shutil, filecmp
B='https://raw.githubusercontent.com/YusukeSasamura/dream-server/main/site/'
OUT=os.environ.get('OUT','/out')
def get(n): return U.urlopen(B+n,timeout=30).read()
try: L=get('sync.txt').decode().split()
except Exception: L=['index.html','en.html','style.css','icon.svg','patch_give.py','patch_freud.py','patch_breaks.py']
T=tempfile.mkdtemp()
for n in L: open(os.path.join(T,n),'wb').write(get(n))
for n in L:
    if n.startswith('patch_') and n.endswith('.py'):
        sys.argv=[n,T]; exec(compile(open(os.path.join(T,n),encoding='utf-8').read(),n,'exec'),{'__name__':'__main__'})
for n in L:
    if n.endswith('.py'): continue
    d=os.path.join(OUT,n)
    if not os.path.exists(d) or not filecmp.cmp(os.path.join(T,n),d,shallow=False):
        shutil.copy(os.path.join(T,n),d); print('updated',n)
shutil.rmtree(T)
