"""Independent exact stress checks for constrained quartic candidate cuts.

This is not an implementation of the cited FPT feasibility algorithm.
It tests rational primal-dual certificates and a one-dimensional integer
separator transcript for explicit convex quartics and degenerate fibers.
"""

from fractions import Fraction as F
from itertools import product
from math import ceil

# Every row is (A,B,c), representing Az+By<=c; there is one variable of each type.
def phi(x): return x*x+x**4
def dphi(x): return 2*x+4*x**3
def f(z,y,a,b): return phi(z-b)+phi(y-a)
def bounds(rows,z):
    lo=hi=None
    for A,B,c in rows:
        rhs=c-A*z
        if B==0:
            if rhs<0: return None
        elif B>0: hi=min(hi,rhs/B) if hi is not None else rhs/B
        else: lo=max(lo,rhs/B) if lo is not None else rhs/B
    if lo is not None and hi is not None and lo>hi: return None
    return lo,hi

def optimum(rows,z,a):
    bd=bounds(rows,z)
    if bd is None: return None
    lo,hi=bd
    return min(hi,max(lo,a) if lo is not None else a) if hi is not None else max(lo,a) if lo is not None else a

def residual(rows,z,y,lam,a,b):
    s=[c-A*z-B*y for A,B,c in rows]
    assert all(t>=0 for t in s) and all(t>=0 for t in lam)
    ry=dphi(y-a)+sum(B*l for (_,B,_),l in zip(rows,lam))
    E=sum(t*l for t,l in zip(s,lam))+ry*ry/4
    q=dphi(z-b)+sum(A*l for (A,_,_),l in zip(rows,lam))
    return E,q,ry,s

def qp(rows,z,y,a,b):
    # Exact rank-one orthant convex QP, accepted only after full KKT verification.
    s=[c-A*z-B*y for A,B,c in rows]
    t=dphi(y-a)
    trial=[[F(0)]*len(rows)]
    for j,(_,B,_) in enumerate(rows):
        if B:
            lam=[F(0)]*len(rows)
            lam[j]=max(F(0),-(2*s[j]+B*t)/(B*B))
            trial.append(lam)
    good=[]
    for lam in trial:
        E,q,ry,_=residual(rows,z,y,lam,a,b)
        grad=[s[j]+rows[j][1]*ry/2 for j in range(len(rows))]
        if all(t>=0 for t in grad) and all(l*t==0 for l,t in zip(lam,grad)):
            good.append((E,q,lam))
    assert good, (rows,z,y,a,b)
    return min(good,key=lambda t:t[0])

def farkas(rows,z):
    for j,(A,B,c) in enumerate(rows):
        if B==0 and c-A*z<0:
            al=[F(0)]*len(rows); al[j]=1; break
    else:
        al=None
        for i,(Ai,Bi,ci) in enumerate(rows):
            for j,(Aj,Bj,cj) in enumerate(rows):
                if Bi<0<Bj and (ci-Ai*z)/(-Bi)+(cj-Aj*z)/Bj<0:
                    al=[F(0)]*len(rows); al[i]=-1/Bi;al[j]=1/Bj;break
            if al is not None: break
        assert al is not None
    assert all(v>=0 for v in al)
    assert sum(row[1]*v for row,v in zip(rows,al))==0
    assert sum((c-A*z)*v for (A,B,c),v in zip(rows,al))<0
    return al

def models(scale):
    return [[],[(1,-1,0)],[(scale,-scale,0),(2,-2,0),(1,-1,1)],
        [(1,-1,2),(1,1,2)],[(1,-1,0),(-1,1,0),(1,0,2),(-1,0,2)],
        [(0,1,0),(0,-1,0),(1,0,1),(-1,0,1)],
        [(scale,-scale,0),(-scale,scale,scale/F(1024))],
        [(1,-1,0),(1,1,0)],[(F(1,3),-1,F(-1,5)),(F(-1,3),1,F(1,5))],
        [(0,-1,-1),(0,1,0)]]

stats=dict(certificates=0,large_multipliers=0,identities=0,inequalities=0,integer_cuts=0,farkas=0,zero_normals=0,tied_cuts=0)
mu=F(2)
for exp in [0,10,100,300]:
  for raw in models(F(1,2**exp)):
    rows=[tuple(map(F,row)) for row in raw]
    for a,b in product(map(F,[-1,0,F(1,2),1]),map(F,[-1,F(-1,2),0,F(1,2),1])):
      for z in map(F,range(-3,4)):
        p=optimum(rows,z,a)
        if p is None:
            al=farkas(rows,z);stats['farkas']+=1
            for w in map(F,range(-3,4)):
                if optimum(rows,w,a) is not None:
                    assert sum((c-A*w)*v for (A,B,c),v in zip(rows,al))>=0
            continue
        lo,hi=bounds(rows,z)
        G=1+abs(dphi(p-a))
        K=1+2+12*(abs(p-a)+1)**2
        delta=min(F(1),mu/(16*(G+1)),mu/(4*K))
        step=min(delta/2,mu*delta*delta/(8*(G+K+1)))
        if hi is None or p+step<=hi: y=p+step
        elif lo is None or p-step>=lo: y=p-step
        else: y=p
        assert abs(y-p)<=delta
        assert f(z,y,a,b)-f(z,p,a,b)<=mu*delta*delta/2
        lamstar=[F(0)]*len(rows)
        gp=dphi(p-a)
        if gp:
            j=next(j for j,(A,B,c) in enumerate(rows) if A*z+B*p==c and B*gp<0)
            lamstar[j]=-gp/rows[j][1]
        assert gp+sum(row[1]*l for row,l in zip(rows,lamstar))==0
        Estar,_,rstar,s=residual(rows,z,y,lamstar,a,b)
        assert sum(l*t for l,t in zip(lamstar,s))==gp*(y-p)
        assert Estar<=G*delta+K*K*delta*delta/(2*mu)<=3*mu/32
        stats['identities']+=1
        if max(lamstar,default=0)>2**200:stats['large_multipliers']+=1
        E,q,lam=qp(rows,z,y,a,b)
        assert E<=Estar<mu/4
        stats['certificates']+=1
        for w in map(F,range(-3,4)):
            v=optimum(rows,w,a)
            if v is None:continue
            # Independently evaluate the full primal-dual inequality (8).
            lhs=f(w,v,a,b)
            rhs=f(z,y,a,b)+q*(w-z)+mu*(w-z)**2/2-E
            assert lhs>=rhs
            stats['inequalities']+=1
            if w!=z:
                assert f(w,v,a,b)-f(z,p,a,b)>=q*(w-z)+mu*(w-z)**2/4
                stats['integer_cuts']+=1
                if f(w,v,a,b)<=f(z,p,a,b):
                    assert q*(w-z)<=-mu/4
                    if f(w,v,a,b)==f(z,p,a,b):stats['tied_cuts']+=1
                if q==0:
                    assert f(w,v,a,b)>f(z,p,a,b)
        if q==0:stats['zero_normals']+=1
print(stats)


def answer(rows, z, a, b):
    """A deterministic integer-query oracle, without objective comparisons."""
    p = optimum(rows, z, a)
    if p is None:
        al = farkas(rows, z)
        return False, sum(A*l for (A, B, c), l in zip(rows, al)), sum(
            c*l for (A, B, c), l in zip(rows, al)
        )
    lo, hi = bounds(rows, z)
    G = 1 + abs(dphi(p-a))
    K = 3 + 12*(abs(p-a)+1)**2
    delta = min(F(1), mu/(16*(G+1)), mu/(4*K))
    step = min(delta/2, mu*delta*delta/(8*(G+K+1)))
    if hi is None or p+step <= hi:
        y = p+step
    elif lo is None or p-step >= lo:
        y = p-step
    else:
        y = p
    E, q, lam = qp(rows, z, y, a, b)
    assert E < mu/4
    return True, q, q*z-mu/4


transcripts = dict(runs=0, queries=0, ties=0, early_stops=0, empty=0)
for exp in [0, 100, 300]:
    for raw in models(F(1, 2**exp)):
        rows = [tuple(map(F, row)) for row in raw]
        for a, b in product(map(F, [-1, 0, F(1, 2), 1]),
                            map(F, [-1, F(-1, 2), 0, F(1, 2), 1])):
            feasible = [z for z in map(F, range(-3, 4))
                        if bounds(rows, z) is not None]
            if not feasible:
                transcripts['empty'] += 1
                continue
            # Initialization only asks for feasibility, not an objective value.
            candidates = [feasible[0]]
            left, right = -3, 3
            while left <= right:
                z = F((left+right)//2)
                is_feasible, normal, rhs = answer(rows, z, a, b)
                transcripts['queries'] += 1
                if is_feasible:
                    candidates.append(z)
                    if normal == 0:
                        transcripts['early_stops'] += 1
                        break
                assert normal*z > rhs
                if normal > 0:
                    right = min(right, rhs//normal)
                elif normal < 0:
                    left = max(left, ceil(rhs/normal))
                else:
                    break
            # Exact values are used only after the oracle run to assess it.
            vals = {z: f(z, optimum(rows, z, a), a, b) for z in feasible}
            best = min(vals.values())
            optima = {z for z, value in vals.items() if value == best}
            assert optima.issubset(candidates)
            transcripts['runs'] += 1
            transcripts['ties'] += len(optima) > 1
print(transcripts)
