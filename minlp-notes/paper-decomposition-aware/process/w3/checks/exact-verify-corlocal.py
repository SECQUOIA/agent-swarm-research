"""Verifier check of Corollary cor:local (Section 6.5, proof in Appendix B.1).

Independent of experiments/: a faithful TRIAL with a common mesh
(Lemma lem:commonmesh) on small random mixed box QPs, exact arithmetic,
brute-force grids. For every instance with a unique minimizer x* and a growth
constant g certified by Lemma lem:growthcert(a), with kappa = max{1, L/g} and
theta = 2^-mu, mu = max{2, ceil(log4(8 kappa))}, we check at every stage:
  * y_j lies in the narrowed box (text before Definition def:facecand),
  * (G2) and (G4) of lem:commonmesh,
and at every stage with h_j <= h* (h* as in cor:local, with A the continuous
coordinates in P at a bound):
  * narrowed box is {x*_i} for integer coordinates and coordinates not in P,
  * J_+ = J_0 cup A,
  * the face candidate exists and equals x*,
  * x* passes the test of Proposition prop:local.
Soundness: whenever the face candidate passes the test at any stage, it is a
global minimizer.
"""
import itertools
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'experiments'))
from oracle import exact_minimum  # noqa: E402


def val(H, b, c, x):
    n = len(x)
    return sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + \
        sum(b[i] * x[i] for i in range(n)) + c


def grad(H, b, x):
    n = len(x)
    return [sum(H[i][j] * x[j] for j in range(n)) + b[i] for i in range(n)]


def is_psd(M):
    m = [list(r) for r in M]
    n = len(m)
    for k in range(n):
        p = m[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(m[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = m[i][k] / p
            for j in range(k + 1, n):
                m[i][j] -= f * m[k][j]
    return True


def solve_linear(M, r):
    n = len(M)
    A = [list(M[i]) + [r[i]] for i in range(n)]
    for k in range(n):
        piv = next((i for i in range(k, n) if A[i][k] != 0), None)
        if piv is None:
            return None
        A[k], A[piv] = A[piv], A[k]
        for i in range(n):
            if i != k and A[i][k] != 0:
                f = A[i][k] / A[k][k]
                A[i] = [a - f * bk for a, bk in zip(A[i], A[k])]
    return [A[i][n] / A[i][i] for i in range(n)]


def graded(lo, hi, c, h, theta, integer):
    nodes = {c}
    for sign, end in ((1, hi), (-1, lo)):
        t, R = F(0), abs(end - c)
        while t < R:
            step = max(1, math.floor(h + theta * t)) if integer else h + theta * t
            t = min(t + step, R)
            nodes.add(c + sign * t)
    return sorted(nodes)


FIRST_HIT = []


def run_instance(H, b, cst, bounds, ints, xs, g, report):
    n = len(xs)
    L_i = [max(H[i][i], F(0)) for i in range(n)]
    P = [i for i in range(n) if L_i[i] > 0]
    L = max(L_i)
    kappa = max(F(1), L / g)
    mu = 2
    while 4 ** mu < 8 * kappa:
        mu += 1
    theta = F(1, 2 ** mu)
    s = max(hi - lo for lo, hi in bounds)
    zeta = grad(H, b, xs)
    IC = [i for i in range(n) if i not in ints]
    J0 = [i for i in IC if bounds[i][0] < xs[i] < bounds[i][1]]
    A = [i for i in IC if i in P and xs[i] in bounds[i]]
    if any(zeta[i] == 0 for i in A):
        return 'skip-weak'
    lamA = min((abs(zeta[i]) for i in A), default=None)
    # Gamma = ||H_AA||_2 + ||H_{J0 A}||_2^2/(2g), spectral norms rounded up
    GammaUB = None
    if A:
        import numpy as np
        spec = lambda rows, cols: (float(np.linalg.norm(np.array(
            [[float(H[i][j]) for j in cols] for i in rows]), 2)) if rows and cols else 0.0)
        nAA = spec(A, A) * (1 + 1e-9) + 1e-12
        nJA = spec(J0, A) * (1 + 1e-9) + 1e-12
        # spectral norms rounded up: GammaUB >= Gamma, only slightly
        GammaUB = F(nAA) + F(nJA) ** 2 / (2 * g)
    dX = None
    for i in range(n):
        if i in IC or i not in P:
            for e in bounds[i]:
                if e != xs[i]:
                    dX = abs(xs[i] - e) if dX is None else min(dX, abs(xs[i] - e))
    terms = []
    if any(i in ints and i in P for i in range(n)):
        terms.append(F(1, 2))
    if any(i in IC or i not in P for i in range(n)):
        terms.append(dX / 6)
    if A:
        terms.append(lamA / (5 * GammaUB))
    m0 = min(terms)
    # h* = m0 / sqrt(n kappa); compare h_j^2 n kappa <= m0^2
    X = [tuple(bd) for bd in bounds]
    c = [bd[0] for bd in bounds]
    U = val(H, b, cst, c)
    stages_hit = 0
    for j in range(60):
        h = s / 2 ** j
        grids = []
        for i in range(n):
            lo, hi = X[i]
            if i in P:
                grids.append(graded(lo, hi, c[i], h, theta, i in ints))
            else:
                grids.append([bounds[i][0], bounds[i][1]])
        # corrections
        d = []
        for i in range(n):
            G = grids[i]
            di = {}
            for k, v in enumerate(G):
                w = F(0)
                for a, a2 in ((G[k - 1], v) if k > 0 else (None, None), (v, G[k + 1]) if k + 1 < len(G) else (None, None)):
                    if a is None:
                        continue
                    ew = F(0) if (i in ints and a2 - a == 1) else a2 - a
                    w = max(w, ew)
                di[v] = L_i[i] * w * w / 8
            d.append(di)
        if math.prod(len(G) for G in grids) > 60000:
            report.append(('too-big', j))
            return 'too-big'
        beta, y = None, None
        marg = [dict() for _ in range(n)]
        for z in itertools.product(*grids):
            Fz = val(H, b, cst, z)
            Qz = Fz - sum(d[i][z[i]] for i in range(n))
            if beta is None or Qz < beta:
                beta, y = Qz, z
            for i in range(n):
                if z[i] not in marg[i] or Qz < marg[i][z[i]]:
                    marg[i][z[i]] = Qz
        Fy = val(H, b, cst, y)
        if Fy < U:
            U = Fy
        OPT = val(H, b, cst, xs)
        assert beta <= OPT <= U
        nk = n * kappa
        # (G2)
        assert sum((y[i] - xs[i]) ** 2 for i in range(n)) <= nk * h * h, 'G2 y'
        assert sum((c[i] - xs[i]) ** 2 for i in range(n)) <= 4 * nk * h * h, 'G2 c'
        # filtering
        newX = []
        for i in range(n):
            if i not in P:
                newX.append(X[i])
                continue
            G = grids[i]
            kept = [(G[k], G[k + 1]) for k in range(len(G) - 1)
                    if min(marg[i][G[k]], marg[i][G[k + 1]]) <= U]
            if len(G) == 1:
                kept = [(G[0], G[0])]
            lo, hi = min(a for a, _ in kept), max(a2 for _, a2 in kept)
            # (G4): within 4.2 sqrt(n kappa) h (+1 for integers) of y_i
            r = max(abs(lo - y[i]), abs(hi - y[i]))
            r0 = r - (1 if i in ints else 0)
            assert r0 <= 0 or r0 * r0 <= F(42, 10) ** 2 * nk * h * h, 'G4'
            newX.append((lo, hi))
        # narrowed box (Prop local)
        Xt = []
        for i in range(n):
            lo, hi = newX[i]
            G = grids[i]
            if i in ints and i in P:
                Z = [v for v in G if marg[i][v] <= U]
                for k in range(len(G) - 1):
                    a, a2 = G[k], G[k + 1]
                    if a2 - a >= 2 and min(marg[i][a], marg[i][a2]) <= U:
                        Z.extend(F(t) for t in range(int(a) + 1, int(a2)))
                Z = [v for v in Z if lo <= v <= hi]
                Xt.append((min(Z), max(Z)))
            elif i not in P:
                a, a2 = G
                if marg[i][a] > U >= marg[i][a2]:
                    Xt.append((a2, a2))
                elif marg[i][a2] > U >= marg[i][a]:
                    Xt.append((a, a))
                else:
                    Xt.append((bounds[i][0], bounds[i][1]))
            else:
                Xt.append((lo, hi))
        assert all(Xt[i][0] <= y[i] <= Xt[i][1] for i in range(n)), 'y in narrowed box'
        Jp = [i for i in range(n) if Xt[i][0] < Xt[i][1]]
        # face candidate
        xt = list(y)
        free = []
        for i in Jp:
            if i in ints:
                continue
            if Xt[i][0] <= bounds[i][0] <= Xt[i][1]:
                xt[i] = bounds[i][0]
            elif Xt[i][0] <= bounds[i][1] <= Xt[i][1]:
                xt[i] = bounds[i][1]
            else:
                free.append(i)
        ok_cand = True
        if free:
            fixed = [i for i in range(n) if i not in free]
            sol = solve_linear([[H[i][k] for k in free] for i in free],
                               [-b[i] - sum(H[i][k] * xt[k] for k in fixed) for i in free])
            if sol is None:
                ok_cand = False
            else:
                for i, v in zip(free, sol):
                    xt[i] = v
        passed = False
        if ok_cand and all(Xt[i][0] <= xt[i] <= Xt[i][1] for i in range(n)) and val(H, b, cst, xt) <= U:
            zt = grad(H, b, xt)
            mu_ = {}
            good = True
            for i in Jp:
                lo, hi = Xt[i]
                if xt[i] == lo and zt[i] >= 0:
                    mu_[i] = zt[i] / (hi - lo)
                elif xt[i] == hi and zt[i] <= 0:
                    mu_[i] = -zt[i] / (hi - lo)
                elif lo < xt[i] < hi and zt[i] == 0:
                    mu_[i] = F(0)
                elif i in ints:
                    mu_[i] = -abs(zt[i])
                else:
                    good = False
            if good:
                passed = is_psd([[H[i][k] + (2 * mu_[i] if i == k else 0) for k in Jp] for i in Jp])
        if passed:
            assert val(H, b, cst, xt) == OPT, 'soundness'
        if h * h * nk <= m0 * m0:
            if stages_hit == 0:
                FIRST_HIT.append(j)
            stages_hit += 1
            for i in range(n):
                if i in ints or i not in P:
                    assert Xt[i] == (xs[i], xs[i]), ('narrowed singleton', i)
            assert sorted(Jp) == sorted(J0 + A), 'J+'
            assert ok_cand and tuple(xt) == tuple(xs), 'face candidate = x*'
            assert passed, 'test passes'
            if stages_hit >= 2:
                return 'checked'
        X = newX
        c = list(y)
    return 'not-reached'


def certified_g(H, b, bounds, ints, xs):
    n = len(xs)
    z = grad(H, b, xs)
    M = []
    for i in range(n):
        if i not in ints and bounds[i][0] < xs[i] < bounds[i][1]:
            M.append(F(0))
        elif i not in ints or (xs[i] == bounds[i][0] and z[i] >= 0) or (xs[i] == bounds[i][1] and z[i] <= 0):
            M.append(abs(z[i]) / (bounds[i][1] - bounds[i][0]))
        else:
            M.append(-abs(z[i]))
    N = [[H[i][j] + (2 * M[i] if i == j else 0) for j in range(n)] for i in range(n)]
    import numpy as np
    lam = min(np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in N])))
    if lam <= 1e-6:
        return None
    g = F(lam / 2 * 0.98).limit_denominator(1000)
    if g <= 0 or not is_psd([[N[i][j] - (2 * g if i == j else 0) for j in range(n)] for i in range(n)]):
        return None
    return g


def main():
    rng = Random(9031)
    counts = {}
    for trial in range(3000):
        n = rng.choice((2, 2, 3))
        H = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = F(rng.randint(-4, 8), rng.choice((1, 2)))
            for j in range(i):
                if rng.random() < 0.7:
                    H[i][j] = H[j][i] = F(rng.randint(-4, 4), rng.choice((1, 2, 4)))
        b = [F(rng.randint(-6, 6), rng.choice((1, 2, 3))) for _ in range(n)]
        ints = set(rng.sample(range(n), rng.randint(0, 1 if n == 2 else 2)))
        bounds = []
        for i in range(n):
            if i in ints:
                lo = rng.randint(-2, 0)
                bounds.append((F(lo), F(lo + rng.randint(1, 4))))
            else:
                lo = F(rng.randint(-2, 0), rng.choice((1, 2)))
                bounds.append((lo, lo + F(rng.randint(1, 3), rng.choice((1, 2)))))
        cst = F(0)
        OPT, pts = exact_minimum(H, b, cst, bounds, ints)
        if len(pts) != 1:
            continue
        xs = tuple(F(v) for v in pts[0])
        g = certified_g(H, b, bounds, ints, xs)
        if g is None:
            counts['no-cert'] = counts.get('no-cert', 0) + 1
            continue
        L = max(max(H[i][i], 0) for i in range(n))
        if L / g > 40:
            counts['kappa>40'] = counts.get('kappa>40', 0) + 1
            continue
        res = run_instance(H, b, cst, bounds, ints, xs, g, [])
        counts[res] = counts.get(res, 0) + 1
        if counts.get('checked', 0) >= 120:
            break
    print(counts)
    hist = {}
    for j in FIRST_HIT:
        hist[j] = hist.get(j, 0) + 1
    print('first stage with h_j <= h*:', dict(sorted(hist.items())))
    assert counts.get('checked', 0) >= 50
    print('ALL PASS')


if __name__ == '__main__':
    main()
