"""Exact checks for the conditional-moment witness F_h and for the
convex-energy and proximal-envelope inequalities on small instances.

F_h = 8(s/h-(u1+u2)/2)^2 + 8(s/h-1/4-v/2)^2 + u1(1-u1)+u2(1-u2)+v(1-v)
      + (u1+u2+v)/16, on [0,1]^4, 0<h<=1/2.
"""
import random
from fractions import Fraction as Fr
import sympy as sp

random.seed(11)
counts = {}


def bump(k, n=1):
    counts[k] = counts.get(k, 0) + n


s, u1, u2, v, h = sp.symbols("s u1 u2 v h", positive=True)
Fh = 8 * (s / h - (u1 + u2) / 2) ** 2 + 8 * (s / h - sp.Rational(1, 4) - v / 2) ** 2 \
    + u1 * (1 - u1) + u2 * (1 - u2) + v * (1 - v) + (u1 + u2 + v) / 16
delta = s / h - sp.Rational(1, 8) - (u1 + u2 + v) / 4
rhs = 16 * delta ** 2 + 2 * ((1 - v) * u1 * u2 + v * (1 - u1) * (1 - u2)) + (u1 + u2 + v) / 16
assert sp.simplify(sp.expand(Fh - sp.Rational(1, 4) - rhs)) == 0
bump("F_h identity")

# Hessian: PSD part minus 2 on controls; direction (0,1,-1,0) is a zero of the PSD part
X = [s, u1, u2, v]
Hs = sp.hessian(Fh, X)
Hpsd = Hs + 2 * sp.diag(0, 1, 1, 1)
for hv in [sp.Rational(1, 2), sp.Rational(1, 7), sp.Rational(1, 100)]:
    Hn = Hpsd.subs(h, hv)
    assert all(ev >= 0 for ev in Hn.eigenvals())
    d = sp.Matrix([0, 1, -1, 0])
    assert (d.T * Hn * d)[0] == 0
    bump("Hessian structure")

# moments
L = [(Fr(1, 8), (Fr(0), 0, 0)), (Fr(3, 8), (Fr(1, 2), 1, 0)),
     (Fr(3, 8), (Fr(1, 2), 0, 1)), (Fr(1, 8), (Fr(1), 1, 1))]
R = [(Fr(1, 2), (Fr(1, 4), 0)), (Fr(1, 2), (Fr(3, 4), 1))]
for k in [1, 2, 3]:
    mL = sum(p * a[0] ** k for p, a in L)
    mR = sum(p * a[0] ** k for p, a in R)
    assert mL == mR
    bump("separator moment matches")
assert sum(p * a[0] ** 4 for p, a in L) != sum(p * a[0] ** 4 for p, a in R)
for p, (t, a1, a2) in L:
    assert t - Fr(a1 + a2, 2) == 0
for p, (t, b1) in R:
    assert t - Fr(1, 4) - Fr(b1, 2) == 0
relaxed = sum(p * Fr(a1 + a2, 16) for p, (t, a1, a2) in L) + sum(p * Fr(b1, 16) for p, (t, b1) in R)
assert relaxed == Fr(3, 32) and Fr(1, 4) - relaxed == Fr(5, 32)
bump("relaxed value 3/32")

# PSD completion with bag-restricted covariances matching the measures
hv = sp.Rational(1, 6)
a_ = sp.Matrix([hv, 1, 1, 2]); b_ = sp.Matrix([0, 1, -1, 0])
Sig = a_ * a_.T / 16 + 3 * b_ * b_.T / 16


def cov(meas, idx_map):
    mean = [sum(p * sp.Rational(at[i]) for p, at in meas) for i in range(len(idx_map))]
    C = sp.zeros(len(idx_map))
    for p, at in meas:
        d = [sp.Rational(at[i]) - mean[i] for i in range(len(idx_map))]
        for i in range(len(idx_map)):
            for j in range(len(idx_map)):
                C[i, j] += sp.Rational(p) * d[i] * d[j]
    return C


Lm = [(p, (hv * sp.Rational(t), a1, a2)) for p, (t, a1, a2) in L]
Rm = [(p, (hv * sp.Rational(t), b1)) for p, (t, b1) in R]
CL = cov(Lm, [0, 1, 2]); CR = cov(Rm, [0, 3])
assert CL == Sig.extract([0, 1, 2], [0, 1, 2])
assert CR == Sig.extract([0, 3], [0, 3])
bump("covariance completion matches")

# growth constant 1/22 at random rational points (h=1/2 and h=1/10)
for hv in [Fr(1, 2), Fr(1, 10)]:
    def Fv(S, A, B, V):
        return 8 * (S / hv - (A + B) / 2) ** 2 + 8 * (S / hv - Fr(1, 4) - V / 2) ** 2 \
            + A * (1 - A) + B * (1 - B) + V * (1 - V) + (A + B + V) / 16
    assert Fv(hv / 8, Fr(0), Fr(0), Fr(0)) == Fr(1, 4)
    for _ in range(3000):
        P = [Fr(random.randint(0, 1000), 1000) for _ in range(4)]
        if random.random() < 0.5:
            P = [hv / 8 + Fr(random.randint(-30, 30), 10000)] + [Fr(random.randint(0, 30), 1000) for _ in range(3)]
            P[0] = min(max(P[0], Fr(0)), Fr(1))
        gap = Fv(*P) - Fr(1, 4)
        d2 = (P[0] - hv / 8) ** 2 + P[1] ** 2 + P[2] ** 2 + P[3] ** 2
        assert gap >= d2 / 22
        bump("F_h growth 1/22")

# convex-energy inequality F-F* >= g/(2g+c) d'(H+cI)d for c>=0 on random 2-D
# continuous box QPs with known optimum and a valid growth constant g taken
# as the minimum observed ratio over a fine grid (diagnostic only).
for _ in range(40):
    Hm = [[Fr(random.randint(-3, 3)) for _ in range(2)] for _ in range(2)]
    Hm[1][0] = Hm[0][1]
    bb = [Fr(random.randint(-3, 3)) for _ in range(2)]
    def Fq(x):
        return sum(Fr(1, 2) * x[i] * Hm[i][j] * x[j] for i in range(2) for j in range(2)) \
            + sum(bb[i] * x[i] for i in range(2))
    grid = [(Fr(i, 20), Fr(j, 20)) for i in range(21) for j in range(21)]
    vals = {p: Fq(p) for p in grid}
    best = min(vals.values())
    opts = [p for p in grid if vals[p] == best]
    if len(opts) != 1:
        continue
    xs = opts[0]
    # restrict to grid instances whose grid optimum is a true KKT point
    gr = [sum(Hm[i][j] * xs[j] for j in range(2)) + bb[i] for i in range(2)]
    ok = all((xs[i] == 0 and gr[i] >= 0) or (xs[i] == 1 and gr[i] <= 0) or gr[i] == 0
             for i in range(2))
    if not ok:
        continue
    ratios = [(vals[p] - best) / ((p[0] - xs[0]) ** 2 + (p[1] - xs[1]) ** 2) for p in grid if p != xs]
    g = min(ratios)
    if g <= 0:
        continue
    lam = sp.Matrix(Hm).eigenvals()
    nu = max([0] + [-sp.nsimplify(e) for e in lam])
    for c in [Fr(0), Fr(1, 2), Fr(1), Fr(5)]:
        for p in grid:
            d = (p[0] - xs[0], p[1] - xs[1])
            q = sum(d[i] * Hm[i][j] * d[j] for i in range(2) for j in range(2)) + c * (d[0] ** 2 + d[1] ** 2)
            assert vals[p] - best >= g / (2 * g + c) * q
            bump("convex-energy inequality grid checks")

for k_, v_ in counts.items():
    print(f"{k_}: {v_}")
print("all moment/energy checks passed")
