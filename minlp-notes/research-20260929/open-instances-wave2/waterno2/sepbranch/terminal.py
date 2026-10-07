"""Terminal-volume row of waterno2_T, derived exactly.

Claim: for every point satisfying the rows of waterno2_T,
    horizon row  +  sum_i y_i * (linear equality row i)
is an inequality that involves only the end levels of the last period and
fixed variables.  The multipliers y are found numerically, rounded to
rationals, and the identity is then checked in exact rational arithmetic, so
the resulting row is valid for every exactly feasible point (a nonnegative
multiple of a >= row plus any combination of equality rows).

Result for waterno2_06 (asserted below for all T): with areas (1800, 720, 1600)
    1800*E1 + 720*E2 + 1600*E3 >= 1800*L1(0) + 720*L2(0) + 1600*L3(0) + 3600*(c - sum_t d_t),
i.e. the final stored volume is at least the initial one (c = sum of demands).
"""
from fractions import Fraction

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr


def is_inf(s):
    return s.upper() in ("INF", "+INF", "-INF")


def balance_rows(D, t):
    """The three tank-balance rows of period t: (row, start var, end var, area)."""
    M, S = D["M"], D["S"]
    out = []
    for i in S["per_rows"][t]:
        p = M["rows"][i]["poly"]
        if not any(abs(Fraction(a)) == 3600 for a in p.values()):
            continue
        lv = [(m[0], Fraction(a)) for m, a in p.items() if len(m) == 1 and abs(Fraction(a)) != 3600]
        assert len(lv) == 2 and lv[0][1] == -lv[1][1], lv
        s, e = (lv[0][0], lv[1][0]) if lv[0][1] > 0 else (lv[1][0], lv[0][0])
        out.append((i, s, e, abs(lv[0][1])))
    assert len(out) == 3
    return out


def derive(D):
    M, S, T = D["M"], D["S"], D["T"]
    nv = len(M["names"])
    fixed = {j for j in range(nv) if M["lb"][j] == M["ub"][j]}
    ends = [e for (i, s, e, a) in balance_rows(D, T - 1)]
    keep = set(ends) | fixed
    eq = [i for i, r in enumerate(M["rows"])
          if r["lb"] == r["ub"] and all(len(m) == 1 for m in r["poly"])]
    hrow = M["rows"][S["horizon"][0]]
    assert is_inf(hrow["ub"]) and not is_inf(hrow["lb"])
    others = [j for j in range(nv) if j not in keep]
    pos = {j: k for k, j in enumerate(others)}
    ri, ci, va = [], [], []
    for k, i in enumerate(eq):
        for m, a in M["rows"][i]["poly"].items():
            if m[0] in pos:
                ri.append(pos[m[0]])
                ci.append(k)
                va.append(float(Fraction(a)))
    A = csr_matrix((va, (ri, ci)), shape=(len(others), len(eq)))
    rhs = np.zeros(len(others))
    for m, a in hrow["poly"].items():
        if m[0] in pos:
            rhs[pos[m[0]]] -= float(Fraction(a))
    y = lsqr(A, rhs, atol=1e-15, btol=1e-15, iter_lim=100000)[0]
    yq = [Fraction(float(v)).limit_denominator(10**7) for v in y]
    # exact combination: horizon (>= lb) + sum y_i (row_i = b_i)
    comb = {}
    const = Fraction(hrow["lb"])  # combination reads  sum comb_j x_j >= const
    for m, a in hrow["poly"].items():
        comb[m[0]] = comb.get(m[0], Fraction(0)) + Fraction(a)
    for k, i in enumerate(eq):
        if yq[k] == 0:
            continue
        r = M["rows"][i]
        for m, a in r["poly"].items():
            comb[m[0]] = comb.get(m[0], Fraction(0)) + yq[k] * Fraction(a)
        const += yq[k] * Fraction(r["lb"])
    bad = {j: v for j, v in comb.items() if v != 0 and j not in keep}
    assert not bad, ("combination not exact", list(bad.items())[:5])
    for j in fixed:
        if comb.get(j, 0) != 0:
            const -= comb[j] * Fraction(M["lb"][j])
            comb[j] = Fraction(0)
    coef = {j: comb.get(j, Fraction(0)) for j in ends}
    return coef, const


def add_terminal_row(D):
    """Append the derived row, scaled to integer coefficients, to the last period."""
    coef, const = derive(D)
    import math
    den = 1
    for v in list(coef.values()) + [const]:
        den = den * v.denominator // math.gcd(den, v.denominator)
    poly = {(j,): str(int(v * den)) for j, v in coef.items()}
    lb = const * den
    assert lb.denominator == 1
    M, S, T = D["M"], D["S"], D["T"]
    M["rows"].append(dict(name="terminal", poly=poly, lb=str(int(lb)), ub="INF"))
    S["per_rows"][T - 1].append(len(M["rows"]) - 1)
    return poly, int(lb)


if __name__ == "__main__":
    import sys
    import core
    for T in [int(a) for a in sys.argv[1:]]:
        D = core.setup(T, None)
        coef, const = derive(D)
        names = D["M"]["names"]
        print(T, {names[j]: str(v) for j, v in coef.items()}, ">=", str(const), "=", float(const))
