"""Generic exact feasibility check of a rational point against an OSIL model.

Usage: python3 check_exact_point.py <instance> <point file> <out json>

Every variable bound, integrality requirement and constraint row is evaluated in exact rational
arithmetic (Python Fraction) from the OSIL data as read by osil_exact.py (decimal constants kept
exactly). Only polynomial expressions are accepted (ExactArith raises otherwise). The objective is
computed exactly and printed with directed decimal rounding.
"""
import os
import json
import sys
import time
from fractions import Fraction

import osil_exact
from exact_io import dec_ceil, dec_floor, read_point

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def main():
    name, pfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
    t0 = time.time()
    I = osil_exact.read(f"{OSIL_DIR}/{name}.osil")
    P = read_point(pfile)
    assert set(P) == set(I["names"]), "point must give every variable exactly once"
    x = [P[nm] for nm in I["names"]]
    A = osil_exact.ExactArith()
    bound_fail, int_fail = [], []
    for j, v in enumerate(x):
        lo, hi = I["lb"][j], I["ub"][j]
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            bound_fail.append(I["names"][j])
        if I["vtype"][j] in ("B", "I") and v.denominator != 1:
            int_fail.append(I["names"][j])
    row_fail, n_eq, n_ineq = [], 0, 0
    max_abs_den_digits = 0
    for r, row in enumerate(I["cons"]):
        v = osil_exact.eval_row(row, x, A)
        lo, hi = row["lb"], row["ub"]
        if lo is not None and hi is not None and lo == hi:
            n_eq += 1
        else:
            n_ineq += 1
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            row_fail.append((row["name"], str(v)))
    obj = osil_exact.eval_row(I["obj"], x, A)
    rec = dict(instance=name, point_file=pfile, n_vars=len(x), n_rows=len(I["cons"]), n_equality_rows=n_eq,
               n_other_rows=n_ineq, bound_failures=len(bound_fail), integrality_failures=len(int_fail),
               row_failures=len(row_fail), first_failures=(bound_fail + int_fail + row_fail)[:5],
               exactly_feasible=not (bound_fail or int_fail or row_fail),
               objective_sense=I["obj"]["sense"],
               objective_floor_40=dec_floor(obj, 40), objective_ceil_40=dec_ceil(obj, 40),
               objective_denominator_digits=len(str(obj.denominator)),
               seconds=round(time.time() - t0, 1))
    print(json.dumps(rec, indent=1))
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
    with open(out.replace(".json", "_objective_exact.txt"), "w") as f:
        f.write(f"{obj.numerator}/{obj.denominator}\n")


if __name__ == "__main__":
    main()
