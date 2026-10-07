"""Verifier check (independent of optsets-prox.py) for Remark rem:falseguess,
the DISC budgets J_khat, and Lemma lem:proximal (i)-(iii) on small instances.

PROX(khat) as in Algorithm alg:prox (optsets.tex): mu>=2 least with
4^-mu khat <= 1/8, theta=2^-mu, eta=L theta^2/4, varrho=2 ceil(sqrt(khat n)).
Stage: box X' = X cap prod[c_i - varrho h, c_i + varrho h], graded grid of X'_i
(Def def:graded, continuous), corrections L_i w_i(v)^2/8 (w_i = largest adjacent
interval), minimize Q_eta(y)=F(y)-D(y)+eta||y-c||^2 over G (enumeration).
Run: python3 -B optsets-verify-falseguess.py
"""
from fractions import Fraction as Fr
from math import isqrt, ceil, log2
import itertools

def csqrt(q):  # ceil(sqrt(q)), q Fraction >= 0
    r = isqrt(q.numerator // q.denominator) + 2
    while r > 0 and Fr((r - 1) ** 2) >= q:
        r -= 1
    return r

def graded(lo, hi, c, h, th):
    pts = [c]
    t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c); pts.append(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo); pts.append(c - t)
    return sorted(set(pts))

def corrections(g, Li):
    d = {}
    for k, v in enumerate(g):
        w = 0
        if k > 0: w = max(w, v - g[k - 1])
        if k + 1 < len(g): w = max(w, g[k + 1] - v)
        d[v] = Li * w * w / 8
    return d

def prox(F, Ls, lo, hi, khat, J):
    n = len(lo); L = max(Ls); s = max(hi[i] - lo[i] for i in range(n))
    mu = 2
    while Fr(khat, 4 ** mu) > Fr(1, 8): mu += 1
    th = Fr(1, 2 ** mu); eta = L * th * th / 4; rho = 2 * csqrt(Fr(khat * n))
    Kth = 8 * 2 ** mu * ceil(log2(n + 2))
    c = list(lo); out = []
    for j in range(J + 1):
        h = s / 2 ** j
        G = []; ds = []
        for i in range(n):
            a = max(lo[i], c[i] - rho * h); b = min(hi[i], c[i] + rho * h)
            g = graded(a, b, c[i], h, th); G.append(g); ds.append(corrections(g, Ls[i]))
        assert max(len(g) for g in G) <= Kth, "node cap (i) violated"
        best = None; arg = []
        for y in itertools.product(*G):
            q = F(y) - sum(ds[i][y[i]] for i in range(n)) + eta * sum((y[i] - c[i]) ** 2 for i in range(n))
            if best is None or q < best: best, arg = q, [y]
            elif q == best: arg.append(y)
        # tie-break towards the current center
        y = min(arg, key=lambda z: sum((z[i] - c[i]) ** 2 for i in range(n)))
        out.append((j, h, tuple(c), y, arg, best, max(len(g) for g in G)))
        c = list(y)
    return out, (mu, th, eta, rho, Kth)

ok = True
# ---- Remark rem:falseguess
F = lambda v: v[0] ** 2 + v[1] ** 2 - 3 * v[0] * v[1] + Fr(63, 128) * (v[0] + v[1])
lo, hi, Ls = [Fr(0)] * 2, [Fr(1)] * 2, [Fr(2)] * 2
# Delta, R, tau of Section 6: Delta = lcm of denominators of H_ii/2=1, H_12=-3, b=63/128, c=0, endpoints
Delta = 128; R = Delta * (Delta * 2) * (Delta * 2); tau = Fr(1, 4 * 2 * R)
budgets = {}
for kh in (1, 2, 4):
    j = 0
    while 4 ** j * tau ** 2 < 4 * kh * 2 * 1: j += 1
    budgets[kh] = j
print("budgets J_khat:", budgets, " R =", R, "= 2^%d" % (R.bit_length() - 1))
assert budgets == {1: 28, 2: 28, 4: 29}
for kh in (1, 2, 4):
    out, par = prox(F, Ls, lo, hi, kh, 33)
    ties = [(j, a) for (j, h, c, y, a, b, k) in out if len(a) > 1]
    allorigin = all(y == (0, 0) for (j, h, c, y, a, b, k) in out)
    print("khat", kh, "params mu,theta,eta,rho,Kth =", par, " origin at all j<=33:", allorigin)
    print("   ties:", [(j, [tuple(str(t) for t in z) for z in a], str(out[j][5])) for j, a in ties])
    ok &= allorigin
    if kh in (1, 2): ok &= not ties
# Lambda at origin and at (1,1)
gx0 = Fr(63, 128); lam0 = 2 * gx0
gx1 = 2 - 3 + Fr(63, 128); lam1 = 2 * abs(gx1)
print("diag at origin", 2 + lam0, " min eig", 2 + lam0 - 3, "; diag at (1,1)", 2 + lam1, " min eig", 2 + lam1 - 3)
ok &= (2 + lam0 == Fr(191, 64)) and (2 + lam0 - 3 == Fr(-1, 64)) and (2 + lam1 == Fr(193, 64)) and (2 + lam1 - 3 > 0)
# OPT and the g_S bound
ok &= F((1, 1)) == Fr(-1, 64)
# brute-force check of uniqueness on a fine rational grid
m = 64
vals = [(F((Fr(a, m), Fr(b, m))), (a, b)) for a in range(m + 1) for b in range(m + 1)]
mn = min(vals)[0]; ok &= mn == Fr(-1, 64) and [p for v, p in vals if v == mn] == [(m, m)]

# ---- Lemma lem:proximal (ii)/(iii) on instances with known kappa_S (khat >= kappa_S)
def dist2_point(y, S):
    return min(sum((y[i] - s[i]) ** 2 for i in range(len(y))) for s in S)
tests = []
# separable: (x-1/3)^2+(y-2/3)^2, L=2, g_S=1 -> kappa_S=2
tests.append(("sep", lambda v: (v[0] - Fr(1, 3)) ** 2 + (v[1] - Fr(2, 3)) ** 2, [Fr(2)] * 2, [Fr(0)] * 2, [Fr(1)] * 2,
              lambda y: dist2_point(y, [(Fr(1, 3), Fr(2, 3))]), 2, Fr(0)))
# (x-y)^2 on [0,1]^2: S diagonal, dist^2 = (x-y)^2/2, g_S=2, L=2 -> kappa_S=1
tests.append(("diag", lambda v: (v[0] - v[1]) ** 2, [Fr(2)] * 2, [Fr(0)] * 2, [Fr(1)] * 2,
              lambda y: (y[0] - y[1]) ** 2 / 2, 1, Fr(0)))
# twocenters F_4: kappa_S <= 40
M = Fr(4)
tests.append(("F4", lambda v: v[0] ** 2 - 2 * v[0] * v[1] + M * v[1], [Fr(2), Fr(0)], [Fr(0)] * 2, [M] * 2,
              lambda y: dist2_point(y, [(0, 0), (M, M)]), 40, Fr(0)))
for name, Fn, Lsn, lon, hin, d2, kS, OPT in tests:
    for kh in (kS, 2 * kS):
        out, par = prox(Fn, Lsn, lon, hin, kh, 12)
        n = len(lon); L = max(Lsn)
        for (j, h, c, y, a, b, k) in out:
            assert d2(c) <= 4 * kh * n * h * h, (name, kh, j, "center hyp")
            assert Fn(y) - OPT <= Fr(99, 256) * L * n * h * h, (name, kh, j, "value")
            assert d2(y) <= Fr(99, 256) * kh * n * h * h, (name, kh, j, "dist")
        print("lem:proximal (ii),(iii) ok:", name, "khat", kh, "max nodes", max(o[6] for o in out), "cap", par[4])
print("ALL PASS" if ok else "FAIL")
