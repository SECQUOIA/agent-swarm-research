"""Two binary QPLIB instances with the unchanged solver (Section 11, Limits).

For a binary QP every coordinate grid is {0,1} with no correction, so the
first stage is an exact dynamic program over the decomposition. This script
records the minimum-fill bag sizes, the number of stage-0 table entries
(sum over bags of 2^|bag|), and, for QPLIB_3852, one solver run with a cap of
10^7 table entries per stage. The certificate of that run is not replayed by
default: the reference checker is too slow at this size (see README).

    python3 run_qplib.py            -> results.json
    python3 run_qplib.py --replay   (also replays the QPLIB_3852 certificate)
"""
import json, os, platform, resource, sys, time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOLVER = HERE.parents[2] / 'research-20261002-decomposition' / 'solver'
sys.path.insert(0, str(SOLVER))
sys.path.insert(0, str(SOLVER / 'extra-benchmarks'))
from corpus import read_qbn                        # noqa: E402
from certified_grid import BoxQP, solve            # noqa: E402
from decomposition import decompose_qp             # noqa: E402
from verify_certificate import verify_certificate  # noqa: E402

LIBRARY_VALUE = {'3852': 234}   # QPLIB objective (maximization) of the best known solution


def main():
    out = {'meta': {'python': sys.version, 'platform': platform.platform(),
                    'load_start': os.getloadavg()}, 'instances': {}}
    for code in ('3852', '5881'):
        p = read_qbn(code)
        d = decompose_qp(p.A)
        sizes = [len(b) for b in d['bags']]
        out['instances'][code] = {'n': len(p.b), 'bags': len(sizes), 'max_bag_size': max(sizes),
                                  'stage0_table_entries': sum(2 ** k for k in sizes)}
        print(code, out['instances'][code], flush=True)
    p = read_qbn('3852')
    prob = BoxQP(p.A, p.b, p.bounds, p.integers, constant=p.c, name=p.name)
    t0 = time.perf_counter()
    cert = solve(prob, epsilon=F(1, 50), time_limit=900, max_stages=4, max_table_states=10 ** 7,
                 convex_presolve=False)
    solve_s = time.perf_counter() - t0
    rec = {k: cert[k] for k in ('status', 'lower', 'upper', 'gap')}
    rec.update(stats=cert['stats'], solve_s=solve_s, table_cap=10 ** 7,
               library_value_min_form=-LIBRARY_VALUE['3852'],
               matches_library=F(cert['upper']) == -LIBRARY_VALUE['3852'],
               maxrss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
    print(rec, flush=True)
    if '--replay' in sys.argv:
        t1 = time.perf_counter()
        rec['replay_valid'] = verify_certificate(cert, max_table_states=10 ** 7)['valid']
        rec['replay_s'] = time.perf_counter() - t1
    out['instances']['3852']['run'] = rec
    out['meta']['load_end'] = os.getloadavg()
    (HERE / 'results.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
