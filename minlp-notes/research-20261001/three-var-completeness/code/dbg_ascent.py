import warnings; warnings.filterwarnings("ignore")
import numpy as np
from cube3 import *
from sdp3 import *
rng = np.random.default_rng(5)
S = Separation(); R = Relaxation(use_family=False)
for s in range(4):
    c = rng.normal(size=10); c[4:7] = np.abs(c[4:7])
    val, st, y = R.solve(c)
    print('start', s, val, st)
    for it in range(8):
        yq = np.array([y[MINDEX[k]] for k in QKEYS])
        sv, sst, p = S.solve(yq)
        rv, rst, y = R.solve(p)
        print('  it', it, 'sep', sv, sst, 'Rmin', rv, rst)
