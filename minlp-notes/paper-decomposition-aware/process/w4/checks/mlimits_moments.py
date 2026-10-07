"""M-limits checks for appendix-moments.tex: Prop lim:prop:moments and Remark lim:rem:moments."""
from fractions import Fraction as Fr
from itertools import product, combinations
from math import comb
import random
import sympy as sp

random.seed(5)
ok = True


def check(c, msg):
    global ok
    if not c:
        ok = False
        print("FAIL:", msg)


def build(r, h):
    """Return function F(state, controls) with state=(s, y1..y_{r-1}, z1..z_{r-1}),
    controls=(u1..ur, v1..v_{r-1}), exact Fractions."""
    lam = Fr(1, 8 * r)

    def F(s, y, z, u, v):
        yy = [Fr(0)] + list(y) + [s]
        zz = [Fr(0)] + list(z)
        rho = [(yy[i] - yy[i - 1]) / h - u[i - 1] for i in range(1, r + 1)]
        rhop = [(zz[j] - zz[j - 1]) / h - v[j - 1] for j in range(1, r)]
        rhop.append((s - zz[r - 1]) / h - Fr(1, 2))
        return 2 * r * (sum(t * t for t in rho) + sum(t * t for t in rhop)) + sum(
            t * (1 - t) for t in u) + sum(t * (1 - t) for t in v) + lam * (sum(u) + sum(v))

    def zeta0(u, v):
        c = list(u) + [Fr(-1, 2)] + [-v[j] for j in range(r - 2, -1, -1)]
        cbar = sum(c)
        nodes = [Fr(0)]
        part = Fr(0)
        for k in range(1, 2 * r + 1):
            part += c[k - 1]
            nodes.append(part - Fr(k, 2 * r) * cbar)
        return nodes, cbar

    def nodes_to_state(nodes):
        s = h * nodes[r]
        y = [h * nodes[k] for k in range(1, r)]
        z = [h * nodes[2 * r - j] for j in range(1, r)]  # zeta_{r+l} = z_{r-l}/h
        return s, y, z

    return F, zeta0, nodes_to_state, lam


for r in range(1, 5):
    h = Fr(1, 4 * r) if r % 2 else Fr(1, 8 * r)
    F, zeta0, n2s, lam = build(r, h)
    gr = lam / (1 + 8 * (2 * r - 1) ** 2)
    s0, y0, z0 = n2s(zeta0([Fr(0)] * r, [Fr(0)] * (r - 1))[0])
    for _ in range(300):
        u = [Fr(random.randint(0, 20), 20) for _ in range(r)]
        v = [Fr(random.randint(0, 20), 20) for _ in range(r - 1)]
        nodes, cbar = zeta0(u, v)
        check(nodes[2 * r] == 0, "last node zero")
        check(all(abs(t) <= 2 * r for t in nodes), "nodes within [-2r,2r]")
        s, y, z = n2s(nodes)
        ub, vb = sum(u), sum(v)
        e2u = sum(u[i] * u[j] for i, j in combinations(range(r), 2))
        e2v = sum(v[i] * v[j] for i, j in combinations(range(r - 1), 2))
        Ups = e2u + e2v - ub * vb + vb
        Psi = cbar ** 2 + sum(t * (1 - t) for t in u) + sum(t * (1 - t) for t in v) + lam * (ub + vb)
        check(F(s, y, z, u, v) == Psi, "F at zeta0 = Psi")
        check(Psi - Fr(1, 4) == 2 * Ups + lam * (ub + vb), "Psi identity")
        # random delta
        delta = [Fr(0)] + [Fr(random.randint(-10, 10), 10) for _ in range(2 * r - 1)] + [Fr(0)]
        nd = [nodes[k] + delta[k] for k in range(2 * r + 1)]
        s2, y2, z2 = n2s(nd)
        lhs = F(s2, y2, z2, u, v)
        rhs = Psi + 2 * r * sum((delta[k] - delta[k - 1]) ** 2 for k in range(1, 2 * r + 1))
        check(lhs == rhs, "split identity momsplit")
        # growth (only meaningful if states feasible)
        if all(-1 <= t <= 1 for t in [s2] + y2 + z2):
            d2 = (s2 - s0) ** 2 + sum((a - b) ** 2 for a, b in zip(y2, y0)) + sum(
                (a - b) ** 2 for a, b in zip(z2, z0)) + sum(t * t for t in u) + sum(t * t for t in v)
            check(lhs - Fr(1, 4) >= gr * d2, "growth g_r")
    # vertex values of Upsilon
    for u in product([0, 1], repeat=r):
        for v in product([0, 1], repeat=r - 1):
            a, b = sum(u), sum(v)
            e2u = comb(a, 2)
            e2v = comb(b, 2)
            check(e2u + e2v - a * b + b == Fr((a - b) * (a - b - 1), 2), "vertex Upsilon")
    # witness: parity laws, moments, value
    pi = [Fr(comb(2 * r, 2 * i), 2 ** (2 * r - 1)) for i in range(r + 1)]
    pip = [Fr(comb(2 * r, 2 * j + 1), 2 ** (2 * r - 1)) for j in range(r)]
    check(sum(pi) == 1 and sum(pip) == 1, "laws sum to 1")
    for al in range(0, 2 * r + 1):
        mL = sum(pi[i] * (h * i) ** al for i in range(r + 1))
        mR = sum(pip[j] * (h * (j + Fr(1, 2))) ** al for j in range(r))
        if al < 2 * r:
            check(mL == mR, f"moment {al} differs r={r}")
        else:
            check(mL != mR, f"moment {al} equal r={r}")
    val = sum(pi[i] * lam * i for i in range(r + 1)) + sum(pip[j] * lam * j for j in range(r))
    check(val == Fr(1, 4) - Fr(2 * r + 1, 16 * r), "witness value")
    # residuals vanish on supports and states in [0, r h]
    for i in range(r + 1):
        u = [Fr(1)] * i + [Fr(0)] * (r - i)
        yy = [h * sum(u[:k]) for k in range(1, r)]
        s = h * i
        check(all(0 <= t <= r * h for t in yy + [s]), "left atoms in [0,rh]")
    for j in range(r):
        v = [Fr(1)] * j + [Fr(0)] * (r - 1 - j)
        zz_ = [h * sum(v[:k]) for k in range(1, r)]
        s = h * (j + Fr(1, 2))
        check(all(0 <= t <= r * h for t in zz_ + [s]), "right atoms in [0,rh]")
        check((s - (zz_[-1] if r > 1 else 0)) / h - Fr(1, 2) == 0, "rho'_r = 0")
print("moments: r=1..4 checked")

# Remark lim:rem:moments
s, u1, u2, v, hh = sp.symbols('s u1 u2 v h', positive=True)
Fh = 8 * (s / hh - (u1 + u2) / 2) ** 2 + 8 * (s / hh - sp.Rational(1, 4) - v / 2) ** 2 \
    + u1 * (1 - u1) + u2 * (1 - u2) + v * (1 - v) + (u1 + u2 + v) / 16
dl = s / hh - sp.Rational(1, 8) - (u1 + u2 + v) / 4
rhs = sp.Rational(1, 4) + 16 * dl ** 2 + 2 * ((1 - v) * u1 * u2 + v * (1 - u1) * (1 - u2)) + (u1 + u2 + v) / 16
check(sp.expand(Fh - rhs) == 0, "remark identity")
Hm = sp.hessian(Fh, [s, u1, u2, v])
chi1 = sp.Matrix([1 / hh, -sp.Rational(1, 2), -sp.Rational(1, 2), 0])
chi2 = sp.Matrix([1 / hh, 0, 0, -sp.Rational(1, 2)])
es = sp.Matrix([1, 0, 0, 0])
check(sp.simplify(Hm + 2 * sp.eye(4) - 16 * chi1 * chi1.T - 16 * chi2 * chi2.T - 2 * es * es.T)
      == sp.zeros(4, 4), "remark Hessian")
check(sp.simplify(Hm[0, 0] - 32 / hh ** 2) == 0, "L=32/h^2")
# growth g = 1/22 at random points
for _ in range(400):
    H_ = Fr(random.randint(1, 50), 100)
    U1, U2, V = (Fr(random.randint(0, 20), 20) for _ in range(3))
    S = Fr(random.randint(0, 100), 100)
    val = 8 * (S / H_ - (U1 + U2) / 2) ** 2 + 8 * (S / H_ - Fr(1, 4) - V / 2) ** 2 + U1 * (1 - U1) \
        + U2 * (1 - U2) + V * (1 - V) + (U1 + U2 + V) / 16
    d2 = (S - H_ / 8) ** 2 + U1 ** 2 + U2 ** 2 + V ** 2
    check(val - Fr(1, 4) >= d2 / 22, "remark growth 1/22")
# measures
L = [(Fr(1, 8), (Fr(0), 0, 0)), (Fr(3, 8), (Fr(1, 2), 1, 0)), (Fr(3, 8), (Fr(1, 2), 0, 1)),
     (Fr(1, 8), (Fr(1), 1, 1))]
R = [(Fr(1, 2), (Fr(1, 4), 0)), (Fr(1, 2), (Fr(3, 4), 1))]
mom = lambda M, k: sum(p * a[0] ** k for p, a in M)
check([mom(L, k) for k in range(1, 5)] == [Fr(1, 2), Fr(5, 16), Fr(7, 32), Fr(11, 64)], "left moments")
check([mom(R, k) for k in range(1, 5)] == [Fr(1, 2), Fr(5, 16), Fr(7, 32), Fr(41, 256)], "right moments")
valL = sum(p * (Fr(a[1] + a[2], 16)) for p, a in L)
valR = sum(p * Fr(a[1], 16) for p, a in R)
check(valL + valR == Fr(3, 32), "remark value 3/32")
# PSD completion and McCormick; work in variables (t=s/h, u1, u2, v), then s = h t
mu = [Fr(1, 2), Fr(1, 2), Fr(1, 2), Fr(1, 2)]  # mean of t, u1, u2, v
a = [1, 1, 1, 2]
b = [0, 1, -1, 0]
Cov = [[Fr(a[i] * a[j], 16) + Fr(3 * b[i] * b[j], 16) for j in range(4)] for i in range(4)]
Ex2 = [[Cov[i][j] + mu[i] * mu[j] for j in range(4)] for i in range(4)]
# bag consistency: left bag (t,u1,u2) and right bag (t,v)
def E2(M, idx):
    return sum(p * a_[idx[0]] * a_[idx[1]] for p, a_ in M)
Lm = [(p, (a_[0], a_[1], a_[2])) for p, a_ in L]
check(all(Ex2[i][j] == sum(p * Fr(x[i]) * Fr(x[j]) for p, x in Lm) for i in range(3) for j in range(3)),
      "completion matches left bag")
Rm = [(p, (x[0], x[1])) for p, x in R]
idx = {0: 0, 3: 1}
check(all(Ex2[i][j] == sum(p * Fr(x[idx[i]]) * Fr(x[idx[j]]) for p, x in Rm) for i in (0, 3) for j in (0, 3)),
      "completion matches right bag")
check(all(Ex2[i][0] * 1 == sum(p * Fr(x[i]) for p, x in Lm) * 0 + mu[i] * mu[0] + Cov[i][0] for i in range(3)),
      "sanity")
for tmax in [Fr(2), Fr(1)]:  # s in [0, 2h] <=> t in [0,2]; also [0,h]
    lo = [Fr(0)] * 4
    hi = [tmax, Fr(1), Fr(1), Fr(1)]
    for i in range(4):
        for j in range(4):
            Y = Ex2[i][j]
            # McCormick: (x_i - lo_i)(x_j - lo_j) >= 0, (hi_i - x_i)(hi_j - x_j) >= 0,
            # (x_i - lo_i)(hi_j - x_j) >= 0
            c1 = Y - lo[j] * mu[i] - lo[i] * mu[j] + lo[i] * lo[j]
            c2 = hi[i] * hi[j] - hi[i] * mu[j] - hi[j] * mu[i] + Y
            c3 = hi[j] * mu[i] - Y - lo[i] * hi[j] + lo[i] * mu[j]
            check(c1 >= 0 and c2 >= 0 and c3 >= 0, f"McCormick {i},{j} tmax={tmax}")
tri = Ex2[1][2] + mu[3] - Ex2[1][3] - Ex2[2][3]
check(tri == Fr(-1, 8), "triangle pseudo-expectation -1/8")
ev = sp.Matrix(4, 4, lambda i, j: Cov[i][j]).eigenvals()
check(all(e >= 0 for e in ev), "Cov PSD")
print("ALL OK" if ok else "SOME FAILURES")
