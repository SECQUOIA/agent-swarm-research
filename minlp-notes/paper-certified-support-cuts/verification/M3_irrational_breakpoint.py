"""M3: depth-two trees have irrational breakpoints in conditional value functions.

P3 example (box [0,1]^3, path x1 - x2 - x3):
    f(x) = (x2 - 1/8) x1 + x2^2 - x2 + x2 x3 + x3^2 - x3.
Rooted at x3, the message of the subtree {x1, x2} is
    mu(t) = min_{x1,x2 in [0,1]} (x2 - 1/8) x1 + x2^2 - x2 + t x2,
which has a breakpoint at t = 1 - sqrt(2)/2 (irrational), while min f = -3/8.
P4 example: f4 = f + (x3 - 1/8) x4 has the same message on both inner edges,
so every choice of root has a depth-two node with an irrational breakpoint.
All computations are exact (sympy for algebraic numbers, Fractions for KKT).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys
sys.dont_write_bytecode = True
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-convexification/theory'))
from fractions import Fraction as Fr
from itertools import combinations
import sympy as sp

t = sp.symbols("t", real=True)
x1, x2 = sp.symbols("x1 x2", real=True)
F2 = (x2 - sp.Rational(1, 8)) * x1 + x2**2 - x2 + t * x2


def box_candidates(expr, xs):
    """All parametric KKT candidates of a 2-variable box QP on [0,1]^2.

    Returns (value(t), validity condition) pairs. Faces: 4 vertices, 4 edges
    (stationary point if edge curvature > 0), interior (if Hessian PD).
    """
    out = []
    a, b = xs
    for va in (0, 1):
        for vb in (0, 1):
            out.append((sp.expand(expr.subs({a: va, b: vb})), sp.true))
    for fixed, free in ((a, b), (b, a)):
        for v in (0, 1):
            g = sp.expand(expr.subs(fixed, v))
            curv = sp.Poly(g, free).coeff_monomial(free**2)
            if curv > 0:
                s = sp.solve(sp.diff(g, free), free)[0]
                out.append((sp.expand(g.subs(free, s)), sp.And(s >= 0, s <= 1)))
    Hm = sp.hessian(expr, xs)
    if Hm[0, 0] > 0 and Hm.det() > 0:
        sol = sp.solve([sp.diff(expr, a), sp.diff(expr, b)], xs, dict=True)[0]
        out.append((sp.expand(expr.subs(sol)), sp.And(*[(sol[v] >= 0) & (sol[v] <= 1) for v in xs])))
    return out


def lower_envelope_on(cands, lo, hi):
    """Exact min of candidate functions on [lo, hi]: returns [(a, b, poly)]."""
    pts = {sp.nsimplify(lo), sp.nsimplify(hi)}
    polys = [c for c, _ in cands]
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            diff = sp.expand(polys[i] - polys[j])
            if diff != 0:
                for r in sp.solve(diff, t):
                    if r.is_real and lo < r < hi:
                        pts.add(sp.simplify(r))
    for c, cond in cands:   # validity boundaries
        atoms = [cond] if isinstance(cond, sp.core.relational.Relational) else getattr(cond, "args", ())
        for atom in atoms:
            if isinstance(atom, sp.core.relational.Relational):
                for r in sp.solve(sp.Eq(atom.lhs, atom.rhs), t):
                    if lo < r < hi:
                        pts.add(r)
    pts = sorted(pts, key=lambda v: sp.N(v, 50))
    pieces = []
    for a, b in zip(pts, pts[1:]):
        mid = sp.nsimplify(sp.Rational(sp.floor(sp.N((a + b) / 2, 30) * 10**12), 10**12))
        assert a < mid < b
        valid = [c for c, cond in cands if bool(cond.subs(t, mid))]
        best = min(valid, key=lambda c: c.subs(t, mid))
        if pieces and sp.expand(pieces[-1][2] - best) == 0:
            pieces[-1] = (pieces[-1][0], b, best)
        else:
            pieces.append((a, b, best))
    return pieces


def kkt_box_min(n, H, g):
    """Exact min of 0.5 x'Hx + g'x on [0,1]^n by face enumeration."""
    best = None
    rows = [([Fr(int(i == j)) for j in range(n)], Fr(1)) for i in range(n)] + \
           [([Fr(-int(i == j)) for j in range(n)], Fr(0)) for i in range(n)]
    for k in range(n + 1):
        for act in combinations(range(2 * n), k):
            M = [list(map(Fr, H[i])) + [rows[r][0][i] for r in act] for i in range(n)]
            M += [rows[r][0] + [Fr(0)] * k for r in act]
            rhs = [-Fr(v) for v in g] + [rows[r][1] for r in act]
            A = [row + [v] for row, v in zip(M, rhs)]
            m = len(A)
            ok = True
            for col in range(m):
                piv = next((r for r in range(col, m) if A[r][col] != 0), None)
                if piv is None:
                    ok = False
                    break
                A[col], A[piv] = A[piv], A[col]
                pv = A[col][col]
                A[col] = [v / pv for v in A[col]]
                for r in range(m):
                    if r != col and A[r][col] != 0:
                        fac = A[r][col]
                        A[r] = [v - fac * w for v, w in zip(A[r], A[col])]
            if not ok:
                continue
            x = [A[i][-1] for i in range(n)]
            if all(0 <= v <= 1 for v in x):
                val = sum(Fr(g[i]) * x[i] for i in range(n)) + Fr(1, 2) * sum(
                    Fr(H[i][j]) * x[i] * x[j] for i in range(n) for j in range(n))
                if best is None or val < best[0]:
                    best = (val, x)
    return best


def main():
    cands = box_candidates(F2, (x1, x2))
    pieces = lower_envelope_on(cands, 0, 1)
    print("mu(t) on [0,1]:")
    for a, b, p in pieces:
        print(f"   [{a}, {b}]: {sp.factor(p)}")
    breaks = [b for (_, b, _) in pieces[:-1]]
    assert len(breaks) == 1
    tau = sp.nsimplify(breaks[0])
    assert sp.simplify(tau - (1 - sp.sqrt(2) / 2)) == 0
    mp = sp.minimal_polynomial(tau, t)
    assert sp.degree(mp, t) == 2 and sp.Poly(mp, t).is_irreducible
    print(f"breakpoint tau = {tau}, minimal polynomial {mp} (irreducible over Q, so tau is irrational)")
    # the two arcs meeting at tau and their difference (defining quadratic)
    left, right = pieces[0][2], pieces[1][2]
    assert sp.expand(left + (1 - t)**2 / 4) == 0 and right == sp.Rational(-1, 8)
    # envelope interpretation: phi(x) = x^2 - x + min(0, x - 1/8); tangent from (0,-1/8)
    u = sp.sqrt(sp.Rational(1, 8))
    sigma = 2 * u - 1
    assert sp.simplify(tau - (-sigma)) == 0
    print(f"envelope tangent point u = {u}, slope sigma = {sp.simplify(sigma)}, tau = -sigma/s with s = 1")

    # Global minimum of P3 (root terms x3^2 - x3) is rational.
    H3 = [[0, 1, 0], [1, 2, 1], [0, 1, 2]]
    g3 = [Fr(-1, 8), -1, -1]
    val3, x3 = kkt_box_min(3, H3, g3)
    assert val3 == Fr(-3, 8)
    # and equals min over t of t^2 - t + mu(t), computed piecewise in sympy
    root_vals = []
    for a, b, p in pieces:
        h = sp.expand(t**2 - t + p)
        cs = [a, b] + [r for r in sp.solve(sp.diff(h, t), t) if a < r < b and sp.diff(h, t, 2) > 0]
        root_vals += [sp.nsimplify(sp.simplify(h.subs(t, c))) for c in cs]
    assert min(root_vals, key=lambda v: sp.N(v, 50)) == sp.Rational(-3, 8)
    print(f"P3 global min = {val3} at x = {[str(v) for v in x3]} (KKT enumeration); "
          f"min_t [t^2 - t + mu(t)] = -3/8")
    from quadratic_star import support_star
    c = {(1, 1, 0): 1, (1, 0, 0): Fr(-1, 8), (0, 2, 0): 1, (0, 1, 0): -1,
         (0, 1, 1): 1, (0, 0, 2): 1, (0, 0, 1): -1}
    star = support_star(((0, 1),) * 3, (), c, center=1)
    assert Fr(star["bound"]) == Fr(-3, 8)
    print(f"rooted at the middle (a star), the inherited oracle returns {star['bound']} with "
          f"rational center breakpoints {[p['interval'] for p in star['pieces']]}")

    # P4: f4 = f + (x3 - 1/8) x4 with x3^2 - x3 kept; symmetric under reversal.
    H4 = [[0, 1, 0, 0], [1, 2, 1, 0], [0, 1, 2, 1], [0, 0, 1, 0]]
    g4 = [Fr(-1, 8), -1, -1, Fr(-1, 8)]
    val4, x4 = kkt_box_min(4, H4, g4)
    s = sp.symbols("s", real=True)
    x3s, x4s = sp.symbols("x3 x4", real=True)
    mirror = (x3s - sp.Rational(1, 8)) * x4s + x3s**2 - x3s + s * x3s
    pieces_m = lower_envelope_on([(c.subs(s, t), cond.subs(s, t)) for c, cond in
                                  box_candidates(mirror, (x4s, x3s))], 0, 1)
    assert [sp.simplify(b - tau) == 0 for (_, b, _) in pieces_m[:-1]] == [True]
    print(f"P4 global min = {val4} at x = {[str(v) for v in x4]}; the messages {{x1,x2}}->x3 and "
          f"{{x3,x4}}->x2 both break at {tau}, so every rooting has an irrational breakpoint")


if __name__ == "__main__":
    main()
