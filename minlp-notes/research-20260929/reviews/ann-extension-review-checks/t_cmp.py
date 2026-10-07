import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys, time
sys.dont_write_bytecode = True
import numpy as np
import annx
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann")
import importlib.util
spec = importlib.util.spec_from_file_location("tmmod", _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ann_tm.py")
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
M = annx.Model(); FM = annx.float_model()
AM = T.SepModel(); AM.full_mu = False; AM.old_min_relw = 1.0 / 16; AM.grad_small = True
UB, ub_u = T.incumbent(AM); lag, _ = T.kkt_lag(AM, ub_u); AM.lag = lag
Z = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
order = np.argsort(Z["key"])
rng = np.random.default_rng(3)
sel = list(order[:10]) + list(rng.choice(len(order), 20, replace=False))
lo, hi = Z["lo"][sel], Z["hi"][sel]
lb, info, plain = M.bound(lo, hi)
R = AM.fbound_combo(lo, hi, UB)
R2 = AM.fbound_combo(lo, hi, np.inf)
for q in range(len(sel)):
    U = lo[q] + (hi[q] - lo[q]) * rng.random((20000, 5))
    f, s, X = FM.eval(U)
    nf = int((s >= 0).sum()); fmin = f[s >= 0].min() if nf else np.inf
    print(f"key {Z['key'][sel[q]]:.4f} | mine {lb[q]:.4f} ({info[q][0]}) | authors(UB) {R['lb'][q]:.4f} tm {R['lb_tm'][q]:.4f} mod {R['mod'][q]} | authors(inf) {R2['lb'][q]:.4f} | "
          f"feasible samples {nf}/20000 min f {fmin:.4f} max slack {s.max():.3e}")
