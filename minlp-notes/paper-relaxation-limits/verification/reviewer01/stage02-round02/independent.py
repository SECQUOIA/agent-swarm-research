"""Independent exact supplementary checks; universal proofs are reviewed in prose."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import json
import sympy as s

out = Path(__file__).parent
checks = {}

# Dyadic dual and explicit resource mixture, including every integer count.
for L in range(2, 10):
    m = 2**L
    w = [Q(1, 2**(l+1)) if l < L else Q(1, m) for l in range(L+1)]
    B = lambda q: Q(L-q+2, 2**q)
    cuts = [q for q in range(1,L) if B(q+1) <= 1 <= B(q)]
    values = []
    for cut in cuts:
        theta = (1-B(cut+1))/(B(cut)-B(cut+1))
        ER = gain = Q(0)
        for q, weight in [(cut,theta),(cut+1,1-theta)]:
            for l, prob in enumerate(w):
                R = 0 if l < q else 2**(l-q+1)
                ER += weight*prob*R
                gain += weight*prob*sum(min(2**j,R) for j in range(1,l+1))
        assert ER == 1
        assert gain == cut + Q(L-cut,2**cut)
        values.append(gain)
        for l in range(L+1):
            F = 0 if l <= cut else 2**(l-cut+1)-2
            assert all(sum(min(2**j,R) for j in range(1,l+1)) <= cut*R+F
                       for R in range(m+1))
    assert len(set(values)) == 1
    assert all(sum(w[j:]) == Q(1,2**j) for j in range(1,L+1))
    order = [int(format(i, f'0{L}b')[::-1],2) for i in range(m)]
    for R in range(m+1):
        assert all(len({v >> (L-j) for v in order[:R]}) == min(2**j,R)
                   for j in range(1,L+1))
    # Transitivity of XOR is checked explicitly at these finite dimensions.
    assert all({v ^ shift for shift in range(m)} == set(range(m)) for v in order)
checks['dyadic_L'] = [2,9]

# Derive eliminated quartics from the actual scalar polynomial.
a,b,c,t = s.symbols('a b c t')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h = F-(37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3))
assert s.hessian(h,(a,b)).det() == 248
p = s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
stationary = s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r = s.expand(h.subs(stationary))
rows = [
 (p,0,Q(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,Q(1,5),Q(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,Q(3,10),Q(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,Q(1,2),Q(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,Q(3,4),1,190464,[15869,22508,34520,45920,31040])]
coeffs = []
for poly,lo,hi,D,nums in rows:
    transformed = s.Poly(poly.subs(c,s.Rational(lo)+s.Rational(hi-lo)*t),t)
    actual = [sum(transformed.nth(j)*s.Rational(comb(i,j),comb(4,j))
                  for j in range(i+1)) for i in range(5)]
    assert actual == [s.Rational(v,D) for v in nums]
    coeffs.extend(actual)
delta = min(coeffs)
assert delta == s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-delta) == s.Rational(1610000,743033)
m = s.symbols('m', positive=True)
finite_num = s.Rational(161,4)-s.Rational(135,4)/m+6/m**2
finite_den = s.Rational(223,12)+s.Rational(135,4)/m+9/m**2
assert (finite_num/finite_den).subs(m,36) == s.Rational(16985,8436)
assert (finite_num/(finite_den-delta)).subs(m,36) == s.Rational(42462500,21081891)
for lam,linear,square,remainder in [
 (s.Rational(5,4),11*a/6+20*c/27-s.Rational(95,108),
  (a-(11-6*c*c)/15)**2,(1-c)*(3*c-2)**2*(3*c+7)/135),
 (s.Rational(24,25),41*a/25+4*c/5-s.Rational(68,75),
  (a-(41-25*c*c)/48)**2,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+lam*a*a-linear-lam*square-remainder) == 0
checks['bernstein_minimum'] = str(delta)

# Integrate the actual orientation and B laws, without their derived formulas.
def orientation_product(x):
    ans = Q(0)
    for bits in product([0,1],repeat=len(x)):
        left = max([1-u if bit else Q(0) for u,bit in zip(x,bits)])
        right = min([Q(1) if bit else u for u,bit in zip(x,bits)])
        ans += max(Q(0),right-left)/2**len(x)
    return ans

def b_product(x):
    ends = sorted({Q(0),Q(1),*(u if u <= Q(1,2) else 2*(1-u) for u in x)})
    ans = Q(0)
    for lo,hi in zip(ends,ends[1:]):
        mid = (lo+hi)/2
        z = Q(1)
        for u in x:
            z *= Q(mid <= u) if u <= Q(1,2) else (Q(1,2) if mid <= 2*(1-u) else 1)
        ans += (hi-lo)*z
    return ans

grid = [Q(j,12) for j in range(13)]
assert all(orientation_product((u,)) == b_product((u,)) == u for u in grid)
tested = 0
for degree in [2,3]:
    for x in combinations_with_replacement(grid,degree):
        upper = min(x)
        lower = max(Q(0),sum(x)-degree+1)
        independent = Q(1)
        for u in x:
            independent *= u
        deficiency = 18*(upper-orientation_product(x))+6*(upper-independent)+7*(upper-b_product(x))
        assert deficiency >= 12*(upper-lower), x
        tested += 1
checks['actual_cubic_quadratic_law_grid_cases'] = tested

# Reconcile adjacent-count envelope with the entire-cube affine formula.
tested = 0
for n in range(2,25):
    for u in grid[1:-1]:
        nu = n*u
        b0 = nu.numerator//nu.denominator
        theta = nu-b0
        for d in range(2,n+1):
            value = (1-theta)*comb(b0,d)+theta*comb(b0+1,d)
            affine = max([Q(0)]+[comb(k,d-1)*nu-(d-1)*comb(k+1,d) for k in range(d-1,n)])
            assert value == affine
            q = value/comb(n,d)
            assert q <= u**d < u
            assert min(u,(d-1)*(1-u))/(u-q) <= 2
            tested += 1
checks['equal_mean_exact_cases'] = tested

checks['finite_sampling_margin'] = str(Q(3131,2275)-Q(1,2))
assert Q(3131,2275)-Q(1,2) > 0
assert 25002-Q(1000**3,23200) < 0
(out/'independent.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
