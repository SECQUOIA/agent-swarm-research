"""Independent exact supplemental checks. Uses only the Python standard library.
Boolean reduction uses bitmask polynomials; finite checks do not prove the theorems.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

out = Path(__file__).parent
checks = {}
def fall(t, k):
    ans = Q(1)
    for j in range(k): ans *= t-j
    return ans

def add(*ps):
    ans = {}
    for p in ps:
        for m,c in p.items(): ans[m] = ans.get(m,Q(0))+c
    return {m:c for m,c in ans.items() if c}
def scale(p,c): return {m:v*c for m,v in p.items() if v*c}
def mul(p,q):
    ans={}
    for m,a in p.items():
        for n,b in q.items(): ans[m|n]=ans.get(m|n,Q(0))+a*b
    return {m:c for m,c in ans.items() if c}
one={0:Q(1)}
def mon(i): return {1<<i:Q(1)}
def expectation(blocks):
    cache={}
    def moment(mask):
        if mask not in cache:
            ans=Q(1); offset=0
            for s,t in blocks:
                k=((mask>>offset)&((1<<s)-1)).bit_count()
                ans *= fall(t,k)/fall(s,k); offset+=s
            cache[mask]=ans
        return cache[mask]
    return lambda p:sum((c*moment(m) for m,c in p.items()),Q(0))

def psd_exact(M):
    # Symmetric elimination is congruence, including singular zero-pivot rows.
    A=[row[:] for row in M]; rank=0
    for k in range(len(A)):
        pivot=A[k][k]
        assert pivot>=0,(k,pivot)
        if pivot==0:
            assert all(A[k][j]==0 for j in range(k,len(A)))
            continue
        rank+=1
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                A[i][j]-=A[i][k]*A[k][j]/pivot; A[j][i]=A[i][j]
    return rank

# Gram entry identities including zero numerator endpoints.
c=0
for d in range(1,7):
    for s in (4*d-2,4*d,4*d+3):
        if s<2*d: continue
        for t in (Q(2*d-1),Q(4*d-1,2),Q(s-2*d+1)):
            for ell in range(d+1):
                rhs=sum((Q(comb(ell,j))*fall(t,2*d-j)*fall(s-t,j) for j in range(ell+1)),Q(0))/fall(s,2*d)
                assert rhs==fall(t,2*d-ell)/fall(s,2*d-ell)
                c+=1
checks['gram_entries_exact']=c

# Sharp failure of this full-preordering functional below the permitted range.
c=0
for r in range(1,9):
    s=4*r
    for a in range(2*r-1):
        t=Q(2*a+1,2); degree=a+2
        assert degree<=2*r and fall(t,degree)/fall(s,degree)<0
        c+=1
checks['negative_slack_boundary_cases']=c

# All globally coupled degree-two squares for two noninteger blocks, order 2.
blocks=[(7,Q(7,2)),(7,Q(7,2))]; n=14; E=expectation(blocks)
basis=[0]+[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
M=[[E({i|j:Q(1)}) for j in basis] for i in basis]
checks['global_order2_psd']={'dimension':len(M),'exact_rank':psd_exact(M)}

# Degree-three balance multipliers, including multipliers mixing both blocks.
basis3=basis+[(1<<i)|(1<<j)|(1<<k) for i,j,k in combinations(range(n),3)]
c=0
for b in range(2):
    e=add(scale(one,-Q(7,2)),*(mon(i) for i in range(7*b,7*(b+1))))
    for mask in basis3:
        assert E(mul(e,{mask:Q(1)}))==0; c+=1
checks['global_balance_products_exact']=c

# Every pair of endpoint slacks (including repetition/conflict), full linear
# global square matrix. Coordinate symmetry permits four representative pairs.
c=0
for i,j in [(0,0),(0,1),(0,7),(7,8)]:
    for si,sj in product((0,1),repeat=2):
        g=mul(mon(i) if si else add(one,scale(mon(i),-1)),mon(j) if sj else add(one,scale(mon(j),-1)))
        B=[0]+[1<<k for k in range(n)]
        psd_exact([[E(mul(g,{a|b:Q(1)})) for b in B] for a in B]); c+=1
checks['representative_global_localizer_matrices_exact']=c

# Endpoint graph maps for arbitrary finite functions: discontinuous step,
# reciprocal with a finite assigned value at zero, high powers, and penalties.
# Their interpolants are affine; local factor values are tested on both actual
# graph endpoints and at a fixed middle witness, never at an interpolated mean.
c=0
for psi in (lambda x:Q(7) if x==0 else 1/x,lambda x:Q(3) if x<Q(1,3) else Q(-2),lambda x:x**101,lambda x:x*(1-x)):
    for i in (0,7):
        y=add(scale(one,psi(Q(0))),scale(mon(i),psi(Q(1))-psi(Q(0))))
        for endpoint in (0,1):
            value=sum(v*(endpoint if m else 1) for m,v in y.items())
            assert value==psi(Q(endpoint)); c+=1
        # These affine bounds are valid on restricted graphs with S_i={0,1}. Full global
        # linear multipliers include every coordinate from both blocks.
        low=min(psi(Q(0)),psi(Q(1))); high=max(psi(Q(0)),psi(Q(1)))
        for g in (add(y,scale(one,-low)),add(scale(one,high),scale(y,-1))):
            B=[0]+[1<<k for k in range(n)]
            psd_exact([[E(mul(g,{a|b:Q(1)})) for b in B] for a in B]); c+=1
        p=Q(1,16)
        assert isinstance(psi(p),Q); c+=1
checks['local_graph_endpoint_and_psd_checks']=c

# Available full-graph identities for discontinuous and nonlinear functions,
# and a written objective coupling graph identities across the two blocks.
c=0
identities=[]
for i in (0,7):
    x=mon(i)
    # Step function values 3,-2: (y-3)(y+2)=0 on its whole graph.
    step=add(scale(one,3),scale(x,-5))
    hstep=mul(add(step,scale(one,-3)),add(step,scale(one,2)))
    # Reciprocal with finite value at zero: x(x*y-1)=0 everywhere.
    reciprocal=add(scale(one,7),scale(x,-6))
    hrec=mul(x,add(mul(x,reciprocal),scale(one,-1)))
    # Penalty lift: y-x+x^2=0; its endpoint interpolant y is zero.
    hpen=add(scale(x,-1),mul(x,x))
    for h,degree in ((hstep,2),(hrec,3),(hpen,2)):
        assert not h
        for mask in basis if degree==2 else [0]+[1<<k for k in range(n)]:
            assert E(mul(h,{mask:Q(1)}))==0; c+=1
        identities.append(h)
objective=add(*(mon(i) for i in range(n)),mul(identities[0],mon(7)),mul(identities[0],identities[3]))
assert E(objective)==Q(7)
checks['available_lifted_graph_identity_products_exact']=c
checks['coupled_written_lifted_objective_exact']='7 = 2K'

# Exact squared-index symmetry exclusion and relative arithmetic.
c=0
for t in range(1,6):
    ell=3*t
    for G in range(1,7):
        differences=[tuple(((b*ell+i+1)**2-(b*ell+i)**2) for i in range(1,ell)) for b in range(G)]
        assert len(set(differences))==G; c+=1
checks['squared_index_block_distinctions']=c
tau=Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)
assert tau==Q(17,128) and Q(2)*tau/Q(6)==Q(17,384)
checks['relative_tau']=str(tau); checks['relative_exponent_per_original_coordinate']=str(Q(2)*tau/Q(6))

# Enumerate all nonempty endpoint-exclusion patterns for asymmetric witnesses.
c=0
for n,k,m in [(4,1,1),(5,2,1),(6,1,2),(6,2,2)]:
    z=n-k-m
    witnesses=[]
    for H in combinations(range(n),k):
        for M in combinations([i for i in range(n) if i not in H],m):
            witnesses.append((set(H),set(range(n))-set(H)-set(M)))
    for states in product(range(4),repeat=n):
        A={i for i,v in enumerate(states) if v&1}; D={i for i,v in enumerate(states) if v&2}
        count=sum(not(H&D) and not(Z&A) for H,Z in witnesses)
        frac=Q(count,len(witnesses))
        assert frac<=min(Q(n-z,n)**len(A),Q(n-k,n)**len(D)); c+=1
checks['asymmetric_endpoint_avoidance_patterns_exact']=c
(out/'check_review10.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
