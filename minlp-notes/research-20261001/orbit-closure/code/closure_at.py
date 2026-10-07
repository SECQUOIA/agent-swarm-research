"""Closure value of family A or B at the Theorem 14 corner for one cost vector (numerical).
Usage: python3 closure_at.py FAM w1 w2 w3"""
import sys, json, warnings, time
import numpy as np
warnings.filterwarnings('ignore')
from orbit_lib import Corner, corner_bound
from closure import closure_value, price
sb = np.array([-4.5, 0, 1.5])
P = np.column_stack([np.array(v) - sb for v in ([-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5])])
fam = sys.argv[1]; w = np.array([float(v) for v in sys.argv[2:5]])
cn = Corner(sb, P)
t = time.time()
zK, lamK = corner_bound(sb, P, w)
z, lam, cuts, th, hist = closure_value(cn, w, fam=fam, maxit=60, tol=1e-7)
pv = price(cn, lam, fam=fam, nsample=20000, nstart=30, rng=np.random.default_rng(7))[0]
print(json.dumps(dict(fam=fam, w=w.tolist(), zK=float(zK), zcl=float(z), zcl_up=float(z / min(pv, 1.0)), lam=lam.tolist(),
                      ratio=float(zK / z), ncuts=len(cuts), seconds=time.time() - t)))
