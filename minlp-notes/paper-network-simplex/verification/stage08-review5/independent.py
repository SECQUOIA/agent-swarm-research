"""Independent Stage8 reviewer5 checks; writes only in reviewer evidence folder."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib, json
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef
from network_simplex_compressed import CompressedNetworkSimplex

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
out = {}
manifest = json.loads((ROOT/'paper-network-simplex/verification/stage07-validation.json').read_text())
out['manifest_hashes'] = len(manifest['sha256'])
out['hash_mismatches'] = [p for p,h in manifest['sha256'].items()
    if hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != h]
assert not out['hash_mismatches']

# Derive positive circuits directly from all small dependent row subsets.
counts=[]
for m in (1,2,3):
    rows = sorted(set(tuple(int(j in S) for j in range(m))
                       for n in range(1,m+1) for S in combinations(range(m),n)) |
                  set(tuple(-int(j==i) for j in range(m)) for i in range(m)) |
                  {(-1,)*m})
    count=0; maxweight=0
    for n in range(2,m+2):
        for ids in combinations(range(len(rows)),n):
            null=sp.Matrix([rows[i] for i in ids]).T.nullspace()
            if len(null)!=1 or any(x==0 for x in null[0]): continue
            v=null[0]
            if not (all(x>0 for x in v) or all(x<0 for x in v)): continue
            den=sp.ilcm(*[x.q for x in v]); w=[abs(int(x*den)) for x in v]
            g=sp.igcd(*w); w=[x//g for x in w]
            count+=1; maxweight=max(maxweight,*w)
    counts.append((m,len(rows),count,maxweight))
assert counts==[(1,2,1,1),(2,6,5,1),(3,11,16,2)]
out['independent_reduced_circuits']=counts

# Verify every given K4 state bound in a dense rational local grid.
C=sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
v=sp.Matrix([sp.Rational(1,2)]*3+[sp.Rational(1,4),sp.Rational(1,2),sp.Rational(1,2)])
total=sp.Matrix([sp.Rational(1,6),sp.Rational(1,24),sp.Rational(1,8)])
checked=0
for a,b in product(range(-15,16),repeat=2):
    p,q=sp.Rational(a,1536),sp.Rational(b,1536)
    if 2*p+q<0: continue
    states=[sp.Matrix([p,q,p]),sp.Matrix([q/2,-q/2,0]),
            sp.Matrix([sp.Rational(1,6)-p-q/2,sp.Rational(1,24)-q/2,sp.Rational(1,8)-p])]
    assert sum(states,sp.zeros(3,1))==total
    for s in states:
        for val,ref in zip(C*s,v): assert -ref/3<=val<=(1-ref)/3
    checked+=1
out['K4_exact_local_witnesses']=checked

fib=[]
for q in range(3,15):
    N=2*q-1
    columns=[(q,0),(q,1)]
    for i in range(3,q+1): columns += [(q+i-2,i-1),(q+i-2,i-2,i-3)]
    columns += [(q-1,q-2)]
    D=sp.zeros(N)
    for j,rows in enumerate(columns):
        for i in rows:D[i,j]=1
    ff=[0,1,1]
    for i in range(3,q+2):ff.append(ff[-1]+ff[-2])
    alpha=sp.Matrix(ff[1:q+1]+[ff[q+1]-1]+[ff[q+1]-ff[i] for i in range(3,q+1)])
    K=sp.ones(N)-D
    assert D.det()!=0 and K.det()!=0
    assert sum(D)==5*q-4
    assert D.T*alpha==sp.ones(N,1)*ff[q+1]
    assert K.T*alpha==sp.ones(N,1)*(sum(alpha)-ff[q+1])
    assert all(0<sum(K[i,:])<N for i in range(N))
    fib.append({'q':q,'ratio':ff[q],'observations':int(sum(D))})
out['Fibonacci_exact_cases']=fib

# Independent original-hull vertex LP, with two circulation blocks and a loop.
# Compare free/fixed simplex slices plus dense coupling rows and nonzero y costs.
m,E=7,5
obs=[(0,0),(1,2),(2,3),(3,0),(4,5)]
arcs=[(0,1,1),(0,1,1),(1,2,1),(1,2,1),(1,1,1)]
flows=[np.array([a,1-a,b,1-b,c],float) for a,b,c in product((0,1),repeat=3)]
vertices=[]
for state in range(m+1):
    y=np.eye(m+1)[state,:m]
    for f in flows:vertices.append(np.r_[f,y,[f[e]*y[j] for e,j in obs]])
vertices=np.asarray(vertices).T
instance=Instance(arcs,np.array([1.,0.,-1.]),m,obs,np.full(E,.5))
comparisons=0; maxerr=0.
for seed in range(16):
    rng=np.random.default_rng(8400+seed)
    weights=([F(1,8),0,F(1,8),F(1,4),0,F(1,4),0] if seed%2 else [F(1,2),0,0,0,0,F(1,2),0])
    for fixed in (None,weights):
        y=np.asarray(weights,float)
        witness=np.r_[np.full(E,.5),y,[.5*y[j] for e,j in obs]]
        objective=rng.normal(size=len(witness)); rows=rng.normal(size=(3,len(witness)))
        rhs=rows@witness+np.array([0.,.02,.15])
        eq=np.ones((1,vertices.shape[1])); beq=np.ones(1)
        if fixed is not None:eq=np.vstack([eq,vertices[E:E+m]]);beq=np.r_[beq,y]
        oracle=linprog(objective@vertices,A_eq=eq,b_eq=beq,A_ub=rows@vertices,b_ub=rhs,bounds=(0,None),method='highs')
        assert oracle.success
        for merge in (False,True):
            result=optimize_ef(instance,objective,fixed,merge=merge,extra_rows=list(zip(rows,rhs)))
            assert result.success and abs(result.fun-oracle.fun)<1e-7
            maxerr=max(maxerr,abs(result.fun-oracle.fun));comparisons+=1
        for eliminate in (False,True):
            model=CompressedNetworkSimplex(arcs,-instance.balances,m,obs,eliminate_observed=eliminate)
            for row,r in zip(rows,rhs):model.ub.append(({i:F(str(a)) for i,a in enumerate(row) if a},F(str(r))))
            result=model.optimize(objective,y_fixed=fixed)
            assert result.success and abs(result.fun-oracle.fun)<1e-7
            maxerr=max(maxerr,abs(result.fun-oracle.fun));comparisons+=1
out['independent_vertex_LP_comparisons']={'count':comparisons,'maximum_absolute_objective_difference':maxerr,'arithmetic':'numerical HiGHS; not exact certificates'}
out['status']='PASS'
(HERE/'independent.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
