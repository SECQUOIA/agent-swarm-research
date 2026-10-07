"""Optimal discount on the chain of copies (Proposition 1.3, added after review).

Path with n edges: root table s_1^2, middle bags P (s_t - s_{t+1})^2
(t = 1..n-1), leaf 0, on a grid of m points in [-1, 1] containing 0.
F has the unique minimizer x = 0 on the grid, so a split phi is exact iff
every bag function F_t^phi attains its minimum at the zero configuration.
This is a set of linear inequalities in phi.

A bound of the form of Theorem 1(b) with discount c w_e around an exact
split psi forces psi + r to be exact whenever |r_e| <= c w_e (all brackets
are then <= 0).  The LP below computes the largest c for which some psi
makes psi + k c a exact for every k in a given set, where
a_e = (-1)^e w_e (w_e from the grid DP):
  - k in {0, 1}:      one alternating pattern (the note's first sketch);
  - k in {0, 1, -1}:  both patterns r^A = c a and r^B = -c a.
Expected: 1/n and 1/(2n).

Part 2 checks the general inequality of Proposition 1.3 on random small
trees: with a_e = (-1)^{depth(e)} w_e, the largest c for which some psi
makes psi + c a and psi - c a exact satisfies
    1/(2n) <= c_LP <= min_{x: m(x) > 0} m(x) / (2 sum_e w_e(x_{S_e})).
(The left inequality is Theorem 1 with the graded split; the right one is
Proposition 1.3.  On trees the right one is an equality, because the DP
split of F - 2c sum_e w_e is exact; the script prints the largest
difference.)  Floating point, HiGHS.

usage: python3 check_chain_discount.py
"""
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


def chain_w(n, s, P):
    m = len(s)
    mid = P * (s[:, None] - s[None, :]) ** 2
    U = [None] * (n + 1)
    U[n] = np.zeros(m)
    for e in range(n - 1, 0, -1):          # bag e holds (s_e, s_{e+1})
        U[e] = (mid + U[e + 1][None, :]).min(axis=1)
    V = [None] * (n + 1)
    V[1] = s ** 2
    for e in range(2, n + 1):
        V[e] = (V[e - 1][:, None] + mid).min(axis=0)
    fstar = (V[1] + U[1]).min()
    w = [None] + [U[e] + V[e] - fstar for e in range(1, n + 1)]
    return mid, w, fstar


def max_discount(n, s, P, ks):
    m = len(s)
    i0 = int(np.argmin(np.abs(s)))
    assert abs(s[i0]) < 1e-14
    mid, w, fstar = chain_w(n, s, P)
    a = [None] + [(-1) ** e * w[e] for e in range(1, n + 1)]
    nv = n * m + 1                          # psi_e(s_j), then c
    ci = n * m

    def col(e, j):
        return (e - 1) * m + j

    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for k in ks:
        # root: s^2 + phi_1(s) - phi_1(0) >= 0
        for j in range(m):
            if j == i0:
                continue
            # -(phi_1(s_j) - phi_1(0) + k c (a_1(s_j) - a_1(0))) <= s_j^2
            rows += [r, r, r]
            cols += [col(1, j), col(1, i0), ci]
            vals += [-1.0, 1.0, -k * (a[1][j] - a[1][i0])]
            rhs.append(s[j] ** 2)
            r += 1
        # middle bag t: P (s_t - s_{t+1})^2 + phi_{t+1}(s_{t+1}) - phi_t(s_t)
        for t in range(1, n):
            for j in range(m):
                for l in range(m):
                    if j == i0 and l == i0:
                        continue
                    # coefficients of the psi differences (keys may repeat)
                    d = {}
                    for kk, vv in [(col(t + 1, l), 1.0), (col(t + 1, i0), -1.0),
                                   (col(t, j), -1.0), (col(t, i0), 1.0)]:
                        d[kk] = d.get(kk, 0.0) + vv
                    kc = k * ((a[t + 1][l] - a[t + 1][i0])
                              - (a[t][j] - a[t][i0]))
                    for kk, vv in d.items():
                        if vv != 0.0:
                            rows.append(r)
                            cols.append(kk)
                            vals.append(-vv)
                    rows.append(r)
                    cols.append(ci)
                    vals.append(-kc)
                    rhs.append(mid[j, l])
                    r += 1
        # leaf: -phi_n(s) + phi_n(0) >= 0
        for j in range(m):
            if j == i0:
                continue
            rows += [r, r, r]
            cols += [col(n, j), col(n, i0), ci]
            vals += [1.0, -1.0, k * (a[n][j] - a[n][i0])]
            rhs.append(0.0)
            r += 1
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, nv))
    cobj = np.zeros(nv)
    cobj[ci] = -1.0
    bounds = [(None, None)] * (n * m) + [(0, 10)]
    # fix phi_e(0) = 0 (the constraints only see differences)
    for e in range(1, n + 1):
        bounds[col(e, i0)] = (0, 0)
    res = linprog(cobj, A_ub=A, b_ub=np.array(rhs), bounds=bounds,
                  method="highs")
    assert res.status == 0, res.message
    return res.x[ci], max(np.max(np.abs(w[e] - s ** 2))
                          for e in range(1, n + 1)), fstar


def tree_lp(tree, xstar, a, ks):
    """Largest c such that some psi makes psi + k c a exact for k in ks.
    Exact iff every bag function is minimized at xstar (a global minimizer)."""
    n, N = tree.n_edges, tree.N
    m = tree.F[1].shape[0]
    nv = n * m + 1
    ci = n * m

    def col(e, j):
        return (e - 1) * m + j

    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for k in ks:
        for t in range(N):
            axes = ([t] if t != 0 else []) + list(tree.children[t])
            T = tree.F[t]
            zs = tuple(xstar[u] for u in axes) if axes else (0,)
            for z in np.ndindex(*T.shape):
                if z == zs:
                    continue
                d, kc = {}, 0.0
                for pos, u in enumerate(axes):
                    sg = -1.0 if (t != 0 and pos == 0) else 1.0
                    for jj, vv in [(z[pos], sg), (zs[pos], -sg)]:
                        d[col(u, jj)] = d.get(col(u, jj), 0.0) + vv
                    kc += sg * k * (a[u][z[pos]] - a[u][zs[pos]])
                for kk, vv in d.items():
                    if vv != 0.0:
                        rows.append(r)
                        cols.append(kk)
                        vals.append(-vv)
                rows.append(r)
                cols.append(ci)
                vals.append(-kc)
                rhs.append(T[z] - T[zs])
                r += 1
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, nv))
    cobj = np.zeros(nv)
    cobj[ci] = -1.0
    bounds = [(None, None)] * (n * m) + [(0, 10)]
    res = linprog(cobj, A_ub=A, b_ub=np.array(rhs), bounds=bounds,
                  method="highs")
    assert res.status == 0, res.message
    return res.x[ci]


def random_tree_part():
    import itertools
    from tree_lib import Tree, random_tree, random_tables
    rng = np.random.default_rng(3)
    worst_lo, worst_hi, cnt, maxdiff, cs = np.inf, np.inf, 0, 0.0, []
    for trial in range(60):
        parent = random_tree(int(rng.integers(3, 6)),
                             1 if trial % 2 == 0 else 2, rng)
        m = 4
        tree = Tree(parent, random_tables(parent, m, rng,
                                          kind="smooth" if trial % 3 else
                                          "uniform"))
        U, V, fstar = tree.value_functions()
        n, N = tree.n_edges, tree.N
        w = [None] + [U[t] + V[t] - fstar for t in range(1, N)]
        depth = [0] * N
        for t in range(1, N):
            depth[t] = depth[parent[t]] + 1
        a = [None] + [(-1) ** depth[t] * w[t] for t in range(1, N)]
        # enumerate x = (s_1, ..., s_n) (one separator variable per edge)
        best, xstar, ratio = np.inf, None, np.inf
        vals = []
        for x in itertools.product(range(m), repeat=n):
            xs = (None,) + x
            F = 0.0
            for t in range(N):
                axes = ([t] if t != 0 else []) + list(tree.children[t])
                F += tree.F[t][tuple(xs[u] for u in axes)] if axes else \
                    tree.F[t][0]
            vals.append((F, xs))
            if F < best:
                best, xstar = F, xs
        for F, xs in vals:
            mx = F - fstar
            sw = sum(w[t][xs[t]] for t in range(1, N))
            if mx > 1e-9 and sw > 1e-12:
                ratio = min(ratio, mx / (2 * sw))
        c = tree_lp(tree, xstar, a, [1, -1])
        cnt += 1
        worst_lo = min(worst_lo, c - 1 / (2 * n))
        worst_hi = min(worst_hi, ratio - c)
        maxdiff = max(maxdiff, abs(ratio - c))
        cs.append(2 * n * c)
    print(f"random trees (paths and branching, m = 4): {cnt} instances; "
          f"min (c_LP - 1/(2n)) = {worst_lo:.2e}, "
          f"min (bound - c_LP) = {worst_hi:.2e}, "
          f"max |bound - c_LP| = {maxdiff:.2e}; "
          f"2n c_LP ranges over [{min(cs):.3f}, {max(cs):.3f}]")
    return worst_lo >= -1e-7 and worst_hi >= -1e-7


def main():
    P = 1e3
    ok = True
    for m in [21, 41]:
        s = np.linspace(-1, 1, m)
        print(f"grid m = {m}, P = {P:g}")
        for n in [2, 3, 4, 6, 8]:
            c1, werr, fstar = max_discount(n, s, P, [0, 1])
            c2, _, _ = max_discount(n, s, P, [0, 1, -1])
            print(f"  n={n}: f*={fstar:.1e}, max|w_e - s^2| = {werr:.1e}; "
                  f"largest c, one pattern: {c1:.6f} (1/n = {1 / n:.6f}); "
                  f"both patterns: {c2:.6f} (1/(2n) = {1 / (2 * n):.6f})")
            ok = ok and abs(c1 - 1 / n) < 1e-7 and abs(c2 - 1 / (2 * n)) < 1e-7
    ok = random_tree_part() and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
