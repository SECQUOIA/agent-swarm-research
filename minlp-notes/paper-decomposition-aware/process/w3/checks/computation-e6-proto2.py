"""Prototype: does a sign-aware variant of the growth certificate (drop A-A couplings of favourable sign) help?"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/process/w3/checks'))
import importlib.util
spec = importlib.util.spec_from_file_location('p', (_PUBLIC_REPO + '/paper-decomposition-aware/process/w3/checks/computation-e6-proto.py'))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
from certified_grid import solve
from localized import candidate

def lam(M):
    return float(np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in M]))[0])

for kind in ('path', 'band2'):
    for n in (8, 12, 16, 24):
        for seed in range(1, 6):
            pr = p.gen(kind, n, 1000 * n + seed + (0 if kind == 'path' else 500))
            c = solve(pr, epsilon=F(1, 2**40), max_stages=400, time_limit=60, max_table_states=10**6, convex_presolve=False)
            x = candidate(pr, tuple(F(v) for v in c['point']))
            H = pr.A
            z = [pr.b[i] + sum(H[i][j] * x[j] for j in range(n)) for i in range(n)]
            S = [i for i in range(n) if -1 < x[i] < 1]; A = [i for i in range(n) if i not in S]
            sg = {i: (1 if x[i] == -1 else -1) for i in A}  # feasible d_i has sign sg[i]
            mu = {i: abs(z[i]) / 2 for i in A}
            K = [[H[i][j] + (2 * mu.get(i, 0) if i == j else 0) for j in range(n)] for i in range(n)]
            K2 = [row[:] for row in K]
            for i in A:
                for j in A:
                    if i != j and sg[i] * sg[j] * K[i][j] > 0:
                        K2[i][j] = 0
            print(kind, n, seed, f'nA={len(A)} lam(H+2M)={lam(K):.3f} lam(signaware)={lam(K2):.3f} lam(H_SS)={lam([[H[i][j] for j in S] for i in S]) if S else float("nan"):.3f}')
