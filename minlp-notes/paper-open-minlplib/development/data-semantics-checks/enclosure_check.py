"""Do the data conversions used by the certificates enclose the exact decimal value?
For every numeric string of the given OSIL files:
  (1) mpmath iv.mpf(s) at the working precisions used by the codes (53, 64 bits; 30, 40, 50,
      60 digits) contains Fraction(s);
  (2) the one-ulp pair [nextafter(fl(s), -inf), nextafter(fl(s), +inf)] (ivnp.const, ivx.const,
      ia.NI.const, rbb.dec_iv) contains Fraction(s);
  (3) iv.mpf(repr(float(s))) (camshape_bound.dec) contains Fraction(s).
Read-only; prints counts of failures (expected 0)."""
import os
import sys
from fractions import Fraction

import mpmath
import numpy as np
from mpmath import iv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_survey import strings  # noqa: E402


def fr_tuple(t):
    s, man, e, bc = t
    if man == 0:
        return Fraction(0)
    q = Fraction(int(man)) * (Fraction(2) ** e if e >= 0 else Fraction(1, 2 ** (-e)))
    return -q if s else q


def ends(v):
    """exact rational end points of an mpmath iv interval (raw tuples, no re-rounding)"""
    a, b = v._mpi_
    return fr_tuple(a), fr_tuple(b)


precs = [("prec", 53), ("prec", 64), ("dps", 30), ("dps", 40), ("dps", 50), ("dps", 60)]
names = sys.argv[1:]
allstr = set()
for n in names:
    allstr |= strings(n)
fail = {p: 0 for p in precs}
fail_ulp = fail_repr = 0
for s in sorted(allstr):
    q = Fraction(s)
    for kind, v in precs:
        setattr(iv, kind, v)
        lo, hi = ends(iv.mpf(s))
        if not (lo <= q <= hi):
            fail[(kind, v)] += 1
    f = float(s)
    lo, hi = Fraction(float(np.nextafter(f, -np.inf))), Fraction(float(np.nextafter(f, np.inf)))
    if not (lo <= q <= hi):
        fail_ulp += 1
    iv.dps = 60
    lo, hi = ends(iv.mpf(repr(f)))
    if not (lo <= q <= hi):
        fail_repr += 1
iv.prec = 53
print(f"{len(names)} OSIL files, {len(allstr)} distinct numeric strings")
for p, c in fail.items():
    print(f"  iv.mpf(s) at {p[0]}={p[1]}: failures {c}")
print(f"  one-ulp pair around fl(s): failures {fail_ulp}")
print(f"  iv.mpf(repr(float(s))) at dps=60: failures {fail_repr}")
