from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
import json, hashlib, subprocess
import sympy as s
import numpy as np
from scipy.optimize import linprog
from scipy.integrate import quad
from scipy.optimize import brentq

out = {}
a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
solution=s.solve([s.diff(h,a),s.diff(h,b)],[a,b])
r=s.expand(h.subs(solution))
rows=[(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for f,l,u,D,vs in rows:
    bern=sum(s.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vs))
    assert s.expand(f.subs(c,l+(u-l)*t)-bern)==0
assert min(Q(v,D) for _,_,_,D,vs in rows for v in vs)==Q(901,120000)
assert s.expand(a*c*c+5*a*a/4-(11*a/6+20*c/27-s.Rational(95,108))
    -s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
out['symbolic']='All five quartic Bernstein identities and two-level square identity exact.'

cases=[(6,[2,3,9,10,7,7],13,[962,778,842,-4816],26,[(1,4,4,17),(2,1,6,8),(6,2,1,1)]),
 (8,[2,3,13,12,8,7],7,[793,770,798,-5882],7,[(1,2,8,2),(1,5,6,4),(8,4,2,1)]),
 (64,[2,3,120,105,70,63],105,[871710,900446,899046,-51743768],735,[(4,19,64,241),(5,19,64,12),(16,40,43,419),(64,31,17,63)])]
finite=[]
for m,coef,D,du,P,atoms in cases:
    def value(A,B,C):
        return sum(x*y for x,y in zip(coef,[C*(C-1)*(C-2)//6,B*C*(C-1)//2,B*(B-1)//2,A*C,A*B,A*(A-1)//2]))
    minimum=min(D*value(A,B,C)-sum(x*y for x,y in zip(du,[A,B,C,1])) for A,B,C in product(range(m+1),repeat=3))
    assert minimum==0
    assert sum(v[3] for v in atoms)==P
    assert [sum(Q(v[3]*v[i],P) for v in atoms) for i in range(3)]==[Q(m,4),Q(m,2),Q(3*m,4)]
    vx=sum(Q(v[3],P)*value(*v[:3]) for v in atoms)
    assert vx==sum(Q(x,D)*y for x,y in zip(du,[Q(m,4),Q(m,2),Q(3*m,4),1]))
    # independently derive all upper and lower term envelopes from orbit means
    orbits=[(comb(m,3),[Q(3,4)]*3),(m*comb(m,2),[Q(1,2),Q(3,4),Q(3,4)]),(comb(m,2),[Q(1,2)]*2),(m*m,[Q(1,4),Q(3,4)]),(m*m,[Q(1,4),Q(1,2)]),(comb(m,2),[Q(1,4)]*2)]
    cv=sum(co*count*min(means) for co,(count,means) in zip(coef,orbits))
    lv=sum(co*count*max(0,sum(means)-len(means)+1) for co,(count,means) in zip(coef,orbits))
    finite.append({'n':3*m,'states':(m+1)**3,'vex':str(vx),'cav':str(cv),'ratio':str((cv-lv)/(cv-vx))})
out['finite_three_group']=finite
out['finite_two_group']=[]
for m,du in [(4,[Q(9),Q(4),Q(-19)]),(8,[Q(47),Q(20),Q(-188)]),(12,[Q(231,2),Q(48),Q(-684)]),(16,[Q(214),Q(177,2),Q(-1686)])]:
    value=lambda A,C:A*comb(C,2)+Q(5*m,4)*comb(A,2)
    assert min(value(A,C)-du[0]*A-du[1]*C-du[2] for A,C in product(range(m+1),repeat=2))==0
    vx=value(m//2,3*m//4)
    assert vx==du[0]*m/2+du[1]*3*m/4+du[2]
    cv=Q(9*m,8)*comb(m,2)
    out['finite_two_group'].append([m,str(vx),str(cv/(cv-vx))])

# Exact integration of complete laws, independent of the case formulas in the proof.
def law_product(means,kind):
    n=len(means)
    breaks=sorted({Q(0),Q(1),*means,*[1-x for x in means],*[2*(1-x) for x in means if x>Q(1,2)]})
    ans=Q(0)
    for l,u in zip(breaks,breaks[1:]):
        v=(l+u)/2
        if kind=='O':
            conditional=[Q(int(v<x)+int(v>1-x),2) for x in means]
        else:
            conditional=[Q(int(v<x)) if x<=Q(1,2) else (Q(1,2) if v<2*(1-x) else Q(1)) for x in means]
        pr=Q(1)
        for z in conditional: pr*=z
        ans+=(u-l)*pr
    return ans
grid=[Q(i,20) for i in range(21)]
checked=0
for n in [2,3]:
    for means in combinations_with_replacement(grid,n):
        gap=min(means)-max(0,sum(means)-n+1)
        ip=Q(1)
        for x in means: ip*=x
        deficiency=(18*(min(means)-law_product(means,'O'))+6*(min(means)-ip)+7*(min(means)-law_product(means,'B')))/31
        assert deficiency>=Q(12,31)*gap,(means,deficiency,gap)
        checked+=1
out['exact_cubic_grid']={'grid_denominator':20,'sorted_pairs_and_triples':checked,'scope':'Finite boundary-rich check; universal proof reviewed separately.'}

# Full-anchor count LP, without imposing nested anchors or the published profiles.
LP=[]
for L in range(2,8):
    m=2**L
    states=list(product(product([0,1],repeat=L),range(m+1)))
    mat=np.array([[1,R,*bits] for bits,R in states],dtype=float).T
    cost=np.array([-sum(bits[j]*min(2**(j+1),R) for j in range(L)) for bits,R in states])
    opt=linprog(cost,A_eq=mat,b_eq=[1,1,*[2**(-j) for j in range(1,L+1)]],bounds=(0,None),method='highs')
    assert opt.success
    cut=next(j for j in range(1,L) if Q(L-j+1,2**(j+1))<=1<=Q(L-j+2,2**j))
    exact=Q(cut)+Q(L-cut,2**cut)
    assert abs(-opt.fun-float(exact))<1e-8
    LP.append([L,len(states),-opt.fun,str(exact)])
out['numerical_full_anchor_LP']=LP

radix=[]
for base in range(2,10):
    for L in range(2,21):
        M=lambda q:Q((L-q)*(base-1)+base,base**q)
        cut=next(q for q in range(1,L) if M(q+1)<=1<=M(q))
        weights=[Q(base-1,base**(l+1)) if l<L else Q(1,base**L) for l in range(L+1)]
        prof=lambda q,l:base**(l-q+1) if l>=q else 0
        mix=(1-M(cut+1))/(M(cut)-M(cut+1))
        assert 0<=mix<=1
        assert sum(weights)==1
        resources=[];objs=[]
        for q in [cut,cut+1]:
            resources.append(sum(weights[l]*prof(q,l) for l in range(L+1)))
            objs.append(sum(weights[l]*sum(min(base**j,prof(q,l)) for j in range(1,l+1)) for l in range(L+1)))
        assert mix*resources[0]+(1-mix)*resources[1]==1
        assert mix*objs[0]+(1-mix)*objs[1]==cut+Q(L-cut,base**cut)
        radix.append([base,L,cut])
out['exact_radix_profiles']=len(radix)

numeric=[]
for d in [2,3,10,100,10000,10**10,10**30]:
    for scale in [1,2,10]:
        M=(d-1)*scale
        lam=1+np.log(float(M)); eta=(d-1)/M
        fun=lambda v: -np.expm1(-(1-eta*v)/(lam*v)) if v else 1.0
        J=lambda z:quad(fun,z,1,epsabs=1e-12)[0]
        z=brentq(lambda z:J(z)-z,1e-14,1-1e-14)
        w=brentq(lambda w:w+np.log(w)-(np.log(lam)-eta),1e-12,100)
        if w>=1: assert z+1e-10>=(w-1/(2*w))/lam
        numeric.append([d,scale,z,w])
out['numerical_fixed_points']=numeric

out['scope']='Independent finite exact identities/count checks and numerical LP/quadrature falsification attempts. No finite computation certifies universal results.'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
