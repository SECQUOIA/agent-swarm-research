"""Pair native and hybrid records per instance and print a comparison table."""
import json, sys
from collections import defaultdict
by = defaultdict(dict)
for l in open(sys.argv[1]):
    r = json.loads(l); by[r["instance"]][r["mode"]] = r
def gap(r):
    if r.get("primal") is None or r.get("dual") is None: return float("inf")
    return abs(r["primal"] - r["dual"]) / max(1e-9, abs(r["primal"]), abs(r["dual"]))
print(f"{'instance':28} {'coll':>4} {'skip':>4} | {'native st':>10} {'time':>7} {'nodes':>8} {'gap%':>8} {'rootdual':>12} | {'hybrid st':>10} {'time':>7} {'nodes':>8} {'gap%':>8} {'rootdual':>12} {'cuts':>6}")
for name in sorted(by):
    n, h = by[name].get("native"), by[name].get("hybrid")
    if not n or not h: continue
    f = lambda r: f"{r['status'][:10]:>10} {r.get('time', 0):7.1f} {r.get('nodes', 0):8d} {min(100*gap(r), 9999):8.2f} {r.get('root_dual', float('nan')):12.5g}" if r["status"] != "error" else f"{'error':>10} {'':7} {'':8} {'':8} {'':12}"
    print(f"{name:28} {h.get('collapsed', 0):4d} {h.get('skipped', 0):4d} | {f(n)} | {f(h)} {h.get('cuts', 0):6d}")
