"""Independent bounded Stage3 checks; no universal conclusions from enumeration."""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb, prod
from random import Random
from pathlib import Path
import json
import networkx as nx

rng = Random(10301)
counts = {}

def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0

def interval_moments(p, patterns):
    d = len(p)
    out = [Q(0)] * (d+2)
    for pattern in patterns:
        cuts = sorted({Q(0), Q(1), *[p[i] if i in pattern else 1-p[i] for i in range(d)]})
        for a,b in zip(cuts, cuts[1:]):
            u = (a+b)/2
            k = sum(u < p[i] if i in pattern else u > 1-p[i] for i in range(d))
            for j in range(d+2):
                out[j] += (b-a)*choose(k,j)/len(patterns)
    return out

def moments(p, N, fair=False):
    d = len(p)
    patterns = [set(c) for c in combinations(range(N),N//2)] if not fair else [set(i for i,z in enumerate(c) if z) for c in product((0,1),repeat=d)]
    C = interval_moments(p,[set(range(d))])
    O = interval_moments(p,patterns)
    P = [Q(0)]*(d+2)
    for state in product((0,1),repeat=d):
        mass = prod(p[i] if z else 1-p[i] for i,z in enumerate(state))
        for j in range(d+2): P[j] += mass*choose(sum(state),j)
    s=sum(p); k=s.numerator//s.denominator; theta=s-k
    V=[(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
    beta = Q(2) if fair else Q(N*(N-1),2*(N//2)*(N-N//2))
    F=[beta*C[j]+V[j]-P[j]-beta*O[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+2)]
    return C,P,O,V,beta,F

checks=0
grid=[Q(0),Q(1,5),Q(1,2),Q(4,5),Q(1)]
for N in range(2,8):
    for d in range(1,min(N,5)+1):
        for p in combinations_with_replacement(grid,d):
            C,P,O,V,beta,F=moments(p,N)
            assert min(F)>=0, (N,p,F)
            # Entire cardinality coefficients, including L=0 and affine terms.
            L=rng.choice([Q(0),Q(1,3),Q(2),Q(7)])
            coeff=[Q(rng.randrange(4)),Q(rng.randrange(4)),Q(rng.randrange(4))][:d+1]
            for j in range(3,d+1): coeff.append(coeff[-1]*L*Q(rng.randrange(5),4))
            lhs=sum(coeff[j]*(C[j]-V[j]) for j in range(d+1))
            rhs=sum(coeff[j]*((L+1)*(C[j]-P[j])+beta*(C[j]-O[j])) for j in range(d+1))
            assert lhs<=rhs
            checks+=1
counts['exact_coefficient_and_entire_cardinality_cases']=checks
p=[Q(2,5),Q(7,10),Q(24,25),Q(97,100)]
p2=[Q(2,5),Q(7,10),Q(959,1000),Q(971,1000)]
assert moments(p,4,True)[-1][3]==Q(6201,12500)
assert moments(p2,4,True)[-1][3]==Q(4961031,10000000)

checks=0
for b in range(2,8):
    for L in range(2,11):
        weights=[Q(b-1,b**(l+1)) if l<L else Q(1,b**L) for l in range(L+1)]
        M=lambda q: Q((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        mix=Q(1-M(s+1),M(s)-M(s+1))
        val=Q(0)
        for q,wq in [(s,mix),(s+1,1-mix)]:
            mean=Q(0)
            for l,w in enumerate(weights):
                r=b**(l-q+1) if l>=q else 0
                rhs=s*r+sum(b**j for j in range(1,max(l-s,0)+1))
                objective=sum(min(b**j,r) for j in range(1,l+1))
                assert rhs==objective
                mean+=w*r; val+=wq*w*objective
            assert mean==M(q)
        assert mix*M(s)+(1-mix)*M(s+1)==1
        assert val==s+Q(L-s,b**s)
        assert sum(M(q) for q in range(s+1,L+1))==Q(L-s,b**s)
        checks+=1
counts['exact_general_radix_cutoffs']=checks

checks=0
for _ in range(100):
    n=rng.randrange(2,9)
    a=[2*rng.randrange(1,30) for i in range(n)]
    A=sum(a); eps=Q(1,16*A**3)
    baseline=1+eps*A/2+eps**2*(Q(A*A,8)-sum(t*t for t in a)/Q(4))
    d0=1-eps**2*A*A/8
    potential=[eps*t+eps**2*(A*t-t*t)/2 for t in a]
    yes=False; tilted=[]
    for z in product((0,1),repeat=n):
        S=sum(t*v for t,v in zip(a,z))
        value=prod(1+eps*t*v for t,v in zip(a,z))
        rem=value-1-eps*S-eps**2*(S*S-sum(t*t*v for t,v in zip(a,z)))/2
        assert 0<=rem<=eps**2/8
        v=value-sum(t*y for t,y in zip(potential,z))
        assert v==d0+eps**2*(S-Q(A,2))**2/2+rem
        tilted.append(v)
        if 2*S==A:
            yes=True
            pair=(value+prod(1+eps*t*(1-v) for t,v in zip(a,z)))/2
            assert pair<=baseline+eps**2/8
        checks+=1
    assert min(tilted)<=d0+eps**2/8 if yes else min(tilted)>=d0+eps**2/2
counts['exact_partition_vertices']=checks

for trial in range(200):
    nv=rng.randrange(2,6); ne=rng.randrange(1,9)
    edges=[tuple(rng.sample(range(nv),2)) for _ in range(ne)]
    degree=[sum(v in e for e in edges) for v in range(nv)]
    tables=[]
    for d in degree:
        inc=sorted(rng.randrange(-8,9) for _ in range(d))
        table=[rng.randrange(-5,6)]
        for x in inc: table.append(table[-1]+x)
        tables.append(table)
    costs=[rng.randrange(-8,9) for _ in edges]
    exact=min(sum(tables[v][sum(z[i] for i,e in enumerate(edges) if v in e)] for v in range(nv))+sum(c*z for c,z in zip(costs,z)) for z in product((0,1),repeat=ne))
    G=nx.Graph()
    for i,(u,v) in enumerate(edges):
        G.add_edge(('m',i,0),('m',i,1),cost=0,mandatory=2)
        for side,node in enumerate((u,v)):
            for k in range(degree[node]):
                G.add_edge(('m',i,side),('s',node,k),cost=tables[node][k+1]-tables[node][k]+(costs[i] if side==0 else 0),mandatory=1)
    W=sum(abs(t['cost']) for *_,t in G.edges(data=True)); bonus=2*W+1
    for *_,t in G.edges(data=True): t['weight']=bonus*t['mandatory']-t['cost']
    match=nx.max_weight_matching(G)
    covered=sum(G[u][v]['mandatory'] for u,v in match)
    assert covered==2*ne
    got=sum(G[u][v]['cost'] for u,v in match)+sum(t[0] for t in tables)
    assert got==exact
counts['exact_integer_convex_matching_instances']=200

payoff_counts={}
for z in product((0,1),repeat=6):
    ab=z[0]==z[1]; bc=z[2]==z[3]; ca=z[4]==z[5]
    payoff=(int(ab and ca),int(not ab and bc),int(not bc and not ca))
    payoff_counts[payoff]=payoff_counts.get(payoff,0)+1
assert len(payoff_counts)==4 and set(payoff_counts.values())=={16}
counts['exact_parity_vertices']=64
counts['status']='PASS; finite checks supplement independent analytic review'
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
