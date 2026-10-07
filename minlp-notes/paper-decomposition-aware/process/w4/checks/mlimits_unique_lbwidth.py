"""M-limits checks: Prop lim:prop:unique, Cor lim:cor:nopolylog, Prop prop:lbwidth,
Prop lim:prop:constraints, Prop lim:prop:oracle counting.  Exact arithmetic."""
from fractions import Fraction as Fr
from itertools import product, combinations
import random
import sympy as sp

random.seed(20261003)
ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)


# ---------------- Prop lim:prop:unique ----------------
def unique_instance(a, a0):
    m = len(a)
    A = sum(a)
    na2 = sum(t * t for t in a)
    lam = Fr(1, m * 2 ** (m + 1))

    def F(x, y):  # y = (y1..y_{m-1})
        yy = [Fr(0)] + list(y) + [Fr(a0)]
        s = sum((yy[i] - yy[i - 1] - a[i - 1] * x[i - 1]) ** 2 for i in range(1, m + 1))
        s += na2 * sum(xi * (1 - xi) for xi in x)
        s += lam * sum(2 ** i * x[i] for i in range(m))
        return s

    def sigma(x):
        e = sum(a[i] * x[i] for i in range(m)) - a0
        return [sum(a[j] * x[j] for j in range(k)) - Fr(k, m) * e for k in range(1, m)]

    def Phi(x):
        e = sum(a[i] * x[i] for i in range(m)) - a0
        return Fr(e * e, m) + na2 * sum(xi * (1 - xi) for xi in x) + lam * sum(
            2 ** i * x[i] for i in range(m))

    verts = list(product([0, 1], repeat=m))
    vals = {v: Phi([Fr(t) for t in v]) for v in verts}
    check(len(set(vals.values())) == len(verts), f"vertex values not distinct {a},{a0}")
    xs = min(verts, key=lambda v: vals[v])
    phis = vals[xs]
    for v in verts:
        if v != xs:
            check(vals[v] - phis >= lam, f"gap<lambda {a},{a0},{v}")
    yes = any(sum(a[i] * v[i] for i in range(m)) == a0 for v in verts)
    if yes:
        check(sum(a[i] * xs[i] for i in range(m)) == a0, "x* not a solution on yes")
        check(phis < Fr(1, 2 * m), "OPT >= 1/(2m) on yes")
    else:
        check(phis >= Fr(1, m), "OPT < 1/m on no")
    g = lam / (m * (1 + 2 * (m - 1) * na2))
    xstar = [Fr(t) for t in xs]
    ystar = sigma(xstar)
    check(all(-A <= t <= 2 * A for t in ystar), "sigma(x*) outside box")
    check(F(xstar, ystar) == phis, "F(z*) != Phi*")
    # growth at random rational points, plus delta=0 points (y = sigma(x))
    for trial in range(300):
        x = [Fr(random.randint(0, 1000), 1000) for _ in range(m)]
        if trial % 3 == 0:  # near x*
            x = [min(1, max(0, xstar[i] + Fr(random.randint(-30, 30), 1000))) for i in range(m)]
        if trial % 2 == 0:
            y = sigma(x)
        else:
            y = [Fr(random.randint(-A * 100, 2 * A * 100), 100) for _ in range(m - 1)]
        check(all(-A <= t <= 2 * A for t in sigma(x)), "sigma(x) outside box")
        d2 = sum((x[i] - xstar[i]) ** 2 for i in range(m)) + sum(
            (y[k] - ystar[k]) ** 2 for k in range(m - 1))
        check(F(x, y) - phis >= g * d2, f"growth fails {a},{a0}")
        # split identity
        delta = [y[k] - sigma(x)[k] for k in range(m - 1)]
        dd = [Fr(0)] + delta + [Fr(0)]
        check(F(x, y) == Phi(x) + sum((dd[i] - dd[i - 1]) ** 2 for i in range(1, m + 1)),
              "split identity")
    kappa_bound = 2 ** (m + 3) * m * m * (1 + 2 * m * na2)
    check(4 / g <= kappa_bound, "kappa bound")
    return yes


ny = nn = 0
for _ in range(60):
    m = random.randint(2, 5)
    a = [random.randint(1, 9) for _ in range(m)]
    a0 = random.randint(0, sum(a))
    if unique_instance(a, a0):
        ny += 1
    else:
        nn += 1
print("unique: instances yes/no =", ny, nn)

# Hessian of Phi concave, coordinate second derivatives (symbolic, m=3)
m = 3
xs_ = sp.symbols('x1:4')
ys_ = sp.symbols('y1:3')
a_ = sp.symbols('a1:4', positive=True)
a0_ = sp.Symbol('a0')
lam_ = sp.Rational(1, m * 2 ** (m + 1))
na2_ = sum(t ** 2 for t in a_)
yy = [0] + list(ys_) + [a0_]
Fs = sum((yy[i] - yy[i - 1] - a_[i - 1] * xs_[i - 1]) ** 2 for i in range(1, m + 1)) \
    + na2_ * sum(t * (1 - t) for t in xs_) + lam_ * sum(2 ** i * xs_[i] for i in range(m))
check(all(sp.simplify(sp.diff(Fs, y, 2) - 4) == 0 for y in ys_), "d2F/dy2 != 4")
check(all(sp.simplify(sp.diff(Fs, xs_[i], 2) - (2 * a_[i] ** 2 - 2 * na2_)) == 0
          for i in range(m)), "d2F/dx2")

# ---------------- Prop prop:lbwidth ----------------
def lbwidth(nv, E):
    def Psi(x):
        return 2 ** nv * (-sum(x) + 2 * sum(x[i] * x[j] for i, j in E)) + sum(
            2 ** i * x[i] for i in range(nv)) + Fr(1, 2 * nv) * sum(t * t - t for t in x)

    def Psi0(x):
        return 2 ** nv * (-sum(x) + 2 * sum(x[i] * x[j] for i, j in E)) + sum(
            2 ** i * x[i] for i in range(nv))

    verts = list(product([0, 1], repeat=nv))
    vals = {v: Psi([Fr(t) for t in v]) for v in verts}
    check(len(set(vals.values())) == len(verts), "lbwidth: binary values not distinct")
    xs = min(verts, key=lambda v: vals[v])
    ps = vals[xs]
    alpha = max(sum(v) for v in verts if all(not (v[i] and v[j]) for i, j in E))
    check(ps // 2 ** nv == -alpha, "floor(Psi*/2^n) != -alpha")
    for t in [Fr(-1, 2), Fr(1, 2), Fr(1, 3), Fr(-1, 3)]:
        check((ps + t) // 2 ** nv == -alpha, "decoding within 1/2 fails")
    for _ in range(80):
        x = [Fr(random.randint(0, 60), 60) for _ in range(nv)]
        d2 = sum((x[i] - xs[i]) ** 2 for i in range(nv))
        check(Psi(x) - ps >= Fr(1, 2 * nv) * d2, "lbwidth growth 1/(2n)")
        check(Psi0(x) - ps >= Fr(1, nv) * d2, "lbwidth Psi0 growth 1/n")


cnt = 0
for nv in range(1, 5):
    pairs = list(combinations(range(nv), 2))
    for mask in range(2 ** len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        lbwidth(nv, E)
        cnt += 1
for _ in range(10):
    nv = 6
    pairs = list(combinations(range(nv), 2))
    E = [p for p in pairs if random.random() < 0.4]
    lbwidth(nv, E)
    cnt += 1
print("lbwidth: graphs checked =", cnt)

# ---------------- Prop lim:prop:constraints ----------------
def constraints_inst(a0, a):
    m = len(a)
    feas = []
    for xb in product([0, 1], repeat=m + 1):
        if a0 * xb[0] + sum(a[i] * xb[i + 1] for i in range(m)) != a0:
            continue
        y = [Fr(0)]
        aa = [a0] + a
        for i in range(m + 1):
            y.append(y[-1] + Fr(aa[i], a0) * xb[i])
        if y[-1] != 1 or any(t < 0 or t > 1 for t in y):
            continue
        Fv = 2 ** (m + 1) * xb[0] + sum(2 ** i * xb[i + 1] for i in range(m))
        feas.append((Fv, xb, y))
    feas.sort()
    check(len(feas) >= 1, "constraints: infeasible")
    check(len(feas) == 1 or feas[0][0] < feas[1][0], "constraints: min not unique")
    yes = any(sum(a[i] * v[i] for i in range(m)) == a0 for v in product([0, 1], repeat=m))
    check((feas[0][1][0] == 0) == yes, "constraints: x0* != 0 iff yes")
    zs = list(feas[0][1]) + feas[0][2]
    for Fv, xb, y in feas:
        z = list(xb) + y
        d2 = sum((Fr(z[i]) - zs[i]) ** 2 for i in range(len(z)))
        check(len(z) == 2 * m + 3, "count 2m+3")
        check(Fv - feas[0][0] >= d2 / (2 * m + 3), "constraints growth")
    return yes


ny = 0
for _ in range(80):
    m = random.randint(1, 7)
    a0 = random.randint(2, 15)
    a = [random.randint(1, a0) for _ in range(m)]
    ny += constraints_inst(a0, a)
print("constraints: instances, yes =", 80, ny)

# ---------------- Prop lim:prop:oracle counting ----------------
import math
for p in range(1, 5):
    for kap in [8 * p, 8 * p + 1, 10 * p, 32 * p, 50 * p, 200 * p]:
        r2 = Fr(2 * p, kap)
        check(4 * r2 <= 1, "2r<=1")
        # |C| = (floor(1/(2r))+1)^p >= (2r)^(-p) = (kappa/8p)^(p/2)
        two_r = math.sqrt(4 * r2)
        Csize = (math.floor(1 / two_r + 1e-12) + 1) ** p
        check(Csize >= (kap / (8 * p)) ** (p / 2) - 1e-9, "|C| bound")

print("ALL OK" if ok else "SOME FAILURES")
