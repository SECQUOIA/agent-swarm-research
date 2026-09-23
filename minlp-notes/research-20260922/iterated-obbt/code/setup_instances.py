"""Stage 0: select instances, download MINLPLib solutions, parse, run FBBT, apply the scope filter.

Writes results/instances.csv (one row per candidate, with the scope decision and the reason).
"""
import os, sys, json, math, re, time
import numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from qcqp import QCQP, fetch_sol

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
META = '/home/sgusev/repo/minlp-notes/code/minlp_solver_lab/instances/instancedata.csv'
POOL = os.path.join(HERE, '..', '..', 'scouting', 'brainstorm2-solvercore-probe', 'pool.csv')
BOUNDMAX = 1e7   # nonlinear variables need finite bounds of at most this magnitude


def family(n):
    m = re.match(r'([a-z]+(?:_[a-z]+)*?)(?=[_\-]?\d|$)', n.lower())
    return m.group(1) if m else n


def candidates():
    d = pd.read_csv(META, sep=';')
    q = d[d.probtype.str.contains('Q') & (d.convex.astype(str) != 'True') & d.nvars.between(5, 2000)
          & (d.nsemi == 0) & (d.nsos1 == 0) & (d.nsos2 == 0) & d.primalbound.notna() & d.dualbound.notna()]
    q = q[(q.primalbound - q.dualbound).abs() / q.primalbound.abs().clip(lower=1) <= 1e-4]
    return q[['name', 'probtype', 'nvars', 'nbinvars', 'nintvars', 'ncons', 'objsense', 'primalbound']]


def job(row):
    name = row['name']
    out = dict(row)
    try:
        P = QCQP(name)
        out.update(n=P.n, m=P.m, nnl=len(P.nlvars), nterms=len(P.terms),
                   nsq=sum(1 for i, j in P.terms if i == j), nint=int(P.isint.sum()))
        fstar = P.sense * row['primalbound']
        out['fstar_min'] = fstar
        x = P.load_sol(fstar)
        if x is not None:
            out['sol_obj_err'] = abs(P.fmin(x) - fstar) / max(1, abs(fstar))
            out['sol_viol'] = P.violation(x)
        t = time.time()
        lb, ub = P.fbbt()
        out['fbbt_time'] = time.time() - t
        nl = np.array(P.nlvars)
        fin = np.isfinite(lb[nl]) & np.isfinite(ub[nl]) & (np.abs(lb[nl]) <= BOUNDMAX) & (np.abs(ub[nl]) <= BOUNDMAX)
        out['nl_unbounded'] = int((~fin).sum())
        if x is not None:
            tol = 1e-6 * (1 + np.abs(x))
            out['sol_out_fbbt'] = int(((x < lb - tol) | (x > ub + tol)).sum())
        out['in_scope'] = bool(fin.all())
        out['reason'] = '' if fin.all() else 'nonlinear var unbounded after FBBT'
        np.savez_compressed(os.path.join(RES, 'fbbt', name + '.npz'), lb=lb, ub=ub)
    except Exception as e:
        out['in_scope'] = False
        out['reason'] = 'error: ' + str(e)[:120]
    return out


if __name__ == '__main__':
    os.makedirs(os.path.join(RES, 'fbbt'), exist_ok=True)
    c = candidates()
    pool = set(pd.read_csv(POOL).name)
    rows = c.to_dict('records')
    with Pool(6) as p:
        p.map(fetch_sol, list(c.name), chunksize=1)
    with Pool(24) as p:
        res = p.map(job, rows, chunksize=1)
    df = pd.DataFrame(res)
    df['family'] = df.name.map(family)
    df['in_probe_pool'] = df.name.isin(pool)
    df.to_csv(os.path.join(RES, 'instances.csv'), index=False)
    print(df.in_scope.sum(), 'in scope of', len(df))
    print(df.reason.value_counts())
