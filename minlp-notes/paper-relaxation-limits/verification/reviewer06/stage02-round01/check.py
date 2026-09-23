from pathlib import Path
from fractions import Fraction as Q
from math import comb
import sympy as s

paper = Path(__file__).resolve().parents[3]
frozen = paper / 'process/snapshots/stage02-round01'
appendix = (frozen/'sections/appendix-cubic-certificates.tex').read_text()
printed = appendix.split(r'\begin{verbatim}')[1].split(r'\end{verbatim}')[0]
exec(compile(printed, 'frozen printed finite checker', 'exec'), {})

# Recompute the eliminated scalar polynomials from F - ell.
a,b,c,t = s.symbols('a b c t')
h = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a-37*a-s.Rational(79,2)*b-38*c+s.Rational(103,3)
bstar = s.solve(s.diff(h,b).subs(a,1),b)[0]
p = s.expand(h.subs({a:1,b:bstar}))
stationary = s.solve([s.diff(h,a),s.diff(h,b)], [a,b])
r = s.expand(h.subs(stationary))
rows = [(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
(p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
(r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
(r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
(r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,lo,hi,D,vs in rows:
    coeff = s.Poly(poly.subs(c,lo+(hi-lo)*t),t)
    bern = [sum(coeff.nth(j)*s.Rational(comb(k,j),comb(4,j)) for j in range(k+1)) for k in range(5)]
    assert bern == [s.Rational(v,D) for v in vs]
delta = min(s.Rational(v,D) for _,_,_,D,vs in rows for v in vs)
assert delta == s.Rational(901,120000)
assert (s.Rational(161,4)/(s.Rational(223,12)-delta)) == s.Rational(1610000,743033)
for coeff,ell,center,resid,atoms,mean,value in [
(s.Rational(5,4),s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135,[(s.Rational(1,4),s.Rational(1,3),1),(s.Rational(3,4),s.Rational(5,9),s.Rational(2,3))],(s.Rational(1,2),s.Rational(3,4)),s.Rational(16,27)),
(s.Rational(24,25),s.Rational(41,25)*a+s.Rational(4,5)*c-s.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480,[(s.Rational(1,2),s.Rational(1,3),1),(s.Rational(1,2),s.Rational(2,3),s.Rational(3,5))],(s.Rational(1,2),s.Rational(4,5)),s.Rational(83,150))]:
    F = a*c*c+coeff*a*a
    assert s.expand(F-ell-coeff*(a-center)**2-resid)==0
    assert tuple(sum(prob*atom[j] for prob,*atom in atoms) for j in range(2))==mean
    assert sum(prob*F.subs({a:aa,c:cc}) for prob,aa,cc in atoms)==value
    assert ell.subs(dict(zip((a,c),mean)))==value
print('Exact scalar eliminations, all Bernstein rows, and both two-level identities/attainments passed.')

# Dyadic profile resource, anchor means, and supporting-line equalities.
for L in range(2,101):
    wl=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q: Q(L-q+2,2**q)
    cutoffs=[q for q in range(1,L) if B(q+1)<=1<=B(q)]
    vals=[]
    for cut in cutoffs:
        mix=(1-B(cut+1))/(B(cut)-B(cut+1))
        expected_R=Q(0); attained=Q(0)
        for q,prob in [(cut,mix),(cut+1,1-mix)]:
            for l,w in enumerate(wl):
                R=0 if l<q else 2**(l-q+1)
                S=sum(min(2**j,R) for j in range(1,l+1))
                intercept=0 if l<=cut else 2**(l-cut+1)-2
                assert S==cut*R+intercept
                expected_R+=prob*w*R
                attained+=prob*w*S
        assert expected_R==1
        assert attained==cut+Q(L-cut,2**cut)
        vals.append(attained)
    assert len(set(vals))==1
    for j in range(1,L+1):
        assert sum(wl[j:])==Q(1,2**j)
# Prefix geometry checked separately, using actual labels.
for L in range(2,9):
    labels=[int(format(i,f'0{L}b')[::-1],2) for i in range(2**L)]
    for R in range(2**L+1):
        for j in range(1,L+1):
            assert len({v>>(L-j) for v in labels[:R]})==min(2**j,R)
print('Exact dyadic profiles L=2..100 and prefix geometry L=2..8 passed.')

# Independent rational arithmetic for finite homogeneous/sampling margins.
assert Q(3225,7)+Q(1840,1000)==Q(80947,175)
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
assert Q(2160)/(Q(1072)+Q(12,5))==Q(2700,1343)
print('Exact finite perturbation and 25,000-variable existence margins passed.')
