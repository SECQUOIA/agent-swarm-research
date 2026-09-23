"""Independent affine-branch audit after eliminating the residual profile.

All observation categories for m=3 are represented by distinct gadgets.
For each positive circuit, extrema over all row branches bound every resulting
original-coordinate coefficient. Repeated gadget categories introduce new
coordinates but do not change this per-coordinate exhaustive check.
"""
from itertools import product, combinations
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as S

def check(m):
    rows={}
    def add(n,r):rows.setdefault(tuple(n),[]).append({k:F(v) for k,v in r.items() if v})
    def unit(j,sgn=1):return tuple(sgn*int(i==j) for i in range(m))
    full=(1,)*m
    add(full,{'xh':-1});add(tuple(-v for v in full),{'xh':1})
    for j in range(m):
        add(unit(j),{});add(unit(j,-1),{})
        add(unit(j),{f'h{j}':-1});add(unit(j,-1),{f'h{j}':1})
    for g,cat in enumerate(product('ABTU',repeat=m)):
        R={f'x{g}':1}
        for j,c in enumerate(cat):
            u=f'u{g},{j}';v=f'v{g},{j}'
            if c in 'AT':R[u]=-1
            if c=='B':R[v]=1
            if c=='A':add(unit(j,-1),{u:-1})
            if c=='B':add(unit(j,-1),{v:-1})
            if c=='T':
                add(unit(j),{u:1,v:1});add(unit(j,-1),{u:-1,v:-1})
        add([int(c=='B') for c in cat],R)
        add([int(c in 'AT') for c in cat],dict({'xh':-1},**{k:-v for k,v in R.items()}))
    zero=rows.pop((0,)*m,[])
    assert all(abs(v)<=1 for r in zero for v in r.values())
    normals=list(rows)
    circuits=[]
    for k in range(2,m+2):
        for ix in combinations(range(len(normals)),k):
            ns=S.Matrix([normals[i] for i in ix]).T.nullspace()
            if len(ns)!=1:continue
            v=ns[0]
            if all(x<0 for x in v):v=-v
            if not all(x>0 for x in v):continue
            v=v/smallest(v)
            pass
            circuits.append((ix,tuple(F(x) for x in v)))
    coordinates=sorted({c for branches in rows.values() for r in branches for c in r})
    worst=F(0);records=[]
    for ix,weights in circuits:
        extremes={}
        for c in coordinates:
            lo=sum(w*min(r.get(c,0) for r in rows[normals[i]]) for i,w in zip(ix,weights))
            hi=sum(w*max(r.get(c,0) for r in rows[normals[i]]) for i,w in zip(ix,weights))
            
            if abs(lo)>1 or abs(hi)>1: assert c=="xh" and max(abs(lo),abs(hi))==2
            worst=max(worst,abs(lo),abs(hi))
            if lo or hi:extremes[c]=[int(lo),int(hi)]
        records.append({'normals':[normals[i] for i in ix],'coefficient_intervals':extremes})
    repaired=0
    from collections import defaultdict
    for ix,weights in circuits:
        if not ((len(ix)==4 and all(sum(normals[i])==1 for i in ix if sum(normals[i])>0)) or any(w==2 for w in weights)):continue
        for chosen in product(*(rows[normals[i]] for i in ix)):
            rhs=defaultdict(F)
            for w,r in zip(weights,chosen):
                for c,v in r.items():rhs[c]+=w*v
            if abs(rhs['xh'])!=2:continue
            sign=rhs['xh']/2
            g=next(c for c,v in rhs.items() if c.startswith('x') and c!='xh' and v==sign)
            # Add -sign*(x_a+x_b+x_h=1) to the affine Farkas row.
            rhs['xh']-=sign;rhs[g]-=sign;rhs['b'+g]-=sign
            assert all(abs(v)<=1 for v in rhs.values())
            repaired+=1
    return dict(repaired_branch_combinations=repaired,m=m,normals=normals,circuits=len(circuits),coordinates=len(coordinates),maximum_coefficient=int(worst),zero_rows=len(zero),details=records)

def smallest(v):return min(v)

out=[check(3)]
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:v for k,v in d.items() if k!='details'} for d in out],indent=2))
