#!/usr/bin/env python3
"""Exact small-rank libraries; compare finite support tests with raw state LP.

No graph preprocessing is tested here. Matrices are fixed fundamental-cycle
matrices for an interval, theta, K4, and a four-rim-edge wheel. Integer library
computations are checked exactly; candidate evaluations use Fraction. SciPy's
independent feasibility comparison is numerical and does not replace the proof.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import gcd, floor
from functools import reduce
import argparse
import json
import random
import time
import numpy as np
from scipy.optimize import linprog


def det(a):
    n = len(a)
    if not n:
        return 1
    return sum((-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i+1,n))
               * np.prod([int(a[i][p[i]]) for i in range(n)], dtype=object)
               for p in permutations(range(n)))


def cross(rows, rank):
    return tuple((-1)**k * int(det([[row[j] for j in range(rank) if j != k]
                                   for row in rows])) for k in range(rank))


def primitive(v):
    g = reduce(gcd, (abs(x) for x in v), 0)
    if not g:
        return None
    v = tuple(x // g for x in v)
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def library(c):
    rank = len(c[0])
    normals = sorted(set(tuple(sign*x for x in row) for row in c for sign in [-1,1]))
    p = len(normals)
    dirs = {primitive(cross(rows,rank)) for rows in combinations(normals,rank-1)}
    dirs.discard(None)
    for d in dirs:
        assert max(map(abs,d)) <= 1
        assert all(abs(dot(a,d)) <= 1 for a in normals)
    rays = {primitive(cross(rows,rank)) for rows in combinations(dirs,rank-1)}
    rays.discard(None)
    rays = sorted(rays | {tuple(-x for x in h) for h in rays})
    hbound = max(1,floor((rank-1)**((rank-1)/2))) if rank > 1 else 1
    assert all(max(map(abs,h)) <= hbound for h in rays)
    bases = []
    for indices in combinations(range(p),rank):
        b = [normals[i] for i in indices]
        db = int(det(b))
        assert db in [-1,0,1], ("non-TU", b, db)
        if db:
            inverse = [[(-1)**(i+j) * int(det([[b[ii][jj] for jj in range(rank) if jj != i]
                       for ii in range(rank) if ii != j])) // db
                       for j in range(rank)] for i in range(rank)]
            assert all(sum(b[i][k]*inverse[k][j] for k in range(rank)) == int(i==j)
                       for i in range(rank) for j in range(rank))
            bases.append((indices,inverse))
    duals = []
    for h in rays:
        candidates = []
        for indices,inv in bases:
            q = tuple(sum(inv[k][i]*h[k] for k in range(rank)) for i in range(rank))
            if min(q) >= 0:
                assert max(q) <= hbound, ("multiplier bound",h,q)
                sparse = tuple((indices[i],q[i]) for i in range(rank) if q[i])
                candidates.append(sparse)
        candidates = sorted(set(candidates))
        assert candidates
        duals.append(candidates)
    # All zero sums of <=rank+1 rows suffice. Supersets of a smaller zero
    # sum are redundant, and retaining them does not weaken any test.
    circuits = []
    for size in range(2,rank+2):
        for idx in combinations(range(p),size):
            if all(sum(normals[i][k] for i in idx)==0 for k in range(rank)):
                if not any(set(j).issubset(idx) for j in circuits):
                    circuits.append(idx)
    return normals,rays,duals,circuits,bases,hbound,len(dirs)


def state_endpoints(c,normals,weights,obs):
    where = {a:i for i,a in enumerate(normals)}
    d = [[w for _ in normals] for w in weights]
    for j,e,value in obs:
        a=tuple(c[e]); pos=where[a]; neg=where[tuple(-x for x in a)]
        d[j][pos]=min(d[j][pos],value)
        d[j][neg]=min(d[j][neg],-value)
    return d


def finite_membership(lib,d,aggregate):
    normals,rays,duals,circuits,bases,hbound,ndirs=lib
    for dj in d:
        if any(sum(dj[i] for i in circuit) < 0 for circuit in circuits):
            return False,'local'
    for h,candidates in zip(rays,duals):
        rhs=sum(min(sum(q*dj[i] for i,q in candidate) for candidate in candidates)
                for dj in d)
        if dot(h,aggregate)>rhs:
            return False,'aggregate'
    return True,'feasible'


def raw_lp(c,weights,obs,aggregate):
    rank=len(c[0]); states=len(weights); ub=[]; rhs=[]; eq=[]; erhs=[]
    for j,w in enumerate(weights):
        for a in c:
            for sign in [-1,1]:
                row=[0]*(rank*states)
                row[j*rank:(j+1)*rank]=[sign*x for x in a]
                ub.append(row); rhs.append(float(w))
    for j,e,value in obs:
        row=[0]*(rank*states); row[j*rank:(j+1)*rank]=c[e]
        eq.append(row); erhs.append(float(value))
    for k,value in enumerate(aggregate):
        row=[0]*(rank*states)
        for j in range(states): row[j*rank+k]=1
        eq.append(row); erhs.append(float(value))
    result=linprog(np.zeros(rank*states),A_ub=ub,b_ub=rhs,A_eq=eq,b_eq=erhs,
                   bounds=[(None,None)]*(rank*states),method='highs')
    assert result.status in [0,2], result.message
    return result.status==0


def exact_support_crosscheck(lib,d,limit):
    normals,rays,duals,circuits,bases,*_=lib
    checked=0
    for dj in d:
        vertices=set()
        for indices,inv in bases:
            v=tuple(dot(row,[dj[i] for i in indices]) for row in inv)
            if all(dot(a,v)<=b for a,b in zip(normals,dj)):
                vertices.add(v)
        local=not any(sum(dj[i] for i in circuit)<0 for circuit in circuits)
        assert bool(vertices)==local
        if not vertices: continue
        for h,candidates in list(zip(rays,duals))[:limit]:
            primal=max(dot(h,v) for v in vertices)
            dual=min(sum(q*dj[i] for i,q in candidate) for candidate in candidates)
            assert primal==dual,(h,primal,dual)
            checked+=1
    return checked


def run(name,c,count,seed):
    start=time.monotonic(); rng=random.Random(seed); rank=len(c[0]); lib=library(c)
    counts={'feasible':0,'local':0,'aggregate':0}; support_checks=0
    # Repeat a coordinate normal to exercise merging repeated arc observations.
    raw_c=c+[c[0]]
    for case in range(count):
        states=rng.randrange(2,6)
        integers=[rng.randrange(0,5) for _ in range(states)]
        if not sum(integers): integers[0]=1
        weights=[F(x,sum(integers)) for x in integers]
        theta=[[w*F(rng.randrange(-1,2),4) for _ in range(rank)] for w in weights]
        assert all(abs(dot(a,t))<=w for a in c for t,w in zip(theta,weights))
        obs=[]
        for j in range(states-1):
            for e,a in enumerate(raw_c):
                if rng.random()<.35:
                    obs.append((j,e,dot(a,theta[j])))
        aggregate=[sum(t[k] for t in theta) for k in range(rank)]
        if case%3==1:
            aggregate[rng.randrange(rank)]+=F(rng.choice([-1,1]),2)
        elif case%3==2 and obs:
            j,e,value=rng.choice(obs)
            obs.append((j,e,value+F(1,7)))
        d=state_endpoints(raw_c,lib[0],weights,obs)
        exact,kind=finite_membership(lib,d,aggregate)
        assert exact==raw_lp(raw_c,weights,obs,aggregate),(name,case,kind)
        counts[kind]+=1
        if case<3:
            support_checks+=exact_support_crosscheck(lib,d,8)
    normals,rays,duals,circuits,bases,hbound,ndirs=lib
    return {'graph':name,'rank':rank,'normals':len(normals),'directions':ndirs,
            'rays':len(rays),'bases':len(bases),'support_duals':sum(map(len,duals)),
            'circuits':len(circuits),'coefficient_bound':hbound,'cases':count,
            'outcomes':counts,'exact_support_checks':support_checks,
            'seconds':round(time.monotonic()-start,3)}


def sharp_section_check():
    c=[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]]
    tested=0; accepted=0
    for pi,qi in product(range(-4,5),repeat=2):
        p=F(pi,256); q=F(qi,256); w=2*p+q
        obs=[(0,0,p),(0,1,q),(0,4,F(0)),(1,0,F(0)),
             (1,5,F(0)),(2,2,F(0)),(2,3,F(0))]
        aggregate=[F(1,8),F(0),F(1,8)]
        feasible=raw_lp(c,[F(1,8)]*4,obs,aggregate)
        assert feasible==(w>=0),(p,q,w)
        tested+=1
        if feasible:
            states=[[p,q,p],[F(0),-q/2,q/2],
                    [q/2,-q/2,F(0)],[F(1,8)-w/2,F(0),F(1,8)-w/2]]
            assert all(abs(dot(a,t))<=F(1,8) for a in c for t in states)
            assert [sum(t[k] for t in states) for k in range(3)]==aggregate
            assert all(dot(c[e],states[j])==value for j,e,value in obs)
            accepted+=1
    return {'grid_points':tested,'feasible':accepted,'exact_decompositions':accepted}


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--cases',type=int,default=40)
    args=parser.parse_args()
    graphs=[('cycle',[[1]]),('theta',[[1,0],[0,1],[1,1]]),
            ('K4',[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]]),
            ('wheel4',[[int(i==j) for i in range(4)] for j in range(4)] +
                      [[1,0,0,1],[-1,1,0,0],[0,-1,1,0],[0,0,-1,-1]])]
    results=[run(name,c,args.cases,9017+i) for i,(name,c) in enumerate(graphs)]
    print(json.dumps({'seed_base':9017,'results':results,
                      'sharp_rank3_section':sharp_section_check()},indent=2))
