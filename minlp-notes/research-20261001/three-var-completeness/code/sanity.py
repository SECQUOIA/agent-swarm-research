import time
import numpy as np
from cube3 import *
from sdp3 import *
p = {(2,0,0):1,(0,2,0):1,(0,0,2):9,(1,1,0):6,(1,0,1):-12,(0,1,1):-12,(1,0,0):-1,(0,1,0):-1,(0,0,1):9,(0,0,0):0.25}
pv = vector_from_quad(p)
print('cube min', cube_min(pv))
fm = family_member(0.5,1,1,3,1)
print('family member equals p:', all(abs(fm.get(k,0)-p.get(k,0))<1e-12 for k in set(fm)|set(p)))
t=time.time(); R0 = Relaxation(use_family=False); print('D3 only', R0.solve(pv)[:2], time.time()-t)
t=time.time(); R1 = Relaxation(use_family=True); print('D3+family', R1.solve(pv)[:2], time.time()-t)
# family copies: compose p with each group element; should also be ~0
vals=[]
for g in GROUP:
    q = compose(p, g)
    vals.append(R1.solve(vector_from_quad(q))[0])
print('min over all 48 compositions', min(vals))
S = Separation()
rng = np.random.default_rng(0)
t=time.time()
for _ in range(3):
    w = rng.normal(size=10); w[0]=1
    val, st, pp = S.solve(w)
    print('sep', val, st, 'cube min of p', cube_min(pp), 'R value', R1.solve(pp)[0])
print(time.time()-t)
