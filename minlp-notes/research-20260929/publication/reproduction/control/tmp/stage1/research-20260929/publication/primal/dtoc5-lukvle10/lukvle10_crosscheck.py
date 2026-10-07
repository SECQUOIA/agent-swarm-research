"""lukvle10: second implementation of the enclosure, without mpmath.

- Model read with the open-instances verifier's OSIL reader (reviews/open-instances-verification/
  osilx.py, decimal strings kept exactly), not with osil_exact.py.
- Arithmetic: fixed-point intervals on Python integers (value = integer / 2^P) with explicit
  floor/ceil rounding of every operation (class FI below). exp and log are enclosed by their
  Taylor/atanh series with explicit remainder bounds (functions fi_exp, fi_log). No floating point
  and no mpmath is used in any bound.
- Steps: (1) solve the rows for their pivot variables from the exact seeds (as lukvle10_enclose.py
  does, but coded independently), at P = 2700 bits; (2) check that every coordinate enclosure lies
  in the saved box points/lukvle10_box.txt.gz; (3) enclose the objective over the coordinate
  enclosures and over the saved box, at P = 500 bits.
Same author as lukvle10_enclose.py, so this is a second implementation, not an independent review.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import gzip
import json
import sys
import time
from fractions import Fraction

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
sys.path.insert(0, _REPO + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

OSIL = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/lukvle10.osil')
P_ROWS = 2700
P_OBJ = 500


def fdiv(a, b):  # floor(a / b), b > 0
    return a // b


def cdiv(a, b):  # ceil(a / b), b > 0
    return -((-a) // b)


class FI:
    """closed interval [lo, hi] / 2^P with integer lo <= hi."""
    __slots__ = ("lo", "hi", "P")

    def __init__(self, lo, hi, P):
        assert lo <= hi
        self.lo, self.hi, self.P = lo, hi, P

    @staticmethod
    def frac(q, P):
        q = Fraction(q)
        return FI(fdiv(q.numerator << P, q.denominator), cdiv(q.numerator << P, q.denominator), P)

    def rescale(self, P2):
        """outward rounding to P2 bits"""
        if P2 >= self.P:
            return FI(self.lo << (P2 - self.P), self.hi << (P2 - self.P), P2)
        s = self.P - P2
        return FI(self.lo >> s, cdiv(self.hi, 1 << s), P2)

    def _c(self, o):
        if isinstance(o, FI):
            assert o.P == self.P
            return o
        return FI.frac(o, self.P)

    def __add__(self, o):
        o = self._c(o)
        return FI(self.lo + o.lo, self.hi + o.hi, self.P)

    __radd__ = __add__

    def __neg__(self):
        return FI(-self.hi, -self.lo, self.P)

    def __sub__(self, o):
        return self + (-self._c(o))

    def __rsub__(self, o):
        return self._c(o) - self

    def __mul__(self, o):
        o = self._c(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return FI(min(p) >> self.P, cdiv(max(p), 1 << self.P), self.P)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._c(o)
        assert o.lo > 0 or o.hi < 0, "division by an interval containing 0"
        num = [self.lo << self.P, self.hi << self.P]
        lows, highs = [], []
        for a in num:
            for b in (o.lo, o.hi):
                if b > 0:
                    lows.append(fdiv(a, b)); highs.append(cdiv(a, b))
                else:
                    lows.append(fdiv(-a, -b)); highs.append(cdiv(-a, -b))
        return FI(min(lows), max(highs), self.P)

    def sq(self):
        if self.lo >= 0:
            return FI(fdiv(self.lo * self.lo, 1 << self.P), cdiv(self.hi * self.hi, 1 << self.P), self.P)
        if self.hi <= 0:
            return (-self).sq()
        m = max(-self.lo, self.hi)
        return FI(0, cdiv(m * m, 1 << self.P), self.P)

    def flo(self):
        return Fraction(self.lo, 1 << self.P)

    def fhi(self):
        return Fraction(self.hi, 1 << self.P)


def fi_exp(Y):
    """encloses exp(y) for all y in Y (Y within [-64, 64])."""
    P = Y.P
    assert Y.flo() >= -64 and Y.fhi() <= 64
    s = 16  # |w| = |y| / 2^16 <= 2^-10
    W = FI(Y.lo >> s, cdiv(Y.hi, 1 << s), P)
    wmax = Fraction(cdiv(max(-W.lo, W.hi), 1 << (P - 40)), 1 << 40)  # >= max |w|, small denominator
    term, S, i = FI.frac(1, P), FI.frac(1, P), 0
    bound = Fraction(1)  # |w|^i / i!  (exact upper bound of the next-term magnitude)
    while True:
        i += 1
        term = (term * W) / i
        S = S + term
        bound = bound * wmax / i
        if bound * wmax < Fraction(1, 1 << (P + 4)):
            break
    # remainder of the Taylor series after the term of degree i: <= |w|^(i+1)/(i+1)! * e^|w| <= 2 bound*wmax/(i+1)
    R = 2 * bound * wmax / (i + 1)
    S = S + FI(-cdiv(R.numerator << P, R.denominator), cdiv(R.numerator << P, R.denominator), P)
    assert S.lo > 0
    for _ in range(s):
        S = S.sq()
    return S


_LN2 = {}


def _atanh_series(T):
    """encloses atanh(t) for t in T, with 0 <= T.lo, T.hi < 1/2."""
    P = T.P
    assert T.lo >= 0 and T.fhi() < Fraction(1, 2)
    T2 = T.sq()
    tmax = Fraction(cdiv(T.hi, 1 << (P - 40)), 1 << 40)  # >= max t, small denominator
    assert tmax < Fraction(1, 2)
    power, S, k = T, T, 0  # power = t^(2k+1)
    while True:
        k += 1
        power = power * T2
        S = S + power / (2 * k + 1)
        if tmax ** (2 * k + 3) < Fraction(1, 1 << (P + 4)):
            break
    tail = tmax ** (2 * k + 3) / ((2 * k + 3) * (1 - tmax * tmax))
    return S + FI(0, cdiv(tail.numerator << P, tail.denominator), P)


def ln2(P):
    if P not in _LN2:
        _LN2[P] = 2 * _atanh_series(FI.frac(Fraction(1, 3), P))
    return _LN2[P]


def fi_log(Z):
    """encloses log(z) for all z in Z, Z.lo > 0."""
    P = Z.P
    assert Z.lo > 0
    k = 0  # find k with 1 <= Z.lo * 2^k < 2
    while Z.flo() * Fraction(2) ** k < 1:
        k += 1
    while Z.flo() * Fraction(2) ** k >= 2:
        k -= 1
    M = FI(Z.lo << k, Z.hi << k, P) if k >= 0 else FI(Z.lo >> -k, cdiv(Z.hi, 1 << -k), P)
    T = (M - 1) / (M + 1)
    if T.lo < 0:  # only possible through rounding at m = 1
        T = FI(0, T.hi, P)
        assert M.lo >= (1 << P) - 1
    return 2 * _atanh_series(T) - k * ln2(P)


def fi_power(base, expo):
    assert base.lo > 0
    return fi_exp(expo * fi_log(base))


def sci(q):
    """Fraction > 0 in scientific notation (3 digits, rounded up), without floating point."""
    if q == 0:
        return "0"
    e = len(str(q.numerator)) - len(str(q.denominator))
    while Fraction(10) ** e > q:
        e -= 1
    while Fraction(10) ** (e + 1) <= q:
        e += 1
    m = q / Fraction(10) ** e  # in [1, 10)
    d = -((-m.numerator * 100) // m.denominator)
    return f"{d // 100}.{d % 100:02d}e{e}"


def main():
    t0 = time.time()
    I = osilx.read(OSIL)
    n = len(I["names"])
    assert all(t == "C" for t in I["vt"])
    assert all(osilx.isinf(I["lb"][k]) and osilx.isinf(I["ub"][k]) for k in range(n)), "all variables free"
    # pivot structure (own code)
    order = {}
    for r, c in enumerate(I["cons"]):
        assert not osilx.isinf(c["lb"]) and Fraction(c["lb"]) == Fraction(c["ub"])
        assert c["nl"] is None
        qv = {i for i, j, _ in c["quad"]} | {j for i, j, _ in c["quad"]}
        p = max(set(c["lin"]) | qv)
        assert p not in qv and Fraction(c["lin"][p]) != 0 and p not in order
        order[p] = r
    seeds = [k for k in range(n) if k not in order]
    seedval = {}
    for line in open("points/lukvle10_seed.txt"):
        if not line.startswith("#"):
            nm, v = line.split()
            seedval[nm] = Fraction(v)
    assert sorted(seedval) == sorted(I["names"][k] for k in seeds)
    X = [None] * n
    for k in range(n):
        if k not in order:
            X[k] = FI.frac(seedval[I["names"][k]], P_ROWS)
            continue
        c = I["cons"][order[k]]
        rest = FI.frac(Fraction(c["constant"]), P_ROWS)
        for j, v in c["lin"].items():
            if j != k:
                rest = rest + Fraction(v) * X[j]
        for i, j, v in c["quad"]:
            rest = rest + Fraction(v) * (X[i].sq() if i == j else X[i] * X[j])
        X[k] = (FI.frac(Fraction(c["lb"]), P_ROWS) - rest) / Fraction(c["lin"][k])
    maxw = max(x.fhi() - x.flo() for x in X)
    print(f"rows propagated, max coordinate width {sci(maxw)} ({time.time() - t0:.1f} s)", flush=True)
    # compare with the saved box
    box = {}
    with gzip.open("points/lukvle10_box.txt.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                nm, cen, rad = line.split()
                box[nm] = (Fraction(cen), Fraction(rad))
    inside = all(box[I["names"][k]][0] - box[I["names"][k]][1] <= X[k].flo() and
                 X[k].fhi() <= box[I["names"][k]][0] + box[I["names"][k]][1] for k in range(n))
    print("all coordinate enclosures inside the saved box:", inside, flush=True)

    fns = {"power": fi_power}

    def num(s):
        return FI.frac(Fraction(s), P_OBJ)

    Xo = [x.rescale(P_OBJ) for x in X]
    obj = osilx.ev_row(I["obj"], Xo, num, fns)
    print(f"objective over the coordinate enclosures: width {sci(obj.fhi() - obj.flo())} "
          f"({time.time() - t0:.1f} s)", flush=True)
    Xb = []
    for k in range(n):
        cen, rad = box[I["names"][k]]
        Xb.append(FI(FI.frac(cen - rad, P_OBJ).lo, FI.frac(cen + rad, P_OBJ).hi, P_OBJ))
    objb = osilx.ev_row(I["obj"], Xb, num, fns)
    dual = Fraction("352.2380254050784")

    def dfl(q, k=40):
        return f"{(q.numerator * 10 ** k) // q.denominator}e-{k}"

    def dce(q, k=40):
        return f"{-((-q.numerator * 10 ** k) // q.denominator)}e-{k}"

    rec = dict(P_rows=P_ROWS, P_obj=P_OBJ, seeds=[I["names"][k] for k in seeds],
               max_coordinate_width=sci(maxw), inside_saved_box=inside,
               objective_tight=[dfl(obj.flo()), dce(obj.fhi())],
               objective_box=[dfl(objb.flo()), dce(objb.fhi())],
               objective_tight_width=sci(obj.fhi() - obj.flo()),
               objective_box_width=sci(objb.fhi() - objb.flo()),
               gap_upper_box=dce(objb.fhi() - dual, 25), seconds=round(time.time() - t0, 1))
    print(json.dumps(rec, indent=1))
    json.dump(rec, open("logs/lukvle10_crosscheck.json", "w"), indent=1)


if __name__ == "__main__":
    main()
