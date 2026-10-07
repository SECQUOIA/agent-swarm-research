"""Exact checks of the growth-scope statements in the abstract and intro (W5 front).

Claims checked on Example ex:family (one block, no coupling) and on a
one-dimensional instance with L = 0:
 (1) point growth g at x* gives H_{J0J0} >= 2 g I, hence lambda_min >= 2L/kappa;
 (2) every x' with F(x') > OPT gives kappa >= L |x'-x*|^2 / (F(x') - OPT);
 (3) with L = 0, nearly tied distant minima do not force kappa > 1.
"""
from fractions import Fraction as Fr

# Example ex:family block: phi(u,v,rho) = u^2+v^2-4uv+(u+v)/4+(rho-u/2)^2 on [0,1]^3.
def phi(u, v, r):
    return u*u + v*v - 4*u*v + Fr(1, 4)*(u + v) + (r - u/2)**2
xs = (Fr(1), Fr(1), Fr(1, 2))
OPT = phi(*xs)
g = Fr(1, 2)                      # growth constant of Example ex:family(a)
L = Fr(21, 8)                     # curvature bound of Example ex:family(b)
kappa = max(Fr(1), L / g)
assert kappa == Fr(21, 4)
# J0 = {rho} (u = v = 1 are at bounds): H_{rho,rho} = 2 >= 2g and >= 2L/kappa.
H_rr = Fr(2)
assert H_rr >= 2*g and H_rr >= 2*L/kappa
# grid check of growth phi - OPT >= g |x - x*|^2 on a rational grid
N = 20
for i in range(N+1):
    for j in range(N+1):
        for k in range(N+1):
            x = (Fr(i, N), Fr(j, N), Fr(k, N))
            d2 = sum((a-b)**2 for a, b in zip(x, xs))
            assert phi(*x) - OPT >= g*d2, x
# (2) at the other strict local minimizer (0,0,0)
xp = (Fr(0), Fr(0), Fr(0))
gap = phi(*xp) - OPT
d2 = sum((a-b)**2 for a, b in zip(xp, xs))
ratio = L*d2/gap
assert kappa >= ratio
print("ex:family block: OPT =", OPT, " gap at (0,0,0) =", gap, " L|x'-x*|^2/gap =", ratio, "<= kappa =", kappa)

# (3) F(x) = -(x-1/2)^2 + eps*x on [0,1]: L = max(H,0) = 0, minima at 0 and 1 tied within eps.
eps = Fr(1, 1000)
F = lambda x: -(x - Fr(1, 2))**2 + eps*x
assert F(Fr(0)) < F(Fr(1)) and F(Fr(1)) - F(Fr(0)) == eps
gmax = min((F(Fr(i, 1000)) - F(Fr(0))) / Fr(i, 1000)**2 for i in range(1, 1001))
print("L = 0 example: tie gap =", eps, " largest growth constant on grid =", gmax, " kappa = max(1, 0/g) = 1")
print("all scope checks passed")
