"""R2-math: symbolic check of identity (6.6)/eq:sdp-identity; and Corollary 6.5 re-split duality on the nested example."""
import sympy as sp
x, y, z, a1, a2, c1, c2, wA, wC, dl = sp.symbols('x y z a1 a2 c1 c2 omegaA omegaC delta')
u = y - a1 - (a2 - a1)*x
v = y - c1 - (c2 - c1)*z
D = u**2 + wA*x*(1-x) + v**2 + wC*z*(1-z)
l = {(0,0): (1-x)*(1-z), (1,0): x*(1-z), (0,1): (1-x)*z, (1,1): x*z}
a = {1: a1, 2: a2}; c = {1: c1, 2: c2}
F = {(i,j): sp.Rational(1,2)*((c[j+1]-a[i+1])**2 - dl**2) for i in (0,1) for j in (0,1)}
rhs = (u+v)**2/2 + sum(F[ij]*l[ij] for ij in l) + (wA - (a2-a1)**2/2)*x*(1-x) + (wC - (c2-c1)**2/2)*z*(1-z)
print("identity residual:", sp.simplify(sp.expand(D - dl**2/2 - rhs)))
# nested example A={0,3}, C={1,2}, y in [0,3]: re-split p(y) = -(1/2)(y-3/2)^2 (from M4) gives pair minima summing to 1/2
t = sp.symbols('t')
p = -sp.Rational(1,2)*(t - sp.Rational(3,2))**2
fA = [ (t-0)**2 - p, (t-3)**2 - p ]
fC = [ (t-1)**2 + p, (t-2)**2 + p ]
def minover(fs):
    vals = []
    for f in fs:
        cands = [sp.Integer(0), sp.Integer(3)] + [r for r in sp.solve(sp.diff(f, t), t) if 0 <= r <= 3]
        vals.append(min(f.subs(t, r) for r in cands))
    return min(vals)
print("re-split pair minima:", minover(fA), minover(fC), "sum:", minover(fA) + minover(fC))
