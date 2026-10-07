"""Referee check 4b: ceiling of the tilted-volume method (Theorem 4.2) for the reference gadget, class (a).
For every mu, Phi(mu) >= max(exp(-mu gamma) [full cube], sup over corner boxes of (vol/8) exp(mu V)).
So even with exact gadget bounds V, Theorem 4.2 gives at most  max_mu 1/Phi(mu)  per gadget.
Corner boxes are found by hill climbing from the 8 corners (boxes of side 0.2) at each mu.
Usage: python3 check4b_ceiling.py > logs/check4b_ceiling.log"""
import itertools
import warnings
import numpy as np
from gadget_indep import Gadget, ClassBound

warnings.simplefilter("ignore")
G = Gadget(); cb = ClassBound(G, d=2)
A = 1 + G.epsv - (1 - G.eta) * (1 - G.y1) ** 2
gam = G.y1 ** 2 * (1 - A) / A

def score(box, mu):
    lo, _, _, _ = cb.bound(tuple(float(v) for v in box), tol=1e-10)
    rho = [(box[1] - box[0]) / 2, (box[3] - box[2]) / 2, (box[5] - box[4]) / 2]
    return float(np.prod(rho) * np.exp(mu * lo))

def climb(box, mu, steps=(0.1, 0.03, 0.01, 0.003)):
    box = list(box); v = score(box, mu)
    for h in steps:
        improved = True
        while improved:
            improved = False
            for k in range(6):
                for sgn in (-1, 1):
                    nb = list(box); nb[k] = float(np.clip(nb[k] + sgn * h, -1, 1))
                    if nb[2 * (k // 2)] >= nb[2 * (k // 2) + 1] - 1e-6:
                        continue
                    nv = score(nb, mu)
                    if nv > v + 1e-12:
                        box, v, improved = nb, nv, True
    return v, box

best_base = 0
for mu in (2.224, 2.3, 2.4, 2.5, 2.6, 2.75, 3.0, 3.5):
    corner = 0; cbox = None
    for s in itertools.product((-1, 1), repeat=3):
        box = []
        for sj in s:
            box += [0.8, 1.0] if sj > 0 else [-1.0, -0.8]
        v, b = climb(box, mu)
        if v > corner:
            corner, cbox = v, b
    full = np.exp(-mu * gam)
    phi_lb = max(full, corner)
    best_base = max(best_base, 1 / phi_lb)
    print("mu=%.3f: full cube %.5f, best corner box %.5f at %s -> Phi(mu) >= %.5f -> base per gadget <= %.4f"
          % (mu, full, corner, np.round(cbox, 3), phi_lb, 1 / phi_lb), flush=True)
print("ceiling of Theorem 4.2 for this gadget (over the mu tested): <= %.4f per gadget, %.4f per variable"
      % (best_base, best_base ** (1 / 3)))
