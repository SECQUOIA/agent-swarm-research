"""Reviewer-created direct comparisons; no author checker imports.

Imports the algorithms under test only. Exhaustive cell words are evaluated
directly, including arbitrary mode dwell. A separate scipy LP formulation
uses durations instead of switch-time variables to check continuous optima.
"""
from fractions import Fraction as Q
from itertools import product, groupby, combinations_with_replacement
from pathlib import Path
from random import Random
import json, sys
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'relocated/verification/stage05'))
from continuous_exact import optimal_continuous
from coarsening import certified_coarsen
from rounding import optimal_few_switches

def changes(w):
    return sum(a != b for a,b in zip(w,w[1:]))

def grid_error(rows, dt, word):
    n=len(rows[0]); a=[Q(0)]*n; w=[Q(0)]*n; ans=Q(0)
    for row,h,mode in zip(rows,dt,word):
        w[mode]+=h
        a=[x+y for x,y in zip(a,row)]
        ans=max(ans,*(abs(x-y) for x,y in zip(a,w)))
    return ans

def dwell_ok(word,dt,dwell):
    return all(sum(dt[j] for j,_ in g)>=dwell[i]
               for i,g in groupby(enumerate(word),key=lambda p:p[1]))

def numeric_duration_lp(rows,dt,s,side):
    """Variables are k nonnegative block lengths plus E; sum lengths=T.

    The time of block j's end is sum of its first j lengths. Use this to
    independently form the piecewise-affine cumulative error coefficients.
    """
    n=len(rows[0]); k=s+1; T=sum(dt); N=len(dt)
    x=[Q(0)]; a=[[Q(0)]*n]
    for r,h in zip(rows,dt):
        x.append(x[-1]+h);a.append([u+v for u,v in zip(a[-1],r)])
    best=float(T); lpcount=0
    for cells in combinations_with_replacement(range(N),k-1):
        for word in product(range(n),repeat=k):
            B=[]; rhs=[]
            for j,c in enumerate(cells,1):
                coeff=[int(h<j) for h in range(k)]+[0]
                B.extend([coeff,[-v for v in coeff]])
                rhs.extend([x[c+1],-x[c]])
            for j in range(1,k+1):
                c=cells[j-1] if j<k else N-1
                for i in range(n):
                    rate=rows[c][i]/dt[c]
                    intercept=a[c][i]-rate*x[c]
                    coeff=[(rate-int(word[h]==i)) if h<j else Q(0) for h in range(k)]
                    B.append([-v for v in coeff]+[-1]);rhs.append(intercept)
                    if not side:
                        B.append(coeff+[-1]);rhs.append(-intercept)
            result=linprog([0]*k+[1],A_ub=np.array(B,float),b_ub=np.array(rhs,float),
                A_eq=[[1]*k+[0]],b_eq=[float(T)],bounds=[(0,float(T))]*(k+1),method='highs')
            assert result.success,result.message
            best=min(best,result.fun);lpcount+=1
    return best,lpcount

def main():
    rng=Random(917051); dwcases=0
    for n,N in [(2,5),(3,5),(4,4)]:
        for trial in range(8):
            dt=tuple(Q(rng.randint(1,5),rng.randint(1,7)) for _ in range(N))
            weights=[tuple(rng.randint(0,5) for i in range(n)) for j in range(N)]
            weights=[w if sum(w) else (1,)+(0,)*(n-1) for w in weights]
            rows=tuple(tuple(h*v/sum(w) for v in w) for h,w in zip(dt,weights))
            T=sum(dt)
            dwell=tuple(T*Q(rng.randint(0,6),5) for i in range(n))
            allwords=[(grid_error(rows,dt,w),w) for w in product(range(n),repeat=N) if dwell_ok(w,dt,dwell)]
            for s in range(N+1):
                vals=[e for e,w in allwords if changes(w)<=s]
                sol=optimal_few_switches(rows,dt,s,minimum_dwell=dwell)
                assert (sol is None)==(not vals)
                if vals:
                    assert sol.error==min(vals)==grid_error(rows,dt,sol.schedule())
                    assert dwell_ok(sol.schedule(),dt,dwell) and changes(sol.schedule())<=s
                dwcases+=1
    out=[]
    for n,N,s in [(2,2,1),(3,2,1),(2,2,2)]:
        dt=(Q(2,7),Q(5,9))
        weights=[tuple(rng.randint(1,5) for i in range(n)) for j in range(N)]
        rows=tuple(tuple(h*v/sum(w) for v in w) for h,w in zip(dt,weights))
        for side in (False,True):
            exact=optimal_continuous(rows,dt,s,one_sided=side)
            numeric,count=numeric_duration_lp(rows,dt,s,side)
            assert abs(numeric-float(exact.error))<1e-9
            # Universal coarsening certificate also checked against continuous,
            # not just the optimum on a finer grid.
            if not side:
                for M in (1,3,4):
                    cert=certified_coarsen(rows,dt,s,cells=M)
                    assert (cert.lower<exact.error if cert.lower_strict else cert.lower<=exact.error)
                    assert exact.error<=cert.upper
            out.append(dict(n=n,N=N,s=s,side=side,error=str(exact.error),programs=count))
    summary=dict(dwell_exhaustive_cases=dwcases,independent_continuous=out)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
