"""Check 1: order and validity of the relaxations on small instances, with node fixings.
Reviewer implementations only (rv_common).  For each instance and node, report
persp <= sdp1 <= sdp2 <= L2 <= L3 <= OPT_node and sdp1 <= zb <= OPT_node (tolerance 1e-6 relative),
and whether each is exact.  Also compares with the author's relax.py values (cross-check of their code).
usage: rv_small.py [ninst]"""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import sys, os, json, time
from rv_common import *  # noqa: F401,F403
from rv_common import gen_core, opt_enum, persp, sdp1, sdp2, Lr, zb, fval
import numpy as np

AUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bb-complexity', 'sparse-regression',
                    'stronger-relaxations', 'code')

ninst = int(sys.argv[1]) if len(sys.argv) > 1 else 6
rows = []
viol = 0
tol = 1e-6
try:
    sys.path.insert(0, AUTH)
    import relax as A  # author's models, used only for comparison
except Exception as e:  # noqa: BLE001
    A = None
    print('author code not importable:', e)

for it in range(ninst):
    n, p, k = [(6, 8, 2), (7, 9, 2), (6, 9, 3), (8, 10, 3), (5, 8, 2), (7, 10, 3)][it % 6]
    kind = ['noise', 'weak', 'planted'][it % 3]
    b = {'noise': 0.0, 'weak': 0.3, 'planted': 1.0}[kind]
    X, y, lam, S = gen_core(n, p, k, b=b, sigma=0.5, seed=900 + it, lam=np.sqrt(n))
    Sstar, _ = S, None
    opt, arg = opt_enum(X, y, lam, k)
    nodes = [((), ()), ((), (int(np.argmax(np.abs(X.T @ y))) if int(np.argmax(np.abs(X.T @ y))) not in arg else
                            [j for j in range(p) if j not in arg][0],)), ((arg[0],), ())]
    for S0, S1 in nodes:
        o, _ = opt_enum(X, y, lam, k, S0, S1)
        t0 = time.time()
        v = dict(persp=persp(X, y, lam, k, S0, S1), sdp1=sdp1(X, y, lam, k, S0, S1), sdp2=sdp2(X, y, lam, k, S0, S1),
                 L2=Lr(X, y, lam, k, 2, S0, S1), L3=Lr(X, y, lam, k, 3, S0, S1), zb=zb(X, y, lam, k, S0, S1),
                 zb_noPC=zb(X, y, lam, k, S0, S1, product_cones=False))
        chain = ['persp', 'sdp1', 'sdp2', 'L2', 'L3']
        bad = []
        for a_, b_ in zip(chain[:-1], chain[1:]):
            if v[a_] > v[b_] + tol * abs(o):
                bad.append(f'{a_}>{b_}')
        for key in chain + ['zb', 'zb_noPC']:
            if v[key] > o + tol * abs(o):
                bad.append(f'{key}>OPT')
        if v['sdp1'] > v['zb'] + tol * abs(o):
            bad.append('sdp1>zb')
        if v['zb_noPC'] > v['zb'] + tol * abs(o):
            bad.append('zbnoPC>zb')
        viol += len(bad)
        ex = {key: int(abs(o - v[key]) <= tol * abs(o)) for key in v}
        cmpA = {}
        if A is not None:
            for key, fn in [('sdp1', A.sdp1), ('sdp2', A.sdp2), ('L2', A.L2), ('zb', A.zb)]:
                va = fn(X, y, lam, k, S0, S1)
                cmpA[key] = None if va is None else float(va - v[key])
        row = dict(inst=it, kind=kind, n=n, p=p, k=k, node=[list(S0), list(S1)], OPT=o,
                   gaps={key: (o - v[key]) / abs(o) for key in v}, exact=ex, bad=bad,
                   author_minus_mine=cmpA, time=round(time.time() - t0, 1))
        rows.append(row)
        print(json.dumps(row), flush=True)

print('TOTAL order/validity violations:', viol)
for key in ['persp', 'sdp1', 'sdp2', 'L2', 'L3', 'zb_noPC', 'zb']:
    print(key, 'exact nodes:', sum(r['exact'][key] for r in rows), '/', len(rows))
if A is not None:
    mx = max(abs(d) for r in rows for d in r['author_minus_mine'].values() if d is not None)
    print('max |author - reviewer| over sdp1, sdp2, L2, zb:', mx)
