"""Validity check: the reference optimal solution must lie in every tightened box.

Reference solution: the MINLPLib .pK.sol whose objective matches the MINLPLib primal bound
(relative error <= 1e-6); otherwise the solution of the default Gurobi run (seed 0) if that run was
optimal and its objective matches the MINLPLib primal bound within 1e-4 (relative).
Writes results/validity.csv (one row per box).
"""
import os, sys, glob, json
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qcqp import QCQP
RES = os.path.join(HERE, '..', 'results')


def reference(P, fstar):
    x = P.load_sol(fstar)
    if x is not None and abs(P.fmin(x) - fstar) <= 1e-6 * max(1, abs(fstar)):
        return x, 'minlplib'
    p = os.path.join(RES, 'final_x', '%s_grb_base_0.npy' % P.name)
    if os.path.exists(p):
        x = np.load(p)
        if abs(P.fmin(x) - fstar) <= 1e-4 * max(1, abs(fstar)) and P.violation(x) <= 1e-5:
            return x, 'gurobi'
    return None, 'none'


if __name__ == '__main__':
    inst = pd.read_csv(os.path.join(RES, 'instances.csv')).set_index('name')
    rows = []
    files = sorted(glob.glob(os.path.join(RES, 'boxes', '*.npz')))
    byname = {}
    for f in files:
        name, src, tag = os.path.basename(f)[:-4].split('__')
        byname.setdefault(name, []).append((src, tag, f))
    for name, lst in byname.items():
        P = QCQP(name)
        fstar = inst.loc[name, 'fstar_min']
        x, how = reference(P, fstar)
        for src, tag, f in lst:
            b = np.load(f)
            lb, ub = b['lb'], b['ub']
            r = dict(name=name, src=src, rule=tag, ref=how)
            if x is not None:
                d = np.maximum(lb - x, 0) + np.maximum(x - ub, 0)
                rel = d / (1 + np.abs(x))
                r.update(maxviol_abs=float(d.max()), maxviol_rel=float(rel.max()),
                         nviol_1e6=int((rel > 1e-6).sum()), nviol_1e4=int((rel > 1e-4).sum()))
            rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RES, 'validity.csv'), index=False)
    print(df.ref.value_counts())
    print(df.groupby('src')[['nviol_1e6', 'nviol_1e4']].apply(lambda g: (g > 0).sum()))
    print(df[df.nviol_1e6 > 0].to_string())
