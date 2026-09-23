from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod
import contextlib, io, json, re
import sympy as s

root = Path(__file__).resolve().parents[3]
frozen = root/'process/snapshots/stage02-round02'
out = Path(__file__).resolve().parent
appendix = (frozen/'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', appendix, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (frozen/'verification/check_stage02_finite.py').read_text()
stream=io.StringIO()
with contextlib.redirect_stdout(stream):
    exec(compile(printed, 'frozen-printed-checker', 'exec'), {})
(out/'printed-checker.log').write_text(stream.getvalue())
report = {'printed_blocks':len(blocks), 'printed_finite_replay':'PASS'}

# Independent exact resource profiles and pointwise affine dual.
dyadic=[]
for L in range(2,10):
    m=2**L
    B=lambda q:Q(L-q+2,2**q)
    cuts=[q for q in range(1,L) if B(q+1)<=1<=B(q)]
    answers=[]
    for cut in cuts:
        theta=(1-B(cut+1))/(B(cut)-B(cut+1))
        w=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
        atoms=[(w[l]*mass,l,0 if l<q else 2**(l-q+1))
               for q,mass in [(cut,theta),(cut+1,1-theta)] for l in range(L+1)]
        assert sum(p for p,l,r in atoms)==1
        assert sum(p*r for p,l,r in atoms)==1
        for j in range(1,L+1):
            assert sum(p for p,l,r in atoms if l>=j)==Q(1,2**j)
        obj=sum(p*sum(min(2**j,r) for j in range(1,l+1)) for p,l,r in atoms)
        assert obj==cut+Q(L-cut,2**cut)
        for l,r in product(range(L+1),range(m+1)):
            const=0 if l<=cut else 2**(l-cut+1)-2
            assert sum(min(2**j,r) for j in range(1,l+1))<=cut*r+const
        answers.append(obj)
    assert len(set(answers))==1
    if L<=6:
        rev=[int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
        for R in range(m+1):
            failures=rev[:R]
            for j in range(1,L+1):
                assert len({v>>(L-j) for v in failures})==min(2**j,R)
            for leaf in range(m):
                assert sum((leaf^shift) in failures for shift in range(m))==R
    dyadic.append({'L':L,'cuts':cuts,'H':str(answers[0])})
report['dyadic_exact']=dyadic

# Recompute eliminated polynomials and read all Bernstein integers from frozen table.
a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b*b+30*a*c+20*a*b+9*a*a
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
H=s.hessian(h,(a,b))
assert H.det()==248
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-s.Rational(3,4)*c*c}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
tex=(frozen/'sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\$?\(([^)]+)\)\$',tex)
assert len(rows)==5, rows
minimum=s.Integer(100)
for name,lo,hi,den,vals in rows:
    lo,hi=s.Rational(lo),s.Rational(hi)
    vals=[int(v) for v in vals.split(',')]
    bern=sum(s.Rational(v,int(den))*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vals))
    assert s.expand(bern-{'p':p,'r':r}[name].subs(c,lo+(hi-lo)*t))==0
    minimum=min(minimum,*[s.Rational(v,int(den)) for v in vals])
assert minimum==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-minimum)==s.Rational(1610000,743033)
for coef,la,lc,l0,center,rem in [
(s.Rational(5,4),s.Rational(11,6),s.Rational(20,27),-s.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
(s.Rational(24,25),s.Rational(41,25),s.Rational(4,5),-s.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+coef*a*a-la*a-lc*c-l0-coef*(a-center)**2-rem)==0
report['symbolic']={'Bernstein_rows':5,'minimum':str(minimum),'two_level_identities':2}

# Integrate O and B from definitions, without the proof's case formulas.
def orientation(x):
    value=Q(0)
    for side in product((0,1),repeat=len(x)):
        left=max([1-v for v,k in zip(x,side) if k]+[Q(0)])
        right=min([v for v,k in zip(x,side) if not k]+[Q(1)])
        value+=max(Q(0),right-left)/2**len(x)
    return value

def lawB(x):
    endpoints=sorted(set([Q(0),Q(1)]+[v if v<=Q(1,2) else 2*(1-v) for v in x]))
    value=Q(0)
    for lo,hi in zip(endpoints,endpoints[1:]):
        mid=(lo+hi)/2
        probabilities=[int(mid<=v) if v<=Q(1,2) else (Q(1,2) if mid<=2*(1-v) else Q(1)) for v in x]
        value+=(hi-lo)*prod(probabilities)
    return value
count=0
for k in (2,3):
    for x in combinations_with_replacement([Q(j,16) for j in range(17)],k):
        u=min(x); gap=u-max(0,sum(x)-k+1)
        deficiency=(18*(u-orientation(x))+6*(u-prod(x))+7*(u-lawB(x)))/31
        assert deficiency>=Q(12,31)*gap,(x,deficiency,gap)
        count+=1
report['actual_cubic_laws_exact_grid_cases']=count
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

# Finite perturbation/sampling margins and equal-mean comparisons.
assert Q(3225,7)+Q(46,25)==Q(80947,175)
assert Q(943)/Q(80947,175)==Q(165025,80947)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)==-Q(524942,29)<0
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
assert (Q(161,4)-Q(135,4*36)+Q(6,36**2))/(Q(223,12)+Q(135,4*36)+Q(9,36**2))==Q(16985,8436)
equal_cases=0
for n in range(2,17):
    for denominator in range(2,13):
        for numerator in range(1,denominator):
            u=Q(numerator,denominator)
            base=(n*u).__floor__(); theta=n*u-base
            for d in range(2,n+1):
                q=((1-theta)*comb(base,d)+theta*comb(base+1,d))/comb(n,d)
                assert 0<=q<=u**d<u
                gap=min(u,(d-1)*(1-u))
                assert gap/(u-q)<2
                equal_cases+=1
report['equal_mean_exact_cases']=equal_cases
report['finite_perturbation_sampling_margins']='PASS'
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
