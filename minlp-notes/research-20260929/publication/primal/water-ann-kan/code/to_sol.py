"""Write 40-digit decimal roundings of the point files in MINLPLib .sol format
(points/<name>.approx40.sol), for convenience only.  The rounded files are NOT exactly
feasible; the exactly feasible points are the JSON point files.

usage: python3 to_sol.py points/*.json
"""
import json
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp


def q(s):
    f = Fr(s)
    return mp.mpf(f.numerator) / f.denominator


def main(path):
    mp.mp.dps = 60
    P = json.load(open(path))
    W = {}
    for k, s in P.get("symbols", {}).items():
        A, B, C, lo, hi = (q(s[f]) for f in ("A", "B", "C", "lo", "hi"))
        d = mp.sqrt(B * B - 4 * A * C)
        (W[int(k)],) = [t for t in ((-B + d) / (2 * A), (-B - d) / (2 * A)) if lo < t < hi]
    out = os.path.join(os.path.dirname(path), P["instance"] + ".approx40.sol")
    with open(out, "w") as f:
        for nm, v in P["x"].items():
            if isinstance(v, str):
                val = q(v)
            elif "w" in v:
                val = q(v["c0"]) + q(v["c1"]) * W[int(v["w"])]
            else:
                val = (mp.mpf(v["lo"]) + mp.mpf(v["hi"])) / 2
            f.write(f"{nm} {mp.nstr(val, 40, min_fixed=-10 ** 9, max_fixed=10 ** 9)}\n")
    print("wrote", out)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
