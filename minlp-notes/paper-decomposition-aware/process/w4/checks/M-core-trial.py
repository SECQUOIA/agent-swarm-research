"""M-core: exact simulation of TRIAL (per-coordinate meshes h_ij, Lemma
lem:inv / lem:states) and of TRIAL with a common mesh (Lemma lem:commonmesh)
on random chain-structured mixed-integer box QPs with a known minimizer x*
and growth constants certified by Lemma lem:growthcert(a).

usage: python3 M-core-trial.py SEED NINST
"""
from fractions import Fraction as Fr
import math, random, sys

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NINST = int(sys.argv[2]) if len(sys.argv) > 2 else 40
rng = random.Random(seed)
fails = []
def check(c, msg):
    if not c:
        fails.append(msg)
        if len(fails) < 20:
            print("FAIL", msg)

def pd(A):
    """exact positive-definiteness test (LDL^T)"""
    n = len(A); A = [row[:] for row in A]
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True

def largest_const(H2M, Dm, lo=Fr(0), iters=24):
    """largest c (dyadic, from below) with H2M - 2 c Dm > 0"""
    hi = Fr(64)
    n = len(H2M)
    def okc(c):
        return pd([[H2M[i][j] - (2 * c * Dm[i] if i == j else 0) for j in range(n)] for i in range(n)])
    if not okc(Fr(0)):
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2
        if okc(mid):
            lo = mid
        else:
            hi = mid
    return lo

def graded(lo, hi, c, h, th, integer, cap):
    nodes = {c}
    for sgn, end in [(1, hi - c), (-1, c - lo)]:
        t = Fr(0)
        while t < end:
            step = h + th * t
            if integer:
                step = max(1, math.floor(step))
            t = min(t + step, end)
            nodes.add(c + sgn * t)
            if len(nodes) > cap:
                return None
    return sorted(nodes)

def eff(a, b, integer):
    return 0 if (integer and b - a == 1) else b - a

def make_instance(n):
    while True:
        integer = [rng.random() < 0.4 for _ in range(n)]
        s = [Fr(rng.randint(1, 9)) if integer[i] else Fr(rng.randint(1, 30), rng.choice([1, 2, 3, 4])) for i in range(n)]
        xs, zeta = [], []
        for i in range(n):
            kind = rng.random()
            if kind < 0.35:
                xs.append(Fr(0)); zeta.append(Fr(rng.randint(0, 6), rng.choice([1, 2, 4])))
            elif kind < 0.6:
                xs.append(s[i]); zeta.append(-Fr(rng.randint(0, 6), rng.choice([1, 2, 4])))
            else:
                if integer[i]:
                    if s[i] < 2:
                        xs.append(Fr(0)); zeta.append(Fr(rng.randint(0, 6))); continue
                    xs.append(Fr(rng.randint(1, int(s[i]) - 1)))
                    zeta.append(Fr(rng.randint(-1, 1), 8))
                else:
                    xs.append(s[i] * Fr(rng.randint(1, 9), 10)); zeta.append(Fr(0))
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fr(rng.randint(-4, 12), rng.choice([1, 2, 4]))
        for i in range(n - 1):
            H[i][i + 1] = H[i + 1][i] = Fr(rng.randint(-8, 8), rng.choice([1, 2, 4]))
        mu = []
        for i in range(n):
            interior = 0 < xs[i] < s[i]
            if interior and not integer[i]:
                mu.append(Fr(0))
            elif (xs[i] == 0 and zeta[i] >= 0) or (xs[i] == s[i] and zeta[i] <= 0):
                mu.append(abs(zeta[i]) / s[i])
            else:
                mu.append(-abs(zeta[i]))
        H2M = [[H[i][j] + (2 * mu[i] if i == j else 0) for j in range(n)] for i in range(n)]
        L = [max(H[i][i], Fr(0)) for i in range(n)]
        if not any(l > 0 for l in L):
            continue
        g = largest_const(H2M, [Fr(1)] * n)
        if g is None or g == 0:
            continue
        gam = largest_const(H2M, L)
        if gam is None or gam == 0:
            continue
        return dict(n=n, integer=integer, s=s, xs=xs, zeta=zeta, H=H, L=L, g=g, gam=gam)

def Fval(I, x):
    n = I['n']; d = [x[i] - I['xs'][i] for i in range(n)]
    v = sum(I['zeta'][i] * d[i] + I['H'][i][i] * d[i] * d[i] / 2 for i in range(n))
    v += sum(I['H'][i][i + 1] * d[i] * d[i + 1] for i in range(n - 1))
    return v

def chain_dp(I, G, corr):
    """exact min-sum on the chain: beta, a minimizer, min-marginals of Q=F-D"""
    n = I['n']; H = I['H']; xs = I['xs']; z = I['zeta']
    un = [{v: z[i] * (v - xs[i]) + H[i][i] * (v - xs[i]) ** 2 / 2 - corr[i][v] for v in G[i]} for i in range(n)]
    pair = lambda i, v, w: H[i][i + 1] * (v - xs[i]) * (w - xs[i + 1])
    f = [dict() for _ in range(n)]; arg = [dict() for _ in range(n)]
    f[0] = dict(un[0])
    for i in range(1, n):
        for w in G[i]:
            best = None
            for v in G[i - 1]:
                val = f[i - 1][v] + pair(i - 1, v, w)
                if best is None or val < best:
                    best, bv = val, v
            f[i][w] = un[i][w] + best; arg[i][w] = bv
    b = [dict() for _ in range(n)]
    b[n - 1] = {v: Fr(0) for v in G[n - 1]}
    for i in range(n - 2, -1, -1):
        for v in G[i]:
            b[i][v] = min(pair(i, v, w) + un[i + 1][w] + b[i + 1][w] for w in G[i + 1])
    mm = [{v: f[i][v] + b[i][v] for v in G[i]} for i in range(n)]
    beta = min(f[n - 1].values())
    y = [None] * n
    y[n - 1] = min(G[n - 1], key=lambda w: f[n - 1][w])
    for i in range(n - 1, 0, -1):
        y[i - 1] = arg[i][y[i]]
    return beta, y, mm

def run_trial(I, theta, common, eps, cap):
    n = I['n']; L = I['L']; P = [i for i in range(n) if L[i] > 0]; nP = len(P)
    s = I['s']; integer = I['integer']; xs = I['xs']
    Lmax = max(L)
    if common:
        smax = max(s)
        mesh = lambda i, j: smax / 2 ** j
        J = 0
        while Fr(9, 16) * Lmax * n * smax ** 2 / 4 ** J > eps:
            J += 1
        g = I['g']; kap = max(Fr(1), Lmax / g)
    else:
        e = {}
        for i in P:
            ei = 0
            while not (Fr(4) ** (ei - 1) < L[i] <= Fr(4) ** ei):
                ei += 1 if L[i] > Fr(4) ** ei else -1
            e[i] = ei
        r = {i: Fr(1, 2 ** e[i]) if e[i] >= 0 else Fr(2 ** (-e[i])) for i in P}
        E = -200
        while not all(Fr(2) ** E * r[i] >= s[i] for i in P):
            E += 1
        eta = lambda j: Fr(2) ** (E - j)
        mesh = lambda i, j: eta(j) * r[i]
        J = 0
        while Fr(9, 16) * nP * eta(0) ** 2 / 4 ** J > eps:
            J += 1
        gam = I['gam']; k = max(Fr(1), 1 / gam)
    box = [(Fr(0), s[i]) for i in range(n)]
    c = [Fr(0)] * n
    U = Fval(I, [Fr(0)] * n)
    for j in range(J + 1):
        G = []
        for i in range(n):
            if i in P:
                Gi = graded(box[i][0], box[i][1], c[i], mesh(i, j), theta, integer[i], cap)
                if Gi is None:
                    return ('abort', j)
                G.append(Gi)
            else:
                G.append([Fr(0), s[i]])
        w = []; corr = []
        for i in range(n):
            wi = {v: Fr(0) for v in G[i]}
            for a, b2 in zip(G[i], G[i][1:]):
                ee = eff(a, b2, integer[i])
                wi[a] = max(wi[a], ee); wi[b2] = max(wi[b2], ee)
            w.append(wi); corr.append({v: L[i] * wi[v] ** 2 / 8 for v in G[i]})
        beta, y, mm = chain_dp(I, G, corr)
        Fy = Fval(I, y)
        if Fy < U:
            U = Fy
        Dy = sum(corr[i][y[i]] for i in range(n))
        check(all(box[i][0] <= xs[i] <= box[i][1] for i in range(n)), "x* in box")
        check(beta <= 0, "beta<=OPT")
        check(Fy - beta == Dy, "F(y)-beta=D(y)")
        if common:
            h = mesh(0, j); rho2 = n * kap
            dc = sum((c[i] - xs[i]) ** 2 for i in range(n))
            dy = sum((y[i] - xs[i]) ** 2 for i in range(n))
            check(dc <= 4 * kap * n * h * h, "G2 c")
            check(dy <= kap * n * h * h, "G2 y")
            check(dy <= Fr(8, 15) * kap * n * h * h, "G2 y 8/15")
            check(U - 0 <= Dy <= Fr(9, 16) * Lmax * n * h * h, "G3")
            for i in P:
                for v in G[i]:
                    check(corr[i][v] <= Lmax * h * h / 4 + Lmax * theta ** 2 / 4 * (v - c[i]) ** 2, "G1 coord")
                    if mm[i][v] <= U:
                        check((v - xs[i]) ** 2 <= Fr(17, 15) * kap * n * h * h, "G2 z (coord)")
        else:
            a = nP * eta(j) ** 2
            dc = sum(L[i] * (c[i] - xs[i]) ** 2 for i in P)
            dy = sum(L[i] * (y[i] - xs[i]) ** 2 for i in P)
            check(dc <= 4 * k * a, "inv(ii)")
            check(dy <= k * a, "inv(iii)")
            check(dy <= Fr(8, 15) * k * a, "inv(iii) 8/15")
            check(U - beta <= Dy <= Fr(9, 16) * a, "inv(iv)")
            for i in P:
                for v in G[i]:
                    check(corr[i][v] <= eta(j) ** 2 / 4 + theta ** 2 / 4 * L[i] * (v - c[i]) ** 2, "energy coord")
                    if mm[i][v] <= U:
                        check(L[i] * (v - xs[i]) ** 2 <= Fr(17, 15) * k * a, "inv(v) coord")
        if U - beta <= eps:
            return ('success', j)
        # filter
        newbox = list(box)
        for i in P:
            ret = [(a, b2) for a, b2 in zip(G[i], G[i][1:]) if min(mm[i][a], mm[i][b2]) <= U]
            if len(G[i]) == 1:
                ret = [(G[i][0], G[i][0])]
            lo = min(a for a, _ in ret); hi = max(b2 for _, b2 in ret)
            newbox[i] = (lo, hi)
            if common:
                R = Fr(42, 10) * Fr(math.isqrt(int(10**12 * n * kap)) + 1, 10**6) * mesh(i, j) + (1 if integer[i] else 0)
                check(y[i] - R <= lo and hi <= y[i] + R, "G4")
            else:
                rho = Fr(math.isqrt(int(10**12 * k * nP)) + 1, 10**6)
                R = 8 * rho * mesh(i, j) + (1 if integer[i] else 0)
                check(y[i] - R <= lo and hi <= y[i] + R, "states radius")
                Rtight = Fr(73, 10) * rho * mesh(i, j) + (1 if integer[i] else 0)
                check(y[i] - Rtight <= lo and hi <= y[i] + Rtight, "states 7.3 radius")
        box = newbox
        c = list(y)
    return ('fail', J)

stats = {}
for inst in range(NINST):
    n = rng.randint(2, 5)
    I = make_instance(n)
    q = rng.randint(6, 16)
    eps = Fr(1, 2 ** q)
    P = [i for i in range(n) if I['L'][i] > 0]; nP = len(P)
    # per-coordinate meshes, grading from kappa-bar
    kb = max(Fr(1), 1 / I['gam'])
    mu = 2
    while 8 * kb > Fr(4) ** mu:
        mu += 1
    theta = Fr(1, 2 ** mu)
    cap = int(10 * 2 ** mu * math.ceil(math.log2(nP + 2)))
    res = run_trial(I, theta, False, eps, cap)
    check(res[0] == 'success', "TRIAL mu* did not succeed: %s kb=%s" % (res, float(kb)))
    stats.setdefault('graded', []).append(res)
    # common mesh, point growth
    Lmax = max(I['L']); kap = max(Fr(1), Lmax / I['g'])
    mu = 2
    while 8 * kap > Fr(4) ** mu:
        mu += 1
    theta = Fr(1, 2 ** mu)
    cap = int(8 * 2 ** mu * math.ceil(math.log2(n + 2)))
    if mu <= 6:
        res = run_trial(I, theta, True, eps, cap)
        check(res[0] == 'success', "common mu* did not succeed: %s kap=%s" % (res, float(kap)))
        stats.setdefault('common', []).append(res)
    print("inst", inst, "n", n, "kb=%.2f kap=%.2f" % (float(kb), float(kap)), stats['graded'][-1], stats.get('common', [None])[-1], flush=True)
print("failures:", len(fails))
print("ALL OK" if not fails else "SOME FAILURES")
