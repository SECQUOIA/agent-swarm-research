"""Independent exact Fibonacci balancing and graph-state witness checks."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as sp

stats={'families':0,'exact_witnesses':0,'exact_exclusions':0,'simple_lift_state_checks':0}
fib=[0,1,1]
for _ in range(15): fib.append(fib[-1]+fib[-2])
for q in range(3,10):
    labels=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
    n=len(labels)
    cols=[{('H',0),('P',1)},{('H',0),('P',2)}]
    for i in range(3,q+1): cols.extend([{('H',i),('P',i)},{('H',i),('P',i-1),('P',i-2)}])
    cols.append({('P',q),('P',q-1)})
    D=sp.Matrix([[int(row in col) for col in cols] for row in labels])
    K=sp.ones(n,n)-D
    alpha=sp.Matrix([fib[i] if typ=='P' else fib[q+1]-(1 if i==0 else fib[i]) for typ,i in labels])
    assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
    assert D.T*alpha==sp.ones(n,1)*fib[q+1]
    beta=(q-2)*fib[q+1]+1
    assert K.T*alpha==sp.ones(n,1)*beta
    inv=K.inv(); knorm=max(sum(abs(x) for x in inv.row(i)) for i in range(n))
    r,s=q-1,0; ratio=F(alpha[r],alpha[s]); a=F(1,2*n); c=a/4
    eps=a/(16*(1+ratio)*(1+F(knorm)))
    base_a=[sum(K.row(i))*a+(n-sum(K.row(i)))*c for i in range(n)]
    for u,v in product(range(-2,3),repeat=2):
        delta=sp.zeros(n,1); delta[r]=F(u,4)*eps; delta[s]=F(v,4)*eps
        slack=ratio*F(delta[r])+F(delta[s])
        if slack<0:
            assert (alpha.T*delta)[0]<0
            stats['exact_exclusions']+=1; continue
        tau=sp.zeros(n,1); tau[s]=slack
        shift=inv*(-delta+tau); w=[a+F(x) for x in shift]
        assert sum(w)==F(1,2) and all(0<x<2*a for x in w)
        aa=[]
        for i in range(n):
            row=[w[j] if K[i,j] else c for j in range(n)]
            # Selected observed cells are the last column for row P_q and
            # first column for row P_1, exactly as in the manuscript.
            if i==r: assert D[i,n-1]==1; row[n-1]+=F(delta[r])
            if i==s: assert D[i,0]==1; row[0]+=F(delta[s])
            if i==s:
                j=next(j for j in range(n) if K[i,j]); row[j]-=slack
            assert all(0<=row[j]<=w[j] for j in range(n))
            assert sum(row)==base_a[i]
            aa.append(row)
        bb=[[w[j]-aa[i][j] for j in range(n)] for i in range(n)]
        hh=[2*a-wj for wj in w]
        assert sum(hh)==F(1,2)
        for j in range(n):
            # Simple lift: connectors carry w_j; each subdivided b_i
            # carries its original b_i state flow on both segments.
            assert all(aa[i][j]+bb[i][j]==w[j] for i in range(n))
            assert all(0<=bb[i][j]<=2*a for i in range(n))
            assert 0<=w[j]<=2*a and w[j]+hh[j]==2*a
            stats['simple_lift_state_checks']+=1
        stats['exact_witnesses']+=1
    stats['families']+=1
K=sp.Matrix([[1,1,1,0],[1,0,0,1],[0,1,0,1],[0,0,1,1]])
assert K.T*sp.Matrix([2,1,1,1])==sp.ones(4,1)*3
stats['four_state_threshold_witnesses']=0
for u,v in product(range(-2,3),repeat=2):
    dr,ds=F(u,65536),F(v,65536)
    slack=2*dr+ds
    if slack<0: continue
    d=K.inv()*sp.Matrix([-dr,2*dr,0,0]); w=[F(1,8)+F(x) for x in d]
    assert sum(w)==F(1,2)
    for i in range(4):
        row=[w[j] if K[i,j] else F(1,32) for j in range(4)]
        if i==0: row[3]+=dr
        if i==1: row[1]+=ds; row[0]-=slack
        assert all(0<=row[j]<=w[j]<=F(1,4) for j in range(4))
        assert sum(row)==(F(13,32) if i==0 else F(5,16))
    stats['four_state_threshold_witnesses']+=1
stats['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
