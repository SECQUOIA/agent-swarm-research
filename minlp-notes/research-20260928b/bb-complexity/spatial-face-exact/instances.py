"""Instances for the face-exact node-complexity checks.  All have known optimal value fstar."""
import math
import numpy as np
from face_bb import Problem

A0, B0 = 1.0 / 3.0, math.sqrt(2.0) - 1.0


def kink(a=A0, b=B0, L=2.0, c=-1.0):
    """f = L|x-a| + c (x-a)(y-b) on [0,1]^2.  Optimal set: segment x = a (aligned), sharp growth."""
    # c(x-a)(y-b) = c xy - c b x - c a y + c a b
    return Problem(f"kink(a={a:.4g})", [0, 0], [1, 1], c=[-c * b, -c * a], terms=[(0, 1, c)],
                   absterms=[([1, 0], a, L)], fstar=0.0, const=c * a * b)


def kink_mirror(a=A0, b=B0, L=2.0, c=-1.0):
    """f = L|y-b| + c (x-a)(y-b): optimal set y = b (aligned with the other coordinate)."""
    return Problem(f"kinkT(b={b:.4g})", [0, 0], [1, 1], c=[-c * b, -c * a], terms=[(0, 1, c)],
                   absterms=[([0, 1], b, L)], fstar=0.0, const=c * a * b)


def tilt(theta, a=0.5, b=0.5, L=2.0, c=1.0):
    """f = L|U| + c U Y with U = (x-a) + theta (y-b), Y = y-b  (theta, c > 0).
    = L|U| + c (x-a)(y-b) + c theta (y-b)^2 ; the (y-b)^2 part is convex and kept exactly.
    Optimal set: the line U = 0, tilted by angle ~theta from the vertical; sharp growth.
    Transversal for theta != 0; along a concave direction of c xy (c > 0)."""
    # c(x-a)(y-b) = c xy - c b x - c a y + c a b ; c theta (y-b)^2 = c theta y^2 - 2 c theta b y + c theta b^2
    Q = np.array([[0.0, 0.0], [0.0, 2 * c * theta]])
    return Problem(f"tilt({theta:g})", [0, 0], [1, 1], c=[-c * b, -c * a - 2 * c * theta * b],
                   terms=[(0, 1, c)], absterms=[([1, theta], a + theta * b, L)], Q=Q,
                   fstar=0.0, const=c * a * b + c * theta * b * b)


def diag(cshift=0.0):
    """f = (x + y - 1)^2 = x^2 + y^2 + 2xy - 2x - 2y + 1 on [0,1]^2; x^2+y^2 exact, 2xy McCormick.
    Optimal set: anti-diagonal x + y = 1 (p = 1), transversal, smooth quadratic growth."""
    Q = np.array([[2.0, 0.0], [0.0, 2.0]])
    return Problem("diag", [0, 0], [1, 1], c=[-2, -2], terms=[(0, 1, 2.0)], Q=Q, fstar=0.0, const=1.0)


def iso(a=A0, b=B0, c=1.0):
    """f = (x-a)^2 + (y-b)^2 + c (x-a)(y-b) (|c| < 2): isolated nondegenerate minimum, smooth."""
    Q = np.array([[2.0, 0.0], [0.0, 2.0]])
    # (x-a)^2 + (y-b)^2 = x^2+y^2 - 2ax - 2by + a^2 + b^2 ; c(x-a)(y-b) = c xy - c b x - c a y + c a b
    return Problem(f"iso(c={c:g})", [0, 0], [1, 1], c=[-2 * a - c * b, -2 * b - c * a],
                   terms=[(0, 1, c)], Q=Q, fstar=0.0, const=a * a + b * b + c * a * b)


def sharp_pt(a=A0, b=B0, L=2.0, c=-1.0):
    """f = L|x-a| + L|y-b| + c (x-a)(y-b): sharp isolated minimum (a,b)."""
    return Problem("sharp_pt", [0, 0], [1, 1], c=[-c * b, -c * a], terms=[(0, 1, c)],
                   absterms=[([1, 0], a, L), ([0, 1], b, L)], fstar=0.0, const=c * a * b)


def aligned_quad(a=A0, gamma=1.0, c=1.0):
    """3 variables (x, y, z) on [0,1]^3, f = gamma (x-a)^2 + c (x-a)(y - z), constraint y = z.
    On the feasible plane f = gamma (x-a)^2: optimal set {x = a, y = z} is aligned
    (tangent (0,1,1) lies in span(e_y, e_z), {y,z} independent in the gap graph) but the
    transverse growth is quadratic.  Relaxation: termwise McCormick of c x y and -c x z."""
    Q = np.array([[2 * gamma, 0, 0], [0, 0, 0], [0, 0, 0]])
    # gamma(x-a)^2 = gamma x^2 - 2 gamma a x + gamma a^2 ; c(x-a)(y-z) = c xy - c xz - c a y + c a z
    A = np.array([[0.0, 1.0, -1.0, 0.0, 0.0]])  # columns x,y,z,w_xy,w_xz
    return Problem("aligned_quad", [0, 0, 0], [1, 1, 1], c=[-2 * gamma * a, -c * a, c * a],
                   terms=[(0, 1, c), (0, 2, -c)], Q=Q, rows=(A, [0.0], [0.0]),
                   fstar=0.0, const=gamma * a * a)


# ---------------------------------------------------------------------------------------------
# Pooling (p-formulation, Haverly 1978) and random box QPs.  Constraints involve lifted variables,
# so the pruning criterion (V) is only necessary there (Section 1); these runs are illustrations.

def _lp_fixed_q(P, qidx, qvals):
    """For pooling: with the pool qualities fixed, the p-formulation is an LP; return its value."""
    from face_bb import relax
    l, u = P.lo.copy(), P.hi.copy()
    for i, v in zip(qidx, qvals):
        l[i] = u[i] = v
    return relax(P, l, u)[0]      # McCormick is exact when one factor is fixed


def haverly(variant=1, qhi=3.0):
    """Haverly pooling problem, one pool.  x = [q, px, py, a, b, cx, cy], w = [q px, q py].
    variant 1: standard (f* = -400); 2: X demand 600 (f* = -600); 3: B cost 13 (f* = -750)."""
    dX = 600.0 if variant == 2 else 100.0
    cB = 13.0 if variant == 3 else 16.0
    lo = [1, 0, 0, 0, 0, 0, 0]
    hi = [qhi, dX, 200, 300, 300, dX, 200]
    # cost: 6a + cB b + 10(cx+cy) - 9(px+cx) - 15(py+cy)
    c = [0, -9, -15, 6, cB, 1, -5]
    # rows on [q, px, py, a, b, cx, cy, w0, w1]
    A = np.array([
        [0, -1, -1, 1, 1, 0, 0, 0, 0],        # a + b = px + py
        [0, 0, 0, -3, -1, 0, 0, 1, 1],        # q(px+py) = 3a + b
        [0, -2.5, 0, 0, 0, -0.5, 0, 1, 0],    # X sulfur <= 2.5
        [0, 0, -1.5, 0, 0, 0, 0.5, 0, 1],     # Y sulfur <= 1.5
        [0, 1, 0, 0, 0, 1, 0, 0, 0],          # X demand
        [0, 0, 1, 0, 0, 0, 1, 0, 0],          # Y demand
    ], float)
    INF = 1e30
    rlo = [0, 0, -INF, -INF, -INF, -INF]
    rhi = [0, 0, 0, 0, dX, 200]
    P = Problem(f"haverly{variant}", lo, hi, c=c, terms=[(0, 1, 0.0), (0, 2, 0.0)], rows=(A, rlo, rhi))
    # objective does not contain w: coefficients 0 (terms define w only through the rows)
    qs = np.linspace(1, qhi, 2001)
    vals = [_lp_fixed_q(P, [0], [q]) for q in qs]
    k = int(np.argmin(vals))
    lo_, hi_ = qs[max(k - 1, 0)], qs[min(k + 1, len(qs) - 1)]
    for _ in range(60):   # golden-section refinement (LP value is piecewise smooth in q)
        m1, m2 = lo_ + 0.382 * (hi_ - lo_), lo_ + 0.618 * (hi_ - lo_)
        if _lp_fixed_q(P, [0], [m1]) <= _lp_fixed_q(P, [0], [m2]):
            hi_ = m2
        else:
            lo_ = m1
    cand = [(v, q) for v, q in [(vals[k], qs[k]), (_lp_fixed_q(P, [0], [lo_]), lo_)]]
    P.fstar, P.qstar = min(cand)
    return P


def haverly_2pool(variant=1, qhi=3.0):
    """Two identical pools: x = [q1, q2, px1, py1, px2, py2, a1, b1, a2, b2, cx, cy];
    w = [q1 px1, q1 py1, q2 px2, q2 py2].  Degenerate optimal set (flow can be split)."""
    dX = 600.0 if variant == 2 else 100.0
    cB = 13.0 if variant == 3 else 16.0
    lo = [1, 1] + [0] * 10
    hi = [qhi, qhi, dX, 200, dX, 200, 300, 300, 300, 300, dX, 200]
    c = [0, 0, -9, -15, -9, -15, 6, cB, 6, cB, 1, -5]
    Z = np.zeros
    rows = []
    def row(d):
        r = np.zeros(16)
        for k, v in d.items():
            r[k] = v
        rows.append(r)
    row({6: 1, 7: 1, 2: -1, 3: -1})                    # pool 1 balance
    row({8: 1, 9: 1, 4: -1, 5: -1})                    # pool 2 balance
    row({12: 1, 13: 1, 6: -3, 7: -1})                  # pool 1 sulfur
    row({14: 1, 15: 1, 8: -3, 9: -1})                  # pool 2 sulfur
    row({12: 1, 14: 1, 2: -2.5, 4: -2.5, 10: -0.5})    # X spec
    row({13: 1, 15: 1, 3: -1.5, 5: -1.5, 11: 0.5})     # Y spec
    row({2: 1, 4: 1, 10: 1})                           # X demand
    row({3: 1, 5: 1, 11: 1})                           # Y demand
    INF = 1e30
    rlo = [0, 0, 0, 0, -INF, -INF, -INF, -INF]
    rhi = [0, 0, 0, 0, 0, 0, dX, 200]
    P = Problem(f"haverly{variant}_2pool", lo, hi, c=c,
                terms=[(0, 2, 0.0), (0, 3, 0.0), (1, 4, 0.0), (1, 5, 0.0)], rows=(np.array(rows), rlo, rhi))
    qs = np.linspace(1, qhi, 81)
    best = min((_lp_fixed_q(P, [0, 1], [q1, q2]), q1, q2) for q1 in qs for q2 in qs)
    P.fstar = best[0]
    return P


def boxqp(n, seed, diag=(0.0, 0.0)):
    """min sum_{i<j} c_ij x_i x_j + sum c_i x_i + sum d_i x_i^2 on [0,1]^n, c ~ N(0,1), d ~ U(diag).
    diag = (0,0): multilinear, optimum at a vertex (enumerated).  Otherwise f* by multistart +
    active-set polishing (exact KKT solve on the optimal face)."""
    import itertools
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(n, n))
    cl = rng.normal(size=n)
    d = rng.uniform(*diag, size=n)
    terms = [(i, j, C[i, j]) for i in range(n) for j in range(i + 1, n)]
    Q = np.diag(2 * d) if diag[1] > 0 else None
    P = Problem(f"boxqp{n}s{seed}" + ("c" if Q is not None else "b"), [0] * n, [1] * n, c=cl, terms=terms, Q=Q)
    if Q is None:
        P.fstar = min(P.f(np.array(v, float)) for v in itertools.product([0, 1], repeat=n))
        return P
    from scipy.optimize import minimize
    H = np.diag(2 * d)
    for (i, j, v) in terms:
        H[i, j] += v; H[j, i] += v
    best = (np.inf, None)
    for _ in range(300):
        r = minimize(P.f, rng.uniform(0, 1, n), jac=lambda x: H @ x + cl, method="L-BFGS-B",
                     bounds=[(0, 1)] * n, options={"ftol": 1e-15, "gtol": 1e-12})
        x = r.x
        # polish: fix coordinates at bounds, solve H_FF x_F = -(c_F + H_FB x_B)
        B = [i for i in range(n) if x[i] < 1e-7 or x[i] > 1 - 1e-7]
        Fr = [i for i in range(n) if i not in B]
        xb = np.round(x[B]) if B else np.array([])
        xx = x.copy(); xx[B] = xb
        if Fr:
            try:
                xF = np.linalg.solve(H[np.ix_(Fr, Fr)], -(cl[Fr] + (H[np.ix_(Fr, B)] @ xb if B else 0)))
                if np.all(xF >= -1e-12) and np.all(xF <= 1 + 1e-12):
                    xx[Fr] = xF
            except np.linalg.LinAlgError:
                pass
        v = P.f(xx)
        if v < best[0]:
            best = (v, xx)
    P.fstar, P.xstar = best
    return P


def _golden_min(fun, lo, hi, iters=90):
    """Minimum of a convex function of one variable on [lo, hi] (vectorised golden section)."""
    g = (math.sqrt(5) - 1) / 2
    a, b = lo.copy(), hi.copy()
    c1, c2 = b - g * (b - a), a + g * (b - a)
    f1, f2 = fun(c1), fun(c2)
    for _ in range(iters):
        left = f1 <= f2
        b = np.where(left, c2, b); a = np.where(left, a, c1)
        c2n = np.where(left, c1, a + g * (b - a)); c1n = np.where(left, b - g * (b - a), c2)
        c1, c2 = c1n, c2n
        f1, f2 = fun(c1), fun(c2)
    t = 0.5 * (a + b)
    return t, fun(t)


def tilt_exact(theta, a=0.5, b=0.5, L=2.0, c=1.0):
    """tilt(theta) with an exact node bound (no QP solver).  f_B = L|U| + vex(c X Y) + c theta Y^2 is
    convex; in every cell of the arrangement {kink line, envelope ridge, box edges} it is linear in x
    plus a convex quadratic in y, so its minimum over the box lies on one of these six segments.
    Each restriction is convex in the segment parameter and is minimised by golden section."""
    P = tilt(theta, a, b, L, c)
    assert c > 0

    def fB(x, y, l, u):
        X, Y = x - a, y - b
        Xl, Xu, Yl, Yu = l[0] - a, u[0] - a, l[1] - b, u[1] - b
        env = c * np.maximum(Yl * X + Xl * Y - Xl * Yl, Yu * X + Xu * Y - Xu * Yu)
        return L * np.abs(X + theta * Y) + env + c * theta * Y * Y

    def custom(l, u):
        segs = []   # (x(t), y(t), t0, t1)
        segs.append((lambda t: np.full_like(t, l[0]), lambda t: t, l[1], u[1]))
        segs.append((lambda t: np.full_like(t, u[0]), lambda t: t, l[1], u[1]))
        segs.append((lambda t: t, lambda t: np.full_like(t, l[1]), l[0], u[0]))
        segs.append((lambda t: t, lambda t: np.full_like(t, u[1]), l[0], u[0]))
        segs.append((lambda t: l[0] + t * (u[0] - l[0]), lambda t: u[1] - t * (u[1] - l[1]), 0.0, 1.0))  # ridge
        # kink line x = a - theta (y - b), y in [l_y,u_y] with x in [l_x,u_x]
        ylo = max(l[1], b + (a - u[0]) / theta); yhi = min(u[1], b + (a - l[0]) / theta)
        if ylo <= yhi:
            segs.append((lambda t: a - theta * (t - b), lambda t: t, ylo, yhi))
        best = (math.inf, None)
        for (xf, yf, t0, t1) in segs:
            t, v = _golden_min(lambda tt: fB(xf(tt), yf(tt), l, u), np.array([t0], float), np.array([t1], float))
            if v[0] < best[0]:
                best = (float(v[0]), np.array([float(xf(t)[0]), float(yf(t)[0])]))
        xh = best[1]
        w = max(l[1] * xh[0] + l[0] * xh[1] - l[0] * l[1], u[1] * xh[0] + u[0] * xh[1] - u[0] * u[1])
        return best[0], xh, np.array([w])

    P.custom_relax = custom
    P.name = f"tiltX({theta:g})"
    return P


def path3(a1=1.0 / 3.0, a2=math.sqrt(2.0) - 1.0):
    """Interaction graph x1 - y - x2 (y has two 'centers').  f = |X1 - X2| + (X1 - X2) y on [0,1]^3,
    X_k = x_k - a_k.  f >= 0, and f = 0 on the plane {X1 = X2} (all y) and on {X1 < X2, y = 1}.
    The face {x1 = a1, x2 = a2} is optimal, but the optimal set also contains the 2-flat {X1 = X2},
    which is not transversal (it contains (1,1,0) in span(e_x1, e_x2)) yet has tau(V,E) = 1/sqrt2 > 0."""
    return Problem("path3", [0, 0, 0], [1, 1, 1], c=[0, 0, -(a1 - a2)], terms=[(0, 2, 1.0), (1, 2, -1.0)],
                   absterms=[([1, -1, 0], a1 - a2, 1.0)], fstar=0.0)


def box_aligned(a=1.0 / 3.0, K=None):
    """Counterexample A of the face-exact review (2026-09-29): box-constrained, no constraints.
    K = None: f = (x-a)^2 + (x-a)(y-z) + (y-z)^2 = (X + D/2)^2 + 3D^2/4  (convex as a whole).
    K > 1   : f = (x-a)^2 + (x-a)(y-z) + K|y-z|  (nonconvex; >= X^2 + (K-1)|D| since |X| <= 1).
    X = x-a, D = y-z; argmin = segment {x = a, y = z}: aligned (tangent (0,1,1) in span(e_y,e_z),
    {y,z} independent in G = {xy, xz}), in ker C, with quadratic growth in x.
    Relaxation: (x-a)^2 and (y-z)^2 or K|y-z| exact, McCormick on xy and -xz."""
    # (x-a)(y-z) = xy - xz - a y + a z
    if K is None:
        Q = np.array([[2.0, 0, 0], [0, 2.0, -2.0], [0, -2.0, 2.0]])
        P = Problem("box_aligned", [0, 0, 0], [1, 1, 1], c=[-2 * a, -a, a], terms=[(0, 1, 1.0), (0, 2, -1.0)],
                    Q=Q, fstar=0.0, const=a * a)
    else:
        Q = np.array([[2.0, 0, 0], [0, 0, 0], [0, 0, 0]])
        P = Problem(f"box_alignedK{K:g}", [0, 0, 0], [1, 1, 1], c=[-2 * a, -a, a],
                    terms=[(0, 1, 1.0), (0, 2, -1.0)], absterms=[([0, 1, -1], 0.0, K)], Q=Q, fstar=0.0, const=a * a)
    P.xstar = np.array([a, 0.5, 0.5])
    return P


def with_incumbent(P, xstar):
    """Attach an optimal point (the incumbent of the fixed-UBD model) for incumbent branching."""
    P.xstar = np.array(xstar, float)
    return P
