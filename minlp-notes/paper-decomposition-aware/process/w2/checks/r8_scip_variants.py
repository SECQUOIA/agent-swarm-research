"""R8 check: sensitivity of the SCIP comparison (E5) to the time limit and to
where the objective constant sits.

Variants on the E5 planted instances (kappa_target = 4, seeds 101/202/303):
  paper60 : the paper's formulation (constant inside t >= F(x)), 60 s limit
            (the certified solver's own limit in E5), paths n >= 32 only;
  offset20: t >= F(x) - c with the constant c added as an objective offset,
            20 s limit (as in the paper), all 21 instances.
Everything else as in run_all.task_scip: single thread, absolute gap 1e-6.
The SCIP point is evaluated exactly (clipped to the box), F* = 0.
At most 4 worker processes.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import os, sys, json, time
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
from fractions import Fraction as F
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))

SEEDS = (101, 202, 303)
E5 = [('path', 16), ('tree', 16), ('band2', 12), ('band3', 8), ('path', 32), ('path', 64), ('path', 128)]


def run(spec):
    from instances import planted
    from pyscipopt import Model, quicksum
    kind, n, seed, variant, tl = spec
    p, info = planted(kind, n, 4, seed)
    m = Model(); m.hideOutput()
    m.setParam('limits/time', float(tl)); m.setParam('limits/absgap', 1e-6)
    m.setParam('parallel/maxnthreads', 1)
    try:
        m.setParam('lp/threads', 1)
    except Exception:
        pass
    m.setParam('randomization/randomseedshift', 0)
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi)) for i, (lo, hi) in enumerate(p.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    quad = quicksum(float(p.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(p.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in p.interactions)
    c = float(p.constant)
    if variant == 'paper60':
        m.addCons(t >= c + quad); m.setObjective(t, 'minimize')
    else:
        m.addCons(t >= quad); m.setObjective(t, 'minimize'); m.addObjoffset(c)
    t0 = time.perf_counter(); m.optimize(); wall = time.perf_counter() - t0
    sol = m.getBestSol()
    pt = tuple(min(max(F(sol[x[i]]), lo), hi) for i, (lo, hi) in enumerate(p.bounds))
    exact = p.value(pt)
    return {'kind': kind, 'n': n, 'seed': seed, 'variant': variant, 'status': m.getStatus(),
            'wall': round(wall, 2), 'primal': m.getPrimalbound(), 'dual': m.getDualbound(),
            'exact_value_scip_point': float(exact),
            'true_gap_scip_point_minus_dual': float(exact) - m.getDualbound()}


if __name__ == '__main__':
    specs = [(k, n, s, 'paper60', 60) for k, n in E5 if n >= 32 for s in SEEDS]
    specs += [(k, n, s, 'offset20', 20) for k, n in E5 for s in SEEDS]
    out = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(run, specs):
            print(json.dumps(r), flush=True); out.append(r)
    json.dump(out, open(os.path.join(os.path.dirname(__file__), 'r8_scip_variants.json'), 'w'), indent=1)
