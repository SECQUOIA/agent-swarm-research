"""Independent bounded checks for frozen Section 3; not a proof substitute."""
from fractions import Fraction as F
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog
from pathlib import Path
results={}
# Physical cycle LPs: each gadget has (uA,vA,mA,uB,vB,mB).
for half, betas in [(False,[1]),(False,[1,3,33]),(True,[3]),(True,[3,3,3])]:
    r=len(betas); nv=6*r; eq=[]; rhs=[]; ub=[]; br=[]; bounds=[]
    def row(entries):
        a=np.zeros(nv)
        for i,v in entries: a[i]+=v
        return a
    for g,beta in enumerate(betas):
        o=6*g; demand=3 if half else 4; gamma=1 if half else beta/2
        bounds += [(0,2),(0,1 if half else 2),(0,demand)]*2
        for j in [0,3]:
            eq.append(row([(o+j,1),(o+j+1,1),(o+j+2,1)]));rhs.append(demand)
            ub.append(row([(o+j,-gamma),(o+j+1,beta-gamma)]));br.append(0)
        eq.append(row([(o+2,1),(o+5,1)]));rhs.append(demand)
        eq.append(row([(o+3,1),(6*((g+1)%r),1)]));rhs.append(2)
    worst=0
    objectives=[]
    for g in range(r):
        for j in [0,3]: objectives.append(row([(6*g+j,1),(6*g+j+1,-2 if half else -1)]))
        objectives.append(row([(6*g,1),(0,-1)]))
    for obj in objectives:
        for sign in [-1,1]:
            sol=linprog(sign*obj,A_ub=ub,b_ub=br,A_eq=eq,b_eq=rhs,bounds=bounds,method='highs')
            assert sol.success
            worst=max(worst,abs(sol.fun))
    assert worst<1e-8
    # Every x in the test grid admits its exact physical formulas.
    for x in [F(0),F(1,7),F(1),F(13,7),F(2)]:
        z=[]
        for beta in betas:
            z.extend([x,x/2,3-3*x/2,2-x,1-x/2,3*x/2] if half else [x,x,4-2*x,2-x,2-x,2*x])
        assert all(sum(F(str(a))*v for a,v in zip(rr,z))==v for rr,v in zip(eq,rhs))
    results[f'physical_{"half" if half else "full"}_{betas}']=float(worst)
# Every dyadic numerator through ten bits: exact arithmetic recurrence.
count=0
for L in range(1,11):
    for c in range(2**L):
        x=F(13,7);t=F(0)
        for k in range(L): t=(t+((c>>k)&1)*x)/2
        assert t==F(c,2**L)*x
        count+=1
results['exact_dyadic_multipliers']=count
# Matsui correction and scale/palette estimates, exact arithmetic.
n=5;p=2;r=F(1,2)
X=sum(F(p**i)*r for i in range(1,n+1));Y=sum(F(p**(2*i))*r for i in range(1,n+1))
assert Y-X*X==-279
assert p*p*F(1,4)/2-p*n*n==-F(99,2)
for n in [5,6,8]:
    p=n**(n**4);P4=p**(4*n);u0=2*P4-p;s=n+n*n;K=4*p**(8*n)
    D=1<<((u0//2).bit_length()-1)
    coeffU=[u0]+[u0+2*s*p**(2*n+i) for i in range(1,n+1)]+[u0+s*p**(i+j) for i in range(1,n+1) for j in range(1,n+1)]
    coeffV=[u0]+[u0-2*s*p**(2*n+i) for i in range(1,n+1)]+[u0+s*p**(i+j) for i in range(1,n+1) for j in range(1,n+1)]
    for U,V in zip(coeffU,coeffV):
        a=F(U,D)-1;rho=(a-1)/32
        assert 1<=a<19 and 0<=rho<1 and K-D*V>0
        assert rho.denominator & (rho.denominator-1)==0
    for bits in product([0,1],repeat=n):
        X=sum(p**(i+1)*v for i,v in enumerate(bits));Y=X*X
        U=u0+Y+2*p**(2*n)*X;V=u0+Y-2*p**(2*n)*X
        assert U>0 and V>0 and U*V<K
        assert U*V-K==(Y-p)**2+4*p**(4*n)*(Y-X*X-p)
    results[f'exact_matsui_n{n}']={'generators':len(coeffU),'binary_points':2**n,'threshold_bits':K.bit_length()}
# Exact complement-group and split supplies at admissible rational gate flows.
cases=[([2,1,1],[F(1),F(1,3),F(2,3)],2),([2,2,2],[F(1,3),F(1,2),F(7,6)],2),([2,2],[F(1,3),F(5,3)],2),([2],[F(0)],0),([2],[F(1)],1)]
for caps,flows,S in cases:
    assert sum(flows)==S
    mates=[c-f for c,f in zip(caps,flows)]
    assert sum(mates)==sum(caps)-S
    if len(caps)==3:
        for fs,supply in [(flows,S),(mates,sum(caps)-S)]:
            collector=[c-f for c,f in zip(caps,fs)]
            assert sum(collector) in [2,4]
            assert sum(collector)==sum(caps)-supply
results['complement_group_and_split_gate_types']=len(cases)
# Independent-set identity for explicit simple edge-colored cubic graphs.
def alpha(n,edges):
    return max(sum(bits) for bits in product([0,1],repeat=n) if all(not(bits[u] and bits[v]) for u,v in edges))
graphs={'K4': [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]], 'K33': [[(i,3+(i+c)%3) for i in range(3)] for c in range(3)]}
for name,colors in graphs.items():
    n=2*len(colors[0]);edges=sum(colors,[]);H=colors[0]+colors[1]
    for k,(u,v) in enumerate(colors[2]): H.extend([(u,n+2*k),(n+2*k,n+2*k+1),(n+2*k+1,v)])
    a=alpha(n,edges);ah=alpha(2*n,H)
    assert ah==n//2+a
    results[f'IS_{name}']={'alpha_G':a,'alpha_H':ah}
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
