"""Library-independent re-check of the lnts existence proofs (no mpmath).

Usage: python3 verify_no_mpmath.py 50 100 200 400

Same construction as verify_lnts_points.py (own OSiL reader and generic
elimination plan are reused from it; they do no floating-point work), but all
numerics use the interval type DI below:
  * an interval is [lo, hi] * 2^-P with Python integers lo <= hi (exact);
  * +, - are exact; * rounds the lower end down (floor) and the upper end up
    (ceil); constants are enclosed by floor/ceil of q * 2^P;
  * sin and cos at a rational point x with |x| <= 1.4 are enclosed by the
    Taylor partial sum S_n plus/minus the first omitted term (alternating
    series whose terms decrease in magnitude, since x^2 <= (n+1)(n+2)),
    computed in exact Fractions; on an interval inside [-1.4, 1.4], sin is
    increasing and cos is increasing on [-1.4, 0] and decreasing on [0, 1.4].
Assumptions: Python integer and Fraction arithmetic are exact; the Taylor
remainder argument above. Nothing else.
"""
import json
import sys
from fractions import Fraction as Fr
from functools import lru_cache

import verify_lnts_points as V

P = 430  # bits after the binary point (about 129 decimal digits)
ONE = 1 << P


def fl(n, d):  # floor(n / d), d > 0
    return n // d


def ce(n, d):
    return -((-n) // d)


class DI:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo, self.hi = lo, hi

    @staticmethod
    def q(x):
        x = Fr(x)
        return DI(fl(x.numerator << P, x.denominator), ce(x.numerator << P, x.denominator))

    def __add__(a, b):
        return DI(a.lo + b.lo, a.hi + b.hi)

    def __sub__(a, b):
        return DI(a.lo - b.hi, a.hi - b.lo)

    def __neg__(a):
        return DI(-a.hi, -a.lo)

    def __mul__(a, b):
        c = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
        return DI(min(c) >> P, -((-max(c)) >> P))

    def ends(a):
        return Fr(a.lo, ONE), Fr(a.hi, ONE)


@lru_cache(maxsize=None)
def taylor(x, which):
    """Enclosure [l, u] (Fractions) of sin(x) or cos(x), |x| <= 1.4, rational x.
    Terms t_n = x^n / n! are kept as integer pairs (num_n, den_n); den_n divides
    every later den, so the partial sum is formed exactly over the last den."""
    x = Fr(x)
    assert abs(x) <= Fr(14, 10)
    p, q = x.numerator, x.denominator
    n = 1 if which == "sin" else 0
    num, den = (p, q) if which == "sin" else (1, 1)
    terms = []
    while True:
        terms.append((num, den))
        num, den = num * p * p, den * q * q * (n + 1) * (n + 2)
        n += 2
        if abs(num) << (P + 16) < den:  # |next term| < 2^-(P+16)
            break
    D = terms[-1][1]
    S = sum((-1) ** k * a * (D // b) for k, (a, b) in enumerate(terms))
    assert all(D % b == 0 for _, b in terms)
    e = Fr(abs(num), den)  # first omitted term bounds the error
    return Fr(S, D) - e, Fr(S, D) + e


def di_from(lo_q, hi_q):
    return DI(fl(lo_q.numerator << P, lo_q.denominator), ce(hi_q.numerator << P, hi_q.denominator))


def di_sin(a):
    lo, hi = a.ends()
    return di_from(taylor(lo, "sin")[0], taylor(hi, "sin")[1])


def di_cos(a):
    lo, hi = a.ends()
    if lo >= 0:  # decreasing
        return di_from(taylor(hi, "cos")[0], taylor(lo, "cos")[1])
    if hi <= 0:  # increasing
        return di_from(taylor(lo, "cos")[0], taylor(hi, "cos")[1])
    return di_from(min(taylor(lo, "cos")[0], taylor(hi, "cos")[0]), Fr(1))


ZERO = DI(0, 0)


class AD:
    __slots__ = ("v", "g")

    def __init__(self, v, g):
        self.v, self.g = v, g

    def __add__(s, o):
        return AD(s.v + o.v, tuple(a + b for a, b in zip(s.g, o.g)))

    def __mul__(s, o):
        return AD(s.v * o.v, tuple(s.v * b + o.v * a for a, b in zip(s.g, o.g)))

    def cmul(s, c):
        return AD(s.v * c, tuple(a * c for a in s.g))


def const(q):
    return AD(DI.q(q), (ZERO,) * 3)


def ev_tree(t, X):
    k = t[0]
    if k == "c":
        return const(t[1])
    if k == "v":
        return X[t[1]].cmul(DI.q(t[2]))
    if k in ("sum", "product"):
        r = ev_tree(t[1], X)
        for u in t[2:]:
            r = (r + ev_tree(u, X)) if k == "sum" else (r * ev_tree(u, X))
        return r
    a = ev_tree(t[1], X)
    if k == "cos":
        d = -di_sin(a.v)
        return AD(di_cos(a.v), tuple(d * x for x in a.g))
    if k == "sin":
        d = di_cos(a.v)
        return AD(di_sin(a.v), tuple(d * x for x in a.g))
    raise ValueError(k)


def ev_row(row, X, skip=None):
    s = const(0)
    for j, c in row["lin"].items():
        if j != skip:
            s = s + X[j].cmul(DI.q(c))
    for i, j, c in row["quad"]:
        s = s + (X[i] * X[j]).cmul(DI.q(c))
    if row["nl"] is not None:
        s = s + ev_tree(row["nl"], X)
    return s


def evaluate(Vv, C, steps, resid, pv):
    X = [None] * len(Vv)
    for j, a in pv.items():
        X[j] = a
    for j, v in enumerate(Vv):
        if v["lb"] == v["ub"] and not V.is_inf(v["lb"]):
            X[j] = const(Fr(v["lb"]))
    for r, u in steps:
        c = C[r]
        cu = c["lin"][u]
        assert cu in (1, -1)  # division by +-1 is exact
        rest = ev_row(c, X, skip=u)
        b = DI.q(Fr(c["lb"]))
        val = b - rest.v
        X[u] = AD(val if cu == 1 else -val, tuple((-g if cu == 1 else g) for g in rest.g))
    F = []
    for r in resid:
        R = ev_row(C[r], X)
        F.append(AD(R.v - DI.q(Fr(C[r]["lb"])), R.g))
    return X, F


def inv3(M):
    """Exact inverse of a 3x3 Fraction matrix (Gauss-Jordan)."""
    n = 3
    A = [list(M[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        assert pv != 0
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def run(N):
    P_ = json.load(open(V.PT.format(N)))
    Vv, obj, C = V.read_osil(P_["osil"])
    names = [v["name"] for v in Vv]
    idx = {nm: j for j, nm in enumerate(names)}
    fixed = {idx[nm]: Fr(s) for nm, s in P_["fixed_controls"].items()}
    zv = [idx[nm] for nm in P_["unknowns_box"]]
    cen = [Fr(P_["unknowns_box"][names[j]]["centre"]) for j in zv]
    rad = [Fr(P_["unknowns_box"][names[j]]["radius"]) for j in zv]
    steps, resid = V.plan(Vv, C, set(fixed) | set(zv))
    assert len(resid) == 3
    Xb = [di_from(c - r, c + r) for c, r in zip(cen, rad)]
    Y = [DI.q(c) for c in cen]
    unit = [tuple(DI(ONE, ONE) if m == k else ZERO for m in range(3)) for k in range(3)]
    base = {j: AD(DI.q(q), (ZERO,) * 3) for j, q in fixed.items()}
    pv = dict(base)
    pv.update({zv[k]: AD(Y[k], (ZERO,) * 3) for k in range(3)})
    _, Fy = evaluate(Vv, C, steps, resid, pv)
    pv = dict(base)
    pv.update({zv[k]: AD(Xb[k], unit[k]) for k in range(3)})
    _, FX = evaluate(Vv, C, steps, resid, pv)
    J = [[FX[i].g[j] for j in range(3)] for i in range(3)]
    Jm = [[sum(J[i][j].ends()) / 2 for j in range(3)] for i in range(3)]
    Cq = inv3(Jm)
    Cd = [[DI(round(x * ONE), round(x * ONE)) for x in row] for row in Cq]  # exact dyadic C
    K = []
    for i in range(3):
        s = Y[i]
        for k in range(3):
            s = s - Cd[i][k] * Fy[k].v
        for j in range(3):
            m = DI(ONE if i == j else 0, ONE if i == j else 0)
            for k in range(3):
                m = m - Cd[i][k] * J[k][j]
            s = s + m * (Xb[j] - Y[j])
        K.append(s)
    ok = all(K[k].lo > Xb[k].lo and K[k].hi < Xb[k].hi for k in range(3))
    assert ok, "Krawczyk failed"
    Z = [DI(max(K[k].lo, Xb[k].lo), min(K[k].hi, Xb[k].hi)) for k in range(3)]
    for k in range(3):
        a, b = Z[k].ends()
        assert cen[k] - rad[k] < a and b < cen[k] + rad[k]
    # full box over Z, bounds, rows (consistency), objective
    pv = dict(base)
    pv.update({zv[k]: AD(Z[k], (ZERO,) * 3) for k in range(3)})
    X, F = evaluate(Vv, C, steps, resid, pv)
    for f in F:
        a, b = f.v.ends()
        assert a <= 0 <= b
    for j, v in enumerate(Vv):
        a, b = X[j].v.ends()
        if not V.is_inf(v["lb"]):
            assert a >= Fr(v["lb"]) and a >= Fr(float(v["lb"])), names[j]
        if not V.is_inf(v["ub"]):
            assert b <= Fr(v["ub"]) and b <= Fr(float(v["ub"])), names[j]
    for c in C:
        a, b = ev_row(c, X).v.ends()
        assert a <= Fr(c["lb"]) <= b
    o = ev_row(obj, X).v
    olo, ohi = o.ends()
    slo, shi = Fr(P_["objective_enclosure"][0]), Fr(P_["objective_enclosure"][1])
    assert slo <= olo and ohi <= shi
    gaps = {tag: float(ohi - Fr(d)) for tag, d in zip(("summary", "verifier"), V.DUALS[N])}
    out = dict(instance=f"lnts{N}", krawczyk_ok=ok, z_widths=[float(z.ends()[1] - z.ends()[0]) for z in Z],
               obj_lo_30=f"{float(olo):.17g}", obj_width=float(ohi - olo),
               obj_inside_stored_25digit=True, gaps=gaps)
    print(json.dumps(out), flush=True)
    return out


if __name__ == "__main__":
    res = [run(int(a)) for a in sys.argv[1:]]
    json.dump(res, open("verify_no_mpmath_" + "_".join(sys.argv[1:]) + ".json", "w"), indent=1)
