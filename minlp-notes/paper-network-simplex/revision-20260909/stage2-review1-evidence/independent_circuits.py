"""Positive circuits and product occurrences, independently from the manuscript."""
import itertools as it
import json
import math
from pathlib import Path
import sympy as s

normals=[tuple(int(mask>>j&1) for j in range(3)) for mask in range(1,8)]
negative=[tuple(-int(j==k) for j in range(3)) for k in range(3)]
normals+=negative+[(-1,-1,-1)]
circuits=[]
for size in range(2,5):
    for ids in it.combinations(range(len(normals)),size):
        ns=s.Matrix([normals[i] for i in ids]).T.nullspace()
        if len(ns)!=1 or any(v==0 for v in ns[0]):continue
        v=ns[0]
        if all(x<0 for x in v):v=-v
        if not all(x>0 for x in v):continue
        den=s.ilcm(*[x.q for x in v]); vals=[int(x*den) for x in v]
        g=math.gcd(*vals); vals=[x//g for x in vals]
        circuits.append(dict(zip((normals[i] for i in ids),vals)))

def canonical(c):return tuple(sorted(c.items()))
expected=[]
for mask in range(1,8):
    row=tuple(int(mask>>j&1) for j in range(3))
    expected.append({row:1,**{negative[j]:1 for j in range(3) if row[j]}})
# Disjoint positive subsets summing to all ones are exactly partitions.
for size in range(1,4):
    for rows in it.combinations(normals[:7],size):
        if all(sum(row[j] for row in rows)==1 for j in range(3)):
            expected.append({(-1,-1,-1):1,**{row:1 for row in rows}})
for i in range(3):
    rows=[tuple(int(j==i or j==k) for j in range(3)) for k in range(3) if k!=i]
    expected.append({(-1,-1,-1):1,negative[i]:1,**{row:1 for row in rows}})
expected.append({(-1,-1,-1):2,(1,1,0):1,(1,0,1):1,(0,1,1):1})
assert set(map(canonical,circuits))==set(map(canonical,expected)) and len(circuits)==16

checked=0
# Pattern codes: none, a only, b only, both. Build original profile RHS
# coefficient dictionaries before aggregation; no production imports.
for pattern in it.product(range(4),repeat=3):
    A={j for j,c in enumerate(pattern) if c==1}
    B={j for j,c in enumerate(pattern) if c==2}
    T={j for j,c in enumerate(pattern) if c==3}
    rows=[]
    r={('a',j):-1 for j in A|T};r.update({('b',j):1 for j in B})
    rows.append((tuple(int(j in B) for j in range(3)),r))
    rows.append((tuple(int(j in A|T) for j in range(3)),{k:-v for k,v in r.items()}))
    for j in A:rows.append((negative[j],{('a',j):-1}))
    for j in B:rows.append((negative[j],{('b',j):-1}))
    for j in T:
        rows.append((negative[j],{('a',j):-1,('b',j):-1}))
        rows.append((tuple(int(k==j) for k in range(3)),{('a',j):1,('b',j):1}))
    products=set(k for _,rhs in rows for k in rhs)
    for product in products:
        options={normal:{0} for normal in normals}
        for normal,rhs in rows:
            if any(normal):options[normal].add(rhs.get(product,0))
            else:assert abs(rhs.get(product,0))<=1
        for circuit in circuits:
            low=sum(weight*min(options[normal]) for normal,weight in circuit.items())
            high=sum(weight*max(options[normal]) for normal,weight in circuit.items())
            assert -1<=low<=high<=1
            checked+=1
result={'positive_circuits':len(circuits),'symbolic_families_match':True,
        'observation_patterns':64,'product_coefficient_ranges':checked,
        'largest_primitive_weight':max(v for c in circuits for v in c.values())}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
