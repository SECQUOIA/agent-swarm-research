"""Exact check of the affine-selector recognition theorem on small random
instances with a scalar parameter, including singular PSD private Hessians.

Instance: phi_z(y) = 1/2 y'Cy + (D z + c)'y, y in [0,u] (r<=3), z in [0,2].
Recognition: solve the central QP at z0=1 exactly (any KKT point), read the
sign pattern of the common central gradient, and solve the single LP for
(a,b) with ybar(z)=a+b(z-1).
Brute force: try all 3^r global patterns (each coordinate identically at its
lower bound with nonnegative gradient, identically at its upper bound with
nonpositive gradient, or zero gradient identically with feasible range).
The theorem predicts: brute force feasible <=> central LP feasible.
Every accepted selector is also checked pointwise by exact KKT at sample z.
All LPs are solved by exact Fourier-Motzkin elimination.
"""
import random
from fractions import Fraction as Fr
from itertools import product

from convexrecourse_common import lp_feasible, matmul, transpose

random.seed(31)
counts = {}


def bump(k, n=1):
    counts[k] = counts.get(k, 0) + n


def central_kkt_point(C, h, l, u):
    r = len(C)
    for pat in product("LFU", repeat=r):
        eqs, cons = [], []
        for i, s in enumerate(pat):
            e = [Fr(int(j == i)) for j in range(r)]
            grad = [C[i][j] for j in range(r)]
            if s == "L":
                eqs.append((e, l[i]))
                cons.append(([-x for x in grad], h[i]))          # grad.y + h_i >= 0
            elif s == "U":
                eqs.append((e, u[i]))
                cons.append((grad, -h[i]))                        # grad.y + h_i <= 0
            else:
                cons.append(([-x for x in e], -l[i]))
                cons.append((e, u[i]))
                eqs.append((grad, -h[i]))
        y = lp_feasible(eqs, cons, r)
        if y is not None:
            return y, pat
    raise RuntimeError("no central optimizer")


def selector_lp(C, D, c, l, u, kinds, z0=Fr(1), rho=Fr(1)):
    """Unknowns x=(a_1..a_r,b_1..b_r).  kinds[i] in 'L','U','F'."""
    r = len(C)
    nv = 2 * r
    h0 = [D[i] * z0 + c[i] for i in range(r)]
    cons, eqs = [], []

    def A_(i):
        return [Fr(int(j == i)) for j in range(nv)]

    def B_(i):
        return [Fr(int(j == r + i)) for j in range(nv)]

    def gamma(i):   # (C a + h0)_i as (coeffs, const)
        return [C[i][j] if j < r else Fr(0) for j in range(nv)], h0[i]

    def T(i):       # (C b + D)_i
        return [C[i][j - r] if j >= r else Fr(0) for j in range(nv)], D[i]

    for i, s in enumerate(kinds):
        ga, g0 = gamma(i)
        ta, t0 = T(i)
        if s in "LU":
            eqs.append((A_(i), l[i] if s == "L" else u[i]))
            eqs.append((B_(i), Fr(0)))
            for sgn in (1, -1):
                coef = [ga[j] + sgn * rho * ta[j] for j in range(nv)]
                const = g0 + sgn * rho * t0
                if s == "L":   # coef.x + const >= 0
                    cons.append(([-x for x in coef], const))
                else:          # coef.x + const <= 0
                    cons.append((coef, -const))
        else:
            eqs.append((ga, -g0))
            eqs.append((ta, -t0))
            for sgn in (1, -1):
                coef = [A_(i)[j] + sgn * rho * B_(i)[j] for j in range(nv)]
                cons.append(([-x for x in coef], -l[i]))
                cons.append((coef, u[i]))
    return lp_feasible(eqs, cons, nv)


def kkt_ok(C, g, l, u, y):
    r = len(C)
    grad = [sum(C[i][j] * y[j] for j in range(r)) + g[i] for i in range(r)]
    for i in range(r):
        if y[i] < l[i] or y[i] > u[i]:
            return False
        if l[i] < y[i] < u[i] and grad[i] != 0:
            return False
        if y[i] == l[i] and grad[i] < 0:
            return False
        if y[i] == u[i] and grad[i] > 0:
            return False
    return True


def run(C, D, c, l, u, tag):
    r = len(C)
    z0 = Fr(1)
    h0 = [D[i] * z0 + c[i] for i in range(r)]
    yhat, cpat = central_kkt_point(C, h0, l, u)
    g0 = [sum(C[i][j] * yhat[j] for j in range(r)) + h0[i] for i in range(r)]
    kinds = ["L" if g0[i] > 0 else "U" if g0[i] < 0 else "F" for i in range(r)]
    sel = selector_lp(C, D, c, l, u, kinds)
    brute = None
    nfeas = 0
    for tau in product("LUF", repeat=r):
        x = selector_lp(C, D, c, l, u, tau)
        if x is not None:
            nfeas += 1
            brute = brute or x
    assert (sel is not None) == (brute is not None), (tag, C, D, c, u)
    if sel is not None:
        a, b = sel[:r], sel[r:]
        for z in [Fr(0), Fr(1, 3), Fr(1), Fr(3, 2), Fr(2)]:
            y = [a[i] + b[i] * (z - z0) for i in range(r)]
            g = [D[i] * z + c[i] for i in range(r)]
            assert kkt_ok(C, g, l, u, y)
            bump("pointwise KKT of accepted selectors")
        bump(f"{tag}: accepted")
        # the active set of the returned central optimizer is misleading
        # when fixing it would fail while the selector exists
        fixed_kinds = ["L" if (cpat[i] == "L") else "U" if cpat[i] == "U" else kinds[i]
                       for i in range(r)]
        if fixed_kinds != kinds and selector_lp(C, D, c, l, u, fixed_kinds) is None:
            bump(f"{tag}: arbitrary central active set would have failed")
    else:
        bump(f"{tag}: rejected (all {3 ** r} global patterns infeasible)")


# named examples
run([[Fr(2), Fr(2)], [Fr(2), Fr(2)]], [Fr(-2), Fr(-2)], [Fr(0), Fr(0)],
    [Fr(0)] * 2, [Fr(1)] * 2, "example (y1+y2-z)^2")
# clipped scalar response, z in [0,2] shifted: (y-(2z-1))^2 crosses both bounds
run([[Fr(2)]], [Fr(-4)], [Fr(2)], [Fr(0)], [Fr(1)], "example clipped")

for trial in range(5000):
    r = random.choice([1, 2, 2, 2, 3]) if trial < 4000 else 3
    srows = random.randint(0, r)          # rank <= srows, often singular
    Rm = [[Fr(random.randint(-2, 2)) for _ in range(r)] for _ in range(srows)]
    C = matmul(transpose(Rm), Rm) if srows else [[Fr(0)] * r for _ in range(r)]
    D = [Fr(random.randint(-3, 3)) for _ in range(r)]
    c = [Fr(random.randint(-4, 4)) for _ in range(r)]
    l = [Fr(0)] * r
    u = [Fr(random.randint(1, 2)) for _ in range(r)]
    sing = any(True for _ in [0]) and (srows < r)
    run(C, D, c, l, u, "random singular" if sing else "random nonsingular")

for k_, v_ in sorted(counts.items()):
    print(f"{k_}: {v_}")
print("all recognition checks passed")
