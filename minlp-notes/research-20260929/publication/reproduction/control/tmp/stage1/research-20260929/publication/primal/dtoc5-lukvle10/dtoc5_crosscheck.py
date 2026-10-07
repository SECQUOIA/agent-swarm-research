"""dtoc5: re-check the rational point with the open-instances verifier's OSIL reader and row
evaluator (reviews/open-instances-verification/osilx.py), in exact rational arithmetic.

Independent of osil_exact.py and check_exact_point.py (shares only the point file).
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import gzip
import json
import sys
import time
from fractions import Fraction

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
sys.path.insert(0, _REPO + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402


def main():
    t0 = time.time()
    I = osilx.read((_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/dtoc5.osil'))
    val = {}
    with gzip.open("points/dtoc5_point.txt.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                nm, v = line.split()
                val[nm] = Fraction(v)
    x = [val[nm] for nm in I["names"]]
    assert len(val) == len(x)
    bad_bounds = sum(1 for j in range(len(x))
                     if (not osilx.isinf(I["lb"][j]) and x[j] < Fraction(I["lb"][j]))
                     or (not osilx.isinf(I["ub"][j]) and x[j] > Fraction(I["ub"][j])))
    bad_int = sum(1 for j in range(len(x)) if I["vt"][j] in ("B", "I") and x[j].denominator != 1)
    bad_rows = 0
    for c in I["cons"]:
        v = osilx.ev_row(c, x, Fraction, {})
        if (not osilx.isinf(c["lb"]) and v < Fraction(c["lb"])) or (not osilx.isinf(c["ub"]) and v > Fraction(c["ub"])):
            bad_rows += 1
    obj = osilx.ev_row(I["obj"], x, Fraction, {})
    mine = open("logs/dtoc5_check_objective_exact.txt").read().strip()
    rec = dict(bad_bounds=bad_bounds, bad_integrality=bad_int, bad_rows=bad_rows, n_rows=len(I["cons"]),
               objective_equals_check_exact_point=(obj == Fraction(mine)),
               objective_floor_30=f"{(obj.numerator * 10 ** 30) // obj.denominator}e-30",
               seconds=round(time.time() - t0, 1))
    print(json.dumps(rec, indent=1))
    json.dump(rec, open("logs/dtoc5_crosscheck.json", "w"), indent=1)


if __name__ == "__main__":
    main()
