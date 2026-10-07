"""Scan gadget parameters for the product-bound base under classes a, b4, b6 (LP core gaps for b_d).
Usage: python3 scan_bd.py CLS y1 eta epsf  -> one line."""
import sys
import numpy as np
from gadget_bound import Gadget, core_gap, PsiEval, evaluate
from robust_bb import gadget_chain, Relax

cls = sys.argv[1]; y1, eta, epsf = map(float, sys.argv[2:5])
fam = gadget_chain(1, y1, eta, epsf)
g = Gadget(lambda x: fam.u[0](x), lambda z: fam.u[2](z), fam.b[0], fam.u[1].coefs[0][2], fam.b[1])
thetas = list(np.round(np.arange(0.40, 1.0 + 1e-9, 0.02), 4))
if cls == "a":
    gam = [core_gap(g, t, t, t)[0] for t in thetas]
else:
    gam = []
    for t in thetas:
        rel = Relax(fam, cls, K=9)
        lo, up, it = rel.bound(np.full(3, -t), np.full(3, t), target=None, maxit=400, tol=1e-10)
        gam.append(max(-up, 0.0))
keep = [k for k, v in enumerate(gam) if v > 1e-9]
if not keep:
    print(cls, y1, eta, epsf, "no gap"); sys.exit()
k0 = keep[0]
cores = [(t, t, t) for t in thetas[k0:]]
base, mu, _ = evaluate(g, cores, N=100, verbose=False, gam=gam[k0:])
print("%s y1=%.2f eta=%.3f eps=%.3f gamma(1)=%.5f base/gadget=%.5f per-var=%.5f mu=%.3f" % (cls, y1, eta, epsf, gam[-1], base, base ** (1 / 3), mu), flush=True)
