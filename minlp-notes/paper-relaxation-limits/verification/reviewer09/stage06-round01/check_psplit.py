"""Independent exact finite checks; no solver and no asymptotic certification."""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path


def solve(rows, rhs):
    n = len(rows)
    a = [list(map(Q, r)) + [Q(b)] for r, b in zip(rows, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [v / scale for v in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [u - scale*v for u, v in zip(a[i], a[j])]
    return tuple(r[-1] for r in a)


def auxiliary_vertices(q, r, d):
    n, U = q+2, (d+r)**2
    rows, rhs = [], []
    for i in range(n):
        row = [Q(0)]*n
        row[i] = -1
        rows.append(row); rhs.append(0)
    for i in range(2):
        row = [Q(0)]*n
        row[i] = 1
        rows.append(row); rhs.append(U)
    rows.extend([[0, 0]+[1]*q, [1]*n])
    rhs.extend([r*r, U+r*r])
    vertices = set()
    for active in combinations(range(len(rows)), n):
        x = solve([rows[i] for i in active], [rhs[i] for i in active])
        if x is not None and all(sum(a*b for a,b in zip(row,x)) <= b
                                 for row,b in zip(rows,rhs)):
            vertices.add(x)
    assert vertices
    # Every vertex of the proposed polytope belongs to one original disjunct.
    for a,b,*c in vertices:
        assert a+sum(c) <= r*r or b+sum(c) <= r*r
    return len(vertices)


counts=[]
for q in range(1,5):
    for r,d in [(Q(1),Q(3)), (Q(2,3),Q(7,4)), (Q(5,2),Q(9))]:
        counts.append(dict(transverse=q,r=str(r),d=str(d),
                           vertices=auxiliary_vertices(q,r,d)))

matrix=((Q(3,5),Q(4,5)),(Q(4,5),Q(-3,5)))
assert all(sum(matrix[i][k]*matrix[k][j] for k in range(2)) == (i==j)
           for i in range(2) for j in range(2))
assert Q(1,2)-Q(4,9)==Q(1,18)
for D in [Q(2),Q(7,3),Q(10),Q(1000)]:
    v=(3*D,4*D); p=(2*D,4*D/3)
    t,w=[sum(a*b for a,b in zip(row,p)) for row in matrix]
    assert t==34*D/15 and w==4*D/5 and 0<=t<=5*D
    assert all(max(x*x,(x-y)**2) <= y*y/2 for x,y in zip(p,v))
    assert all(2*max(x*x,(x-y)**2) <= (y+1)**2 for x,y in zip(p,v))

report={"arithmetic":"exact rational", "auxiliary_hull_vertex_checks":counts,
        "rational_witness_parameters":["2","7/3","10","1000"],
        "limitations":"Finite dimensions and parameters only; the universal convex-image and Hausdorff claims require the analytic proofs."}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
