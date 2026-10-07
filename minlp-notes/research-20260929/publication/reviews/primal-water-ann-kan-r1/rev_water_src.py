"""Compare the author's exact waterno2 points with their numerical sources (reviewer's code).
Row violations of the source points are computed exactly in Fractions from the decimal strings.
usage: python3 rev_water_src.py"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../..'))
import json
from fractions import Fraction as Fr

import rosil
import rev_water

W2 = _RESEARCH + "/open-instances-wave2/waterno2"


class AQ:
    num = staticmethod(Fr)


def viol(M, X):
    worst = (Fr(0), None)
    for c in M["cons"]:
        b = rosil.eval_body(c, X, AQ)
        v = max(Fr(0), (c["lb"] - b) if c["lb"] is not None else 0, (b - c["ub"]) if c["ub"] is not None else 0)
        if v > worst[0]:
            worst = (v, c["name"])
    bv = Fr(0)
    for j in range(M["n"]):
        if M["lb"][j] is not None:
            bv = max(bv, M["lb"][j] - X[j])
        if M["ub"][j] is not None:
            bv = max(bv, X[j] - M["ub"][j])
    return worst, bv


def main():
    for tag, src in (("06", "data/waterno2_06.p4.sol"), ("09", "logs/primal_09_w2.json"),
                     ("12", "logs/primal_12_w2.json"), ("18", "logs/primal_18_w2.json"),
                     ("24", "logs/primal_24_w2.json")):
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            Xe, M, J = rev_water.main(tag)
        N = M["names"]
        if src.endswith(".sol"):
            vals = {}
            for line in open(f"{W2}/{src}"):
                p = line.split()
                if len(p) == 2:
                    vals[p[0]] = p[1]
            extra = sorted(set(vals) - set(N))
            X = [Fr(vals.get(nm, "0")) for nm in N]
            note = f"sparse .sol (absent = 0); entries not model variables: {extra}"
        else:
            d = json.load(open(f"{W2}/{src}"))
            X = [Fr(s) for s in d["x"]]
            note = f"stored obj {d['obj']!r}"
        (rv, rn), bv = viol(M, X)
        objsrc = sum(a * X[j] for j, a in M["obj"]["lin"].items())
        # distance to exact point (enclose field values)
        dist = Fr(0)
        for j in range(M["n"]):
            lo, hi = rev_water.enclose(Xe[j], 200)
            dist = max(dist, abs(lo - X[j]), abs(hi - X[j]))
        fe = Fr(J["objective"])
        print(f"waterno2_{tag}: source {src} ({note})")
        print(f"   source point: max row violation {float(rv):.3e} (row {rn}), max bound violation {float(bv):.3e}, "
              f"objective (sum of cost values) {float(objsrc)!r}")
        print(f"   exact point objective - source objective = {float(fe - objsrc):.4e}; "
              f"max |x_exact - x_source| <= {float(dist):.3e}")


if __name__ == "__main__":
    main()
