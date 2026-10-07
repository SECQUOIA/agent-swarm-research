"""Verifier for finding C-computation-1 (E5: cause of SCIP's primal shortfall).

Rebuilds the E5 SCIP model as experiments/run_all.task_scip does (default
settings, epigraph form, absgap 1e-6) and, for SCIP's best solution x, t:
  * lists every coordinate outside [-1, 1], whether it is in the planted
    active set A and whether the violation is outward from x*_i;
  * splits t's shortfall F(clip x) - t into
        bounds:   F(clip x) - F(x)   and   epigraph: F(x) - t   (all exact);
  * compares the bound part with the first-order prediction mu * sum(viol);
  * asks SCIP whether it considers its own solution feasible.
Also fits shortfall = n_A*mu*1e-8 + 9e-7 to all 21 rows of E5_scip.csv.
"""
import csv
import os
import sys
from fractions import Fraction as F
from pathlib import Path

for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'experiments'))
from instances import planted  # noqa: E402


def csv_fit():
    print('Fit of E5_scip.csv: shortfall vs n_A*mu*1e-8 + 9e-7')
    fr = []
    for r in csv.DictReader(open(ROOT / 'experiments/results/E5_scip.csv')):
        n = int(r['n'])
        na = max(1, round(0.25 * n))
        mu = float(F(r['mu']))
        s = float(r['epigraph_shortfall'])
        pred = na * mu * 1e-8 + 9e-7
        fr.append(na * mu * 1e-8 / s)
        print(f"  {r['kind']:5s} {n:3d} s{r['seed']}: shortfall {s:.5e} pred {pred:.5e} "
              f"rel.err {abs(s - pred) / s:.1e} bound share {na * mu * 1e-8 / s:.3f}")
    print(f'  bound share range {min(fr):.4f} .. {max(fr):.4f}')


def run(kind, n, seed, tl=20.0):
    from pyscipopt import Model, quicksum
    problem, info = planted(kind, n, 4, seed)
    m = Model()
    m.hideOutput()
    m.setParam('limits/time', tl)
    m.setParam('limits/absgap', 1e-6)
    m.setParam('parallel/maxnthreads', 1)
    m.setParam('lp/threads', 1)
    m.setParam('randomization/randomseedshift', 0)
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi)) for i, (lo, hi) in enumerate(problem.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    quad = quicksum(float(problem.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(problem.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in problem.interactions)
    m.addCons(t >= float(problem.constant) + quad)
    m.setObjective(t, 'minimize')
    m.optimize()
    sol = m.getBestSol()
    heur = sol.getHeur() if hasattr(sol, 'getHeur') else None
    try:
        heurname = heur.getName() if heur is not None else 'relaxation/none'
    except Exception:
        heurname = '?'
    raw = [F(sol[v]) for v in x]
    tv = F(sol[t])
    clip = [min(max(v, lo), hi) for v, (lo, hi) in zip(raw, problem.bounds)]
    act = set(info['active'])
    xs = [F(s) for s in info['xstar']]
    mu = F(info['mu'])
    viol = {}
    for i, (v, (lo, hi)) in enumerate(zip(raw, problem.bounds)):
        if v > hi:
            viol[i] = v - hi
        elif v < lo:
            viol[i] = lo - v
    outward = all(i in act and ((raw[i] > 1) == (xs[i] == 1)) for i in viol)
    f_raw, f_clip = problem.value(tuple(raw)), problem.value(tuple(clip))
    feas = m.checkSol(sol, printreason=False, completely=True, checkbounds=True,
                      checkintegrality=True, checklprows=True, original=True)
    print(f'{kind}{n} s{seed}: status {m.getStatus()} primal {m.getPrimalbound():.6e} '
          f'dual {m.getDualbound():.6e} found by {heurname}')
    print(f'   violated coords {sorted(viol)} (|A|={len(act)}, all in A and outward: {outward}); '
          f'violations {sorted(set(float(v) for v in viol.values()))}')
    print(f'   F(clip x) = {float(f_clip):.3e}, F(x) = {float(f_raw):.6e}, t = {float(tv):.6e}')
    print(f'   shortfall F(clip x)-t = {float(f_clip - tv):.6e} = bounds {float(f_clip - f_raw):.6e} '
          f'+ epigraph {float(f_raw - tv):.6e}; mu*sum(viol) = {float(mu * sum(viol.values())):.6e}')
    print(f'   SCIP checkSol(original, bounds) feasible: {feas}')


if __name__ == '__main__':
    csv_fit()
    for spec in (('path', 16, 202), ('band2', 12, 101), ('tree', 16, 303), ('band3', 8, 303),
                 ('path', 32, 101)):
        run(*spec)
