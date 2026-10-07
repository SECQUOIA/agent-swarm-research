"""R8 check: does SCIP's time-limit outcome on paths n >= 32 (E5) come from
numerical tolerances?  Paper formulation, 20 s, absolute gap 1e-6, with
numerics/feastol = numerics/dualfeastol = 1e-9 (variant 'tight'), and the
default tolerances with absolute gap 1e-5 (variant 'gap1e-5').  4 workers.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import os, sys, json, time
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
from fractions import Fraction as F
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))


def run(spec):
    from instances import planted
    from pyscipopt import Model, quicksum
    kind, n, seed, variant = spec
    p, info = planted(kind, n, 4, seed)
    m = Model(); m.hideOutput()
    m.setParam('limits/time', 20.0)
    m.setParam('limits/absgap', 1e-5 if variant == 'gap1e-5' else 1e-6)
    m.setParam('parallel/maxnthreads', 1); m.setParam('randomization/randomseedshift', 0)
    if variant == 'tight':
        m.setParam('numerics/feastol', 1e-9); m.setParam('numerics/dualfeastol', 1e-9)
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi)) for i, (lo, hi) in enumerate(p.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    expr = float(p.constant) + quicksum(float(p.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(p.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in p.interactions)
    m.addCons(t >= expr); m.setObjective(t, 'minimize')
    t0 = time.perf_counter(); m.optimize(); wall = time.perf_counter() - t0
    sol = m.getBestSol()
    pt = tuple(min(max(F(sol[x[i]]), lo), hi) for i, (lo, hi) in enumerate(p.bounds))
    return {'kind': kind, 'n': n, 'seed': seed, 'variant': variant, 'status': m.getStatus(),
            'wall': round(wall, 2), 'primal': m.getPrimalbound(), 'dual': m.getDualbound(),
            'exact_value_scip_point': float(p.value(pt)), 'nodes': m.getNTotalNodes()}


if __name__ == '__main__':
    specs = [('path', n, s, v) for v in ('tight', 'gap1e-5') for n in (32, 64, 128) for s in (101, 202, 303)]
    out = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(run, specs):
            print(json.dumps(r), flush=True); out.append(r)
    json.dump(out, open(os.path.join(os.path.dirname(__file__), 'r8_scip_tight.json'), 'w'), indent=1)
