"""Diagnostic only (not a bound): the author's fixed-leaf Shor SDP (diag_leaf.py, angle rows
dropped, leaf state W_11, W_29,29, w_R, w_I fixed at p1) re-solved with Clarabel tolerances
1e-10, to see whether the 1.1e-3 difference to obj(p1) reported in diag_leaf.log is solver error."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os, sys
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow/ext")
import pf_model as pm
from pf_primal import solve_primal, residuals, complex_W
name = "powerflow0039p"
M = pm.decode(name)
rows = [r for r in M["rows"] if r["kind"] != "angle"]
vals = {}
for line in open(f"{_REPRO_ROOT}/research-20260929/open-instances-wave3/sol/{name}.p1.sol"):
    p = line.split()
    if len(p) == 2:
        vals[p[0]] = p[1]
names = M["I"]["names"]
V = np.array([float(vals[names[vv]]) * np.exp(1j * float(vals.get(names[tt], "0"))) for vv, tt in M["busmap"]])
W1 = V[1] * np.conj(V[29])
fix = lambda Q, v, nm: dict(name=nm, lin={}, Q=Q, qy={}, lb=Fr(v), ub=Fr(v), kind="fix")
extra = [fix({(2, 2): Fr(1), (3, 3): Fr(1)}, abs(V[1]) ** 2, "fW11"),
         fix({(58, 58): Fr(1), (59, 59): Fr(1)}, abs(V[29]) ** 2, "fW29"),
         fix({(2, 58): Fr(1), (3, 59): Fr(1)}, W1.real, "fwR"),
         fix({(3, 58): Fr(1), (2, 59): Fr(-1)}, W1.imag, "fwI")]
t_ = 1e-10
res = solve_primal(M, rows, extra, solver_kw=dict(tol_gap_abs=t_, tol_gap_rel=t_, tol_feas=t_, tol_ktratio=t_, max_iter=500))
ev = np.linalg.eigvalsh(complex_W(M, res["W"]))
print(f"fixed leaf, tol 1e-10: value {res['value']!r} ({res['status']}), max row residual {residuals(M, res)[0][0]:.1e}, "
      f"top eigenvalues {ev[-3:]}; obj(p1) 41869.0515113202; difference {41869.0515113202 - res['value']:.3e}")
