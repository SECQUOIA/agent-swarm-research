"""Reproducibility spot check (NOT an independent check): run the earlier review's certifier
indep_cert.Certifier, unchanged and without the eg-recheck MarginCertifier wrapper, on random
leaves of every part (boxes from leaves_p<k>.npz, re-derived by own_bookkeeping.py) and confirm
that the recorded outcome (certified) is reproduced.  Also re-checks, for leaves recorded as
certified by a row bound at the leaf itself (how = 0), that the certifier's smallest row-bound
margin max_k (c_k + rmin_k) - theta* equals the recorded margin, by recomputing it here from
the certifier's public Model methods with exact Fractions."""
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "reviews", "eg-retry-review-checks"))
from indep_cert import Certifier  # noqa: E402

TH = "5.642100574331458"
n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 100
C = Certifier("eg_disc2_s", TH)
M = C.M
tot = bad = mism = nrow = 0
for p in range(8):
    z = np.load(os.path.join(HERE, f"leaves_p{p}.npz"))
    lo, hi, mg, how = z["lo"], z["hi"], z["mg"], z["how"]
    sel = np.random.default_rng(100 + p).choice(len(lo), n_per, replace=False)
    ok = C.certify_batch(lo[sel], hi[sel])
    tot += len(sel); bad += int((~ok).sum())
    # row-bound margins of how == 0 leaves
    r = sel[how[sel] == 0]
    if len(r):
        c, rr, beta, aL, aU = M.taylor(lo[r], hi[r])
        nlo, nhi = M.natural(lo[r], hi[r])
        for t, j in enumerate(r):
            dl = [Fr(a) - Fr(b) for a, b in zip(lo[j], c[t])]
            dh = [Fr(a) - Fr(b) for a, b in zip(hi[j], c[t])]
            best = None
            for k in range(24):
                cand = [Fr(nlo[t, k])] if np.isfinite(nlo[t, k]) else []
                if np.isfinite(aL[t, k]):
                    cand.append(Fr(aL[t, k]) + sum(Fr(b) * (a if b >= 0 else h) for b, a, h in zip(beta[t, k], dl, dh)))
                if cand:
                    v = M.qc[k] + max(cand) - Fr(TH)
                    best = v if best is None or v > best else best
            nrow += 1
            mism += float(best) != mg[j]
    print(f"part {p}: {len(sel)} random leaves; certified now {int(ok.sum())}; row-bound margins recomputed for "
          f"{len(r)} how=0 leaves", flush=True)
print(f"total {tot} leaves, not reproduced {bad}; row margins recomputed {nrow}, differing from recorded {mism}; stats {C.stats}")
