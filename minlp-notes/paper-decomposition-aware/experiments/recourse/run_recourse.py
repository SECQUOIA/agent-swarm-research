"""Plain corrected grids versus certified recourse on the recourse fixtures.

Instances: the fixed diagnostic corpus of research-20261002-decomposition
(completion/benchmarks/corpus.py).  For each instance we run the plain grid
solver and the recourse pipeline (affine recognition, min-cut residual or
convex value factors), replay both certificates with the independent
checkers, and record status, gap, table states and times.
    python3 run_recourse.py   ->  results.json, results.csv (next to this file)
"""
import csv, json, os, platform, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))  # outputs are written here, whatever the cwd
ROOT = os.path.abspath(os.path.join(HERE, '../../../research-20261002-decomposition'))
sys.path.insert(0, os.path.join(ROOT, 'solver'))
sys.path.insert(0, os.path.join(ROOT, 'completion/benchmarks'))
sys.path.insert(0, os.path.join(ROOT, 'completion/theory/piecewise-recourse'))
from corpus import cases                                   # noqa: E402
from certified_grid import BoxQP, solve                    # noqa: E402
from decomposition import decompose_qp                     # noqa: E402
from verify_certificate import verify_certificate          # noqa: E402
from recourse import solve_with_recourse                   # noqa: E402
from verify_recourse import verify_pipeline                # noqa: E402

EPS = F(1, 1024)
CASES = ['affine_star_5_shuffled', 'affine_star_17_shuffled', 'piecewise_convex_1',
         'piecewise_convex_100', 'dense_mincut_7', 'dense_mincut_33']


def problem(name):
    p = cases()[name]
    d = decompose_qp(p.A)
    return p, BoxQP(p.A, p.b, p.bounds, p.integers, d['bags'], d['edges'], constant=p.c, name=p.name), max(map(len, d['bags']))


def states(cert):
    st = cert.get('stats') or {}
    if 'completed_table_states' in st:
        return st['completed_table_states']
    inner = cert.get('reduced_certificate') or cert.get('certificate') or {}
    st = inner.get('stats') or {}
    return st.get('completed_table_states', st.get('table_states'))


rows = []
for name in CASES:
    p, prob, bag = problem(name)
    ref = p.description
    # plain grid
    t0 = time.perf_counter()
    g = solve(prob, epsilon=EPS, time_limit=20, max_stages=128, max_table_states=200000)
    t1 = time.perf_counter(); okg = verify_certificate(g); t2 = time.perf_counter()
    rows.append({'case': name, 'n': len(p.b), 'bag': bag, 'method': 'grid', 'status': g['status'],
                 'gap': float(F(g['gap'])), 'states': states(g), 'solve_s': round(t1 - t0, 3),
                 'replay_s': round(t2 - t1, 3), 'replay_ok': bool(okg)})
    print(rows[-1], flush=True)
    opts = {}
    if name.startswith('piecewise'):
        opts = {'backend': 'convex', 'blocks': [[1, 2]], 'discover': False}
    t0 = time.perf_counter()
    r = solve_with_recourse(prob, epsilon=EPS, time_limit=20, max_stages=128, max_table_states=200000, **opts)
    t1 = time.perf_counter(); okr = verify_pipeline(r); t2 = time.perf_counter()
    rows.append({'case': name, 'n': len(p.b), 'bag': bag, 'method': 'recourse' + ('-convex' if opts else ''),
                 'status': r.get('status'), 'gap': float(F(r['gap'])) if r.get('gap') is not None else None,
                 'states': states(r), 'solve_s': round(t1 - t0, 3), 'replay_s': round(t2 - t1, 3),
                 'replay_ok': bool(okr), 'lower': r.get('lower'), 'upper': r.get('upper')})
    print(rows[-1], flush=True)

meta = {'python': sys.version, 'platform': platform.platform(), 'epsilon': str(EPS), 'load': os.getloadavg()}
json.dump({'meta': meta, 'rows': rows}, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
with open(os.path.join(HERE, 'results.csv'), 'w', newline='') as f:
    keys = sorted({k for r in rows for k in r})
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
