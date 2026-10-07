"""One B&B job; prints one line.  Usage:
  python3 run_job.py chain CLS EPS DELTA G [BASE]    (BASE: gadget = theorem's base split, default; balanced)
  python3 run_job.py program CLS BASE EPS SEED n     (kappa=0.1, b=0.8, c ~ U(-0.3,0.3) with SEED, or zero if SEED<0)
"""
import sys, os, json
import numpy as np
from scipy import optimize
from robust_bb import gadget_chain, program_family, bb

def fstar_local(fam, starts=40):
    n = fam.n; rng = np.random.default_rng(0); best = None
    for x0 in [np.zeros(n)] + [rng.uniform(-1, 1, n) for _ in range(starts)]:
        r = optimize.minimize(fam.f, x0, method="L-BFGS-B", bounds=[(-1, 1)] * n,
                              options={"ftol": 1e-15, "gtol": 1e-12, "maxiter": 5000})
        if best is None or r.fun < best.fun:
            best = r
    return float(best.fun)

kind = sys.argv[1]
if kind == "chain":
    cls, eps, delta, G = sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
    base = sys.argv[6] if len(sys.argv) > 6 else "gadget"
    fam = gadget_chain(G, delta=delta)
    fs = fstar_local(fam)
    r = bb(fam, cls, eps, base=base, fstar=min(fs, 0.0))
    print(json.dumps(dict(kind=kind, cls=cls, base=base, eps=eps, delta=delta, G=G, n=3 * G, fstar_local=fs, **r)), flush=True)
else:
    cls, base, eps, seed, n = sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    c = np.zeros(n) if seed < 0 else np.random.default_rng(seed).uniform(-0.3, 0.3, n)
    fam = program_family(n, 0.1, 0.8, c)
    fs = fstar_local(fam)
    r = bb(fam, cls, eps, base=base, fstar=fs)
    print(json.dumps(dict(kind=kind, cls=cls, base=base, eps=eps, seed=seed, n=n, fstar=fs, **r)), flush=True)
