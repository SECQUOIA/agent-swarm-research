"""Independent exact sparse-merger audits and path-vertex LP comparisons."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,random
import numpy as np
from scipy.optimize import linprog
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import membership_ef,optimize_ef

rng=random.Random(619037)
manifest=json.loads(Path('paper-network-simplex/verification/stage06-validation.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in manifest['sha256'].items())
decompositions=cuts=numerical_memberships=0
for m in (0,1,6,53):
    for trial in range(16):
        L=1+trial%4;a=min(m,trial%5)
        labels=rng.sample(range(m),a)
        obs={(e,j) for j in labels for e in range(2*L+1) if rng.random()<.4}
        # Ensure each chosen label occurs, including nonconsecutive labels.
        obs.update((2*L,j) for j in labels if not any(k==j for _,k in obs))
        model=FlatChainSimplex(L,m,obs)
        raw=[rng.randrange(4) for _ in range(m+1)]
        if not sum(raw):raw[-1]=1
        weights=tuple(F(v,sum(raw)) for v in raw)
        flows=[]
        for j in range(m+1):
            w=F(rng.randrange(7),6);row=[]
            for i in range(L):
                aa=w*F(rng.randrange(6),5);row.extend((aa,w-aa))
            flows.append(tuple(row)+(1-w,))
        x=tuple(sum(weights[j]*flows[j][e] for j in range(m+1)) for e in range(2*L+1))
        z={(e,j):weights[j]*flows[j][e] for e,j in obs}
        candidates=[Point(x,weights[:-1],z)]
        if obs:
            altered=dict(z);key=rng.choice(sorted(obs));altered[key]+=F(1,37)
            candidates.append(Point(x,weights[:-1],altered))
        for p in candidates:
            answer=model.separate(p)
            assert answer.feasible==model.separate(p,decompose=False).feasible
            if answer.feasible:
                dec=answer.decomposition
                assert dec.weights==weights and len(dec.group_profile)==len(model.labels)+1
                assert all(len(row)==len(model.labels)+1 for row in dec.group_arc_a)
                recovered={j:dec.flow(j) for j in dec.positive_states()}
                for row in recovered.values():
                    assert all(0<=v<=1 for v in row)
                    assert all(row[2*i]+row[2*i+1]+row[-1]==1 for i in range(L))
                assert all(sum(weights[j]*row[e] for j,row in recovered.items())==p.x[e] for e in range(2*L+1))
                assert all((weights[j]*recovered[j][e] if weights[j] else 0)==v for (e,j),v in p.z.items())
                unused=[j for j in recovered if j not in model.labels]
                if unused:assert all(recovered[j]==recovered[unused[0]] for j in unused)
                decompositions+=1
            else:
                cut=answer.cut;assert cut.evaluate(p)>0
                # Optimize the cut exactly over every simplex vertex; for a
                # chain path independently select the better arc in each pair.
                for j in range(m+1):
                    coeff=[cut.coefficients.get(('x',e),0)+cut.coefficients.get(('z',e,j),0) for e in range(2*L+1)]
                    value=cut.constant+cut.coefficients.get(('y',j),0)+max(coeff[-1],sum(max(coeff[2*i:2*i+2]) for i in range(L)))
                    assert value<=0
                if len(model.labels)<=3:
                    assert all(abs(v)<=1 for k,v in cut.coefficients.items() if k[0] in ('x','z'))
                cuts+=1
            if m<=6:
                instance=Instance(list(model.arcs),-np.asarray(model.balances,float),m,list(model.observations),np.asarray(p.x,float))
                for merge in (False,True):
                    for two in (False,True):
                        result=membership_ef(instance,p.x,p.y,[p.z[o] for o in instance.observations],merge=merge,two_state=two)
                        assert result.status==(0 if answer.feasible else 2)
                        numerical_memberships+=1

# An independent convex-combination LP over actual path/simplex vertices
# checks free/fixed original y and coupled x/y/z rows of the strong baselines.
L,m=3,6;obs=[(0,1),(2,5),(6,1)]
arcs=[(i,i+1,1) for i in range(L) for _ in range(2)]+[(0,L,1)]
inst=Instance(arcs,np.array([1,0,0,-1]),m,obs,np.array([.25]*6+[.5]))
paths=[(0,)*6+(1,)]
paths += [tuple(int(e%2==selection[e//2]) for e in range(6))+(0,) for selection in product((0,1),repeat=L)]
vertices=[]
for path in paths:
    for state in range(m+1):
        yy=tuple(int(j==state) for j in range(m))
        vertices.append(path+yy+tuple(path[e]*yy[j] for e,j in obs))
V=np.array(vertices,float).T
optimization_comparisons=0
for trial in range(8):
    cost=np.array([rng.randrange(-8,9)/7 for _ in range(len(V))])
    center=V.mean(axis=1)
    rows=[np.array([rng.randrange(-3,4)/5 for _ in range(len(V))]) for _ in range(2)]
    rhs=[float(row@center+.1) for row in rows]
    for fixed in (False,True):
        eq=np.ones((1,V.shape[1]));beq=np.ones(1)
        yf=center[7:7+m] if fixed else None
        if fixed:eq=np.vstack((eq,V[7:7+m]));beq=np.r_[beq,yf]
        independent=linprog(V.T@cost,A_ub=np.array(rows)@V,b_ub=rhs,A_eq=eq,b_eq=beq,bounds=(0,None),method='highs')
        assert independent.status==0
        for merge in (False,True):
            result=optimize_ef(inst,cost,y_fixed=yf,merge=merge,extra_rows=list(zip(rows,rhs)))
            assert result.status==0 and abs(result.fun-independent.fun)<1e-7
            optimization_comparisons+=1
out={'status':'PASS','dependency_hashes':len(manifest['sha256']),
     'exact_decompositions':decompositions,'exact_globally_valid_cuts':cuts,
     'numerical_membership_comparisons':numerical_memberships,
     'independent_path_vertex_optimization_comparisons':optimization_comparisons}
Path(__file__).with_name('check-output.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
