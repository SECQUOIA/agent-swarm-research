"""Follow-up to postprocess_positions.py: for the configurations whose face
F(B) contains p with p(0) > 1e-4 at the positions found by the search,
take p* = argmax p(0) over the face (base <p,u> = 1, exact cube description)
and record its relaxation values (D3 only, and R), its zero set, whether a
vertex is blocked for its actual zero set (Lemma 2.4 test), and the best
family fit.  Numerical only."""
import json
import warnings

import cvxpy as cp
import numpy as np

warnings.filterwarnings("ignore")
from blocking_positions import rows_theta  # noqa: E402
from check_nond3_blocked import blocked_vertex, numeric_zeros  # noqa: E402
from cube3 import QKEYS  # noqa: E402
from fit_family import fit  # noqa: E402
from sdp3 import SOLVER_OPTS, Relaxation, Separation, cube_min  # noqa: E402

recs = [json.loads(ln) for ln in open('../logs/postprocess_positions.jsonl')]
cand = [r for r in recs if r.get('maxp0') not in (None, 'None') and float(r['maxp0']) > 1e-4]
S = Separation()
A = cp.Parameter((12, 10))
prob = cp.Problem(cp.Maximize(S.pv[0]), S.prob.constraints + [A @ S.pv == 0])
R1 = Relaxation(use_family=True)
R0 = Relaxation(use_family=False)
out = []
for r in cand:
    B = tuple(tuple(s) for s in r['config'])
    th = np.array(r['theta'])
    Rm = rows_theta(B, th)
    Ap = np.zeros((12, 10))
    Ap[:Rm.shape[0]] = Rm
    A.value = Ap
    prob.solve(**SOLVER_OPTS)
    p = np.array(S.pv.value)
    p = p / np.abs(p).max()
    r1 = R1.solve(p)[0]
    r0 = R0.solve(p)[0]
    z = numeric_zeros(p, 1e-6)
    bl = blocked_vertex(p, z)
    c, g, par = fit(p, n_starts=4)
    rec = dict(config=B, theta=th.tolist(), p=p.tolist(), p0=p[0], cubemin=cube_min(p),
               r_d3=r0, r_R=r1, zeros=[(list(s), np.round(x, 4).tolist()) for s, x in z],
               blocked_vertices=[list(v) for v in bl], family_fit_residual=c,
               family_fit_params=list(par) if par is not None else None,
               square_coefs=[p[QKEYS.index(k)] for k in ((2, 0, 0), (0, 2, 0), (0, 0, 2))])
    out.append(rec)
    print('config', B, 'p0 %.3g' % p[0], 'cubemin %.2e' % rec['cubemin'], 'r_d3 %.2e' % r0,
          'r_R %.2e' % r1, 'zeros', rec['zeros'], 'blocked', rec['blocked_vertices'],
          'fit %.2e' % c, flush=True)
json.dump(out, open('../logs/special_config_check.json', 'w'), default=float)
