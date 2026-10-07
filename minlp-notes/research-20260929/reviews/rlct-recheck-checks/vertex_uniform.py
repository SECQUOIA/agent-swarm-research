"""Lemma 3.3a uniformity in g: m = delta (x + y) + x^2 + y^2 on [0,1]^2, exact alphaBB, alpha = alpha' = 1.
N_v = number of levels j >= 1 at which the corner cell [0,s_j]^2 is processed and not pruned.
Bound of Lemma 3.3a(c): N_v <= 1 + c + sqrt(3M/2 + 1) I_E / log 2, with M = 2, Lambda_0 = 1/2, so c = 0,
and I_E = int_0^1 (delta t + t^2 + eps)^(-1/2) dt (edge y = 0). Also Lemma 3.3a(a): pruned once s_j <= g/(alpha'+M/2)."""
import math
from scipy.integrate import quad
alpha, M = 1.0, 2.0
def phi_min(delta, s):  # min over [0,s] of delta y + y^2 - alpha y (s - y), closed form (convex quadratic)
    a, b = 1 + alpha, delta - alpha*s
    y = min(max(-b/(2*a), 0.0), s)
    return delta*y + y*y - alpha*y*(s - y)
print(" delta     eps     N_v   Lemma3.3a(a) max level   I_E      bound(c)   N_v/I_E")
for delta in (1e-1, 1e-3, 1e-5, 1e-7):
    for eps in (1e-4, 1e-8, 1e-12, 1e-16):
        Nv = 0; j = 1
        while True:
            s = 2.0**-j
            if 2*phi_min(delta, s) < -eps: Nv += 1; j += 1
            else: break
        IE = quad(lambda t: (delta*t + t*t + eps)**-0.5, 0, 1, points=[math.sqrt(eps), delta], limit=400)[0]
        jmax = math.log2(1.0*(alpha + M/2)/delta)   # levels with s_j > g/(alpha'+M/2)
        bound = 1 + math.sqrt(1.5*M + 1)*IE/math.log(2)
        print("%7.0e %7.0e %5d %12.2f %20.4f %10.2f %9.3f" % (delta, eps, Nv, jmax, IE, bound, Nv/IE))
