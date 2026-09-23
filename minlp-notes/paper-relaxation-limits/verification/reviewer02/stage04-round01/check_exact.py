"""Independent finite exact checks; no manuscript or author-check imports."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from functools import lru_cache
from pathlib import Path
import json
import random
import sympy as sp

counts = {}
def fall(x,a):
    out=1
    for j in range(a): out*=x-j
    return out
s,t=sp.symbols('s t')
count=0
for d in range(1,8):
    for ell in range(d+1):
        rhs=sum(comb(ell,j)*fall(t,2*d-j)*fall(s-t,j) for j in range(ell+1))
        lhs=fall(t,2*d-ell)*fall(s-2*d+ell,ell)
        assert sp.Poly(rhs-lhs,s,t).is_zero
        count+=1
counts['symbolic_gram_entries']=count

# Exact polynomial identities supporting SDP and clique arithmetic.
c=t/s; dd=t*(t-1)/(s*(s-1))
for expr in [c+(s-1)*dd-t*c, c-dd-t*(s-t)/(s*(s-1)),
             dd-c*c+(c-dd)/s, 1-2*c+dd-(s-t)*(s-t-1)/(s*(s-1))]:
    assert sp.cancel(expr)==0
k=sp.symbols('k'); K=k+sp.Rational(1,2)
assert sp.expand(K*K-2*k*K+k*(k+1)-(k+sp.Rational(1,4)))==0
assert Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)==Q(17,128)
assert Q(2)*Q(17,128)/6==Q(17,384)
assert (Q(1,2)-2*Q(1,8)-2*Q(1,32))/6==Q(1,32)
counts['symbolic_sdp_clique_and_constant_checks']=8

# All two avoidance events jointly enumerated, no independence within a block.
cases=0
for n in range(2,7):
    for k in range(n):
        for m in range(1,n-k+1):
            z=n-k-m
            witnesses=[]
            full=(1<<n)-1
            for H in combinations(range(n),k):
                hm=sum(1<<i for i in H)
                for Z in combinations([i for i in range(n) if i not in H],z):
                    witnesses.append((hm,sum(1<<i for i in Z)))
            # Full cross-product of exclusion cardinalities, representative overlap patterns.
            for a in range(n+1):
                A=(1<<a)-1
                for dd in range(n+1):
                    for shift in (0,n-dd):
                        D=((1<<dd)-1)<<shift
                        frac=Q(sum(not (H&D or Z&A) for H,Z in witnesses),len(witnesses))
                        bound=min(Q(n-z,n)**a,Q(n-k,n)**dd)
                        assert frac<=bound
                        # Square both sides to verify fractional |R|/2 exponents rationally.
                        assert frac**2 <= max(Q(n-z,n),Q(n-k,n))**((A|D).bit_count())
                        cases+=1
counts['endpoint_avoidance_cases']=cases

@lru_cache(None)
def leaves(a,b):
    return 1 if a==0 or b==0 else leaves(a-1,b)+leaves(a,b-1)
for n in range(2,51):
    for k in range(n): assert leaves(k+1,n-k)==comb(n+1,k+1)
counts['midpoint_tree_counts']=sum(range(2,51))

# Boolean polynomial arithmetic with exact rational coefficients.
def add(p,q):
    o=dict(p)
    for m,c in q.items(): o[m]=o.get(m,Q(0))+c
    return {m:c for m,c in o.items() if c}
def mul(p,q):
    o={}
    for m,c in p.items():
        for n,d in q.items(): o[m|n]=o.get(m|n,Q(0))+c*d
    return {m:c for m,c in o.items() if c}
def indicator(A,B):
    p={sum(1<<i for i in A):Q(1)}
    for j in B: p=mul(p,{0:Q(1),1<<j:Q(-1)})
    return p
rng=random.Random(20260906)
local=0
for r in range(1,5):
    s=4*r; t=Q(4*r-1,2)
    def expect(poly):
        return sum(c*Q(fall(t,m.bit_count()),fall(s,m.bit_count())) for m,c in poly.items())
    for a in range(2*r+1):
        for b in range(2*r-a+1):
            A=list(range(a)); B=list(range(a,a+b)); I=indicator(A,B)
            pi=Q(fall(t,a)*fall(s-t,b),fall(s,a+b))
            assert expect(I)==pi>=0
            d=(2*r-a-b)//2
            for trial in range(3):
                p={0:Q(rng.randrange(-3,4))}
                for _ in range(8):
                    mon=sum(1<<i for i in rng.sample(range(s),rng.randrange(d+1)))
                    p=add(p,{mon:Q(rng.randrange(-3,4))})
                assert expect(mul(I,mul(p,p)))>=0
                local+=1
counts['exact_indicator_global_square_checks']=local

# Tensor expectations of squares coupling three independent fractional blocks.
tensor=0
for r in (1,2,3):
    dims=[4*r]*3
    params=[Q(4*r-1,2),Q(4*r+1,2),Q(2*r)]
    def tensor_expect(poly):
        ans=Q(0)
        for mask,coef in poly.items():
            v=coef; off=0
            for dim,param in zip(dims,params):
                size=((mask>>off)&((1<<dim)-1)).bit_count()
                v*=Q(fall(param,size),fall(dim,size)); off+=dim
            ans+=v
        return ans
    for v in range(2*r+1):
        d=(2*r-v)//2
        for trial in range(20):
            inds=rng.sample(range(sum(dims)),v)
            split=rng.randrange(v+1)
            I=indicator(inds[:split],inds[split:])
            p={0:Q(1)}
            for _ in range(8):
                mon=sum(1<<i for i in rng.sample(range(sum(dims)),rng.randrange(d+1)))
                p=add(p,{mon:Q(rng.randrange(-3,4))})
            assert tensor_expect(mul(I,mul(p,p)))>=0
            tensor+=1
counts['exact_three_block_coupled_square_checks']=tensor
out={'status':'PASS','arithmetic':'Exact integers, rational numbers, and polynomial identities; no floating-point tests.', 'counts':counts,'limits':'Finite checks supplement, but do not prove, universal positivity or graph-lift claims.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
