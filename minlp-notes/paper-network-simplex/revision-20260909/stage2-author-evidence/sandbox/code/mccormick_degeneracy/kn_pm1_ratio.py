"""Exact worst ratio  sum|a| / (mu+ - mu-)  over all ±1 weightings of K_n (this equals the
McCormick/hull gap ratio at x = (1/2,...,1/2) by Boland et al. Lemma 1 and Lemma 3.9 of
Luedtke et al.).  Exhaustive for n <= 7."""
import numpy as np, itertools, math, sys
for n in range(3, 8):
    edges = list(itertools.combinations(range(n), 2)); m = len(edges)
    # cut incidence matrix: rows = cuts (subsets S containing vertex 0 to halve), cols = edges
    cuts = []
    for mask in range(1 << (n - 1)):
        s = [1] + [(mask >> i) & 1 for i in range(n - 1)]
        cuts.append([1 if s[i] != s[j] else 0 for (i, j) in edges])
    Cm = np.array(cuts, dtype=np.int8)                       # 2^(n-1) x m
    best = 0.0; best_w = None
    # enumerate sign patterns in blocks
    B = 1 << 16
    for start in range(0, 1 << m, B):
        idx = np.arange(start, min(start + B, 1 << m), dtype=np.int64)
        W = ((idx[:, None] >> np.arange(m)) & 1).astype(np.int8) * 2 - 1   # block x m, entries ±1
        cutw = W.astype(np.int32) @ Cm.T.astype(np.int32)                  # block x cuts
        rng = cutw.max(axis=1) - cutw.min(axis=1)
        rng = np.maximum(rng, 1)
        r = m / rng
        k = int(np.argmax(r))
        if r[k] > best:
            best = float(r[k]); best_w = W[k].copy()
    print(f"K_{n}: edges={m} degeneracy={n-1} worst ratio={best:.4f} ratio/sqrt(d)={best/math.sqrt(n-1):.4f} weights={best_w.tolist()}")
    sys.stdout.flush()
