"""Independent symbolic branch audit and path-mixture LP comparison."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import json, random
import numpy as np
import sympy as sp
from scipy.optimize import linprog

rng=random.Random(5504)
stats={"circuits":{},"symbolic_branches":0,"bypass_repairs":0,"path_LP_queries":0,"exact_recoveries":0}

def add(*terms):
    out=defaultdict(int)
    for weight,a in terms:
        for k,v in a.items(): out[k]+=weight*v
    return {k:v for k,v in out.items() if v}

def val(a,p): return sum(v*p.get(k,0) for k,v in a.items())
def unit(m,j): return tuple(int(i==j) for i in range(m))
def minus(a): return tuple(-x for x in a)

def library(m):
    ns=sorted(set(product((0,1),repeat=m))-{(0,)*m}|{minus(unit(m,j)) for j in range(m)}|{(-1,)*m})
    circuits=[]
    for n in range(2,m+2):
        for ids in combinations(range(len(ns)),n):
            ker=sp.Matrix([ns[i] for i in ids]).T.nullspace()
            if len(ker)!=1 or any(x==0 for x in ker[0]): continue
            v=ker[0]
            if all(x<0 for x in v): v=-v
            if not all(x>0 for x in v): continue
            den=lcm(*(int(x.q) for x in v)); ints=[int(x*den) for x in v]
            g=reduce(gcd,ints)
            circuits.append([(ns[i],x//g) for i,x in zip(ids,ints)])
    bs=[]
    for ids in combinations(range(len(ns)),m):
        b=sp.Matrix([ns[i] for i in ids])
        if b.det(): bs.append(([ns[i] for i in ids],[[F(x) for x in row] for row in b.inv().tolist()]))
    stats["circuits"][str(m)]=len(circuits)
    return ns,circuits,bs

for dim,expected in [(1,1),(2,5),(3,16)]:
    lib=library(dim)
    assert len(lib[1])==expected
    if dim==3: ns,circuits,bases=lib
m,L=3,3
for case in range(60):
    cats=[[rng.randrange(4) for _ in range(m)] for i in range(L)] # 0 none,1 a,2 b,3 both
    bypass=[j for j in range(m) if rng.randrange(2)]
    if case==0: cats=[[1,0,0],[0,1,0],[0,0,1]]; bypass=[]
    if case==1: cats=[[2,2,0],[2,0,2],[0,2,2]]; bypass=[]
    rows=defaultdict(list); observations=[]
    def put(n,a,meta=None): rows[n].append((a,meta))
    for j in range(m):
        put(unit(m,j),{f'y{j}':1}); put(minus(unit(m,j)),{})
    full=(1,)*m; t={'c':1,'xh':-1}
    put(full,t); put(minus(full),{'xh':1,**{f'y{j}':-1 for j in range(m)}})
    for j in bypass:
        z=f'zh{j}'; observations.append((2*L,j,z))
        put(unit(m,j),{f'y{j}':1,z:-1}); put(minus(unit(m,j)),{f'y{j}':-1,z:1})
    for i,cs in enumerate(cats):
        R={f'xa{i}':1}
        for j,c in enumerate(cs):
            za,zb=f'za{i}_{j}',f'zb{i}_{j}'
            if c&1: observations.append((2*i,j,za)); R[za]=-1
            if c&2: observations.append((2*i+1,j,zb))
            if c==2: R[zb]=1
            if c==1: put(minus(unit(m,j)),{za:-1})
            if c==2: put(minus(unit(m,j)),{zb:-1})
            if c==3:
                put(unit(m,j),{za:1,zb:1}); put(minus(unit(m,j)),{za:-1,zb:-1})
        put(tuple(int(c==2) for c in cs),R,('lower',i))
        put(tuple(int(c in (1,3)) for c in cs),add((1,t),(-1,R)),('upper',i))
    for cir in circuits:
        if any(n not in rows for n,_ in cir): continue
        for picks in product(*(rows[n] for n,_ in cir)):
            a=add(*[(w,pick[0]) for (_,w),pick in zip(cir,picks)])
            assert all(abs(v)<=1 for k,v in a.items() if k.startswith('z') or (k.startswith('x') and k!='xh'))
            if abs(a.get('xh',0))==2:
                sign=1 if a['xh']==-2 else -1
                kind='upper' if sign==1 else 'lower'
                chosen=next(meta[1] for _,meta in picks if meta and meta[0]==kind)
                a=add((1,a),(sign,{f'xa{chosen}':1,f'xb{chosen}':1,'xh':1,'c':-1}))
                stats['bypass_repairs']+=1
            assert all(abs(v)<=1 for k,v in a.items() if k.startswith(('x','z')))
            stats['symbolic_branches']+=1
    paths=[]
    for bits in product((0,1),repeat=L):
        paths.append([int(e//2<L and e%2==bits[e//2]) if e<2*L else 0 for e in range(2*L+1)])
    paths.append([0]*(2*L)+[1])
    raw=[rng.randrange(4) for _ in range(m+1)]
    if not sum(raw): raw[0]=1
    weights=[F(x,sum(raw)) for x in raw]
    fs=[]
    for weight in weights:
        mix=[rng.randrange(4) for _ in paths]
        if not sum(mix): mix[0]=1
        fs.append([weight*sum(F(a,sum(mix))*path[e] for a,path in zip(mix,paths)) for e in range(2*L+1)])
    aggregate=[sum(f[e] for f in fs) for e in range(2*L+1)]
    point={'c':F(1),'xh':aggregate[-1],**{f'y{j}':weights[j] for j in range(m)}}
    for i in range(L): point[f'xa{i}'],point[f'xb{i}']=aggregate[2*i:2*i+2]
    for e,j,z in observations: point[z]=fs[j][e]
    for trial in range(5):
        p=dict(point)
        if trial and observations:
            _,_,z=rng.choice(observations); p[z]+=F(rng.choice((-2,-1,1,2)),17)
        gamma={n:min(val(a,p) for a,_ in choices) for n,choices in rows.items()}
        ok=all(p[z]>=0 for _,_,z in observations) and gamma.get((0,)*m,0)>=0
        ok=ok and all(sum(w*gamma[n] for n,w in cir)>=0 for cir in circuits if all(n in gamma for n,_ in cir))
        # Independent LP on nonnegative mixtures of complete path/state vertices.
        lp_rows=[]; rhs=[]
        for j in range(m+1):
            lp_rows.append([int(j==k) for k in range(m+1) for path in paths]); rhs.append(weights[j])
        for e,x in enumerate(aggregate):
            lp_rows.append([path[e] for k in range(m+1) for path in paths]); rhs.append(x)
        for e,j,z in observations:
            lp_rows.append([path[e]*int(k==j) for k in range(m+1) for path in paths]); rhs.append(p[z])
        res=linprog(np.zeros(len(paths)*(m+1)),A_eq=np.array(lp_rows,dtype=float),b_eq=np.array(rhs,dtype=float),bounds=(0,None),method='highs')
        assert res.status in (0,2) and ok==(res.status==0)
        stats['path_LP_queries']+=1
        if not ok: continue
        for norms,inv in bases:
            if not all(n in gamma for n in norms): continue
            w=[sum(a*gamma[n] for a,n in zip(row,norms)) for row in inv]
            if all(sum(a*b for a,b in zip(n,w))<=g for n,g in gamma.items()): break
        else: raise AssertionError('No recovery basis')
        w.append(1-p['xh']-sum(w))
        assert all(0<=a<=b for a,b in zip(w,weights))
        recovered=[[F(0)]*(2*L+1) for _ in weights]
        for i,cs in enumerate(cats):
            aa=[None]*(m+1)
            for j,c in enumerate(cs):
                if c&1: aa[j]=p[f'za{i}_{j}']
                elif c==2: aa[j]=w[j]-p[f'zb{i}_{j}']
            rem=p[f'xa{i}']-sum(v for v in aa if v is not None)
            for j in range(m+1):
                if aa[j] is None: aa[j]=min(rem,w[j]); rem-=aa[j]
                assert 0<=aa[j]<=w[j]
                recovered[j][2*i]=aa[j]; recovered[j][2*i+1]=w[j]-aa[j]
            assert rem==0
        for j in range(m+1): recovered[j][-1]=weights[j]-w[j]
        assert all(sum(f[e] for f in recovered)==aggregate[e] for e in range(2*L+1))
        assert all(recovered[j][e]==p[z] for e,j,z in observations)
        stats['exact_recoveries']+=1
stats['status']='PASS'
assert stats['bypass_repairs']>=2
Path(__file__).with_suffix('.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
