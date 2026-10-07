#!/usr/bin/env python3
"""Exact finite checks for two optimal-set statements positioned in the lit-ext memo.

(A) Diagonal (box-Lagrangian) certificate, cf. Li-Wu-Quan 2015 Cor. 2:
    F(x)=x'Hx/2+b'x on a box, s a KKT point, d_i=+-2 dF_i(s)/(u_i-l_i) at bounds, 0 inside.
    Checks: the expansion identity at all grid points; when H+D is PSD, the optimal grid
    points are exactly those satisfying (H+D)(x-s)=0 and d_i(x_i-l_i)(u_i-x_i)=0; and every
    optimal grid point t has D(t)=D(s) (invariance = saddle-point product structure).

(B) Rosenberg-type face characterization for coordinatewise-concave quadratics
    F(x)=x'Qx+c'x with Q_ii<=0: x is optimal iff x_i is an endpoint whenever Q_ii<0 and every
    vertex of the smallest box face containing x is an optimal vertex.  Also checks the
    single-bag form of the interpolation identity
      F(x)-OPT = sum_v (F(v)-OPT) W(v;x) - sum_i Q_ii (x_i-l_i)(u_i-x_i).
Exact rational arithmetic; finite checks only.
"""
from fractions import Fraction as Fr
from itertools import product
import random, sys

def rf(lo, hi, den=4):
    return Fr(random.randint(lo * den, hi * den), den)

def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]

def quad(A, x):
    return sum(x[i] * A[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))

def check_A(seed):
    random.seed(seed)
    n = random.randint(2, 4)
    l = [rf(-2, 0) for _ in range(n)]
    u = [l[i] + Fr(random.randint(1, 4), 2) for i in range(n)]
    # choose s: each coordinate at l, at u, or interior
    s, kind = [], []
    for i in range(n):
        k = random.choice(['l', 'u', 'm'])
        kind.append(k)
        s.append(l[i] if k == 'l' else u[i] if k == 'u' else (l[i] + u[i]) / 2)
    d = [Fr(random.randint(0, 6), 2) if kind[i] != 'm' else Fr(0) for i in range(n)]
    r = random.randint(0, n)          # rank of PSD part (rank-deficient -> nonunique optima)
    A = [[rf(-2, 2) for _ in range(r)] for _ in range(n)]
    M = [[sum(A[i][k] * A[j][k] for k in range(r)) for j in range(n)] for i in range(n)]
    H = [[M[i][j] - (d[i] if i == j else 0) for j in range(n)] for i in range(n)]
    grad_s = [d[i] * (u[i] - l[i]) / 2 if kind[i] == 'l' else -d[i] * (u[i] - l[i]) / 2 if kind[i] == 'u' else Fr(0)
              for i in range(n)]
    Hs = matvec(H, s)
    b = [grad_s[i] - Hs[i] for i in range(n)]
    F = lambda x: quad(H, x) / 2 + sum(b[i] * x[i] for i in range(n))
    grads = lambda x: [v + b[i] for i, v in enumerate(matvec(H, x))]
    HD = [[H[i][j] + (d[i] if i == j else 0) for j in range(n)] for i in range(n)]   # = M, PSD
    pts = [sorted({l[i], u[i], s[i]} | {l[i] + (u[i] - l[i]) * Fr(k, 4) for k in range(1, 4)}) for i in range(n)]
    Fs = F(s)
    nopt = 0
    for x in product(*pts):
        x = list(x)
        e = [x[i] - s[i] for i in range(n)]
        rhs = quad(HD, e) / 2 + sum(d[i] * (x[i] - l[i]) * (u[i] - x[i]) for i in range(n)) / 2
        assert F(x) - Fs == rhs, ("identity", seed)
        desc = all(v == 0 for v in matvec(HD, e)) and all(d[i] * (x[i] - l[i]) * (u[i] - x[i]) == 0 for i in range(n))
        opt = (F(x) == Fs)
        assert opt == desc, ("description", seed, x)
        if opt:
            nopt += 1
            g = grads(x)
            # x must be a KKT point with the same diagonal entries
            dt = []
            for i in range(n):
                if x[i] == l[i]:
                    assert g[i] >= 0
                    dt.append(2 * g[i] / (u[i] - l[i]))
                elif x[i] == u[i]:
                    assert g[i] <= 0
                    dt.append(-2 * g[i] / (u[i] - l[i]))
                else:
                    assert g[i] == 0
                    dt.append(Fr(0))
            # entries agree wherever x is at a bound or d_i>0 (interior coords have d_i(x)=0=d_i(s)
            # because positive d forces an endpoint)
            assert dt == d, ("invariance", seed, x, dt, d)
    return nopt

def check_B(seed):
    random.seed(10_000 + seed)
    n = random.randint(1, 4)
    l = [rf(-2, 0) for _ in range(n)]
    u = [l[i] + Fr(random.randint(1, 4), 2) for i in range(n)]
    Q = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        Q[i][i] = random.choice([Fr(0), Fr(0), -Fr(random.randint(1, 4), 2)])
        for j in range(i + 1, n):
            Q[i][j] = Q[j][i] = random.choice([Fr(0), rf(-2, 2)])
    c = [random.choice([Fr(0), rf(-2, 2)]) for _ in range(n)]
    F = lambda x: quad(Q, x) + sum(c[i] * x[i] for i in range(n))
    verts = list(product(*[(l[i], u[i]) for i in range(n)]))
    OPT = min(F(list(v)) for v in verts)
    optv = {v for v in verts if F(list(v)) == OPT}
    pts = [sorted({l[i], u[i]} | {l[i] + (u[i] - l[i]) * Fr(k, 3) for k in (1, 2)}) for i in range(n)]
    nopt = 0
    for x in product(*pts):
        x = list(x)
        val = F(x)
        assert val >= OPT
        # interpolation identity (one bag)
        tot = Fr(0)
        for v in verts:
            W = Fr(1)
            for i in range(n):
                W *= (x[i] - l[i]) / (u[i] - l[i]) if v[i] == u[i] else (u[i] - x[i]) / (u[i] - l[i])
            tot += (F(list(v)) - OPT) * W
        tot -= sum(Q[i][i] * (x[i] - l[i]) * (u[i] - x[i]) for i in range(n))
        assert val - OPT == tot, ("identity B", seed)
        # Rosenberg-type face criterion
        face = [((l[i],) if x[i] == l[i] else (u[i],) if x[i] == u[i] else (l[i], u[i])) for i in range(n)]
        crit = all(x[i] in (l[i], u[i]) for i in range(n) if Q[i][i] < 0) and all(v in optv for v in product(*face))
        assert (val == OPT) == crit, ("criterion", seed, x)
        nopt += (val == OPT)
    return nopt

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    a = sum(check_A(k) for k in range(N))
    bcount = sum(check_B(k) for k in range(N))
    print(f"PASS (A): {N} random box QPs with a diagonal certificate; identity, full-set description and "
          f"invariance of D verified at all grid points ({a} optimal grid points in total).")
    print(f"PASS (B): {N} random coordinatewise-concave box QPs; interpolation identity and face criterion "
          f"verified at all grid points ({bcount} optimal grid points in total).")
