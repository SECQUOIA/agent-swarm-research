"""Independent finite checks; no external solver and no universal inference."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, prod
import json
import random

rng = random.Random(902603)

def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0

def moments(p, ambient, fair=False):
    d = len(p)
    C = [F(sum(min((p[i] for i in s), default=1)
               for s in combinations(range(d), j))) for j in range(d+2)]
    P = [sum((prod(p[i] for i in s) for s in combinations(range(d), j)), F(0))
         for j in range(d+2)]
    k = int(sum(p)); theta = sum(p)-k
    V = [(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
    coins = list(product((0,1), repeat=ambient)) if fair else [
        tuple(int(i in s) for i in range(ambient))
        for s in combinations(range(ambient), ambient//2)]
    O = [F(0)]*(d+2)
    for coin in coins:
        ends = sorted({F(0), F(1), *[p[i] if coin[i] else 1-p[i] for i in range(d)]})
        for lo, hi in zip(ends, ends[1:]):
            u = (lo+hi)/2
            count = sum(u<p[i] if coin[i] else u>1-p[i] for i in range(d))
            for j in range(d+2):
                O[j] += (hi-lo)*choose(count,j)/len(coins)
    beta = F(2) if fair else F(ambient*(ambient-1), 2*(ambient//2)*(ambient-ambient//2))
    defects = [beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0)
               for j in range(d+2)]
    return C,P,V,O,beta,defects

coefficient_cases = 0
regularity_cases = 0
for N in range(2,8):
    for trial in range(16):
        d = rng.randrange(0,N+1)
        p = [F(rng.randrange(13),12) for _ in range(d)]
        C,P,V,O,beta,defects = moments(p,N)
        assert min(defects) >= 0
        coefficient_cases += 1
        for L in [F(0),F(1,3),F(3)]:
            a=[F(0)]*(d+2)
            if d>=2:
                a[2]=F(1)
            for j in range(3,d+1):
                a[j]=a[j-1]*L*F(rng.randrange(5),4)
            dot=lambda v:sum(a[j]*v[j] for j in range(d+2))
            assert dot(C)-dot(V) <= (L+1)*(dot(C)-dot(P))+beta*(dot(C)-dot(O))
            regularity_cases += 1

first = moments([F(2,5),F(7,10),F(24,25),F(97,100)],4,True)[-1][3]
second = moments([F(2,5),F(7,10),F(959,1000),F(971,1000)],4,True)[-1][3]
assert first==F(6201,12500) and second-first==F(231,10000000)

radix_cases=0
for b in range(2,11):
    for L in range(2,25):
        w=[F(b-1,b**(l+1)) for l in range(L)]+[F(1,b**L)]
        assert sum(w)==1
        M=lambda q:F((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        mix=(1-M(s+1))/(M(s)-M(s+1))
        objectives=[]
        for q in (s,s+1):
            counts=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
            assert sum(w[l]*counts[l] for l in range(L+1))==M(q)
            obj=F(0)
            for l,R in enumerate(counts):
                value=sum(min(b**j,R) for j in range(1,l+1))
                assert value==s*R+sum(b**j for j in range(1,l-s+1))
                obj+=w[l]*value
            objectives.append(obj)
        assert mix*objectives[0]+(1-mix)*objectives[1]==s+F(L-s,b**s)
        assert sum(M(q) for q in range(s+1,L+1))==F(L-s,b**s)
        radix_cases+=1

payoff_counts={}
for ab1,ab2,bc1,bc2,ca1,ca2 in product((0,1),repeat=6):
    payoff=(int(ab1==ab2 and ca1==ca2),int(ab1!=ab2 and bc1==bc2),int(bc1!=bc2 and ca1!=ca2))
    assert sum(payoff)<=1
    payoff_counts[str(payoff)]=payoff_counts.get(str(payoff),0)+1
assert sorted(payoff_counts.values())==[16]*4

hardness_instances=0
hardness_vertices=0
for n in range(2,8):
    for trial in range(10):
        a=[2*rng.randrange(1,15) for _ in range(n)]
        A=sum(a); eps=F(1,16*A**3)
        pi=[eps*t+eps**2*F(A*t-t*t,2) for t in a]
        d0=1-eps**2*F(A*A,8)
        vals=[]
        sums=[]
        for z in product((0,1),repeat=n):
            S=sum(t*x for t,x in zip(a,z))
            cost=prod(1+eps*t*x for t,x in zip(a,z))
            rem=cost-1-eps*S-eps**2*F(S*S-sum(t*t*x for t,x in zip(a,z)),2)
            assert 0<=rem<=eps**2/8
            tilted=cost-sum(v*x for v,x in zip(pi,z))
            assert tilted==d0+eps**2*F((S-A//2)**2,2)+rem
            vals.append(tilted);sums.append(S)
            hardness_vertices+=1
        if A//2 in sums:
            assert min(vals)+eps**2/32 < d0+eps**2/4
        else:
            assert min(vals)-eps**2/32 > d0+eps**2/4
        hardness_instances+=1

print(json.dumps(dict(arithmetic='exact fractions', coefficient_cases=coefficient_cases,
    regularity_cases=regularity_cases, radix_cases=radix_cases, parity_counts=payoff_counts,
    schur_counterexample_delta=str(second-first), hardness_instances=hardness_instances,
    hardness_vertices=hardness_vertices, result='PASS'),indent=2))
