"""R8 check: how many stages does the height-rule acceptance need in ONE run?

exact_output.solve_exact restarts the grid solver from scratch for each
precision q = 4, 8, ..., 512, so its stage count (up to 542 in S1) includes
all rounds.  Here one run of the unchanged solver targets the acceptance
threshold 1/(2*Omega*W) directly, for the code's Omega (row-norm Hadamard)
and for the paper's Omega (eq:exact-constants, diagonal product).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, csv, math, time
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/process/w2/checks'))
from instances import random_small
from exact_output import rational_heights
from certified_grid import solve
from r8_omega_lib import paper_omega

rows = {r['name']: r for r in csv.DictReader(open(
    (_PUBLIC_REPO + '/paper-decomposition-aware/experiments/results/S1_localized.csv')))}
# S1 design: seed 7000+, n in (4,6,8,12,16), kinds, 2 reps; pick the n=16 ones with 542 stages
targets = {'random_band2_n16_s7029', 'random_band2_n16_s7030', 'random_path_n16_s7026',
           'random_tree_n16_s7028', 'random_band2_n8_s7017'}
seed = 7000
for n in (4, 6, 8, 12, 16):
    for kind in ('path', 'tree', 'band2'):
        for rep in range(2):
            seed += 1
            name = f'random_{kind}_n{n}_s{seed}'
            if name not in targets:
                continue
            p = random_small(n, kind, 1 + (n >= 8), seed)
            W = F(rows[name]['height_rule_value']).denominator
            for label, om in (('code', int(F(rational_heights(p)['value']))), ('paper', paper_omega(p))):
                eps = F(1, 2 * om * W)
                t0 = time.perf_counter()
                c = solve(p, epsilon=eps, max_stages=2000, time_limit=120, max_table_states=300000,
                          convex_presolve=False)
                print(f"{name:26s} Omega={label:5s} bits={math.log2(om*W):6.1f} single-run stages="
                      f"{c['stats']['completed_stages']:4d} status={c['status']} "
                      f"({time.perf_counter()-t0:.1f}s)  solve_exact stages={rows[name]['height_rule_stages']}",
                      flush=True)
