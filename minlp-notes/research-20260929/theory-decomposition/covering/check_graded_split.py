"""Checks of Theorem 1 (graded joint exact split and the sliver bound) on
random finite trees and paths with one-dimensional separators.

For each random instance:
  (a) the per-bag deficits with the DP split as reference sum to the gap;
  (b) the graded split psi (theta_t = (2 E_t + 1)/(2n)) is exact;
  (c) gap(psi + r) <= sum_e [max(r_e - w_e/2n) + max(-r_e - w_e/2n)] for
      random perturbations r of several scales, and the ratio gap/bound;
  (d) the one-edge case (n = 1) is an equality (band identity);
  (e) reversing the grading on paths (theta increasing towards the leaf)
      is not exact in general;
  (f) the per-edge discount 1/(2n) cannot be raised to a constant: with
      discount c*w_e on every edge the inequality fails for some r;
  (g) Theorem 1' with random bag errors; (h) Lemma 0 by enumeration;
  (i) the reversed DP split L is not exact on trees with branching.

Floating point; exact minima over finite grids.
"""
import sys
import numpy as np
from tree_lib import (Tree, graded_split, graded_theta, sliver_bound,
                      random_tree, random_tables)


def one_instance(rng, n_nodes, maxch, m, kind):
    parent = random_tree(n_nodes, maxch, rng)
    tables = random_tables(parent, m, rng, kind=kind)
    tree = Tree(parent, tables)
    U, V, fstar = tree.value_functions()
    w = [None] + [U[t] + V[t] - fstar for t in range(1, tree.N)]
    return tree, U, V, fstar, w


def main():
    rng = np.random.default_rng(20260930)
    tol = 1e-9
    stats = dict(inst=0, ident_err=0.0, exact_err=0.0, viol=0, ratio_max=0.0,
                 checks=0, n1_eq_err=0.0, rev_nonexact=0, rev_total=0,
                 wmin_err=0.0)
    ratios = []
    for trial in range(400):
        n_nodes = int(rng.integers(2, 7))
        maxch = 1 if trial % 2 == 0 else 2          # paths and trees
        m = int(rng.integers(4, 8)) if maxch == 2 else int(rng.integers(5, 12))
        kind = "uniform" if trial % 4 < 2 else "smooth"
        tree, U, V, fstar, w = one_instance(rng, n_nodes, maxch, m, kind)
        stats["inst"] += 1
        n = tree.n_edges
        # pinch sets exist: min_s w_e = 0 on every edge
        for t in range(1, tree.N):
            stats["wmin_err"] = max(stats["wmin_err"], abs(w[t].min()))
        psi = graded_split(tree, U, V, fstar)
        gap_psi = fstar - tree.rho(psi)
        stats["exact_err"] = max(stats["exact_err"], abs(gap_psi))
        for scale in [0.01, 0.1, 0.3, 1.0, 3.0]:
            for rep in range(5):
                r = [None] + [scale * rng.normal(size=tree.F[t].shape[0])
                              for t in range(1, tree.N)]
                # structured perturbations: proportional to w, or cellwise
                if rep == 3:
                    r = [None] + [scale * rng.uniform(-1, 1) * w[t]
                                  for t in range(1, tree.N)]
                if rep == 4:
                    r = [None] + [np.repeat(scale * rng.normal(size=2),
                                            [len(w[t]) // 2,
                                             len(w[t]) - len(w[t]) // 2])
                                  for t in range(1, tree.N)]
                phi = [None] + [psi[t] + r[t] for t in range(1, tree.N)]
                gap = fstar - tree.rho(phi)
                defs = tree.bag_deficits(phi, U, fstar)
                stats["ident_err"] = max(stats["ident_err"],
                                         abs(sum(defs) - gap))
                b = sliver_bound(tree, r, w)
                stats["checks"] += 1
                if gap > b + tol:
                    stats["viol"] += 1
                if b > 1e-6:
                    ratios.append(gap / b)
                if n == 1:
                    stats["n1_eq_err"] = max(stats["n1_eq_err"], abs(gap - b))
        # (e) reversed grading on paths
        if maxch == 1 and n >= 2:
            th = graded_theta(tree)
            rev = [None] + [1 - th[t] for t in range(1, tree.N)]
            psi_r = graded_split(tree, U, V, fstar, theta=rev)
            g = fstar - tree.rho(psi_r)
            stats["rev_total"] += 1
            if g > 1e-9:
                stats["rev_nonexact"] += 1
    ratios = np.array(ratios)
    print("Theorem 1 checks on random finite trees (1D separators)")
    print(f"instances: {stats['inst']} (half paths, half trees with <= 2 "
          f"children), perturbation checks: {stats['checks']}")
    print(f"max |min_s w_e| (pinch sets exist): {stats['wmin_err']:.2e}")
    print(f"(a) max |sum of bag deficits - gap|: {stats['ident_err']:.2e}")
    print(f"(b) max |gap(graded psi)|: {stats['exact_err']:.2e}")
    print(f"(c) violations of gap <= sliver bound: {stats['viol']}")
    print(f"    gap/bound over {len(ratios)} cases with bound > 1e-6: "
          f"max {ratios.max():.4f}, median {np.median(ratios):.4f}, "
          f"min {ratios.min():.4f}")
    print(f"(d) n = 1: max |gap - bound| = {stats['n1_eq_err']:.2e}")
    print(f"(e) reversed grading on paths: non-exact in "
          f"{stats['rev_nonexact']} of {stats['rev_total']}")

    # (g) Theorem 1': relaxed bags F_t - err_t, theta' = (3E+2)/(3n+1)
    # (h) Lemma 0: gap(phi) = max_x [sum_t delta_t(x_{S_t}) - m(x)]
    rng2 = np.random.default_rng(99)
    viol_g, cnt_g, err_h, cnt_h = 0, 0, 0.0, 0
    for trial in range(200):
        n_nodes = int(rng2.integers(2, 6))
        maxch = 1 if trial % 2 == 0 else 2
        m = int(rng2.integers(3, 6))
        tree, U, V, fstar, w = one_instance(rng2, n_nodes, maxch, m, "uniform")
        n = tree.n_edges
        # (h): enumerate all separator assignments x
        import itertools
        allx = list(itertools.product(range(m), repeat=n))
        def F_of(x, tables):
            tot = 0.0
            for t in range(tree.N):
                idx = []
                if t != 0:
                    idx.append(x[t - 1])
                for u in tree.children[t]:
                    idx.append(x[u - 1])
                tot += tables[t][tuple(idx)]
            return tot
        phi = [None] + [rng2.normal(size=m) for _ in range(n)]
        # reduced value functions and delta (bottom-up)
        Ured = [None] * tree.N
        delta = [None] * tree.N
        for t in tree.order:
            if t == 0:
                continue
            G = tree._add_child_terms(t, phi)
            Ured[t] = G.reshape(G.shape[0], -1).min(axis=1)
            d = Ured[t] - phi[t]
            delta[t] = d - d.min()
        gap = fstar - tree.rho(phi)
        best = max(sum(delta[t][x[t - 1]] for t in range(1, tree.N))
                   - (F_of(x, tree.F) - fstar) for x in allx)
        err_h = max(err_h, abs(gap - best))
        cnt_h += 1
        # (g)
        errs = [rng2.uniform(0, 0.5, size=tree.F[t].shape) for t in range(tree.N)]
        relaxed = [tree.F[t] - errs[t] for t in range(tree.N)]
        rtree = Tree(tree.parent, relaxed)
        # bag-projection margins W_t(z) of the ORIGINAL problem, by enumeration
        W = [np.full(tree.F[t].shape, np.inf) for t in range(tree.N)]
        for x in allx:
            mx = F_of(x, tree.F) - fstar
            for t in range(tree.N):
                idx = []
                if t != 0:
                    idx.append(x[t - 1])
                for u in tree.children[t]:
                    idx.append(x[u - 1])
                idx = tuple(idx)
                if mx < W[t][idx]:
                    W[t][idx] = mx
        D = 1.0 / (3 * n + 1)
        th = [None] + [(3 * tree.E[t] + 2) * D for t in range(1, tree.N)]
        psi = [None] + [(1 - th[t]) * U[t] + th[t] * (fstar - V[t])
                        for t in range(1, tree.N)]
        for scale in [0.0, 0.05, 0.3]:
            r = [None] + [scale * rng2.normal(size=m) for _ in range(n)]
            ph = [None] + [psi[t] + r[t] for t in range(1, tree.N)]
            g = fstar - rtree.rho(ph)
            b = sum(np.max(r[t] - D * w[t]) + np.max(-r[t] - D * w[t])
                    for t in range(1, tree.N))
            b += sum(np.max(errs[t] - D * W[t]) for t in range(tree.N))
            cnt_g += 1
            if g > b + 1e-9:
                viol_g += 1
    print(f"(g) Theorem 1' (relaxed bags): violations {viol_g} of {cnt_g}")
    print(f"(h) Lemma 0: max |gap(phi) - max_x[sum delta - m]| over {cnt_h} "
          f"instances: {err_h:.2e}")

    # (i) the reversed DP split phi_t = L_t on trees with branching
    rng3 = np.random.default_rng(5)
    cnt_i, tot_i, worst_i = 0, 0, 0.0
    for trial in range(300):
        parent = random_tree(int(rng3.integers(3, 7)), 2, rng3)
        nch = [0] * len(parent)
        for t, p in enumerate(parent):
            if p >= 0:
                nch[p] += 1
        if max(nch) < 2:
            continue
        tr = Tree(parent, random_tables(parent, 5, rng3))
        U, V, f = tr.value_functions()
        g = f - tr.rho([None] + [f - V[t] for t in range(1, tr.N)])
        tot_i += 1
        if g > 1e-9:
            cnt_i += 1
            worst_i = max(worst_i, g)
    print(f"(i) split phi = L on trees with branching: non-exact in {cnt_i} "
          f"of {tot_i} (max gap {worst_i:.3f})")

    # (f) discount c*w with c constant fails on a chain of copies.
    # Path, bag tables: root f(s1); middle bags P*(a-b)^2 (copies); leaf 0.
    print("(f) chain of copies: sliver bound with discount c*w_e instead of "
          "w_e/(2n)")
    m = 41
    s = np.linspace(-1, 1, m)
    for n in [2, 4, 8]:
        parent = [-1] + list(range(n))
        P = 1e3
        tables = [s ** 2]
        for t in range(1, n):
            tables.append(P * (s[:, None] - s[None, :]) ** 2)
        tables.append(np.zeros(m))
        tree = Tree(parent, tables)
        U, V, fstar = tree.value_functions()
        w = [None] + [U[t] + V[t] - fstar for t in range(1, tree.N)]
        psi = graded_split(tree, U, V, fstar)
        # r_e = -c w_e : each edge sits c*w_e below psi
        for c in [1.0 / (2 * n), 0.25, 0.5]:
            r = [None] + [-c * w[t] for t in range(1, tree.N)]
            phi = [None] + [psi[t] + r[t] for t in range(1, tree.N)]
            gap = fstar - tree.rho(phi)
            bound_c = sum(np.max(r[t] - c * w[t]) + np.max(-r[t] - c * w[t])
                          for t in range(1, tree.N))
            print(f"    n={n} c={c:.4f}: gap={gap:.4f}, bound with discount "
                  f"c*w = {bound_c:.4f}  -> {'holds' if gap <= bound_c + 1e-9 else 'FAILS'}")
    return 0 if stats["viol"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
