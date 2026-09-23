import numpy as np, time, sys
from bh import *
from facets import *
from ecg_bnb import bnb
P = PBH(6, W0=1)
for s in (F13, F14, F15):
    a, c = parse(s)
    val, z = P.minimize(a)
    z = np.round(z*6)/6
    t = time.time()
    res = bnb(6, z, verbose=True, maxboxes=int(float(sys.argv[1])))
    print(res['status'], res['best'][0], len(res['cand']), res.get('processed'), time.time()-t, flush=True)
