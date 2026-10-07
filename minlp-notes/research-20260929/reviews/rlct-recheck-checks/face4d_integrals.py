"""Referee's own evaluation of the face4d integrals and the node-count comparison.

I_face(eps) = int_{[-.4,.5]^3} (y^4+z^4+w^4+eps)^(-3/2)       (face x = 0, d = 3)
I_full(eps) = int_{X0} (x(1-x)+y^4+z^4+w^4+eps)^(-2)           (d = n = 4)
Method A: Laplace transform with incomplete gamma functions (1D integral in s).
Method B (check of A): scaled 3D cubature for I_face at two eps values.
Then compares with the referee's own bisection counts in logs/face4d_own.jsonl.
"""
import json, math
import numpy as np
from scipy import integrate, special

G = special.gamma
def g(s):  # int_{-0.4}^{0.5} exp(-s y^4) dy
    s = np.asarray(s, float)
    return 0.25*s**-0.25*G(0.25)*(special.gammainc(0.25, 0.4**4*s) + special.gammainc(0.25, 0.5**4*s))
def h(s):  # int_0^0.9 exp(-s x(1-x)) dx, closed form via Dawson's function
    r = math.sqrt(s)
    return (special.dawsn(r/2) + math.exp(-0.09*s)*special.dawsn(0.4*r))/r
def h_quad(s):  # check of h by direct quadrature, split at the boundary layer
    c = min(0.9, 50.0/s)
    f = lambda x: math.exp(-s*x*(1-x))
    return (integrate.quad(f, 0, c, epsabs=0, epsrel=1e-13)[0] +
            (integrate.quad(f, c, 0.9, epsabs=0, epsrel=1e-13)[0] if c < 0.9 else 0.0))

def laplace(eps, a, Z):
    # (m+eps)^(-a) = Gamma(a)^(-1) int s^(a-1) e^(-s(m+eps)) ds; s = e^u
    f = lambda u: math.exp(a*u - math.exp(u)*eps) * Z(math.exp(u))
    hi = math.log(60/eps)
    val = integrate.quad(f, -40, hi, limit=800, epsabs=0, epsrel=1e-11,
                         points=[math.log(1/eps)])[0]
    return val/G(a)

def I_face(eps): return laplace(eps, 1.5, lambda s: float(g(s))**3)
def I_full(eps): return laplace(eps, 2.0, lambda s: h(s)*float(g(s))**3)

def I_face_cubature(eps):
    e = eps**0.25
    F = lambda w, z, y: (y**4 + z**4 + w**4 + 1.0)**-1.5
    tot = 0.0
    for A in (0.4, 0.5):
        for B in (0.4, 0.5):
            for C in (0.4, 0.5):
                tot += integrate.tplquad(F, 0, A/e, 0, B/e, 0, C/e, epsabs=1e-10, epsrel=1e-9)[0]
    return tot*eps**-0.75

alpha = 1.05
cF = (3*alpha/math.pi**2)**1.5           # Theorem 3.1 constant, d = 3
cX = (4*alpha/math.pi**2)**2             # Theorem 3.1 constant, d = n = 4
lead = 8*G(1.25)**3*G(0.75)/G(1.5)       # Lemma 2.2(i): c_Z Gamma(3/4)/Gamma(3/2), c_Z = 8 Gamma(5/4)^3
print("predicted leading constant of I_face: %.6f" % lead)
print("h closed form vs quadrature:", ["%.2e" % abs(h(s)/h_quad(s)-1) for s in (1e-3, 1, 30, 1e3, 1e6, 1e10)])
leadX = 8*G(1.25)**3*G(0.25)/G(2.0)
print("predicted leading constant of I_full (eps^(-1/4)): %.6f" % leadX)
for eps in (1e-4, 1e-6):
    a, b = I_face(eps), I_face_cubature(eps)
    print("cross-check eps=%g  Laplace %.10g  cubature %.10g  rel diff %.2e" % (eps, a, b, abs(a-b)/b))

runs = [json.loads(l) for l in open("logs/face4d_own.jsonl")]
print("\n eps          leaves     I_face      I_face*eps^.75  I_full     faceLB    fullLB   leaves/faceLB  leaves*eps^.25  leaves*eps^.75")
rows = []
for d in runs:
    eps = d["eps"]; L = d["leaves"]
    If, Ix = I_face(eps), I_full(eps)
    rows.append((eps, L, If, Ix))
    print("%.3e %10d %11.5g %11.6f %11.5g %9.4g %8.4g %10.2f %12.1f %10.2f" %
          (eps, L, If, If*eps**0.75, Ix, cF*If, cX*Ix, L/(cF*If), L*eps**0.25, L*eps**0.75))
rows = np.array(rows)
def slope(x, y): return np.polyfit(np.log(1/x), np.log(y), 1)[0]
def local(col, e_lo, e_hi, grid=None):
    m = (rows[:, 0] >= e_lo*0.999) & (rows[:, 0] <= e_hi*1.001)
    if grid is not None:
        m &= np.isclose((np.log10(rows[:, 0])*grid) % 1, 0) | np.isclose((np.log10(rows[:, 0])*grid) % 1, 1)
    return slope(rows[m, 0], rows[m, col]), int(m.sum())
print()
print("LS slope leaves over [1e-6,1e-3], grid 10^(-k/2): %.4f (n=%d)" % local(1, 1e-6, 1e-3, grid=2))
print("LS slope leaves over [1e-6,1e-3], grid 10^(-k/4): %.4f (n=%d)" % local(1, 1e-6, 1e-3))
print("LS slope leaves over [1e-7,1e-4], grid 10^(-k/4): %.4f (n=%d)" % local(1, 1e-7, 1e-4))
m6 = rows[:, 0] >= 1e-6*0.999
r = rows[m6, 1]/(cF*rows[m6, 2])
print("leaves/faceLB over [1e-6,1e-1]: min %.2f max %.2f ratio %.2f" % (r.min(), r.max(), r.max()/r.min()))
r7 = rows[:, 1]/(cF*rows[:, 2])
print("leaves/faceLB over [1e-7,1e-1]: min %.2f max %.2f ratio %.2f" % (r7.min(), r7.max(), r7.max()/r7.min()))
q = rows[m6, 1]*rows[m6, 0]**0.25
print("leaves*eps^(1/4): %.1f at 1e-1, %.1f at 1e-6, factor %.0f" % (q[0], q[-1], q[-1]/q[0]))
e = rows[:, 0]
for e1, e2 in ((1e-8, 1e-7),):
    pass
# local slopes of the integrals at small eps
for eps in (1e-6, 1e-8, 1e-10, 1e-14, 1e-20):
    k = 1.01
    sf = (math.log(I_face(eps/k)) - math.log(I_face(eps*k)))/(2*math.log(k))
    sx = (math.log(I_full(eps/k)) - math.log(I_full(eps*k)))/(2*math.log(k))
    print("local slope at eps=%g: I_face %.4f, I_full %.4f; I_face*eps^.75/lead = %.5f, I_full*eps^.25/leadX = %.4f" %
          (eps, sf, sx, I_face(eps)*eps**0.75/lead, I_full(eps)*eps**0.25/leadX))
