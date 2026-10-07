"""Referee checks of RLCT constants and small claims, by routes different from the note's scripts.
1. A_cusp = area{|u^2 - v^3| <= 1}, integrating in u (the note integrates in v).
2. V(t)/t^(5/12) for the cusp on its box, by exact 1D integration in y, tends up to A_cusp.
3. c_V = 2 for x^2 y^2 on [-0.9,1.3]^2: V(t)/(sqrt(t) log(1/t)).
4. xy + x^3 + y^3 on [0,1]^2 (corner of the face): V(t)/(t log(1/t)) -> 1/3, and the edge y = 0 (m = x^3)
   has integral (x^3+eps)^(-1/2) ~ eps^(-1/6).
5. m = (x+y)^2 + (x-y)^4 on [0,1]^2 (a zero at a box corner, m >= 0 on R^2): V(t)/t -> 1/2, so lambda = 1,
   while the Newton distance in the coordinates (u, v) = (x+y, x-y) gives 1/l = 3/4.
6. Convexity thresholds alpha0: -min eigenvalue/2 of the Hessian of m on a fine grid, for xy2 and cusp.
"""
import math

import numpy as np
from scipy.integrate import quad

# 1
f = lambda u: (u * u + 1) ** (1 / 3) - np.cbrt(u * u - 1)
A = 2 * (quad(f, 0, 1, limit=200)[0] + quad(f, 1, np.inf, limit=400)[0])
print(f"1. A_cusp by u-integration = {A:.6f} (note: 7.962229)")

# 2 cusp box [-0.45, 0.65]^2: for fixed y, {x : |x^2 - y^3| <= tau}, tau = sqrt(t)
lo, hi = -0.45, 0.65


def xlen(y, tau):
    c = y ** 3
    a2, b2 = c - tau, c + tau          # x^2 in [a2, b2]
    if b2 < 0:
        return 0.0
    rb = math.sqrt(b2)
    ra = math.sqrt(a2) if a2 > 0 else 0.0
    # x in [ra, rb] or [-rb, -ra], clipped to [lo, hi]
    L = max(0.0, min(rb, hi) - max(ra, lo)) + max(0.0, min(-ra, hi) - max(-rb, lo))
    return L


for t in [1e-6, 1e-10, 1e-14, 1e-18]:
    tau = math.sqrt(t)
    s = tau ** (1 / 3)
    pts = [lo, -s, 0, s, 10 * s, hi]
    V = sum(quad(lambda y: xlen(y, tau), pts[i], pts[i + 1], limit=400)[0] for i in range(len(pts) - 1))
    print(f"2. cusp t={t:.0e}: V/t^(5/12) = {V / t ** (5 / 12):.5f}")

# 3 x^2 y^2 on [-a, b]^2: exact V(t) = 4 tau (1 + log(ab/tau)), tau = sqrt(t) (valid for tau <= a^2)
a, b = 0.9, 1.3


def V_xy(t):
    tau = math.sqrt(t)
    g = lambda x: min(a, tau / abs(x)) + min(b, tau / abs(x))
    # integrate in s = log|x| to resolve the 1/x tail
    pos = quad(lambda s: g(math.exp(s)) * math.exp(s), math.log(tau * 1e-3), math.log(b), limit=400)[0]
    neg = quad(lambda s: g(math.exp(s)) * math.exp(s), math.log(tau * 1e-3), math.log(a), limit=400)[0]
    return pos + neg + 2 * tau * 1e-3 * (a + b)


for t in [1e-6, 1e-12, 1e-24, 1e-48]:
    tau = math.sqrt(t)
    exact = 4 * tau * (1 + math.log(a * b / tau))
    print(f"3. x^2y^2 t={t:.0e}: V/(sqrt(t) log(1/t)) = {V_xy(t) / (tau * math.log(1 / t)):.5f}, "
          f"closed form {exact / (tau * math.log(1 / t)):.5f}  (-> 2)")

# 4 xy + x^3 + y^3 on [0,1]^2: for fixed x, y solves y^3 + x y + x^3 = t (increasing in y); Newton from an upper bound


def ymax(x, t):
    c = t - x ** 3
    if c <= 0:
        return 0.0
    y = min(c / x if x > 0 else np.inf, c ** (1 / 3))
    for _ in range(60):
        y -= (y ** 3 + x * y - c) / (3 * y * y + x)
    return y


for t in [1e-4, 1e-8, 1e-16, 1e-24]:
    x0 = t * 1e-6
    V = quad(lambda s: ymax(math.exp(s), t) * math.exp(s), math.log(x0), math.log(t ** (1 / 3)),
             limit=500, epsrel=1e-10)[0] + x0 * t ** (1 / 3)
    print(f"4. xy+x^3+y^3 t={t:.0e}: V/(t log(1/t)) = {V / (t * math.log(1 / t)):.4f}, "
          f"(V - t log(1/t)/3)/t = {(V - t * math.log(1 / t) / 3) / t:.4f}")
for e in [1e-6, 1e-12, 1e-18]:
    Ie = quad(lambda x: (x ** 3 + e) ** -0.5, 0, 1, points=[e ** (1 / 3)], limit=400)[0]
    print(f"4. edge y=0, m=x^3: eps={e:.0e} I_edge*eps^(1/6) = {Ie * e ** (1 / 6):.4f}")

# 5 (x+y)^2 + (x-y)^4 on [0,1]^2


def V5(t):
    # for fixed x, y in [0,1] with (x+y)^2 + (x-y)^4 <= t: the set of y is an interval (convex in y)
    def ylen(x):
        ys = np.linspace(0, min(1.0, math.sqrt(t)), 4001)
        ok = (x + ys) ** 2 + (x - ys) ** 4 <= t
        return ok.mean() * min(1.0, math.sqrt(t)) if ok.any() else 0.0
    return quad(ylen, 0, math.sqrt(t), limit=200)[0]


for t in [1e-2, 1e-4, 1e-6]:
    print(f"5. (x+y)^2+(x-y)^4 on [0,1]^2 t={t:.0e}: V/t = {V5(t) / t:.4f} (-> 1/2)")

# 6 Hessian thresholds
g = np.linspace(-0.9, 1.3, 1201)
X, Y = np.meshgrid(g, g, indexing="ij")
H11, H22, H12 = 2 * Y ** 2, 2 * X ** 2, 4 * X * Y
emin = (H11 + H22) / 2 - np.sqrt(((H11 - H22) / 2) ** 2 + H12 ** 2)
print(f"6. xy2: -min eig/2 = {-emin.min() / 2:.4f} (note alpha0 1.69)")
g = np.linspace(-0.45, 0.65, 1201)
X, Y = np.meshgrid(g, g, indexing="ij")
G = X ** 2 - Y ** 3
gx, gy = 2 * X, -3 * Y ** 2
H11 = 2 * gx * gx + 2 * G * 2
H22 = 2 * gy * gy + 2 * G * (-6 * Y)
H12 = 2 * gx * gy
emin = (H11 + H22) / 2 - np.sqrt(((H11 - H22) / 2) ** 2 + H12 ** 2)
print(f"6. cusp: -min eig/2 = {-emin.min() / 2:.4f} (note alpha0 2.72)")
