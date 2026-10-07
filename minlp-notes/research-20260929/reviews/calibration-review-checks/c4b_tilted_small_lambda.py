"""Rerun of c4 with a milder tilt (lam = 1 for alpha = -2, lam = 4 for alpha = 1) and finer meshes.

The strictness constant of the tilted calibration is of order eps*exp(-lam*T); with lam = 8
(c4) it is about 1.7e-4 and the transferred family is not yet exact at N = 320.
"""
import contextlib
import importlib.util
import io
import json

spec = importlib.util.spec_from_file_location("c4", "c4_nonstrict_lq_gap.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)  # also rewrites logs/c4_nonstrict_lq_gap.json identically
rows = []
for alpha, q, phiT, lam in [(-2.0, 0.0, 1.0, 1.0), (1.0, 1.0, 0.0, 4.0)]:
    for r in m.run(alpha, q, phiT, eps=0.5, lam=lam, Ns=(40, 160, 640, 2560)):
        r.update({"alpha": alpha, "q": q, "phiT": phiT, "lam": lam, "eps": 0.5})
        print(json.dumps({k: r[k] for k in ("alpha", "lam", "N", "field_gap", "tilted_gap",
                                            "tilted_worst_stage_defect")}))
        rows.append(r)
json.dump(rows, open("logs/c4b_tilted_small_lambda.json", "w"), indent=1)
