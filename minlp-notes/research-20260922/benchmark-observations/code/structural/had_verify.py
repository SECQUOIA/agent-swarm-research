"""Deterministic re-verification of certs/hadamard_n.json (no search, no floating point in the checks).

For each n: (1) the OSiL row is exactly det(B) (had_model.check); (2) the stored bounds on D01(n) are
recomputed with exact integer/Fraction arithmetic; (3) the stored primal matrix is evaluated exactly in the
OSiL model with objvar = det(B), all bounds/rows/integrality checked; (4) for n = 6 the exhaustive
maximum |det| over all 0/1 6x6 matrices is recomputed (exact integer arithmetic).
Usage: python had_verify.py [--skip-exhaustive]
"""
import json
import os
import sys

import numpy as np

from had_bounds import d01_bound, exact_primal, exhaustive6
from had_model import check as check_model

HERE = os.path.dirname(os.path.abspath(__file__))

ok_all = True
for n in (6, 7, 8, 9):
    C = json.load(open(os.path.join(HERE, "certs", f"hadamard_{n}.json")))
    M, _ = check_model(n)
    b = d01_bound(n)
    assert {k: (v["Dpm_sq"], v["D01_int"]) for k, v in b.items()} == \
        {k: (v["Dpm_sq"], v["D01_int"]) for k, v in C["bounds"].items()}
    dual = min(v["D01_int"] for v in b.values())
    B = np.array(C["primal_matrix_rowmajor"]).reshape(n, n)
    D, obj, _ = exact_primal(n, B, M)
    ok = dual == C["certified_dual_int"] and D == C["primal_det_exact"] and obj == D
    msg = f"hadamard_{n}: dual <= {dual} ({', '.join(f'{k} {v['D01_int']}' for k, v in b.items())}); " \
          f"primal {D} (feasible, exact); closed={D == dual}"
    if n == 6 and "--skip-exhaustive" not in sys.argv:
        ex = exhaustive6()
        ok &= ex == C["exhaustive_max_abs_det"] == 9
        msg += f"; exhaustive max|det| = {ex}"
    ok_all &= ok
    print(msg, "OK" if ok else "MISMATCH", flush=True)
print("ALL VERIFIED" if ok_all else "FAILED")
sys.exit(0 if ok_all else 1)
