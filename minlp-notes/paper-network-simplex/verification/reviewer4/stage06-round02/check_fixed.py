"""Independent exact primal/dual audit of fixed-y numerical baseline outputs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef

# The flow domain is affinely a box in (t,ell,s), so these eight vertices
# are complete. It includes a reverse arc, bridge, loops, a zero capacity,
# a separate cyclic component, and an isolated vertex.
arcs=[(0,1,3),(1,0,2),(0,0,2),(1,2,2),(3,4,3),(4,3,3),(4,4,0)]
b=[1,1,-2,0,0,0]; E=len(arcs)
flows=[(t,t-1,ell,2,s,s,0) for t,ell,s in product((1,3),(0,2),(0,3))]
ref=[sum(F(v[e]) for v in flows)/8 for e in range(E)]
def rational(v): return F(float(v)).limit_denominator(10**7)
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
counts=dict(vertex_dual_certificates=0,exact_baseline_optima=0,zero_observations=0,infeasible_comparisons=0)
for m in (0,1,7):
    labels=[] if m==0 else ([0] if m==1 else [1,4,6])
    obs=[(e,j) for j in labels for e in (0,1,2,4,6)]
    inst=Instance(arcs,np.asarray(b,float),m,obs,np.asarray(ref,float))
    vertices=[]
    for state in range(m+1):
        yy=tuple(F(state==j) for j in range(m))
        for f in flows: vertices.append(tuple(map(F,f))+yy+tuple(F(f[e])*yy[j] for e,j in obs))
    dim=E+m+len(obs)
    V=np.asarray(vertices,float).T
    patterns=[(F(0),)*m]
    if m: patterns += [(F(1),)+(F(0),)*(m-1),tuple(F(1,m+1) for _ in range(m))]
    if m==7:
        patterns += [tuple(map(F,(0,0,0,1,0,0,0))),
                     (F(1,7),0,F(2,7),0,F(1,7),0,0),
                     (0,F(1,3),0,0,F(2,3),0,0),
                     (0,F(1,3),0,0,F(1,3),0,F(1,3))]
    for pattern in patterns:
        y=tuple(map(F,pattern))
        witness=tuple(ref)+y+tuple(ref[e]*y[j] for e,j in obs)
        eq=[tuple(F(1) for _ in vertices)]+[tuple(v[E+j] for v in vertices) for j in range(m)]
        beq=(F(1),)+y
        for seed in range(6):
            rng=np.random.default_rng(802000+100*m+seed)
            cost=tuple(map(F,map(int,rng.integers(-5,6,size=dim))))
            rows=[tuple(map(F,map(int,rng.integers(-3,4,size=dim)))) for _ in range(3)]
            rhs=tuple(dot(row,witness)+F(i,10) for i,row in enumerate(rows))
            vm=[tuple(dot(row,v) for v in vertices) for row in rows]
            vc=tuple(dot(cost,v) for v in vertices)
            vr=linprog(np.array(vc,float),A_eq=np.array(eq,float),b_eq=np.array(beq,float),A_ub=np.array(vm,float),b_ub=np.array(rhs,float),bounds=(0,None),method='highs')
            assert vr.status==0
            dualeq=tuple(map(rational,vr.eqlin.marginals)); dualub=tuple(map(rational,vr.ineqlin.marginals))
            assert all(d<=0 for d in dualub)
            assert all(sum(dualeq[i]*eq[i][k] for i in range(len(eq)))+sum(dualub[i]*vm[i][k] for i in range(3))<=vc[k] for k in range(len(vertices)))
            lower=dot(dualeq,beq)+dot(dualub,rhs)
            counts['vertex_dual_certificates']+=1
            for merge in (False,True):
                res=optimize_ef(inst,np.array(cost,float),y_fixed=y,merge=merge,extra_rows=[(np.array(a,float),float(r)) for a,r in zip(rows,rhs)])
                assert res.status==0
                labs=labels if merge else list(range(m))
                states=[(j,w) for j,w in zip(labs+[m],[y[j] for j in labs]+[1-sum(y[j] for j in labs)]) if w>0]
                assert res.model_stats['variables']==E*len(states)
                assert res.model_stats['rows']==len(b)*len(states)+3
                fs=[tuple(map(rational,f)) for f in res.x.reshape(len(states),E)]
                for (j,w),f in zip(states,fs):
                    assert all(0<=v<=w*u for v,(_,_,u) in zip(f,arcs))
                    balance=[F(0)]*len(b)
                    for value,(tail,head,_) in zip(f,arcs): balance[tail]+=value;balance[head]-=value
                    assert balance==[w*z for z in b]
                grouped=dict(zip((j for j,w in states),fs))
                p=tuple(sum(f[e] for f in fs) for e in range(E))+y+tuple(grouped[j][e] if j in grouped else F(0) for e,j in obs)
                assert tuple(map(rational,res.original_point))==p
                assert all(dot(a,p)<=r for a,r in zip(rows,rhs))
                assert dot(cost,p)==lower
                assert abs(float(lower)-res.fun)<1e-8
                for (e,j),z in zip(obs,p[E+m:]):
                    if y[j]==0: assert z==0;counts['zero_observations']+=1
                counts['exact_baseline_optima']+=1
        # A contradictory row on a fixed coordinate, including unobserved y.
        row=[F(0)]*dim
        pos=E+(0 if m==1 else 3) if m else 3
        row[pos]=1
        rr=witness[pos]-F(1,4)
        for merge in (False,True):
            res=optimize_ef(inst,np.zeros(dim),y_fixed=y,merge=merge,extra_rows=[(row,rr)])
            assert res.status==2 and not hasattr(res,'original_point')
            counts['infeasible_comparisons']+=1
counts['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts))
