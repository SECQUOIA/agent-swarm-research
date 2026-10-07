"""R8 check: the chain G_m starts at its minimizer (lower corner).

Re-run the unchanged solver with a warm start at the upper corner (so the
lower corner, the minimizer 0, is not among the polishing starts) and compare
stages, max grid nodes, table states and the initial upper bound.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments/chain'))
from run_chain import chain, solve, verify_certificate

for m in (4, 8, 16, 32):
    p = chain(m)
    for label, ws in (('default (start at lower corner = x*)', None),
                      ('warm start at upper corner', [hi for lo, hi in p.bounds])):
        t0 = time.perf_counter()
        cert = solve(p, epsilon=F(1, 1000), time_limit=120, max_stages=200,
                     max_table_states=10**7, warm_start=ws)
        t1 = time.perf_counter()
        ok = verify_certificate(cert)['valid']
        st = cert['stages']
        print(f"m={m:2d} {label:38s} status={cert['status']} U0={float(F(cert['initial']['upper'])):.3g} "
              f"stages={len(st)} trials={len({s['trial'] for s in st})} "
              f"max_nodes={max(len(g) for s in st for g in s['grids'])} "
              f"states={cert['stats']['completed_table_states']} solve={t1-t0:.2f}s replay_ok={ok}")
