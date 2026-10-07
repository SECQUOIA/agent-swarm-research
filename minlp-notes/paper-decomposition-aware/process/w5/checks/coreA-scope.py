# Exact checks for Remark rem:nonconvex (W5 coreA) on one block of Example ex:family
# phi(u,v,rho)=u^2+v^2-4uv+(u+v)/4+(rho-u/2)^2 on [0,1]^3, x*=(1,1,1/2), g=1/2.
from fractions import Fraction as Fr
from itertools import product

def phi(u, v, r):
    return u*u + v*v - 4*u*v + Fr(1, 4)*(u + v) + (r - u/2)**2

xs = (Fr(1), Fr(1), Fr(1, 2))
opt = phi(*xs)
L = [Fr(5, 2), Fr(2), Fr(2)]          # diagonal Hessian entries (all positive)
Lmax = max(L)
g = Fr(1, 2)
kappa = max(Fr(1), Lmax / g)
gamma = g / Lmax
kbar = max(Fr(1), 1 / gamma)

# point growth with g=1/2 on a rational grid of [0,1]^3
pts = [Fr(k, 12) for k in range(13)]
worst = None
for x in product(pts, repeat=3):
    d2 = sum((a - b)**2 for a, b in zip(x, xs))
    if d2 == 0:
        continue
    r = (phi(*x) - opt) / d2
    worst = r if worst is None or r < worst else worst
    assert phi(*x) - opt >= g * d2, x
print("min ratio on grid", worst, ">= g =", g)

# local inequality: H_{J0J0} = [2] (J0 = {rho}); kappa >= 2L/lambda_min
assert kappa >= 2 * Lmax / 2
# global inequalities at the local minimizer x'=(0,0,0)
xp = (Fr(0), Fr(0), Fr(0))
gap = phi(*xp) - opt
d = [a - b for a, b in zip(xp, xs)]
assert kappa >= Lmax * sum(t*t for t in d) / gap
assert kbar >= sum(Li*t*t for Li, t in zip(L, d)) / gap
assert sum(Li*t*t for Li, t in zip(L, d)) <= Lmax * sum(t*t for t in d)
print("kappa", kappa, ">=", Lmax * sum(t*t for t in d) / gap,
      "; kbar", kbar, ">=", sum(Li*t*t for Li, t in zip(L, d)) / gap)

# L=0 example: F=-(x-1/2)^2+eps*x on [0,1]; nearly tied far minima, kappa=1
eps = Fr(1, 1000)
F = lambda x: -(x - Fr(1, 2))**2 + eps*x
xstar = Fr(0)
gstar = min((F(Fr(k, 1000)) - F(xstar)) / (Fr(k, 1000))**2 for k in range(1, 1001))
print("L=0 example: g* on grid", gstar, "; L=0 so kappa=max(1,0/g)=1")
print("PASS")
