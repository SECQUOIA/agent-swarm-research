"""SCIP-evaluation counts (new vs cert3) and slope statistics, for comparison
with the note's Sections 5.2 and 6.5 (own code; pickles via stub).

usage: python3 scip_slope_stats.py certB.pkl.gz state0.pkl.gz certB_cert.pkl.gz
"""
import sys

import numpy as np

import load_cs


def flat(d):
    return {(k, sk): e for k, v in d["evals"].items() for sk, e in v.items()}


b, a = flat(load_cs.load(sys.argv[1])), flat(load_cs.load(sys.argv[2]))
new = {k: e for k, e in b.items() if k not in a}
over = sum(1 for k in a if k in b and b[k].get("time") != a[k].get("time"))
t = np.array([e["time"] for e in new.values()])
print(f"SCIP evaluations: cert3 {len(a)}, new {len(new)}, cert3 entries overwritten {over}; new CPU {t.sum():.0f}s, "
      f"median {np.median(t):.2f}s, status timelimit {sum(e['status'] == 'timelimit' for e in new.values())}, "
      f"infeasible {sum(e['status'] == 'infeasible' for e in new.values())}")
d = load_cs.load(sys.argv[3])
for l in range(5):
    L = np.array([d["lam"][l][c] for c in d["leaves"][l]])
    B = np.array(d["base"][l])
    lo = np.array([d["cells"][l][c]["lo"] for c in d["leaves"][l]])
    hi = np.array([d["cells"][l][c]["hi"] for c in d["leaves"][l]])
    w = hi - lo
    D = np.abs(L - B)
    print(f"link {l}: wave-2 slope {np.round(B, 3).tolist()}; |slope - wave2| median {np.round(np.median(D, 0), 2).tolist()} "
          f"max {np.round(D.max(0), 2).tolist()}; ranges {[(round(L[:, k].min(), 1), round(L[:, k].max(), 1)) for k in range(3)]}; "
          f"leaves spanning tank 1 [2,5]: {(w[:, 0] >= 3).sum()} (of these with tank-2 width >= 0.83: "
          f"{((w[:, 0] >= 3) & (w[:, 1] >= 0.83)).sum()}); leaves with the wave-2 slope: {(D.max(1) == 0).sum()}")
