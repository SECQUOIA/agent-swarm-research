"""S1: replay the certificates of the EX runs that supply S1's reference values.

run_all.py (task_localized) runs EX (`solve_exact`) on the 30 S1 instances
and uses its status, value and stage count, but does not pass the EX
certificate to the checker. This script reruns EX with the same arguments,
checks that status, value and completed stages equal those in
results/S1_localized.csv, and replays the certificate with
verify_certificate.

    python3 replay_s1_ex.py            -> results/S1_ex_replay.csv

At most 4 worker processes; well under a minute of wall time.
"""
import os
for _var in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_var] = '1'

import csv
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from instances import random_small  # noqa: E402
from exact_output import solve_exact  # noqa: E402
from verify_certificate import verify_certificate  # noqa: E402


def s1_specs():
    """The S1 instances of run_all.design(), in the same order."""
    specs, seed = [], 7000
    for n in (4, 6, 8, 12, 16):
        for kind in ('path', 'tree', 'band2'):
            for _ in range(2):
                seed += 1
                specs.append((n, kind, 1 + (n >= 8), seed))
    return specs


def run(spec):
    n, kind, n_int, seed = spec
    problem = random_small(n, kind, n_int, seed)
    ex = solve_exact(problem, time_limit=60, max_rounds=12, max_stages=3000,
                     max_table_states=300000)
    t0 = time.perf_counter()
    try:
        valid = verify_certificate(ex, max_table_states=10 ** 7)['valid']
    except Exception as exc:  # record, never hide, a failed replay
        valid = repr(exc)
    return {'name': problem.name, 'status': ex['status'], 'value': ex['upper'],
            'stages': ex['stats']['completed_stages'], 'replay_valid': valid,
            'replay_s': round(time.perf_counter() - t0, 3)}


def main():
    with ProcessPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run, s1_specs()))
    saved = {r['name']: r for r in csv.DictReader(open(HERE / 'results' / 'S1_localized.csv'))}
    for r in rows:
        s = saved[r['name']]
        r['as_in_S1'] = (r['status'] == s['height_rule_status']
                         and F(r['value']) == F(s['height_rule_value'])
                         and r['stages'] == int(s['height_rule_stages']))
    with open(HERE / 'results' / 'S1_ex_replay.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} EX runs; exact: {sum(r['status'] == 'exact' for r in rows)}; "
          f"status, value and stages as in S1_localized.csv: {sum(r['as_in_S1'] for r in rows)}; "
          f"replays valid: {sum(r['replay_valid'] is True for r in rows)}")


if __name__ == '__main__':
    main()
