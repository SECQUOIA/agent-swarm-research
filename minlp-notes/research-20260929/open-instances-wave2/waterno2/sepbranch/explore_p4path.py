"""Pair values (SCIP estimates, exploration only) along cells of width w centred
at the link levels of MINLPLib point p4, for two slope choices."""
import sys, json
import numpy as np
sys.path.insert(0, "..")
import core, terminal, period, bundle, evalpt, sepbranch
T = 6
D = core.setup(T, "../logs/implied_06.json")
terminal.add_terminal_row(D)
M, S = D["M"], D["S"]
x, obj = evalpt.read_sol("../data/waterno2_06.p4.sol", M["names"])
lev = [np.array([float(x[a]) for (i, a, b) in S["link"][t]]) for t in range(T - 1)]
areas = sepbranch.link_areas(D)
def fold(m):
    return [[l[k] + m["mu"] * float(ar[k]) / 3600 for k in range(3)] for l, ar in zip(m["lam"], areas)]
slopes = {"wave2": fold(json.load(open("../logs/mult_06_w1_impl.json"))),
          "kkt_p4": fold(json.load(open("../logs/kkt_p4_06.json")))}
from multiprocessing import Pool
def job(a):
    name, w, t = a
    lam = slopes[name]
    box = {}
    for (link, idx) in ((t - 1, 1), (t, 0)):
        if 0 <= link < T - 1:
            lo, hi = core.level_box(D, link)
            for k, row in enumerate(S["link"][link]):
                v = row[1 + idx]
                box[v] = (max(lo[k], lev[link][k] - w / 2), min(hi[k], lev[link][k] + w / 2))
    L = [[0.0] * 3 for _ in range(T - 1)]
    if t > 0: L[t - 1] = lam[t - 1]
    if t < T - 1: L[t] = lam[t]
    r = period.solve_window(D, t, t + 1, L, 0.0, 60, bundle.NOPROP, box)
    return name, w, t, r["primal"], r["dual"], r["status"]
jobs = [(n, w, t) for n in slopes for w in (3.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.02, 0.0) for t in range(T)]
with Pool(16) as p:
    res = p.map(job, jobs, chunksize=1)
tab = {}
for n, w, t, pr, du, st in res:
    tab.setdefault((n, w), []).append((pr, du, st))
for (n, w), v in tab.items():
    print(n, w, "sum primal %.4f" % sum(a[0] for a in v), "sum dual %.4f" % sum(a[1] for a in v),
          [round(a[0], 3) for a in v], set(a[2] for a in v))
