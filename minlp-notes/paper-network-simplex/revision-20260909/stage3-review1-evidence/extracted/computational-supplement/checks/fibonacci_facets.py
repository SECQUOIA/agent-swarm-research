"""Independent exact validation against all path--simplex vertices.

SciPy locates a candidate supporting row. SymPy rational arithmetic alone
validates the row, its face dimension, and its retained-product ratio.
No manuscript/production code is imported.
"""
from itertools import product
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import linprog


def instance(q):
    n = 2*q-1
    rows = [('P', i) for i in range(1, q+1)] + [('H', 0)] + [('H', i) for i in range(3, q+1)]
    columns = [[('H', 0), ('P', 1)], [('H', 0), ('P', 2)]]
    for i in range(3, q+1):
        columns.extend([[('H', i), ('P', i)], [('H', i), ('P', i-1), ('P', i-2)]])
    columns.append([('P', q), ('P', q-1)])
    d = sp.Matrix([[int(row in col) for col in columns] for row in rows])
    obs = [(i,j) for i in range(n) for j in range(n) if d[i,j]]
    assert len(obs) == 5*q-4
    f = [0,1,1]
    while len(f) <= q+1:
        f.append(f[-1]+f[-2])
    alpha = sp.Matrix([f[i] if kind == 'P' else f[q+1]-(1 if i == 0 else f[i]) for kind,i in rows])
    k = sp.ones(n)-d
    assert d.det() and k.det()
    assert d.T*alpha == sp.ones(n,1)*f[q+1]
    assert k.T*alpha == sp.ones(n,1)*(sum(alpha)-f[q+1])
    a,c = sp.Rational(1,2*n),sp.Rational(1,8*n)
    xa = [sum(k.row(i))*a + sum(d.row(i))*c for i in range(n)]
    center = sp.Matrix([v for value in xa for v in (value,sp.Rational(1,2)-value)] + [sp.Rational(1,2)] + [sp.Rational(1,n)]*n + [c]*len(obs))
    vertices=[]
    # Every unit acyclic flow vertex is either the bypass or one binary path.
    paths=[[v for bit in bits for v in (bit,1-bit)]+[0] for bits in product((0,1),repeat=n)]
    paths.append([0]*(2*n)+[1])
    for path in paths:
        for state in range(-1,n):
            vertices.append(path + [int(state==j) for j in range(n)] + [path[2*i]*int(state==j) for i,j in obs])
    vertices=sp.Matrix(vertices)
    iu=2*n+1+n+obs.index((q-1,n-1))
    iv=2*n+1+n+obs.index((0,0))
    dif=vertices-sp.ones(vertices.rows,1)*center.T
    eq=np.zeros((2,vertices.cols));eq[0,iu]=1;eq[1,iv]=1
    sol=linprog(np.zeros(vertices.cols),A_ub=-np.array(dif,dtype=float),b_ub=np.zeros(vertices.rows),A_eq=eq,b_eq=[f[q],1],bounds=[(None,None)]*vertices.cols,method='highs')
    assert sol.success, sol.message
    normal=sp.Matrix([sp.Rational(float(v)).limit_denominator(10**6) for v in sol.x])
    slack=dif*normal
    assert min(slack)>=0 and normal[iu]==f[q] and normal[iv]==1
    tight=[i for i,x in enumerate(slack) if x==0]
    hull_rank=(vertices[1:,:]-sp.ones(vertices.rows-1,1)*vertices[0,:]).rank()
    tv=vertices[tight,:]
    face_rank=(tv[1:,:]-sp.ones(tv.rows-1,1)*tv[0,:]).rank()
    assert face_rank == hull_rank-1
    for equation in (vertices[1:,:]-sp.ones(vertices.rows-1,1)*vertices[0,:]).nullspace():
        assert equation[iu] == 0 and equation[iv] == 0
    # Independently construct the simple graph, with distinct join sides.
    nodes=['s','t']+[f'{side}{i}' for i in range(1,n) for side in ('in','out')]+[f'mid{i}' for i in range(n)]
    arcs=[]
    for i in range(n):
        tail='s' if i==0 else f'out{i}'
        head='t' if i==n-1 else f'in{i+1}'
        arcs.extend([(tail,head),(tail,f'mid{i}'),(f'mid{i}',head)])
    arcs += [(f'in{i}',f'out{i}') for i in range(1,n)] + [('s','t')]
    assert len(nodes)==3*n and len(arcs)==4*n and len(set(arcs))==len(arcs)
    assert max(sum(v in edge for edge in arcs) for v in nodes)==3
    incidence=sp.Matrix([[int(v==head)-int(v==tail) for tail,head in arcs] for v in nodes])
    demand=sp.Matrix([-1,1]+[0]*(len(nodes)-2))
    for path in paths:
        expanded=[v for i in range(n) for v in (path[2*i],path[2*i+1],path[2*i+1])]+[1-path[-1]]*(n-1)+[path[-1]]
        assert incidence*sp.Matrix(expanded)==demand
    assert len(arcs)-len(nodes)+1==2*q
    # At the center, a small negative U perturbation is exactly excluded.
    eps=sp.Rational(1,10000*n)
    outside=center.copy();outside[iu]-=eps
    assert ((outside-center).T*normal)[0] == -f[q]*eps
    return {'q':q,'vertices':vertices.rows,'ambient_coordinates':vertices.cols,
      'affine_dimension':hull_rank,'support_face_dimension':face_rank,
      'is_facet':face_rank==hull_rank-1,'product_ratio':f[q],
      'minimum_exact_vertex_slack':str(min(slack)),
      'normal':list(map(str,normal)), 'rhs':str((center.T*normal)[0]),
      'u_index':iu,'v_index':iv,'tight_vertices':len(tight),
      'affine_equation_coefficients_on_free_products_zero':True,
      'simple_graph':{'vertices':len(nodes),'arcs':len(arcs),'max_degree':3,'exact_path_lifts':len(paths)}}


if __name__=='__main__':
    results=[instance(q) for q in (3,4)]
    out={'status':'PASS','arithmetic':'Exact rational final checks; floating-point LP only proposes row','instances':results}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
