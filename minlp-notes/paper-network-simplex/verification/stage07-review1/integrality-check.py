"""Independent exact checks of the new proof's perturbation and refinement steps."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as s

graphs = [
    (2, [(0,1),(0,1)], [1,1]),
    (3, [(0,1),(1,2),(2,0),(0,2)], [1,1,1,1]),
    (4, [(0,1),(0,1),(1,1),(2,3)], [1,1,2,0]),
    (4, [(0,1),(1,2),(2,0),(0,2),(2,3),(3,0)], [1]*6),
    (3, [(0,0),(1,1),(1,2),(1,2)], [2,0,1,1]),
]
checked=0; support_checks=0
for n, arcs, u in graphs:
    E=len(arcs); A=s.zeros(n,E)
    for e,(tail,head) in enumerate(arcs): A[tail,e]-=1; A[head,e]+=1
    cache={}
    for digits in product(range(4),repeat=E):
        x=tuple(F(k*cap,3) for k,cap in zip(digits,u))
        b=A*s.Matrix(x)
        if any(v.q!=1 for v in b): continue
        nonintegral=tuple(e for e,v in enumerate(x) if v.denominator!=1)
        if not nonintegral:continue
        if nonintegral not in cache:
            null=A[:,nonintegral].nullspace()
            assert null, (arcs,x,b)
            d=[F(0)]*E
            for e,value in zip(nonintegral,null[0]): d[e]=F(value)
            assert any(d) and A*s.Matrix(d)==s.zeros(n,1)
            cache[nonintegral]=d;support_checks+=1
        d=cache[nonintegral]
        epsilon=min(min(x[e],u[e]-x[e])/abs(d[e]) for e in range(E) if d[e])/2
        assert epsilon>0
        lo=[x[e]-epsilon*d[e] for e in range(E)]
        hi=[x[e]+epsilon*d[e] for e in range(E)]
        assert lo!=hi
        assert A*s.Matrix(lo)==b==A*s.Matrix(hi)
        assert all(0<=lo[e]<=u[e] and 0<=hi[e]<=u[e] for e in range(E))
        assert all((lo[e]+hi[e])/2==x[e] for e in range(E))
        checked+=1

# Direct refinement of several simplex-state flows on a parallel-pair-plus-loop
# polytope. There are four integral vertices (a,1-a,t), a,t in {0,1}.
refinements=0
obs=[(0,0),(1,0),(2,0),(0,1),(2,1)]
for state_weights in [(F(1,2),F(0),F(1,2)),(F(0),F(0),F(1)),
                      (F(1,3),F(1,3),F(1,3))]:
    original=[F(0)]*(3+2+len(obs));refined=[F(0)]*len(original)
    for state,w in enumerate(state_weights):
        y=[F(state==j) for j in range(2)]
        a,t=F(state+1,5),F(state+1,4)
        x=[a,1-a,t]
        p=x+y+[x[e]*y[j] for e,j in obs]
        original=[v+w*q for v,q in zip(original,p)]
        for ai,ti in product((0,1),repeat=2):
            alpha=(a if ai else 1-a)*(t if ti else 1-t)
            xv=[F(ai),F(1-ai),F(ti)]
            vertex=xv+y+[xv[e]*y[j] for e,j in obs]
            refined=[v+w*alpha*q for v,q in zip(refined,vertex)]
    assert original==refined
    refinements+=1
# m=0 does not mean one integral graph point suffices.
x=(F(1,3),F(2,3));assert any(v.denominator!=1 for v in x)
assert x==tuple(F(1,3)*a+F(2,3)*b for a,b in zip((1,0),(0,1)))
result=dict(graphs=len(graphs),nonintegral_points_with_two_sided_perturbation=checked,
            distinct_fractional_supports=support_checks,exact_state_refinements=refinements,
            m0_integral_count_counterexample=True)
print(json.dumps(result,indent=2))
(Path(__file__).parent/'integrality-check.json').write_text(json.dumps(result,indent=2)+'\n')
