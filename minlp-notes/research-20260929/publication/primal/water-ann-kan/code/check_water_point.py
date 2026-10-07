"""Second, separately written exact check of a waterno2 point file (points/waterno2_TT.exact.json).

It does not use qfield.py or the construction.  Each symbol w_k (root of
A w^2 + B w + C in (lo, hi)) is rewritten as w_k = (-B + s sqrt(d)) / (2A) with
d = B^2 - 4AC and the sign s fixed exactly from (lo, hi).  Values are pairs
(a, b) meaning a + b sqrt(d_k); products use sqrt(d)^2 = d.  Signs are decided
by comparing a^2 with b^2 d.  Every OSIL row, bound and integrality requirement
is checked exactly, and the objective is recomputed.

usage: python3 check_water_point.py points/waterno2_TT.exact.json
"""
import json
import sys
from fractions import Fraction as Fr

import osil


class E:
    """a + b sqrt(d_k); k None: rational."""
    __slots__ = ("k", "a", "b")
    D = {}

    def __init__(self, k, a, b=Fr(0)):
        if b == 0:
            k = None
        self.k, self.a, self.b = k, Fr(a), Fr(b)

    def _k(self, o):
        if self.k is None:
            return o.k
        if o.k is None or o.k == self.k:
            return self.k
        raise ValueError("two different fields in one expression")

    def __add__(self, o):
        o = o if isinstance(o, E) else E(None, o)
        return E(self._k(o), self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, E) else E(None, o)
        return E(self._k(o), self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        o = o if isinstance(o, E) else E(None, o)
        k = self._k(o)
        d = E.D[k] if k is not None else Fr(0)
        return E(k, self.a * o.a + self.b * o.b * d, self.a * o.b + self.b * o.a)

    def sign(self):
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        d = E.D[self.k]
        sb = 1 if b > 0 else -1
        if a == 0:
            return sb
        sa = 1 if a > 0 else -1
        if sa == sb:
            return sa
        # opposite signs: compare a^2 with b^2 d
        c = a * a - b * b * d
        assert c != 0
        return sa if c > 0 else sb


def side(A, B, C, s, t):
    """sign of root_s - t, root_s = (-B + s sqrt(d)) / (2A), A > 0."""
    d = B * B - 4 * A * C
    # root - t = (-B - 2 A t + s sqrt(d)) / (2A)
    E.D["tmp"] = d
    return E("tmp", -B - 2 * A * t, s).sign()


def load_point(P, M):
    syms = {}
    for k, s in P["symbols"].items():
        A, B, C, lo, hi = (Fr(s[f]) for f in ("A", "B", "C", "lo", "hi"))
        assert A > 0
        d = B * B - 4 * A * C
        assert d > 0
        cands = [sg for sg in (1, -1) if side(A, B, C, sg, lo) > 0 and side(A, B, C, sg, hi) < 0]
        assert len(cands) == 1, "isolating interval must contain exactly one root"
        sg = cands[0]
        E.D[int(k)] = d
        syms[int(k)] = (-B / (2 * A), Fr(sg) / (2 * A))  # w = p + q sqrt(d)
    x = []
    for nm in M["names"]:
        v = P["x"][nm]
        if isinstance(v, str):
            x.append(E(None, Fr(v)))
        else:
            k = int(v["w"])
            p, q = syms[k]
            c0, c1 = Fr(v["c0"]), Fr(v["c1"])
            x.append(E(k, c0 + c1 * p, c1 * q))
    return x


def tree(t, x):
    if t[0] == "var":
        return x[t[1]] * t[2]
    if t[0] == "num":
        return E(None, t[1])
    if t[0] == "pow":
        assert t[2][0] == "num" and t[2][1] == 3
        b = tree(t[1], x)
        return b * b * b
    raise ValueError(t[0])


def main(path):
    P = json.load(open(path))
    M = osil.load(P["instance"])
    x = load_point(P, M)
    neq = nin = 0
    for c in M["cons"]:
        v = E(None, c["const"])
        for j, a in c["lin"].items():
            v = v + x[j] * a
        for i, j, a in c["quad"]:
            v = v + x[i] * x[j] * a
        if c["nl"] is not None:
            v = v + tree(c["nl"], x)
        if c["lb"] is not None and c["lb"] == c["ub"]:
            r = v - c["lb"]
            assert r.a == 0 and r.b == 0, c["name"]
            neq += 1
        else:
            if c["lb"] is not None:
                assert (v - c["lb"]).sign() >= 0, c["name"]
            if c["ub"] is not None:
                assert (v - c["ub"]).sign() <= 0, c["name"]
            nin += 1
    for j, nm in enumerate(M["names"]):
        if M["lb"][j] is not None:
            assert (x[j] - M["lb"][j]).sign() >= 0, nm
        if M["ub"][j] is not None:
            assert (x[j] - M["ub"][j]).sign() <= 0, nm
        if M["vtype"][j] in ("B", "I"):
            assert x[j].k is None and x[j].a.denominator == 1, nm
    obj = E(None, M["obj"]["const"])
    for j, a in M["obj"]["lin"].items():
        obj = obj + x[j] * a
    assert not M["obj"]["quad"] and M["obj"]["nl"] is None
    assert obj.k is None and obj.a == Fr(P["objective"])
    print(f"{P['instance']}: {neq} equality rows hold exactly, {nin} inequality rows and all "
          f"{len(M['names'])} variable bounds hold, integrality holds; objective = {P['objective']} "
          f"(= {float(obj.a):.12f}); {len(P['symbols'])} quadratic-irrational speeds")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
