"""Exact checks for PROX (Algorithm alg:prox) and Lemma lem:proximal
(optsets.tex / appendix-proximal.tex, W3 revision), and for Remark
rem:falseguess.

PROX(khat): mu >= 2 least with 4^-mu khat <= 1/8, theta = 2^-mu,
eta = L theta^2/4, varrho = 2 ceil(sqrt(khat n)), K_theta = 8 theta^-1
ceil(log2(n+2)). Stage with center c and mesh h: box X' = X cap
prod [c_i - varrho h, c_i + varrho h]; graded grid of X'_i from c_i with step
h + theta t; corrections L_i w^2/8; minimize
Q_eta(y) = F(y) - D(y) + eta ||y - c||^2 over the grid (brute force, n <= 3).
Iteration: c^0 = l, h_j = s 2^-j, c^{j+1} = y^j.

Checks
1. Constants: theta^-1 <= 6 sqrt(khat), 8 khat theta^2 <= 1, the 99/64
   arithmetic, K_theta bound 3 + (8/theta) ln(n+2) <= 8 theta^-1 ceil(log2(n+2)).
2. Lemma (i) and (iii) on instances with known kappa_S:
   F = (x-1/3)^2 + (y-2/3)^2 (L = 2, g_S = 1, kappa_S = 2),
   F = (x-y)^2 on [0,1]^2 (L = 2, g_S = 2, kappa_S = 1; S a segment),
   F = x^2 - 2xz + 4z on [0,4]^2 (prop:twocenters, kappa_S <= 40).
3. Remark rem:falseguess: F = x^2+y^2-3xy+63/128(x+y) on [0,1]^2,
   khat in {1,2,4}, stages 0..33: list argmin sets; with ties broken towards
   the current center, the origin is returned at every stage.
Run: python3 -B optsets-prox.py
"""
from fractions import Fraction as Fr
from math import isqrt, log, sqrt, ceil, log2
import itertools


def ceil_sqrt_frac(q):
    # ceil(sqrt(q)) for a nonnegative Fraction q
    r = isqrt(q.numerator // q.denominator)
    while Fr(r * r) < q:
        r += 1
    while r > 0 and Fr((r - 1) ** 2) >= q:
        r -= 1
    return r


def params(khat, n, L):
    mu = 2
    while Fr(khat) / 4 ** mu > Fr(1, 8):
        mu += 1
    th = Fr(1, 2 ** mu)
    eta = L * th * th / 4
    varrho = 2 * ceil_sqrt_frac(Fr(khat) * n)
    Kth = 8 * 2 ** mu * ceil(log2(n + 2) - 1e-12)
    return mu, th, eta, varrho, Kth


def graded(c, lo, hi, h, th):
    nodes = {c}
    t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c)
        nodes.add(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo)
        nodes.add(c - t)
    return sorted(nodes)


def corr(nodes, Li):
    d = {}
    for k, v in enumerate(nodes):
        w = Fr(0)
        if k > 0:
            w = max(w, v - nodes[k - 1])
        if k + 1 < len(nodes):
            w = max(w, nodes[k + 1] - v)
        d[v] = Li * w * w / 8
    return d


def prox_run(F, Ls, lo, hi, khat, stages, tiebreak_center=False):
    n = len(lo)
    L = max(Ls)
    s = max(hi[i] - lo[i] for i in range(n))
    mu, th, eta, varrho, Kth = params(khat, n, L)
    c = tuple(lo)
    out = []
    for j in range(stages + 1):
        h = s / 2 ** j
        grids = []
        for i in range(n):
            a, b = max(lo[i], c[i] - varrho * h), min(hi[i], c[i] + varrho * h)
            grids.append(graded(c[i], a, b, h, th))
        ds = [corr(grids[i], Ls[i]) for i in range(n)]
        best, args = None, []
        for y in itertools.product(*grids):
            q = F(*y) - sum(ds[i][y[i]] for i in range(n)) + eta * sum((y[i] - c[i]) ** 2 for i in range(n))
            if best is None or q < best:
                best, args = q, [y]
            elif q == best:
                args.append(y)
        if tiebreak_center:
            arg = min(args, key=lambda y: sum((y[i] - c[i]) ** 2 for i in range(n)))
        else:
            arg = args[0]
        out.append(dict(j=j, h=h, arg=arg, nargs=len(args), sizes=[len(g) for g in grids], Kth=Kth))
        c = arg
    return out


def check_constants():
    ok = True
    for khat in [1, 2, 3, 4, 5, 8, 16, 100, 1000, 12345]:
        mu, th, eta, varrho, Kth = params(khat, 1, Fr(1))
        ok &= Fr(1) / th <= 6 * sqrt(khat) + 1e-12 and 8 * khat * th * th <= 1 and th <= Fr(1, 4)
    ok &= 1 + Fr(1, 2) * (1 + Fr(1, 32)) + Fr(1, 32) == Fr(99, 64)
    for n in range(1, 100000, 7):
        lhs = 3 * 0.25 + 8 * log(n + 2)  # times theta^-1, using 3 <= 3/(4 theta)
        ok &= lhs <= 7 * ceil(log2(n + 2) - 1e-12)
        ok &= 1.5 + sqrt(n / 2) <= n + 2
    ok &= 48 * sqrt(2) < 68
    print("constants:", ok)
    return ok


def check_lemma():
    ok = True
    cases = [
        ("separable", lambda x, y: (x - Fr(1, 3)) ** 2 + (y - Fr(2, 3)) ** 2, [Fr(2), Fr(2)],
         [Fr(0), Fr(0)], [Fr(1), Fr(1)], 2,
         lambda x, y: (x - Fr(1, 3)) ** 2 + (y - Fr(2, 3)) ** 2),
        ("segment", lambda x, y: (x - y) ** 2, [Fr(2), Fr(2)], [Fr(0), Fr(0)], [Fr(1), Fr(1)], 1,
         lambda x, y: (x - y) ** 2 / 2),
        ("twocenters", lambda x, z: x * x - 2 * x * z + 4 * z, [Fr(2), Fr(0)], [Fr(0), Fr(0)],
         [Fr(4), Fr(4)], 40,
         lambda x, z: min(x * x + z * z, (4 - x) ** 2 + (4 - z) ** 2)),
    ]
    for name, F, Ls, lo, hi, kS, dist2 in cases:
        for khat in sorted({kS, 2 * kS}):
            out = prox_run(F, Ls, lo, hi, khat, 12)
            n = 2
            for r in out:
                bound = Fr(99, 256) * khat * n * r["h"] ** 2
                good = dist2(*r["arg"]) <= bound and max(r["sizes"]) <= r["Kth"]
                ok &= good
                if not good:
                    print("FAIL", name, khat, r)
            print(f"lemma (i),(iii) {name}, khat={khat}: max nodes {max(max(r['sizes']) for r in out)}"
                  f" <= K_theta={out[0]['Kth']}: ok so far {ok}")
    return ok


def check_falseguess():
    F = lambda x, y: x * x + y * y - 3 * x * y + Fr(63, 128) * (x + y)
    Ls = [Fr(2), Fr(2)]
    lo, hi = [Fr(0), Fr(0)], [Fr(1), Fr(1)]
    # budgets: Delta = 128, P_ii = 256, R = 128*256*256, tau = 1/(4 n R)
    R = 128 * 256 * 256
    tau = Fr(1, 4 * 2 * R)
    ok = True
    for khat in [1, 2, 4]:
        J = 0
        while 4 ** J * tau * tau < 4 * khat * 2:
            J += 1
        out = prox_run(F, Ls, lo, hi, khat, 33, tiebreak_center=True)
        origin = all(r["arg"] == (0, 0) for r in out)
        ties = [(r["j"], r["nargs"]) for r in out if r["nargs"] > 1]
        print(f"falseguess khat={khat}: J={J}; origin at all stages 0..33 (ties to center): {origin};"
              f" stages with ties: {ties}")
        ok &= origin and J <= 33
        if khat in (1, 2):
            ok &= not ties
    # tie set at khat = 4, stages 0 and 1
    out = prox_run(F, Ls, lo, hi, 4, 1)
    # list all minimizers at stages 0 and 1 (center (0,0) both times)
    for j in [0, 1]:
        mu, th, eta, varrho, Kth = params(4, 2, Fr(2))
        h = Fr(1, 2 ** j)
        grids = [graded(Fr(0), Fr(0), min(Fr(1), varrho * h), h, th)] * 2
        ds = [corr(g, Fr(2)) for g in grids]
        vals = {}
        for y in itertools.product(*grids):
            vals[y] = F(*y) - ds[0][y[0]] - ds[1][y[1]] + eta * (y[0] ** 2 + y[1] ** 2)
        m = min(vals.values())
        print(f"  khat=4 stage {j}: min Q_eta = {m}, argmins = {[y for y, v in vals.items() if v == m]}")
    # matrices of the remark
    lam0 = 2 * Fr(63, 128)
    g1 = 2 - 3 + Fr(63, 128)
    lam1 = 2 * abs(g1)
    ok &= (2 + lam0 == Fr(191, 64)) and (2 + lam0 - 3 == Fr(-1, 64)) and (2 + lam1 == Fr(193, 64)) \
        and (2 + lam1 - 3 > 0)
    # unique optimizer (1,1), OPT = -1/64, F(0) = 0
    ok &= F(Fr(1), Fr(1)) == Fr(-1, 64)
    print("falseguess:", ok)
    return ok


if __name__ == "__main__":
    res = [check_constants(), check_lemma(), check_falseguess()]
    print("ALL PASS" if all(res) else "SOME FAIL")
