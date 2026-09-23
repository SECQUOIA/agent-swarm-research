"""Reviewer-written exact check of the printed sparse balanced construction."""
import json
from pathlib import Path
from sympy import Matrix, Rational, ones, zeros
results=[]
for q in range(3,16):
    n=2*q-1
    primary=list(range(q)); aux={0:q,**{i:q+i-2 for i in range(3,q+1)}}
    cols=[{aux[0],0},{aux[0],1}]
    for i in range(3,q+1):cols += [{aux[i],i-1},{aux[i],i-2,i-3}]
    cols += [{q-1,q-2}]
    D=Matrix(n,n,lambda i,j:int(i in cols[j])); K=ones(n)-D
    F=[0,1,1]
    for i in range(3,q+2):F.append(F[-1]+F[-2])
    alpha=Matrix([F[i] for i in range(1,q+1)]+[F[q+1]-1]+[F[q+1]-F[i] for i in range(3,q+1)])
    assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
    assert D.T*alpha==F[q+1]*ones(n,1)
    assert K.T*alpha==((q-2)*F[q+1]+1)*ones(n,1)
    inv=K.inv(); norm=max(sum(abs(inv[i,j]) for j in range(n)) for i in range(n))
    a=Rational(1,2*n); c=a/4; ratio=F[q]
    eps=a/(16*(1+ratio)*(1+norm))
    accepted=rejected=0
    for dr in range(-3,4):
      for ds in range(-3,4):
        delta=zeros(n,1); delta[q-1]=dr*eps/4; delta[0]=ds*eps/4
        slack=(alpha.T*delta)[0]
        if slack<0:rejected+=1;continue
        tau=zeros(n,1);tau[0]=ratio*delta[q-1]+delta[0]
        w=a*ones(n,1)+inv*(-delta+tau)
        assert sum(w)==Rational(1,2) and all(0<v<2*a for v in w)
        for i in range(n):
            row=[w[j] if K[i,j] else c for j in range(n)]
            free_col=n-1 if i==q-1 else (0 if i==0 else None)
            if free_col is not None:row[free_col]+=delta[i]
            if i==0:row[next(j for j in range(n) if K[i,j])]-=tau[i]
            assert sum(row)==sum(K[i,j] for j in range(n))*a+sum(D[i,j] for j in range(n))*c
            assert all(0<=row[j]<=w[j] for j in range(n))
            # b_i state entries and bypass obey the same scaled capacities.
            assert all(0<=w[j]-row[j]<=2*a and 0<=2*a-w[j]<=2*a for j in range(n))
        accepted+=1
    results.append(dict(q=q,ratio=ratio,observations=int(sum(D)),accepted=accepted,rejected=rejected))
print(json.dumps(results,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')
