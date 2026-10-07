"""Reviewer r1 (second reviewer): independent recomputation of the family ratios on random corners
(note, Section 7.1) and own exact certificates for the 12 orbit misses.  Does not import stream code.

Orbit: max t s.t. sym(G Mbar) >= I, sym(G V_j) >= t I over the vertices V_j = sbar + (z/w_j) p_j,
bisection in z (no preconditioning; explicit G gives a lower bound by its exact one-cut bound).
Point rule: G = Psym Mbar^{-1}.  BCM: dense scan phi (20000 points) + golden refinement.
For each orbit miss: rays rounded (denominator 10^6, after division by w_j as in the note),
z_lo certified by exact min of det over T_{z_lo} (own face enumeration over all affinely
independent subsets), z_up by an own rational PD dual certificate (exact projection).
Usage: python3 rev_orbit.py LOGDIR NSAMPLE
"""
import itertools
import json
import sys
from fractions import Fraction as Fr

import cvxpy as cp
import numpy as np

LOGDIR, NS = sys.argv[1], int(sys.argv[2])
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])


def det4(s):
    return s[0] * s[3] - s[1] * s[2]


def m2(s):
    return np.array([[s[0], s[1]], [s[2], s[3]]], float)


def step(G, s, p):
    A = G @ m2(s); A = (A + A.T) / 2
    B = G @ m2(p); B = (B + B.T) / 2
    if np.linalg.eigvalsh(A)[0] <= 0:
        return -np.inf
    Li = np.linalg.inv(np.linalg.cholesky(A))
    mn = np.linalg.eigvalsh(Li @ B @ Li.T)[0]
    return np.inf if mn >= 0 else -1.0 / mn


def bound(G, s, P, w):
    return min(w[j] * step(G, s, P[:, j]) for j in range(P.shape[1]))


def lmi_best(s, P, w, zk, fam, iters=34):
    Mb = m2(s)
    if fam == 'orbit':
        Gv = cp.Variable((2, 2)); G = Gv
    else:
        Ps = cp.Variable((2, 2), symmetric=True); G = Ps @ np.linalg.inv(Mb)
    t = cp.Variable(); z = cp.Parameter(nonneg=True)
    se = lambda X: 0.5 * (G @ X + (G @ X).T)
    cons = [se(Mb) >> np.eye(2), t <= 1] + [se(Mb) + (z / w[j]) * se(m2(P[:, j])) >> t * np.eye(2) for j in range(P.shape[1])]
    prob = cp.Problem(cp.Maximize(t), cons)

    def feas(zz):
        z.value = zz
        for solver in ('CLARABEL', 'SCS'):
            try:
                prob.solve(solver=solver)
            except Exception:
                continue
            if t.value is not None:
                return (G.value if t.value >= -1e-9 else None)
        return None
    best = -np.inf
    Gz = feas(zk * (1 - 1e-7))
    if Gz is not None:
        return min(bound(Gz, s, P, w), zk) / zk, 1.0
    lo, hi = 0.0, 1.0
    for _ in range(iters):
        mid = (lo + hi) / 2
        Gm = feas(mid * zk)
        if Gm is not None:
            lo = mid
            try:
                best = max(best, bound(Gm, s, P, w))
            except np.linalg.LinAlgError:
                pass
        else:
            hi = mid
    return min(best, zk) / zk, hi


def bcm_best(s, P, w):
    def val(ph):
        G = np.cos(ph) * np.eye(2) + np.sin(ph) * J2
        try:
            return bound(G, s, P, w)
        except np.linalg.LinAlgError:
            return -np.inf
    grid = np.linspace(0, 2 * np.pi, 20000, endpoint=False)
    v = np.array([val(x) for x in grid])
    k = int(np.argmax(v)); lo, hi = grid[k] - 2 * np.pi / 20000, grid[k] + 2 * np.pi / 20000
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(60):
        a = hi - gr * (hi - lo); b = lo + gr * (hi - lo)
        if val(a) >= val(b):
            hi = b
        else:
            lo = a
    return max(v[k], val((lo + hi) / 2))


# ---------------- exact tools (own)
def Bq(s, t):
    return Fr(1, 2) * (s[0] * t[3] + s[3] * t[0] - s[1] * t[2] - s[2] * t[1])


def solve(A, b):
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def min_det_polytope(V):
    """min of det over conv(V): over subsets with nonsingular face KKT systems (affinely dependent
    subsets are singular and are covered by Caratheodory; singular independent faces attain their
    minimum on lower faces)."""
    n = len(V); H = [[Bq(V[i], V[j]) for j in range(n)] for i in range(n)]
    best = None
    for r in range(1, min(n, 5) + 1):
        for F in itertools.combinations(range(n), r):
            if r == 1:
                mu = [Fr(1)]
            else:
                A = [[2 * H[i][j] for j in F] + [Fr(-1)] for i in F] + [[Fr(1)] * r + [Fr(0)]]
                sol = solve(A, [Fr(0)] * r + [Fr(1)])
                if sol is None:
                    continue
                mu = sol[:r]
                if any(x <= 0 for x in mu):
                    continue
            val = sum(mu[a] * mu[b] * H[F[a]][F[b]] for a in range(r) for b in range(r))
            best = val if best is None or val < best else best
    return best


def own_dual(Vs):
    nv = len(Vs)
    Vn = [m2([float(x) for x in v]) for v in Vs]
    Ys = [cp.Variable((2, 2), symmetric=True) for _ in range(nv)]
    t = cp.Variable()
    cons = [Y >> t * np.eye(2) for Y in Ys] + [sum(cp.trace(Y) for Y in Ys) == 1, sum(Vn[i] @ Ys[i] for i in range(nv)) == 0]
    for solver in ('CLARABEL', 'SCS'):
        try:
            cp.Problem(cp.Maximize(t), cons).solve(solver=solver); break
        except Exception:
            continue
    if t.value is None or t.value <= 0:
        return False
    rows = []
    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        row = []
        for v in Vs:
            Vm = [[v[0], v[1]], [v[2], v[3]]]
            row += [Vm[i][0] if j == 0 else Fr(0), (Vm[i][1] if j == 0 else Fr(0)) + (Vm[i][0] if j == 1 else Fr(0)),
                    Vm[i][1] if j == 1 else Fr(0)]
        rows.append(row)
    for den in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10):
        y = []
        for Y in Ys:
            y += [Fr(Y.value[0, 0]).limit_denominator(den), Fr(Y.value[0, 1]).limit_denominator(den), Fr(Y.value[1, 1]).limit_denominator(den)]
        r = [sum(a * b for a, b in zip(row, y)) for row in rows]
        AAt = [[sum(a * b for a, b in zip(ri, rj)) for rj in rows] for ri in rows]
        lam = solve(AAt, r)
        if lam is None:
            continue
        y = [y[k] - sum(lam[i] * rows[i][k] for i in range(4)) for k in range(len(y))]
        assert all(sum(a * b for a, b in zip(row, y)) == 0 for row in rows)
        if all(y[3 * k] > 0 and y[3 * k] * y[3 * k + 2] - y[3 * k + 1] ** 2 > 0 for k in range(nv)):
            return True
    return False


rng_s = np.random.default_rng(777)
for name, N in (('exp_random_N4_a.jsonl', 4), ('exp_random_N4_b.jsonl', 4), ('exp_random_N8.jsonl', 8)):
    recs = [json.loads(l) for l in open(LOGDIR + '/' + name)]
    by = {r['idx']: r for r in recs if r.get('zK') is not None}
    miss = {i for i, r in by.items() if r['ratios']['orbit'] < 1 - 1e-5}
    sample = set(rng_s.choice(sorted(set(by) - miss), size=min(NS, len(by) - len(miss)), replace=False).tolist()) | miss
    rng = np.random.default_rng(recs[0]['seed'])
    tries = 0; dmax = {'orbit': 0.0, 'pr': 0.0, 'bcm': 0.0}
    while tries < max(sample):
        tries += 1
        s = rng.normal(size=4)
        if det4(s) <= 0:
            continue
        P = rng.normal(size=(4, N)); w = rng.uniform(0.2, 2.0, N)
        if tries not in sample:
            continue
        r = by[tries]; zk = r['zK']
        res = {'orbit': lmi_best(s, P, w, zk, 'orbit')[0], 'pr': lmi_best(s, P, w, zk, 'pr')[0],
               'bcm': min(bcm_best(s, P, w), zk) / zk}
        for k in dmax:
            dmax[k] = max(dmax[k], abs(res[k] - r['ratios'][k]))
        line = '%s idx %3d: orbit own %.6f log %.6f | pr own %.6f log %.6f | bcm own %.6f log %.6f' % (
            name, tries, res['orbit'], r['ratios']['orbit'], res['pr'], r['ratios']['pr'], res['bcm'], r['ratios']['bcm'])
        if tries in miss:
            sb = [Fr(x).limit_denominator(10 ** 6) for x in s]
            Pq = [[Fr(x).limit_denominator(10 ** 6) for x in P[:, j] / w[j]] for j in range(N)]
            zlo = Fr(int(np.floor(zk * (1 - 1e-5) * 10 ** 8)), 10 ** 8)
            V = [sb] + [[sb[c] + zlo * Pq[j][c] for c in range(4)] for j in range(N)]
            mlo = min_det_polytope(V)
            zup = None
            for du in (2e-6, 2e-5, 2e-4):
                z = Fr(int(np.ceil((res['orbit'] + du) * zk * 10 ** 8)), 10 ** 8)
                Vu = [sb] + [[sb[c] + z * Pq[j][c] for c in range(4)] for j in range(N)]
                if own_dual(Vu):
                    zup = z; break
            line += ' | MISS rounded corner: det>0 on T_zlo: %s; own dual cert at z_up: %s; exact ratio <= %s' % (
                mlo > 0, zup is not None, ('%.6f' % float(zup / zlo)) if (zup is not None and mlo > 0) else 'none')
        print(line, flush=True)
    print('%s: max |own - log| ratio: %s' % (name, {k: '%.2e' % v for k, v in dmax.items()}), flush=True)
