"""Root gaps of the uniform design chain UD for the balanced and the unsplit factorization (per-factor
envelopes, class 'env' of robust_bb) and for class (a); n = 3..16.  Floating point."""
import sys, json
import numpy as np
sys.path.insert(0, "..")
from robust_bb import Family, Relax
from uniform_design import make_pw, dp_fstar
from run_uniform import PARAMS, B
u = make_pw(PARAMS[0], B, *PARAMS[1:])
for n in [3, 4, 5, 6, 8, 10, 12, 16]:
    fs, xs = dp_fstar(u, B, n)
    out = dict(n=n, fstar=fs)
    for name, cls, base in [("bal", "env", "balanced"), ("unsplit", "env", "unsplit"), ("a", "a", "balanced")]:
        rel = Relax(Family([u] * n, [B] * (n - 1)), cls, base, K=7)
        lo, up, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=120, tol=1e-10)
        out[name] = (round(fs - up, 6), round(fs - lo, 6))
    print(json.dumps(out), flush=True)
