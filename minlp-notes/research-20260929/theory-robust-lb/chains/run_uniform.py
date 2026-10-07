"""B&B on the uniform design chain UD (uniform_design.make_pw with params (0.2, 6, 0.3, 3, 0.6, 4), b = 0.6).

Usage: python3 run_uniform.py CLS RULE EPS n [BASE]      -> one JSON line (BASE: balanced (default) or unsplit).
"""
import sys
import json
import numpy as np
sys.path.insert(0, "..")
from robust_bb import Family  # noqa: E402
from uniform_design import make_pw, dp_fstar  # noqa: E402
from bb_rules import bb  # noqa: E402

PARAMS = (0.2, 6.0, 0.3, 3.0, 0.6, 4.0)
B = 0.6

if __name__ == "__main__":
    cls, rule, eps, n = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    base = sys.argv[5] if len(sys.argv) > 5 else "balanced"
    u = make_pw(PARAMS[0], B, *PARAMS[1:])
    fs, xs = dp_fstar(u, B, n)
    fam = Family([u] * n, [B] * (n - 1))
    r = bb(fam, cls, eps, fs, rule=rule, base=base)
    print(json.dumps(dict(family="UD", cls=cls, base=base, rule=rule, eps=eps, n=n, fstar=fs, **r)), flush=True)
