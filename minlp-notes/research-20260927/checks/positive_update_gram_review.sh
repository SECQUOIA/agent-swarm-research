python - <<'PY'
from itertools import combinations
from collections import defaultdict
from random import Random
from sympy import Matrix, Rational, floor, eye, zeros
rng=Random(9817)
n=5; d=2; eps=Rational(4,5); delta=eps/(d*n)
checks=collisions=branches=0
for trial in range(12):
    vals=[(rng.choice([-1,0,1]),rng.choice([-1,0,1]),rng.choice([1,1,2])) for _ in range(n)]
    costs=[rng.randint(-3,4) for _ in range(n)]
    W=[Matrix([u,b])*Matrix([[u,b]])/di for u,b,di in vals]
    fixed=Matrix([[1,0],[0,0]])
    atoms=W+[fixed]
    def kmat(mask):
        return fixed+sum((W[i] for i in range(n) if mask>>i&1),zeros(d))
    def gain(mask):
        K=kmat(mask)
        return K[1,1]-K[0,1]**2/K[0,0]
    for B in combinations(range(n+1),d):
        A=sum((atoms[i] for i in B),zeros(d))
        if A.det()==0: continue
        inv=A.inv()
        if (inv*fixed).trace()>d: continue
        allowed=[i for i in range(n) if (inv*W[i]).trace()<=d]
        L,D=A.LDLdecomposition(hermitian=False)
        scales=[]
        for k in range(d):
            s=Rational(1)
            while s*s*D[k,k]<1: s*=2
            while s*s*D[k,k]>=4: s/=2
            scales.append(s)
        R=Matrix.diag(*scales)*L.inv()
        anchor=sum(1<<i for i in B if i<n)
        keys=[tuple(int(floor((R*w*R.T)[p,q]/delta)) for p in range(d) for q in range(p,d)) for w in W]
        groups=defaultdict(list)
        for mask in range(1<<n):
            if mask&anchor!=anchor or any(mask>>i&1 for i in range(n) if i not in allowed): continue
            key=tuple(sum(keys[i][j] for i in range(n) if mask>>i&1) for j in range(3))
            groups[key].append(mask)
        for masks in groups.values():
            if len(masks)>1: collisions+=len(masks)-1
            T=min(masks,key=lambda m:sum(costs[i] for i in range(n) if m>>i&1))
            for S in masks:
                E=kmat(T)-(1-eps)*kmat(S)
                assert E[0,0]>=0 and E[1,1]>=0 and E.det()>=0
                assert gain(T)>=(1-eps)*gain(S)
                assert sum(costs[i] for i in range(n) if T>>i&1)<=sum(costs[i] for i in range(n) if S>>i&1)
                checks+=1
        branches+=1
print({'exact_pair_checks':checks,'key_collisions':collisions,'valid_branches':branches,'trials':12,'epsilon':str(eps),'negative_costs':True})
PY
