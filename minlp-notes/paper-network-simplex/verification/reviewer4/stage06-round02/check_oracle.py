"""Fresh graph/path checks of the changed production flat oracle."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from unittest.mock import patch
import json,random
import numpy as np
from scipy.optimize import linprog
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import membership_ef

rng=random.Random(64064)
stats={'queries':0,'exact_decompositions':0,'exact_global_cuts':0,'vertex_checks':0,'LP_comparisons':0}
stats['strong_membership_comparisons']=0

def paths(L):
    return [tuple(int(e%2==bits[e//2]) for e in range(2*L))+(0,) for bits in product((0,1),repeat=L)]+[(0,)*(2*L)+(1,)]

def validate(model,p,lp=True):
    ans=model.separate(p)
    assert model.separate(p,decompose=False).feasible==ans.feasible
    stats['queries']+=1
    L,m=model.gadgets,model.simplex_size
    pp=paths(L)
    lam=p.y+(1-sum(p.y),)
    if ans.feasible:
        dec=ans.decomposition
        assert dec.weights==lam
        flows={j:dec.flow(j) for j,w in enumerate(lam) if w}
        for j,x in flows.items():
            assert all(0<=v<=1 for v in x)
            assert all(x[2*i]+x[2*i+1]+x[-1]==1 for i in range(L))
        assert tuple(sum(lam[j]*x[e] for j,x in flows.items()) for e in range(2*L+1))==p.x
        assert all(z==(lam[j]*flows[j][e] if lam[j] else 0) for (e,j),z in p.z.items())
        assert sum(dec.profile)==1-p.x[-1]
        assert all(0<=v<=w for v,w in zip(dec.profile,lam))
        aa=dec.arc_a
        assert all(sum(row)==p.x[2*i] for i,row in enumerate(aa))
        assert len(dec.group_profile)==len(model.labels)+1
        stats['exact_decompositions']+=1
    else:
        cut=ans.cut
        assert cut.evaluate(p)>0
        for j in range(m+1):
            for x in pp:
                value=cut.constant
                for key,c in cut.coefficients.items():
                    if key[0]=='x': value+=c*x[key[1]]
                    elif key[0]=='y': value+=c*int(key[1]==j)
                    else: value+=c*x[key[1]]*int(key[2]==j)
                assert value<=0
                stats['vertex_checks']+=1
        if len(model.labels)<=3:
            assert all(abs(c)<=1 for k,c in cut.coefficients.items() if k[0] in ('x','z'))
        stats['exact_global_cuts']+=1
    if lp:
        eq=[];rhs=[]
        for j,w in enumerate(lam):
            eq.append([int(j==s) for s in range(m+1) for x in pp]);rhs.append(w)
        for e,v in enumerate(p.x):
            eq.append([x[e] for s in range(m+1) for x in pp]);rhs.append(v)
        for (e,j),v in p.z.items():
            eq.append([x[e]*int(j==s) for s in range(m+1) for x in pp]);rhs.append(v)
        res=linprog(np.zeros((m+1)*len(pp)),A_eq=np.array(eq,float),b_eq=np.array(rhs,float),bounds=(0,None),method='highs')
        assert res.status in (0,2) and ans.feasible==(res.status==0)
        stats['LP_comparisons']+=1
        b=np.zeros(L+1);b[0]=1;b[-1]=-1
        instance=Instance(model.arcs,b,m,model.observations,np.asarray(p.x,float))
        for merge in (False,True):
            for two_state in (False,True):
                baseline=membership_ef(instance,p.x,p.y,[p.z[o] for o in model.observations],merge=merge,two_state=two_state)
                assert baseline.status==res.status
                stats['strong_membership_comparisons']+=1
    return ans

for m,L in [(0,1),(1,2),(2,3),(3,1),(3,3),(4,2),(23,2)]:
    for trial in range(8):
        labels=rng.sample(range(m),rng.randrange(min(m,4)+1))
        obs={(rng.randrange(2*L+1),j) for j in labels}
        obs.update((e,j) for j in labels for e in range(2*L+1) if rng.random()<.35)
        model=FlatChainSimplex(L,m,obs)
        raw=[rng.randrange(4) for _ in range(m+1)]
        if not sum(raw):raw[-1]=1
        lam=[F(w,sum(raw)) for w in raw]
        pp=paths(L);fs=[]
        for w in lam:
            x1,x2=rng.choices(pp,k=2)
            fs.append(tuple(w*F(a+b,2) for a,b in zip(x1,x2)))
        x=tuple(sum(f[e] for f in fs) for e in range(2*L+1))
        z={(e,j):fs[j][e] for e,j in obs}
        p=Point(x,lam[:-1],z)
        validate(model,p)
        if z:
            zz=dict(z);zz[rng.choice(list(z))]+=F(rng.choice((-2,-1,1,2)),19)
            validate(model,Point(x,lam[:-1],zz))
        xx=list(x);xx[0]+=F(1,11)
        validate(model,Point(xx,lam[:-1],z))

# Both exceptional three-label repairs, audited over every path/state vertex.
validate(FlatChainSimplex(3,3,[(2*i,i) for i in range(3)]),Point([F(2,5),F(1,10)]*3+[F(1,2)],[F(1,3)]*3,{(2*i,i):0 for i in range(3)}))
z={(2*i+1,j):F(1,20) for i,pair in enumerate(((0,1),(0,2),(1,2))) for j in pair}
validate(FlatChainSimplex(3,3,z),Point([F(1,20),F(9,20)]*3+[F(1,2)],[F(1,4)]*3,z))

# Sparse three-label residual-profile regression with two positive default constituents.
y=[F(0)]*23
for j in (2,7,22):y[j]=F(1,6)
y[0]=F(1,4)
model=FlatChainSimplex(3,23,[(6,j) for j in (2,7,22)])
ans=validate(model,Point([F(1,8)]*6+[F(3,4)],y,{(6,j):y[j] for j in (2,7,22)}))
assert ans.decomposition.group_profile==(0,0,0,F(1,4))
assert ans.decomposition.flow(0)==ans.decomposition.flow(23)

# The four-label obstruction survives sparse renumbering among 23 original labels.
labels=(1,7,11,22); allowed=({0,1,2},{0,3},{1,3},{2,3})
obs=[(2*i,labels[j]) for i,S in enumerate(allowed) for j in range(4) if j not in S]
xx=[]
for S in allowed:
    aa=len(S)*F(1,8)+(4-len(S))*F(1,32);xx.extend((aa,F(1,2)-aa))
xx.append(F(1,2));yy=[F(0)]*23
for j in labels: yy[j]=F(1,4)
zz={o:F(1,32) for o in obs};model=FlatChainSimplex(4,23,obs)
validate(model,Point(xx,yy,zz))
zz[0,22]-=F(1,100000)
ans=validate(model,Point(xx,yy,zz))
assert abs(ans.cut.coefficients['z',0,22]/ans.cut.coefficients['z',2,7])==2

# Many globally unused labels must never request a parameter library.
with patch('network_simplex.flat_chain.reduced_library',side_effect=AssertionError('unexpected circuit library')),patch('network_simplex.flat_chain._reduced_bases',side_effect=AssertionError('unexpected basis library')):
    m=2000;model=FlatChainSimplex(2,m,[(0,17),(2,1999)])
    p=Point([F(1,4)]*4+[F(1,2)],[F(1,2*m)]*m,{(0,17):F(1,8*m),(2,1999):F(1,8*m)})
    validate(model,p,lp=False)
stats['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
