"""Reviewer checks: direct integration, alternative duration LPs, exact comparisons."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement, groupby
from pathlib import Path
from random import Random
import sys
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'relocated/verification/stage05'))
from continuous_exact import optimal_continuous
from coarsening import certified_coarsen
from rounding import optimal_few_switches

rng=Random(40517)

def knots(dt):
    v=[Q(0)]
    for x in dt: v.append(v[-1]+x)
    return v

def cumulative(rows, dt, t):
    xs=knots(dt)
    return [sum(row[i]*max(Q(0),min(t,b)-a)/d
                for row,d,a,b in zip(rows,dt,xs,xs[1:])) for i in range(len(rows[0]))]

def direct(rows,dt,word,ts,side=False):
    answer=Q(0)
    for t in sorted(set(knots(dt)+list(ts))):
        aa=cumulative(rows,dt,t)
        ww=[sum(max(Q(0),min(t,b)-a) for p,a,b in zip(word,ts,ts[1:]) if p==i)
            for i in range(len(aa))]
        answer=max(answer,*(w-a if side else abs(w-a) for a,w in zip(aa,ww)))
    return answer

def changes(w): return sum(a!=b for a,b in zip(w,w[1:]))

def random_input(n,N):
    dt=tuple(Q(rng.randint(1,4),rng.randint(2,7)) for _ in range(N))
    weight=[tuple(rng.randint(0,5) for _ in range(n)) for _ in dt]
    weight=[w if sum(w) else (1,)+(0,)*(n-1) for w in weight]
    return tuple(tuple(d*x/sum(w) for x in w) for w,d in zip(weight,dt)),dt

def dwell_ok(w,dt,dwell):
    return all(sum(dt[j] for j,_ in run)>=dwell[i]
               for i,run in groupby(enumerate(w),key=lambda p:p[1]))

def grid_tests():
    count=0
    for n,N in ((2,4),(3,4),(4,3)):
        for rep in range(6):
            rows,dt=random_input(n,N)
            dwell=tuple(Q(rng.randint(0,5),4) for _ in range(n)) if rep%2 else (Q(0),)*n
            objectives={w:direct(rows,dt,w,knots(dt)) for w in product(range(n),repeat=N)
                        if dwell_ok(w,dt,dwell)}
            for s in (0,1,2,8):
                values=[e for w,e in objectives.items() if changes(w)<=s]
                got=optimal_few_switches(rows,dt,s,minimum_dwell=dwell)
                assert (got is None)==(not values)
                if values:
                    assert got.error==min(values)==objectives[got.schedule()]
                    assert changes(got.schedule())<=s
                count+=1
    print('PASS independent direct grid/dwell cases:',count,flush=True)

def numeric_duration_optimum(rows,dt,s,side):
    """Independent LP formulation: block durations, sum constraint, affine samples."""
    n,N,k=len(rows[0]),len(dt),s+1
    xs=knots(dt); T=xs[-1]
    best=float(T)
    for word in product(range(n),repeat=k):
        for cells in combinations_with_replacement(range(N),k-1):
            mat=[]; rhs=[]
            for j,cell in enumerate(cells,1):
                rr=[Q(int(h<j)) for h in range(k)]+[Q(0)]
                mat.extend([rr,[-x for x in rr]]); rhs.extend([xs[cell+1],-xs[cell]])
            for j in range(1,k+1):
                cell=cells[j-1] if j<k else N-1
                rate=[x/dt[cell] for x in rows[cell]]
                start=cumulative(rows,dt,xs[cell])
                for i in range(n):
                    # A(sum duration[:j])-sum service[:j], using affine extension.
                    rr=[rate[i]-int(word[h]==i) if h<j else Q(0) for h in range(k)]
                    constant=start[i]-rate[i]*xs[cell]
                    mat.append([-x for x in rr]+[Q(-1)]); rhs.append(constant)
                    if not side:
                        mat.append(rr+[Q(-1)]); rhs.append(-constant)
            result=linprog([0]*k+[1],A_ub=np.array(mat,float),b_ub=np.array(rhs,float),
                           A_eq=[[1]*k+[0]],b_eq=[float(T)],
                           bounds=[(0,float(T))]*(k+1),method='highs')
            if result.success: best=min(best,result.fun)
            else: assert result.status==2
    return best

def continuous_tests():
    count=0
    # Independent analytic binary constant-rate one-switch optima.
    for a in [Q(j,7) for j in range(1,7)]:
        expected=a*(1-a)/(1+max(a,1-a))
        dt=(Q(2,5),Q(3,5))
        rows=tuple((d*a,d*(1-a)) for d in dt)
        got=optimal_continuous(rows,dt,1)
        assert got.error==expected==direct(rows,dt,got.modes,got.times)
        count+=1
    print('PASS independent analytic continuous cases:',count,flush=True)
    count=0
    for n,N,s in ((2,2,2),(2,2,2),(3,2,1),(3,2,1)):
        rows,dt=random_input(n,N)
        for side in (False,True):
            got=optimal_continuous(rows,dt,s,one_sided=side)
            assert got.error==direct(rows,dt,got.modes,got.times,side)
            benchmark=numeric_duration_optimum(rows,dt,s,side)
            assert abs(float(got.error)-benchmark)<1e-8
            count+=1
    print('PASS independent duration-LP comparisons (numerical optimum, exact returned error):',count,flush=True)

def transfer_tests():
    # Solve the supported prefix polytope with independent LP construction,
    # then verify every returned assignment exactly and at all original cuts.
    for case in range(36):
        n=rng.randint(2,6); N=rng.randint(1,9); h=Q(rng.randint(1,5),7); T=N*h
        ts=sorted({Q(0),T}|{T*Q(rng.randint(1,100),101) for _ in range(14)})
        word=tuple(rng.randrange(n) for _ in ts[1:])
        dt=tuple(b-a for a,b in zip(ts,ts[1:]))
        rows=tuple(tuple(d if i==p else Q(0) for i in range(n)) for d,p in zip(dt,word))
        ends=[h*j for j in range(N+1)]
        cum=[cumulative(rows,dt,t) for t in ends]
        support=[[cum[j+1][i]>cum[j][i] for i in range(n)] for j in range(N)]
        mat=[]; rhs=[]
        for j in range(1,N+1):
            for i in range(n):
                ss=cum[j][i]/h
                rr=[int(q<j and p==i) for q in range(N) for p in range(n)]
                mat.extend([rr,[-x for x in rr]])
                rhs.extend([-(-ss.numerator//ss.denominator),-(ss.numerator//ss.denominator)])
        eq=[[int(q==j) for q in range(N) for i in range(n)] for j in range(N)]
        bounds=[(0,1 if support[j][i] else 0) for j in range(N) for i in range(n)]
        result=linprog([rng.randint(-99,99) for _ in range(n*N)],A_ub=mat,b_ub=rhs,
                       A_eq=eq,b_eq=[1]*N,bounds=bounds,method='highs')
        assert result.success and all(abs(x-round(x))<1e-8 for x in result.x)
        y=[round(x) for x in result.x]
        chosen=tuple(next(i for i in range(n) if y[j*n+i]) for j in range(N))
        assert all(sum(y[j*n:(j+1)*n])==1 and support[j][chosen[j]] for j in range(N))
        for rr,b in zip(mat,rhs): assert sum(a*v for a,v in zip(rr,y))<=b
        assert changes(chosen)<=changes(word)
        assert direct(rows,dt,chosen,ends)<h
        # Construct the chronological source-block witnesses explicitly.
        idx=[next(q for q,(a,b,p) in enumerate(zip(ts,ts[1:],word))
                  if p==chosen[j] and max(a,ends[j])<min(b,ends[j+1])) for j in range(N)]
        assert idx==sorted(idx)
    print('PASS independent supported-transfer exact witnesses:',36,flush=True)

def coarse_tests():
    cases=0
    for rep in range(8):
        n,N,M=3,3,rng.choice((2,3,4))
        rows,dt=random_input(n,N); T=sum(dt)
        for s in (0,1,2):
            got=certified_coarsen(rows,dt,s,cells=M)
            ends=[T*Q(j,M) for j in range(M+1)]
            values=[direct(rows,dt,w,ends) for w in product(range(n),repeat=M) if changes(w)<=s]
            assert min(values)==got.exact_error==direct(rows,dt,got.schedule,ends)
            ca=[cumulative(rows,dt,t) for t in ends]
            assert got.coarse_masses==tuple(tuple(b-a for a,b in zip(ca[j],ca[j+1])) for j in range(M))
            cases+=1
    print('PASS independent nonaligned coarse integration/optimization cases:',cases,flush=True)

if __name__=='__main__':
    grid_tests(); continuous_tests(); transfer_tests(); coarse_tests()
