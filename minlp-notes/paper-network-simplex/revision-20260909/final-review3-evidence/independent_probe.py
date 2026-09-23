from itertools import combinations, product
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import sympy as sp
import numpy as np
from scipy.optimize import linprog
import json, random

def primitive(v):
    den=lcm(*(int(x.q) for x in v)); a=[int(x*den) for x in v]
    g=reduce(gcd,a); a=[x//abs(g) for x in a]
    if next(x for x in a if x)<0:a=[-x for x in a]
    return tuple(a)

# Derive every m=3 positive circuit independently by exact nullspaces.
n=3
pos=[tuple(int(mask>>j&1) for j in range(n)) for mask in range(1,2**n)]
neg=[tuple(-int(i==j) for j in range(n)) for i in range(n)]+[(-1,)*n]
norms=sorted(set(pos+neg)); circuits=[]
for k in range(2,n+2):
    for ids in combinations(range(len(norms)),k):
        ns=sp.Matrix([norms[i] for i in ids]).T.nullspace()
        if len(ns)!=1 or any(x==0 for x in ns[0]):continue
        v=primitive(ns[0])
        if min(v)>0:circuits.append([(norms[i],q) for i,q in zip(ids,v)])
assert len(circuits)==16
# All 64 local observation patterns; for each present product and circuit,
# independently maximize/minimize its coefficient over row choices per normal.
# A zero contribution always exists from a different gadget with that normal.
occ_checks=0
for pattern in product(range(4),repeat=3): # 0 none,1 a,2 b,3 both
    A=[j for j,p in enumerate(pattern) if p==1]; B=[j for j,p in enumerate(pattern) if p==2]; T=[j for j,p in enumerate(pattern) if p==3]
    rows=[]
    for j,p in enumerate(pattern):
        e=tuple(int(k==j) for k in range(3)); me=tuple(-x for x in e)
        if p==1:rows.append((me,{('a',j):-1}))
        if p==2:rows.append((me,{('b',j):-1}))
        if p==3:
            rows.extend([(e,{('a',j):1,('b',j):1}),(me,{('a',j):-1,('b',j):-1})])
    r={('a',j):-1 for j in A+T};r.update({('b',j):1 for j in B})
    rows.extend([(tuple(int(j in B) for j in range(3)),r),(tuple(int(j in A+T) for j in range(3)),{z:-q for z,q in r.items()})])
    zs=set().union(*(set(coeff) for _,coeff in rows))
    for z in zs:
        for circuit in circuits:
            lo=hi=0
            for normal,weight in circuit:
                values=[0]+[coeff.get(z,0) for a,coeff in rows if a==normal]
                lo+=weight*min(values);hi+=weight*max(values)
            assert lo>=-1 and hi<=1,(pattern,z,circuit,lo,hi)
            occ_checks+=1
# Independent finite support library for the rank-three K4 cycle matrix.
C=sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
arcs=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=sp.Matrix([[int(h==i)-int(t==i) for t,h in arcs] for i in range(4)])
assert A*C==sp.zeros(4,3)
M=sorted(set(tuple(C.row(i)) for i in range(6))|set(tuple(-C.row(i)) for i in range(6)))
D=set()
for ids in combinations(range(len(M)),2):
    ns=sp.Matrix([M[i] for i in ids]).nullspace()
    if len(ns)==1:D.add(primitive(ns[0]))
assert all(abs(sum(a*b for a,b in zip(row,d)))<=1 for row in M for d in D)
R=set()
for dd in combinations(D,2):
    ns=sp.Matrix(dd).nullspace()
    if len(ns)==1:
        v=primitive(ns[0]);R.add(v);R.add(tuple(-x for x in v))
assert max(abs(x) for h in R for x in h)<=2
bases=[]
for ids in combinations(range(len(M)),3):
    B=sp.Matrix([M[i] for i in ids])
    if B.det():
        assert abs(B.det())==1;bases.append((ids,B.inv()))
duals={h:[] for h in R}
for h in R:
    for ids,inv in bases:
        q=inv.T*sp.Matrix(h)
        if min(q)>=0:
            assert max(q)<=2;duals[h].append((ids,tuple(q)))
rng=random.Random(904033)
support_checks=sum_checks=0
for case in range(35):
    gammas=[]
    for j in range(1+case%5):
        center=[F(rng.randint(-3,3),8) for _ in range(3)]
        gamma=[sum(a*b for a,b in zip(row,center))+F(rng.randrange(4),8) for row in M]
        if case%5==0:gamma=[sum(a*b for a,b in zip(row,center)) for row in M] # point
        gammas.append(gamma)
    supports=[]
    for g in gammas:
        vals={h:min(sum(qk*g[i] for i,qk in zip(ids,q)) for ids,q in duals[h]) for h in R}
        for h in R:
            lp=linprog(-np.array(h,dtype=float),A_ub=np.array(M,dtype=float),b_ub=np.array(g,dtype=float),bounds=[(None,None)]*3,method='highs')
            assert lp.success and abs(float(vals[h])+lp.fun)<1e-8
            support_checks+=1
        supports.append(vals)
    for probe in range(8):
        p=[F(rng.randint(-12,12),16) for _ in range(3)]
        finite=all(sum(a*b for a,b in zip(h,p))<=sum(s[h] for s in supports) for h in R)
        cnt=len(gammas); aub=np.zeros((len(M)*cnt,3*cnt))
        for j in range(cnt):aub[j*len(M):(j+1)*len(M),j*3:(j+1)*3]=np.array(M,dtype=float)
        lp=linprog(np.zeros(3*cnt),A_ub=aub,b_ub=np.array(sum(gammas,[]),dtype=float),A_eq=np.tile(np.eye(3),(1,cnt)),b_eq=np.array(p,dtype=float),bounds=[(None,None)]*(3*cnt),method='highs')
        assert finite==lp.success,(case,p,lp.message)
        sum_checks+=1
result={'status':'PASS','positive_circuits_m3':len(circuits),'all_local_patterns':64,'product_occurrence_extrema_checked':occ_checks,'K4_directions':len(D),'K4_rays':len(R),'K4_normal_bases':len(bases),'max_ray_entry':int(max(abs(x) for h in R for x in h)), 'max_multiplier':int(max(qk for ds in duals.values() for ids,q in ds for qk in q)),'support_vs_independent_LP':support_checks,'sum_membership_vs_joint_LP':sum_checks,'limits':'Circuit and multiplier checks exact; LP comparisons numerical; rank-three scope only; recovered-state checks run separately from supplied independent script.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
