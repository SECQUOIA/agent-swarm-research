from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, time, json
from fractions import Fraction as Fr
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))
from certified_grid import BoxQP, solve
from verify_certificate import verify_certificate

def chain(m):
    n = 2*m
    S = lambda t: 2*(t-1)
    Z = lambda t: 2*(t-1)+1
    A = [[Fr(0)]*n for _ in range(n)]
    b = [Fr(0)]*n
    def addsq(coefs):  # add (sum c_i x_i)^2 -> A += 2 a a^T
        for i,ci in coefs.items():
            for j,cj in coefs.items():
                A[i][j] += 2*ci*cj
    for t in range(1, m+1):
        r = {S(t): Fr(1), Z(t): Fr(-1)}
        if t >= 2: r[S(t-1)] = Fr(-2)
        addsq(r)
        b[Z(t)] += Fr(1, 8)
        A[Z(t)][Z(t)] += Fr(-2, 8)
    A[S(m)][S(m)] += 2
    bounds = []
    for t in range(1, m+1):
        bounds.append((0, 2**t - 1)); bounds.append((0, 1))
    bags = [(S(1), Z(1))] + [(S(t-1), S(t), Z(t)) for t in range(2, m+1)]
    edges = [(k, k+1) for k in range(len(bags)-1)]
    return BoxQP(A=A, b=b, bounds=bounds, integers=[], bags=bags, edges=edges, name=f"chain{m}")

for m in [int(a) for a in sys.argv[1:]]:
    p = chain(m)
    t0 = time.time()
    cert = solve(p, epsilon=Fr(1, 1000), time_limit=20, max_stages=80, max_table_states=200000)
    dt = time.time() - t0
    st = cert.get('stats', {})
    print(m, cert['status'], cert['gap'], round(dt, 2), {k: st[k] for k in list(st)[:12]})
