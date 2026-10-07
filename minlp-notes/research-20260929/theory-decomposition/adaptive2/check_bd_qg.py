"""Rule bd of covering-upper-half.md (Corollary 3.2) under quadratic growth, exact-bag model
(adaptive-matching.md, Proposition 6).

Quadratic path in the exact-bag model of [K]/covering note: separators s_1..s_n in [-1,1],
root bag s_1^2, bag t (1 <= t <= n-1): b s_t s_{t+1} + s_{t+1}^2, leaf bag n: 0. So
F = sum_t s_t^2 + b sum_t s_t s_{t+1}, x* = 0, f* = 0, (QG) with c_g = 1 - |b|.
Value functions are exact quadratics (Riccati): U_t = u_t s^2, V_t = v_t s^2, L_t = -v_t s^2,
w_t = q_t s^2 (q_t = u_t + v_t), graded split psi_t = U_t - theta_t w_t = p_t s^2 with
theta_t = (2(n-t)+1)/(2n).

(1) bd: refine a dyadic cell D of [-1,1] while its Theorem 1(c) bracket
      g(D) = inf_affine l [ sup_D (l - psi - w/(2n)) + sup_D (psi - w/(2n) - l) ]
    exceeds eps/n. The bracket is computed exactly (convex in the slope; inner maxima of quadratics
    in closed form; golden-section search on the slope, 200 iterations). The lower bound of
    Proposition 6 for edges t <= (n+1)/2 with K_t = (n|p_t| - q_t/2)/q_t > 11 is
    floor((1/2) log2(q_t/eps)) sqrt(K_t - 2)/12 cells; the column prints min over those edges of
    (cells used by bd)/(bound) and the smallest bound.
(2) Comparison: a split built bottom-up from chords of the reduced value functions (each bag is
    affine in its parent separator, so the reduced value function is concave and its chord makes the
    bag minimum exactly 0), on cells graded at ratio 1/4 with core h around x* = 0 on every edge.
    (A single cell on edges 2..n does not work: the chord sagittas at x* add up along the chain,
    Lemma 0 of the covering note at x = 0; gap about 0.2 (n-1) in a first run, not kept.) The split gap f* - rho(phi) is computed exactly (bag minima: concave minus affine on
    each cell, so at cell endpoints; root: convex quadratic per cell), up to floating point.
"""
import sys
import numpy as np

B = 0.8


def riccati(n, b):
    u = np.zeros(n + 2)
    v = np.zeros(n + 2)
    u[n] = 0.0
    for t in range(n - 1, 0, -1):
        u[t] = -b * b / (4 * (1 + u[t + 1]))
    v[1] = 1.0
    for t in range(1, n):
        v[t + 1] = 1 - b * b / (4 * v[t])
    return u, v


def max_quad(a, m, lo, hi):
    """max over s in [lo,hi] of m s - a s^2 (vectorized over m)."""
    cand = [m * lo - a * lo * lo, m * hi - a * hi * hi]
    if a > 0:
        s = np.clip(m / (2 * a), lo, hi)
        cand.append(m * s - a * s * s)
    return np.max(np.stack(cand), axis=0)


def bracket(p, q, n, lo, hi):
    """g(D) for psi = p s^2, w = q s^2 on D = [lo, hi]."""
    up, dn = p + q / (2 * n), p - q / (2 * n)     # psi + w/2n, psi - w/2n

    def G(m):
        # sup (m s + c - up s^2) + sup (dn s^2 - m s - c), c cancels
        return max_quad(up, m, lo, hi) + max_quad(-dn, -m, lo, hi)
    a, c = -10.0, 10.0
    gr = (np.sqrt(5) - 1) / 2
    x1, x2 = c - gr * (c - a), a + gr * (c - a)
    f1, f2 = G(x1), G(x2)
    for _ in range(200):
        if f1 < f2:
            c, x2, f2 = x2, x1, f1
            x1 = c - gr * (c - a)
            f1 = G(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + gr * (c - a)
            f2 = G(x2)
    return min(f1, f2)


def bd_cells(p, q, n, eps):
    tol = eps / n
    stack = [(-1.0, 1.0)]
    final = []
    while stack:
        lo, hi = stack.pop()
        if bracket(p, q, n, lo, hi) > tol and hi - lo > 1e-12:
            mid = 0.5 * (lo + hi)
            stack += [(lo, mid), (mid, hi)]
        else:
            final.append((lo, hi))
    return sorted(final)


def graded_cells(h, theta):
    stack = [(-1.0, 1.0)]
    final = []
    while stack:
        lo, hi = stack.pop()
        d = max(lo, -hi, 0.0)
        if hi - lo > max(h, theta * d) * (1 + 1e-12):
            mid = 0.5 * (lo + hi)
            stack += [(lo, mid), (mid, hi)]
        else:
            final.append((lo, hi))
    return sorted(final)


def g_reduced(b, lo2, hi2, m2, c2, s):
    """U^phi_t(s) = min_y [b s y + y^2 + phi_{t+1}(y)] for cellwise affine phi_{t+1} (exact)."""
    lin = b * s[:, None] + m2[None, :]
    y = np.clip(-lin / 2, lo2[None, :], hi2[None, :])
    return np.min(y * y + lin * y + c2[None, :], axis=1)


def split_gap(n, b, cells_per_edge):
    """Exact-bag split built bottom-up: phi_n = U_n = 0; for t = n-1..1, phi_t on each of its cells is
    the chord of the reduced value function U^phi_t (concave in s, since bag t is affine in s_t).
    Returns (f* - rho(phi), largest |non-root bag minimum|); all bag minima are computed exactly
    (concave minus affine on each cell: minimum at cell endpoints; root: convex quadratic per cell)."""
    lo = np.array([c[0] for c in cells_per_edge[n]]); hi = np.array([c[1] for c in cells_per_edge[n]])
    pieces = {n: (lo, hi, np.zeros(len(lo)), np.zeros(len(lo)))}
    worst_bag = 0.0
    for t in range(n - 1, 0, -1):
        lo2, hi2, m2, c2 = pieces[t + 1]
        lo = np.array([c[0] for c in cells_per_edge[t]]); hi = np.array([c[1] for c in cells_per_edge[t]])
        glo, ghi = g_reduced(b, lo2, hi2, m2, c2, lo), g_reduced(b, lo2, hi2, m2, c2, hi)
        m = (ghi - glo) / (hi - lo)
        c = glo - m * lo
        pieces[t] = (lo, hi, m, c)
        # bag t minimum: min over cells of min over endpoints of g - phi_t
        bag = float(np.min(np.minimum(glo - (m * lo + c), ghi - (m * hi + c))))
        worst_bag = max(worst_bag, abs(bag))
    lo, hi, m, c = pieces[1]
    s = np.clip(-m / 2, lo, hi)
    root = float(np.min(s * s + m * s + c))
    leaf = 0.0  # bag n: -phi_n = 0
    return -(root + leaf), worst_bag


def main():
    eps = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-6
    print("quadratic path, b = %.2f, eps = %.0e; bd tolerance eps/n per edge" % (B, eps))
    print("%5s %10s %10s %12s %14s %18s | %14s %12s %10s" % (
        "n", "bd cells", "per edge", "/sqrt(n)", "min|p_t|/q_t", "min cells/LB (LB)",
        "graded cells", "per edge", "gap/eps"))
    for n in (4, 8, 16, 32, 64, 128, 256):
        u, v = riccati(n, B)
        q = u + v
        theta = np.array([(2 * (n - t) + 1) / (2 * n) for t in range(n + 2)])
        p = u - theta * q
        tot = 0
        ratio = []      # (bd cells on edge t) / (lower bound of Proposition 6), edges t <= (n+1)/2
        lbmin = np.inf
        for t in range(1, n + 1):
            cells = bd_cells(p[t], q[t], n, eps)
            tot += len(cells)
            Kt = (n * abs(p[t]) - q[t] / 2) / q[t]
            if t <= (n + 1) / 2 and Kt > 11:
                ranges = int(np.floor(0.5 * np.log2(q[t] / eps)))
                lb = ranges * np.sqrt(Kt - 2) / 12
                ratio.append(len(cells) / lb)
                lbmin = min(lbmin, lb)
        # comparison: cells graded at ratio 1/4 around 0 on every edge, core h with n (|u|/4) h^2 <= eps/2
        h = 2.0 ** -np.ceil(np.log2(1 / np.sqrt(2 * eps / (n * 0.2))))
        gc = graded_cells(h, 0.25)
        gap, worst_bag = split_gap(n, B, {t: gc for t in range(1, n + 1)})
        lbtxt = ("%6.2f (%5.1f)" % (min(ratio), lbmin)) if ratio else "   n/a (K<=11)"
        print("%5d %10d %10.1f %12.2f %14.3f %18s | %14d %12d %10.3f  (max |non-root bag min| = %.1e)" % (
            n, tot, tot / n, tot / n / np.sqrt(n), float(np.min(np.abs(p[1:n + 1]) / q[1:n + 1])),
            lbtxt, n * len(gc), len(gc), gap / eps, worst_bag), flush=True)


if __name__ == "__main__":
    main()
