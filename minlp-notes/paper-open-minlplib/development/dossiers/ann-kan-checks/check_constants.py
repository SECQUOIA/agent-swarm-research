"""Exact rational check of the mpmath-derived constants used by the rigorous exp routines:
 (a) kan_iv.LN2 = [_l2lo, _l2hi] and LN2_64; (b) the 64 table entries [_TLO[j], _THI[j]] of exp(j ln2/64);
 (c) annx's LN2 enclosure (recomputed here exactly as annx does).
ln 2 is bracketed by the alternating-free series ln2 = sum_{k>=1} 1/(k 2^k) with tail bound 1/((n+1)2^n);
exp(q) for rational q in [0, ln2) is bracketed by its Taylor polynomial plus remainder q^(N+1)/(N+1)! * 2."""
import sys
from fractions import Fraction as F
sys.path.insert(0, '.')
import numpy as np
import math
import kan_iv as K

def ln2_bracket(n=200):
    s = sum(F(1, k * 2**k) for k in range(1, n + 1))
    return s, s + F(1, (n + 1) * 2**n)          # tail < sum_{k>n} 1/((n+1) 2^k) = 1/((n+1)2^n)
L2lo, L2hi = ln2_bracket()
print('ln2 bracket width', float(L2hi - L2lo))
lo, hi = F(float(K.LN2.lo)), F(float(K.LN2.hi))
print('(a) kan_iv LN2 encloses ln 2:', lo <= L2lo and L2hi <= hi, float(hi - lo))
lo64, hi64 = F(float(K.LN2_64.lo)), F(float(K.LN2_64.hi))
print('    LN2_64 encloses ln2/64:', lo64 <= L2lo / 64 and L2hi / 64 <= hi64)

def exp_bracket(qlo, qhi, N=40):
    """[lower bound of exp(qlo), upper bound of exp(qhi)] for 0 <= qlo <= qhi < 1."""
    def poly(q):
        t, s = F(1), F(1)
        for k in range(1, N + 1):
            t = t * q / k; s += t
        return s
    rem = qhi**(N + 1) / F(math.factorial(N + 1)) * 3   # e^q <= 3 for q < 1
    return poly(qlo), poly(qhi) + rem

ok = True
for j in range(K._TN):
    elo, ehi = exp_bracket(j * L2lo / 64, j * L2hi / 64)
    tlo, thi = F(float(K._TLO[j])), F(float(K._THI[j]))
    if not (tlo <= elo and ehi <= thi):
        ok = False; print('table entry', j, 'NOT enclosed')
print('(b) all 64 table entries enclose exp(j ln2/64):', ok)

# (c) annx LN2 as constructed in annx.py (60-digit mpmath decimal, then compared exactly)
import mpmath as mp
with mp.workdps(60):
    _l2q = F(mp.nstr(mp.log(2), 58, strip_zeros=False))
_l2f = float(_l2q); _eps = F(1, 10**55)
alo = _l2f if F(_l2f) <= _l2q - _eps else float(np.nextafter(_l2f, -np.inf))
ahi = _l2f if F(_l2f) >= _l2q + _eps else float(np.nextafter(_l2f, np.inf))
print('(c) annx LN2 encloses ln 2:', F(alo) <= L2lo and L2hi <= F(ahi))

# (d) Taylor remainder constants: kan_iv iexp_pt (deg 18, |r|<=0.36, _REM=1e-21), iexp_pt_fast (deg 8, |r|<=0.0055,
# _REM2=1e-25), annx iexp_pt (deg 22, |r|<=0.36, _REM=1e-30).  Bound |r|^(N+1)/(N+1)! * e^|r| with e^|r| <= 3/2.
def rem(N, r):
    return F(r)**(N + 1) / math.factorial(N + 1) * F(3, 2)
print('(d) kan_iv deg 18:', rem(18, F(36, 100)) <= F(1, 10**21), ' kan_iv fast deg 8:', rem(8, F(55, 10000)) <= F(1, 10**25),
      ' annx deg 22:', rem(22, F(36, 100)) <= F(1, 10**30))
