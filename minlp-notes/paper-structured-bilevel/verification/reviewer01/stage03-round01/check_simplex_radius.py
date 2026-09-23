"""Independent rational check of overlapping simplex covers and radius labels.

Uses a 2D square surrogate cell, full-rank signed dense perturbation, and exact
KKT checks. This finite diagnostic does not establish asymptotic complexity.
"""
from itertools import combinations, product
from pathlib import Path
import json
import sympy as s

N = 8
x, u = s.symbols('x u')
y = s.Matrix([x/4, u/4, (1-x)/4, (1-u)/4, s.Rational(1,2), s.Rational(2,5), 0, 1])
a = -y
a[6] = 1
a[7] = -2
E = s.Matrix(N, N, lambda i,j: s.Rational(((-1)**i*(i+1)) if i == j else ((i+j)%3-1), 3000))
assert E == E.T and E.rank() == N
Q = s.eye(N) + E
eps = max(sum(abs(E[i,j]) for j in range(N)) for i in range(N))
vertices = list(product((s.Integer(0), s.Integer(1)), repeat=2))
nominal = ['F'] * 6 + ['L', 'U']
transition = []
for v in vertices:
    yy = y.subs({x:v[0],u:v[1]})
    gg = (y+a).subs({x:v[0],u:v[1]})
    transition.append({i for i in range(N) if yy[i] in (0,1) and gg[i] == 0})
q = max(map(len,transition))
simplexes = []
margins = []
for n in (1,2,3):
    for ids in combinations(range(4),n):
        matrix = s.Matrix.hstack(*(s.Matrix([*vertices[i],1]) for i in ids))
        if matrix.rank() < n:
            continue
        J = set.union(*(transition[i] for i in ids))
        assert len(J) <= 3*q
        simplexes.append((ids,J,matrix))
        for i in set(range(N))-J:
            for j in ids:
                yy=y.subs({x:vertices[j][0],u:vertices[j][1]})
                gg=(y+a).subs({x:vertices[j][0],u:vertices[j][1]})
                ms=[yy[i],1-yy[i]] if nominal[i]=='F' else [gg[i] if nominal[i]=='L' else -gg[i]]
                assert all(m > 0 for m in ms)
                margins.extend(ms)
sigma=min(margins)
R=3
eps0=min(s.Rational(1,2),sigma/(4*R*2))
assert eps <= eps0
assert 2*eps*R <= sigma/2 and 4*eps*R <= sigma/2

# Exact affine KKT candidate list; final two statuses are checked, not assumed.
patterns=[]
for lower in product((False,True),repeat=4):
    fixed=[i for i in range(4) if lower[i]]+[6,7]
    free=[i for i in range(N) if i not in fixed]
    zz=s.zeros(N,1);zz[7]=1
    ff=Q[free,free].inv()*(-a[free,:]-Q[free,[7]])
    for i,value in zip(free,ff):zz[i]=s.expand(value)
    patterns.append(zz)


def exact_response(v):
    for candidate in patterns:
        z=candidate.subs({x:v[0],u:v[1]})
        g=Q*z+a.subs({x:v[0],u:v[1]})
        if all(0<=z[i]<=1 and (g[i]>=0 if z[i]==0 else g[i]<=0 if z[i]==1 else g[i]==0) for i in range(N)):
            return z,g
    raise AssertionError(v)


def in_simplex(v,matrix):
    try:sol,params=matrix.gauss_jordan_solve(s.Matrix([*v,1]))
    except ValueError:return False
    return params.rows==0 and all(w>=0 for w in sol)

grid=list(product([s.Rational(i,4) for i in range(5)],repeat=2))
assert all(any(in_simplex(v,mat) for _,_,mat in simplexes) for v in grid)
checks=0
for ids,J,mat in simplexes:
    center=tuple(sum(vertices[j][i] for j in ids)/len(ids) for i in range(2))
    for v in [vertices[j] for j in ids]+[center]:
        z,g=exact_response(v)
        yy=y.subs({x:v[0],u:v[1]});gg=(y+a).subs({x:v[0],u:v[1]})
        assert sum(t*t for t in z-yy) <= (2*eps*R)**2
        assert sum(t*t for t in g-gg) <= (4*eps*R)**2
        for i in set(range(N))-J:
            assert (0<z[i]<1 and g[i]==0) if nominal[i]=='F' else (z[i]==0 and g[i]>0) if nominal[i]=='L' else (z[i]==1 and g[i]<0)
        checks+=1

report={'simplexes':len(simplexes),'grid_coverage_points':len(grid),'exact_response_checks':checks,'q':q,'max_transition_union':max(len(J) for _,J,_ in simplexes),'sigma':str(sigma),'epsilon0':str(eps0),'perturbation_norm':str(eps),'perturbation_rank':E.rank()}
print(json.dumps(report,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
