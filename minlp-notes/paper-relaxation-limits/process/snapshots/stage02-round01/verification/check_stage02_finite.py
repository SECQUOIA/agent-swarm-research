from fractions import Fraction as Q
from itertools import product
from math import comb

# m, coefficients, denominator, integer affine coefficients,
# probability denominator, (state, probability numerator), ratio
cases = [
 (6, (2,3,9,10,7,7), 13, (962,778,842,-4816), 26,
  [((1,4,4),17), ((2,1,6),8), ((6,2,1),1)],
  Q(20891,10411)),
 (8, (2,3,13,12,8,7), 7, (793,770,798,-5882), 7,
  [((1,2,8),2), ((1,5,6),4), ((8,4,2),1)],
  Q(6601,3225)),
 (64, (2,3,120,105,70,63), 105,
  (871710,900446,899046,-51743768), 735,
  [((4,19,64),241), ((5,19,64),12),
   ((16,40,43),419), ((64,31,17),63)],
  Q(7443345,3445256))]

def phi(a, b, c, coef):
    values = (comb(c,3), b*comb(c,2), comb(b,2),
              a*c, a*b, comb(a,2))
    return sum(v*w for v,w in zip(values,coef))

for m,coef,D,dual,P,atoms,ratio in cases:
    for a,b,c in product(range(m+1), repeat=3):
        rhs = sum(v*w for v,w in zip((a,b,c,1),dual))
        assert D*phi(a,b,c,coef) >= rhs
    assert all(p >= 0 for _,p in atoms)
    assert sum(p for _,p in atoms) == P
    means = [sum(Q(p,P)*state[j] for state,p in atoms)
             for j in range(3)]
    assert means == [Q(m,4), Q(m,2), Q(3*m,4)]
    primal = sum(Q(p,P)*phi(*state,coef) for state,p in atoms)
    lower = sum(Q(v,D)*w for v,w in zip(dual,means+[1]))
    assert primal == lower
    sizes = (comb(m,3), m*comb(m,2), comb(m,2),
             m*m, m*m, comb(m,2))
    upper = (Q(3,4), Q(1,2), Q(1,2), Q(1,4), Q(1,4), Q(1,4))
    cav = sum(c*s*u for c,s,u in zip(coef,sizes,upper))
    term_lower = Q(coef[0]*comb(m,3),4)
    assert cav > primal
    assert (cav-term_lower)/(cav-primal) == ratio
    assert ratio > 2
    print(3*m, cav, term_lower, primal, ratio)

mins = []
for a in range(17):
    residuals = [2*(a*comb(c,2)+20*comb(a,2))
                 -428*a-177*c+3372 for c in range(17)]
    mins.append(min(residuals))
assert mins == [540,352,204,96,28,0,9,7,0,0,19,63,
                132,235,369,540,742]
assert 8*comb(12,2)+20*comb(8,2) == 1088
assert 214*8+Q(177,2)*12-1686 == 1088
assert Q(2160,2160-1088) == Q(135,67)
print("All finite cubic certificates passed.")
