"""Evaluate the refined KKT primal of optcdeg2 with the repository's 50-digit OSIL evaluator."""
import json
import sys

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
sys.path.insert(0, _REPO + "/research-20260929/open-instances")
from optcdeg2_common import N, h, to_osil  # noqa: E402
from osil_eval import check  # noqa: E402

u = np.load(_REPO + "/research-20260929/theory-bangbang/logs/optcdeg2_kkt_u.npy")
y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
for t in range(N):
    y[t + 1] = y[t] + h * v[t]
    v[t + 1] = v[t] + h * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
vN = v[N]; v = v.copy(); v[N] = 0.0
chk = check("optcdeg2", to_osil(u, y, v))
rec = dict(simulated_vN=float(vN), obj=float(chk["obj"]), obj_str=str(chk["obj"]), cons_viol=float(chk["cons_viol"]),
           bound_viol=float(chk["bound_viol"]), worst_row=chk["worst_row"],
           u_frac=[float(u[3091]), float(u[47290])])
print(json.dumps(rec))
json.dump(rec, open(_REPO + "/research-20260929/theory-bangbang/logs/optcdeg2_kkt_primal_check.json", "w"), indent=1)
