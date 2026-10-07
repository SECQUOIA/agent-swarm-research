"""Referee check (round 2 confirmation): exact parts of Proposition C.5 / Section 4.6 of robust-chains.md.

  ids     sympy: the decompositions used in C.5(a)-(d) (general b, g, ev, M), end terms with linear and quadratic
          box constraints; the threshold M <= 1.0408 at (0.6, 0.3, 0.05).
  dir     the unbounded direction for univariate multipliers: symbolic LDL^T pivots of the clique moment matrix in
          the natural basis (1, x, y, x^2, xy, y^2), and an exact (fractions) feasibility check of the global moment
          vector for n = 5 and s = 1, 10, 1000 with the objective value.
  gap     rigorous upper bounds on the relaxation value (so lower bounds on the root gap) for some placements:
          solver moment vector, mixed with the moments of the uniform product measure (weight lam), rounded to
          rationals, then every PSD/linear constraint checked in exact arithmetic (LDL^T with fractions).
Usage: python3 d3_exact.py ids|dir|gap
"""
import sys
from fractions import Fraction as Fr


def ids():
    import sympy as sp
    x, y, t, b, g, ev, M = sp.symbols("x y t b g ev M", real=True)
    a = b + ev
    W = a / 2 * (x**2 + y**2) + b * x * y + g / 2 * (x * y**2 - x**2 * y)
    h = lambda z: -g / 2 * z**3
    lhs = W + h(x) - h(y)
    dec_ab = ((b / 2 - g) * (x + y)**2 + ev / 2 * (x**2 + y**2)) + g / 2 * (x + y)**2 * (1 + y) + g / 2 * (x + y)**2 * (1 - x)
    print("(a),(b) bracket decomposition residual:", sp.expand(lhs - dec_ab))
    for sgn, nm in ((1, "a/2 t^2 - h(t)"), (-1, "a/2 t^2 + h(t)")):
        e = a / 2 * t**2 - sgn * h(t) - ((a - g) / 2 * t**2 + g / 2 * t**2 * (1 + sgn * t))
        print(f"    end term {nm} - [((a-g)/2) t^2 + (g/2) t^2 (1 {'+' if sgn > 0 else '-'} t)] =", sp.expand(e))
    print("(c) 1 + y - [(1+y)^2/2 + (1-y^2)/2] =", sp.expand(1 + y - ((1 + y)**2 / 2 + (1 - y**2) / 2)),
          "; 1 - x - [(1-x)^2/2 + (1-x^2)/2] =", sp.expand(1 - x - ((1 - x)**2 / 2 + (1 - x**2) / 2)))
    print("    end term with 1 - t^2: t^2 (1 +/- t) - [t^2 (1 +/- t)^2/2 + t^2 (1 - t^2)/2] =",
          [sp.expand(t**2 * (1 + s * t) - (t**2 * (1 + s * t)**2 / 2 + t**2 * (1 - t**2) / 2)) for s in (1, -1)])
    dec_d = ((b - g * (M**2 + 1)) / 2 * (x + y)**2 + ev / 2 * (x**2 + y**2)) \
        + g / 4 * (x + y)**2 * ((1 + y)**2 + (1 - x)**2) + g / 4 * (x + y)**2 * (2 * M**2 - x**2 - y**2)
    print("(d) residual with ball 2M^2 - x^2 - y^2:", sp.expand(lhs - dec_d))
    al = (b - g * (M**2 + 1)) / 2
    Q = sp.Matrix([[al + ev / 2, al], [al, al + ev / 2]])
    print("    first bracket as a quadratic form: eigenvalues", [sp.simplify(e) for e in Q.eigenvals()],
          "-> PSD iff b - g(M^2+1) + ev/2 >= 0 (and ev >= 0)")
    Mmax = sp.sqrt((sp.Rational(6, 10) + sp.Rational(5, 200)) / sp.Rational(3, 10) - 1)
    print("    at (0.6, 0.3, 0.05): M <=", Mmax, "=", sp.N(Mmax, 8))
    # degrees: every SOS term has degree <= 4, every multiplier times constraint has degree <= 4
    print("    degrees: (x+y)^2 (1+y): 3 (multiplier (x+y)^2 of degree 2 times linear 1+y); (x+y)^2 (1+y)^2: 4; "
          "(x+y)^2 (2M^2 - x^2 - y^2): 4 (degree-2 multiplier times quadratic)")


def ldl_pivots(A):
    """exact LDL^T pivots of a symmetric Fraction matrix (list of lists); returns pivots (None if a zero pivot
    with nonzero column occurs)."""
    n = len(A)
    A = [row[:] for row in A]
    piv = []
    for k in range(n):
        p = A[k][k]
        piv.append(p)
        if p == 0:
            if any(A[i][k] != 0 for i in range(k + 1, n)):
                return None
            continue
        for i in range(k + 1, n):
            f = A[i][k] / p
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return piv


def is_psd_exact(A):
    piv = ldl_pivots(A)
    return piv is not None and all(p >= 0 for p in piv), (min(piv) if piv else None)


BASIS2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
BASIS1 = [(0, 0), (1, 0), (0, 1)]


def direction():
    import sympy as sp
    s = sp.symbols("s", nonnegative=True)
    T = 4 * s**2 + 2
    mom = {(0, 0): 1, (2, 0): sp.Rational(1, 2), (0, 2): sp.Rational(1, 2), (1, 2): -s, (4, 0): 2 * T, (0, 4): 2 * T, (2, 2): T}
    Mx = sp.Matrix([[mom.get((p[0] + q[0], p[1] + q[1]), 0) for q in BASIS2] for p in BASIS2])
    print("clique moment matrix (basis 1, x, y, x^2, xy, y^2):", Mx.tolist())
    # symbolic LDL^T pivots in the natural order
    A = Mx.copy()
    piv = []
    for k in range(6):
        p = sp.simplify(A[k, k])
        piv.append(sp.factor(p))
        for i in range(k + 1, 6):
            f = A[i, k] / p
            for j in range(k + 1, 6):
                A[i, j] = sp.simplify(A[i, j] - f * A[k, j])
    print("LDL^T pivots:", piv)
    print("all pivots positive for every real s:", all(sp.solve(sp.numer(sp.together(pv)) <= 0, s) == sp.false or
                                                     sp.Poly(sp.numer(sp.together(pv)), s).all_coeffs() and
                                                     all(c >= 0 for c in sp.Poly(sp.numer(sp.together(pv)), s).all_coeffs())
                                                     for pv in piv))
    print("det:", sp.factor(Mx.det()))
    # exact global feasibility for n = 5 with fractions
    n = 5
    for sv in (Fr(1), Fr(10), Fr(1000)):
        Tv = 4 * sv * sv + 2
        mm = {(0, 0): Fr(1), (2, 0): Fr(1, 2), (0, 2): Fr(1, 2), (1, 2): -sv, (4, 0): 2 * Tv, (0, 4): 2 * Tv, (2, 2): Tv}
        uni_mom = {0: Fr(1), 1: Fr(0), 2: Fr(1, 2), 3: Fr(0), 4: 2 * Tv}
        ok = True
        for k in range(n - 1):
            # univariate moments of clique k agree with the shared ones (both coordinates)
            for d in range(5):
                ok &= mm.get((d, 0), Fr(0)) == uni_mom[d] and mm.get((0, d), Fr(0)) == uni_mom[d]
            A = [[mm.get((p[0] + q[0], p[1] + q[1]), Fr(0)) for q in BASIS2] for p in BASIS2]
            ok &= is_psd_exact(A)[0]
        for sg in (1, -1):  # localizing of 1 + sg x with basis (1, x)
            L = [[uni_mom[p + q] + sg * uni_mom[p + q + 1] for q in range(2)] for p in range(2)]
            ok &= is_psd_exact(L)[0]
        a, g = Fr(65, 100), Fr(3, 10)
        obj = a * n * Fr(1, 2) - g / 2 * (n - 1) * sv
        print(f"n = 5, s = {sv}: all clique moment matrices and univariate localizing matrices PSD (exact): {ok}; "
              f"objective = {obj} = {float(obj):.3f}")


def gap():
    import numpy as np
    import d2_sdp as D

    class Rec(D.Relax):
        def __init__(self, n):
            super().__init__(n)
            self.specs = []

        def psd(self, k, basis, poly):
            self.specs.append((k, basis, poly))
            super().psd(k, basis, poly)

    def unif(key):  # moments of the uniform product measure on [-1,1]^n
        def m1(p):
            return Fr(0) if p % 2 else Fr(1, p + 1)
        if key == ("1",):
            return Fr(1)
        if key[0] == "u":
            return m1(key[2])
        return m1(key[2]) * m1(key[3])

    cases = [(5, "opp", None, False, False), (8, "opp", None, False, False), (8, "opp", 2.0, False, False),
             (5, "opp", 10.0, False, False), (5, "uni", None, True, False)]
    for (n, place, ball, yb, zb) in cases:
        D.Relax = Rec
        prob, R = D.build(n, place, ball, yb, zb)
        prob.solve(solver="CLARABEL")
        val = prob.value
        for lam in (Fr(1, 10**4), Fr(1, 10**3), Fr(1, 100)):
            ym = {}
            for kk, var in R.mom.items():
                ym[kk] = (1 - lam) * Fr(float(var.value)).limit_denominator(10**12) + lam * unif(kk)

            def Y(k, i, j):
                kk = R.key(k, i, j)
                return Fr(1) if kk == ("1",) else ym[kk]
            ok = True
            worst = None
            for (k, basis, poly) in R.specs:
                A = [[sum(Fr(cf).limit_denominator(10**6) * Y(k, p[0] + q[0] + m[0], p[1] + q[1] + m[1]) for cf, m in poly)
                      for q in basis] for p in basis]
                good, mn = is_psd_exact(A)
                ok &= good
                worst = mn if worst is None or (mn is not None and mn < worst) else worst
            if yb:
                ok &= all(abs(v) <= 1 for v in ym.values())
            a, b, g = Fr(65, 100), Fr(6, 10), Fr(3, 10)
            obj = sum(a / 2 * (Y(k, 2, 0) + Y(k, 0, 2)) + b * Y(k, 1, 1) + g / 2 * (Y(k, 1, 2) - Y(k, 2, 1)) for k in range(n - 1))
            obj += a / 2 * Y(0, 2, 0) + a / 2 * Y(n - 2, 0, 2)
            print(f"n = {n}, {place}, ball = {ball}, ybound = {yb}: solver value {val:.7f}; lam = {lam}: rational point feasible "
                  f"(exact LDL^T): {ok}; exact objective = {float(obj):.7f}" + (" -> relaxation value <= this < 0 (gap proved)" if ok and obj < 0 else ""),
                  flush=True)
            if ok:
                break
        D.Relax = Rec.__mro__[1]


if __name__ == "__main__":
    {"ids": ids, "dir": direction, "gap": gap}[sys.argv[1]]()
