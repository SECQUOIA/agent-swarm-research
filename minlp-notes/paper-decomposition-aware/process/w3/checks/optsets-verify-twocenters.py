"""Verifier check (independent of optsets-twocenters.py) for Proposition
prop:twocenters (optsets.tex).

1. Bound (eq:twocenters) for random rational (M, theta, h<=M, c_x), G_z={0,M},
   d_z=0, L_x=2 (worst case), exact.
2. Faithful TRIAL/CT (growth.tex: per-coordinate mesh h_{xj}=eta_j r_x, cap
   K_mu = 10*2^mu*ceil(log2(n_P+2)), filtering by hull of retained intervals for
   i in P only, G_z={0,M} since L_z=0) on F_M; at every stage check (a): the
   x-interval is [0,M], beta <= -max{theta^2 M^2/379, h^2/20}; stage 0 has
   G_x={0,M}, beta<=-M^2/4, M<=h_x0<2M; and (b) with eps=-beta (when beta<0):
   |G_x| > M/(48 sqrt eps), table entries > M/(24 sqrt eps). Also the common-mesh
   variant (h_j = s 2^-j).
Run: python3 -B optsets-verify-twocenters.py
"""
from fractions import Fraction as Fr
from math import sqrt, ceil, log2
import random

def graded(lo, hi, c, h, th):
    pts = [c]; t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c); pts.append(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo); pts.append(c - t)
    return sorted(set(pts))

def corr(g, L):
    d = []
    for k, v in enumerate(g):
        w = 0
        if k > 0: w = max(w, v - g[k - 1])
        if k + 1 < len(g): w = max(w, g[k + 1] - v)
        d.append(L * w * w / 8)
    return d

def FM(M, x, z): return x * x - 2 * x * z + M * z

def bound(M, th, h): return max(th * th * M * M / 379, h * h / 20)

ok = True
random.seed(12345)
worst = None
for _ in range(3000):
    M = Fr(random.randint(1, 200), random.randint(1, 20))
    th = Fr(1, 4) * Fr(random.randint(1, 1000), 1000)
    h = M * Fr(random.randint(1, 1000), 1000)
    cx = M * Fr(random.randint(0, 1000), 1000)
    gx = graded(Fr(0), M, cx, h, th)
    if len(gx) > 20000: continue
    dx = corr(gx, Fr(2))
    beta = min(min(FM(M, v, Fr(0)) - dx[k], FM(M, v, M) - dx[k]) for k, v in enumerate(gx))
    r = -beta / bound(M, th, h)
    ok &= r >= 1
    worst = r if worst is None else min(worst, r)
print("1. random parameter sets: min (-beta)/bound =", float(worst), "(must be >= 1)")

def run_ct(M, eps, common=False, maxmu=14):
    """returns list of stage records; stops at the successful trial"""
    # per-coordinate mesh for x (L_x=2): e=1, r=1/2; E least with 2^E r >= M
    E = 0
    while Fr(2) ** E / 2 < M: E += 1
    while Fr(2) ** (E - 1) / 2 >= M: E -= 1
    eta0 = Fr(2) ** E
    J = 0
    while Fr(9, 16) * eta0 ** 2 / 4 ** J > eps: J += 1
    recs = []
    U = FM(M, 0, 0)  # incumbent l
    for mu in range(2, maxmu + 1):
        th = Fr(1, 2 ** mu); K = 10 * 2 ** mu * ceil(log2(1 + 2))
        lo, hi = Fr(0), M; c = Fr(0)
        for j in range(J + 1):
            h = (M / 2 ** j) if common else eta0 / 2 ** j / 2
            gx = graded(lo, hi, c, h, th)
            if len(gx) > K: break  # abort
            dx = corr(gx, Fr(2)); gz = [Fr(0), M]
            Q = [[FM(M, v, z) - dx[k] for z in gz] for k, v in enumerate(gx)]
            beta = min(min(r) for r in Q)
            ky, kz = next((k, l) for k in range(len(gx)) for l in range(2) if Q[k][l] == beta)
            y = gx[ky]
            U = min(U, FM(M, y, gz[kz]))
            recs.append(dict(mu=mu, j=j, th=th, h=h, lo=lo, hi=hi, nx=len(gx), entries=2 * len(gx), beta=beta, U=U, gx0=gx if j == 0 else None))
            if U - beta <= eps:
                return recs, True
            mx = [min(r) for r in Q]
            keep = [k for k in range(len(gx) - 1) if min(mx[k], mx[k + 1]) <= U]
            lo, hi = gx[keep[0]], gx[keep[-1] + 1]
            c = y
    return recs, False

for (M, eps, common) in [(Fr(64), Fr(1, 4), False), (Fr(64), Fr(1), False), (Fr(100), Fr(1), False),
                         (Fr(256), Fr(1), False), (Fr(64), Fr(1, 4), True), (Fr(37, 3), Fr(1, 16), False)]:
    recs, succ = run_ct(M, eps, common)
    for r in recs:
        ok &= (r['lo'] == 0 and r['hi'] == M)
        ok &= -r['beta'] >= bound(M, r['th'], r['h'])
        if r['j'] == 0 and not common:
            ok &= (M <= r['h'] < 2 * M) and r['gx0'] == [0, M] and r['beta'] <= -M * M / 4
        if r['beta'] < 0:
            e = float(-r['beta'])
            ok &= r['nx'] > float(M) / (48 * sqrt(e)) and r['entries'] > float(M) / (24 * sqrt(e))
    last = recs[-1]
    print("2. M=%s eps=%s common=%s success=%s at mu=%d j=%d: nx=%d entries=%d, M/(24 sqrt eps)=%.1f, stages=%d"
          % (M, eps, common, succ, last['mu'], last['j'], last['nx'], last['entries'], float(M) / (24 * sqrt(float(eps))), len(recs)))
    ok &= succ
# constants
ok &= Fr(23, 100) ** 2 / 20 > Fr(1, 379)
ok &= (Fr(1, 2) - Fr(9, 64)) * Fr(16, 25) == Fr(23, 100)
ok &= sqrt(20) + sqrt(379) < 24
print("ALL PASS" if ok else "FAIL")
