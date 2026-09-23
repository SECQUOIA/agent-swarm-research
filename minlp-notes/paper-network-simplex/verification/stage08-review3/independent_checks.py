"""Independent exact checks transcribed from the frozen manuscript, no production imports."""
import itertools
import json
from pathlib import Path
import sympy as S

out = {}
fib_cases = []
for q in range(3, 13):
    n = 2*q-1
    primary = list(range(q))
    aux = [q] + list(range(q+1, n))
    cols = [{q, 0}, {q, 1}]
    for i in range(3, q+1):
        hi = q+i-2
        cols.extend([{hi, i-1}, {hi, i-2, i-3}])
    cols.append({q-1, q-2})
    D = S.Matrix(n, n, lambda i,j: int(i in cols[j]))
    F = [0, 1, 1]
    for i in range(3,q+2): F.append(F[-1]+F[-2])
    gamma = F[q+1]
    alpha = S.Matrix(F[1:q+1] + [gamma-1] + [gamma-F[i] for i in range(3,q+1)])
    K = S.ones(n)-D
    assert sum(D)==5*q-4
    assert D.T*alpha == gamma*S.ones(n,1)
    assert sum(alpha)==(q-1)*gamma+1
    assert K.det()!=0 and D.det()!=0
    inv = K.inv()
    beta = sum(alpha)-gamma
    assert K.T*alpha == beta*S.ones(n,1)
    a,c = S.Rational(1,2*n),S.Rational(1,8*n)
    norm = max(sum(abs(inv[i,j]) for j in range(n)) for i in range(n))
    R = S.Integer(F[q]); eps = a/(16*(1+R)*(1+norm))
    rr, ss = q-1, 0
    count=0
    for dr,ds in itertools.product([-eps/2,0,eps/2], repeat=2):
        delta=S.zeros(n,1); delta[rr]=dr;delta[ss]=ds
        if R*dr+ds<0:
            assert (alpha.T*delta)[0]<0
            continue
        tau=S.zeros(n,1);tau[ss]=R*dr+ds
        w=a*S.ones(n,1)+inv*(-delta+tau)
        assert sum(w)==S.Rational(1,2)
        flows=S.zeros(n,n)
        for i in range(n):
            for j in range(n): flows[i,j]=w[j] if K[i,j] else c
        flows[rr,n-1]+=dr;flows[ss,0]+=ds
        chosen=next(j for j in range(n) if K[ss,j])
        flows[ss,chosen]-=tau[ss]
        for i in range(n):
            rowtarget=sum(K[i,j] for j in range(n))*a+sum(D[i,j] for j in range(n))*c
            assert sum(flows[i,j] for j in range(n))==rowtarget
            for j in range(n): assert 0<=flows[i,j]<=w[j]<=2*a
        assert all(0<=2*a-w[j]<=2*a for j in range(n))
        count+=1
    # Construct the split/subdivided graph and verify counts, acyclicity, simplicity.
    nodes=[('v',0),('v',n)]
    for i in range(1,n): nodes.extend([('in',i),('out',i)])
    nodes += [('sub',i) for i in range(1,n+1)]
    edges=[]
    for i in range(1,n+1):
        tail=('v',0) if i==1 else ('out',i-1)
        head=('v',n) if i==n else ('in',i)
        edges.extend([(tail,head),(tail,('sub',i)),(('sub',i),head)])
    edges += [(('in',i),('out',i)) for i in range(1,n)]
    edges += [(('v',0),('v',n))]
    deg={v:0 for v in nodes}
    for u,v in edges: deg[u]+=1;deg[v]+=1
    assert len(nodes)==6*q-3 and len(edges)==8*q-4
    assert max(deg.values())==3 and len(set(edges))==len(edges)
    assert len(edges)-len(nodes)+1==2*q
    fib_cases.append(dict(q=q,ratio=F[q],feasible_local_witnesses=count,vertices=len(nodes),arcs=len(edges)))
out['fibonacci']=fib_cases

# Enumerate minimal positive dependencies independently in each full reduced universe.
circuits={}
for m in range(1,4):
    normals=list(dict.fromkeys([tuple(int(i in sub) for i in range(m)) for k in range(1,m+1) for sub in itertools.combinations(range(m),k)]+[tuple(-int(i==j) for i in range(m)) for j in range(m)]+[(-1,)*m]))
    found=[]
    for size in range(2,m+2):
        for ids in itertools.combinations(range(len(normals)),size):
            ns=S.Matrix([normals[i] for i in ids]).T.nullspace()
            if len(ns)!=1: continue
            v=ns[0]
            if all(x<0 for x in v):v=-v
            if not all(x>0 for x in v):continue
            v=v*S.ilcm(*[x.q for x in v]); g=S.igcd(*list(v));v=v/g
            found.append((ids,list(map(int,v))))
    assert len(found)==[1,5,16][m-1]
    circuits[m]=dict(normals=len(normals),circuits=len(found),maximum_weight=max(max(v) for _,v in found))
out['reduced_circuit_enumeration']=circuits

# Sharp five-product K4: exact sufficiency and necessary support at a grid.
C=S.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
v=S.Matrix([S.Rational(1,2)]*3+[S.Rational(1,4),S.Rational(1,2),S.Rational(1,2)])
agg=S.Matrix([S.Rational(1,6),S.Rational(1,24),S.Rational(1,8)])
count=0
for p,q in itertools.product([S.Rational(i,1000) for i in range(-10,11)],repeat=2):
    if 2*p+q<0:continue
    st=[S.Matrix([p,q,p]),S.Matrix([q/2,-q/2,0]),S.Matrix([S.Rational(1,6)-p-q/2,S.Rational(1,24)-q/2,S.Rational(1,8)-p])]
    assert sum(st,S.zeros(3,1))==agg
    for theta in st:
        f=v/3+C*theta
        assert all(0<=x<=S.Rational(1,3) for x in f)
    count+=1
out['sharp_k4_feasible_grid_witnesses']=count
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
