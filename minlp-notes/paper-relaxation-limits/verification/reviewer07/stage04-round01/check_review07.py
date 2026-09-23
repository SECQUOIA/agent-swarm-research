"""Independent exact boundary/graph checks; not a proof of universal positivity."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
from pathlib import Path
import json
import sympy as sp

out=Path(__file__).parent
counts={}
def fall(t,a):
    ans=sp.S.One
    for j in range(a): ans*=t-j
    return ans

def expectation(poly, us, t):
    pp=sp.Poly(sp.expand(poly),*us)
    return sp.factor(sum(c*fall(t,sum(e>0 for e in a))/fall(len(us),sum(e>0 for e in a)) for a,c in pp.terms()))

# Polynomial Gram identities independent of any floating-point eigensolver.
s,t=sp.symbols('s t')
for d in range(1,6):
    for ell in range(d+1):
        rhs=sum(comb(ell,j)*fall(t,2*d-j)*fall(s-t,j) for j in range(ell+1))
        lhs=fall(t,2*d-ell)*fall(s-2*d+ell,ell)
        assert sp.expand(rhs-lhs)==0
        counts['gram_entries']=counts.get('gram_entries',0)+1

# Equality tolerance optimum and all midpoint stopping counts, exact arithmetic.
for n in range(2,13):
    for k in range(n):
        def leaves(a,b):
            if a==0 or b==0:return 1
            return leaves(a-1,b)+leaves(a,b-1)
        assert leaves(k+1,n-k)==comb(n+1,k+1)
        counts['tree_counts']=counts.get('tree_counts',0)+1
        for delta in [Q(0),Q(1,7),Q(49,100)]:
            for v in [Q(1,2)-delta,Q(1,2)+delta]:
                assert v*(1-v)==Q(1,4)-delta*delta
                counts['tolerance_endpoints']=counts.get('tolerance_endpoints',0)+1

# Noncompact graph y=1/x for x>0 and y=0 at x=0, finite everywhere.
# r=2; k=m=z=5; restrict one middle coordinate to its true witness p=1/10.
# All other coordinate domains can be nonclosed: {0,1} union (0,1/2).
n=15
xs=sp.symbols('x:15'); ys=sp.symbols('y:15'); us=sp.symbols('u:14')
p=sp.Rational(1,10); demand=sp.Rational(11,2); rem=demand-p
sub={xs[0]:p,ys[0]:1/p}
sub.update({xs[i]:us[i-1] for i in range(1,n)})
sub.update({ys[i]:us[i-1] for i in range(1,n)})
def L(poly): return expectation(sp.expand(poly).subs(sub,simultaneous=True),us,rem)
assert L(1)==1
F=sum(x*(1-x) for x in xs)
assert L(F)==p*(1-p)
e=sum(xs)-demand
basis=[xs[0],xs[1],xs[2],ys[0],ys[1],ys[2]]
for degree in range(4):
    for inds in combinations_with_replacement(range(len(basis)),degree):
        v=sp.prod(basis[i] for i in inds)
        assert L(e*v)==0
        counts['lifted_balance_products']=counts.get('lifted_balance_products',0)+1
for i in range(3):
    h=xs[i]**2*ys[i]-xs[i]
    for v in [sp.S.One]+list(xs)+list(ys):
        assert L(h*v)==0
        counts['lifted_graph_equalities']=counts.get('lifted_graph_equalities',0)+1
# A written objective couples two graph blocks; agreement is on the full graph.
Ft=F+(xs[1]**2*ys[1]-xs[1])*ys[2]
assert L(Ft)==L(F)
counts['coupled_objective']=1
# Local nonnegative polynomials, repeated products and globally coupled squares.
gens=[xs[0],1-xs[0],ys[0],xs[1],1-xs[1],ys[1],ys[1]-xs[1],xs[2],1-xs[2],ys[2]]
for inds in combinations_with_replacement(range(len(gens)),2):
    g=sp.prod(gens[i] for i in inds)
    P=1+sum((-1)**i*(i+1)*ys[i] for i in range(n))
    assert L(g*P**2)>=0
    counts['global_square_localizers']=counts.get('global_square_localizers',0)+1
for inds in combinations_with_replacement(range(len(gens)),4):
    assert L(sp.prod(gens[i] for i in inds))>=0
    counts['degree_four_local_products']=counts.get('degree_four_local_products',0)+1
# Integer threshold and negative noninteger boundary probes.
for r in range(1,6):
    for twice in range(1,4*r-2,2):
        t=sp.Rational(twice,2); a=int(t)+2; ss=max(2*r,a)
        assert fall(t,a)/fall(ss,a)<0
        counts['negative_indicator_boundaries']=counts.get('negative_indicator_boundaries',0)+1
eta=Q(1,32); theta=Q(1,32); K=Q(5,2)
tau=Q(1,4)-theta*(K+Q(1,4))-eta
assert tau==Q(17,128) and Q(2,6)*tau==Q(17,384)
report={'status':'PASS','arithmetic':'exact symbolic/rational','counts':counts,'scope':'Finite supplemental checks; universal PSD and lift transfer require analytic proofs.'}
(out/'check_review07.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
