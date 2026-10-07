"""Comparison harness: runs the AUTHORS' per-box bound (ann_fast.FastModel.fbound) as a black box
on the verifier's boxes, and checks the authors' rigorous tanh against mpmath.  The verifier's own
bounds come from annv.py; this file only collects the authors' numbers for comparison.

Run with PYTHONDONTWRITEBYTECODE=1 so nothing is written under open-instances-wave3/.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import json
import os
import sys
from fractions import Fraction as Fr

import mpmath
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import annv  # noqa: E402

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann")
import ann_bb as ab  # noqa: E402
import ann_fast as af  # noqa: E402

M = af.FastModel()
N = M.D["names"]
idx = {n: j for j, n in enumerate(N)}
# the multipliers of the authors' log, built exactly as in their main()
M.lag = [(idx["x647"], Fr(58.509053436320386), M.cb[idx["x647"]][0], 1),
         (idx["x772"], Fr(20891.433722402617), M.cb[idx["x772"]][0], 1)]
print("authors' lag:", [(N[j], float(l), b, s) for j, l, b, s in M.lag])

if len(sys.argv) > 1 and sys.argv[1] == "boxes2":
    rows = json.load(open(os.path.join(HERE, "boxes2_verifier.json")))
    lo = np.array([r["lo"] for r in rows]); hi = np.array([r["hi"] for r in rows])
    alb = np.concatenate([M.fbound(lo[k:k + 256], hi[k:k + 256])["lb"] for k in range(0, len(rows), 256)])
    fm = np.array([r["sampled_min"] for r in rows]); vlb = np.array([r["lb"] for r in rows])
    d = alb - fm
    print(f"authors on {len(rows)} boxes (each contains a feasible point): infinite lb {int(np.sum(~np.isfinite(alb)))} (must be 0); "
          f"max(authors lb - best feasible f in box) = {np.max(d):.3e}; "
          f"authors lb > verifier lb + 1e-6 on {int(np.sum(alb > vlb + 1e-6))} boxes; "
          f"max(authors lb - verifier lb) = {np.max(alb - vlb):.3e}; median(verifier - authors) = {np.median(vlb - alb):.3e}")
    k = int(np.argmax(d))
    print("  closest box: authors lb", alb[k], "verifier lb", vlb[k], "best feasible f", fm[k], "widths", (hi[k] - lo[k]).tolist())
    json.dump([float(a) for a in alb], open(os.path.join(HERE, "boxes2_authors.json"), "w"))
    sys.exit(0)

D = annv.decode()
boxes, ustar = annv.make_boxes(D, np.random.default_rng(20260930))
lo = np.array([b[1] for b in boxes])
hi = np.array([b[2] for b in boxes])
R = M.fbound(lo, hi)
out = []
for (name, a, b), lb in zip(boxes, R["lb"]):
    print(f"{name:14s} authors lb {lb!r}")
    out.append(dict(box=name, authors_lb=float(lb)))
json.dump(out, open(os.path.join(HERE, "boxes_authors.json"), "w"), indent=1)

# rigorous tanh of the authors vs mpmath (60 digits)
rng = np.random.default_rng(3)
z = np.concatenate([rng.normal(0, 3, 20000), rng.normal(0, 1e-6, 2000), rng.uniform(-400, 400, 2000),
                    np.array([0.0, 1e-300, -1e-300, 5e-324, 19.0, 19.5, 20.0, 25.0, 299.999, 300.0, 301.0, -300.0, 1e5])])
T = ab.tanh_pt(z)
bad = 0
with mpmath.workdps(60):
    for zi, l, h in zip(z, T.lo, T.hi):
        t = mpmath.tanh(mpmath.mpf(float(zi)))
        if not (mpmath.mpf(float(l)) <= t <= mpmath.mpf(float(h))):
            bad += 1
            print("tanh enclosure fails at", zi, l, h, t)
print(f"authors' tanh_pt: {len(z)} points, failures {bad}, max width {np.max(T.hi - T.lo):.3e}")
