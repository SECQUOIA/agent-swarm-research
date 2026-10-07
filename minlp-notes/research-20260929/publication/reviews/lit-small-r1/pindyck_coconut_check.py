# Independent recomputation (reviewer's own code) of the pindyck objective at
# the COCONUT prices, under the MINLPLib structure, with exponent factor f.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re, mpmath as mp
mp.mp.dps = 40
src=(_PUBLIC_REPO + '/research-20260929/publication/literature/small/sources/')
res=open(src+'coconut/lib1_pindyck.res').read()
x={int(k):mp.mpf(v) for k,v in re.findall(r'x\((\d+)\)\s*=\s*([-0-9.eE+]+)',res)}
p=[x[i] for i in range(1,17)]
g=open(src+'minlplib_gms/pindyck.gms').read()
consts=[mp.mpf(c) for c in re.findall(r'e\d+\.\.\s+0\.13\*x\d+ - 0\.87\*x\d+ \+ x\d+ =E= ([0-9.]+);',g)]
assert len(consts)==16, len(consts)
m=re.search(r'e97\.\.(.*?)=E= 0;',g,flags=re.S).group(1)
disc=[mp.mpf(1)]+[mp.mpf(c) for c in re.findall(r'- ([0-9.]+)\*x1\d\d',m)]
assert len(disc)==16, len(disc)
def J(f):
    td=mp.mpf(18); s=mp.mpf('6.5'); cs=mp.mpf(0); R=mp.mpf(500); tot=0; mind=None
    for t in range(16):
        td=mp.mpf('0.87')*td-mp.mpf('0.13')*p[t]+consts[t]
        a=mp.mpf('0.75')*s; b=mp.mpf('1.1')+mp.mpf('0.1')*p[t]
        F=lambda z: z-a-b*mp.power(mp.mpf('1.02'),-f*(cs+z))
        snew=mp.findroot(F,a+b/2)
        s=snew; cs=cs+s
        d=td-s; R=R-d
        tot+=disc[t]*(p[t]-250/R)*d
        mind=d if mind is None else min(mind,d)
    return tot,mind
for f in (mp.mpf(1), mp.mpf('0.142857142857143')):
    tot,mind=J(f)
    print('factor',mp.nstr(f,15),'J =',mp.nstr(tot,18),'min OPEC demand =',mp.nstr(mind,8))
print('ln(1.02) =',mp.nstr(mp.log(mp.mpf('1.02')),20))
