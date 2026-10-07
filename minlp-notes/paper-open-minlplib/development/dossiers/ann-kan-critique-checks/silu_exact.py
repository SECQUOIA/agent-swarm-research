import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'.')
from fractions import Fraction as F
import kan_iv as K
import rint
print('SILU_MIN_LO', repr(K.SILU_MIN_LO), K._ZS_LO, K._ZS_HI)
def g_bounds(z):
    lo_e, hi_e = rint.exp_bounds(-z)
    slo, shi = 1/(1+hi_e), 1/(1+lo_e)
    v=[1+z*(1-slo), 1+z*(1-shi)]
    return min(v), max(v)
zl, zr = F(K._ZS_LO), F(K._ZS_HI)
print(g_bounds(zl)[1] < 0, g_bounds(zr)[0] > 0)
zm=(zl+zr)/2
lo_e,_=rint.exp_bounds(-zm)
mv = zm/(1+lo_e) - max(abs(g_bounds(zl)[0]), abs(g_bounds(zr)[1]))*(zr-zl)/2
print('mv_lb', float(mv), 'SILU_MIN_LO <= mv_lb:', F(K.SILU_MIN_LO) <= mv, float(mv - F(K.SILU_MIN_LO)))
