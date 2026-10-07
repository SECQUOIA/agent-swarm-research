"""Second, independent evaluation of I_full(eps) = int_{X0} (x(1-x) + S + eps)^(-2), S = y^4+z^4+w^4.
Route: I_full = int_0^0.9 J(x(1-x) + eps) dx with J(c) = int_{[-.4,.5]^3} (S + c)^(-2)
= int_0^inf s e^(-s c) g(s)^3 ds (no h(s) needed). Compared with face4d_integrals.I_full."""
import math
from scipy import integrate
import face4d_integrals as F

def J(c):
    f = lambda u: math.exp(2*u - math.exp(u)*c) * float(F.g(math.exp(u)))**3
    return integrate.quad(f, -40, math.log(60/c), limit=800, epsabs=0, epsrel=1e-11,
                          points=[math.log(1/c)])[0]

def I_full_x(eps):
    f = lambda v: math.exp(v) * J(math.exp(v)*(1 - math.exp(v)) + eps)  # x = e^v
    lo = math.log(eps) - 30
    a = integrate.quad(f, lo, math.log(0.5), limit=400, epsabs=0, epsrel=1e-9,
                       points=[math.log(eps)])[0]
    b = integrate.quad(lambda x: J(x*(1-x) + eps), 0.5, 0.9, epsabs=0, epsrel=1e-10)[0]
    return a + b + math.exp(lo)*J(eps)   # [0, e^lo] piece, J ~ const there

for eps in (1e-2, 1e-4, 1e-6, 1e-8):
    a, b = F.I_full(eps), I_full_x(eps)
    print("eps=%g  Laplace-in-all-variables %.8g   x-outer route %.8g   rel diff %.1e" % (eps, a, b, abs(a-b)/b))
