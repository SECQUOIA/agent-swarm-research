"""Independent exact finite/symbolic checks, not an implementation of the algorithms."""
from itertools import product
from random import Random
import json
import sympy as s

rng = Random(202609091)
results = {}

# Compare every connected-cut feasibility test with enumeration of integral
# signed flows. Incidence total unimodularity makes these integer instances
# also checks of real feasibility. Check box rank and signed greedy support.
for trial in range(180):
    n = rng.randrange(2, 6)
    edges = [(i, i+1) if rng.randrange(2) else (i+1, i) for i in range(n-1)]
    if n > 2 and trial % 2:
        edges.append((n-1, 0))
    lo = [rng.randrange(-2, 2) for _ in edges]
    hi = [x+rng.randrange(3) for x in lo]
    alpha = [rng.randrange(-4, 3) for _ in range(n)]
    beta = [a+rng.randrange(6) for a in alpha]
    masks = range(1 << n)
    sets = [{i for i in range(n) if m >> i & 1} for m in masks]
    def div(w):
        d = [0]*n
        for (a,b),x in zip(edges,w): d[a] += x; d[b] -= x
        return d
    divergences = [div(w) for w in product(*(range(a,b+1) for a,b in zip(lo,hi)))]
    feasible = [d for d in divergences if all(a <= v <= b for a,v,b in zip(alpha,d,beta))]
    def cut(S):
        return sum(h for (a,b),h in zip(edges,hi) if a in S and b not in S)-sum(l for (a,b),l in zip(edges,lo) if a not in S and b in S)
    def lowercut(S):
        return sum(l for (a,b),l in zip(edges,lo) if a in S and b not in S)-sum(h for (a,b),h in zip(edges,hi) if a not in S and b in S)
    def connected(S):
        if not S: return False
        seen = {next(iter(S))}
        while True:
            new = seen | {b for a,b in edges if a in seen and b in S} | {a for a,b in edges if b in seen and a in S}
            if seen == new: return seen == S
            seen = new
    ok = all(sum(alpha[i] for i in S) <= cut(S) and sum(beta[i] for i in S) >= lowercut(S) for S in sets if connected(S))
    assert ok == bool(feasible), trial
    if feasible:
        g = {tuple(sorted(S)): min(cut(T)+sum(beta[i] for i in S-T)-sum(alpha[i] for i in T-S) for T in sets) for S in sets}
        assert g[()] == g[tuple(range(n))] == 0
        assert all(g[tuple(sorted(S))] == max(sum(d[i] for i in S) for d in feasible) for S in sets)
        cost = [rng.randrange(-4,5) for _ in range(n)]
        order = sorted(range(n),key=lambda i:-cost[i]); dstar=[0]*n; prefix=set(); previous=0
        for i in order:
            prefix.add(i); current=g[tuple(sorted(prefix))]; dstar[i]=current-previous; previous=current
        assert dstar in feasible
        assert sum(c*d for c,d in zip(cost,dstar)) == max(sum(c*x for c,x in zip(cost,d)) for d in feasible)
results['signed_cuts_box_rank_greedy'] = '180 exact path/cycle instances passed'

for trial in range(250):
    n=rng.randrange(1,10); unary=[(rng.randrange(-5,6),rng.randrange(-5,6)) for _ in range(n)]
    a=[rng.randrange(5) for _ in range(n-1)]; b=[rng.randrange(5) for _ in range(n-1)]
    e0=unary[0][0]; D=unary[0][1]-unary[0][0]; P=D; Z=0
    for i in range(1,n):
        e0 += unary[i][0]+min(0,D+b[i-1])
        u=unary[i][1]-unary[i][0]
        Z=min(a[i-1]-P,max(-b[i-1]-P,Z)); P+=u
        D=u+min(a[i-1],max(-b[i-1],D))
        assert D == P+Z
    brute=min(sum(unary[i][x[i]] for i in range(n))+sum(a[i-1] if (x[i-1],x[i])==(0,1) else b[i-1] if (x[i-1],x[i])==(1,0) else 0 for i in range(1,n)) for x in product((0,1),repeat=n))
    assert e0+min(0,D)==brute
results['clamp'] = '250 exact signed-unary path energies passed'

q,C1,C2,R,L,U,w1,w2,bj,Bj,v,W0,W1=s.symbols('q C1 C2 R L U w1 w2 bj Bj v W0 W1')
g1,g2=C1-q,C2-q
outlet=g1*(R-g2*L)/(C1-C2)
assert s.factor(outlet/g1+(R-outlet)/g2-L)==0
W0expr=q*bj*(Bj-1)+q*(1-q)*v
W1expr=bj*(Bj-q)-W0expr
assert s.factor(-W0expr/q+W1expr/(1-q)-(bj-v))==0
h1,h2,Bh,beta1,beta2=s.symbols('h1 h2 Bh beta1 beta2')
# The residual identity holds for arbitrary projected qualities gamma.
aa=(h1-q)*g2-(h2-q)*g1
ff=g1*(bj*(Bh-q)*g2-(h2-q)*R)
res=(h1-q)*w1/g1+(h2-q)*(R-w1)/g2-bj*(Bh-q)
assert s.factor(res*g1*g2-(aa*w1-ff))==0
results['symbolic'] = 'outlet inversion, two-vector identity, residual-vector identity passed'
print(json.dumps(results,indent=2))
