"""M4: exact checks of the 1/128 pair-hull example (Report B overlap.tex,
Report A theory/overlap-review.md).

Checks, all in exact rational arithmetic:
  * moments of the two local measures and the point v-bar;
  * lifted values of D, D_L, D_R at v-bar;
  * expansion of D, the cut coefficients and the constant -7/128;
  * violation 1/128 of the cut at v-bar;
  * minimum of D on the cube equals 1/128, unique minimizer (1, 11/16, 1);
  * the covariance / dense-PSD / McCormick remark;
  * the reduced certificate (3) of overlap-review.md;
  * the constrained example of overlap-review.md.
Run: .venv/bin/python M4_example.py
"""
from fractions import Fraction as F
import itertools
import sympy as sp

x, y, z = sp.symbols("x y z")


def expect(measure, f):
    return sum(p * f(*pt) for p, pt in measure)


# ---- local measures -------------------------------------------------------
left = [(F(1, 2), (F(0), F(1, 4))), (F(1, 2), (F(1), F(3, 4)))]          # (x, y)
right = [(F(1, 5), (F(0), F(0))), (F(4, 5), (F(5, 8), F(1)))]            # (y, z)
assert sum(p for p, _ in left) == 1 and sum(p for p, _ in right) == 1

mL = {
    "x": expect(left, lambda a, b: a), "y": expect(left, lambda a, b: b),
    "xx": expect(left, lambda a, b: a * a), "xy": expect(left, lambda a, b: a * b),
    "yy": expect(left, lambda a, b: b * b),
}
mR = {
    "y": expect(right, lambda b, c: b), "z": expect(right, lambda b, c: c),
    "yy": expect(right, lambda b, c: b * b), "yz": expect(right, lambda b, c: b * c),
    "zz": expect(right, lambda b, c: c * c),
}
assert mL["y"] == mR["y"] == F(1, 2)
assert mL["yy"] == mR["yy"] == F(5, 16)
vbar = (mL["x"], mL["y"], mR["z"], mL["xx"], mL["yy"], mR["zz"], mL["xy"], mR["yz"])
assert vbar == (F(1, 2), F(1, 2), F(4, 5), F(1, 2), F(5, 16), F(4, 5), F(3, 8), F(1, 2)), vbar

# ---- D and its expansion --------------------------------------------------
DL = (y - sp.Rational(1, 4) - x / 2) ** 2 + x * (1 - x)
DR = (y - sp.Rational(5, 8) * z) ** 2 + z * (1 - z)
D = sp.expand(DL + DR)
P = sp.Poly(D, x, y, z)
coef = {m: P.coeff_monomial(m) for m in [y**2, y, x*y, y*z, x, x**2, z, z**2, 1, x*z]}
expected = {y**2: 2, y: sp.Rational(-1, 2), x*y: -1, y*z: sp.Rational(-5, 4), x: sp.Rational(5, 4),
            x**2: sp.Rational(-3, 4), z: 1, z**2: sp.Rational(-39, 64), 1: sp.Rational(1, 16), x*z: 0}
assert coef == expected, coef
# cut: D >= 1/128  <=>  (D - const) >= 1/128 - 1/16 = -7/128
assert sp.Rational(1, 128) - coef[1] == sp.Rational(-7, 128)


def lift(poly, v):
    """Linear lift of a quadratic polynomial in (x,y,z) at moment vector v."""
    mx, my, mz, sx, sy, sz, cxy, cyz = [sp.Rational(t.numerator, t.denominator) for t in v]
    Pp = sp.Poly(sp.expand(poly), x, y, z)
    table = {(0, 0, 0): 1, (1, 0, 0): mx, (0, 1, 0): my, (0, 0, 1): mz, (2, 0, 0): sx,
             (0, 2, 0): sy, (0, 0, 2): sz, (1, 1, 0): cxy, (0, 1, 1): cyz}
    total = 0
    for mon, c in Pp.terms():
        if mon not in table:
            raise ValueError("monomial outside the sparse lift: %s" % (mon,))
        total += c * table[mon]
    return sp.nsimplify(total)


assert lift(DL, vbar) == 0 and lift(DR, vbar) == 0 and lift(D, vbar) == 0
cut_lhs = D - coef[1]
assert lift(cut_lhs, vbar) == sp.Rational(-1, 16)
violation = sp.Rational(-7, 128) - lift(cut_lhs, vbar)
assert violation == sp.Rational(1, 128), violation

# ---- exact minimum of D on the cube --------------------------------------
# For fixed y, D is separable in x and z with negative square coefficients,
# hence concave in each leaf: the minimum over [0,1]^2 is at a binary pair.
assert sp.Poly(D, x).coeff_monomial(x**2) == sp.Rational(-3, 4)
assert sp.Poly(D, z).coeff_monomial(z**2) == sp.Rational(-39, 64)
assert sp.Poly(D, x, z).coeff_monomial(x*z) == 0
best = []
for xv, zv in itertools.product([0, 1], repeat=2):
    q = sp.expand(D.subs({x: xv, z: zv}))
    # quadratic 2y^2+..., minimize on [0,1]
    cands = [sp.Integer(0), sp.Integer(1)]
    st = sp.solve(sp.diff(q, y), y)[0]
    if 0 <= st <= 1:
        cands.append(st)
    val, arg = min((q.subs(y, c), c) for c in cands)
    best.append((val, (xv, arg, zv)))
best.sort()
assert best[0] == (sp.Rational(1, 128), (1, sp.Rational(11, 16), 1)), best
assert best[1][0] > sp.Rational(1, 128)          # unique minimizing binary pair
assert sorted(b[0] for b in best) == [sp.Rational(1, 128), sp.Rational(1, 32),
                                      sp.Rational(9, 128), sp.Rational(9, 32)]

# ---- global representing measure impossible -------------------------------
mx, my, mz, sx, sy, sz, cxy, cyz = vbar
assert mx - sx == 0 and mz - sz == 0                       # E x(1-x) = E z(1-z) = 0
assert lift((y - sp.Rational(1, 4) - x / 2) ** 2, vbar) == 0
assert lift((y - sp.Rational(5, 8) * z) ** 2, vbar) == 0

# ---- dense PSD / McCormick remark ----------------------------------------
var_x, var_y, var_z = sx - mx**2, sy - my**2, sz - mz**2
cov_xy, cov_yz = cxy - mx * my, cyz - my * mz
assert (var_x, var_y, var_z) == (F(1, 4), F(1, 16), F(4, 25))
assert cov_xy**2 == var_x * var_y and cov_xy > 0          # saturated, positive
assert cov_yz**2 == var_y * var_z and cov_yz > 0
w = sp.Symbol("w")
M = sp.Matrix([[1, mx, my, mz], [mx, sx, cxy, w], [my, cxy, sy, cyz], [mz, w, cyz, sz]])
M = M.applyfunc(lambda e: sp.nsimplify(e))
# null vectors forced by the two zero squares
uL = sp.Matrix([-sp.Rational(1, 4), -sp.Rational(1, 2), 1, 0])
uR = sp.Matrix([0, 0, 1, -sp.Rational(5, 8)])
assert (uL.T * M * uL)[0] == 0 and (uR.T * M * uR)[0] == 0
# PSD + zero quadratic form => M u = 0, which pins w:
sol_L = sp.solve((M * uL)[3], w)
sol_R = sp.solve((M * uR)[1], w)
assert sol_L == sol_R == [sp.Rational(3, 5)], (sol_L, sol_R)
M35 = M.subs(w, sp.Rational(3, 5))
# exact PSD test: every principal minor is nonnegative
for r in range(1, 5):
    for idx in itertools.combinations(range(4), r):
        assert M35.extract(list(idx), list(idx)).det() >= 0
assert M35.rank() == 2
# uniqueness: for w != 3/5, v = uL - t e4 with t = (M uL)_4 / M_44 gives
# v^T M v = -(M uL)_4^2 / M_44 < 0, so no other completion is PSD.
e4 = sp.Matrix([0, 0, 0, 1])
for wv in [sp.Rational(3, 5) + sp.Rational(1, 1000), sp.Rational(3, 5) - sp.Rational(1, 1000), 0, 1]:
    Mw = M.subs(w, wv)
    g = (Mw * uL)[3]
    tt = g / Mw[3, 3]
    v = uL - tt * e4
    assert (v.T * Mw * v)[0] == -g**2 / Mw[3, 3] < 0
# covariance of x,z forced to 1/5 and E[xz] = 3/5 > E[x] = 1/2
assert sp.Rational(3, 5) - mx * mz == sp.Rational(1, 5)
assert sp.Rational(3, 5) > mx            # violates McCormick  w <= m_x
assert sp.Rational(3, 5) <= mz and sp.Rational(3, 5) >= 0 and sp.Rational(3, 5) >= mx + mz - 1

# ---- reduced certificate (3) of overlap-review.md ------------------------
Dt = sp.expand((y - sp.Rational(1, 4) - x / 2) ** 2 + (y - sp.Rational(5, 8) * z) ** 2
               + sp.Rational(1, 4) * x * (1 - x) + sp.Rational(25, 64) * z * (1 - z))
Dt_claim = 2*y**2 - y/2 - x*y - sp.Rational(5, 4)*y*z + sp.Rational(1, 16) + x/2 + sp.Rational(25, 64)*z
assert sp.expand(Dt - Dt_claim) == 0
assert sp.Poly(Dt, x).degree() == 1 and sp.Poly(Dt, z).degree() == 1
assert lift(Dt, vbar) == 0
vals = []
for xv, zv in itertools.product([0, 1], repeat=2):
    q = sp.expand(Dt.subs({x: xv, z: zv}))
    st = sp.solve(sp.diff(q, y), y)[0]
    cands = [c for c in (sp.Integer(0), sp.Integer(1), st) if 0 <= c <= 1]
    vals.append(min(q.subs(y, c) for c in cands))
assert min(vals) == sp.Rational(1, 128)

# ---- constrained example of overlap-review.md ----------------------------
SL = [(0, F(0)), (0, F(1)), (1, F(1, 4)), (1, F(3, 4))]            # (x, y)
SR = [(F(0), 0), (F(1), 0), (F(1, 3), 1), (F(2, 3), 1)]            # (y, z)
for xv, yv in SL:
    assert xv * xv == xv and yv * yv - yv + F(3, 16) * xv == 0
for yv, zv in SR:
    assert zv * zv == zv and yv * yv - yv + F(2, 9) * zv == 0
# completeness of the finite sets: each equation is a quadratic in y
assert sorted(sp.solve(y**2 - y + sp.Rational(3, 16), y)) == [sp.Rational(1, 4), sp.Rational(3, 4)]
assert sorted(sp.solve(y**2 - y + sp.Rational(2, 9), y)) == [sp.Rational(1, 3), sp.Rational(2, 3)]
common = sorted({yv for _, yv in SL} & {yv for yv, _ in SR})
assert common == [0, 1]
muL = [F(1, 6), F(1, 6), F(1, 3), F(1, 3)]
muR = [F(7, 32), F(7, 32), F(9, 32), F(9, 32)]
assert sum(muL) == 1 and sum(muR) == 1
EyL = [sum(p * pt[1] ** j for p, pt in zip(muL, SL)) for j in range(5)]
EyR = [sum(p * pt[0] ** j for p, pt in zip(muR, SR)) for j in range(5)]
assert EyL[:4] == EyR[:4] == [1, F(1, 2), F(3, 8), F(5, 16)]
assert EyL[4] == F(35, 128) and EyR[4] == F(5, 18)
assert sum(p * pt[0] for p, pt in zip(muL, SL)) == F(2, 3)
assert sum(p * pt[0] * pt[1] for p, pt in zip(muL, SL)) == F(1, 3)
assert sum(p * pt[1] for p, pt in zip(muR, SR)) == F(9, 16)
assert sum(p * pt[0] * pt[1] for p, pt in zip(muR, SR)) == F(9, 32)
# q = y(1-y): q^2 = (3/16) q on S_L and q^2 = (2/9) q on S_R
for _, yv in SL:
    q = yv * (1 - yv)
    assert q * q == F(3, 16) * q
for yv, _ in SR:
    q = yv * (1 - yv)
    assert q * q == F(2, 9) * q

print("M4_example: all exact checks passed (moments, v-bar, cut -7/128, violation 1/128,"
      " min 1/128 at (1,11/16,1), PSD completion w=3/5 unique, McCormick w<=m_x violated,"
      " reduced certificate, constrained example).")
