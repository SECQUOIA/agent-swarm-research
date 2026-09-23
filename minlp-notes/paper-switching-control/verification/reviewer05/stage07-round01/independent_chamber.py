"""Reconstruct the chamber certificate rows without importing project code."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
BASE=Path(__file__).parent/'relocated'/'verification'
old=list(map(Q,json.loads((BASE/'reference/general_reach_relaxation_witness.json').read_text())['variables']))
cert=json.loads((BASE/'stage03/chronological_chamber_certificate.json').read_text())
labels=set(range(6))
events=[(h,tuple(U)) for h,minimum in [(2,3),(3,4)] for size in range(6,minimum-1,-1) for U in combinations(range(6),size)]
assert len(events)==64
position={v:j for j,v in enumerate(events)}
def ti(v):return 6+7*position[v]
def ai(v,i):return ti(v)+1+i
rows=[];eq=[]
def row(rhs,*terms):
    d={}
    for i,a in terms:d[i]=d.get(i,0)+a
    rows.append((d,rhs))
for i in range(1,6):row(0,(0,1),(i,-1))
row(-6,*[(i,-1) for i in range(1,6)])
for i in range(6):row(-1,(i,-1))
for v in events:
    h,U=v; present=set(U)
    eq.append(({ti(v):-1,**{ai(v,i):1 for i in range(6)}},0))
    for i in U:
        row(1,(i,1),(ai(v,i),-1))
        if h==2:
            for j in U:
                if j!=i:row(-1,(j,1),(ti(v),-1),(ai(v,i),1))
        else:
            w=(2,tuple(j for j in U if j!=i))
            row(-1,(ti(w),1),(ti(v),-1),(ai(v,i),1))
    for w in events:
        hh,V=w
        if v!=w and h<=hh and present<=set(V):
            for i in range(6):row(0,(ai(v,i),1),(ai(w,i),-1))
    if set(range(h))<=present and present!=labels:
        for i in range(6):row(0,(ai((h,tuple(range(6))),i),1),(ai(v,i),-1))
assert len(rows)==3660 and len(eq)==64
obj={}
for i in range(4):
    for omitted in [{i}]+[{i,j} for j in range(6) if j!=i]:
        t=ti((3,tuple(sorted(labels-omitted))))
        obj[t]=obj.get(t,0)+1
assert sum(obj.values())==24
value=lambda coeff,x:sum(a*x[i] for i,a in coeff.items())
assert all(value(a,old)<=b for a,b in rows)
assert all(value(a,old)==b for a,b in eq)
assert value(obj,old)==Q(40328,387)
order=sorted(range(64),key=lambda j:(old[6+7*j],j))
assert order==cert['order'] and set(order[:42])==set(range(42))
violations=[old[7+7*a+i]-old[7+7*b+i] for j,a in enumerate(order) for b in order[j+1:] for i in range(6) if old[7+7*a+i]>old[7+7*b+i]]
assert len(violations)==239 and max(violations)==Q(224,645)
for a,b in zip(order,order[1:]):
    for i in range(6):row(0,(7+7*a+i,1),(7+7*b+i,-1))
assert len(rows)==4038
key=lambda ar: (tuple(sorted((i,c) for i,c in ar[0].items() if c)),ar[1])
rows.sort(key=key);eq.sort(key=key)
Y=list(map(Q,cert['inequality_dual']));Z=list(map(Q,cert['equality_dual']))
assert len(Y)==len(rows) and len(Z)==len(eq) and max(Y)<=0
res=[Q(obj.get(i,0)) for i in range(454)]
for weights,system in [(Y,rows),(Z,eq)]:
    for multiplier,(a,b) in zip(weights,system):
        for i,c in a.items():res[i]-=multiplier*c
assert min(res)>=0
bound=sum(y*b for y,(a,b) in zip(Y,rows))+sum(z*b for z,(a,b) in zip(Z,eq))
assert bound==Q(13104,125)
# Construct the uniform primal directly, without using the stored primal array.
x=[Q(6,5)]*6
for h,U in events:
    t=6*(Q(6,5)**h-1)
    x += [t]+[t/6]*6
assert all(value(a,x)<=b for a,b in rows)
assert all(value(a,x)==b for a,b in eq)
assert value(obj,x)==bound
assert x==list(map(Q,cert['primal']))
print('PASS independently reconstructed 3660 base rows, 378 chamber rows and 64 equalities')
print('PASS nonphysical witness, exact dual lower bound, independently constructed uniform primal')
print('PASS exact single-chamber optimum',bound,'; nonzero dual rows',sum(y!=0 for y in Y)+sum(z!=0 for z in Z))
