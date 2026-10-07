"""Find rbb's unbranchable leaf for a record and check its LP point against
the original rows (float evaluation, diagnosis only)."""
import sys, pickle, heapq
import numpy as np
sys.path.insert(0, "..")
import tasks, core, rbb
from dpcells import CellPlan  # noqa
P = pickle.load(open(sys.argv[1], "rb"))
rec = P.crecs[int(sys.argv[2])]
tasks.init(P.T, "../logs/implied_06.json", True)
D = tasks._W["D"]
t = rec["t"]
PB = core.PeriodBounder(D, t)
W = PB.W
lo, hi = PB.box(None if rec["cin_box"] is None else (np.array(rec["cin_box"][0]), np.array(rec["cin_box"][1])),
                None if rec["cout_box"] is None else (np.array(rec["cout_box"][0]), np.array(rec["cout_box"][1])))
c = PB.objective(rec["lam_in"], rec["lam_out"], rec["mu"])
target = rec["target"]
orig = rbb.choose_branch
found = []
def spy(W_, lo_, hi_, x):
    v, s = orig(W_, lo_, hi_, x)
    if v is None:
        found.append((lo_.copy(), hi_.copy(), x.copy()))
    return v, s
rbb.choose_branch = spy
W.lo0, W.hi0 = lo, hi
res = rbb.solve(W, c, target, node_limit=20000, time_limit=120, obbt_vars=PB.obbt_vars)
print("rbb", res)
M = D["M"]
for (l, h, x) in found[:3]:
    val = float(c @ x)
    worst = 0.0
    for k, (kind, args) in enumerate(W.auxdef):
        worst = max(worst, abs(x[W.n0 + k] - rbb.mono_val(kind, args, x)))
    names = [M["names"][v] for v in W.gv]
    bins = [int(round(x[k])) for k in range(W.n0) if W.isbin[k]]
    lev = {names[k]: round(x[k], 5) for k in (PB.sidx or []) + (PB.eidx or [])}
    widths = {names[k]: h[k] - l[k] for k in range(W.n0) if h[k] - l[k] > 1e-7 and not W.isbin[k]}
    # row violations of the original rows at x
    xs = {v: x[k] for k, v in enumerate(W.gv)}
    maxv = 0.0
    for i in [i for tt in [t] for i in D["S"]["per_rows"][tt]]:
        r = M["rows"][i]
        s = 0.0
        for mono, a in r["poly"].items():
            term = float(a)
            for v in mono:
                term *= xs[v]
            s += term
        if r["lb"].upper() != "-INF":
            maxv = max(maxv, float(r["lb"]) - s)
        if r["ub"].upper() not in ("INF", "+INF"):
            maxv = max(maxv, s - float(r["ub"]))
    print(f"leaf: LP value {val:.6f}, max monomial error {worst:.2e}, max row violation {maxv:.2e}, bins {bins}, levels {lev}")
    print("   free continuous widths:", {k: float("%.3g" % v) for k, v in list(widths.items())[:12]})
for (l, h, x) in found[:1]:
    for k, (kind, args) in enumerate(W.auxdef):
        err = abs(x[W.n0 + k] - rbb.mono_val(kind, args, x))
        if err > 1e-6:
            print(kind, [(M["names"][W.gv[a]], l[a], h[a], x[a], bool(W.isbin[a])) for a in args],
                  "w", x[W.n0 + k], "[", l[W.n0 + k], h[W.n0 + k], "] err", err)
