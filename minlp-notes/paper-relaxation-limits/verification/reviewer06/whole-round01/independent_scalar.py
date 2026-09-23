"""Independent exact verification of the printed cubic scalar certificate."""
import json
from pathlib import Path
import sympy as s

a, b, c, t = s.symbols('a b c t')
R = s.Rational
h = 6*c**3 + 27*b*c**2 + 18*b**2 + 30*a*c + 20*a*b + 9*a**2 - (37*a+R(79,2)*b+38*c-R(103,3))
p = (-972*c**4+576*c**3+1404*c**2-768*c+101)/96
r = (-78732*c**4+212256*c**3-203796*c**2+82032*c-11275)/2976
assert s.expand(h.subs({a:1,b:R(13,24)-3*c**2/4})-p) == 0
stationary = s.solve([s.diff(h,a),s.diff(h,b)], [a,b])
assert s.expand(h.subs(stationary)-r) == 0
rows = [
    (p,0,R(1,5),60000,[63125,39125,20975,9395,4133]),
    (p,R(1,5),R(3,10),240000,[16532,6008,1802,3788,11597]),
    (r,R(3,10),R(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
    (r,R(1,2),R(3,4),190464,[25808,18056,7964,9230,15869]),
    (r,R(3,4),1,190464,[15869,22508,34520,45920,31040])
]
for poly, lo, hi, denominator, numerators in rows:
    bernstein = sum(R(v,denominator)*s.binomial(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(numerators))
    assert s.expand(poly.subs(c,lo+(hi-lo)*t)-bernstein) == 0
minimum = min(R(v,denominator) for _,_,_,denominator,nums in rows for v in nums)
assert minimum == R(901,120000)
result = {'arithmetic':'exact symbolic rational', 'eliminations_verified':2, 'bernstein_rows_verified':5, 'bernstein_coefficients':25, 'minimum':str(minimum)}
Path(__file__).with_name('independent-scalar-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
