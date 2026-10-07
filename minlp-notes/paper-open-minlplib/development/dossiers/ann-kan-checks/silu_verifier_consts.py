"""Exact rational check of the verifier's SiLU constants (ZS_LO, ZS_HI, SMIN_LO from kan_bnb._zstar)."""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/tmp/annkan_dossier"); sys.path.insert(0, "/tmp/annkan_dossier/kanrig")
import rint
import importlib.util
spec = importlib.util.spec_from_file_location("kb", "/tmp/annkan_dossier/kanrig/kan_bnb.py")
# compute the constants exactly as kan_bnb does, without running its main
src = open("/tmp/annkan_dossier/kanrig/kan_bnb.py").read()
start = src.index("def _zstar():"); end = src.index("ZS_LO, ZS_HI, SMIN_LO = _zstar()")
ns = {}
exec(src[start:end], ns)
zl, zr, smin = ns["_zstar"]()
print("verifier constants:", repr(zl), repr(zr), repr(smin))
def g(z):
    lo_e, hi_e = rint.exp_bounds(-z)
    s_lo, s_hi = 1 / (1 + hi_e), 1 / (1 + lo_e)
    v = [1 + z * (1 - s_lo), 1 + z * (1 - s_hi)]
    return min(v), max(v)
ZL, ZR, SM = F(zl), F(zr), F(smin)
print("sign of silu' at ZS_LO (upper end < 0):", g(ZL)[1] < 0, " at ZS_HI (lower end > 0):", g(ZR)[0] > 0)
# mean-value lower bound of min silu on [ZL, ZR]
zm = (ZL + ZR) / 2
lo_e, _ = rint.exp_bounds(-zm)
silu_zm_lo = zm / (1 + lo_e)
gmax = max(abs(g(ZL)[0]), abs(g(ZR)[1]))
lb = silu_zm_lo - gmax * (ZR - ZL) / 2
print("rigorous lower bound of min silu:", float(lb), " SMIN_LO <= it:", SM <= lb)
