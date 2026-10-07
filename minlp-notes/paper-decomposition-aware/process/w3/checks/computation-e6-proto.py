"""Prototype for E6: random unplanted continuous box QPs; growth certificate rate and kappa bracket."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time
from fractions import Fraction as F
from random import Random
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
from certified_grid import BoxQP, solve
from instances import graph_edges, is_psd
from localized import candidate

def gen(kind, n, seed):
    rng = Random(seed)
    edges = graph_edges(kind, n, rng)
    H = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = F(rng.randint(-4, 8), 2)
    for i, j in edges:
        H[i][j] = H[j][i] = F(rng.choice((-1, 1)) * rng.randint(1, 6), 4)
    b = [F(rng.randint(-8, 8), 4) for _ in range(n)]
    return BoxQP(A=H, b=b, bounds=[(F(-1), F(1))] * n, integers=[], name=f'rand_{kind}_n{n}_s{seed}')

def cert(p, x):
    n = len(x); H = p.A
    z = [p.b[i] + sum(H[i][j] * x[j] for j in range(n)) for i in range(n)]
    S = [i for i in range(n) if p.bounds[i][0] < x[i] < p.bounds[i][1]]
    A = [i for i in range(n) if i not in S]
    if any(z[i] != 0 for i in S): return 'zeta_S!=0', None
    for i in A:
        if (x[i] == p.bounds[i][0] and z[i] < 0) or (x[i] == p.bounds[i][1] and z[i] > 0): return 'sign', None
    mu = {i: abs(z[i]) / (p.bounds[i][1] - p.bounds[i][0]) for i in A}
    M = [[H[i][j] + (2 * mu.get(i, 0) if i == j else 0) for j in range(n)] for i in range(n)]
    lm = float(np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in M]))[0])
    if lm <= 0: return f'minorant not PD ({lm:.3g})', None
    gam = F(int(lm / 2 * 0.999 * 2**20), 2**20)
    if not is_psd([[M[i][j] - (2 * gam if i == j else 0) for j in range(n)] for i in range(n)]): return 'ldl fail', None
    L = max(max(H[i][i], 0) for i in range(n))
    # upper bounds on g
    ubs = []
    if S:
        hss = np.array([[float(H[i][j]) for j in S] for i in S]); w, V = np.linalg.eigh(hss)
        v = [F(float(t)).limit_denominator(10**6) for t in V[:, 0]]
        ubs.append(sum(v[a] * H[S[a]][S[c]] * v[c] for a in range(len(S)) for c in range(len(S))) / (2 * sum(t * t for t in v)))
    f0 = p.value(tuple(x))
    for i in A:
        y = list(x); y[i] = p.bounds[i][1] if x[i] == p.bounds[i][0] else p.bounds[i][0]
        ubs.append((p.value(tuple(y)) - f0) / (y[i] - x[i]) ** 2)
    gub = min(ubs)
    return 'ok', (float(max(1, L / gub)), float(max(1, L / gam)), len(S), lm)

if __name__ == '__main__':
    for kind in ('path', 'band2'):
        for n in (8, 12, 16, 24):
            for seed in range(1, 6):
                p = gen(kind, n, 1000 * n + seed + (0 if kind == 'path' else 500))
                t0 = time.perf_counter()
                c = solve(p, epsilon=F(1, 2**40), max_stages=400, time_limit=60, max_table_states=10**6, convex_presolve=False)
                xs = candidate(p, tuple(F(v) for v in c['point']))
                st, info = cert(p, xs) if xs else ('no cand', None)
                lamH = float(np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in p.A]))[0])
                mx = max(len(g) for s in c['stages'] for g in s['grids'])
                print(kind, n, seed, c['status'], len(c['stages']), 'trial', c['stages'][-1]['trial'], 'maxnodes', mx, st, info, f'lamH={lamH:.2f}', f'{time.perf_counter()-t0:.1f}s', flush=True)
