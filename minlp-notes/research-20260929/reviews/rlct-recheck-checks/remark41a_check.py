"""Remark 4.1a example: m = xy + x^3 + y^3 on [0,1]^2 (corner of a 2-face).
V(t) = int_0^{t^(1/3)} y_max(x) dx, y_max the root of y^3 + x y + x^3 - t = 0 (increasing in y).
Also the edge integral eps^(1/6) int_0^1 (x^3+eps)^(-1/2) dx -> Gamma(1/3)Gamma(1/6)/(3 Gamma(1/2))."""
import math
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma
def ymax(x, t):
    c = t - x**3
    if c <= 0: return 0.0
    return brentq(lambda y: y**3 + x*y - c, 0, c**(1/3) + 1e-300, xtol=1e-300, rtol=1e-15, maxiter=500)
for t in (1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    x1 = t**(1/3)
    # x = e^v on [t^2, t^(1/3)] (log scale), plus [0, t^2] where y_max ~ t^(1/3)
    V = quad(lambda v: math.exp(v)*ymax(math.exp(v), t), math.log(t*t), math.log(x1),
             points=[math.log(t)*2/3], limit=400, epsrel=1e-11)[0] + t*t*ymax(0.0, t)
    L = math.log(1/t)
    print("t=%.0e  V/(t log(1/t)) = %.5f   (V - t log(1/t)/3)/t = %.5f" % (t, V/(t*L), (V - t*L/3)/t))
c = gamma(1/3)*gamma(1/6)/(3*gamma(0.5))
for e in (1e-8, 1e-12, 1e-16):
    I = quad(lambda x: (x**3 + e)**-0.5, 0, 1, points=[e**(1/3)], limit=400)[0]
    print("eps=%.0e  eps^(1/6) I_edge = %.5f  (limit %.5f)" % (e, I*e**(1/6), c))
