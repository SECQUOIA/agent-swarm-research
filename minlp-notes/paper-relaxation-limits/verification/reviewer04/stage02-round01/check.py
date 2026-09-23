"""Independent exact checks of frozen Stage 2 data and the actual O/B laws.
Finite checks supplement the general arguments documented in the review.
"""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
from pathlib import Path
import json, re
import sympy as s

out={}
# Integrate product success under actual endpoint orientations, without
# using the manuscript's closed form for deficiency.
def O(x):
    ans=Q(0)
    for signs in product((0,1),repeat=len(x)):
        lo=max([Q(0)]+[1-p for p,b in zip(x,signs) if b])
        hi=min([Q(1)]+[p for p,b in zip(x,signs) if not b])
        ans+=max(Q(0),hi-lo)/2**len(x)
    return ans

def B(x):
    cuts=sorted({Q(0),Q(1)}|{p if p<=Q(1,2) else 2*(1-p) for p in x})
    ans=Q(0)
    for lo,hi in zip(cuts,cuts[1:]):
        t=(lo+hi)/2
        val=Q(1)
        for p in x:
            val*=Q(t<=p) if p<=Q(1,2) else (Q(1,2) if t<=2*(1-p) else Q(1))
        ans+=(hi-lo)*val
    return ans

num=0
for degree in (1,2,3):
    for x in combinations_with_replacement([Q(i,20) for i in range(21)],degree):
        u=min(x)
        t=u-max(Q(0),sum(x)-degree+1)
        pr=s.prod(x)
        oo,bb=O(x),B(x)
        if degree==1:
            assert oo==bb==u
        else:
            assert 18*(u-oo)+6*(u-pr)+7*(u-bb)>=12*t
            num+=1
out['exact_actual_law_tuples']=num

# Dyadic resource certificates and all actual prefix counts through L=8.
for L in range(2,101):
    m=2**L
    def budget(q):return Q(L-q+2,2**q)
    ss=[i for i in range(1,L) if budget(i+1)<=1<=budget(i)]
    values=set()
    for k in ss:
        theta=(1-budget(k+1))/(budget(k)-budget(k+1))
        er=eg=Q(0)
        for l in range(L+1):
            weight=Q(1,2**(l+1)) if l<L else Q(1,2**L)
            for q,alpha in ((k,theta),(k+1,1-theta)):
                r=0 if l<q else 2**(l-q+1)
                utility=sum(min(2**j,r) for j in range(1,l+1))
                affine=k*r+(0 if l<=k else 2**(l-k+1)-2)
                assert utility==affine and 0<=r<=m
                er+=weight*alpha*r
                eg+=weight*alpha*utility
        assert er==1 and eg==k+Q(L-k,2**k)
        values.add(eg)
    assert len(values)==1
    if L<=8:
        order=[int(format(r,'0%db'%L)[::-1],2) for r in range(m)]
        for r in range(m+1):
            for j in range(1,L+1):
                assert len({v>>(L-j) for v in order[:r]})==min(r,2**j)
out['dyadic_exact_resource_L']='2..100; actual prefix geometry 2..8'

# Independently compute every finite affine residual and exact primal mean.
cases=[(6,(2,3,9,10,7,7),13,(962,778,842,-4816),[(1,4,4),(2,1,6),(6,2,1)],[Q(17,26),Q(4,13),Q(1,26)]),(8,(2,3,13,12,8,7),7,(793,770,798,-5882),[(1,2,8),(1,5,6),(8,4,2)],[Q(2,7),Q(4,7),Q(1,7)]),(64,(2,3,120,105,70,63),105,(871710,900446,899046,-51743768),[(4,19,64),(5,19,64),(16,40,43),(64,31,17)],[Q(241,735),Q(12,735),Q(419,735),Q(63,735)])]
for m,c,D,dual,atoms,weights in cases:
    def f(v):
        a,b,w=v
        return sum(z*coef for z,coef in zip((comb(w,3),b*comb(w,2),comb(b,2),a*w,a*b,comb(a,2)),c))
    tight=[]
    for v in product(range(m+1),repeat=3):
        residual=D*f(v)-sum(a*b for a,b in zip((*v,1),dual))
        assert residual>=0
        if residual==0:tight.append(v)
    means=[sum(w*v[i] for v,w in zip(atoms,weights)) for i in range(3)]
    assert sum(weights)==1 and means==[Q(m,4),Q(m,2),Q(3*m,4)]
    assert all(v in tight for v in atoms)
    lower=sum(w*f(v) for v,w in zip(atoms,weights))
    sizes=(comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2))
    upper=sum(Q(a)*b*c for a,b,c in zip(c,sizes,[Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]))
    termlow=Q(c[0]*comb(m,3),4)
    out[f'finite_{3*m}']={'tight':tight,'vex':str(lower),'cav':str(upper),'T/H':str((upper-termlow)/(upper-lower))}
res=[min(2*(a*comb(c,2)+20*comb(a,2))-428*a-177*c+3372 for c in range(17)) for a in range(17)]
assert res==[540,352,204,96,28,0,9,7,0,0,19,63,132,235,369,540,742]
out['two_level_16_residual_minima']=res

# Expand all five Bernstein rows from the actual frozen source.
root=Path(__file__).resolve().parents[3]
tex=(root/'process/snapshots/stage02-round01/sections/03-cubic-equal-means.tex').read_text()
a,b,c,t=s.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b*b+30*a*c+20*a*b+9*a*a-37*a-s.Rational(79,2)*b-38*c+s.Rational(103,3)
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',tex)
assert len(rows)==5
slacks=[]
for which,lo,hi,den,nums in rows:
    lo,hi=s.Rational(lo),s.Rational(hi)
    coeff=[s.Rational(v,int(den)) for v in nums.split(',')]
    bern=sum(v*s.binomial(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(coeff))
    assert s.expand((p if which=='p' else r).subs(c,lo+(hi-lo)*t)-bern)==0
    slacks+=coeff
assert min(slacks)==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-min(slacks))==s.Rational(1610000,743033)
assert s.expand(a*c*c+s.Rational(5,4)*a*a-s.Rational(11,6)*a-s.Rational(20,27)*c+s.Rational(95,108)-s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+s.Rational(24,25)*a*a-s.Rational(41,25)*a-s.Rational(4,5)*c+s.Rational(68,75)-s.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
out['scalar_identities']='five frozen Bernstein rows, both eliminations, both two-level identities: exact'
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)
assert 25*1000+2-Q(1000**3,23200)<0
out['sampling_margin']='3987/4550; exact logarithm upper bound negative'
print(json.dumps(out,indent=2))
