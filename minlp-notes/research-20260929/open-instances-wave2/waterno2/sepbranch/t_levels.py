"""rbb bound vs node limit on p4-centred pairs (exploration)."""
import sys, json, time
import numpy as np
sys.path.insert(0, "..")
import core, terminal, evalpt, sepbranch
T = 6
D = core.setup(T, "../logs/implied_06.json")
terminal.add_terminal_row(D)
M, S = D["M"], D["S"]
x, obj = evalpt.read_sol("../data/waterno2_06.p4.sol", M["names"])
lev = [np.array([float(x[a]) for (i, a, b) in S["link"][t]]) for t in range(T - 1)]
areas = sepbranch.link_areas(D)
m = json.load(open("../logs/kkt_p4_06.json"))
lam = [[l[k] + m["mu"] * float(ar[k]) / 3600 for k in range(3)] for l, ar in zip(m["lam"], areas)]
ws = np.array([float(v) for v in sys.argv[1].split(",")])
def cell(link):
    lo, hi = core.level_box(D, link)
    return (np.maximum(lo, lev[link] - ws / 2), np.minimum(hi, lev[link] + ws / 2))
for t in [int(v) for v in sys.argv[2].split(",")]:
    PB = core.PeriodBounder(D, t)
    cin = cell(t - 1) if t > 0 else None
    cout = cell(t) if t < T - 1 else None
    for nl, ob in ((1, True), (1, False), (20, True), (100, True), (100000, True)):
        r = PB.bound(cin, cout, lam[t - 1] if t > 0 else [0] * 3, lam[t] if t < T - 1 else [0] * 3, 0.0,
                     1e9 if nl < 100000 else float(sys.argv[3].split(",")[t]) , node_limit=nl, time_limit=300, obbt=ob)
        print(t, "nodes", nl, "obbt", ob, "bound %.4f" % r["bound"], r["status"], "time %.1f" % r["time"], flush=True)
