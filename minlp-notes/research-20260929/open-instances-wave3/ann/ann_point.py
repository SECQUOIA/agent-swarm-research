"""Full OSIL point of ann_cumene_tanh from the 5 inputs (60 digits): forward rows, then the
undetermined variables from the bilinear rows (x787..x791 = RHS/x746, x792 from e787 / x766,
x793 = 1 - x792, x754 = x747 x748 / x753, x756 from e750).  Evaluates every row and bound.

    python3 ann_point.py u1 u2 u3 u4 u5
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import ev  # noqa: E402

import ann_model as am  # noqa: E402

ev.MPFNS["tanh"] = mp.tanh


def build(u, dps=60):
    D = am.decode()
    I = D["I"]
    N = D["names"]
    idx = {n: j for j, n in enumerate(N)}
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    with mp.workdps(dps):
        x = [None] * len(N)
        for i, j in enumerate(D["inputs"]):
            x[j] = mp.mpf(u[i])
        for op in D["ops"]:
            if op[0] == "lin":
                _, v, cv, terms, rhs = op
                s = q(rhs)
                for o, a in terms:
                    s -= q(a) * x[o]
                x[v] = s / q(cv)
            else:
                x[op[1]] = mp.tanh(x[op[2]])
        byname = {c["name"]: c for c in I["cons"]}
        # e782..e786: x746*x78k + sum others = 0
        for e, v in zip(["e782", "e783", "e784", "e785", "e786"], ["x787", "x788", "x789", "x790", "x791"]):
            c = byname[e]
            s = mp.mpf(0); coef = None
            for a, b, cc in c["quad"]:
                if idx[v] in (a, b):
                    coef = mp.mpf(cc)
                else:
                    s += mp.mpf(cc) * x[a] * x[b]
            x[idx[v]] = -s / (coef * x[idx["x746"]])
        c = byname["e787"]
        s = mp.mpf(0); coef = None
        for a, b, cc in c["quad"]:
            if idx["x792"] in (a, b):
                coef = mp.mpf(cc)
            else:
                s += mp.mpf(cc) * x[a] * x[b]
        x[idx["x792"]] = -s / (coef * x[idx["x766"]])
        x[idx["x793"]] = 1 - x[idx["x792"]]
        x[idx["x754"]] = x[idx["x747"]] * x[idx["x748"]] / x[idx["x753"]]
        x[idx["x756"]] = 1 - x[idx["x754"]] - x[idx["x755"]] - x[idx["x778"]]
        # objvar from e790
        c = byname["e790"]
        s = mp.mpf(0)
        for j, a in c["lin"].items():
            if N[j] != "objvar":
                s += mp.mpf(a) * x[j]
        for a, b, cc in c["quad"]:
            s += mp.mpf(cc) * x[a] * x[b]
        x[idx["objvar"]] = s - mp.mpf(c["lb"])     # -objvar + s = lb
        assert all(v is not None for v in x)
        return I, x


if __name__ == "__main__":
    I, x = build(sys.argv[1:6])
    r = ev.evaluate(I, x, 60)
    print(f"obj {mp.nstr(r['obj'], 20)}  max row viol {mp.nstr(r['row_viol'], 3)} ({r['worst_row']})  "
          f"max bound viol {mp.nstr(r['bound_viol'], 3)} ({r['worst_var']})")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sol", "ann_cumene_tanh.wave3.sol")
    with open(out, "w") as f:
        for nm, v in zip(I["names"], x):
            f.write(f"{nm} {mp.nstr(v, 30, min_fixed=-10**9, max_fixed=10**9)}\n")
    vals = ev.read_sol(out)
    r2 = ev.evaluate(I, [vals[n] for n in I["names"]], 60)
    print(f"rounded 30-digit point: obj {mp.nstr(r2['obj'], 20)}  max row viol {mp.nstr(r2['row_viol'], 3)} ({r2['worst_row']})  "
          f"max bound viol {mp.nstr(r2['bound_viol'], 3)}")
