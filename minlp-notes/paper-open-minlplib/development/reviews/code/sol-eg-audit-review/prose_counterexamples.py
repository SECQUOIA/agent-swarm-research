from fractions import Fraction as F
import mpmath as mp
import numpy as np
mp.mp.prec=512
eps=mp.mpf(1)/10**14
rng=np.random.default_rng(406)
found={}
for x in rng.uniform(-5,0,100000):
    ex=mp.exp(mp.mpf(float(x)))
    y=float(ex*(1+eps))
    while mp.mpf(y)>ex*(1+eps):
        y=float(np.nextafter(y,-np.inf))
    elo=y*(1-1e-14)
    if mp.mpf(elo)>ex and 'elo' not in found:
        found['elo']=(float(x),y,elo,float(mp.mpf(elo)/ex-1))
    y=float(ex*(1-eps))
    while mp.mpf(y)<ex*(1-eps):
        y=float(np.nextafter(y,np.inf))
    ehi=y*(1+1e-14)+1e-300
    if mp.mpf(ehi)<ex and 'ehi' not in found:
        found['ehi']=(float(x),y,ehi,float(mp.mpf(ehi)/ex-1))
    if len(found)==2:
        break
assert len(found)==2
for what,case in found.items():
    print(what,'(x, hypothetical E-compliant y, computed end, relative defect):',case)
u=F(1,2**53)
pad0=F(1.1e-14)*(1-u)**4
dw_limit=1-1/((1+pad0)*(1-u)**2)
print('Conservative exact dw intercept eps limit:',float(dw_limit))
print('Quoted 1.0778e-14 exceeds that exact limit:',F('1.0778e-14')>dw_limit)
print('These are counterexamples to individual table properties under (E), not to final term bounds.')
