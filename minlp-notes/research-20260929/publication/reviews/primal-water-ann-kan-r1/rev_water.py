"""Reviewer's exact check of the author's waterno2 points (independent code).

Each coordinate in points/waterno2_XX.exact.json is a rational or c0 + c1*w_k, where w_k
is a root of A w^2 + B w + C in (lo, hi).  Here w_k is written exactly as p_k + q_k*sqrt(D_k)
and every row is evaluated in the multi-quadratic field Q(sqrt(D_1), ..., sqrt(D_m)),
with elements stored as {frozenset(S): Fraction} = sum_S c_S prod_{i in S} sqrt(D_i).
Products use sqrt(D_i)^2 = D_i exactly.  Sign decisions:
  - all coefficients 0               -> value is exactly 0;
  - else an enclosure from rational bounds on each sqrt(D_i) (integer isqrt, no floating point);
    if it excludes 0 the sign is decided; otherwise the row is reported UNDECIDED.
For elements of a single field a + b sqrt(D) the sign is also decided exactly
(compare a^2 with b^2 D) as a cross-check.
usage: python3 rev_water.py 06|09|12|18|24
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../..'))
import json
import math
import sys
import time
from fractions import Fraction as Fr

import rosil

PTS = _RESEARCH + "/publication/primal/water-ann-kan/points"

# exact certified duals (reviews/waterno2-cellslopes-review.md line 237; reviews/waterno2-recheck.md lines 262-265)
DUAL = {
    "06": Fr(39157472136693483, 140737488355328),
    "09": Fr(3627661341387654598825371, 4398046511104000000000),
    "12": Fr(9190837775594918144252281, 4398046511104000000000),
    "18": Fr(5267563083146225483626937, 1099511627776000000000),
    "24": Fr(115688878681251187594323079, 17592186044416000000000),
}


class MQ:
    """Element of Q(sqrt(D_1),...,sqrt(D_m)); D is a shared list of rationals."""
    D = []
    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = {} if t is None else {k: v for k, v in t.items() if v != 0}

    @staticmethod
    def num(q):
        return MQ({frozenset(): Fr(q)})

    def __add__(self, o):
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return MQ(r)

    def __neg__(self):
        return MQ({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                c = v1 * v2
                for i in k1 & k2:
                    c *= MQ.D[i]
                k = k1 ^ k2
                r[k] = r.get(k, 0) + c
        return MQ(r)

    def is_zero(self):
        return not self.t

    def rational(self):
        if not self.t:
            return Fr(0)
        if list(self.t) == [frozenset()]:
            return self.t[frozenset()]
        return None


SQB = {}  # (i, P) -> (lo, hi) rational bounds of sqrt(D_i)


def sqrt_bounds(i, P):
    key = (i, P)
    if key not in SQB:
        D = MQ.D[i]
        n, d = D.numerator, D.denominator
        assert n > 0 and d > 0
        s = math.isqrt(n * d * 4 ** P)  # s <= sqrt(n d) 2^P < s + 1
        SQB[key] = (Fr(s, 2 ** P * d), Fr(s + 1, 2 ** P * d))
    return SQB[key]


def enclose(x, P=400):
    lo = hi = Fr(0)
    for k, c in x.t.items():
        a, b = Fr(1), Fr(1)
        for i in k:
            l, h = sqrt_bounds(i, P)
            a, b = a * l, b * h
        if c >= 0:
            lo, hi = lo + c * a, hi + c * b
        else:
            lo, hi = lo + c * b, hi + c * a
    return lo, hi


def sign(x):
    if x.is_zero():
        return 0
    # exact single-field decision when possible
    ks = [k for k in x.t if k]
    if len(ks) == 1 and len(ks[0]) == 1:
        (i,) = ks[0]
        a = x.t.get(frozenset(), Fr(0))
        b = x.t[ks[0]]
        D = MQ.D[i]
        sb = 1 if b > 0 else -1
        if a == 0:
            ex = sb
        elif (a > 0) == (b > 0):
            ex = 1 if a > 0 else -1
        else:
            # a + b sqrt(D), opposite signs: sign = sign(a) if a^2 > b^2 D else sign(b)
            ex = (1 if a > 0 else -1) if a * a > b * b * D else sb
            assert a * a != b * b * D
    else:
        ex = None
    for P in (400, 2000):
        lo, hi = enclose(x, P)
        if lo > 0:
            s = 1
            break
        if hi < 0:
            s = -1
            break
    else:
        s = None
    if ex is not None:
        assert s == ex, ("exact/enclosure sign mismatch", s, ex)
    return s


class AMQ:
    num = staticmethod(MQ.num)


def main(tag):
    t0 = time.time()
    name = f"waterno2_{tag}"
    J = json.load(open(f"{PTS}/{name}.exact.json"))
    M = rosil.load(name)
    N = M["names"]
    print(f"{name}: {M['n']} variables, {len(M['cons'])} rows; point file {name}.exact.json "
          f"({len(J['x'])} values, {len(J['symbols'])} quadratic symbols)")
    # --- symbols
    MQ.D = []
    SQB.clear()  # sqrt bounds are per instance
    W = {}
    for k, s in J["symbols"].items():
        A, B, C, lo, hi = (Fr(s[f]) for f in ("A", "B", "C", "lo", "hi"))
        assert A != 0 and lo < hi
        q = lambda w: A * w * w + B * w + C
        assert q(lo) * q(hi) < 0, (k, "no sign change on (lo, hi)")
        D = B * B - 4 * A * C
        assert D > 0
        i = len(MQ.D)
        MQ.D.append(D)
        found = []
        for sg in (1, -1):
            r = MQ({frozenset(): -B / (2 * A), frozenset([i]): Fr(sg) / (2 * A)})
            if sign(r - MQ.num(lo)) == 1 and sign(MQ.num(hi) - r) == 1:
                found.append((sg, r))
        assert len(found) == 1, (k, "root selection", len(found))
        r = found[0][1]
        assert (MQ.num(A) * r * r + MQ.num(B) * r + MQ.num(C)).is_zero()
        W[int(k)] = r
        # D a perfect square? (then w is rational; harmless)
    print(f"symbols: {len(W)} roots identified exactly (sign change on (lo,hi) and the root lies in (lo,hi)); "
          f"max width hi-lo = {max(float(Fr(s['hi']) - Fr(s['lo'])) for s in J['symbols'].values()):.1e}")
    # --- values
    X = [None] * M["n"]
    nfield = 0
    for j, nm in enumerate(N):
        v = J["x"][nm]
        if isinstance(v, str):
            X[j] = MQ.num(Fr(v))
        else:
            nfield += 1
            assert set(v) == {"w", "c0", "c1"}, v
            X[j] = MQ.num(Fr(v["c0"])) + MQ.num(Fr(v["c1"])) * W[int(v["w"])]
    assert len(J["x"]) == M["n"]
    print(f"values: {M['n'] - nfield} rational, {nfield} in a quadratic field")
    # --- integrality and bounds
    nb = 0
    for j in range(M["n"]):
        if M["vtype"][j] in ("B", "I"):
            r = X[j].rational()
            assert r is not None and r.denominator == 1, N[j]
            nb += 1
        if M["lb"][j] is not None:
            assert sign(X[j] - MQ.num(M["lb"][j])) in (0, 1), ("lb", N[j])
        if M["ub"][j] is not None:
            assert sign(MQ.num(M["ub"][j]) - X[j]) in (0, 1), ("ub", N[j])
    print(f"integrality: {nb} binaries integral (and within [0,1] by the bound check); all {M['n']} variable bounds hold exactly")
    # --- rows
    neq = nin = nmulti = 0
    tight = 0
    bad = []
    und = []
    for c in M["cons"]:
        body = rosil.eval_body(c, X, AMQ)
        nf = set()
        for k in body.t:
            nf |= k
        if len(nf) > 1:
            nmulti += 1
        if c["lb"] is not None and c["lb"] == c["ub"]:
            neq += 1
            if not (body - MQ.num(c["lb"])).is_zero():
                s = sign(body - MQ.num(c["lb"]))
                (und if s is None else bad).append((c["name"], "eq", s))
            continue
        nin += 1
        for side, d in (("lb", None if c["lb"] is None else body - MQ.num(c["lb"])),
                        ("ub", None if c["ub"] is None else MQ.num(c["ub"]) - body)):
            if d is None:
                continue
            s = sign(d)
            if s is None:
                und.append((c["name"], side))
            elif s < 0:
                bad.append((c["name"], side))
            elif s == 0:
                tight += 1
    print(f"rows: {neq} equalities, {nin} inequalities; rows whose value involves >1 field: {nmulti}; "
          f"tight inequality sides: {tight}; violated: {bad[:5]} ({len(bad)}); undecided: {und[:5]} ({len(und)})")
    assert not bad and not und
    # --- objective
    o = M["obj"]
    assert o["sense"] == "min" and o["const"] == 0 and not o["quad"] and o["nl"] is None
    f = MQ.num(0)
    for j, a in o["lin"].items():
        f = f + MQ.num(a) * X[j]
    fr = f.rational()
    claimed = Fr(J["objective"])
    if fr is not None:
        print(f"objective: exactly rational = {fr} = {float(fr)!r}; equals the claimed value: {fr == claimed}")
        flo = fhi = fr
    else:
        flo, fhi = enclose(f, 400)
        print(f"objective: in a field, enclosure width {float(fhi - flo):.1e}; claimed {claimed}; "
              f"claimed inside enclosure: {flo <= claimed <= fhi}")
    dual = DUAL[tag]
    gap = fhi - dual
    print(f"dual (exact certified rational) {dual} = {float(dual)!r}")
    print(f"rigorous gap = primal - dual = {float(gap)!r} (exact {gap.numerator}/{gap.denominator} if short)"[:300])
    print(f"gap/|dual| = {float(gap / abs(dual)):.6e}; gap/|primal| = {float(gap / abs(flo)):.6e}")
    print(f"time {time.time() - t0:.1f} s")
    return X, M, J


if __name__ == "__main__":
    main(sys.argv[1])
