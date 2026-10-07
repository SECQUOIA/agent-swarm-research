"""Cross-check: re-certify the stored targets of a certification run with the
plain B&B (no root OBBT, no reduced-cost tightening)."""
import os, sys, json
import period, rbb

T = int(sys.argv[1])
cert = json.load(open(sys.argv[2]))
D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
lam = [[float(v) for v in l] for l in cert["lam"]]
mu = float(cert["mu"])
for t in [int(a) for a in sys.argv[3].split(",")]:
    r = [x for x in cert["results"] if x["t0"] == t][0]
    W = rbb.Window(D, t, t + 1)
    c = W.objective(lam, mu)
    res = rbb.solve(W, c, r["target"], node_limit=400000, time_limit=1800, rc=False, obbt_vars=None)
    print(f"period {t}: target {r['target']:.6f} plain B&B -> {res['status']} bound {res['bound']:.6f} "
          f"nodes {res['nodes']} time {res['time']:.0f}s (with OBBT+rc: {r['nodes']} nodes)", flush=True)
