"""Timing of rbb on cell pairs of different widths (exploration)."""
import sys, json, time
import numpy as np
import core, period, bundle
T = 6
D = core.setup(T, "../logs/implied_06.json")
m = json.load(open("../logs/mult_06_w1_impl.json"))
lam, mu = m["lam"], m["mu"]
t = int(sys.argv[1])
s = np.array([float(v) for v in sys.argv[2].split(",")])
e = np.array([float(v) for v in sys.argv[3].split(",")])
PB = core.PeriodBounder(D, t)
for w in [float(v) for v in sys.argv[4].split(",")]:
    lo0, hi0 = core.level_box(D, t - 1)
    lo1, hi1 = core.level_box(D, t)
    cin = (np.maximum(lo0, s - w / 2), np.minimum(hi0, s + w / 2))
    cout = (np.maximum(lo1, e - w / 2), np.minimum(hi1, e + w / 2))
    # SCIP estimate (exploration only)
    box = {}
    for k, (i, a, b) in enumerate(D["S"]["link"][t - 1]):
        box[b] = (cin[0][k], cin[1][k])
    for k, (i, a, b) in enumerate(D["S"]["link"][t]):
        box[a] = (cout[0][k], cout[1][k])
    tic = time.time()
    r = period.solve_window(D, t, t + 1, lam, mu, 60, bundle.NOPROP, box)
    ts = time.time() - tic
    for obbt in (True, False):
        res = PB.bound(cin, cout, lam[t - 1], lam[t], mu, r["primal"] - 1e-4, node_limit=20000, time_limit=300, obbt=obbt)
        print(f"w={w} scip {r['status']} {r['primal']:.6f} ({ts:.1f}s)  rbb obbt={obbt} bound {res['bound']:.6f} {res['status']} nodes {res['nodes']} {res['time']:.1f}s", flush=True)
