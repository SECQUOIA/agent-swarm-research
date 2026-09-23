"""Numerical checks for results/mip-relaxation-binary-lower-bounds.md.

(i)  The depth-L sawtooth relaxation of x^2 on [0,1] (Beach et al., Part I,
     Definition 5) is built as a union of 2^L polyhedra, one per binary vector
     alpha; its maximum vertical error is computed by LP and compared with the
     explicit formula, confirming E_max = 2^{-2L-2} for L = 1..6.
(ii) The area lemma for xy: a set S in [0,1]^2 with |dx*dy| <= 4E for every
     pair of its points has bounding-box area X*Y <= 20E and Lebesgue measure
     <= 16 ln2 E.  Random greedy point sets test the box bound and the
     pointwise section inequalities; random envelopes test the measure bound.

Run: source ~/miniconda3/etc/profile.d/conda.sh && conda activate minlp-notes
     python code/mip_relaxation_binaries/check_bounds.py
"""
import itertools
import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import linprog


# ---------------------------------------------------------------------------
# (i) sawtooth relaxation of x^2
# ---------------------------------------------------------------------------
def tooth(t):
    return np.minimum(2 * t, 2 * (1 - t))


def F(j, x):
    """Piecewise linear interpolant of x^2 at breakpoints i/2^j (Part I, eq. (6))."""
    g = np.array(x, dtype=float)
    val = np.array(x, dtype=float).copy()
    for k in range(1, j + 1):
        g = tooth(g)
        val = val - 4.0 ** (-k) * g
    return val


def sawtooth_envelopes_explicit(L, x):
    """Upper and lower boundary of the depth-L sawtooth relaxation at points x."""
    upper = F(L, x)
    lower = np.maximum.reduce([F(j, x) - 4.0 ** (-j) / 4 for j in range(L + 1)]
                              + [np.zeros_like(x), 2 * x - 1])
    return upper, lower


def sawtooth_piece_lp(L, alpha, x):
    """Max and min z of the polyhedron of Definition 5 with alpha fixed and x fixed.

    Variables: (g_1..g_L, z).  Returns (None, None) if x is infeasible for alpha.
    """
    nv = L + 1
    A, b = [], []

    def row(coeffs, rhs):
        r = np.zeros(nv)
        for i, c in coeffs:
            r[i] += c
        A.append(r)
        b.append(rhs)

    # g_0 = x is a constant; g_j variables are indices 0..L-1, z is index L.
    def gidx(j):
        return j - 1

    for j in range(1, L + 1):
        prev = [(gidx(j - 1), 1.0)] if j > 1 else []
        prev_const = 0.0 if j > 1 else x
        # 2(g_{j-1} - alpha_j) <= g_j
        row([(gidx(j), -1.0)] + [(i, 2 * c) for i, c in prev], 2 * alpha[j - 1] - 2 * prev_const)
        # g_j <= 2 g_{j-1}
        row([(gidx(j), 1.0)] + [(i, -2 * c) for i, c in prev], 2 * prev_const)
        # 2(alpha_j - g_{j-1}) <= g_j
        row([(gidx(j), -1.0)] + [(i, -2 * c) for i, c in prev], -2 * alpha[j - 1] + 2 * prev_const)
        # g_j <= 2(1 - g_{j-1})
        row([(gidx(j), 1.0)] + [(i, 2 * c) for i, c in prev], 2 - 2 * prev_const)

    def f_coeffs(j):
        # f_j(x, g) = x - sum_{k<=j} 4^{-k} g_k
        return [(gidx(k), -(4.0 ** (-k))) for k in range(1, j + 1)], x

    # z <= f_L(x,g)
    cf, c0 = f_coeffs(L)
    row([(L, 1.0)] + [(i, -c) for i, c in cf], c0)
    # z >= f_j(x,g) - 4^{-j}/4, j = 0..L
    for j in range(L + 1):
        cf, c0 = f_coeffs(j)
        row([(L, -1.0)] + cf, -c0 + 4.0 ** (-j) / 4)
    row([(L, -1.0)], 0.0)          # z >= 0
    row([(L, -1.0)], 1 - 2 * x)    # z >= 2x - 1
    A = np.array(A)
    b = np.array(b)
    bounds = [(0, 1)] * L + [(None, None)]
    out = []
    for sign in (-1.0, 1.0):
        c = np.zeros(nv)
        c[L] = sign
        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
        if res.status != 0:
            return None, None
        out.append(sign * res.fun)
    return out[0], out[1]  # (max z, min z)


def check_sawtooth(L_max=6):
    print("(i) sawtooth relaxation of x^2: maximum error")
    ok = True
    for L in range(1, L_max + 1):
        # dyadic grid at resolution 2^{-(L+3)} contains all candidate extrema
        # (piece midpoints, breakpoints, tangent intersections) plus a fine grid.
        xs = np.unique(np.concatenate([np.linspace(0, 1, 2 ** (L + 3) + 1),
                                       np.linspace(0, 1, 4001)]))
        up, lo = sawtooth_envelopes_explicit(L, xs)
        err_explicit = max(np.max(up - xs ** 2), np.max(xs ** 2 - lo))
        # union-of-polyhedra check by LP on the dyadic grid, per binary vector
        xs_lp = np.linspace(0, 1, 2 ** (L + 3) + 1)
        err_lp = 0.0
        cover = np.zeros(len(xs_lp), dtype=bool)
        for alpha in itertools.product((0, 1), repeat=L):
            for k, x in enumerate(xs_lp):
                zmax, zmin = sawtooth_piece_lp(L, alpha, float(x))
                if zmax is None:
                    continue
                cover[k] = True
                err_lp = max(err_lp, zmax - x * x, x * x - zmin)
                # consistency with explicit envelopes
                u, l = sawtooth_envelopes_explicit(L, np.array([x]))
                assert zmax <= u[0] + 1e-9 and zmin >= l[0] - 1e-9
        target = 2.0 ** (-2 * L - 2)
        good = (abs(err_explicit - target) < 1e-9 and abs(err_lp - target) < 1e-7
                and cover.all())
        ok &= good
        print(f"  L={L}: 2^L pieces, E_max(explicit)={err_explicit:.10f}, "
              f"E_max(LP)={err_lp:.10f}, 2^(-2L-2)={target:.10f}, "
              f"{'OK' if good else 'MISMATCH'}")
    return ok


# ---------------------------------------------------------------------------
# (ii) area lemma for xy
# ---------------------------------------------------------------------------
def random_compatible_set(rng, E, n_trials, seed_pair=True):
    """Greedy random set S in [0,1]^2 with |dx dy| <= 4E for all pairs."""
    pts = []
    if seed_pair:
        # start from a pair with large x-spread so that X is not tiny
        h = rng.uniform(0, 4 * E)
        pts = [np.array([0.0, 0.5]), np.array([1.0, 0.5 + h])]
    for _ in range(n_trials):
        c = rng.uniform(0, 1, size=2)
        if all(abs((c[0] - q[0]) * (c[1] - q[1])) <= 4 * E for q in pts):
            pts.append(c)
    return np.array(pts)


def check_area_lemma(n_sets=300, seed=0):
    print("(ii) area lemma: pairwise |dx dy| <= 4E  =>  X*Y <= 20E and sections short")
    rng = np.random.default_rng(seed)
    worst_box = 0.0
    worst_sec = 0.0
    ok = True
    for t in range(n_sets):
        E = 10 ** rng.uniform(-4, -1)
        S = random_compatible_set(rng, E, n_trials=2000, seed_pair=(t % 2 == 0))
        if len(S) < 2:
            continue
        X = S[:, 0].max() - S[:, 0].min()
        Y = S[:, 1].max() - S[:, 1].min()
        ratio = X * Y / E
        worst_box = max(worst_box, ratio)
        ok &= ratio <= 20 + 1e-9
        # x-section bound: with a = argmin x, b = argmax x, every point c
        # satisfies |c_y - a_y| <= 4E/|c_x - a_x| and |c_y - b_y| <= 4E/|c_x - b_x|,
        # so the y-values at abscissa u lie in an interval of length
        # min(8E/(u - a_x), 8E/(b_x - u)); we check the pointwise inequalities.
        a = S[np.argmin(S[:, 0])]
        b = S[np.argmax(S[:, 0])]
        for c in S:
            for q in (a, b):
                d = abs(c[0] - q[0])
                if d > 0:
                    ok &= abs(c[1] - q[1]) <= 4 * E / d + 1e-12
                    worst_sec = max(worst_sec, abs(c[1] - q[1]) * d / E)
    print(f"  {n_sets} random sets: max X*Y/E = {worst_box:.3f} (bound 20), "
          f"max |dy|*|dx|/E = {worst_sec:.3f} (bound 4), {'OK' if ok else 'VIOLATION'}")
    # measure bound: S lies in the envelope
    #   T = {(u,y) in [0,1]^2 : |y-a_y| <= 4E/(u-a_x), |y-b_y| <= 4E/(b_x-u)},
    # whose u-section has length <= min(8E/(u-a_x), 8E/(b_x-u)); integrating gives
    # lambda(T) <= 16 ln2 E.  Check numerically on random (a,b,E).
    worst_env = 0.0
    for _ in range(200):
        E = 10 ** rng.uniform(-4, -1)
        ax, bx = np.sort(rng.uniform(0, 1, size=2))
        ay, by = rng.uniform(0, 1, size=2)
        if bx - ax < 1e-6 or abs(ay - by) * (bx - ax) > 4 * E:
            continue

        def section(u):
            lo = max(0.0, ay - 4 * E / (u - ax), by - 4 * E / (bx - u))
            hi = min(1.0, ay + 4 * E / (u - ax), by + 4 * E / (bx - u))
            return max(0.0, hi - lo)

        mid = (ax + bx) / 2
        area = quad(section, ax, mid, limit=200)[0] + quad(section, mid, bx, limit=200)[0]
        worst_env = max(worst_env, area / E)
        ok &= area <= 16 * math.log(2) * E * (1 + 1e-6)
    print(f"  200 random envelopes: max measure/E = {worst_env:.3f} "
          f"(bound 16 ln2 = {16 * math.log(2):.3f}), {'OK' if ok else 'VIOLATION'}")
    return ok


if __name__ == "__main__":
    a = check_sawtooth()
    b = check_area_lemma()
    print("ALL OK" if a and b else "FAILURE")
