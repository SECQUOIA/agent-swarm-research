"""Smoke test of the two bounding codes on p4-centred pairs (periods 2 and 5):
rbb (core/tasks) certifies a target, vbb2 (crosscheck_pairs) re-certifies it;
and a negative control: vbb2 must not certify target + 0.05 above a SCIP point."""
import sys, json
import numpy as np
sys.path.insert(0, "..")
import core, terminal, evalpt, plan, tasks, crosscheck_pairs as cc
T = 6
cfg = {"T": 6, "implied": "../logs/implied_06.json", "mult": "../logs/kkt_p4_06.json"}
tasks.init(T, cfg["implied"], True)
D = tasks._W["D"]
M, S = D["M"], D["S"]
x, obj = evalpt.read_sol("../data/waterno2_06.p4.sol", M["names"])
lev = [np.array([float(x[a]) for (i, a, b) in S["link"][t]]) for t in range(T - 1)]
lam = plan.load_slopes(D, cfg)
cc._init(cfg)
w = np.array([0.5, 0.5, 0.5])
def cell(link):
    lo, hi = core.level_box(D, link)
    return [list(np.maximum(lo, lev[link] - w / 2)), list(np.minimum(hi, lev[link] + w / 2))]
for t in (2, 5):
    cin = cell(t - 1)
    cout = cell(t) if t < T - 1 else None
    lin = lam[t - 1]
    lout = lam[t] if t < T - 1 else [0.0] * 3
    _, e = tasks.scip_task(((t,), t, cin, cout, lin, lout, 0.0, 60))
    _, r = tasks.rbb_task(((t,), t, cin, cout, lin, lout, 0.0, e["est"] - 1e-4, 20000, 600))
    print("period", t, "SCIP", e["est"], "rbb", r["bound"], r["status"], r["nodes"], flush=True)
    rec = dict(r, t=t)
    _, v = cc._run((0, rec, 600))
    print("   vbb2 at rbb bound:", v.get("status"), v.get("bound"), v.get("nodes"), "%.0fs" % v["time"], flush=True)
    rec2 = dict(rec, bound=e["est"] + 0.05)
    _, v2 = cc._run((0, rec2, 300))
    print("   vbb2 at SCIP+0.05 (must not certify):", v2.get("status"), v2.get("bound"), flush=True)
