"""Validity checks of the tree dynamic program in tree_gr.py (adaptive-matching.md, Section 8.4).

  python3 check_tree_dp.py

(1) The nested-bisection solver against a 801 x 801 grid minimum on 200 random sub-boxes
    (the bisection value must not exceed the grid minimum).
(2) For m = 7, 15 (random c, b = 0.55), nine GR stages with theta = 1/8, R = 4: l_r <= f*, and the
    unrelaxed value of the minimizing configuration (bag functions at its copies plus slope terms)
    is >= l_r (it exceeds l_r by the relaxation errors at the copies). This alone is a weak test.
(3) Added after review: for the same stages, the relaxed value Phi(c) of the reconstructed minimizing
    configuration (relaxed bag functions on its leaves at its copies plus slope terms, Lemma 1.5 of the
    decomposition note), recomputed from scratch, equals l_r up to rounding, and the configuration
    constraints hold: each copy lies in its leaf, the separator coordinate of each non-root copy lies
    in its cell, and that cell meets the parent leaf's projection on the separator (closed intervals).
"""
import sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import tree_gr as TG
rng = np.random.default_rng(3)
b, kappa = 0.55, 0.1
# 1) solver vs brute force on random sub-boxes
worst = 0
for trial in range(200):
    l1, l2 = rng.uniform(-1, 0.5, 2); w = rng.uniform(0.01, 0.5)
    u1, u2 = l1 + w, l2 + w
    L1 = rng.uniform(l1, u1); U1 = min(u1, L1 + rng.uniform(0, w))
    lin1, lin2 = rng.normal(0, 0.3, 2); root = bool(rng.integers(2))
    v, z1, z2 = TG.solve(*[np.array([q]) for q in (l1, u1, l2, u2, L1, U1, lin1, lin2)], b, kappa, root)
    g1 = np.linspace(L1, U1, 801)[:, None]; g2 = np.linspace(l2, u2, 801)[None, :]
    f = (TG.phi(g1, kappa) if root else 0) + lin1 * g1 + b * g1 * g2 - (abs(b) / 2) * ((g1 - l1) * (u1 - g1) + (g2 - l2) * (u2 - g2)) + TG.phi(g2, kappa) + lin2 * g2
    worst = max(worst, v[0] - f.min())
print("solver: max(bisection value - grid min) = %.2e (should be <= ~0)" % worst)
# 2) l_r <= f*; unrelaxed value of the min configuration >= l_r
# 3) relaxed value of the min configuration equals l_r; configuration constraints
rel_err, tot_viol = 0.0, 0
for m in (7, 15):
    c = rng.uniform(-0.2, 0.2, m)
    xs, fs = TG.global_min_tree(m, b, kappa, c)
    T = TG.TreeDecomp(m); P = TG.TreePartition(m)
    xprev = np.zeros(m)
    for j in range(9):
        lam = TG.slopes(xprev, b)
        D = TG.dp_min(T, P, lam, b, kappa, c)
        # (2) unrelaxed bag functions at the copies + slope terms (>= l_r; a weak test)
        z = D["z"]
        phi_exact = 0.0
        for v in range(1, m):
            z1, z2 = z[v]
            a = b * z1 * z2 + TG.phi(z2, kappa) + c[v] * z2 + ((TG.phi(z1, kappa) + c[0] * z1) if v == 1 else 0)
            phi_exact += a
            if v >= 2:
                pv = T.parent[v]
                parent_copy = z[pv][0] if v == 2 else z[pv][1]
                phi_exact += lam[v] * (parent_copy - z1)
        # (3) relaxed value of the configuration, from its leaves, and its constraints
        phi_rel = 0.0
        viol = 0
        for v in range(1, m):
            Lv = P.leaves[v]
            q = D["leaf"][v]
            l1, u1, l2, u2 = (Lv[key][q] for key in ("l1", "u1", "l2", "u2"))
            z1, z2 = z[v]
            viol += int(not (l1 <= z1 <= u1 and l2 <= z2 <= u2))
            rel = (b * z1 * z2 - (abs(b) / 2) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2))
                   + TG.phi(z2, kappa) + c[v] * z2 + ((TG.phi(z1, kappa) + c[0] * z1) if v == 1 else 0))
            phi_rel += rel
            if v >= 2:
                pv = T.parent[v]
                parent_copy = z[pv][0] if v == 2 else z[pv][1]
                phi_rel += lam[v] * (parent_copy - z1)
                C = P.cells[v]
                d = D["cell"][v]
                lo, hi = C["lo"][d], C["hi"][d]
                Lp = P.leaves[pv]
                qp = D["leaf"][pv]
                plo, phi_ = ((Lp["l1"][qp], Lp["u1"][qp]) if v == 2 else (Lp["l2"][qp], Lp["u2"][qp]))
                viol += int(not (lo <= z1 <= hi)) + int(not (lo <= phi_ and plo <= hi))
        rel_err = max(rel_err, abs(phi_rel - D["lr"]))
        tot_viol += viol
        print("m=%d j=%d lr=% .6e  f*=% .6e  lr<=f*: %s  Phi_unrelaxed(min conf)-lr=%.2e (>=0)  "
              "|Phi_relaxed(min conf)-lr|=%.1e  constraint violations=%d" % (
                  m, j, D["lr"], fs, D["lr"] <= fs + 1e-12, phi_exact - D["lr"], abs(phi_rel - D["lr"]), viol))
        TG.refine(T, P, z, 2.0 * 2.0 ** (-j) / 2, 2.0 * 2.0 ** (-j), 1 / 8, 4)
        xprev = D["x"]
print("check (3): max |Phi_relaxed(min conf) - l_r| = %.1e over all stages; constraint violations = %d" % (
    rel_err, tot_viol))
