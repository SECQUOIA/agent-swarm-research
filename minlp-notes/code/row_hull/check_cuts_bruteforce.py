"""Independent validity check of separated cuts on study instances: every cut returned by
RowSeparator.separate is compared with the exact minimum of  omega.gamma - pi.v  over ALL row vertices,
computed by plain enumeration of the 2^n subsets (no dynamic program, no merging).
python check_cuts_bruteforce.py out.jsonl"""
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from instances import transport, netflow, transport_fc
import rowhull.separate as sepmod
from rowhull.strengthen import cut_loop

records = []
orig = sepmod.RowSeparator.separate


def spy(self, zhat, tphat, tol=1e-6, max_iter=200):
    cut = orig(self, zhat, tphat, tol, max_iter)
    if cut is not None:
        records.append((self.row, cut))
    return cut


sepmod.RowSeparator.separate = spy


def exact_min(row, pi, omega):
    n, B, w = row.n, row.B, row.widths
    masks = np.arange(1 << n, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(n)) & 1).astype(float)
    tot, prof = bits @ w, bits @ (pi * w)
    best = np.inf
    tolB = 1e-9 * max(1.0, abs(B))
    for j in range(n):
        free = bits[:, j] == 0
        r = B - tot[free]
        ok = (r >= -tolB) & (r <= w[j] + tolB)
        rr = np.clip(r[ok], 0.0, w[j])
        val = omega[j] * row.items[j].gap(rr) - pi[j] * rr - prof[free][ok]
        if len(val):
            best = min(best, float(val.min()))
    return best


cells = [("t", 8, 12, s, c, k) for s in (0, 1) for c in ("random", "uncap") for k in ("quad", "log")] + \
        [("t", 10, 15, 3, "random", "quad"), ("t", 10, 15, 0, "random", "sqrt"),
         ("g", 40, 3, 3, "random", "quad"), ("g", 40, 3, 2, "random", "log"), ("g", 60, 3, 1, "random", "log"),
         ("f", 8, 12, 0, "random", "quad"), ("f", 8, 12, 1, "random", "log")]
with open(sys.argv[1], "w") as fh:
    for kind, m, n, s, cap, cost in cells:
        p = {"t": transport, "g": netflow, "f": transport_fc}[kind](m, n, s, cap, cost)
        records.clear()
        cut_loop(p)
        worst, bad = 0.0, 0
        for row, cut in records:
            ex = exact_min(row, cut["pi"], cut["omega"])
            scale = max(1.0, np.abs(cut["pi"]).max(), np.abs(cut["omega"]).max())
            excess = (cut["pi0"] - ex) / scale          # positive: cut constant above the true minimum
            worst = max(worst, excess)
            bad += excess > 1e-7
        rec = {"name": p.name, "cuts_checked": len(records), "invalid": int(bad), "worst_excess": worst}
        fh.write(json.dumps(rec) + "\n"); fh.flush(); print(rec, flush=True)
