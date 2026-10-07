"""R8 probe: the paper's showcase Example ex:family (coupled indefinite blocks,
2^m strict local minima) is not run in the computational section.  Run the
unchanged default solver (capped schedule, eps = 1e-6) on Gamma = path of m
blocks, replay the certificate, and check the planted value -3m/2.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))
from certified_grid import BoxQP, solve
from verify_certificate import verify_certificate

def family(m):
    n = 3 * m
    A = [[F(0)] * n for _ in range(n)]
    b = [F(0)] * n
    Delta = 2 if m > 2 else 1
    u = lambda k: 3 * k; v = lambda k: 3 * k + 1; r = lambda k: 3 * k + 2
    for k in range(m):
        A[u(k)][u(k)] += F(5, 2); A[v(k)][v(k)] += 2; A[r(k)][r(k)] += 2
        A[u(k)][v(k)] = A[v(k)][u(k)] = F(-4)
        A[u(k)][r(k)] = A[r(k)][u(k)] = F(-1)
        b[u(k)] += F(1, 4); b[v(k)] += F(1, 4)
    for k in range(m - 1):  # (u_k - u_{k+1})^2 / (16 Delta)
        w = F(1, 16 * Delta)
        A[u(k)][u(k)] += 2 * w; A[u(k + 1)][u(k + 1)] += 2 * w
        A[u(k)][u(k + 1)] = A[u(k + 1)][u(k)] = -2 * w
    return BoxQP(A=A, b=b, bounds=[(0, 1)] * n, integers=[], name=f'family_path{m}')

for m in (4, 8, 16, 32):
    p = family(m)
    t0 = time.perf_counter()
    c = solve(p, epsilon=F(1, 10**6), max_stages=200, time_limit=120, max_table_states=10**6)
    t1 = time.perf_counter()
    ok = verify_certificate(c, max_table_states=10**7)['valid']
    t2 = time.perf_counter()
    st = c['stages']
    print(f"m={m:2d} n={3*m:3d} bag={max(map(len,p.bags))} status={c['status']} gap={float(F(c['gap'])):.1e} "
          f"upper==-3m/2: {F(c['upper']) == F(-3*m, 2)} stages={len(st)} trials={len({s['trial'] for s in st})} "
          f"max_nodes={max((len(g) for s in st for g in s['grids']), default=0)} "
          f"states={c['stats']['completed_table_states']} solve={t1-t0:.2f}s replay={t2-t1:.2f}s valid={ok}", flush=True)
