"""Diagnostics (not part of any bound): for powerflow0039p,
  (a) the root Shor SDP (primal form, angle rows dropped): leaf quantities at bus 29 and the
      top eigenvalues of the complex W;
  (b) the same SDP with the leaf state (W_11, W_29,29, w_R, w_I of line 1-29) fixed to its
      value at the MINLPLib point p1: if the rest of the network is exact, the value is
      obj(p1) up to solver accuracy.
    python3 diag_leaf.py
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import ev  # noqa: E402
import pf_model as pm  # noqa: E402
import leafcut as lc  # noqa: E402
from pf_primal import solve_primal, residuals, complex_W  # noqa: E402

name = "powerflow0039p"
M = pm.decode(name)
info = lc.leaf_info(M)
b = float(info["b"])
rows = [r for r in M["rows"] if r["kind"] != "angle"]
yi = {y: q for q, y in enumerate(M["ys"])}


def report(tag, res):
    Wc = complex_W(M, res["W"])
    W11, W29, w = Wc[1, 1].real, Wc[29, 29].real, Wc[1, 29]
    Pg, Qg = res["y"][yi[info["Pg"]]], res["y"][yi[info["Qg"]]]
    print(f"{tag}: SDP value {res['value']!r} ({res['status']}), max row residual {residuals(M, res)[0][0]:.1e}")
    print(f"   top eigenvalues of complex W {np.linalg.eigvalsh(Wc)[-3:]}")
    print(f"   W_11 {W11:.8f} W_29,29 {W29:.8f} |W_1,29|^2/W_11 {abs(w)**2/W11:.8f}  Pg29 {Pg:.6f} Qg29 {Qg:.6f}"
          f"  F(Pg,Qg,W_29,29) {W29 - 2*Qg/b + (Qg*Qg + Pg*Pg)/(b*b*W29):.8f}")


report("root", solve_primal(M, rows))
vals = ev.read_sol(os.path.join(HERE, "..", "..", "sol", f"{name}.p1.sol"))
names = M["I"]["names"]
V = np.array([float(vals[names[vv]]) * np.exp(1j * float(vals.get(names[tt], "0"))) for vv, tt in M["busmap"]])
W1 = V[1] * np.conj(V[29])


def fix(Q, val, nm):
    return dict(name=nm, lin={}, Q=Q, qy={}, lb=Fr(val), ub=Fr(val), kind="fix")


extra = [fix({(2, 2): Fr(1), (3, 3): Fr(1)}, abs(V[1]) ** 2, "fW11"),
         fix({(58, 58): Fr(1), (59, 59): Fr(1)}, abs(V[29]) ** 2, "fW29"),
         fix({(2, 58): Fr(1), (3, 59): Fr(1)}, W1.real, "fwR"),
         fix({(3, 58): Fr(1), (2, 59): Fr(-1)}, W1.imag, "fwI")]
report("leaf state fixed at p1", solve_primal(M, rows, extra))
