"""T3: adversarial local search for large gaps under the hypotheses of Corollaries B/C
(acyclic, no edge constraints, finite apertures).

Score (Euclidean):  (OPT/REL_H - 1) / (kappa_max - 1),  kappa_e = sec(theta_e)  (<= 1 by Cor. B)
Score (squared):    (OPT/REL_H - 1) / (kappa^sq_max - 1), kappa^sq_e = sec^2(theta_e) for balls.
Templates: fork-merge, crossing, double crossing, layered 2x3 balls (all in R^2 or R^3).
Usage: python3 t3_adversarial.py [norm l2|sq] [iters per template] [seed]
"""
import sys
import numpy as np
from gcslib import *

NORM = sys.argv[1] if len(sys.argv) > 1 else "l2"
IT = int(sys.argv[2]) if len(sys.argv) > 2 else 150
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
KAP = kappa_l2 if NORM == "l2" else kappa_sq
COST = L2 if NORM == "l2" else SQ

# template: list of (name, kind), edges; parameters: centre (dim) per vertex (+ radius for balls)
TEMPLATES = {
    "forkmerge": ([("s", "p"), ("A", "b"), ("P", "p"), ("M", "p"), ("B", "b"), ("t", "p")],
                  [("s", "A"), ("A", "P"), ("A", "M"), ("P", "B"), ("M", "B"), ("B", "t")]),
    "crossing": ([("s", "p"), ("u1", "p"), ("u2", "p"), ("v", "b"), ("w1", "p"), ("w2", "p"), ("t", "p")],
                 [("s", "u1"), ("s", "u2"), ("u1", "v"), ("u2", "v"), ("v", "w1"), ("v", "w2"), ("w1", "t"), ("w2", "t")]),
    "dblcross": ([("s", "p"), ("u1", "p"), ("u2", "p"), ("v1", "b"), ("m1", "p"), ("m2", "p"), ("v2", "b"),
                  ("w1", "p"), ("w2", "p"), ("t", "p")],
                 [("s", "u1"), ("s", "u2"), ("u1", "v1"), ("u2", "v1"), ("v1", "m1"), ("v1", "m2"), ("m1", "v2"),
                  ("m2", "v2"), ("v2", "w1"), ("v2", "w2"), ("w1", "t"), ("w2", "t")]),
    "layer2x3": ([("s", "p"), ("a1", "b"), ("a2", "b"), ("b1", "b"), ("b2", "b"), ("c1", "b"), ("c2", "b"), ("t", "p")],
                 [("s", "a1"), ("s", "a2"), ("a1", "b1"), ("a1", "b2"), ("a2", "b1"), ("a2", "b2"),
                  ("b1", "c1"), ("b1", "c2"), ("b2", "c1"), ("b2", "c2"), ("c1", "t"), ("c2", "t")]),
}


def build(tmpl, prm, dim):
    V, E = TEMPLATES[tmpl]
    sets, k = {}, 0
    for name, kind in V:
        c = prm[k:k + dim]
        k += dim
        if kind == "b":
            sets[name] = ball(c, abs(prm[k]) + 1e-3)
            k += 1
        else:
            sets[name] = point(c)
    return GCS(sets, E, "s", "t", COST)


def nparams(tmpl, dim):
    V, _ = TEMPLATES[tmpl]
    return sum(dim + (kind == "b") for _, kind in V)


def score(tmpl, prm, dim):
    g = build(tmpl, prm, dim)
    km = max(KAP(g.sets[u], g.sets[v]) for u, v in g.edges)
    if not np.isfinite(km) or km > 4 or km - 1 < 1e-4:   # guard: tiny kappa-1 makes the score solver noise
        return -1.0, None
    rh = relax(g, hull=True)
    if not np.isfinite(rh) or rh <= 1e-6:
        return -1.0, None
    o = opt(g)
    return (o / rh - 1) / (km - 1), (o / rh, km)


def init(tmpl, dim):
    V, _ = TEMPLATES[tmpl]
    prm = []
    order = {n: i for i, (n, _) in enumerate(V)}
    for name, kind in V:
        x = np.r_[3.0 * order[name] + rng.uniform(-1, 1), rng.uniform(-3, 3, dim - 1)]
        prm += list(x)
        if kind == "b":
            prm.append(rng.uniform(0.3, 1.5))
    return np.array(prm)


best_all = {}
for tmpl in (TEMPLATES if __name__ == "__main__" else []):
    for dim in (2, 3):
        best, bp, binfo = -1, None, None
        for it in range(IT):
            if bp is None or rng.random() < 0.15:
                p = init(tmpl, dim)
            else:
                p = bp + rng.standard_normal(len(bp)) * rng.choice([0.03, 0.1, 0.3])
            try:
                sc, info = score(tmpl, p, dim)
            except Exception:
                continue
            if sc > best:
                best, bp, binfo = sc, p, info
        best_all[(tmpl, dim)] = (best, binfo, bp)
        print(f"{NORM} {tmpl:9s} dim={dim} best score={best:.4f} OPT/REL_H={binfo[0] if binfo else float('nan'):.5f} "
              f"kmax={binfo[1] if binfo else float('nan'):.5f}", flush=True)
if best_all:
    b = max(best_all.items(), key=lambda kv: kv[1][0])
    print(f"[{NORM}] overall best score {b[1][0]:.4f} ({b[0]}); params={np.round(b[1][2], 4).tolist()}")
