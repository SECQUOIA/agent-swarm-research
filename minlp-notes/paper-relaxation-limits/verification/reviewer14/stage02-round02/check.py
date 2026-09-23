"""Independent Stage 2 review checks; no optimization solver is needed."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, exp, log, expm1
from contextlib import redirect_stdout
from io import StringIO
import hashlib
import json
import re

import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
PAPER = OUT.parents[2]
SNAP = PAPER / 'process/snapshots/stage02-round02'
report = {}

# Replay the code visible to a reader, checking both blocks against the file.
tex = (SNAP / 'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', tex, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (SNAP / 'verification/check_stage02_finite.py').read_text()
buf = StringIO()
with redirect_stdout(buf):
    exec(compile(printed, 'frozen printed appendix', 'exec'), {})
report['printed_exact_replay'] = {
    'blocks': 2, 'sha256': hashlib.sha256(printed.encode()).hexdigest(),
    'three_group_states': 7**3 + 9**3 + 65**3,
    'two_group_states': 5**2 + 9**2 + 13**2 + 17**2,
    'output': buf.getvalue().splitlines(),
}

# Recompute the scalar eliminations, then independently derive Bernstein
# coefficients from power coefficients rather than trusting the table.
a,b,c,t,m = s.symbols('a b c t m')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h = F-(37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3))
Hess = s.hessian(h,(a,b))
assert Hess.det() == 248 and Hess[0,0] > 0
boundary = {a:1,b:s.Rational(13,24)-3*c**2/4}
p = s.expand(h.subs(boundary))
stationary = s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r = s.factor(h.subs(stationary))
assert s.diff(h,b).subs(boundary).expand() == 0
assert s.diff(h,a).subs(boundary).subs(c,s.Rational(3,10)) == -s.Rational(31,60)
scalar = (SNAP/'sections/03-cubic-equal-means.tex').read_text()
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',scalar)
assert len(rows) == 5
all_coeff=[]
for name,lo,hi,den,nums in rows:
    lo,hi = s.Rational(lo),s.Rational(hi)
    transformed = s.Poly((p if name=='p' else r).subs(c,lo+(hi-lo)*t),t)
    coeff=[s.expand(sum(transformed.nth(j)*s.binomial(i,j)/s.binomial(4,j)
                        for j in range(i+1))) for i in range(5)]
    displayed=[s.Rational(v,int(den)) for v in nums.split(',')]
    assert coeff == displayed
    all_coeff.extend(coeff)
delta=min(all_coeff)
assert delta == s.Rational(901,120000)
assert (s.Rational(161,4)/(s.Rational(223,12)-delta)) == s.Rational(1610000,743033)
bin2=lambda v:v*(v-1)/2
bin3=lambda v:v*(v-1)*(v-2)/6
count=2*bin3(m*c)+3*m*b*bin2(m*c)+2*m*bin2(m*b)+5*m**3*a*c/3+10*m**3*a*b/9+m*bin2(m*a)
assert s.expand(18*count/m**3-F+(18*c**2+27*b*c+18*b+9*a)/m-12*c/m**2)==0
for k,ell,center,sqextra in [
    (s.Rational(5,4),s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108),
     (11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (s.Rational(24,25),s.Rational(41,25)*a+s.Rational(4,5)*c-s.Rational(68,75),
     (41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+k*a*a-ell-k*(a-center)**2-sqextra)==0
finite_num=s.Rational(161,4)-s.Rational(135,4)/36+s.Rational(6,36**2)
finite_den=s.Rational(223,12)+s.Rational(135,4)/36+s.Rational(9,36**2)
assert finite_num/finite_den == s.Rational(16985,8436)
assert finite_num/(finite_den-delta) == s.Rational(42462500,21081891)
report['exact_symbolic']={'bernstein_coefficients':25,'minimum':str(delta),'two_level_identities':2,'m36_with_slack':str(finite_num/(finite_den-delta))}

# Actual O and B laws integrated on their constant-probability intervals.
# This code does not use the manuscript's deficiency formulas by low class.
def orientation_expectation(means):
    total=Q(0)
    for orientations in product((0,1),repeat=len(means)):
        starts=[Q(0) if v==0 else 1-x for x,v in zip(means,orientations)]
        stops=[x if v==0 else Q(1) for x,v in zip(means,orientations)]
        total+=max(Q(0),min(stops)-max(starts))
    return total/2**len(means)

def b_law(means):
    ends=sorted({Q(0),Q(1),*(x if x<=Q(1,2) else 2*(1-x) for x in means)})
    joint=Q(0)
    marg=[Q(0)]*len(means)
    for lo,hi in zip(ends,ends[1:]):
        midpoint=(lo+hi)/2
        probs=[Q(midpoint<x) if x<=Q(1,2) else 1-Q(midpoint<2*(1-x),2) for x in means]
        term=Q(1)
        for i,v in enumerate(probs):
            term*=v
            marg[i]+=(hi-lo)*v
        joint+=(hi-lo)*term
    assert marg == list(means)
    return joint

grid=sorted({Q(i,16) for i in range(17)}|{Q(1,3),Q(2,3)})
n_laws=0
min_slack=None
for degree in (2,3):
    for means in combinations_with_replacement(grid,degree):
        u=min(means)
        term_gap=u-max(Q(0),sum(means)-degree+1)
        pi=Q(1)
        for x in means: pi*=x
        deficiency=18*(u-orientation_expectation(means))+6*(u-pi)+7*(u-b_law(means))
        slack=deficiency-12*term_gap
        assert slack>=0
        if term_gap>0: min_slack=slack if min_slack is None else min(min_slack,slack)
        n_laws+=1
report['exact_actual_laws']={'marginal_tuples':n_laws,'grid':[str(x) for x in grid],'minimum_unnormalized_slack':str(min_slack)}

# Exact dyadic dual checks, resource means, and explicit leaf-set realization.
dyadic=[]
for L in range(2,11):
    mm=2**L
    B=lambda q:Q(L-q+2,2**q)
    valid=[ss for ss in range(1,L) if B(ss+1)<=1<=B(ss)]
    values=[]
    for ss in valid:
        expected=Q(0); failed_mean=Q(0); anchor_mean=[Q(0)]*L
        theta=(1-B(ss+1))/(B(ss)-B(ss+1))
        for q,weight in [(ss,theta),(ss+1,1-theta)]:
            for ell in range(L+1):
                mass=weight*Q(1,2**(ell+1) if ell<L else 2**L)
                R=0 if ell<q else 2**(ell-q+1)
                failed_mean+=mass*R
                for j in range(1,L+1): anchor_mean[j-1]+=mass*(j<=ell)
                expected+=mass*sum(min(2**j,R) for j in range(1,ell+1))
                selected=[int(format(k,f'0{L}b')[::-1],2) for k in range(R)]
                assert all(len({v//2**(L-j) for v in selected})==min(2**j,R) for j in range(1,L+1))
                if L<=6 and mass:
                    leaf_hits=[0]*mm
                    for shift in range(mm):
                        for leaf in selected: leaf_hits[leaf^shift]+=1
                    assert leaf_hits == [R]*mm
        assert failed_mean==1
        assert anchor_mean==[Q(1,2**j) for j in range(1,L+1)]
        assert expected==ss+Q(L-ss,2**ss)
        for ell,R in product(range(L+1),range(mm+1)):
            offset=0 if ell<=ss else 2**(ell-ss+1)-2
            assert sum(min(2**j,R) for j in range(1,ell+1))<=ss*R+offset
        values.append(expected)
    assert len(set(values))==1
    dyadic.append({'L':L,'cutoffs':valid,'H':str(values[0])})
report['exact_dyadic']=dyadic

# Equal-mean count formula equals the classical max-of-affines specialization.
n_equal=0
for n in range(2,21):
    for u in (Q(i,13) for i in range(1,13)):
        floor=(n*u).numerator//(n*u).denominator
        theta=n*u-floor
        for d in range(2,n+1):
            convex=(1-theta)*comb(floor,d)+theta*comb(floor+1,d)
            classical=max([Q(0)]+[comb(k,d-1)*n*u-(d-1)*comb(k+1,d) for k in range(d-1,n)])
            assert convex==classical
            q=convex/comb(n,d)
            assert 0<=q<u**d<u
            assert min(u,(d-1)*(1-u))/(u-q)<2
            n_equal+=1
report['exact_equal_means']={'cases':n_equal}

# Numerical supplement, explicitly not a certified universal proof.
numeric=[]
for degree in [2,3,4,10,100,10000]:
    for factor in [1,1.5,10,10000]:
        M=(degree-1)*factor
        lam=1+log(M); eta=(degree-1)/M
        integrand=lambda v:-expm1(-(1-eta*v)/(lam*v)) if v else 1.0
        J=lambda z:quad(integrand,z,1,epsabs=1e-12,epsrel=1e-12)[0]
        root=brentq(lambda z:J(z)-z,1e-12,1,xtol=1e-14)
        w=brentq(lambda w:w+log(w)-log(lam)+eta,1e-12,max(1,lam))
        bound=(w-1/(2*w))/lam if w>=1 else None
        assert bound is None or root+1e-11>=bound
        for pp in [1e-8,0.01,0.49]:
            end=min(M*pp,1); norm=1+log(end/pp)
            integral=pp/norm+quad(lambda tt:pp/(tt*norm),pp,end,epsabs=1e-13)[0]
            assert abs(integral-pp)<1e-10
        numeric.append({'d':degree,'M':M,'zeta':root,'lambert_lower':bound})
report['numerical_harmonic']={'cases':numeric,'normalizations':len(numeric)*3,'status':'sanity checks only; quadrature/root tolerances are not interval certificates'}

assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
assert Q(943)/(Q(3225,7)+Q(1840,1000))==Q(165025,80947)
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
report['finite_padding_and_sampling']='exact rational checks passed'
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:('passed' if k!='numerical_harmonic' else 'numerical sanity passed') for k in report},indent=2))
