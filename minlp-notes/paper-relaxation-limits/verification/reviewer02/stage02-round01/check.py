"""Independent exact checks of the frozen Stage 2 certificates.

Run with the repository's minlp-notes Python environment (requires SymPy).
Finite enumerations certify only the stated finite instances; symbolic
identities support the continuous arguments assessed in the review report.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json
import re
import sympy as s

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2]
FROZEN = PAPER / "process/snapshots/stage02-round01/sections"
results = {}

# Independently transcribed manuscript tables, with exact integer enumeration.
cases = [
    (6, (2,3,9,10,7,7), (13,962,778,842,-4816),
     [((1,4,4),Q(17,26)),((2,1,6),Q(4,13)),((6,2,1),Q(1,26))]),
    (8, (2,3,13,12,8,7), (7,793,770,798,-5882),
     [((1,2,8),Q(2,7)),((1,5,6),Q(4,7)),((8,4,2),Q(1,7))]),
    (64, (2,3,120,105,70,63), (105,871710,900446,899046,-51743768),
     [((4,19,64),Q(241,735)),((5,19,64),Q(12,735)),
      ((16,40,43),Q(419,735)),((64,31,17),Q(63,735))]),
]
finite = []
for m, coeff, dual, atoms in cases:
    D,da,db,dc,d0 = dual
    def value(a,b,c):
        c1,c2,c3,c4,c5,c6 = coeff
        return (c1*c*(c-1)*(c-2)//6 + c2*b*c*(c-1)//2
                + c3*b*(b-1)//2 + c4*a*c + c5*a*b + c6*a*(a-1)//2)
    minima = []
    zeros = []
    for c in range(m+1):
        residuals = []
        for a,b in product(range(m+1), repeat=2):
            residual = D*value(a,b,c)-da*a-db*b-dc*c-d0
            assert residual >= 0
            residuals.append(residual)
            if residual == 0:
                zeros.append((a,b,c))
        minima.append(min(residuals))
    assert {state for state,p in atoms} <= set(zeros)
    assert all(p >= 0 for state,p in atoms)
    assert sum(p for state,p in atoms) == 1
    means = [sum(p*state[j] for state,p in atoms) for j in range(3)]
    assert means == [Q(m,4),Q(m,2),Q(3*m,4)]
    primal = sum(p*value(*state) for state,p in atoms)
    assert primal == (da*means[0]+db*means[1]+dc*means[2]+d0)/D
    sizes = [comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2)]
    upper = sum(c*n*u for c,n,u in zip(coeff,sizes,[Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]))
    lower = Q(coeff[0]*comb(m,3),4)
    finite.append(dict(n=3*m,states=(m+1)**3,monomials=sum(sizes),
                       cav=str(upper),vex=str(primal),term_lower=str(lower),
                       hull=str(upper-primal),ratio=str((upper-lower)/(upper-primal)),
                       residual_min_by_c=minima))
assert finite[0]['ratio'] == '20891/10411'
assert finite[1]['ratio'] == '6601/3225'
assert finite[2]['ratio'] == '7443345/3445256'
assert finite[0]['monomials'] == 212 and finite[1]['monomials'] == 464
results['finite_three_groups'] = finite

mins = [min(a*c*(c-1)+20*a*(a-1)-428*a-177*c+3372
            for c in range(17)) for a in range(17)]
assert mins == [540,352,204,96,28,0,9,7,0,0,19,63,132,235,369,540,742]
assert 8*comb(12,2)+20*comb(8,2) == 1088
results['two_group_residual_minima'] = mins

a,b,c,t,m = s.symbols('a b c t m')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell = 37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h = F-ell
assert s.hessian(h,(a,b)).det() == 248
bstar = s.solve(s.diff(h,b).subs(a,1),b)[0]
assert s.expand(bstar-(s.Rational(13,24)-3*c**2/4)) == 0
p = s.expand(h.subs({a:1,b:bstar}))
stationary = s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r = s.expand(h.subs(stationary))
assert s.diff(h,a).subs({a:1,b:bstar,c:s.Rational(3,10)}, simultaneous=True).subs(c,s.Rational(3,10)) == -s.Rational(31,60)
text = (FROZEN/'03-cubic-equal-means.tex').read_text()
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$', text)
assert len(rows) == 5
all_coeff = []
for name,lo,hi,den,nums in rows:
    lo,hi,den = s.Rational(lo),s.Rational(hi),int(den)
    nums = [int(v) for v in nums.split(',')]
    transform = s.Poly((p if name=='p' else r).subs(c,lo+(hi-lo)*t),t)
    # Convert ordinary powers to Bernstein coefficients independently.
    derived = [sum(transform.nth(j)*s.Rational(comb(i,j),comb(4,j))
                   for j in range(i+1)) for i in range(5)]
    assert derived == [s.Rational(v,den) for v in nums]
    all_coeff.extend(derived)
delta = min(all_coeff)
assert delta == s.Rational(901,120000)
results['bernstein_minimum'] = str(delta)
results['strongest_lower'] = str((s.Rational(161,4))/(s.Rational(223,12)-delta))
assert results['strongest_lower'] == '1610000/743033'

phi = (2*(m*c)*(m*c-1)*(m*c-2)/6 + 3*m*b*(m*c)*(m*c-1)/2
       +2*m*(m*b)*(m*b-1)/2+s.Rational(5,3)*m**3*a*c
       +s.Rational(10,9)*m**3*a*b+m*(m*a)*(m*a-1)/2)
assert s.expand(18*phi/m**3-F+(18*c*c+27*b*c+18*b+9*a)/m-12*c/m**2) == 0
for gamma,linear,square,residue,atoms in [
    (s.Rational(5,4),11*a/6+20*c/27-s.Rational(95,108),
     (11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135,
     [(s.Rational(1,4),s.Rational(1,3),1),(s.Rational(3,4),s.Rational(5,9),s.Rational(2,3))]),
    (s.Rational(24,25),41*a/25+4*c/5-s.Rational(68,75),
     (41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480,
     [(s.Rational(1,2),s.Rational(1,3),1),(s.Rational(1,2),s.Rational(2,3),s.Rational(3,5))]),
]:
    F2 = a*c*c+gamma*a*a
    assert s.expand(F2-linear-gamma*(a-square)**2-residue) == 0
    assert sum(w*x for w,x,y in atoms) == s.Rational(1,2)
    assert all(s.simplify((F2-linear).subs({a:x,c:y}))==0 for w,x,y in atoms)
results['two_level_identities'] = 'Both exact identities and equality atoms passed'
assert Q(3225,7)+Q(1840,1000)==Q(80947,175)
assert Q(943)/Q(80947,175)==Q(165025,80947)
assert Q(2160)/(1072+Q(120*20,1000))==Q(2700,1343)
assert 36*comb(16,2)==4320
assert Q(2)*Q(1,10)**2/464==Q(1,23200)
assert Q(1000**3,23200)>25002
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)>0
results['padding_sampling_constants'] = 'All exact identities and strict margins passed'

dyadic=[]
for L in range(2,65):
    w=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q:Q(L-q+2,2**q)
    cutoffs=[k for k in range(1,L) if B(k+1)<=1<=B(k)]
    values=set()
    for k in cutoffs:
        mix=(1-B(k+1))/(B(k)-B(k+1))
        atoms=[(w[l]*weight,l,0 if l<q else 2**(l-q+1))
               for q,weight in [(k,mix),(k+1,1-mix)] for l in range(L+1)]
        assert sum(prob*R for prob,l,R in atoms)==1
        attained=sum(prob*sum(min(2**j,R) for j in range(1,l+1))
                     for prob,l,R in atoms)
        certified=k+sum(w[l]*(0 if l<=k else 2**(l-k+1)-2) for l in range(L+1))
        assert attained==certified==k+Q(L-k,2**k)
        values.add(attained)
        for l in range(L+1):
            # Check every piecewise-linear breakpoint, plus zero and final cap.
            for R in [0]+[2**j for j in range(1,l+1)]+[2**L]:
                assert sum(min(2**j,R) for j in range(1,l+1))<=k*R+(0 if l<=k else 2**(l-k+1)-2)
    assert len(values)==1
    dyadic.append(dict(L=L,cutoffs=cutoffs,H=str(next(iter(values)))))
results['dyadic_exact_L2_to_64']=dyadic
for L in range(2,9):
    ordering=[int(f'{v:0{L}b}'[::-1],2) for v in range(2**L)]
    for R in range(2**L+1):
        for j in range(1,L+1):
            assert len({v>>(L-j) for v in ordering[:R]})==min(2**j,R)
results['bit_reversal_finite_checks'] = 'Every R and level for L=2,...,8 passed'

(HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('Independent exact checks passed; results.json contains the certificate values.')
