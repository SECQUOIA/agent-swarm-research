import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys, time
sys.dont_write_bytecode = True
import numpy as np
import annx
M = annx.Model()
Z = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
rng = np.random.default_rng(5)
sel = rng.choice(len(Z["key"]), 256, replace=False)
Lstar = float(Z["LB"])
for B in (16, 64):
    t0 = time.time()
    for q in range(0, 256, B):
        m, h, C, A, R, S = M.forward(Z["lo"][sel[q:q+B]], Z["hi"][sel[q:q+B]])
    t1 = time.time()
    print(f"forward only, batch {B}: {(t1-t0)/256*1e3:.2f} ms/box")
t0 = time.time()
lbs = []; infos = []
for q in range(0, 256, 64):
    lb, info, plain = M.bound(Z["lo"][sel[q:q+64]], Z["hi"][sel[q:q+64]], target=Lstar)
    lbs.append(lb); infos += info
lb = np.concatenate(lbs)
from collections import Counter
print(f"full bound: {(time.time()-t0)/256*1e3:.2f} ms/box; kinds {Counter(i[0] for i in infos)}; >= L*: {(lb >= Lstar).mean():.3f}; >= UB-tol: {(lb >= -3379.9857).mean():.3f}")
