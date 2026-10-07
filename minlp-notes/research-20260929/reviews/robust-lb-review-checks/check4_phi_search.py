"""Referee check 4: adversarial search against Theorem 4.3(2) and Section 4.3(a).

(i) Theorem 4.2 needs Phi(mu) = sup_B (vol(B)/8) exp(mu Dhat(B)) with Dhat >= V (class bound of the gadget).
    The authors' computed bound is Phi(2.224) <= 1/1.16278 = 0.86001.  Since Dhat >= V, any box with
    (vol/8) exp(mu V_lower(B)) > 0.86001 would refute it.  We maximise the left side over boxes by random
    search and coordinate hill climbing (several restarts, full cube excluded as a start), using certified
    lower bounds on V.  For other mu the largest value found is a LOWER bound on the true Phi(mu), hence an
    upper bound on what Theorem 4.2 can give with exact gadget bounds at that mu.
(ii) Transport inequality of Section 4.3(a): V(B) <= -gamma + sum_j 2 Lambda_j (1 - rho_j) on every box.
Usage: python3 check4_phi_search.py > logs/check4_phi_search.log"""
import warnings
import numpy as np
from gadget_indep import Gadget, ClassBound

warnings.simplefilter("ignore")
G = Gadget()
cb = ClassBound(G, d=2)
PHI_CLAIM = 1 / 1.16278
A = 1 + G.epsv - (1 - G.eta) * (1 - G.y1) ** 2
gam = G.y1 ** 2 * (1 - A) / A
Lam = np.array([2 * G.y1 ** 2 + 2 * G.y1, 2 * G.y1 + 2 * G.c + G.bp, 2 * G.bp])

def V(box):
    lo, up, _, _ = cb.bound(tuple(float(v) for v in box), tol=1e-10)
    return lo, up

def score(box, mu):
    lo, _ = V(box)
    rho = np.array([(box[1] - box[0]) / 2, (box[3] - box[2]) / 2, (box[5] - box[4]) / 2])
    return float(np.prod(rho) * np.exp(mu * lo))

rng = np.random.default_rng(12345)
boxes = []
worst_transport = -np.inf
for s in range(3000):
    box = []
    for j in range(3):
        a, b = np.sort(rng.uniform(-1, 1, 2))
        if rng.random() < 0.5:
            a, b = -1 + (a + 1) * rng.random() ** 3, 1 - (1 - b) * rng.random() ** 3
        box += [a, b]
    lo, up = V(box)
    rho = np.array([(box[1] - box[0]) / 2, (box[3] - box[2]) / 2, (box[5] - box[4]) / 2])
    worst_transport = max(worst_transport, up - (-gam + np.sum(2 * Lam * (1 - rho))))
    boxes.append(tuple(box))
print("transport check on 3000 random boxes: max of V_upper - Dhat_transport = %.4f (must be <= 0)" % worst_transport)
for th in (0.3, 0.46, 0.6, 0.8, 0.9, 0.95, 0.98):
    for j in range(3):
        box = [-1, 1, -1, 1, -1, 1]; box[2 * j + 1] = th
        boxes.append(tuple(box))
    boxes.append((-th, th, -th, th, -th, th))

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
    return v, tuple(box)

full = (-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
for mu in (2.224, 1.5, 3.0, 4.0, 6.0):
    ranked = sorted(((score(b, mu), b) for b in boxes), reverse=True)
    starts = [b for _, b in ranked[:10]]
    found = [(score(full, mu), full)]
    for b in starts:
        found.append(climb(b, mu))
    found.sort(reverse=True)
    v, b = found[0]
    lo, up = V(b)
    nonfull = [f for f in found if max(abs(np.array(f[1]) - np.array(full))) > 1e-9]
    print("mu=%.3f: largest (vol/8) exp(mu V) found = %.5f at box %s (V=%.5f); best non-full-cube %.5f at %s"
          % (mu, v, np.round(b, 3), lo, nonfull[0][0] if nonfull else float('nan'),
             np.round(nonfull[0][1], 3) if nonfull else None))
    print("        => Theorem 4.2 with exact V at this mu gives at most %.4f per gadget (%.4f per variable)"
          % (1 / v, (1 / v) ** (1 / 3)))
    if abs(mu - 2.224) < 1e-9:
        print("        claimed Phi(2.224) <= %.5f -> %s" % (PHI_CLAIM, "consistent" if v <= PHI_CLAIM else "VIOLATION"))
