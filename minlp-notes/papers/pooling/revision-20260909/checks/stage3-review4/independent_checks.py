"""Independent exact small-instance checks; not a proof or full algorithm implementation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sympy as s

rng = random.Random(2026090904)
results = {}

# Exhaustive signed integral flows test the arbitrary-graph box rank and greedy
# formula. Integer network bounds ensure integral extrema, so no LP tolerance
# is involved in these checks.
for trial in range(120):
    n = rng.randint(2, 5)
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    rng.shuffle(edges)
    edges = [e if rng.randrange(2) else e[::-1] for e in edges[:rng.randint(1, min(5, len(edges)))]]
    lower = [rng.randint(-2, 0) for _ in edges]
    upper = [x + rng.randint(0, 2) for x in lower]
    def divergence(w):
        d = [0]*n
        for (i,j),x in zip(edges,w): d[i] += x; d[j] -= x
        return tuple(d)
    witness = divergence([rng.randint(a,b) for a,b in zip(lower,upper)])
    alpha = [x-rng.randint(0,2) for x in witness]
    beta = [x+rng.randint(0,2) for x in witness]
    divergences = {divergence(w) for w in product(*(range(a,b+1) for a,b in zip(lower,upper)))}
    feasible = [d for d in divergences if all(a<=x<=b for a,x,b in zip(alpha,d,beta))]
    subsets = range(1<<n)
    def total(v,mask): return sum(v[i] for i in range(n) if mask>>i&1)
    def cut(mask):
        return sum(u for (i,j),u in zip(edges,upper) if mask>>i&1 and not mask>>j&1)-sum(l for (i,j),l in zip(edges,lower) if not mask>>i&1 and mask>>j&1)
    g = [min(cut(t)+total(beta,mask&~t)-total(alpha,t&~mask) for t in subsets) for mask in subsets]
    assert g[0] == g[-1] == 0
    assert all(g[a]+g[b]>=g[a|b]+g[a&b] for a in subsets for b in subsets)
    assert all(g[a] == max(total(d,a) for d in feasible) for a in subsets)
    costs = [rng.randint(-3,3) for _ in range(n)]
    order = sorted(range(n), key=lambda i:-costs[i])
    mask = 0; greedy = [0]*n
    for i in order:
        nxt = mask | 1<<i; greedy[i] = g[nxt]-g[mask]; mask = nxt
    assert tuple(greedy) in feasible
    assert sum(c*x for c,x in zip(costs,greedy)) == max(sum(c*x for c,x in zip(costs,d)) for d in feasible)
results['box_rank_and_greedy_exact_instances'] = 120

# Exact clamp recurrence against complete binary enumeration, with signed
# unary values, zero penalties, and cycles handled by fixed first label.
for trial in range(160):
    n = rng.randint(2,8)
    U = [[F(rng.randint(-9,9),rng.randint(1,4)) for _ in range(2)] for i in range(n)]
    a = [F(rng.randint(0,7),rng.randint(1,4)) for i in range(n)]
    b = [F(rng.randint(0,7),rng.randint(1,4)) for i in range(n)]
    def path_min(V):
        E0 = V[0][0]; D = V[0][1]-V[0][0]; P = D; Z = F(0)
        endpoints = [F(0)]
        for i in range(1,n):
            E0 += V[i][0]+min(0,D+b[i])
            lo,hi = -b[i]-P,a[i]-P
            endpoints += [lo,hi]
            Z = min(hi,max(lo,Z))
            P += V[i][1]-V[i][0]; D = P+Z
            assert Z in endpoints
        return E0+min(0,D)
    def energy(x,cycle):
        val = sum(U[i][x[i]] for i in range(n))
        for i in range(1,n):
            val += a[i] if (x[i-1],x[i])==(0,1) else b[i] if (x[i-1],x[i])==(1,0) else 0
        if cycle: val += a[0] if (x[-1],x[0])==(0,1) else b[0] if (x[-1],x[0])==(1,0) else 0
        return val
    assert path_min(U) == min(energy(x,False) for x in product(range(2),repeat=n))
    # For the cycle, absorb first-incident edges into the two endpoint unaries
    # on the remaining path, as in the manuscript's fixed-label construction.
    vals=[]
    for x0 in range(2):
        V=[row[:] for row in U[1:]]
        for t in range(2):
            V[0][t] += a[1] if (x0,t)==(0,1) else b[1] if (x0,t)==(1,0) else 0
            V[-1][t] += a[0] if (t,x0)==(0,1) else b[0] if (t,x0)==(1,0) else 0
        E=V[0][:]
        for j in range(1,len(V)):
            E=[V[j][0]+min(E[0],E[1]+b[j+1]), V[j][1]+min(E[1],E[0]+a[j+1])]
        vals.append(U[0][x0]+min(E))
    assert min(vals) == min(energy(x,True) for x in product(range(2),repeat=n))
results['clamp_path_and_cycle_exact_instances'] = 160

q,C1,C2,b,B,z1,z2,v,al,U=s.symbols('q C1 C2 b B z1 z2 v al U')
g1,g2=C1-q,C2-q
R=(g1*z1+g2*z2)
assert s.expand(g1*(R-g2*(z1+z2))/(C1-C2)-g1*z1).cancel()==0
W0=q*b*(B-1)+q*(1-q)*v
W1=b*(B-q)-W0
assert s.factor(b+W0/q-W1/(1-q)-v)==0
assert s.factor((-q)*(-W0/q)+(1-q)*(W1/(1-q))-b*(B-q))==0
results['scalar_outlet_and_two_vector_symbolic_identities'] = 'pass'

# Direct symbolic cancellation in the full-vector residual formulas.
K=4
Cs=s.symbols('c0:4'); Ds=s.symbols('d0:4'); Qs=s.symbols('q0:4'); Bs=s.symbols('b0:4')
beta0=[1,2,4,8]
ga=sum(beta0[i]*(Cs[i]-Qs[i]) for i in range(K))
gb=sum(beta0[i]*(Ds[i]-Qs[i]) for i in range(K))
rr=b*sum(beta0[i]*(Bs[i]-Qs[i]) for i in range(K))
for h in range(K):
    aa=s.expand((Cs[h]-Qs[h])*gb-(Ds[h]-Qs[h])*ga)
    ff=s.expand(ga*(b*(Bs[h]-Qs[h])*gb-(Ds[h]-Qs[h])*rr))
    assert s.Poly(aa,*Qs).total_degree()<=1
    assert s.Poly(ff,*Qs).total_degree()<=2
results['full_vector_residual_degree_cancellation'] = 'pass (K=4 symbolic)'

# Exact endpoint interpolation logic for all rational pairs on a small grid.
count=0
for qs,rs,qp,rp in product([F(i,8) for i in range(9)],repeat=4):
    rho=rs-qs*qs
    if rho<=0 or not 0<qp<1: continue
    lam=rho/(2*(rho+1))
    qx=(1-lam)*qs+lam*qp; rx=(1-lam)*rs+lam*rp
    assert 0<qx<1 and qx*qx-rx <= -rho/2
    count+=1
results['QP_negative_minimum_interior_mixing_pairs'] = count
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
