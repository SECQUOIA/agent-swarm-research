"""Independent exact checks of the frozen Stage 2 certificates.

This checks finite instances and polynomial identities, not universal claims
by finite sampling. Run with the repository conda Python for SymPy.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sympy as S

out = {}
dyadic = []
for L in range(2, 13):
    m = 2**L
    w = [Q(1, 2**(l+1)) if l < L else Q(1, m) for l in range(L+1)]
    budget = lambda q: Q(L-q+2, 2**q)
    cutoffs = [s for s in range(1,L) if budget(s+1) <= 1 <= budget(s)]
    answers = []
    for s in cutoffs:
        mix = (1-budget(s+1))/(budget(s)-budget(s+1))
        assert 0 <= mix <= 1
        mean_r = 0
        payoff = 0
        for q,p in [(s,mix),(s+1,1-mix)]:
            for l in range(L+1):
                r = 0 if l < q else 2**(l-q+1)
                mean_r += p*w[l]*r
                payoff += p*w[l]*sum(min(2**j,r) for j in range(1,l+1))
        assert mean_r == 1
        assert payoff == s+Q(L-s,2**s)
        for l in range(L+1):
            intercept = 0 if l <= s else 2**(l-s+1)-2
            assert all(sum(min(2**j,r) for j in range(1,l+1)) <= s*r+intercept
                       for r in range(m+1))
        answers.append(payoff)
    assert len(set(answers)) == 1
    assert all(sum(w[j:]) == Q(1,2**j) for j in range(1,L+1))
    # Check every prefix-count at every possible failure count, independently
    # constructing reversed binary labels rather than assuming hit counts.
    rev = [int(f'{v:0{L}b}'[::-1],2) for v in range(m)]
    seen = [set() for _ in range(L)]
    for r,label in enumerate(rev,1):
        for j in range(1,L+1):
            seen[j-1].add(label >> (L-j))
            assert len(seen[j-1]) == min(2**j,r)
    if L <= 6:
        for r in range(m+1):
            hits = [0]*m
            for shift in range(m):
                for leaf in rev[:r]:
                    hits[leaf ^ shift] += 1
            assert hits == [r]*m
    dyadic.append({'L':L,'s':cutoffs,'H':str(answers[0])})
out['dyadic'] = dyadic

# Independent direct count enumeration, retaining tight sets to check primal
# support membership, with all expected values evaluated as exact fractions.
cases = [
 (6,[2,3,9,10,7,7],13,[962,778,842,-4816],
  [((1,4,4),Q(17,26)),((2,1,6),Q(4,13)),((6,2,1),Q(1,26))]),
 (8,[2,3,13,12,8,7],7,[793,770,798,-5882],
  [((1,2,8),Q(2,7)),((1,5,6),Q(4,7)),((8,4,2),Q(1,7))]),
 (64,[2,3,120,105,70,63],105,[871710,900446,899046,-51743768],
  [((4,19,64),Q(241,735)),((5,19,64),Q(12,735)),
   ((16,40,43),Q(419,735)),((64,31,17),Q(63,735))])]
finite = []
for m,co,D,dual,atoms in cases:
    def cost(A,B,C):
        return (co[0]*C*(C-1)*(C-2)//6+co[1]*B*C*(C-1)//2
                +co[2]*B*(B-1)//2+co[3]*A*C+co[4]*A*B+co[5]*A*(A-1)//2)
    tight=[]
    for A,B,C in product(range(m+1), repeat=3):
        residual=D*cost(A,B,C)-dual[0]*A-dual[1]*B-dual[2]*C-dual[3]
        assert residual >= 0
        if residual == 0:
            tight.append((A,B,C))
    assert sum(p for _,p in atoms) == 1
    assert all(state in tight and p >= 0 for state,p in atoms)
    means = [sum(state[j]*p for state,p in atoms) for j in range(3)]
    assert means == [Q(m,4),Q(m,2),Q(3*m,4)]
    vex = sum(cost(*state)*p for state,p in atoms)
    assert vex == (sum(dual[j]*means[j] for j in range(3))+dual[3])/D
    counts=[comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2)]
    cav=sum(c*n*u for c,n,u in zip(co,counts,[Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]))
    termlow=co[0]*Q(comb(m,3),4)
    finite.append({'n':3*m,'supports':sum(counts),'tight':tight,'cav':str(cav),
                   'vex':str(vex),'T/H':str((cav-termlow)/(cav-vex))})
out['finite']=finite

supports={tuple([i,16+j,16+k]) for i in range(16) for j,k in combinations(range(16),2)}
supports.update(tuple([i,j,32+k]) for i,j in combinations(range(16),2) for k in range(20))
assert len(supports)==4320 and all(len(set(e))==3 for e in supports)
assert set().union(*map(set,supports))==set(range(52))
assert all(2*(A*comb(C,2)+20*comb(A,2))-428*A-177*C+3372 >= 0
           for A,C in product(range(17),repeat=2))
assert Q(2160,1)/(2160-1088+Q(12,5))==Q(2700,1343)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
out['unit_supports']=len(supports)

a,b,c,t = S.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2-37*a-S.Rational(79,2)*b-38*c+S.Rational(103,3)
p=S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
sol=S.solve([S.diff(h,a),S.diff(h,b)],[a,b])
r=S.expand(h.subs(sol))
rows=[(p,0,S.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,S.Rational(1,5),S.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,S.Rational(3,10),S.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,S.Rational(1,2),S.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,S.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,lo,hi,D,vs in rows:
    assert S.expand(poly.subs(c,lo+(hi-lo)*t)-sum(S.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vs)))==0
delta=min(Q(v,D) for _,_,_,D,vs in rows for v in vs)
assert delta==Q(901,120000)
assert Q(161,4)/(Q(223,12)-delta)==Q(1610000,743033)
assert S.expand(a*c*c+S.Rational(5,4)*a*a-S.Rational(11,6)*a-S.Rational(20,27)*c+S.Rational(95,108)-S.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert S.expand(a*c*c+S.Rational(24,25)*a*a-S.Rational(41,25)*a-S.Rational(4,5)*c+S.Rational(68,75)-S.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
out['symbolic']='Five Bernstein identities and both two-level identities passed exactly.'
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
