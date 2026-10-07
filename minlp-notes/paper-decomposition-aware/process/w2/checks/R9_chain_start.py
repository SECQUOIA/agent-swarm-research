"""R9: chain G_m starts at its minimizer (lower corner). Compare default start
with a warm start at the upper corner (m=4,8,16)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments/chain'))
from run_chain import chain, solve, verify_certificate
for m in (4, 8, 16):
    p = chain(m)
    for label, ws in (('lower corner (= x*)', None), ('upper corner', [hi for lo, hi in p.bounds])):
        t0 = time.perf_counter()
        cert = solve(p, epsilon=F(1, 1000), time_limit=60, max_stages=200,
                     max_table_states=10**7, warm_start=ws)
        st = cert['stages']
        print(f"m={m:2d} start={label:20s} status={cert['status']} U0={float(F(cert['initial']['upper'])):.3g} "
              f"stages={len(st)} max_nodes={max(len(g) for s in st for g in s['grids'])} "
              f"states={cert['stats']['completed_table_states']} t={time.perf_counter()-t0:.2f}s "
              f"replay={verify_certificate(cert)['valid']}", flush=True)
