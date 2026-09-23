"""Independent finite exact checks; these do not prove universal positivity."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import comb, factorial
from pathlib import Path
import json
import sympy as sp


def fall(x, k):
    ans = 1
    for i in range(k):
        ans *= x-i
    return ans


counts = {}
s, t = sp.symbols('s t')
counts['symbolic_gram_entries'] = 0
for d in range(1, 9):
    for ell in range(d+1):
        lhs = sum(comb(ell,j)*fall(t,2*d-j)*fall(s-t,j) for j in range(ell+1))
        rhs = fall(t,2*d-ell)*fall(s-2*d+ell,ell)
        assert sp.expand(lhs-rhs) == 0
        counts['symbolic_gram_entries'] += 1

counts['homogenization_products'] = 0
for n, capacity, degree in [(2,F(1),1),(4,F(3,2),1),(6,F(3),2),(7,F(7,2),2),(10,F(5),3)]:
    subsets = [frozenset(c) for a in range(degree+1) for c in combinations(range(n),a)]
    homogeneous = [S for S in subsets if len(S)==degree]
    @lru_cache(None)
    def moment(a):
        return F(fall(capacity,a),fall(n,a))
    for S in subsets:
        denom = F(fall(capacity-len(S),degree-len(S)),factorial(degree-len(S)))
        assert denom > 0
        extensions = [T for T in homogeneous if S <= T]
        for V in subsets:
            rhs = sum(moment(len(T|V)) for T in extensions)/denom
            assert moment(len(S|V)) == rhs
            counts['homogenization_products'] += 1

counts['indicator_expansion_identities'] = 0
counts['nonnegative_allowed_indicator_weights'] = 0
for n in range(2,15):
    for twice_capacity in range(0,2*n+1):
        capacity = F(twice_capacity,2)
        for a in range(n+1):
            for b in range(n-a+1):
                for c in range(n-a-b+1):
                    direct = sum((-1)**j*comb(b,j)*F(fall(capacity,a+c+j),fall(n,a+c+j)) for j in range(b+1))
                    formula = F(fall(capacity,a+c)*fall(n-capacity,b),fall(n,a+b+c))
                    assert direct == formula
                    counts['indicator_expansion_identities'] += 1
                for order in range(1,n//2+1):
                    if capacity >= 2*order-1 and n-capacity >= 2*order-1 and a+b <= 2*order:
                        weight = F(fall(capacity,a)*fall(n-capacity,b),fall(n,a+b))
                        assert weight >= 0
                        if a+b <= 2*order-2:
                            assert weight > 0
                        counts['nonnegative_allowed_indicator_weights'] += 1

counts['avoidance_bounds'] = 0
for n in range(2,31):
    for z in range(n):
        for excluded in range(n+1):
            numerator = comb(n-excluded,z) if z <= n-excluded else 0
            assert F(numerator,comb(n,z)) <= F(n-z,n)**excluded
            counts['avoidance_bounds'] += 1

tau = F(1,4)-F(1,32)*(F(5,2)+F(1,4))-F(1,32)
assert tau == F(17,128)
assert F(2,6)*tau == F(17,384)
counts['relative_example'] = {'tau':str(tau),'exponent_per_original_coordinate':str(F(2,6)*tau)}
result = {'status':'PASS','arithmetic':'exact integer/rational and symbolic polynomial identities','checks':counts,
          'limit':'Finite checks support formulas and boundaries; universal PSD, local-lift and tensor claims were reviewed algebraically.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
