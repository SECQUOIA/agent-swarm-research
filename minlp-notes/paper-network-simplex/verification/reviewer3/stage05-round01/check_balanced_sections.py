"""Exact balanced-incidence witnesses and Fibonacci identities, independent code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as s

def rational(x):
    return F(int(x.p),int(x.q))
counts={'matrices':0,'feasible_witnesses':0,'negative_certificates':0,'fibonacci':[]}
def check(K,alpha,r,zrow):
    N=K.rows
    assert K.cols==N and K.det()!=0
    assert all(0<sum(K.row(i))<N for i in range(N))
    balanced=K.T*s.Matrix(alpha)
    assert len(set(balanced))==1 and balanced[0]>0
    inv=K.inv()
    norm=max(sum(abs(rational(inv[i,j])) for j in range(N)) for i in range(N))
    a=F(1,2*N);c=a/4;ratio=F(alpha[r],alpha[zrow])
    eps=a/(16*(1+ratio)*(1+norm))
    Ucol=next(j for j in range(N) if K[r,j]==0)
    Vcol=next(j for j in range(N) if K[zrow,j]==0)
    for pr,pv in product(range(-2,3),repeat=2):
        delta=[F(0)]*N
        delta[r]=pr*eps/3;delta[zrow]=pv*eps/3
        if sum(a*b for a,b in zip(alpha,delta))<0:
            counts['negative_certificates']+=1
            continue
        tau=[F(0)]*N;tau[zrow]=ratio*delta[r]+delta[zrow]
        rhs=[-d+t for d,t in zip(delta,tau)]
        deviation=[sum(rational(inv[i,j])*rhs[j] for j in range(N)) for i in range(N)]
        w=[a+d for d in deviation]
        assert sum(w)==F(1,2)
        assert all(0<=t<=2*a for t in w)
        flow=[]
        for i in range(N):
            row=[w[j] if K[i,j] else c for j in range(N)]
            if i==r:row[Ucol]+=delta[r]
            if i==zrow:row[Vcol]+=delta[zrow]
            if i==zrow:
                chosen=next(j for j in range(N) if K[i,j])
                row[chosen]-=tau[i]
            assert all(0<=v<=t for v,t in zip(row,w))
            expected=int(sum(K.row(i)))*a+(N-int(sum(K.row(i))))*c
            assert sum(row)==expected
            flow.append(row)
        assert all(0<=2*a-wj<=2*a for wj in w)
        counts['feasible_witnesses']+=1
    counts['matrices']+=1

small=s.Matrix([[1,1,1,0],[1,0,0,1],[0,1,0,1],[0,0,1,1]])
check(small,[2,1,1,1],0,1)
for q in range(3,10):
    rows=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
    columns=[[('H',0),('P',1)],[('H',0),('P',2)]]
    for i in range(3,q+1):
        columns.extend([[('H',i),('P',i)],[('H',i),('P',i-1),('P',i-2)]])
    columns.append([('P',q),('P',q-1)])
    D=s.Matrix([[int(row in col) for col in columns] for row in rows])
    assert D.rows==D.cols==2*q-1 and sum(D)==5*q-4
    fib=[0,1,1]
    for i in range(3,q+2):fib.append(fib[-1]+fib[-2])
    gamma=fib[q+1]
    alpha=[fib[i] if tag=='P' else gamma-(1 if i==0 else fib[i]) for tag,i in rows]
    assert D.T*s.Matrix(alpha)==s.ones(2*q-1,1)*gamma
    assert sum(alpha)==(q-1)*gamma+1
    K=s.ones(2*q-1,2*q-1)-D
    check(K,alpha,q-1,0)
    counts['fibonacci'].append({'q':q,'ratio':fib[q],'observations':int(sum(D))})
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(counts)
