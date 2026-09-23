"""Probe B: sensitivity of SCIP 10 node counts to spatial-branching choices.

Every run gets the MINLPLib primal value as objective limit (removes primal-heuristic noise),
1 thread, 300 s. Settings: default, two random-seed shifts (noise floor), branching point
(LP value vs midpoint), branching on auxiliary variables (subexpressions such as linear forms),
and variable-score weights.
"""
import sys, json, pandas as pd
from multiprocessing import Pool
from common import solve

SET = {
    'dflt': {},
    'seed1': {'randomization/randomseedshift': 1, 'randomization/permutationseed': 1},
    'seed2': {'randomization/randomseedshift': 2, 'randomization/permutationseed': 2},
    'pt_lp': {'branching/midpull': 0.0},
    'pt_mid': {'branching/midpull': 1.0},
    'aux0': {'constraints/nonlinear/branching/aux': 0},
    'viol_only': {'constraints/nonlinear/branching/pscostweight': 0.0},
    'dual1': {'constraints/nonlinear/branching/dualweight': 1.0},
    'dom1': {'constraints/nonlinear/branching/domainweight': 1.0},
}

def job(a):
    name, U, sense, s = a
    tol = 1e-6 * max(1.0, abs(U))
    try:
        _, o = solve(name, dict(SET[s], **{'limits/time': 300}), objlimit=U + tol if sense == 'min' else U - tol)
    except Exception as e:
        o = dict(name=name, status='error:' + str(e)[:80])
    o['setting'] = s
    print(json.dumps(o), flush=True)
    return o

if __name__ == '__main__':
    sel = pd.read_csv(sys.argv[1])
    jobs = [(r.name, r.primalbound, 'min' if r.objsense == 'min' else 'max', s) for r in sel.itertuples() for s in SET]
    with Pool(17, maxtasksperchild=1) as p:
        res = p.map(job, jobs, chunksize=1)
    pd.DataFrame(res).to_csv('probeB.csv', index=False)
