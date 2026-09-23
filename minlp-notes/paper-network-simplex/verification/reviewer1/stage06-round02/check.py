"""Reviewer-owned original-vertex LP checks; never writes production artifacts."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib, json, sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'code'))
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef

manifest = json.loads((ROOT/'paper-network-simplex/verification/stage06-validation.json').read_text())
for filename, expected in manifest['sha256'].items():
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest() == expected, filename

rng = np.random.default_rng(906021)
counts = dict(dependency_hashes=len(manifest['sha256']), fixed_vertex_comparisons=0,
              free_vertex_comparisons=0, reconstructed_points=0, infeasible_rows=0)
# The four vertices are immediate from x0+x1=2 and independent 0<=x2<=3.
# This also exercises parallel arcs, a loop, and an isolated balance equation.
flow_vertices = np.array([[a, 2-a, t] for a,t in product([0.,2.], [0.,3.])])
for m, obs, families in [
    (6, [(0,1),(1,5),(2,1),(2,0)], [
        [F(0)]*6,
        [F(0),F(0),F(1),F(0),F(0),F(0)],
        [F(0),F(1,2),F(0),F(0),F(0),F(1,2)],
        [F(0),F(1,4),F(1,4),F(0),F(0),F(0)],
        [F(1,8)]*6,
        [F(1,3),F(1,3),F(0),F(0),F(0),F(1,3)]]),
    (6, [], [[F(0)]*6, [F(0),F(0),F(1),F(0),F(0),F(0)], [F(1,8)]*6]),
    (0, [], [[]]),
]:
    inst = Instance([(0,1,2),(0,1,2),(1,1,3)], np.array([2.,-2.,0.]), m,
                    obs, np.array([1.,1.,1.5]))
    E=3; N=E+m+len(obs)
    vertices=[]
    for state in range(m+1):
        y=np.zeros(m)
        if state<m: y[state]=1
        for x in flow_vertices:
            vertices.append(np.r_[x,y,[x[e]*y[j] for e,j in obs]])
    V=np.array(vertices).T
    for weights in families:
        yf=np.array(weights,float)
        center=np.r_[inst.reference,yf,[inst.reference[e]*yf[j] for e,j in obs]]
        for trial in range(5):
            objective=rng.normal(size=N)
            # Dense x/y/z rows, generally coupling all state subproblems.
            C=rng.normal(size=(3,N)); rhs=C@center+rng.uniform(.01,.3,size=3)
            rows=list(zip(C,rhs)) if trial else []
            ref=linprog(objective@V, A_eq=np.vstack([np.ones(V.shape[1]),V[E:E+m]]),
                        b_eq=np.r_[1,yf], A_ub=C@V if rows else None,
                        b_ub=rhs if rows else None, bounds=(0,None),method='highs')
            assert ref.success, ref.message
            for merge in [False,True]:
                ans=optimize_ef(inst,objective,weights,merge=merge,extra_rows=rows)
                assert ans.success, ans.message
                assert abs(ans.fun-ref.fun)<1e-7,(m,weights,merge,ans.fun,ref.fun)
                p=ans.original_point
                assert np.max(np.abs(p[E:E+m]-yf),initial=0)<1e-12
                assert abs(objective@p-ans.fun)<1e-8
                if rows: assert np.max(C@p-rhs)<1e-8
                labels=sorted({j for _,j in obs}) if merge else list(range(m))
                state_weights=[(j,weights[j]) for j in labels]
                state_weights.append((m,1-sum(weights[j] for j in labels)))
                state_weights=[(j,w) for j,w in state_weights if w>0]
                fs=ans.x.reshape(len(state_weights),E)
                assert ans.model_stats['variables']==len(state_weights)*E
                assert np.max(np.abs(fs.sum(axis=0)-p[:E]))<1e-10
                slots={j:i for i,(j,_) in enumerate(state_weights)}
                for i,(j,w) in enumerate(state_weights):
                    assert abs(fs[i,0]+fs[i,1]-2*float(w))<1e-8
                    assert fs[i].min()>-1e-8
                    assert np.max(fs[i]-float(w)*np.array([2,2,3]))<1e-8
                for k,(e,j) in enumerate(obs):
                    assert abs(p[E+m+k]-(fs[slots[j],e] if j in slots else 0))<1e-10
                counts['fixed_vertex_comparisons']+=1
                counts['reconstructed_points']+=1
        # Impossible fixed-y row must remain impossible after affine substitution.
        if m:
            row=np.zeros(N);row[E]=1
            for merge in [False,True]:
                ans=optimize_ef(inst,np.ones(N),weights,merge=merge,
                                extra_rows=[(row,float(weights[0])-.25)])
                assert ans.status==2
                counts['infeasible_rows']+=1
        # A zero-weight observed product cannot satisfy a negative upper bound.
        for k,(e,j) in enumerate(obs):
            if weights[j]==0:
                row=np.zeros(N);row[E+m+k]=1
                for merge in [False,True]:
                    assert optimize_ef(inst,np.ones(N),weights,merge=merge,
                                       extra_rows=[(row,-.25)]).status==2
                    counts['infeasible_rows']+=1
                break
    # Preserve the free-weight branch, with dense original-coordinate coupling.
    for trial in range(4):
        objective=rng.normal(size=N); C=rng.normal(size=(2,N));rhs=C@V.mean(axis=1)+.1
        ref=linprog(objective@V,A_eq=np.ones((1,V.shape[1])),b_eq=[1],
                    A_ub=C@V,b_ub=rhs,bounds=(0,None),method='highs')
        for merge in [False,True]:
            ans=optimize_ef(inst,objective,merge=merge,extra_rows=list(zip(C,rhs)))
            assert ans.success and ref.success
            assert abs(ans.fun-ref.fun)<1e-7
            counts['free_vertex_comparisons']+=1
print(json.dumps(counts,indent=2))
(Path(__file__).parent/'check-result.json').write_text(json.dumps(counts,indent=2)+'\n')
