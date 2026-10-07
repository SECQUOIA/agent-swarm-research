"""Pair values (SCIP estimates, exploration only) along p4-centred cells with
per-tank widths, for two slope choices: which tanks must be refined?"""
import sys, json, itertools
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
    name, ws, t = a
    lam = slopes[name]
    box = {}
    for (link, idx) in ((t - 1, 1), (t, 0)):
        if 0 <= link < T - 1:
            lo, hi = core.level_box(D, link)
            for k, row in enumerate(S["link"][link]):
                v = row[1 + idx]
                box[v] = (max(lo[k], lev[link][k] - ws[k] / 2), min(hi[k], lev[link][k] + ws[k] / 2))
    L = [[0.0] * 3 for _ in range(T - 1)]
    if t > 0: L[t - 1] = lam[t - 1]
    if t < T - 1: L[t] = lam[t]
    r = period.solve_window(D, t, t + 1, L, 0.0, 60, bundle.NOPROP, box)
    return name, ws, t, r["primal"], r["status"]
W = [9.0, 1.0, 0.5, 0.2]
jobs = [(n, ws, t) for n in slopes for ws in itertools.product(W, W, W) for t in range(T)]
with Pool(16) as p:
    res = p.map(job, jobs, chunksize=1)
tab = {}
for n, ws, t, pr, st in res:
    tab.setdefault((n, ws), []).append(pr)
for (n, ws), v in sorted(tab.items()):
    print(n, ws, "sum %.3f" % sum(v))
