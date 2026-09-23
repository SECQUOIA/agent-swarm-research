from fractions import Fraction as F
from itertools import product, combinations
import random, json
rng=random.Random(3505)
N=[(1,0),(0,1),(1,1)]
def vertices(bounds):
    lines=[(a,b,v) for (a,b),(l,u) in zip(N,bounds) for v in (l,u)]
    out=set()
    for (a,b,c),(d,e,f) in combinations(lines,2):
        det=a*e-b*d
        if det:
            p=(F(c*e-b*f,det),F(a*f-c*d,det))
            if feasible(p,bounds): out.add(p)
    return out

def feasible(p,b): return all(l<=a*p[0]+c*p[1]<=u for (a,c),(l,u) in zip(N,b))
def supports(b):
    (ls,us),(lt,ut),(lh,uh)=b
    return [(max(ls,lh-ut),min(us,uh-lt)),(max(lt,lh-us),min(ut,uh-ls)),(max(lh,ls+lt),min(uh,us+ut))]
def nonempty(b):
    (ls,us),(lt,ut),(lh,uh)=b
    return all(l<=u for l,u in b) and ls+lt<=uh and lh<=us+ut

def choose(b):
    (ls,us),(lt,ut),(lh,uh)=b
    s=max(ls,lh-ut)
    return (s,max(lt,lh-s))
def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def hull(points):
    p=sorted(set(points))
    if len(p)<=1:return p
    def half(seq):
        h=[]
        for q in seq:
            while len(h)>=2 and cross(h[-2],h[-1],q)<=0:h.pop()
            h.append(q)
        return h
    return half(p)[:-1]+half(p[::-1])[:-1]
ints=list(combinations([-2,-1,0,1,2],2))+[(i,i) for i in [-2,-1,0,1,2]]
domains=[]
for b in product(ints,repeat=3):
    v=vertices(b)
    assert bool(v)==nonempty(b)
    if not v:continue
    assert feasible(choose(b),b)
    sp=supports(b)
    for (a,c),(l,u) in zip(N,sp):
        assert l==min(a*p[0]+c*p[1] for p in v)
        assert u==max(a*p[0]+c*p[1] for p in v)
    domains.append((b,v))
for _ in range(400):
    b,v=rng.choice(domains); c,w=rng.choice(domains)
    summed=[(lo+lc,up+uc) for (lo,up),(lc,uc) in zip(supports(b),supports(c))]
    actual=hull([(p[0]+q[0],p[1]+q[1]) for p in v for q in w])
    predicted=hull(vertices(summed))
    assert actual==predicted
for _ in range(400):
    fam=[rng.choice(domains) for __ in range(rng.randint(1,9))]
    picks=[rng.choice(sorted(v)) for b,v in fam]
    aggregate=tuple(sum(p[i] for p in picks) for i in (0,1))
    remaining=aggregate
    recovered=[]
    for i,(b,v) in enumerate(fam):
        suffix=[supports(bb) for bb,vv in fam[i+1:]]
        rvals=[remaining[0],remaining[1],sum(remaining)]
        inter=[(max(l,rvals[k]-sum(s[k][1] for s in suffix)),min(u,rvals[k]-sum(s[k][0] for s in suffix))) for k,(l,u) in enumerate(b)]
        assert nonempty(inter)
        point=choose(inter)
        assert feasible(point,b)
        recovered.append(point)
        remaining=tuple(remaining[k]-point[k] for k in (0,1))
    assert remaining==(0,0)
# Exhaustive integer matrices for each random interval family give an independent
# discrete membership test; integral transportation vertices make it exact here.
for _ in range(500):
    k=rng.randint(2,4); d=rng.randint(1,3)
    colbounds=[[(rng.randint(-1,0),rng.randint(0,1)) for i in range(k)] for j in range(d)]
    columns=[[v for v in product(*[range(l,u+1) for l,u in b]) if sum(v)==0] for b in colbounds]
    sums={(0,)*k}
    for col in columns:sums={tuple(a[i]+b[i] for i in range(k)) for a in sums for b in col}
    delta=tuple(rng.randint(-3,3) for i in range(k-1))
    delta=delta+(-sum(delta),)
    holds=True
    for mask in range(1<<k):
        ids=[i for i in range(k) if (mask>>i)&1]
        rhs=sum(min(sum(b[i][1] for i in ids),-sum(b[i][0] for i in range(k) if i not in ids)) for b in colbounds)
        holds &= sum(delta[i] for i in ids)<=rhs
    assert holds==(delta in sums)
print(json.dumps({'bounded_interval_triples_checked':len(ints)**3,'nonempty_domains':len(domains),'exact_minkowski_pairs':400,'exact_recoveries':400,'subset_vs_exhaustive_integer_matrix_checks':500,'status':'PASS'},indent=2))
