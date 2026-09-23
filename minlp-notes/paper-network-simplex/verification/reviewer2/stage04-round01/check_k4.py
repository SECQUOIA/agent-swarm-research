"""Independent exact graph-level check of both K4 coefficient examples."""
import itertools
import json
from pathlib import Path
import sympy as s
R=s.Rational
edges=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=s.zeros(4,6)
for e,(u,vv) in enumerate(edges): A[u,e]-=1; A[vv,e]+=1
C=s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
assert A*C==s.zeros(4,3) and C.rank()==3
h=s.ones(3,1)
records=[]
for variant in ['five','seven']:
    if variant=='five':
        v=s.Matrix([R(1,2)]*3+[R(1,4),R(1,2),R(1,2)])
        b=s.Matrix([-R(5,4),-R(3,4),R(1,2),R(3,2)])
        aggregate=s.Matrix([R(1,6),R(1,24),R(1,8)])
        weight=R(1,3); origin=R(1,6); denominator=960
        fixed={(4,1):R(1,6),(2,2):R(1,6),(3,2):R(1,12)}
    else:
        v=s.ones(6,1)/2
        b=s.Matrix([-R(3,2),-R(1,2),R(1,2),R(3,2)])
        aggregate=s.Matrix([R(1,8),0,R(1,8)])
        weight=R(1,4); origin=R(1,8); denominator=320
        fixed={(4,1):R(1,8),(0,2):R(1,8),(5,2):R(1,8),(2,3):R(1,8),(3,3):R(1,8)}
    assert A*v==b
    x=v+C*aggregate
    assert A*x==b and all(0<=t<=1 for t in x)
    valid=invalid=0
    for i,j in itertools.product(range(-9,10),repeat=2):
        p,q=R(i,denominator),R(j,denominator)
        w=2*p+q
        # Upper support of the residual obtained directly from arcs 12 and 03.
        residual_upper=weight*((1-v[0])+v[5])
        assert (h.T*aggregate)[0]==residual_upper
        if w<0:
            # Every admissible explicit state has h-coordinate w,0 (or w,0,0).
            # Thus residual h-coordinate exceeds its exact arc-bound upper bound.
            assert (h.T*aggregate)[0]-w>residual_upper
            invalid+=1
            continue
        if variant=='five':
            theta=[s.Matrix([R(1,6)-p-q/2,R(1,24)-q/2,R(1,8)-p]),s.Matrix([p,q,p]),s.Matrix([q/2,-q/2,0])]
        else:
            aa=R(1,8)-w/2
            theta=[s.Matrix([aa,0,aa]),s.Matrix([p,q,p]),s.Matrix([0,-q/2,q/2]),s.Matrix([q/2,-q/2,0])]
        assert sum(theta,s.zeros(3,1))==aggregate
        flows=[weight*v+C*t for t in theta]
        assert sum(flows,s.zeros(6,1))==x
        for f in flows:
            assert A*f==weight*b and all(0<=t<=weight for t in f)
        observations=dict(fixed); observations[(0,1)]=p+origin; observations[(1,1)]=q+origin
        for (e,k),value in observations.items(): assert flows[k][e]==value
        for k in range(2,len(theta)): assert (h.T*theta[k])[0]==0
        assert (h.T*theta[1])[0]==w
        valid+=1
    records.append({'variant':variant,'exact_graph_witnesses':valid,'exact_section_infeasibility_certificates':invalid})
# Independent symbolic derivation of a valid original-coordinate inequality for
# the five-observation model. The residual support bound supplies the only
# inequality, while state balances identify all other terms.
x12,x13,x23,y1,y2,U,V,z02,z23,z01=s.symbols('x12 x13 x23 y1 y2 U V z02 z23 z01')
expr=2*U+V+z02+z23+z01-(x12+x13+x23-R(5,2)+3*y1+R(7,4)*y2)
section=expr.subs({x12:R(2,3),x13:R(13,24),x23:R(5,8),y1:R(1,3),y2:R(1,3),z02:R(1,6),z23:R(1,6),z01:R(1,12)})
assert s.expand(section)==2*U+V-R(1,2)
record={'status':'PASS','cases':records,'five_product_global_cut':'2 z12,1 + z13,1 + z02,1 + z23,2 + z01,2 >= x12+x13+x23 - 5/2 + 3 y1 + (7/4)y2','warning':'This verification does not claim the displayed global inequality itself is facet-defining; the manuscript section lemma supplies existence of a facet with the ratio.'}
Path(__file__).with_name('result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
