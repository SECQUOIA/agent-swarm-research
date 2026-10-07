"""R8 check: QPLIB_3852 with a larger table cap.

The paper reports that both QPLIB runs stopped at the table limit before the
first stage. The cap used there was 3e4 states per stage. For a binary QP the
stage-0 grids are {0,1} with zero correction, so stage 0 is an exact DP. Here
the unchanged solver runs with a 1e7 cap; the certificate is replayed.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time, json, resource
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver/extra-benchmarks'))
from corpus import read_qbn
from certified_grid import BoxQP, solve
from verify_certificate import verify_certificate

p = read_qbn('3852')
prob = BoxQP(p.A, p.b, p.bounds, p.integers, constant=p.c, name=p.name)
print('max bag size', max(map(len, prob.bags)), flush=True)
t0 = time.perf_counter()
cert = solve(prob, epsilon=F(1, 50), time_limit=480, max_stages=4, max_table_states=10**7,
             convex_presolve=False)
t1 = time.perf_counter()
print(json.dumps({k: cert[k] for k in ('status', 'lower', 'upper', 'gap')}), cert['stats'],
      'solve_s=%.1f' % (t1 - t0), flush=True)
t2 = time.perf_counter()
chk = verify_certificate(cert, max_table_states=10**7)
print('replay valid', chk['valid'], 'replay_s=%.1f' % (time.perf_counter() - t2),
      'maxrss_GB=%.2f' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6), flush=True)
print('library solution value (min form):', -234)
