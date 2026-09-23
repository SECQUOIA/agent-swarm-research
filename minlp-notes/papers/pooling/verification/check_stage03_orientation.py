"""Independent stage-3 reviewer 01 regression, retained without rerunning.

Requires NumPy and SciPy. Orientation enumeration is exact; physical LP
comparisons use floating-point HiGHS. These finite checks are not proofs.
"""
from itertools import product, combinations
import random
import numpy as np
from scipy.optimize import linprog

def orient(es,caps):
    es=sorted(es,key=lambda e:-e[2]); load=[0]*len(caps)
    def go(i):
        if i==len(es): return True
        u,v,w=es[i]
        for k in (u,v):
            if load[k]+w<=caps[k]:
                load[k]+=w
                if go(i+1): return True
                load[k]-=w
        return False
    return go(0)

def sat(cs,n): return any(all(any(bool(a[i])==s for i,s in c) for c in cs) for a in product((0,1),repeat=n))
def gadget(cs,n):
    es=[(2*i,2*i+1,2) for i in range(n)]; caps=[2]*(2*n)
    for cl in cs:
        v=len(caps); caps.append(2)
        es.extend((v,2*i+int(sign),1) for i,sign in cl)
        if len(cl)==2:
            k=len(caps); caps.extend([2]*3)
            es.extend([(v,k,1),(k,k+1,2),(k+1,k+2,2),(k+2,k,2)])
    return es,caps
clauses=[tuple(zip(ids,signs)) for ids in combinations(range(3),2) for signs in product((False,True),repeat=2)]
clauses += [tuple(zip(range(3),signs)) for signs in product((False,True),repeat=3)]
checked=0
for m in range(1,4):
    for cs in combinations(clauses,m):
        if any(sum((i,s) in cl for cl in cs)>2 for i in range(3) for s in (False,True)): continue
        es,caps=gadget(cs,3)
        assert sat(cs,3)==orient(es,caps)
        ds=[]; dc=caps[:]
        for u,v,w in es:
            k=len(dc); dc.append(w); ds.extend([(u,k,w),(k,v,w)])
        assert orient(ds,dc)==sat(cs,3)
        assert len(set((min(u,v),max(u,v)) for u,v,w in ds))==len(ds)
        assert max(sum(k in (u,v) for u,v,w in ds) for k in range(len(dc)))<=3
        checked+=1
print('SAT/orientation/subdivision exhaustive distinct-clause cases:',checked)

def pooling(es,caps,private_inputs,pool_cap):
    m=len(es); eq=[]; rhs=[]; ub=[]; bs=[]; obj=np.tile([1,0,-2,-1],m)
    for e,(u,v,w) in enumerate(es):
        a=np.zeros(4*m); a[4*e:4*e+4]=[1,1,-1,-1]; eq.append(a);rhs.append(0)
        if pool_cap:
            a=np.zeros(4*m); a[4*e:4*e+2]=1;ub.append(a);bs.append(w)
        for offset in ((0,1) if private_inputs else (2,3)):
            a=np.zeros(4*m);a[4*e+offset]=1;ub.append(a);bs.append(w)
    for v,cap in enumerate(caps):
        a=np.zeros(4*m)
        for e,(u,z,w) in enumerate(es):
            if v==u:a[4*e+(2 if private_inputs else 0)]=1
            if v==z:a[4*e+(3 if private_inputs else 1)]=1
        ub.append(a);bs.append(cap)
    best=0
    for mode in product((0,1),repeat=m):
        bounds=[(0,None)]*(4*m)
        for e,k in enumerate(mode):bounds[4*e+(1 if k==0 else 2)]=(0,0)
        r=linprog(obj,A_ub=ub,b_ub=bs,A_eq=eq,b_eq=rhs,bounds=bounds,method='highs')
        assert r.success
        best=min(best,r.fun)
    return best
rng=random.Random(713)
for case in range(22):
    edges=rng.sample([(u,v) for u in range(3) for v in range(3,6)],rng.randint(1,6))
    es=[(u,v,rng.choice((1,2))) for u,v in edges]; caps=[rng.choice((1,2)) for _ in range(6)]
    yes=orient(es,caps); threshold=-sum(w for u,v,w in es)
    for private_inputs,pool_cap in product((False,True),repeat=2):
        val=pooling(es,caps,private_inputs,pool_cap)
        assert val>=threshold-1e-8
        assert (abs(val-threshold)<1e-8)==yes,(case,private_inputs,pool_cap,val,threshold,yes)
print('Both placements with/without pool capacity:',22*4,'complete branch-LP optimizations')
