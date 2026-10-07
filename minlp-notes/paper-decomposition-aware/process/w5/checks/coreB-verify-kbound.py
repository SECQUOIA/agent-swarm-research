"""W5 coreB verification: the K(theta,n_P) bound moved to Appendix A and the
algebra of Prop. prop:sharp / Cor. cor:uniformgrid (graded rule)."""
import math, random
from fractions import Fraction as Fr
import sympy as sp

# 1. phi(1), phi(2) (50-digit precision via sympy)
m = sp.symbols('m', positive=True)
phi = sp.Rational(3, 4) + 8*sp.log(sp.Rational(5, 4) + 4*sp.sqrt(2*m))
p1, p2 = sp.N(phi.subs(m, 1), 50), sp.N(phi.subs(m, 2), 50)
assert p1 < sp.Rational(163, 10) <= 10*math.ceil(math.log2(3)), p1
assert p2 < sp.Rational(186, 10) <= 10*2, p2
# 2. phi'(m) <= 4/m for all m>0: m*phi'(m) = 16 sqrt(2m)/(5/4+4 sqrt(2m)) < 4
dphi = sp.simplify(sp.diff(phi, m)*m)
x = sp.symbols('x', positive=True)          # x = sqrt(2m)
assert sp.simplify(dphi.subs(m, x**2/2) - 16*x/(sp.Rational(5, 4)+4*x)) == 0
# 16x/(5/4+4x) < 4  <=>  16x < 5 + 16x : true
# 3. d/dm 10 log2(m+2) = 10/((m+2) ln 2) >= 7.2/m for m >= 2 (increasing in m)
assert 10*2/(4*math.log(2)) >= 7.2
# 4. direct check of 1+2ceil((4/t) ln(5/4+4 sqrt(2m))) <= 10/t ceil(log2(m+2))
random.seed(1)
thetas = [2.0**-mu for mu in range(2, 14)] + [random.uniform(1e-4, 0.25) for _ in range(40)]
bad = 0
for t in thetas:
    for mm in list(range(1, 3000)) + [10**k for k in range(4, 10)]:
        lhs = 1 + 2*math.ceil((4/t)*math.log(1.25 + 4*math.sqrt(2*mm)))
        rhs = 10/t*math.ceil(math.log2(mm + 2))
        bad += lhs > rhs*(1 + 1e-12)
assert bad == 0, bad
# 5. Prop. sharp algebra: completing the square and the bound on Q_1(a,v_a)
L, g, a, v, lam, h, n = sp.symbols('Lambda g a v lambda h n', positive=True)
ts = -(L - 2*g)*a/L
assert sp.simplify(L/2*v**2 + (L-2*g)*a*v - (L/2*(v-ts)**2 - (L-2*g)**2*a**2/(2*L))) == 0
Q1 = (L**2-(L-2*g)**2)/(2*L)*a**2 + L/2*(lam/2)**2 - L/8*lam**2
assert sp.simplify(Q1 - 2*g*(L-g)/L*a**2) == 0
k = sp.symbols('kappa', positive=True)
thr = (n-2)*L**2*h**2/(16*g*(L-g))
assert sp.simplify(thr.subs(L, k*g) - (n-2)*h**2*k**2/(16*(k-1))) == 0
assert sp.simplify(k**2/(k-1) - k - k/(k-1)) == 0      # >= kappa for kappa > 1
# 6. graded rule: t_k = h'((1+theta)^k-1)/theta for unclipped steps h'+theta*t
for th in [Fr(1, 4), Fr(1, 8), Fr(3, 50)]:
    hp, tk = Fr(1, 3), Fr(0)
    for kk in range(1, 30):
        tk = tk + hp + th*tk
        assert tk == hp*((1+th)**kk - 1)/th
print("OK: phi(1)=%.4f phi(2)=%.4f; K bound 0 violations; sharp/graded algebra verified" % (p1, p2))
