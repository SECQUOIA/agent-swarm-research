"""Second recheck: slopes of log(leaves) for face4d from the note's own log.

Reads research-20260929/rlct/logs/revision_sweep.jsonl and reports, over
eps in [1e-6, 1e-3]: the least-squares slope of log(leaves) against
log(1/eps), the two-endpoint slope, leaves / face lower bound, and
leaves * eps^(1/4).
Usage: python3 face4d_slopes2.py > logs/face4d_slopes2.log
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "..", "..", "rlct", "logs", "revision_sweep.jsonl")

rows = sorted((r["eps"], r["leaves"]) for r in map(json.loads, open(LOG))
              if r["instance"] == "face4d")
rows = rows[::-1]
print("eps, leaves:")
for e, L in rows:
    print(f"  {e:.3e} {L}")

sel = [(e, L) for e, L in rows if 1e-6 * 0.999 <= e <= 1e-3 * 1.001]
x = np.array([math.log(1 / e) for e, _ in sel])
y = np.array([math.log(L) for _, L in sel])
ls = np.polyfit(x, y, 1)[0]
ep = (y[-1] - y[0]) / (x[-1] - x[0])
print(f"\n[1e-6, 1e-3]: {len(sel)} points; least-squares slope {ls:.4f}; endpoint slope {ep:.4f}")

# face lower bound (3 alpha/pi^2)^(3/2) I_face, with I_face from face4d_integrals2 route B
# is not recomputed here; see face4d_integrals2.log.  Only the eps^(1/4) growth is printed.
g = [L * e ** 0.25 for e, L in rows]
print(f"leaves * eps^(1/4): {g[0]:.1f} at {rows[0][0]:.0e}, {g[-1]:.1f} at {rows[-1][0]:.0e}, "
      f"factor {g[-1] / g[0]:.1f}")
