"""Independent finite exact checks. No floating point and no universal proof claim."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from functools import lru_cache
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent

def ff(t,a):
    q=F(1)
    for j in range(a): q*=t-j
    return q

def subsets(n,d):
    return [sum(1<<i for i in c) for a in range(d+1) for c in combinations(range(n),a)]

def psd_rank(A):
    A=[row[:] for row in A]; rank=0
    for k in range(len(A)):
        pivot=A[k][k]
        assert pivot>=0, (k,pivot)
        if not pivot:
            assert all(A[k][j]==0 for j in range(k+1,len(A))), k
            continue
        rank+=1
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                A[i][j]-=A[i][k]*A[k][j]/pivot
                A[j][i]=A[i][j]
    return rank

# Falling-factorial entry identity, rational samples including zeros at boundaries.
gram=0
for d in range(1,8):
    for s in [4*d-2 if d>1 else 2,4*d+3]:
        for t in [F(2*d-1),F(s-(2*d-1)),F(s,2)]:
            for ell in range(d+1):
                rhs=sum(F(comb(ell,j))*ff(t,2*d-j)*ff(s-t,j) for j in range(ell+1))/ff(s,2*d)
                assert rhs==ff(t,2*d-ell)/ff(s,2*d-ell)
                gram+=1

# Two fractional blocks, each seven variables, with cardinality 7/2.
# Boolean reduction handles all repeated powers in a square multiplier.
@lru_cache(None)
def E(mask):
    a=(mask&127).bit_count(); b=(mask>>7).bit_count()
    return ff(F(7,2),a)/ff(7,a)*ff(F(7,2),b)/ff(7,b)

def local(mask,A,B):
    return sum((-1)**len(c)*E(mask|A|sum(1<<i for i in c))
               for j in range(len(B)+1) for c in combinations(B,j))

basis=subsets(14,2)
rank=psd_rank([[E(a|b) for b in basis] for a in basis])
local_ranks={}
linear=subsets(14,1)
for name,A,B in [('lower',1,()),('cross',1,(7,)),('same_block',1,(1,)),('upper_pair',0,(0,7)),('repeated_lower',1,()),('conflicting',1,(0,))]:
    local_ranks[name]=psd_rank([[local(a|b,A,B) for b in linear] for a in linear])

# Every global monomial multiplier through degree three after Boolean reduction.
equalities=0
for mask in subsets(14,3):
    for start in [0,7]:
        assert sum(E(mask|(1<<i)) for i in range(start,start+7))==F(7,2)*E(mask)
        equalities+=1

# All distinct assignment indicators through degree four; constants in squares.
indicators=0
for inds in [c for a in range(5) for c in combinations(range(14),a)]:
    for signs in product([0,1],repeat=len(inds)):
        A=sum(1<<i for i,x in zip(inds,signs) if x)
        B=tuple(i for i,x in zip(inds,signs) if not x)
        assert local(0,A,B)>=0
        indicators+=1

# Exact negative-moment obstruction strictly outside the noninteger range.
negative=0
for r in range(1,8):
    s=4*r+1
    for k in range(2*r-1):
        t=F(2*k+1,2); a=k+2
        assert a<=2*r and ff(t,a)/ff(s,a)<0
        negative+=1

# Complete avoidance checks for all endpoint-exclusion patterns, small asymmetric n.
avoidance=0
for n,k,m in [(4,1,1),(5,1,2),(5,2,1),(6,2,2)]:
    z=n-k-m
    witnesses=[]
    for H in combinations(range(n),k):
        for M in combinations([i for i in range(n) if i not in H],m):
            witnesses.append((sum(1<<i for i in H),sum(1<<i for i in range(n) if i not in H and i not in M)))
    for A in range(1<<n):
        for D in range(1<<n):
            frac=F(sum(not(Z&A or H&D) for H,Z in witnesses),len(witnesses))
            assert frac<=min(F(n-z,n)**A.bit_count(),F(n-k,n)**D.bit_count())
            avoidance+=1

# Exact relative exponent.
tau=F(1,4)-F(1,32)*(F(5,2)+F(1,4))-F(1,32)
assert tau==F(17,128) and F(2,6)*tau==F(17,384)
result=dict(arithmetic='exact fractions',gram_entry_samples=gram,
    global_moment_matrix_size=len(basis),global_moment_rank=rank,
    localizer_matrix_sizes=len(linear),localizer_ranks=local_ranks,
    global_balance_products=equalities,assignment_indicators=indicators,
    negative_boundary_products=negative,endpoint_avoidance_patterns=avoidance,
    relative_tau=str(tau),relative_exponent_per_original_variable=str(F(2,6)*tau),
    limitation='Finite checks supplement the separately reconstructed proofs. They do not prove universal positivity or arbitrary graph-lift validity.')
(OUT/'check_exact.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
