"""E5: why SCIP's reported primal bounds lie below the optimum.

Reruns the 21 default E5 SCIP tasks of run_all.py (same model, same
parameters as task_scip) and, for SCIP's best solution (x, t), splits the
shortfall F(clip x) - t, which run_all.py records as `epigraph_shortfall`
(clip = projection onto the box), exactly into
    bound part     F(clip x) - F(x)   (x violates box bounds), and
    epigraph part  F(x) - t           (t lies below F at SCIP's own point).
It also records the largest bound violation, the violated coordinates, and
whether SCIP itself accepts its solution as feasible.

    python3 scip_shortfall.py          -> results/E5_scip_shortfall.csv

At most 4 worker processes, one thread each; about one minute of wall time
(nine runs stop at the 20 s limit). The primal bound of every rerun is
compared with E5_scip.csv.
"""
import os
for _var in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_var] = '1'

import csv
import sys
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from instances import planted  # noqa: E402

SEEDS = (101, 202, 303)
E5 = [('path', 16), ('tree', 16), ('band2', 12), ('band3', 8), ('path', 32), ('path', 64),
      ('path', 128)]


def run(spec):
    kind, n, seed = spec
    from pyscipopt import Model, quicksum
    problem, info = planted(kind, n, 4, seed)
    m = Model()
    m.hideOutput()
    m.setParam('limits/time', 20.0)
    m.setParam('limits/absgap', 1e-6)
    for name, val in (('parallel/maxnthreads', 1), ('lp/threads', 1),
                      ('randomization/randomseedshift', 0)):
        try:
            m.setParam(name, val)
        except Exception:
            pass
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi),
                  vtype='I' if i in problem.integers else 'C')
         for i, (lo, hi) in enumerate(problem.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    quad = quicksum(float(problem.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(problem.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in problem.interactions)
    m.addCons(t >= float(problem.constant) + quad)
    m.setObjective(t, 'minimize')
    m.optimize()
    sol = m.getBestSol()
    raw = [F(sol[v]) for v in x]          # exact binary values of the doubles
    tv = F(sol[t])
    clip = [min(max(v, lo), hi) for v, (lo, hi) in zip(raw, problem.bounds)]
    viol = {i: max(lo - v, v - hi) for i, (v, (lo, hi)) in enumerate(zip(raw, problem.bounds))
            if v < lo or v > hi}
    active = set(info['active'])
    xstar = [F(s) for s in info['xstar']]
    outward = all(i in active and ((raw[i] > 1) == (xstar[i] == 1)) for i in viol)
    f_raw, f_clip = problem.value(tuple(raw)), problem.value(tuple(clip))
    feasible = m.checkSol(sol, printreason=False, completely=True, checkbounds=True,
                          checkintegrality=True, checklprows=True, original=True)
    shortfall = f_clip - tv
    return {'kind': kind, 'n': n, 'seed': seed, 'status': m.getStatus(),
            'primal_bound': m.getPrimalbound(), 'dual_bound': m.getDualbound(),
            'n_active': len(active), 'n_violated': len(viol),
            'violations_all_active_outward': outward,
            'max_bound_violation': float(max(viol.values(), default=0)),
            'F_unclipped': float(f_raw), 'F_clipped': float(f_clip), 't': float(tv),
            'shortfall': float(shortfall), 'bound_part': float(f_clip - f_raw),
            'epigraph_part': float(f_raw - tv),
            'bound_share': float((f_clip - f_raw) / shortfall),
            'mu_times_violations': float(F(info['mu']) * sum(viol.values(), F(0))),
            'scip_accepts_solution': bool(feasible)}


def main():
    specs = [(kind, n, seed) for kind, n in E5 for seed in SEEDS]
    with ProcessPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run, specs))
    saved = {(r['kind'], int(r['n']), int(r['seed'])): float(r['primal_bound'])
             for r in csv.DictReader(open(HERE / 'results' / 'E5_scip.csv'))}
    for r in rows:
        r['primal_bound_as_in_E5'] = r['primal_bound'] == saved[(r['kind'], r['n'], r['seed'])]
    with open(HERE / 'results' / 'E5_scip_shortfall.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    shares = [r['bound_share'] for r in rows]
    print(f"{len(rows)} runs; primal bound as in E5_scip.csv: "
          f"{sum(r['primal_bound_as_in_E5'] for r in rows)}; violations all active and outward: "
          f"{sum(r['violations_all_active_outward'] for r in rows)}; SCIP accepts its solution: "
          f"{sum(r['scip_accepts_solution'] for r in rows)}")
    print(f"max bound violation {min(r['max_bound_violation'] for r in rows):.4e} .. "
          f"{max(r['max_bound_violation'] for r in rows):.4e}")
    print(f"shortfall {min(r['shortfall'] for r in rows):.3e} .. {max(r['shortfall'] for r in rows):.3e}; "
          f"bound share {min(shares):.4f} .. {max(shares):.4f}; epigraph part "
          f"{min(r['epigraph_part'] for r in rows):.4e} .. {max(r['epigraph_part'] for r in rows):.4e}; "
          f"F at unclipped point {min(r['F_unclipped'] for r in rows):.3e} .. "
          f"{max(r['F_unclipped'] for r in rows):.3e}")


if __name__ == '__main__':
    main()
