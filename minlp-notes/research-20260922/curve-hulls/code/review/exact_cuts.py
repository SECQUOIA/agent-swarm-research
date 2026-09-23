"""Exact-rational validity check of saved curve-hull cuts for (t, k2 t^2, k3 t^3) curves.

For a cut {v, funcs, l, u, c0, c}, the claim is p(t) = c0 + c[0] t + c[1] g1(t) + c[2] g2(t) >= 0 on [l, u].
All floats are converted exactly to Fractions.  p is a cubic with rational coefficients; its minimum on an
interval is attained at an endpoint or at a real root of p' in the interval.  Roots are r = (-B +- sqrt(D)) / (2A)
(A, B, C of p' = A t^2 + B t + C); p(r) is reduced exactly to X + Y sqrt(D) and its sign decided exactly.
Checked on two intervals: the float bounds stored in the cut file, and the exact decimal bounds from the
OSiL file (these differ by rounding, e.g. .58); the check uses their union.
Also checks: l, u equal the OSiL bounds of variable v (as floats); v has a diagonal x_v^2 term and an
x_v^3 term in the OSiL model; funcs are exactly k*t**2 and k*t**3 with k a power of two.
python exact_cuts.py <instance> [cuts file]"""
import json, math, os, sys
from fractions import Fraction as F
import mpmath
import rbuild

mpmath.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))


def sign_surd(X, Y, D):
    """Exact sign of X + Y sqrt(D), D >= 0 rational."""
    if Y == 0 or D == 0:
        return (X > 0) - (X < 0)
    sy = 1 if Y > 0 else -1
    if X == 0:
        return sy
    sx = 1 if X > 0 else -1
    if sx == sy:
        return sx
    # opposite signs: compare X^2 with Y^2 D
    d = X * X - Y * Y * D
    return sx if d > 0 else (sy if d < 0 else 0)


class Surd:
    """a + b sqrt(D) with rational a, b and fixed D."""
    def __init__(s, a, b, D):
        s.a, s.b, s.D = F(a), F(b), D

    def __add__(s, o):
        o = o if isinstance(o, Surd) else Surd(o, 0, s.D)
        return Surd(s.a + o.a, s.b + o.b, s.D)

    def __mul__(s, o):
        o = o if isinstance(o, Surd) else Surd(o, 0, s.D)
        return Surd(s.a * o.a + s.b * o.b * s.D, s.a * o.b + s.b * o.a, s.D)

    def sign(s):
        return sign_surd(s.a, s.b, s.D)

    def mp(s):
        return mpmath.mpf(s.a.numerator) / s.a.denominator + \
            mpmath.mpf(s.b.numerator) / s.b.denominator * mpmath.sqrt(mpmath.mpf(s.D.numerator) / s.D.denominator)


def cubic_min(coef, lo, hi):
    """coef = [a0, a1, a2, a3] Fractions; exact minimum sign info on [lo, hi].
    Returns (sign of min, mp value of min, argmin description)."""
    p = lambda t: ((coef[3] * t + coef[2]) * t + coef[1]) * t + coef[0]
    cands = [(p(lo), "l"), (p(hi), "u")]
    best_sign = min((v > 0) - (v < 0) for v, _ in cands)
    vals = [(mpmath.mpf(v.numerator) / v.denominator, w) for v, w in cands]
    A, B, C = 3 * coef[3], 2 * coef[2], coef[1]
    roots = []
    if A == 0:
        if B != 0:
            r = -C / B
            if lo <= r <= hi:
                v = p(r)
                roots.append(((v > 0) - (v < 0), mpmath.mpf(v.numerator) / v.denominator))
    else:
        D = B * B - 4 * A * C
        if D >= 0:
            for s in (1, -1):
                r = Surd(-B / (2 * A), F(s) / (2 * A), D)  # (-B +- sqrt(D)) / (2A)
                if (r + (-lo)).sign() >= 0 and (Surd(hi, 0, D) + r * (-1)).sign() >= 0:
                    v = ((r * coef[3] + coef[2]) * r + coef[1]) * r + coef[0]
                    roots.append((v.sign(), v.mp()))
    for sg, val in roots:
        best_sign = min(best_sign, sg)
        vals.append((val, "crit"))
    mv = min(vals, key=lambda z: z[0])
    return best_sign, mv[0], mv[1]


def main(name, path=None):
    path = path or os.path.join(HERE, "..", "cuts", f"{name}.json")
    cuts = json.load(open(path))
    P = rbuild.parse(name)
    sq = {i for c in P["cons"] for i, j, _ in c["quad"] if i == j}
    cu = {i for c in P["cons"] for i in c["cube"]}
    nbad = nfail_exact = 0
    worst = None
    worst_rel = None
    for c in cuts:
        v = c["v"]
        d = P["V"][v]
        assert d["type"] == "C", d
        assert v in sq and v in cu, v
        assert c["l"] == d["lb"] and c["u"] == d["ub"], (v, c["l"], c["u"], d)
        k = [rbuild.func_multiplier(f) for f in c["funcs"]]
        assert [p for _, p in k] == [2, 3] and all(kk & (kk - 1) == 0 for kk, _ in k), c["funcs"]
        coef = [F(c["c0"]), F(c["c"][0]), F(c["c"][1]) * k[0][0], F(c["c"][2]) * k[1][0]]
        lo = min(F(c["l"]), F(d["lb_s"]))
        hi = max(F(c["u"]), F(d["ub_s"]))
        sg, val, where = cubic_min(coef, lo, hi)
        scale = sum(abs(mpmath.mpf(x.numerator) / x.denominator) for x in coef[1:])
        rel = val / scale
        if sg < 0:
            nfail_exact += 1
        if worst is None or val < worst[0]:
            worst = (val, v, where)
        if worst_rel is None or rel < worst_rel[0]:
            worst_rel = (rel, v, where)
    print(json.dumps({"name": name, "file": os.path.basename(path), "ncuts": len(cuts),
                      "violated_exactly": nfail_exact,
                      "worst_abs_slack": mpmath.nstr(worst[0], 6), "worst_abs_at_var": worst[1], "worst_abs_where": worst[2],
                      "worst_rel_slack": mpmath.nstr(worst_rel[0], 6), "worst_rel_at_var": worst_rel[1],
                      "distinct_vars": len({c['v'] for c in cuts})}))


if __name__ == "__main__":
    main(*sys.argv[1:])
