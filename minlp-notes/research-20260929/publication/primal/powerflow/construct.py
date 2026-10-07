"""Phase 1 (construction, floating point only): build a candidate exactly feasible point.

    python3 construct.py <name>

1. Start from MINLPLib's point p1 (open-instances-wave3/sol/<name>.p1.sol).
2. Active set: inequality sides with slack < ACT at p1.
3. Fixed variables (exact rationals):
   - a variable whose single-variable linear equality row says a*x = b gets x = b/a;
   - a variable with an active single-variable bound row gets that bound exactly;
   - the remaining degrees of freedom are chosen by column-pivoted QR of the Jacobian
     of the square system; those variables keep p1's decimal value (an exact rational).
4. Square system S: every other equality row, plus every active row with two or more
   variables, taken as an equality at its active side.
5. Simplified Newton in 70-digit arithmetic (float LU of the Jacobian at p1 as the
   iteration matrix) on S for the free variables.
6. Write points/<name>.json: fixed values, the 60-digit centre of the free variables,
   the rows of S with their sides.  Nothing here is a proof; certify.py checks the file.
"""
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np
import scipy.linalg as sl
from mpmath import mp

import pfmodel as pm

HERE = os.path.dirname(os.path.abspath(__file__))
ACT = mp.mpf("1e-9")


def single_var(c):
    return c["nl"] is None and not c["quad"] and len(c["lin"]) == 1


def main(name):
    mp.dps = 70
    I = pm.load(name)
    cons, names = I["cons"], I["names"]
    nv = len(names)
    p1 = pm.read_p1(I, name)
    x = [mp.mpf(s) for s in p1]
    num = pm.ctx_num(mp)
    fixed = {}
    why = {}

    def fix(j, val, reason):
        if j in fixed:
            assert fixed[j] == val, (names[j], fixed[j], val)
        fixed[j] = val
        why[j] = reason

    S = []
    for c in cons:
        v = pm.ev_row(c, x, mp, num).v
        eq = c["lbF"] is not None and c["lbF"] == c["ubF"]
        if single_var(c):
            (j, a), = c["lin"].items()
            a, k = Fr(a), Fr(c["constant"])
            if eq:
                fix(j, (c["lbF"] - k) / a, f"equality row {c['name']}")
            else:
                for side in ("lb", "ub"):
                    b = c[side + "F"]
                    if b is not None and abs(v - mp.mpf(c[side])) < ACT:
                        fix(j, (b - k) / a, f"active {side} of {c['name']}")
            continue
        if eq:
            S.append((c["name"], "lb"))
            continue
        for side in ("lb", "ub"):
            if c[side + "F"] is not None and abs(v - mp.mpf(c[side])) < ACT:
                S.append((c["name"], side))
    byname = {c["name"]: c for c in cons}
    free = [j for j in range(nv) if j not in fixed]
    for j, q in fixed.items():
        x[j] = mp.mpf(q.numerator) / q.denominator
    # Jacobian of S w.r.t. the not-yet-fixed variables, at p1
    col = {j: t for t, j in enumerate(free)}
    J = np.zeros((len(S), len(free)))
    for i, (rn, side) in enumerate(S):
        d = pm.ev_row(byname[rn], x, mp, num)
        for j, g in d.g.items():
            if j in col:
                J[i, col[j]] += float(g)
    m = len(S)
    assert m <= len(free), (m, len(free))
    _, R, piv = sl.qr(J, pivoting=True, mode="economic")
    basic = sorted(free[k] for k in piv[:m])
    for k in piv[m:]:
        fix(free[k], Fr(p1[free[k]]), "degree of freedom kept at p1 (QR choice)")
        x[free[k]] = mp.mpf(p1[free[k]])
    col = {j: t for t, j in enumerate(basic)}

    def FJ(xx, jac):
        F = []
        Jm = np.zeros((m, m)) if jac else None
        for i, (rn, side) in enumerate(S):
            c = byname[rn]
            d = pm.ev_row(c, xx, mp, num)
            F.append(d.v - mp.mpf(c[side]))
            if jac:
                for j, g in d.g.items():
                    if j in col:
                        Jm[i, col[j]] += float(g)
        return F, Jm

    F, J0 = FJ(x, True)
    print(f"{name}: |S| = {m}, free = {len(basic)}, fixed = {len(fixed)}, cond(J) = {np.linalg.cond(J0):.3e}")
    print("  p1 residual of S:", mp.nstr(max(abs(f) for f in F), 3))
    lu = sl.lu_factor(J0)
    for it in range(40):
        F, _ = FJ(x, False)
        res = max(abs(f) for f in F)
        print(f"  iter {it}: max |F| = {mp.nstr(res, 3)}")
        if res < mp.mpf("1e-62"):
            break
        # correction: float solve of a scaled residual (the scale keeps it in float range)
        sc = float(res)
        dx = sl.lu_solve(lu, np.array([float(f / sc) for f in F]))
        for j, t in col.items():
            x[j] -= mp.mpf(dx[t]) * sc
    else:
        raise SystemExit("Newton did not converge")
    move = max(abs(x[j] - mp.mpf(p1[j])) for j in basic)
    print("  max move of free variables from p1:", mp.nstr(move, 3))
    obj = pm.ev_obj(I, x, mp, num)
    print("  objective at centre (float, 70 digits):", mp.nstr(obj, 25))
    out = dict(
        instance=name,
        note="centre of a Krawczyk box; fixed variables are exact rationals; see certify.py",
        radius="1e-45",
        system=[dict(row=rn, side=side) for rn, side in S],
        fixed={names[j]: dict(value=f"{q.numerator}/{q.denominator}", reason=why[j]) for j, q in sorted(fixed.items())},
        free={names[j]: mp.nstr(x[j], 60, strip_zeros=False) for j in basic},
    )
    os.makedirs(os.path.join(HERE, "points"), exist_ok=True)
    with open(os.path.join(HERE, "points", f"{name}.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    reasons = {}
    for j, r in why.items():
        key = r.split(" ")[0] + " " + r.split(" ")[1]
        reasons.setdefault(key, []).append(names[j])
    for k, v in reasons.items():
        print(f"  fixed ({k}...): {len(v)}: {' '.join(v)}")
    act = [f"{rn}:{side}" for rn, side in S if byname[rn]["lbF"] != byname[rn]["ubF"]]
    print("  active multi-variable inequality rows in S:", " ".join(act))


if __name__ == "__main__":
    main(sys.argv[1])
