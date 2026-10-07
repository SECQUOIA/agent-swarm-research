"""Independent check of the per-edge band-bracket plateau (Section 5
"Numerical plateau" and Section 7.4 of covering-upper-half.md), with my own
code, a cutting-plane LP, and finer grids than the author's (m <= 257).

Instance (type D, as described in Section 7.3 and in check_naive_failure):
path with n edges, s_e in [-1, 1], kappa = 10; node 0 (root) acts on s_1,
middle node t on (s_t, s_{t+1}) with kappa (s_t - s_{t+1})^2 + u_t(s_{t+1}),
leaf node n on s_n.  u_t = (|s| - 0.3)_+^2 + concave kinks
min(0, 0.5 sigma (p - s)) at node 0: p=0.65 (+), 1: -0.7 (-), 2: 0.6 (+),
4: -0.8 (-), 5: 0.75 (+) (nodes <= n), plus +0.3 sin(3s) at the root and
-0.3 sin(3s) at the leaf.

Rules (dyadic cells per edge): naive (one-edge band bracket of [L_e, U_e]
<= tol, tol = eps/n and eps/n^2), bd (Theorem 1 sliver bracket <= eps/n),
B4 (M r^2 - min w_e <= eps/n, M = 24.7).  For each cell set: LP optimum of
rho over ALL cellwise-affine splits on the cells (cells half-open, last
closed), by cutting planes with HiGHS; the reported value is f* - LP value.
"""
import sys
import time
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog, minimize_scalar

KAPPA, A, V, AMP, FREQ = 10.0, 1.0, 0.3, 0.3, 3.0
KINKS = {0: (0.65, 1), 1: (-0.7, -1), 2: (0.6, 1), 4: (-0.8, -1), 5: (0.75, 1)}
M_CURV = 2 * KAPPA + 2 * A + AMP * FREQ ** 2


def unaries(n, s):
    out = []
    for node in range(n + 1):
        f = A * np.maximum(np.abs(s) - V, 0.0) ** 2
        if node in KINKS:
            p, sg = KINKS[node]
            f = f + np.minimum(0.0, 0.5 * sg * (p - s))
        if node == 0:
            f = f + AMP * np.sin(FREQ * s)
        if node == n:
            f = f - AMP * np.sin(FREQ * s)
        out.append(f)
    return out


def minconv(s, g):
    return (KAPPA * (s[:, None] - s[None, :]) ** 2 + g[None, :]).min(axis=1)


def value_functions(n, s, u):
    U = [None] * (n + 1)
    U[n] = u[n].copy()
    for e in range(n - 1, 0, -1):
        U[e] = minconv(s, u[e] + U[e + 1])
    fstar = np.min(u[0] + U[1])
    V_ = [None] * (n + 1)
    V_[1] = u[0].copy()
    for e in range(2, n + 1):
        V_[e] = minconv(s, V_[e - 1]) + u[e - 1]
    return U, V_, fstar


def bracket(xs, up, lo):
    if len(xs) == 1:
        return lo[0] - up[0]
    f = lambda lam: np.max(lam * xs - up) + np.max(lo - lam * xs)
    sl = np.max(np.abs(np.concatenate([np.diff(up), np.diff(lo)])) / (xs[1] - xs[0])) + 1
    return minimize_scalar(f, bounds=(-2 * sl, 2 * sl), method="bounded",
                           options=dict(xatol=1e-13, maxiter=1000)).fun


def refine(m, test):
    todo, final = [(0, m - 1)], []
    while todo:
        i0, i1 = todo.pop()
        if i1 - i0 > 1 and test(i0, i1):
            mid = (i0 + i1) // 2
            todo += [(i0, mid), (mid, i1)]
        else:
            final.append((i0, i1))
    return sorted(final)


def lp_gap(n, s, u, cells, fstar, max_iter=200):
    """f* - max over PA splits on the cells of sum_t min F_t^phi, by cutting
    planes.  Variables: per edge per cell (lam, beta); per node c_t."""
    m = len(s)
    cid, off, nv = {}, {}, 0
    for e in range(1, n + 1):
        idx = np.empty(m, dtype=int)
        for k, (i0, i1) in enumerate(cells[e]):
            idx[i0:i1] = k
        idx[m - 1] = len(cells[e]) - 1
        cid[e] = idx
        off[e] = nv
        nv += 2 * len(cells[e])
    coff = nv
    nv += n + 1
    rows = []   # each: (node, i, j) meaning point (s_i[, s_j])

    def row_entries(node, i, j):
        """coefficients of c_node - F^phi_node(point) <= F_node(point)."""
        cols, vals = [coff + node], [1.0]
        if node == 0:           # F0 + phi_1(s_1 = i)
            k = cid[1][i]
            cols += [off[1] + 2 * k, off[1] + 2 * k + 1]; vals += [-s[i], -1.0]
            rhs = u[0][i]
        elif node == n:         # Fn - phi_n(s_n = i)
            k = cid[n][i]
            cols += [off[n] + 2 * k, off[n] + 2 * k + 1]; vals += [s[i], 1.0]
            rhs = u[n][i]
        else:                   # mid: + phi_{t+1}(j) - phi_t(i)
            t = node
            k1 = cid[t + 1][j]
            k0 = cid[t][i]
            cols += [off[t + 1] + 2 * k1, off[t + 1] + 2 * k1 + 1,
                     off[t] + 2 * k0, off[t] + 2 * k0 + 1]
            vals += [-s[j], -1.0, s[i], 1.0]
            rhs = KAPPA * (s[i] - s[j]) ** 2 + u[t][j]
        return cols, vals, rhs

    active = set()
    for i in range(m):
        active.add((0, i, 0))
        active.add((n, i, 0))
    for t in range(1, n):
        for i in range(0, m, 4):
            for dj in (-1, 0, 1):
                j = min(m - 1, max(0, i + dj))
                active.add((t, i, j))
    cost = np.zeros(nv)
    cost[coff:] = -1.0
    bounds = [(-60, 60)] * coff + [(None, None)] * (n + 1)
    for e in range(1, n + 1):
        bounds[off[e] + 1] = (0.0, 0.0)    # gauge: constants telescope
    for it in range(max_iter):
        R, C, Vv, b = [], [], [], []
        for r, key in enumerate(sorted(active)):
            cols, vals, rhs = row_entries(*key)
            R += [r] * len(cols); C += cols; Vv += vals; b.append(rhs)
        Am = sp.csr_matrix((Vv, (R, C)), shape=(len(b), nv))
        res = linprog(cost, A_ub=Am, b_ub=np.array(b), bounds=bounds,
                      method="highs")
        if res.status != 0:
            raise RuntimeError(res.message)
        x = res.x
        phi = [None]
        for e in range(1, n + 1):
            lam = x[off[e]:off[e] + 2 * len(cells[e]):2][cid[e]]
            bet = x[off[e] + 1:off[e] + 2 * len(cells[e]):2][cid[e]]
            phi.append(lam * s + bet)
        # true bag minima under this phi
        true = [np.min(u[0] + phi[1])]
        added = 0
        for t in range(1, n):
            T = (KAPPA * (s[:, None] - s[None, :]) ** 2 + u[t][None, :]
                 + phi[t + 1][None, :] - phi[t][:, None])
            true.append(T.min())
            viol = T < x[coff + t] - 1e-10
            if viol.any():
                flat = np.argsort(T, axis=None)[:40]
                for f in flat:
                    i, j = divmod(int(f), m)
                    if T[i, j] < x[coff + t] - 1e-10 and (t, i, j) not in active:
                        active.add((t, i, j)); added += 1
        true.append(np.min(u[n] - phi[n]))
        rho_true = sum(true)
        if added == 0:
            return fstar - rho_true, it + 1
    return fstar - rho_true, max_iter


def main():
    ms = [int(a) for a in sys.argv[1:]] or [257]
    print(f"M = {M_CURV:.2f}")
    for m in ms:
        s = np.linspace(-1, 1, m)
        ns = [4, 6, 8] if m <= 257 else [6, 8]
        for n in ns:
            u = unaries(n, s)
            U, Vf, fstar = value_functions(n, s, u)
            data = {}
            for e in range(1, n + 1):
                L = fstar - Vf[e]
                w = U[e] - L
                th = (2 * (n - e) + 1) / (2 * n)
                psi = U[e] - th * w
                data[e] = dict(U=U[e], L=L, w=w, up=psi + w / (2 * n),
                               lo=psi - w / (2 * n))
            for eps in [1e-2, 1e-3]:
                line = f"m={m} n={n} eps={eps:g}:"
                rules = [("naive", eps / n), ("naive/n", eps / n ** 2)]
                if m <= 257:
                    rules += [("bd", eps / n), ("B4", eps / n)]
                for name, tol in rules:
                    cells = {}
                    for e in range(1, n + 1):
                        d = data[e]
                        if name.startswith("naive"):
                            test = lambda i0, i1, d=d, tol=tol: bracket(
                                s[i0:i1 + 1], d["U"][i0:i1 + 1], d["L"][i0:i1 + 1]) > tol
                        elif name == "bd":
                            test = lambda i0, i1, d=d, tol=tol: bracket(
                                s[i0:i1 + 1], d["up"][i0:i1 + 1], d["lo"][i0:i1 + 1]) > tol
                        else:
                            test = lambda i0, i1, d=d, tol=tol: (
                                M_CURV * ((s[i1] - s[i0]) / 2) ** 2
                                - d["w"][i0:i1 + 1].min() > tol)
                        cells[e] = refine(m, test)
                    t0 = time.time()
                    g, its = lp_gap(n, s, u, cells, fstar)
                    tot = sum(len(c) for c in cells.values())
                    line += (f"  {name}: {tot} cells, LP gap {g:.3e}"
                             f"{' >eps' if g > eps * (1 + 1e-9) else ''}"
                             f" ({its} rounds, {time.time() - t0:.0f}s);")
                print(line)
                sys.stdout.flush()


if __name__ == "__main__":
    main()
