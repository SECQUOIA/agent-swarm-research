"""Chain of copies (Remark 1.2 of covering-upper-half.md).

Path: root s_1^2; middle bags P (s_t - s_{t+1})^2, t = 1..n-1; leaf 0.
Grid of q points on [-1, 1]; P = 1e3 makes the copies exact on the grid.
Then U_e = 0, L_e = -s^2, w_e = s^2 (checked).

(1) The author's check (f): graded split with r_e = -c w_e has gap
    c - 1/(2n) when c > 1/(2n) (direct evaluation).
(2) Sharpness for EVERY exact split.  A bound of the form of Theorem 1(b)
    with discount c around an exact split psi forces psi + r to be exact
    for every r with |r_e| <= c w_e (the brackets are then <= 0).  LP:
    largest c such that some psi is exact and psi + r^A, psi + r^B are exact,
    r^A_e = (-1)^e c w_e, r^B = -r^A.  The note's sketch uses one
    alternating pattern and gets c <= 1/n; with both patterns the argument
    gives c <= 1/(2n), i.e. the graded split's discount is optimal here.
Floating point, HiGHS.
"""
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


def chain(n, q, P=1e3):
    s = np.linspace(-1, 1, q)
    root = s ** 2
    mid = P * (s[:, None] - s[None, :]) ** 2
    leaf = np.zeros(q)
    return s, root, mid, leaf


def value_functions(n, s, root, mid, leaf):
    q = len(s)
    U = [None] * (n + 1)
    U[n] = leaf.copy()
    for e in range(n - 1, 0, -1):   # bag e holds (s_e, s_{e+1})
        U[e] = (mid + U[e + 1][None, :]).min(axis=1)
    fstar = (root + U[1]).min()
    V = [None] * (n + 1)
    V[1] = root.copy()
    for e in range(2, n + 1):
        V[e] = (V[e - 1][:, None] + mid).min(axis=0)
    return U, V, fstar


def rho(n, root, mid, leaf, phi):
    tot = (root + phi[1]).min()
    for t in range(1, n):
        tot += (mid + phi[t + 1][None, :] - phi[t][:, None]).min()
    tot += (leaf - phi[n]).min()
    return tot


def max_c(n, s, root, mid, leaf, w, patterns):
    """Largest c such that some psi makes psi + c*R exact for all R in
    patterns (each R a list of arrays, R[e] multiplies w_e)."""
    q = len(s)
    fstar = 0.0

    def feasible(c):
        # variables: psi_e (n*q), then per pattern (n+1) bag bounds
        npsi = n * q
        K = len(patterns)
        nv = npsi + K * (n + 1)
        rows, cols, vals, rhs = [], [], [], []
        eq_rows, eq_cols, eq_vals, eq_rhs = [], [], [], []
        r = 0
        er = 0
        for k, R in enumerate(patterns):
            off = npsi + k * (n + 1)
            rr = [None] + [c * R[e] * w[e] for e in range(1, n + 1)]
            # root: c0 <= root + psi_1 + r_1
            for i in range(q):
                rows += [r, r]; cols += [off, (0) * q + i]; vals += [1, -1]
                rhs.append(root[i] + rr[1][i]); r += 1
            for t in range(1, n):
                for i in range(q):
                    for j in range(q):
                        # c_t <= mid + psi_{t+1}(j) + r_{t+1}(j) - psi_t(i) - r_t(i)
                        rows += [r, r, r]
                        cols += [off + t, t * q + j, (t - 1) * q + i]
                        vals += [1, -1, 1]
                        rhs.append(mid[i, j] + rr[t + 1][j] - rr[t][i]); r += 1
            for i in range(q):
                rows += [r, r]; cols += [off + n, (n - 1) * q + i]; vals += [1, 1]
                rhs.append(leaf[i] - rr[n][i]); r += 1
            # sum of bag bounds >= f*
            for t in range(n + 1):
                rows.append(r); cols.append(off + t); vals.append(-1)
            rhs.append(-fstar + 1e-12); r += 1
        A = sp.csr_matrix((vals, (rows, cols)), shape=(r, nv))
        bounds = [(-10, 10)] * npsi + [(None, None)] * (K * (n + 1))
        res = linprog(np.zeros(nv), A_ub=A, b_ub=np.array(rhs),
                      bounds=bounds, method="highs")
        return res.status == 0

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid_c = (lo + hi) / 2
        if feasible(mid_c):
            lo = mid_c
        else:
            hi = mid_c
    return lo


def main():
    q = 21
    print("Chain of copies: root s1^2, middle P(s_t - s_{t+1})^2 (P = 1e3), "
          f"leaf 0; grid q = {q}")
    for n in [2, 3, 4, 6, 8]:
        s, root, mid, leaf = chain(n, q)
        U, V, fstar = value_functions(n, s, root, mid, leaf)
        w = [None] + [U[e] + V[e] - fstar for e in range(1, n + 1)]
        werr = max(np.max(np.abs(w[e] - s ** 2)) for e in range(1, n + 1))
        # graded split
        psi = [None] + [U[e] - (2 * (n - e) + 1) / (2 * n) * w[e]
                        for e in range(1, n + 1)]
        line = (f"n={n}: f*={fstar:.1e}, max|w_e - s^2|={werr:.1e}, "
                f"gap(graded)={fstar - rho(n, root, mid, leaf, psi):.1e};")
        for c in [1 / (2 * n), 0.25, 0.5]:
            phi = [None] + [psi[e] - c * w[e] for e in range(1, n + 1)]
            g = fstar - rho(n, root, mid, leaf, phi)
            line += f" c={c:.4f}: gap={g:.4f} (c-1/(2n)={c - 1 / (2 * n):+.4f});"
        print(line)
        zero = [None] + [np.zeros(q)] * n
        A = [None] + [(-1.0) ** e * np.ones(q) for e in range(1, n + 1)]
        B = [None] + [-(-1.0) ** e * np.ones(q) for e in range(1, n + 1)]
        c1 = max_c(n, s, root, mid, leaf, w, [zero, A])
        c2 = max_c(n, s, root, mid, leaf, w, [zero, A, B])
        print(f"   largest c with psi, psi + c r^A exact: {c1:.5f} "
              f"(1/n = {1 / n:.5f});  with psi, psi + c r^A, psi + c r^B "
              f"exact: {c2:.5f} (1/(2n) = {1 / (2 * n):.5f})")


if __name__ == "__main__":
    main()
