"""Summarize the all-node sweep (s1007_all_*.jsonl) and the eight p = 3200 instances."""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import json, glob
import numpy as np
from sparse_s1007_audit import instance, n, p, k
d = [json.loads(l) for f in sorted(glob.glob("s1007_all_*.jsonl")) for l in open(f)]
X, y, lam, S = instance(1007)
XS = X[:, S]; r = y - XS @ np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y); a = X.T @ r
nul = np.array([j for j in range(p) if j not in set(S.tolist())]); order = nul[np.argsort(-np.abs(a[nul]))]
rank = {int(j): i + 1 for i, j in enumerate(order)}
print("seed 1007: %d forced-in nodes solved (all nulls); max certified bracket width %.2e" %
      (len(d), max(x["up"] - x["lo"] for x in d)))
print("  nodes with value < f(S*) (certified by the feasible point):",
      [(x["j"], rank[x["j"]], round(x["up"], 4)) for x in sorted(d, key=lambda x: x["up"]) if x["up"] < 0])
print("  nodes whose bracket contains 0:", [x["j"] for x in d if x["lo"] < 0 <= x["up"]])
pos = [x for x in d if x["lo"] > 0]
print("  nodes certified > f(S*) by the dual bound: %d; smallest margin %.4f (j=%d, rank %d)" %
      (len(pos), min(x["lo"] for x in pos), min(pos, key=lambda x: x["lo"])["j"], rank[min(pos, key=lambda x: x["lo"])["j"]]))
mx = max(d, key=lambda x: x["up"])
print("  largest node value - f(S*): %.4f (j=%d, rank %d); price m0^2/lam = %.4f; smallest recovered fraction %.3f"
      % (mx["up"], mx["j"], rank[mx["j"]], (np.min(np.abs(a[S]))) ** 2 / lam, 1 - mx["up"] / (np.min(np.abs(a[S])) ** 2 / lam)))
print("  rank-2 null j=%d margin [%.5f, %.5f]" % (order[1], [x for x in d if x["j"] == order[1]][0]["lo"],
                                                  [x for x in d if x["j"] == order[1]][0]["up"]))
print("  nodes with value above 2.75: %d" % sum(x["up"] > 2.75 for x in d))
print("eight p = 3200 instances (seeds 1000-1007): violators |a_l| > m0, sat-gain sum (|a|-m0)_+^2/n, tau^2, price")
for s in range(1000, 1008):
    X, y, lam, S = instance(s)
    XS = X[:, S]; r = y - XS @ np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y); a = X.T @ r
    m0 = np.min(np.abs(a[S])); nl = np.ones(p, bool); nl[S] = False
    print("  seed %d: f(S*) = %.4f, violators %3d, sat-gain %.1f, tau^2 %.3f, price %.2f" %
          (s, float(y @ r), int(np.sum(np.abs(a[nl]) > m0)), float(np.sum(np.maximum(np.abs(a[nl]) - m0, 0) ** 2) / n),
           (m0 / np.linalg.norm(r)) ** 2, m0 ** 2 / lam))
