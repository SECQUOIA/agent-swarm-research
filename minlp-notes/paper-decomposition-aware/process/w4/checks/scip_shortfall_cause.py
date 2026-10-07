"""Where does SCIP's primal bound below OPT=0 come from (E5)?

Rebuilds the E5 SCIP model exactly as run_all.task_scip does and decomposes
the shortfall exact F(clip(x)) - t into
  (a) bound violation of x:      F(clip(x)) - F(x)          (exact, unclipped x)
  (b) epigraph violation:        F(x) - t                   (exact)
Runs default settings and feastol = dualfeastol = 1e-9.
"""
import os
import sys
from fractions import Fraction as F
from pathlib import Path

for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import planted  # noqa: E402
from pyscipopt import Model, quicksum  # noqa: E402


def run(kind, n, seed, feastol=None, offset=False, tl=20.0):
    problem, info = planted(kind, n, 4, seed)
    m = Model()
    m.hideOutput()
    m.setParam('limits/time', tl)
    m.setParam('limits/absgap', 1e-6)
    m.setParam('parallel/maxnthreads', 1)
    m.setParam('lp/threads', 1)
    m.setParam('randomization/randomseedshift', 0)
    if feastol:
        m.setParam('numerics/feastol', feastol)
        m.setParam('numerics/dualfeastol', feastol)
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi)) for i, (lo, hi) in enumerate(problem.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    quad = quicksum(float(problem.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(problem.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in problem.interactions)
    if offset:
        m.addCons(t >= quad)
        m.addObjoffset(float(problem.constant))
    else:
        m.addCons(t >= float(problem.constant) + quad)
    m.setObjective(t, 'minimize')
    m.optimize()
    sol = m.getBestSol()
    raw = [F(sol[v]) for v in x]
    tval = F(sol[t]) + (F(float(problem.constant)) if offset else 0)
    clip = [min(max(v, lo), hi) for v, (lo, hi) in zip(raw, problem.bounds)]
    viol = [max(lo - v, v - hi, 0) for v, (lo, hi) in zip(raw, problem.bounds)]
    f_raw = problem.value(tuple(raw))
    f_clip = problem.value(tuple(clip))
    print(f"{kind}{n} s{seed} feastol={feastol} offset={offset} status={m.getStatus()} "
          f"primal={m.getPrimalbound():.3e} dual={m.getDualbound():.3e}")
    print(f"   max bound violation {float(max(viol)):.3e}, #violated {sum(1 for v in viol if v > 0)}")
    print(f"   F(clip x) - t = {float(f_clip - tval):.3e}  "
          f"= [F(clip x)-F(x)] {float(f_clip - f_raw):.3e} + [F(x)-t] {float(f_raw - tval):.3e}")


if __name__ == '__main__':
    run('path', 16, 202)
    run('path', 16, 202, feastol=1e-9)
    run('band2', 12, 101)
    run('path', 16, 202, offset=True)
