from fractions import Fraction as F
from itertools import combinations,product
from math import lcm,gcd
import json, random, sys
from pathlib import Path
import sympy as sp
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'code'))
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex,reduced_library
rng=random.Random(8040401)
out={}
# Independent SymPy exact nullspaces, without implementation elimination routines.
for m in (1,2,3):
    N=sorted(set(product((0,1),repeat=m))-{(0,)*m}|{tuple(-int(i==j) for i in range(m)) for j in range(m)}|{(-1,)*m})
    circuits=[]
    for k in range(2,m+2):
        for ids in combinations(range(len(N)),k):
            null=sp.Matrix([N[i] for i in ids]).T.nullspace()
            if len(null)!=1 or not (all(x>0 for x in null[0]) or all(x<0 for x in null[0])):continue
            w=[abs(x) for x in null[0]]; den=lcm(*[int(x.q) for x in w]); w=[int(x*den) for x in w]; g=gcd(*w)
            circuits.append((ids,tuple(x//g for x in w)))
    n,c=reduced_library(m)
    assert tuple(N)==n and set(circuits)==set(c)
    out[f'circuits_m{m}']={'normals':len(N),'circuits':len(c),'max_weight':max(max(w) for _,w in c)}
# Exhaustive coefficient occurrences for each product type and all 64 gadget patterns.
# Add zero as a possible branch from other gadgets. One chosen row per normal.
N,c=reduced_library(3); ni={n:i for i,n in enumerate(N)}
checks=0
for cats in product('ABTU',repeat=3):
    for j in range(3):
        for arc in ('a','b'):
            if (arc=='a' and cats[j] not in 'AT') or (arc=='b' and cats[j] not in 'BT'):continue
            opts={n:{0} for n in N}
            plus=tuple(int(i==j) for i in range(3)); minus=tuple(-x for x in plus)
            opts[minus].add(-1)
            if cats[j]=='T':opts[plus].add(1)
            r=(-1 if arc=='a' else 1 if cats[j]=='B' else 0)
            for normal,coeff in [(tuple(int(t=='B') for t in cats),r),(tuple(int(t in 'AT') for t in cats),-r)]:
                if normal in opts:opts[normal].add(coeff)
            for ids,w in c:
                lo=sum(mu*min(opts[N[i]]) for i,mu in zip(ids,w));hi=sum(mu*max(opts[N[i]]) for i,mu in zip(ids,w))
                assert -1<=lo<=hi<=1,(cats,j,arc,ids,lo,hi)
                checks+=1
out['exhaustive_product_occurrence_circuit_checks']=checks
# Full path-simplex vertex hull assembled independently; exact oracle output audited against every vertex.
counts={'queries':0,'feasible':0,'cuts':0,'vertex_cut_evaluations':0,'decompositions':0}
for trial in range(360):
    L=rng.randrange(1,5);m=rng.randrange(1,5)
    if trial%30==0:m=40
    labels=rng.sample(range(m),min(m,rng.randrange(1,4)))
    obs=[(e,j) for e in range(2*L+1) for j in labels if rng.random()<.52]
    model=FlatChainSimplex(L,m,obs)
    raw=[rng.randrange(0,5) for _ in range(m+1)]
    if sum(raw)==0:raw[-1]=1
    weights=[F(x,sum(raw)) for x in raw]; y=tuple(weights[:-1])
    paths=[]
    for choices in product((0,1),repeat=L):
        p=[0]*(2*L+1)
        for i,j in enumerate(choices):p[2*i+j]=1
        paths.append(tuple(p))
    paths.append((0,)*(2*L)+(1,))
    f=[]
    for j in range(m+1):
        r=[rng.randrange(1,4) for p in paths];den=sum(r)
        f.append(tuple(weights[j]*sum(F(q*p[e],den) for q,p in zip(r,paths)) for e in range(2*L+1)))
    x=tuple(sum(fj[e] for fj in f) for e in range(2*L+1));z={(e,j):f[j][e] for e,j in obs}
    if trial%3:
        for e,j in obs:
            low=max(F(0),x[e]+y[j]-1);high=min(x[e],y[j]);z[e,j]=low+(high-low)*F(rng.randrange(0,11),10)
    point=Point(x,y,z);ans=model.separate(point)
    # Drop zero states only in independent vertex LP; preserves all original observations.
    verts=[]
    for j in range(m+1):
        if not weights[j]:continue
        yy=tuple(F(int(j==h)) for h in range(m))
        for path in paths:verts.append(Point(path,yy,{(e,h):F(path[e]*int(j==h)) for e,h in obs}))
    arr=np.array([[1,*p.x,*p.y,*[p.z[o] for o in model.observations]] for p in verts],dtype=float).T
    rhs=np.array([1,*x,*y,*[z[o] for o in model.observations]],float)
    lp=linprog(np.zeros(len(verts)),A_eq=arr,b_eq=rhs,bounds=(0,None),method='highs')
    assert lp.status in (0,2)
    assert (lp.status==0)==(ans.cut is None),(trial,lp.message,ans)
    counts['queries']+=1
    if ans.cut:
        counts['cuts']+=1
        assert ans.cut.evaluate(point)>0
        # All states, including zero-weight states at query, required for GLOBAL cut validity.
        for j in range(m+1):
            yy=tuple(F(int(j==h)) for h in range(m))
            for path in paths:
                v=Point(path,yy,{(e,h):F(path[e]*int(j==h)) for e,h in obs})
                assert ans.cut.evaluate(v)<=0
                counts['vertex_cut_evaluations']+=1
        if len(model.labels)<=3:assert all(abs(v)<=1 for k,v in ans.cut.coefficients.items() if k[0] in ('x','z'))
    else:
        counts['feasible']+=1;dec=ans.decomposition
        flows={j:dec.flow(j) for j in dec.positive_states()}
        for j,fl in flows.items():
            assert all(0<=v<=1 for v in fl)
            assert all(fl[2*i]+fl[2*i+1]+fl[-1]==1 for i in range(L))
        assert all(sum(weights[j]*fl[e] for j,fl in flows.items())==x[e] for e in range(2*L+1))
        assert all(weights[j]*flows[j][e]==v if weights[j] else v==0 for (e,j),v in z.items())
        counts['decompositions']+=1
out['independent_path_hull_audit']=counts
# Exact K4 section witnesses over grid, independently form incidence and all states.
C=sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
v=sp.Matrix([F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2)])
bar=sp.Matrix([F(1,6),F(1,24),F(1,8)])
n=0
for p,q in product([F(i,1000) for i in range(-10,11)],repeat=2):
    if 2*p+q<0:continue
    states=[sp.Matrix([p,q,p]),sp.Matrix([q/2,-q/2,0]),sp.Matrix([F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p])]
    assert sum(states,sp.zeros(3,1))==bar
    assert all(0<=val<=F(1,3) for st in states for val in v/3+C*st)
    n+=1
out['k4_exact_witness_grid']=n
# Check all 88 current manifest hashes without trusting prior PASS.
import hashlib
manifest=json.load(open(ROOT/'paper-network-simplex/verification/stage07-validation.json'))
mismatch=[p for p,h in manifest['sha256'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
out['source_hash_audit']={'count':len(manifest['sha256']),'mismatches':mismatch}
assert not mismatch
print(json.dumps(out,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
