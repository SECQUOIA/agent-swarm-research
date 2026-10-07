"""Chain G_m started away from its minimizer.

The minimizer 0 of G_m is the lower corner, which is the solver's default
starting point. This run uses the opposite (upper) corner as the warm start,
so the lower corner is not among the three polishing starts (warm start,
upper corner, midpoint). Same settings as run_chain.py otherwise.
    python3 run_chain_warmstart.py   ->  results_warmstart.csv
"""
import csv, os, sys, time
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_chain import EPS, MS, chain, solve, verify_certificate  # noqa: E402


def main():
    rows = []
    for m in MS:
        p = chain(m)
        t0 = time.perf_counter()
        cert = solve(p, epsilon=EPS, time_limit=120, max_stages=200, max_table_states=10 ** 7,
                     warm_start=[hi for lo, hi in p.bounds])
        t1 = time.perf_counter()
        ok = verify_certificate(cert)
        t2 = time.perf_counter()
        st = cert['stages']
        rows.append({'m': m, 'n': 2 * m, 'start': 'upper corner', 'status': cert['status'],
                     'gap': float(Fr(cert['gap'])), 'initial_upper': cert['initial']['upper'],
                     'stages': len(st), 'trials': len({s['trial'] for s in st}),
                     'table_states': cert['stats']['completed_table_states'],
                     'max_grid_nodes': max((len(g) for s in st for g in s['grids']), default=0),
                     'solve_s': round(t1 - t0, 3), 'replay_s': round(t2 - t1, 3), 'replay_ok': bool(ok)})
        print(rows[-1], flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'results_warmstart.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    main()
