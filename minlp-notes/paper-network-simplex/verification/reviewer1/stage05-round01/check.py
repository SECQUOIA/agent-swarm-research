"""Independent exact audits of reduced profile circuits and coefficient claims."""
from itertools import combinations,product
from fractions import Fraction as F
from math import gcd,lcm
from functools import reduce
from pathlib import Path
import sympy as s
import json

def universe(m):
    return sorted(set(product((0,1),repeat=m))-{(0,)*m} |
                  {tuple(-int(i==j) for i in range(m)) for j in range(m)} |
                  {(-1,)*m})
def circuits(m):
    rows=universe(m);out=[]
    for size in range(2,m+2):
        for ids in combinations(range(len(rows)),size):
            ns=s.Matrix([rows[i] for i in ids]).T.nullspace()
            if len(ns)!=1 or any(v==0 for v in ns[0]):continue
            q=list(ns[0])
            if all(v<0 for v in q):q=[-v for v in q]
            if not all(v>0 for v in q):continue
            den=lcm(*(v.q for v in q));q=[int(v*den) for v in q]
            g=reduce(gcd,q);q=[v//g for v in q]
            out.append([(rows[i],w) for i,w in zip(ids,q)])
    return out

counts={};occurrence_checks=0
for m in (1,2,3):
    lib=circuits(m);counts[m]=len(lib)
    assert len(lib)=={1:1,2:5,3:16}[m]
    if m==3:
        types=[0,0,0,0]
        for circuit in lib:
            weights=dict(circuit)
            if (-1,)*m not in weights:kind=0
            elif weights[(-1,)*m]==2:kind=3
            elif any(sum(a)==-1 for a in weights):kind=2
            else:kind=1
            types[kind]+=1
        assert types==[7,5,3,1]
    if m==1:continue
    unit=lambda j:tuple(int(i==j) for i in range(m))
    for status in product('UABT',repeat=m):
        rows=[]
        A={j for j,t in enumerate(status) if t=='A'}
        B={j for j,t in enumerate(status) if t=='B'}
        T={j for j,t in enumerate(status) if t=='T'}
        lower={'xa':1};upper={'xa':-1,'xh':-1}
        for j in A|T:lower['a'+str(j)]=-1;upper['a'+str(j)]=1
        for j in B:lower['b'+str(j)]=1;upper['b'+str(j)]=-1
        rows += [(tuple(int(j in B) for j in range(m)),lower),
                 (tuple(int(j in A|T) for j in range(m)),upper)]
        for j,t in enumerate(status):
            products=(["a"+str(j)] if t=='A' else ["b"+str(j)] if t=='B' else
                      ["a"+str(j),"b"+str(j)] if t=='T' else [])
            if products:rows.append((tuple(-x for x in unit(j)),{p:-1 for p in products}))
            if t=='T':rows.append((unit(j),{p:1 for p in products}))
        variables={p for _,rhs in rows for p in rhs}-{'xh'}
        for circuit in lib:
            for p in variables:
                lo=hi=0
                for normal,weight in circuit:
                    available=[0]+[rhs.get(p,0) for n,rhs in rows if n==normal]
                    lo+=weight*min(available);hi+=weight*max(available)
                assert lo>=-1 and hi<=1,(m,status,circuit,p,lo,hi)
                occurrence_checks+=1

# Check both exceptional flow coefficients and exact violations independently.
assert 2*F(1,2)-3*F(2,5)==-F(1,5)
assert 3*F(3,20)+2*(F(1,4)-F(1,2))==-F(1,20)
for x,y,z in ((F(2,5),F(1,3),F(0)),(F(9,20),F(1,4),F(1,20))):
    assert max(0,x+y-1)<=z<=min(x,y)

fib=[0,1,1]
for i in range(3,13):fib.append(fib[-1]+fib[-2])
fib_cases=0
for q in range(3,10):
    labels=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
    cols=[{('H',0),('P',1)},{('H',0),('P',2)}]
    for i in range(3,q+1):cols += [{('H',i),('P',i)},{('H',i),('P',i-1),('P',i-2)}]
    cols += [{('P',q),('P',q-1)}]
    D=s.Matrix([[int(row in col) for col in cols] for row in labels]);N=2*q-1
    K=s.ones(N)-D;gamma=fib[q+1]
    alpha=s.Matrix([fib[i] if kind=='P' else gamma-(1 if i==0 else fib[i]) for kind,i in labels])
    assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
    assert D.T*alpha==gamma*s.ones(N,1)
    assert K.T*alpha==((q-2)*gamma+1)*s.ones(N,1)
    assert sum(alpha)==(q-1)*gamma+1 and all(a>0 for a in alpha)
    fib_cases+=1

# The m=4 balanced-incidence example: exact constructive half-plane witnesses.
K=s.Matrix([[1,1,1,0],[1,0,0,1],[0,1,0,1],[0,0,1,1]])
ki=K.inv();a=s.Rational(1,8);c=s.Rational(1,32)
positive=negative=0
for ir,js in product(range(-9,10),repeat=2):
    dr,ds=s.Rational(ir,10000),s.Rational(js,10000)
    slack=2*dr+ds
    if slack<0:negative+=1;continue
    delta=s.Matrix([dr,ds,0,0]);tau=s.Matrix([0,slack,0,0]);w=a*s.ones(4,1)+ki*(-delta+tau)
    assert sum(w)==s.Rational(1,2) and all(0<z<s.Rational(1,4) for z in w)
    for i in range(4):
        row=[w[j] if K[i,j] else c+(dr if (i,j)==(0,3) else ds if (i,j)==(1,1) else 0) for j in range(4)]
        if i==1:row[0]-=slack
        assert all(0<=z<=ww for z,ww in zip(row,w))
        assert sum(row)==sum(K[i,j]*a+(1-K[i,j])*c for j in range(4))
    positive+=1
out={'status':'PASS','reduced_circuit_counts':counts,'m3_types':types,
     'exact_product_and_local_flow_occurrence_checks':occurrence_checks,
     'fibonacci_cases':fib_cases,'m4_exact_section_witnesses':positive,
     'm4_section_negative_sides':negative,'both_repair_examples_checked':True}
Path(__file__).with_name('check-output.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
