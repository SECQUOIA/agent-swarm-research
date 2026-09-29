"""Summarize cvp_bounds.jsonl + cvp_bounds_big.jsonl (medians per (kind, n)) and check the deterministic
consequences that must hold on every instance:
  om43 >= lb43 = N43 - M43   (deletion bound used in Theorem 3.4)
  omg_big <= 12              (proof of Proposition 3.6(c): at most 12 members of any
                              clique have phi >= 2.2 OPT)
"""
import json
import sys
import numpy as np
from collections import defaultdict

files = sys.argv[1:] or ["cvp_bounds.jsonl", "cvp_bounds_big.jsonl"]
rows = [json.loads(l) for f in files for l in open(f)]
g = defaultdict(list)
for r in rows:
    g[(r["kind"], r["n"])].append(r)
bad_del = sum(1 for r in rows if r["om43"] < r["lb43"])
bad_big = sum(1 for r in rows if r.get("omg_big", 0) > 12)
print(f"instances: {len(rows)}; violations om43 < N43-M43: {bad_del}; violations omg_big > 12: {bad_big}")
hdr = "kind   n  runs  OPT/GH2  lam1^2/GH2  N43  M43  om43  Nc   Nc/(n+1)  N2    omg   max omg_big  pred(4/3)^(n/2)  pred(3/2)^(n/2)"
print(hdr)
for (kind, n), rs in sorted(g.items()):
    med = lambda k: float(np.median([r[k] for r in rs])) if k in rs[0] else float("nan")
    mx = lambda k: max(r[k] for r in rs) if k in rs[0] else float("nan")
    print(f"{kind:5s} {n:3d} {len(rs):5d} {med('OPT'):8.3f} {med('lam1sq'):10.3f} {med('N43'):5.1f} {med('M43'):4.1f} {med('om43'):5.1f} "
          f"{med('Nc'):5.1f} {med('class_lb'):8.2f} {med('N2'):6.1f} {med('omg'):6.1f} {mx('omg_big'):8} "
          f"{(4/3)**(n/2):12.1f} {(3/2)**(n/2):14.1f}")
