from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import json
import sympy as s

x,y,z,u,v,a,b,c,h,sign=s.symbols('x y z u v a b c h sign')
cut=3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
lhs=(1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
assert s.expand(lhs-cut+sign*((v-u*z)+c*(u-x*y))/2)==0
assert s.expand(v-x*y*z-(v-u*z)-z*(u-x*y))==0

points=[Q(i,2) for i in range(-2,3)]
intervals=list(combinations(points,2))+[(p,p) for p in points]
checks=0
for box in product(intervals,repeat=3):
    lows=[t[0] for t in box]
    width=max(t[1]-t[0] for t in box)
    for xx,yy,zz in product(*[sorted(set(t)) for t in box]):
        for uu,sgn in product((-1,1),repeat=2):
            q=3*width/2-Q(sgn,2)*(uu*(zz-lows[2])+lows[2]*(xx*yy-lows[0]*lows[1]))
            assert q>=0
            checks+=1
# A law genuinely outside the graph, obeying the two graph equations in mean.
law=[(Q(1,2),Q(1,2),Q(0),Q(-1,2),Q(1,2)),(Q(1,2),Q(1,2),Q(1),Q(1),Q(1,2))]
assert sum(t[3]-t[0]*t[1] for t in law)==0
assert sum(t[4]-t[3]*t[2] for t in law)==0
assert all(t[3]!=t[0]*t[1] for t in law)
value=sum((1-t[4])/2 for t in law)/2
true_node_min=Q(3,8)
assert value==Q(1,4)<true_node_min
assert value>=Q(1,2)-Q(3,2)
# All support families on 4 originals with row size <= 3.
rows=[i for i in range(1,16) if i.bit_count()<=3]
families=0
for choose in range(1<<len(rows)):
    selected=[row for j,row in enumerate(rows) if choose>>j&1]
    basis={}; original_basis=[]; union=0
    for row in selected:
        union|=row; t=row
        while t:
            pivot=t.bit_length()-1
            if pivot not in basis:
                basis[pivot]=t; original_basis.append(row); break
            t^=basis[pivot]
    basis_union=0
    for row in original_basis: basis_union|=row
    assert union==basis_union
    assert union.bit_count()<=3*len(basis)
    fiber=sum(all((row&w).bit_count()%2==0 for row in selected) for w in range(16))
    assert fiber==2**(4-len(basis))
    families+=1
assert 384*3**24<2**64
out={'symbolic_identities':2,'exact_quadratic_box_vertex_checks':checks,'support_families':families,'non_graph_law_cost':str(value),'true_node_graph_min':str(true_node_min),'integer_deletion_inequality':True,'limits':'Exact finite checks supplement the analytic review; they do not establish universal theorems.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
