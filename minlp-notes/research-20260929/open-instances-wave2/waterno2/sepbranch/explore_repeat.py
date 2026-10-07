"""Cost of exploiting period repetition (SCIP estimates, exploration only):
p4-centred cells of widths (w1, w2, w3); slopes per link (KKT at p4) versus
one common slope for all links; and, for periods 1-4, the demand relaxed to the
interval of the middle-period demands (one pair evaluation would then serve
all four periods)."""
import sys, json, copy
import numpy as np
sys.path.insert(0, "..")
import core, terminal, period, bundle, evalpt, plan
T = 6
D0 = core.setup(T, "../logs/implied_06.json")
terminal.add_terminal_row(D0)
M, S = D0["M"], D0["S"]
x, obj = evalpt.read_sol("../data/waterno2_06.p4.sol", M["names"])
lev = [np.array([float(x[a]) for (i, a, b) in S["link"][t]]) for t in range(T - 1)]
cfg = {"mult": "../logs/kkt_p4_06.json"}
lam_link = plan.load_slopes(D0, cfg)
lam_common = [list(np.mean(np.array(lam_link), axis=0))] * (T - 1)
dem = {}
for t in range(T):
    for i in S["per_rows"][t]:
        r = M["rows"][i]
        if len(r["poly"]) == 1 and r["lb"] == r["ub"] and len(next(iter(r["poly"]))) == 1:
            dem[t] = i
dmid = sorted(M["rows"][dem[t]]["lb"] for t in range(1, T - 1))
D1 = copy.deepcopy(D0)
for t in range(1, T - 1):
    D1["M"]["rows"][dem[t]]["lb"] = min(dmid, key=float)
    D1["M"]["rows"][dem[t]]["ub"] = max(dmid, key=float)
print("demand rows", {t: M["rows"][dem[t]]["name"] for t in dem}, "middle interval", min(dmid, key=float), max(dmid, key=float))
from multiprocessing import Pool
def job(a):
    variant, ws, t = a
    lam = lam_link if variant == "per-link" else lam_common
    D = D1 if variant == "common+interval" else D0
    box = {}
    for (link, idx) in ((t - 1, 1), (t, 0)):
        if 0 <= link < T - 1:
            lo, hi = core.level_box(D0, link)
            for k, row in enumerate(S["link"][link]):
                box[row[1 + idx]] = (max(lo[k], lev[link][k] - ws[k] / 2), min(hi[k], lev[link][k] + ws[k] / 2))
    L = [[0.0] * 3 for _ in range(T - 1)]
    if t > 0: L[t - 1] = lam[t - 1]
    if t < T - 1: L[t] = lam[t]
    r = period.solve_window(D, t, t + 1, L, 0.0, 60, bundle.NOPROP, box)
    return variant, ws, t, r["primal"]
jobs = [(v, ws, t) for v in ("per-link", "common", "common+interval")
        for ws in ((1.0, 1.0, 0.5), (0.5, 0.5, 0.5), (0.25, 0.25, 0.25), (0.1, 0.1, 0.1)) for t in range(T)]
with Pool(8) as p:
    res = p.map(job, jobs, chunksize=1)
tab = {}
for v, ws, t, pr in res:
    tab.setdefault((v, ws), []).append(pr)
for (v, ws), vals in tab.items():
    print(v, ws, "sum %.3f" % sum(vals), [round(a, 3) for a in vals])
