"""Independent finite checks. Exact rational checks unless explicitly numerical.

Run with /home/sgusev/miniconda3/envs/minlp-notes/bin/python.
No manuscript or existing verification code is imported.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import sqrt
import json
import sympy as sp


def edges(n):
    return list(combinations(range(n), 2))


def cuts(n, a, W=None):
    W = set(range(n)) if W is None else set(W)
    es = [(i, j, c) for (i, j), c in zip(edges(n), a) if i in W and j in W]
    vals = [sum(c*s[i]*s[j] for i,j,c in es) for s in product((-1,1), repeat=n)]
    return sum(abs(c) for _,_,c in es), F(max(vals)-min(vals), 2)


def check_graphs():
    n = 4
    subsets = [set(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
    worst = F(0)
    for a in product((-1,0,1), repeat=6):
        L, R = cuts(n,a)
        rho = max(F(sum(bool(c) for (i,j),c in zip(edges(n),a) if i in W and j in W),len(W)) for W in subsets if W)
        degree = [sum(bool(c) for (i,j),c in zip(edges(n),a) if k in (i,j)) for k in range(n)]
        assert L*L <= 16*rho*R*R
        assert L*L <= 4*max(degree)*R*R
        # Enumerate cut blocks and both sign sides independently of Q range.
        polar = 0
        for W in subsets:
            block = [(i,j,c) if i in W else (j,i,c) for (i,j),c in zip(edges(n),a) if (i in W) != (j in W)]
            polar = max(polar, max(sum(c*s[i]*s[j] for i,j,c in block) for s in product((-1,1),repeat=n)))
        assert polar == R
        # Numerical only: row square roots.
        assert float(R)+1e-12 >= sum(sqrt(d) for d in degree)/4
        # All rectangle densities are exact rational values.
        beta = max((F(sum(bool(c)*((i in W and j in Z)+(j in W and i in Z)) for (i,j),c in zip(edges(n),a)),len(W)+len(Z)) for W in subsets for Z in subsets if W or Z), default=F(0))
        assert beta == rho
        if R:
            worst = max(worst, F(L,R))
        # Exactness independently means existence of both prescribed cuts.
        pos = {(i,j) for (i,j),c in zip(edges(n),a) if c>0}
        neg = {(i,j) for (i,j),c in zip(edges(n),a) if c<0}
        support = pos | neg
        actual_cuts = [{(i,j) for i,j in support if (i in W)!=(j in W)} for W in subsets]
        assert (L == R) == (pos in actual_cuts and neg in actual_cuts)
    return {"graphs_exact": 729, "largest_center_ratio": str(worst), "row_norm_checks_numerical":729}


def check_envelopes():
    # Enumerate every basic feasible vertex law, with rational arithmetic.
    vertices = list(product((0,1),repeat=3))
    M = sp.Matrix([[1]*8]+[[v[i] for v in vertices] for i in range(3)])
    bases=[]
    for ids in combinations(range(8),4):
        B=M[:,ids]
        if B.det():
            bases.append((ids,B.inv()))
    means=list(product((F(0),F(1,4),F(1,2),F(3,4),F(1)), repeat=3))
    laws={}
    for p in means:
        laws[p]=[]
        rhs=sp.Matrix([1,*p])
        for ids,inv in bases:
            ws=inv*rhs
            if min(ws)>=0:
                law=[F(0)]*8
                for i,w in zip(ids,ws):
                    law[i]=F(w)
                laws[p].append(law)
        assert laws[p]
    def bounds(values,p):
        vals=[sum(w*y for w,y in zip(law,values)) for law in laws[p]]
        return min(vals),max(vals)
    checks=0
    for a in product((-2,0,3),repeat=3):
        values=[sum(c*v[i]*v[j] for (i,j),c in zip(edges(3),a)) for v in vertices]
        C=max((F(L,R) if R else F(0) for W in (set(i for i in range(3) if mask>>i&1) for mask in range(8)) for L,R in [cuts(3,a,W)]))
        for p in means:
            lo,hi=bounds(values,p)
            T=sum(abs(c)*min(p[i],p[j],1-p[i],1-p[j]) for (i,j),c in zip(edges(3),a))
            assert T <= C*(hi-lo)
            if all(x in (0,F(1,2),1) for x in p):
                L,R=cuts(3,a,{i for i,x in enumerate(p) if x==F(1,2)})
                assert hi-lo==R/2 and T==F(L,2)
            checks+=1
    # Exact nonnegative-box expansion and common upper test, including lower zero.
    boxchecks=0
    for ell,width in [((1,2,3),(1,2,1)),((0,1,0),(2,1,3))]:
        physical=[tuple(ell[i]+width[i]*v[i] for i in range(3)) for v in vertices]
        values=[sp.prod(v) for v in physical]
        expanded=[]
        for mask in range(8):
            support=[i for i in range(3) if mask>>i&1]
            coeff=sp.prod(width[i] if i in support else ell[i] for i in range(3))
            expanded.append((support,coeff))
        for p in means:
            lo,hi=bounds(values,p)
            term_upper=sum(c*(min(p[i] for i in S) if S else 1) for S,c in expanded)
            term_lower=sum(c*max(0,sum(p[i] for i in S)-len(S)+1) for S,c in expanded)
            assert hi==term_upper
            assert hi-lo <= term_upper-term_lower
            boxchecks+=1
    return {"bilinear_rational_LP_checks":checks,"box_rational_LP_checks":boxchecks,"nonsingular_bases":len(bases),"means":len(means)}


if __name__ == "__main__":
    print(json.dumps({"status":"PASS", "graph":check_graphs(),"envelopes":check_envelopes()},indent=2))
