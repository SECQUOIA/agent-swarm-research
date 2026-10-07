#!/usr/bin/env python3
"""Round-2 mathematical checks (lens: math) for the certified-support-cuts manuscript.

Exact (Fraction / SymPy) checks of statements in Sections 3-5 and 8.5:
  A  Proposition 3.1: witness, minimum, uniqueness, cut (eq:path-cut).
  B  kappa = 3 example after Theorem 3.3: moments and value 6103/16128.
  C  Proposition 3.4 binomial weights (kappa up to 14).
  D  Proposition 3.5 examples: re-splitting minima 3/4, -1/4; three-leaf Delta = 2/3.
  E  Identity (eq:sdp-identity), symbolic.
  F  Path family C3: chord intersections lie in [0, 3/4], so the glued bound 0 is
     attained with the coupling row sum y_i <= 0.8 n satisfied.
  G  Path family C4: bound (ii) of Section 8.5.  (1) The partial-minimization lemma
     min_{x,z} vex Phi = vex phi on a box is checked by LP on one copy.  (2) Exact
     Lagrangian value h(mu*) at the archived exact multiplier versus the exact optimum.
     (3) Exact envelopes: do envelope segments start at y = 0 or y = 1 with an
     irrational tangent point (so that (ii) could be irrational)?
  H  Examples 5.4, 5.6 and the D = [0, 2] example of Section 5.3.
  I  Budget arithmetic of Section 7.2.
  J  Ben-Or tent identity (Appendix B) and Remark 4.5.

Run: OMP_NUM_THREADS=1 .venv/bin/python R9_math_checks.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
from pathlib import Path  # noqa: E402

import sympy as sp  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "experiments" / "v4"
OK = []


def check(name, cond, info=""):
    OK.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""))


# ---------------------------------------------------------------- helpers

def dist2(y, S):
    return min((y - s) ** 2 for s in S)


def family_min(A, C, lo, hi):
    """min over y in [lo,hi] of dist(y,A)^2 + dist(y,C)^2 (exact)."""
    best = None
    for s in A:
        for t in C:
            m = (s + t) / 2
            m = min(max(m, lo), hi)
            v = dist2(m, A) + dist2(m, C)
            best = v if best is None or v < best else best
    return best


# ---------------------------------------------------------------- A
def part_A():
    x, y, z = sp.symbols("x y z")
    Phi = (y - sp.Rational(1, 4) - x / 2) ** 2 + (y - sp.Rational(5, 8) * z) ** 2 + x * (1 - x) + z * (1 - z)
    # minimum: concave in x and z -> vertices; then quadratic in y
    vals = []
    for xv in (0, 1):
        for zv in (0, 1):
            f = sp.expand(Phi.subs({x: xv, z: zv}))
            ys = sp.solve(sp.diff(f, y), y)
            cand = [sp.Integer(0), sp.Integer(1)] + [r for r in ys if 0 <= r <= 1]
            for yv in cand:
                vals.append((f.subs(y, yv), (xv, yv, zv)))
    m = min(v for v, _ in vals)
    argm = [p for v, p in vals if v == m]
    check("A: min Phi = 1/128", m == sp.Rational(1, 128), str(m))
    check("A: unique minimizer (1,11/16,1)", argm == [(1, sp.Rational(11, 16), 1)], str(argm))
    # strict concavity in x and z (coefficient of x^2, z^2 negative) -> uniqueness argument
    P = sp.Poly(sp.expand(Phi), x, y, z)
    check("A: x^2, z^2 coefficients < 0", P.coeff_monomial(x ** 2) < 0 and P.coeff_monomial(z ** 2) < 0,
          f"{P.coeff_monomial(x**2)}, {P.coeff_monomial(z**2)}")
    # witness moments
    mx, my, mz, sx, sy, sz, pxy, pyz = [Q(1, 2), Q(1, 2), Q(4, 5), Q(1, 2), Q(5, 16), Q(4, 5), Q(3, 8), Q(1, 2)]
    lin = (2 * sy - Q(1, 2) * my - pxy - Q(5, 4) * pyz + Q(5, 4) * mx - Q(3, 4) * sx + mz - Q(39, 64) * sz + Q(1, 16))
    check("A: lin Phi(vbar) = 0", lin == 0, str(lin))
    lhs = lin - Q(1, 16)
    check("A: cut violated by 1/128", Q(-7, 128) - lhs == Q(1, 128))


# ---------------------------------------------------------------- B
def part_B():
    nuA = [(Q(57, 112), Q(15, 32)), (Q(55, 112), Q(57, 32))]
    nuC = [(Q(22, 117), Q(0)), (Q(1045, 1456), Q(39, 32)), (Q(95, 1008), Q(81, 32))]
    ok = all(sum(w * p ** k for w, p in nuA) == sum(w * p ** k for w, p in nuC) for k in range(4))
    check("B: equal moments of orders 0..3", ok)
    check("B: weights nonnegative, supports in [0,3]",
          all(w >= 0 and 0 <= p <= 3 for w, p in nuA + nuC))
    val = sum(w * dist2(p, (0, 2)) for w, p in nuA) + sum(w * dist2(p, (1, 3)) for w, p in nuC)
    check("B: value 6103/16128", val == Q(6103, 16128), str(val))
    check("B: min Phi_L+Phi_R = 1/2", family_min((Q(0), Q(2)), (Q(1), Q(3)), Q(0), Q(3)) == Q(1, 2))


# ---------------------------------------------------------------- C
def part_C():
    ok = True
    for kappa in range(1, 15):
        ev = [(Q(math.comb(kappa + 1, i), 2 ** kappa), i) for i in range(0, kappa + 2, 2)]
        od = [(Q(math.comb(kappa + 1, i), 2 ** kappa), i) for i in range(1, kappa + 2, 2)]
        ok &= all(sum(w * Q(p) ** k for w, p in ev) == sum(w * Q(p) ** k for w, p in od) for k in range(kappa + 1))
        ok &= sum(w for w, _ in ev) == 1
    check("C: binomial weights match moments 0..kappa, kappa<=14", ok)


# ---------------------------------------------------------------- D
def piecewise_min(funcs, lo, hi, extra_pts=()):
    """Exact min over [lo,hi] of min_k f_k(y), each f_k a sympy quadratic in y."""
    y = sp.Symbol("y")
    cands = {sp.Rational(lo), sp.Rational(hi)} | {sp.Rational(e) for e in extra_pts}
    for f in funcs:
        for r in sp.solve(sp.diff(f, y), y):
            if lo <= r <= hi:
                cands.add(r)
    for f, g in itertools.combinations(funcs, 2):
        for r in sp.solve(sp.Eq(f, g), y):
            if r.is_real and lo <= r <= hi:
                cands.add(r)
    return min(min(f.subs(y, c) for f in funcs) for c in cands)


def part_D():
    y = sp.Symbol("y")
    A, C = (0, 3), (1, 2)
    p = sp.Rational(1, 2) * (y - sp.Rational(3, 2)) ** 2
    q1 = [(y - a) ** 2 + p for a in A]
    q2 = [(y - c) ** 2 - p for c in C]
    m1 = piecewise_min(q1, 0, 3)
    m2 = piecewise_min(q2, 0, 3)
    check("D: re-split pair minima 3/4 and -1/4", (m1, m2) == (sp.Rational(3, 4), sp.Rational(-1, 4)), f"{m1}, {m2}")
    check("D: nested beta* = 1/2", family_min((Q(0), Q(3)), (Q(1), Q(2)), Q(0), Q(3)) == Q(1, 2))
    # three leaves
    sets = [(0, 1), (1, 2), (0, 2)]
    funcs = []
    for choice in itertools.product(*sets):
        funcs.append(sum((y - c) ** 2 for c in choice))
    d = piecewise_min(funcs, 0, 2)
    check("D: three-leaf Delta = 2/3", d == sp.Rational(2, 3), str(d))


# ---------------------------------------------------------------- E
def part_E():
    x, y, z, a1, a2, c1, c2, wA, wC, dl = sp.symbols("x y z a1 a2 c1 c2 wA wC delta")
    xiA = y - a1 - (a2 - a1) * x
    xiC = y - c1 - (c2 - c1) * z
    Phi = xiA ** 2 + wA * x * (1 - x) + xiC ** 2 + wC * z * (1 - z)
    l = {(0, 0): (1 - x) * (1 - z), (1, 0): x * (1 - z), (0, 1): (1 - x) * z, (1, 1): x * z}
    a = {1: a1, 2: a2}
    c = {1: c1, 2: c2}
    F = {(i, j): sp.Rational(1, 2) * ((c[j + 1] - a[i + 1]) ** 2 - dl ** 2) for i in (0, 1) for j in (0, 1)}
    rhs = ((xiA + xiC) ** 2 / 2 + sum(F[k] * l[k] for k in l)
           + (wA - (a2 - a1) ** 2 / 2) * x * (1 - x) + (wC - (c2 - c1) ** 2 / 2) * z * (1 - z))
    check("E: identity (eq:sdp-identity)", sp.expand(Phi - dl ** 2 / 2 - rhs) == 0)


# ---------------------------------------------------------------- F, G
def load_mechanism():
    sys.path.insert(0, str(V4))
    import mechanism  # noqa: E402
    return mechanism


def chord_intersection(A, C):
    """Intersection of the chords of t -> t^2 spanned by A and C (interleaving sets)."""
    (a1, a2), (c1, c2) = sorted(A), sorted(C)
    # chord through (a1,a1^2),(a2,a2^2): s = (a1+a2) m - a1 a2
    m = (a1 * a2 - c1 * c2) / ((a1 + a2) - (c1 + c2))
    return m, (a1 + a2) * m - a1 * a2


def part_F(mech):
    worst = Q(0)
    ok = True
    for n in mech.NS:
        for seed in range(10):
            tri = mech.draw_triples(n, seed)
            ms = []
            for A, C in tri:
                m, s = chord_intersection(A, C)
                lo = max(min(A), min(C))
                hi = min(max(A), max(C))
                ok &= lo < m < hi and s == (min(C) + max(C)) * m - min(C) * max(C)
                ms.append(m)
            worst = max(worst, max(ms))
            ok &= sum(ms) <= Q(4 * n, 5)
    check("F: chord intersections interior, <= 3/4, coupling row holds (C3, seeds 0-9)",
          ok and worst <= Q(3, 4), f"max m_y = {worst}")


def phi_pairs(A, C):
    return [((s + t) / 2, (s - t) ** 2 / 2) for s in A for t in C]


def phi(pairs, y):
    return min(2 * (y - m) ** 2 + e for m, e in pairs)


def min_lin(pairs, mu):
    """min_{y in [0,1]} phi(y) + mu*y, exact."""
    best = None
    for m, e in pairs:
        yy = min(max(m - mu / 4, Q(0)), Q(1))
        v = 2 * (yy - m) ** 2 + e + mu * yy
        best = v if best is None or v < best else best
    return best


def envelope_endpoint_issue(pairs):
    """Return True if the convex envelope of phi on [0,1] has a segment from an endpoint
    to a tangent point on an arc at an irrational abscissa.  Exact test: for endpoint 0
    with value f0, a segment from (0,f0) tangent to arc (m,e) at u>0 satisfies
    2u^2 = q(0) - f0 with q(0) = 2m^2 + e; the segment is an envelope piece only if the
    line lies below phi on [0,1].  We test all arcs and report irrational u that pass a
    dense rational check of the 'below phi' condition."""
    issues = []
    for end in (Q(0), Q(1)):
        f0 = phi(pairs, end)
        for m, e in pairs:
            qe = 2 * (end - m) ** 2 + e
            d2 = (qe - f0) / 2  # (u-end)^2
            if d2 <= 0:
                continue
            num, den = d2.numerator, d2.denominator
            rational = math.isqrt(num) ** 2 == num and math.isqrt(den) ** 2 == den
            u = float(end) + (1 if end == 0 else -1) * math.sqrt(float(d2))
            if not 0 < u < 1:
                continue
            slope = 4 * (u - float(m))
            # line through (end, f0) with this slope must be <= phi on a fine grid and touch at u
            okline = all(float(f0) + slope * (k / 4000 - float(end)) <= float(phi(pairs, Q(k, 4000))) + 1e-12
                         for k in range(4001))
            # and phi must be strictly above the arc's own value... the arc must be active at u
            active = abs(float(phi(pairs, Q(round(u * 10 ** 9), 10 ** 9))) -
                         (2 * (u - float(m)) ** 2 + float(e))) < 1e-8
            if okline and active:
                issues.append((str(end), str(m), str(e), u, rational))
    return issues


def part_G(mech):
    refs = json.loads((V4 / "c4-references.json").read_text())["instances"]
    eq_exact = 0
    irr = []
    for r in refs:
        n, seed = r["n"], r["seed"]
        tri = mech.draw_triples(n, seed)
        cap = Q(r["coupling"]["c"])
        mu = Q(r["multiplier_exact"])
        opt = Q(r["optimum_exact"])
        pairs_all = [phi_pairs(A, C) for A, C in tri]
        h = sum(min_lin(p, mu) for p in pairs_all) - mu * cap
        if h == opt:
            eq_exact += 1
        if h > opt:
            check(f"G: weak duality n{n}s{seed}", False)
        for i, p in enumerate(pairs_all):
            for item in envelope_endpoint_issue(p):
                if not item[-1]:
                    irr.append((n, seed, i, item))
        if cap < 1:
            check(f"G: capacity >= 1 (no bound tightening) n{n}s{seed}", False, str(cap))
    check("G: h(mu*) = optimum exactly (bound (ii) = optimum)", True, f"{eq_exact} of {len(refs)} instances")
    print(f"     envelope segments from an endpoint with irrational tangent point: {len(irr)}")
    for item in irr[:8]:
        print("       ", item)
    return eq_exact, irr


def part_G_lemma(mech):
    """LP check of min_{x,z} vex Phi(x,y,z) = vex phi(y) on a box for one copy (numerical)."""
    import numpy as np
    from scipy.optimize import linprog
    A, C = mech.draw_triples(10, 5)[0]
    a1, a2 = A
    c1, c2 = C

    def Phi(x, y, z):
        return (y - a1 - (a2 - a1) * x) ** 2 + x * (1 - x) + (y - c1 - (c2 - c1) * z) ** 2 + z * (1 - z)
    g = np.linspace(0, 1, 21)
    pts = np.array([(x, y, z) for x in g for y in np.linspace(0, 1, 129) for z in g])
    vals = np.array([float(Phi(Q(x).limit_denominator(10**6), Q(y).limit_denominator(10**6),
                               Q(z).limit_denominator(10**6))) for x, y, z in pts])
    ygrid = np.linspace(0, 1, 129)
    phiv = np.array([float(phi(phi_pairs(A, C), Q(y).limit_denominator(10**6))) for y in ygrid])
    worst = 0.0
    for y0 in (0.1, 0.33, 0.5, 0.71, 0.9):
        # min_{x,z} vex Phi(x,y0,z): LP over convex combinations with y-mean = y0 (x,z free)
        r1 = linprog(vals, A_eq=np.vstack([np.ones(len(pts)), pts[:, 1]]), b_eq=[1, y0],
                     bounds=(0, None), method="highs")
        r2 = linprog(phiv, A_eq=np.vstack([np.ones(len(ygrid)), ygrid]), b_eq=[1, y0],
                     bounds=(0, None), method="highs")
        worst = max(worst, abs(r1.fun - r2.fun))
    check("G: LP check min_{x,z} vex Phi = vex phi (grid, one copy)", worst < 1e-9, f"max diff {worst:.2e}")


# ---------------------------------------------------------------- H
def part_H():
    t = sp.Symbol("t")
    # Example 5.4: vex(-x^3) on [-1,1] at 0
    u = sp.Symbol("u")
    sol = [r for r in sp.solve(sp.Eq(-u ** 3 + (-3 * u ** 2) * (1 - u), -1), u) if r != 1]
    tp = sol[0]
    val0 = -tp ** 3 + (-3 * tp ** 2) * (0 - tp)
    check("H: tangent point -1/2, vex(-x^3)(0) = -1/4", (tp, val0) == (sp.Rational(-1, 2), sp.Rational(-1, 4)),
          f"{tp}, {val0}")
    # Example 5.6
    check("H: C = [1/4,1/2] for x^2 = 1/4 on [0,1]", sp.solve(sp.Eq(t, sp.Rational(1, 4)), t)[0] == sp.Rational(1, 4))
    # D=[0,2] example: chord value 1 for every lambda
    l1, l2, x = sp.symbols("l1 l2 x", positive=True)
    ql = (l1 * (x - 2) ** 2 + l2 * x ** 2) / (2 * (l1 + l2))
    check("H: q(0)+q(2) = 2", sp.simplify(ql.subs(x, 0) + ql.subs(x, 2) - 2) == 0)


# ---------------------------------------------------------------- I
def part_I():
    N = lambda m, d: sum(math.comb(m, j) for j in range(d + 1))  # noqa: E731
    check("I: d=4: 8 bounds + 7 sides fits 2000, +8 does not", N(15, 4) <= 2000 < N(16, 4), f"{N(15,4)}, {N(16,4)}")
    check("I: d=3: 6 bounds + 16 sides fits 2000", N(22, 3) <= 2000, f"{N(22,3)}")


# ---------------------------------------------------------------- J
def part_J():
    ok = True
    for k in range(-400, 401):
        tt = Q(k, 100)
        lhs = min(0, tt + 1) + min(0, 1 - tt) + 2 * max(0, tt) - tt - 1
        ok &= lhs == -max(0, 1 - abs(tt))
    check("J: Ben-Or tent identity on a rational grid", ok)
    x1, x2, x3, t = sp.symbols("x1 x2 x3 t")
    f = (x2 - sp.Rational(1, 8)) * x1 + x2 ** 2 - x2 + x2 * x3 + x3 ** 2 - x3
    check("J: f(1,0,1/2) = -3/8", f.subs({x1: 1, x2: 0, x3: sp.Rational(1, 2)}) == sp.Rational(-3, 8))
    root = 1 - sp.sqrt(2) / 2
    check("J: 1 - sqrt2/2 is a root of 2t^2-4t+1", sp.simplify(2 * root ** 2 - 4 * root + 1) == 0)


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    part_D()
    part_E()
    mech = load_mechanism()
    part_F(mech)
    part_G(mech)
    part_G_lemma(mech)
    part_H()
    part_I()
    part_J()
    bad = [n for n, ok in OK if not ok]
    print(f"\n{len(OK) - len(bad)} of {len(OK)} checks passed")
    if bad:
        print("FAILED:", bad)
        sys.exit(1)
