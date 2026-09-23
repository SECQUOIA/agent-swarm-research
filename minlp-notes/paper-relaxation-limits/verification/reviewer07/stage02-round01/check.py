"""Independent exact checks of the frozen Stage 2 certificates; no solver."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import re
import sympy as S

ROOT = Path(__file__).resolve().parents[3]
FROZEN = ROOT / "process/snapshots/stage02-round01"
out = {}

# Independently transcribed rational certificates, evaluated as count polynomials.
cases = [
    (6, [2,3,9,10,7,7], [962,778,842,-4816], 13,
     [(1,4,4),(2,1,6),(6,2,1)], [Q(17,26),Q(4,13),Q(1,26)]),
    (8, [2,3,13,12,8,7], [793,770,798,-5882], 7,
     [(1,2,8),(1,5,6),(8,4,2)], [Q(2,7),Q(4,7),Q(1,7)]),
    (64, [2,3,120,105,70,63], [871710,900446,899046,-51743768],105,
     [(4,19,64),(5,19,64),(16,40,43),(64,31,17)],
     [Q(241,735),Q(12,735),Q(419,735),Q(63,735)])]
finite = []
for m, co, dual, den, atoms, ps in cases:
    def value(a,b,c):
        return (co[0]*c*(c-1)*(c-2)//6 + co[1]*b*c*(c-1)//2
                + co[2]*b*(b-1)//2 + co[3]*a*c + co[4]*a*b
                + co[5]*a*(a-1)//2)
    residuals = [den*value(a,b,c)-dual[0]*a-dual[1]*b-dual[2]*c-dual[3]
                 for a,b,c in product(range(m+1),repeat=3)]
    assert min(residuals) == 0
    assert sum(ps) == 1 and min(ps) >= 0
    mean = [sum(p*atom[j] for atom,p in zip(atoms,ps)) for j in range(3)]
    assert mean == [Q(m,4),Q(m,2),Q(3*m,4)]
    primal = sum(p*value(*atom) for atom,p in zip(atoms,ps))
    assert primal == (sum(dual[j]*mean[j] for j in range(3))+dual[3])/den
    sizes = [comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2)]
    upper = [Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]
    cav = sum(c*n*u for c,n,u in zip(co,sizes,upper))
    lower = co[0]*comb(m,3)*Q(1,4)
    ratio = (cav-lower)/(cav-primal)
    assert ratio > 2
    finite.append(dict(n=3*m, states=len(residuals), cav=str(cav), vex=str(primal), ratio=str(ratio)))
out['finite'] = finite
res = [[2*(a*comb(c,2)+20*comb(a,2))-428*a-177*c+3372 for c in range(17)] for a in range(17)]
assert min(map(min,res)) == 0
assert 8*comb(12,2)+20*comb(8,2) == 1088
out['two_level_minima'] = list(map(min,res))

# Derive quartics from the actual scalar polynomial, then verify printed rows.
a,b,c,t = S.symbols('a b c t')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell = 37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3)
h = F-ell
p = S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
sol = S.solve([S.diff(h,a),S.diff(h,b)],[a,b])
r = S.expand(h.subs(sol))
tex = (FROZEN/'sections/03-cubic-equal-means.tex').read_text()
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',tex)
assert len(rows)==5
all_co = []
for name,lo,hi,den,nums in rows:
    lo,hi,den = S.Rational(lo),S.Rational(hi),int(den)
    co = [S.Rational(int(x),den) for x in nums.split(',')]
    bern = sum(co[i]*comb(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    assert S.expand((p if name=='p' else r).subs(c,lo+(hi-lo)*t)-bern)==0
    all_co += co
assert min(all_co)==S.Rational(901,120000)
assert S.Rational(161,4)/(S.Rational(223,12)-min(all_co)) == S.Rational(1610000,743033)
out['bernstein'] = dict(rows=len(rows), minimum=str(min(all_co)))
for k,aa,bb,cc,center,residue in [
    (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert S.expand(a*c*c+k*a*a-aa*a-bb*c+cc-k*(a-center)**2-residue)==0
out['two_level_symbolic_identities']=2

# Exact dyadic resource profiles and geometry, including cutoff ties.
dyadic=[]
for L in range(2,13):
    m=2**L
    w=[Q(1,2**(l+1)) for l in range(L)]+[Q(1,m)]
    B=lambda q: Q(L-q+2,2**q)
    choices=[s for s in range(1,L) if B(s+1)<=1<=B(s)]
    values=[]
    for s in choices:
        mix=(1-B(s+1))/(B(s)-B(s+1))
        er=eh=Q(0)
        for q,prob in [(s,mix),(s+1,1-mix)]:
            for l in range(L+1):
                R=0 if l<q else 2**(l-q+1)
                er+=prob*w[l]*R
                eh+=prob*w[l]*sum(min(2**j,R) for j in range(1,l+1))
        assert er==1 and eh==s+Q(L-s,2**s)
        for l in range(L+1):
            cap=0 if l<=s else 2**(l-s+1)-2
            assert all(sum(min(2**j,R) for j in range(1,l+1))<=s*R+cap for R in range(m+1))
        values.append(eh)
    assert len(set(values))==1
    if L<=7:
        order=[int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
        for R in range(m+1):
            failed=order[:R]
            for j in range(1,L+1):
                assert len({i>>(L-j) for i in failed})==min(2**j,R)
            # Every leaf receives R failures across the uniform XOR shifts.
            assert all(sum((leaf^shift) in failed for shift in range(m))==R for leaf in range(m))
    dyadic.append(dict(L=L, cutoffs=choices, H=str(values[0])))
out['dyadic']=dyadic

# Finite existence arithmetic and explicit support size.
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
U=range(16); W=range(16,32); Z=range(32,52)
supports={tuple(sorted((i,j,k))) for i in U for j,k in combinations(W,2)}
supports.update(tuple(sorted((i,j,k))) for i in Z for j,k in combinations(U,2))
assert len(supports)==4320 and all(len(set(e))==3 for e in supports)
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
out['finite_sampling'] = dict(candidate_terms=464*1000**3, log_failure_upper=str(25002-Q(1000**3,23200)), normalized_margin=str(Q(3987,4550)))
out['explicit_unit_supports']=len(supports)
print(json.dumps(out,indent=2))
(Path(__file__).parent/'results.json').write_text(json.dumps(out,indent=2)+'\n')
