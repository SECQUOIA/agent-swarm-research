from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod, log, exp, expm1
from pathlib import Path
import json
import sympy as S
from scipy.integrate import quad
from scipy.optimize import brentq

out = {}
# Actual law integration, not the piecewise deficiency formulas in the proof.
def endpoint(means):
    return sum((max(Q(0), min(x if o == 0 else Q(1) for x,o in zip(means,orient))
                    -max(Q(0) if o == 0 else 1-x for x,o in zip(means,orient)))
                for orient in product(range(2), repeat=len(means))),Q(0))/2**len(means)
def law_b(means):
    cuts = sorted({Q(0),Q(1)} | {x if x <= Q(1,2) else 2*(1-x) for x in means})
    val = Q(0)
    for left,right in zip(cuts,cuts[1:]):
        t=(left+right)/2
        success = [Q(t<=x) if x<=Q(1,2) else (Q(1,2) if t<=2*(1-x) else Q(1)) for x in means]
        val += (right-left)*prod(success)
    return val
nchecks=0
minratio=Q(1)
for k in (1,2,3):
    for means in combinations_with_replacement([Q(i,16) for i in range(17)],k):
        upper=min(means)
        oi,bi=endpoint(means),law_b(means)
        if k==1:
            assert oi==bi==upper
            continue
        t=upper-max(Q(0),sum(means)-k+1)
        deficit=(18*(upper-oi)+6*(upper-prod(means))+7*(upper-bi))/31
        assert deficit >= Q(12,31)*t, means
        if t: minratio=min(minratio,deficit/t)
        nchecks+=1
out['cubic_exact_integrated_tuples']=nchecks
out['cubic_minimum_fraction']=str(minratio)

# Integer resource certificate and simultaneous prefix realization.
for L in range(2,10):
    m=2**L
    w=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    bs=lambda q: Q(L-q+2,2**q)
    for s in range(1,L):
        if not(bs(s+1)<=1<=bs(s)): continue
        theta=(1-bs(s+1))/(bs(s)-bs(s+1))
        budget=utility=Q(0)
        for l in range(L+1):
            fl=0 if l<=s else 2**(l-s+1)-2
            for r in range(m+1):
                assert sum(min(2**j,r) for j in range(1,l+1))<=s*r+fl
            for q,weight in ((s,theta),(s+1,1-theta)):
                r=0 if l<q else 2**(l-q+1)
                val=sum(min(2**j,r) for j in range(1,l+1))
                assert val==s*r+fl
                budget+=w[l]*weight*r
                utility+=w[l]*weight*val
        assert budget==1 and utility==s+Q(L-s,2**s)
    reverse=[int(format(i,f'0{L}b')[::-1],2) for i in range(m)]
    for r in range(m+1):
        for j in range(1,L+1):
            assert len({v>>(L-j) for v in reverse[:r]})==min(2**j,r)
out['dyadic_exact_L']='2..9, every integer count and all admissible tied cutoffs'

# Fresh symbolic elimination, Bernstein reconstruction and two-level factorization.
a,b,c,t=S.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a-37*a-S.Rational(79,2)*b-38*c+S.Rational(103,3)
opt=S.solve([S.diff(h,a),S.diff(h,b)],(a,b))
r=S.expand(h.subs(opt))
p=S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
rows=[(p,0,Q(1,5),60000,[63125,39125,20975,9395,4133]),
(p,Q(1,5),Q(3,10),240000,[16532,6008,1802,3788,11597]),
(r,Q(3,10),Q(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
(r,Q(1,2),Q(3,4),190464,[25808,18056,7964,9230,15869]),
(r,Q(3,4),1,190464,[15869,22508,34520,45920,31040])]
coefficients=[]
for pol,lo,hi,D,nums in rows:
    rhs=sum(S.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(nums))
    assert S.expand(pol.subs(c,lo+(hi-lo)*t)-rhs)==0
    coefficients += [Q(v,D) for v in nums]
assert min(coefficients)==Q(901,120000)
assert Q(161,4)/(Q(223,12)-min(coefficients))==Q(1610000,743033)
for weight,linear,center,residual,atoms in [
(S.Rational(5,4),S.Rational(11,6)*a+S.Rational(20,27)*c-S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135,[(Q(1,4),Q(1,3),Q(1)),(Q(3,4),Q(5,9),Q(2,3))]),
(S.Rational(24,25),S.Rational(41,25)*a+S.Rational(4,5)*c-S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480,[(Q(1,2),Q(1,3),Q(1)),(Q(1,2),Q(2,3),Q(3,5))])]:
    difference=a*c*c+weight*a*a-linear
    assert S.expand(difference-weight*(a-center)**2-residual)==0
    assert all(difference.subs({a:aa,c:cc})==0 for _,aa,cc in atoms)
out['symbolic']='five Bernstein identities from eliminated Hessian; both scalar sum-of-squares identities and equality atoms'

# Harmonic actual conditional product integrated on every cutoff segment.
harmonic_cases=0
for degree in [2,3,5,12,40]:
    for factor in [1,1.25,5,30]:
        M=(degree-1)*factor
        lam=1+log(M); eta=(degree-1)/M
        J=lambda z: quad(lambda v:-expm1(-(1-eta*v)/(lam*v)),z,1,epsabs=1e-12)[0]
        zeta=brentq(lambda z:J(z)-z,1e-12,1-1e-12,xtol=1e-14)
        w=brentq(lambda w:w+log(w)-log(lam)+eta,1e-12,max(2,log(lam)+2))
        if w>=1: assert zeta+1e-11 >= (w-1/(2*w))/lam
        for u in [.01,.5]:
            for scale in [.00001,.1,.49]:
                ps=[scale*(.13**j) for j in range(degree-1)]
                if degree>2: ps[-1]=0
                gap=min(u,sum(ps))
                z=min(max(ps)/gap,1)
                def q(p,time):
                    if p==0: return 0.
                    h=min(M*p,1.)
                    return min(1,p/time)/(1+log(h/p)) if time<h else 0.
                bounds=sorted({0.,1.}|{v/u for p in ps for v in (p,min(M*p,1.)) if 0<v<u})
                val=sum(quad(lambda v:1-prod(1-q(p,v*u) for p in ps),l,r,epsabs=1e-13)[0] for l,r in zip(bounds,bounds[1:]))*u/gap
                assert val+1e-9>=J(z), (degree,factor,u,scale,val,J(z))
                harmonic_cases+=1
out['harmonic_numeric_cases']=harmonic_cases
out['harmonic_numeric_limit']='floating quadrature only, separate from the universal analytic proof'

# Exact equal-mean positivity and adjacent-count theorem consequences.
cases=0
for n in range(2,25):
    for j in range(1,20):
        u=Q(j,20); b=(n*u).__floor__(); theta=n*u-b
        for d in range(2,n+1):
            q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
            td=min(u,(d-1)*(1-u))
            assert 0<=q<=u**d<u and td/(u-q)<2
            cases+=1
out['equal_mean_exact_cases']=cases
print(json.dumps(out,indent=2))
Path(__file__).with_name('independent-results.json').write_text(json.dumps(out,indent=2)+'\n')
