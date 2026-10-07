"""Exact-law predictor of static-order B&B tree sizes (Section 7.3).
Replaces every node bound by its first-order value from Theorem 1.3,
    pb(d, Wr) = f(x^Wr) * (1 - (N - d)/(2M)),
(the free coordinates absorb the fraction (N-d)/(2M) of the residual
v = w + 2 B_Wr 1), prunes when pb >= f(x*) = W, and counts the nodes of the
static-order tree.  Compared with the real static-order trees of
exp_trees.py on the same seeds.
Usage (from data/): python3 ../code/predict_trees.py trees_b1.jsonl [trees_b1_256.jsonl ...]
"""
import sys, json, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from core import instance
from exp_trees import rho_of


def predicted_static(B, w, cap=10**6):
    N = B.shape[1]; M = B.shape[0]
    W = float(w @ w)
    Gm = B.T @ B
    zeta = B.T @ w
    # iterative DFS over (d, current f-value, list of wrong indices)
    count = 0
    stack = [(0, W, ())]
    while stack:
        d, fW, Wr = stack.pop()
        count += 1
        if count > cap:
            return count, False
        pb = fW * (1 - (N - d) / (2.0 * M))
        if pb >= W * (1 - 1e-12) or d == N:
            continue
        # children: fix coordinate d correctly (same f) or wrongly
        stack.append((d + 1, fW, Wr))
        # f(x^{Wr + d}) - f(x^Wr) = 4 zeta_d + 4 G_dd + 8 sum_{j in Wr} G_dj
        inc = 4 * zeta[d] + 4 * Gm[d, d] + 8 * sum(Gm[d, j] for j in Wr)
        stack.append((d + 1, fW + inc, Wr + (d,)))
    return count, True


if __name__ == "__main__":
    rows = []
    for fn in sys.argv[1:]:
        rows += [json.loads(l) for l in open(fn)]
    seen = set()
    out = []
    for r in rows:
        if r["rule"] != "static" or not r["done"] or not r["xstar_opt"]:
            continue
        key = (r["N"], r["beta"], r["tag"], r["seed"])
        if key in seen:
            continue
        seen.add(key)
        N = r["N"]; M = int(round(r["beta"] * N))
        A, y, xs, B, w = instance(N, M, rho_of(r["tag"], N), r["seed"])
        pc, ok = predicted_static(B, w)
        out.append((N, r["beta"], r["tag"], r["seed"], r["nodes"], pc if ok else None))
    import collections
    g = collections.defaultdict(list)
    for o in out:
        g[(o[1], o[0], o[2])].append(o)
    print("| beta | N | rho tag | runs | real static nodes (geo. mean) | predicted (geo. mean) | median ratio real/pred |")
    print("|---:|---:|---|---:|---:|---:|---:|")
    for k in sorted(g):
        L = [o for o in g[k] if o[5] is not None]
        if not L:
            continue
        real = np.array([o[4] for o in L], float); pred = np.array([o[5] for o in L], float)
        print("| %g | %d | %s | %d | %.0f | %.0f | %.2f |" % (k[0], k[1], k[2], len(L), np.exp(np.mean(np.log(real))), np.exp(np.mean(np.log(pred))), np.median(real / pred)))
