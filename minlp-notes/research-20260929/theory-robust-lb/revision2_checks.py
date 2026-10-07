"""Second revision: independent checks of the recheck's numerical points
(reviews/robust-lb-recheck.md).  Run: python3 revision2_checks.py > logs/revision2_checks.log

(1) Exact certificate for gamma_10 = 0 at the reference parameters.  The coefficients of
    q are the recheck's rational ones; root counting and signs are recomputed here with sympy.
(2) Corner-box threshold mu0 for the parameter sets of Section 6.5 and the recheck, by
    continuous multi-start minimization of ln(8/vol)/g(vertex) (the recheck used a grid).
(3) Uniform cap: on [-1,-1/2]^3 every term of both factors is >= its value at the vertex
    (-1/2,-1/2,-1/2), so V >= g(-1/2,-1/2,-1/2) > c/4 > 1/4, hence mu0 < 4 ln 64.
(4) E_4(L) at y1 = 0.30 by a discretized LP (lower bound) and fine-grid evaluation.
"""
import numpy as np
import sympy as sp
from scipy.optimize import linprog, minimize

# ---------------------------------------------------------------- (1)
y = sp.symbols("y")
y1, eta, ev = sp.Rational(19, 50), sp.Rational(1, 20), sp.Rational(1, 50)
a = [sp.Rational(1002795549, 10**9), sp.Rational(209764167, 5 * 10**8),
     sp.Rational(-3338707087, 10**9), sp.Rational(4161904633, 10**9),
     sp.Rational(-796748491, 5 * 10**8)]
q = sum(c * y**(2 * j) for j, c in enumerate(a))
rho = sp.expand(y**2 * q)                         # even, degree 10
Lout = 2 * y1 * y - y1**2                        # L on [y1, 1]
Uout = (1 + ev) * y**2 - (1 - eta) * (y - y1)**2  # U on [y1, 1]
tests = [("q - 1 on [0, y1]", q - 1, 0, y1),
         ("1 + eps_v - q on [0, y1]", 1 + ev - q, 0, y1),
         ("rho - L on [y1, 1]", rho - Lout, y1, 1),
         ("U - rho on [y1, 1]", Uout - rho, y1, 1)]
print("(1) gamma_10 = 0 certificate, rho = y^2 q(y), deg rho =", sp.degree(rho, y))
for name, p, lo, hi in tests:
    P = sp.Poly(sp.expand(p), y)
    nroots = P.count_roots(lo, hi)
    mid = P.eval((lo + hi) / 2)
    print("  %-26s real roots in closed interval: %d; value at midpoint %.3e" % (name, nroots, float(mid)))
print("  => L <= rho <= U on [-1,1] (evenness), so LB_b10(root) >= 0; with L(0) = U(0), gamma_10 = 0.")


# ---------------------------------------------------------------- (2), (3)
def gadget(y1, eta, ev):
    b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + ev
    z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1

    def u(z):
        z = abs(z)
        return bp**2 * z**2 / (4 * eta) if z <= z1 else (bp * z + k)**2 / 4 - (1 - eta) * y1**2

    def g(x, yy, z):
        return y1**2 * x**2 + b * x * yy + c * yy**2 + u(z) + bp * yy * z
    A = 1 + ev - (1 - eta) * (1 - y1)**2
    return g, y1**2 * (1 - A) / A, c


def mu0_corner(y1, eta, ev, seed=0):
    """min over boxes [-1,-a]x[-1,-b]x[-1,-c] of ln(8/vol)/g(-a,-b,-c)."""
    g, gam, _ = gadget(y1, eta, ev)

    def obj(v):
        a_, b_, c_ = np.clip(v, 0, 0.999)
        return np.log(8 / ((1 - a_) * (1 - b_) * (1 - c_))) / g(-a_, -b_, -c_)
    rng = np.random.default_rng(seed)
    best = None
    for s in list(rng.uniform(0, 0.95, (40, 3))) + [np.array([0.5, 0.87, 0.81])]:
        r = minimize(obj, s, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-10, "maxiter": 4000})
        if best is None or r.fun < best.fun:
            best = r
    return best.fun, np.clip(best.x, 0, 0.999), gam


print("\n(2) corner-box threshold mu0 (class-(a) gap gamma; cap = exp(mu0 gamma) per gadget)")
for p in [(0.38, 0.05, 0.02), (0.38, 0.01, 0.005), (0.38, 0.05, 0.1), (0.38, 0.05, 0.2),
          (0.30, 0.01, 0.005), (0.45, 0.01, 0.005), (0.30, 0.005, 0.002), (0.50, 0.005, 0.002)]:
    m0, box, gam = mu0_corner(*p)
    print("  %-20s gamma_a = %.5f  mu0 = %.4f  box upper corner = -(%.3f, %.3f, %.3f)  cap %.4f per gadget, %.4f per variable"
          % (p, gam, m0, *box, np.exp(m0 * gam), np.exp(m0 * gam / 3)))

print("\n(3) uniform cap: V([-1,-1/2]^3) >= g(-1/2,-1/2,-1/2) > c/4 > 1/4")
rng = np.random.default_rng(1)
worst = np.inf
for _ in range(20000):
    y1r, etar = rng.uniform(0.01, 0.99, 2)
    evr = rng.uniform(1e-6, 1) * (1 - etar) * (1 - y1r)**2
    g, _, c = gadget(y1r, etar, evr)
    worst = min(worst, g(-0.5, -0.5, -0.5) - c / 4)
print("  min over 20000 random admissible parameters of g(-1/2,-1/2,-1/2) - c/4 = %.3e (> 0)" % worst)
print("  (1/64) exp(mu/4) >= 1 once mu >= 4 ln 64 = %.4f; 8 ln 64 = %.4f" % (4 * np.log(64), 8 * np.log(64)))


# ---------------------------------------------------------------- (4)
def E_even(y1, d, n=4001):
    t = np.linspace(0, 1, n)
    L = np.where(t <= y1, t**2, 2 * y1 * t - y1**2)
    M = np.stack([t**(2 * j) for j in range(d // 2 + 1)], axis=1)
    m = M.shape[1]
    # variables (coeffs, s); minimize s subject to |L - M a| <= s
    A_ub = np.block([[M, -np.ones((n, 1))], [-M, -np.ones((n, 1))]])
    b_ub = np.concatenate([L, -L])
    r = linprog(np.r_[np.zeros(m), 1.0], A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)] * m + [(0, None)], method="highs")
    tf = np.linspace(0, 1, 200001)
    Lf = np.where(tf <= y1, tf**2, 2 * y1 * tf - y1**2)
    err = np.max(np.abs(Lf - np.stack([tf**(2 * j) for j in range(m)], axis=1) @ r.x[:m]))
    return r.x[-1], err


print("\n(4) E_d(L), even best approximation (grid-LP lower bound, fine-grid error of the LP polynomial)")
for y1v, d in [(0.38, 4), (0.30, 4)]:
    lo, hi = E_even(y1v, d)
    print("  y1 = %.2f, d = %d: E_d in [%.6f, %.6f]" % (y1v, d, lo, hi))
lo, hi = E_even(0.30, 4)
print("  y1 = 0.30, d = 4, mu = 2.4: exp(2.4 * 2 E_4 / 3) = %.4f per variable; with gamma_4 = 0.0247 and mu0 = 2.378: %.4f"
      % (np.exp(2.4 * 2 * hi / 3), np.exp(2.378 * 0.0247 / 3)))
