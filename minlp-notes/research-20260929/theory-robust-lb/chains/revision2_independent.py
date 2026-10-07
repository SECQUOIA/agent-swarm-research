"""Independent cross-checks for revision 2 of robust-chains.md (written separately from revision2_chains.py).

Commands:
  python3 revision2_independent.py wall   Lemma A.4 by a second route: the split built from the shifts r_i relative to
                                          the balanced split (sympy, n = 4..14); the factor minima of the first, last and
                                          odd bonds (sympy, symbolic); min H and min phi on the squares left over by the
                                          monotonicity argument, by interval arithmetic (mpmath.iv, outward rounding).
  python3 revision2_independent.py sos    The SOS side (Putinar certificates, Gram matrices) of the order-2 sparse
                                          relaxation of the chiral chain at (b, g, ev) = (0.6, 0.3, 0.05), for several
                                          placements of the box constraints; compare with the moment side in
                                          logs/revision2_sos.log. Also: an explicit unbounded direction of the moment
                                          relaxation with univariate multipliers (Waki et al. (20)), checked by eigenvalues;
                                          and the sympy identity for the ball 2M^2 - x^2 - y^2.
  python3 revision2_independent.py direction   part (F) only.
"""
import sys
import itertools


def wall():
    import sympy as sp
    from mpmath import iv, mpf
    t = sp.symbols("t", real=True)
    u = sp.Rational(1022, 1000) * t + sp.Rational(189, 1000) * t**2 + sp.Rational(1774, 1000) * t**3 \
        + sp.Rational(1086, 1000) * t**4
    b = sp.Rational(962, 1000)
    U = lambda z: u.subs(t, z)
    # (A) split from the shifts r_i (relative to the balanced split): r_i = b t - u/2 (i even), u/2 - b t (i odd)
    ok = True
    for n in range(4, 15, 2):
        X = sp.symbols(f"x1:{n + 1}", real=True)
        r = {i: (b * X[i - 1] - U(X[i - 1]) / 2 if i % 2 == 0 else U(X[i - 1]) / 2 - b * X[i - 1]) for i in range(2, n)}
        facs = []
        for e in range(1, n):  # bond e joins x_e and x_{e+1}
            F = (U(X[e - 1]) + U(X[e])) / 2 + b * X[e - 1] * X[e]
            if e == 1:
                F += U(X[0]) / 2
            if e == n - 1:
                F += U(X[-1]) / 2
            F += r.get(e + 1, 0) - r.get(e, 0)
            facs.append(sp.expand(F))
        f = sum(U(z) for z in X) + b * sum(X[i] * X[i + 1] for i in range(n - 1))
        ok &= sp.expand(sum(facs) - f) == 0
        x, y = X[0], X[1]
        # factor shapes
        ok &= sp.expand(facs[0] - (U(X[0]) + b * X[1] * (X[0] + 1))) == 0
        ok &= sp.expand(facs[-1] - (U(X[-1]) + b * X[-2] * (X[-1] + 1))) == 0
        for e in range(2, n - 1):
            xa, xb = X[e - 1], X[e]
            target = U(xa) + U(xb) + b * xa * xb - b * (xa + xb) if e % 2 == 0 else b * (xa + 1) * (xb + 1) - b
            ok &= sp.expand(facs[e - 1] - target) == 0
    print(f"(A) shifts r_i give the factors of Lemma A.4 and add up to f_n, n = 4..14 even: {ok}")
    # (B) end bond: u(x) + b y (x + 1) >= u(x) - b (x + 1) (y = -1, as x + 1 >= 0), and d/dx [u(x) - b(x+1)] = u' - b > 0
    du = sp.diff(u, t)
    pos = sp.Poly(du - b, t).count_roots(-1, 1) == 0 and (du - b).subs(t, 0) > 0
    print(f"(B) u' - b has no root in [-1,1] and is positive at 0: {pos}; so the end-bond minimum is u(-1) = {U(-1)}")
    # (C) min H on [-1, x0]^2, x0 = 1 - 1/b, and min phi on [-1, -1/(2b)]^2, by interval arithmetic on a 64 x 64 split
    iv.dps = 30
    uc = [iv.mpf(0), iv.mpf("1.022"), iv.mpf("0.189"), iv.mpf("1.774"), iv.mpf("1.086")]
    bi = iv.mpf("0.962")

    def ui(z):
        return uc[1] * z + uc[2] * z**2 + uc[3] * z**3 + uc[4] * z**4
    c = [r for r in sp.Poly(du - 2 * b, t).real_roots() if -1 <= r <= 1][0]
    Hc = sp.N(U(-1) + U(c) - 2 * b * c + b, 30)
    m2 = sp.N(U(-1) + U(c) - 2 * b * c, 30)

    def lower(fun, lo, hi, K=64):
        best = None
        for i in range(K):
            for j in range(K):
                X = iv.mpf([lo + (hi - lo) * mpf(i) / K, lo + (hi - lo) * mpf(i + 1) / K])
                Y = iv.mpf([lo + (hi - lo) * mpf(j) / K, lo + (hi - lo) * mpf(j + 1) / K])
                v = fun(X, Y).a
                best = v if best is None or v < best else best
        return best
    x0 = 1 - mpf(1) / mpf("0.962")
    lbH = lower(lambda X, Y: ui(X) + ui(Y) + bi * X * Y - bi * (X + Y), mpf(-1), x0 + mpf("1e-6"))
    print(f"(C) interval lower bound of H on [-1, x0]^2: {lbH}; H(-1,c) = {Hc}; margin {lbH - mpf(str(Hc))}")
    x1 = -mpf(1) / (2 * mpf("0.962"))
    lbP = lower(lambda X, Y: ui(X) + ui(Y) + 2 * bi * X * Y, mpf(-1), x1 + mpf("1e-6"))
    print(f"    interval lower bound of 2 phi on [-1, -1/(2b)]^2: {lbP}; 2m = {m2}; margin {lbP - mpf(str(m2))}")


def sos():
    import numpy as np
    import cvxpy as cp
    import sympy as sp
    # (D) identity with the ball 2M^2 - x^2 - y^2
    x, y, b, g, ev, M = sp.symbols("x y b g ev M", real=True)
    a = b + ev
    W = a / 2 * (x**2 + y**2) + b * x * y + g / 2 * (x * y**2 - x**2 * y)
    lhs = W - g / 2 * x**3 + g / 2 * y**3
    rhs = ((b - g * (M**2 + 1)) / 2 * (x + y)**2 + ev / 2 * (x**2 + y**2)) \
        + g / 4 * (x + y)**2 * ((1 + y)**2 + (1 - x)**2) + g / 4 * (x + y)**2 * (2 * M**2 - x**2 - y**2)
    print(f"(D) W + h(x) - h(y) - [((b - g(M^2+1))/2)(x+y)^2 + (ev/2)(x^2+y^2) + (g/4)(x+y)^2((1+y)^2+(1-x)^2)"
          f" + (g/4)(x+y)^2(2M^2-x^2-y^2)] = {sp.expand(lhs - rhs)}")
    print("    the first bracket is >= 0 when b - g(M^2+1) + ev/2 >= 0 (use x^2 + y^2 >= (x+y)^2/2);"
          f" at (0.6, 0.3, 0.05): M <= {float(sp.sqrt(sp.Rational(625, 300) - 1)):.4f}")

    bb, gg, ee = 0.6, 0.3, 0.05
    aa = bb + ee

    def mono(n, d):
        return tuple(d.get(i, 0) for i in range(n))

    def objective(n):
        P = {}

        def add(m, c):
            P[m] = P.get(m, 0.0) + c
        for i in range(n):
            add(mono(n, {i: 2}), aa)
        for i in range(n - 1):
            add(mono(n, {i: 1, i + 1: 1}), bb)
            add(mono(n, {i: 1, i + 1: 2}), gg / 2)
            add(mono(n, {i: 2, i + 1: 1}), -gg / 2)
        return P

    def certificate(n, placement, ball=None):
        """max lam s.t. f - lam = sum_k sigma_k(x_k, x_{k+1}) + sum_j s_j g_j; s_j SOS on the stated support."""
        lam = cp.Variable()
        expr = {}
        cons = []

        def addto(m, e):
            expr[m] = expr.get(m, 0) + e

        def gram(basis, poly):  # adds poly(x) * basis^T Q basis, Q PSD; poly = {mono: coef}
            k = len(basis)
            Q = cp.Variable((k, k), PSD=True)
            for i in range(k):
                for j in range(k):
                    for pm, pc in poly.items():
                        m = tuple(basis[i][q] + basis[j][q] + pm[q] for q in range(n))
                        addto(m, pc * Q[i, j])
        one = {mono(n, {}): 1.0}

        def basis_clique(k, deg):
            out = []
            for d0 in range(deg + 1):
                for d1 in range(deg + 1 - d0):
                    out.append(mono(n, {k: d0, k + 1: d1}))
            return out
        for k in range(n - 1):
            gram(basis_clique(k, 2), one)
            if ball is not None:
                gram(basis_clique(k, 1), {mono(n, {}): 2 * ball**2, mono(n, {k: 2}): -1.0, mono(n, {k + 1: 2}): -1.0})
        for i in range(n):  # 0-based variable i lies in cliques i-1 (if i >= 1) and i (if i <= n-2)
            left = i - 1 if i >= 1 else i
            right = i if i <= n - 2 else i - 1
            up = {mono(n, {}): 1.0, mono(n, {i: 1}): -1.0}   # 1 - x_i
            lo = {mono(n, {}): 1.0, mono(n, {i: 1}): 1.0}    # 1 + x_i
            if placement == "every":
                for k in sorted({left, right}):
                    gram(basis_clique(k, 1), up)
                    gram(basis_clique(k, 1), lo)
            elif placement == "match":
                gram(basis_clique(right, 1), up)
                gram(basis_clique(left, 1), lo)
            elif placement == "opp":
                gram(basis_clique(left, 1), up)
                gram(basis_clique(right, 1), lo)
            elif placement == "uni":
                ub = [mono(n, {}), mono(n, {i: 1})]
                gram(ub, up)
                gram(ub, lo)
            else:
                raise ValueError(placement)
        P = objective(n)
        allm = set(expr) | set(P) | {mono(n, {})}
        for m in allm:
            target = P.get(m, 0.0) - (lam if m == mono(n, {}) else 0.0)
            cons.append(expr.get(m, 0) == target)
        prob = cp.Problem(cp.Maximize(lam), cons)
        return prob, lam

    for n in (5, 8):
        for placement, ball in (("every", None), ("match", None), ("opp", None), ("opp", 1.0), ("opp", 2.0), ("uni", None)):
            res = []
            for solver in ("CLARABEL", "SCS"):
                prob, lam = certificate(n, placement, ball)
                kw = dict(eps=1e-9, max_iters=200000) if solver == "SCS" else {}
                try:
                    prob.solve(solver=solver, **kw)
                    res.append(f"{solver}: {prob.status} {prob.value if prob.value is None else round(float(prob.value), 7)}")
                except Exception as exc:  # noqa: BLE001
                    res.append(f"{solver}: error {str(exc)[:60]}")
            print(f"(E) SOS side, n = {n}, placement = {placement}, ball M = {ball}: " + "; ".join(res), flush=True)
    direction()


def direction():
    import numpy as np
    aa, gg = 0.65, 0.3
    # (F) unbounded direction for univariate multipliers (linear box constraints): moments of one clique (x, y)
    def clique_matrix(s, T, delta=0.5):
        # basis 1, x, y, x^2, xy, y^2; first and mixed second moments 0, y_{x^2} = y_{y^2} = delta,
        # y_{x y^2} = -s, other cubic moments 0, y_{x^4} = y_{y^4} = 2T, y_{x^2 y^2} = T, other quartic moments 0.
        # The univariate moments (0, delta, 0, 2T) are the same in every clique, so the cliques are consistent.
        mom = {(0, 0): 1, (2, 0): delta, (0, 2): delta, (1, 2): -s, (4, 0): 2 * T, (0, 4): 2 * T, (2, 2): T}
        B = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
        return np.array([[mom.get((p[0] + q[0], p[1] + q[1]), 0.0) for q in B] for p in B])
    import sympy as sp
    sv = sp.symbols("s", nonnegative=True)
    d, T = sp.Rational(1, 2), 4 * sv**2 + 2
    Bk = sp.Matrix([[1, 0, d, d], [0, d, 0, -sv], [d, 0, 2 * T, T], [d, -sv, T, 2 * T]])  # rows 1, x, x^2, y^2
    Bs = sp.Matrix([[d, -sv], [-sv, T]])  # rows y, xy; the two blocks do not interact
    minors = [sp.factor(Bk[:k, :k].det()) for k in range(1, 5)] + [sp.factor(Bs[:k, :k].det()) for k in range(1, 3)]
    print("(F) exact: leading principal minors of the two diagonal blocks of the clique moment matrix (T = 4 s^2 + 2):",
          minors, "-> all positive for s >= 0:",
          all(sp.Poly(sp.expand(mm), sv).all_coeffs() and all(cf >= 0 for cf in sp.Poly(sp.expand(mm), sv).all_coeffs())
              and sp.expand(mm).subs(sv, 0) > 0 for mm in minors))
    for s in (1, 10, 100):
        ev_min = np.linalg.eigvalsh(clique_matrix(s, T=4.0 * s**2 + 2)).min()
        loc = np.array([[1, -0.5], [-0.5, 0.5]])  # (1 -/+ x) [1, x][1, x]^T with y_x = 0, y_{x^2} = 0.5, y_{x^3} = 0
        n = 5
        print(f"(F) s = {s}: min eigenvalue of every clique moment matrix {ev_min:.4f} (T = 4 s^2 + 2); univariate "
              f"localizing matrices of 1 -/+ x_i: min eigenvalue {np.linalg.eigvalsh(loc).min():.4f}; objective at n = {n}: "
              f"a n delta - (g/2)(n-1) s = {aa * n * 0.5 - gg / 2 * (n - 1) * s:.3f} (-> -inf as s grows)")


if __name__ == "__main__":
    {"wall": wall, "sos": sos, "direction": direction}[sys.argv[1]]()  # "sos" ends with part (F)
