"""Independent vertex-mixture LP audit of strong baselines on integral networks."""
from fractions import Fraction as F
import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef,optimize_independent_states,membership_ef
rng=np.random.default_rng(62991)
optchecks=memberchecks=statechecks=0
for seed in range(12):
    E=6;m=4;n=4
    arcs=[(int(rng.integers(3)),int(rng.integers(3)),int(rng.integers(1,3))) for _ in range(E)]
    A=np.zeros((n,E),dtype=int)
    for e,(u,v,c) in enumerate(arcs):A[u,e]+=1;A[v,e]-=1
    reference=np.array([int(rng.integers(c+1)) for u,v,c in arcs])
    b=A@reference
    obs=[(e,j) for e in range(E) for j in (0,2) if rng.random()<.5]
    inst=Instance(arcs,b,m,obs,reference)
    flows=[np.array(v,dtype=int) for v in itertools.product(*(range(c+1) for u,v,c in arcs)) if np.array_equal(A@v,b)]
    # Incidence integrality means these integer points generate the flow polytope.
    columns=[]
    for j in range(m+1):
        yy=np.array([int(k==j) for k in range(m)])
        for flow in flows:columns.append(np.r_[flow,yy,[flow[e]*yy[k] for e,k in obs]])
    V=np.array(columns,dtype=float).T
    for fixed in (None,[F(1,5)]*m):
        for coupling in (False,True):
            objective=rng.normal(size=E+m+len(obs))
            extras=[]
            if coupling:
                center=np.r_[reference,np.ones(m)/5,[reference[e]/5 for e,j in obs]]
                for _ in range(3):
                    row=rng.normal(size=len(objective));extras.append((row,float(row@center+F(1,9))))
            eq=[np.ones(V.shape[1])];rhs=[1.]
            if fixed is not None:
                eq.extend(V[E:E+m]);rhs.extend(map(float,fixed))
            ref=linprog(objective@V,A_eq=np.array(eq),b_eq=rhs,A_ub=np.array([c@V for c,r in extras]) if extras else None,b_ub=[r for c,r in extras] if extras else None,bounds=(0,None),method='highs')
            assert ref.status==0
            for merge in [False,True]:
                result=optimize_ef(inst,objective,fixed,merge=merge,extra_rows=extras)
                assert result.status==0 and abs(result.fun-ref.fun)<1e-7
                assert all(c@result.original_point<=r+1e-7 for c,r in extras)
                optchecks+=1
            if fixed is not None and not coupling:
                result=optimize_independent_states(inst,objective,fixed)
                assert result.status==0 and abs(result.fun-ref.fun)<1e-7
                statechecks+=1
    for y in [(F(1,2),0,F(1,2),0),(F(1,3),0,0,F(1,3)),(0,F(1),0,0),(0,0,0,0)]:
        x=[F(int(v)) for v in reference]
        z=[x[e]*y[j] for e,j in obs]
        for perturb in [False,True]:
            zz=list(z)
            if perturb and zz:zz[0]+=F(1,4)
            point=np.array(x+list(y)+zz,dtype=float)
            ref=linprog(np.zeros(V.shape[1]),A_eq=np.vstack((np.ones(V.shape[1]),V)),b_eq=np.r_[1.,point],bounds=(0,None),method='highs')
            assert ref.status in (0,2)
            for merge,reduce in itertools.product([False,True],repeat=2):
                result=membership_ef(inst,x,y,zz,merge=merge,two_state=reduce)
                assert result.status==ref.status,(seed,y,perturb,merge,reduce)
                memberchecks+=1
record={'status':'PASS','independent_reference':'Explicit graph-point convex combinations using all integer feasible flow points; no disaggregation row builder used in reference','optimization_comparisons':optchecks,'fixed_y_independent_network_comparisons':statechecks,'membership_comparisons':memberchecks,'scope':['free and fixed y','all original y objective terms','three coupled dense x/y/z rows','global state merging','two-state elimination','loops and parallel arcs','isolated vertex','zero-weight and globally unused labels'],'qualification':'LP classifications and objective comparisons are numerical, with tolerance 1e-7 for objectives.'}
Path(__file__).with_name('baseline-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
