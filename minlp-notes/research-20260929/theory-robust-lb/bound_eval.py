"""Evaluate the product lower bound (Theorem 3) for the bang-bang gadget chain.
Usage: python3 bound_eval.py [N]   -> logs/bound_eval.log
Core gaps: class (a)/(b2)/(b3) from the explicit symmetric fooling (gadget_bound.core_gap);
classes b4, b6 from the LP fooling value (robust_bb.Relax, primal = explicit consistent measures).
Psi from gadget_bound.PsiEval (grid sandwich, Dirac foolings)."""
import sys, time
import numpy as np
from gadget_bound import Gadget, core_gap, PsiEval, evaluate
from robust_bb import gadget_chain, Relax

Y1, ETA, EPSF = 0.38, 0.05, 0.02
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
fam = gadget_chain(1, Y1, ETA, EPSF)
g = Gadget(lambda x: fam.u[0](x), lambda z: fam.u[2](z), fam.b[0], fam.u[1].coefs[0][2], fam.b[1],
           name="bang-bang y1=%.2f eta=%.2f eps=%.2f" % (Y1, ETA, EPSF))
print(g.name, "b=%.4f bp=%.4f c=%.4f" % (g.b, g.bp, g.c), flush=True)
t0 = time.time()
P = PsiEval(g, N)
print("Psi grid N=%d set up in %.1fs" % (N, time.time() - t0), flush=True)

def lp_gap(cls, th):
    rel = Relax(fam, cls, K=9)
    lo, up, it = rel.bound(np.full(3, -th), np.full(3, th), target=None, maxit=400, tol=1e-10)
    return -up, -lo

for cls, step in [("a", 0.02), ("b4", 0.02), ("b6", 0.02)]:
    thetas = list(np.round(np.arange(0.40, 1.0 + 1e-9, step), 4))
    if cls == "a":
        gam = [core_gap(g, t, t, t)[0] for t in thetas]
        chk = [lp_gap("a", t)[0] for t in (0.6, 0.8, 1.0)]
        print("class a: symmetric-fooling gaps at theta=.6,.8,1:", [round(gam[thetas.index(t)], 6) for t in (0.6, 0.8, 1.0)],
              " LP gaps:", [round(v, 6) for v in chk], flush=True)
    else:
        gam = [max(lp_gap(cls, t)[0], 0.0) for t in thetas]
    keep = [k for k, v in enumerate(gam) if v > 0]
    k0 = keep[0]
    cores = [(t, t, t) for t in thetas[k0:]]
    gg = gam[k0:]
    print("class %s: gamma(theta) for theta=%s..1: first %.5f, last %.5f" % (cls, thetas[k0], gg[0], gg[-1]), flush=True)
    base, mu, _ = evaluate(g, cores, N=N, verbose=False, gam=gg, P=P)
    print("class %s: best mu=%.3f  base per gadget=%.5f  per variable=%.5f" % (cls, mu, base, base ** (1 / 3)), flush=True)
