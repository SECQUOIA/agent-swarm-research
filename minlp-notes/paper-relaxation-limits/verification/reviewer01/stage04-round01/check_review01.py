"""Independent finite exact checks; no universal theorem is inferred from them."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import json

counts = {}

def chord_lb(box, demand):
    """Exact continuous knapsack LP, by sorting affine objective slopes."""
    x = [a for a, b in box]
    remaining = demand - sum(x)
    if remaining < 0 or remaining > sum(b-a for a,b in box):
        return None
    for i in sorted(range(len(box)), key=lambda i: 1-sum(box[i])):
        extra = min(remaining, box[i][1]-box[i][0])
        x[i] += extra
        remaining -= extra
    assert remaining == 0
    return sum(a*b+(1-a-b)*v for (a,b),v in zip(box,x))

def midpoint_leaves(n, k, prefix=()):
    if prefix.count(1) == k+1 or prefix.count(0) == n-k:
        yield tuple((Q(1,2),Q(1)) if v else (Q(0),Q(1,2)) for v in prefix) + ((Q(0),Q(1)),)*(n-len(prefix))
    else:
        assert len(prefix) < n
        yield from midpoint_leaves(n,k,prefix+(0,))
        yield from midpoint_leaves(n,k,prefix+(1,))

cnt = 0
for n in range(2,10):
    for k in range(n):
        leaves = list(midpoint_leaves(n,k))
        assert len(leaves) == comb(n+1,k+1)
        for box in leaves:
            value = chord_lb(box,Q(2*k+1,2))
            assert value is None or value >= Q(1,4)
            cnt += 1
counts['exact_midpoint_leaf_LPs_n2_to9'] = cnt

cnt = 0
for n in range(2,8):
    for k in range(n):
        for alpha in (Q(1,7),Q(1,4),Q(2,5)):
            intervals = ((Q(0),alpha),(alpha,1-alpha),(1-alpha,Q(1)))
            leaves=[]
            # First middle interval terminates; all-low/high strings reach depth n.
            for i in range(n):
                for pre in product((0,2),repeat=i):
                    leaves.append(tuple(intervals[v] for v in pre)+(intervals[1],)+((Q(0),Q(1)),)*(n-i-1))
            for pre in product((0,2),repeat=n):
                leaves.append(tuple(intervals[v] for v in pre))
            assert len(leaves) == 2**(n+1)-1
            assert 2*len(leaves)-1 == 2**(n+2)-3
            for box in leaves:
                value=chord_lb(box,Q(2*k+1,2))
                assert value is None or value >= alpha*(1-alpha)
                cnt += 1
counts['positive_tolerance_leaf_LPs_n2_to7'] = cnt

# Enumerate vertices of tolerance slabs: all Boolean points inside the slab,
# and intersections of its two sum faces with cube edges.
cnt=0
for n in range(2,8):
    for k in range(n):
        for delta in (Q(0),Q(1,5),Q(49,100),Q(1,2),Q(3,4)):
            K=Q(2*k+1,2)
            vertices=set()
            for x in product((Q(0),Q(1)),repeat=n):
                if abs(sum(x)-K)<=delta:
                    vertices.add(x)
            for i in range(n):
                for other in product((Q(0),Q(1)),repeat=n-1):
                    for total in (K-delta,K+delta):
                        v=total-sum(other)
                        if 0<=v<=1:
                            vertices.add(other[:i]+(v,)+other[i:])
            optimum=min(sum(v*(1-v) for v in x) for x in vertices)
            expected=Q(1,4)-delta**2 if delta<Q(1,2) else Q(0)
            assert optimum == expected
            cnt+=len(vertices)
counts['slab_vertices_n2_to7'] = cnt

# All endpoint exclusion patterns A,D through n=5, including empty classes.
# Square probabilities to compare half-integer exponents without floating point.
cnt=0
for n in range(2,6):
    positions=set(range(n))
    for k in range(n):
        for m in range(1,n-k+1):
            z=n-k-m
            witnesses=[]
            for H in combinations(range(n),k):
                for Z in combinations(sorted(positions-set(H)),z):
                    witnesses.append((set(H),set(Z)))
            for pattern in product(range(4),repeat=n):
                A={i for i,v in enumerate(pattern) if v&1}
                D={i for i,v in enumerate(pattern) if v&2}
                allowed=sum(not(H&D or Z&A) for H,Z in witnesses)
                probability=Q(allowed,len(witnesses))
                assert probability<=min(Q(n-z,n)**len(A),Q(n-k,n)**len(D))
                assert probability**2<=max(Q(n-z,n)**len(A|D),Q(n-k,n)**len(A|D))
                cnt+=1
counts['endpoint_avoidance_patterns_n2_to5'] = cnt

# Independently form complete SDP matrices on representative asymmetric boxes.
cnt=0
for k,m,z in ((1,1,1),(2,3,2),(3,2,3),(4,1,3)):
    n=k+m+z; p=Q(1,2*m); w=[Q(1)]*k+[p]*m+[Q(0)]*z
    K=Q(2*k+1,2)
    for num in range(min(k,z)):
        for tup in combinations(range(n),num):
            R=set(tup); U=set(range(n))-R; s=len(U); t=K-sum(w[i] for i in R)
            c=t/s; d=t*(t-1)/(s*(s-1))
            mu=[w[i] if i in R else c for i in range(n)]
            X=[[mu[i]*mu[j] if i in R or j in R else (c if i==j else d) for j in range(n)] for i in range(n)]
            for degenerate in (False,True):
                box=[((w[i],w[i]) if degenerate else (w[i]/2,(1+w[i])/2)) if i in R else (Q(0),Q(1)) for i in range(n)]
                assert sum(mu)==K
                for i in range(n):
                    assert sum(X[i])==K*mu[i]
                    for j in range(n):
                        covariance=X[i][j]-mu[i]*mu[j]
                        expected=Q(0) if i in R or j in R else (c-d)*((i==j)-Q(1,s))
                        assert covariance==expected and c-d>=0
                        a,b=box[i]; aj,bj=box[j]
                        assert min(X[i][j]-a*mu[j]-aj*mu[i]+a*aj,
                                   bj*mu[i]-X[i][j]-a*bj+a*mu[j],
                                   b*mu[j]-X[i][j]-b*aj+aj*mu[i],
                                   b*bj-b*mu[j]-bj*mu[i]+X[i][j])>=0
                assert sum(mu[i]-X[i][i] for i in range(n))==sum(w[i]*(1-w[i]) for i in R)
                cnt+=1
counts['exact_SDP_constructions_including_degenerate_boxes']=cnt

def falling(v,a):
    return prod((v-j for j in range(a)), start=Q(1))

cnt=0
for d in range(1,7):
    for s in range(max(2*d,4*d-2),4*d+3):
        for t in (Q(2*d-1),Q(4*d-1,2),Q(s-(2*d-1))):
            if min(t,s-t)<2*d-1: continue
            coeff=[falling(t,2*d-j)*falling(s-t,j)/falling(s,2*d) for j in range(d+1)]
            assert min(coeff)>=0
            for ell in range(d+1):
                assert sum(coeff[j]*comb(ell,j) for j in range(ell+1))==falling(t,2*d-ell)/falling(s,2*d-ell)
                cnt+=1
counts['Gram_entries_including_zero_coefficient_boundaries']=cnt
assert Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)==Q(17,128)
assert Q(2)*Q(17,128)/6==Q(17,384)

out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps({'arithmetic':'exact fractions only','checks':counts,'status':'PASS','limits':'Finite instances corroborate identities and constants; universal graph-lift, positivity and tensor proofs were reviewed analytically.'},indent=2)+'\n')
print(out.read_text())
