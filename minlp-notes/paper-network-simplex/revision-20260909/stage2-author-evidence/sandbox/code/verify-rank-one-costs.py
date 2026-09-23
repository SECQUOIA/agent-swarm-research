"""Exact sanity checks for the rank-one-cost greedy-envelope algorithm.

The independent reference enumerates every row and column bound pattern, which
works for arbitrary cost matrices. Both paths compare rational-plus-square-root
values with exact sign-aware rational squaring; no solver tolerances are used.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def sign(x):
    return (x > 0) - (x < 0)


def sign_one_radical(a, b, d):
    """Sign of a+b*sqrt(d), for rational a,b,d and d>=0."""
    if not b or not d:
        return sign(a)
    if not a:
        return sign(b)
    if sign(a) == sign(b):
        return sign(a)
    return sign(a) * sign(a*a-b*b*d)


def compare(v, w):
    """Compare beta+sqrt(delta) pairs exactly, with nonnegative delta."""
    a, b, c = v[0]-w[0], v[1], w[1]
    sx = sign_one_radical(a, F(1), b)
    if sx < 0:
        return -1
    if sx == 0:
        return -sign(c)
    return sign_one_radical(a*a+b-c, 2*a, b)


def choose(best, candidate):
    return candidate if best is None or compare(candidate, best) < 0 else best


def piece_min(alpha, beta, gamma, lo, hi):
    best = (F(0), F(0)) if lo == 0 else None
    for s in {lo, hi}:
        if s > 0:
            best = choose(best, (alpha*s+beta+gamma/s, F(0)))
    if alpha > 0 and gamma > 0:
        d = gamma/alpha
        if lo*lo <= d <= hi*hi:
            best = choose(best, (beta, 4*alpha*gamma))
    return best


def interval(l, u, ll, uu):
    if any(a > b for a,b in zip(l,u)) or any(a > b for a,b in zip(ll,uu)):
        return None
    lo, hi = max(sum(l),sum(ll)), min(sum(u),sum(uu))
    return (lo,hi) if lo <= hi else None


def envelope(p, l, u, reverse):
    cursor, value = sum(l), sum(a*b for a,b in zip(p,l))
    pieces=[]
    for j in sorted(range(len(p)), key=lambda j:p[j], reverse=reverse):
        cap=u[j]-l[j]
        if cap:
            pieces.append((cursor,cursor+cap,p[j],value-p[j]*cursor))
            cursor += cap
            value += p[j]*cap
    return pieces or [(cursor,cursor,F(0),value)]


def greedy(p,q,l,u,ll,uu):
    totals=interval(l,u,ll,uu)
    if totals is None:
        return None
    lo,hi=totals
    if hi == 0:
        return F(0),F(0)
    curves=[envelope(p,l,u,r) for r in [False,True]]
    curves += [envelope(q,ll,uu,r) for r in [False,True]]
    breaks={lo,hi}
    for curve in curves:
        for left,right,_,_ in curve:
            breaks.update(t for t in [left,right] if lo <= t <= hi)
    breaks=sorted(breaks)
    cells=list(zip(breaks,breaks[1:])) or [(lo,hi)]
    best=None
    for left,right in cells:
        mid=(left+right)/2
        coeff=[]
        for curve in curves:
            coeff.append(next((a,b) for s,t,a,b in curve if s<=mid<=t))
        for a,b in coeff[:2]:
            for c,d in coeff[2:]:
                best=choose(best,piece_min(a*c,a*d+b*c,b*d,left,right))
    return best


def patterns(l,u):
    out=[]
    n=len(l)
    for k in range(n):
        others=[j for j in range(n) if j!=k]
        for choices in product([0,1],repeat=len(others)):
            intercept=[F(0)]*n
            for j,upper in zip(others,choices):
                intercept[j]=(u if upper else l)[j]
            total=sum(intercept)
            intercept[k]=-total
            slope=[F(0)]*n
            slope[k]=F(1)
            out.append((total+l[k],total+u[k],slope,intercept))
    return out


def exhaustive(C,l,u,ll,uu):
    totals=interval(l,u,ll,uu)
    if totals is None:
        return None
    lo,hi=totals
    best=(F(0),F(0)) if lo==0 else None
    for rl,rh,a,b in patterns(l,u):
        for cl,ch,c,d in patterns(ll,uu):
            left,right=max(lo,rl,cl),min(hi,rh,ch)
            if left>right or right==0:
                continue
            alpha=beta=gamma=F(0)
            for i in range(len(l)):
                for j in range(len(ll)):
                    alpha+=C[i][j]*a[i]*c[j]
                    beta+=C[i][j]*(a[i]*d[j]+b[i]*c[j])
                    gamma+=C[i][j]*b[i]*d[j]
            best=choose(best,piece_min(alpha,beta,gamma,left,right))
    return best


def main():
    # Sign branches, including an equality between differently encoded radicals.
    comparisons=[((F(0),F(4)),(F(2),F(0)),0),
                 ((F(-3),F(4)),(F(0),F(0)),-1),
                 ((F(2),F(3)),(F(1),F(8)),-1),
                 ((F(0),F(2)),(F(1),F(0)),1)]
    for v,w,expected in comparisons:
        assert compare(v,w)==expected
    rng=Random(20260904)
    feasible=infeasible=0
    for _ in range(160):
        m,n=rng.randint(1,3),rng.randint(1,3)
        p=[F(rng.randint(-3,3)) for _ in range(m)]
        q=[F(rng.randint(-3,3)) for _ in range(n)]
        l=[F(rng.randint(0,2),rng.choice([1,2])) for _ in range(m)]
        ll=[F(rng.randint(0,2),rng.choice([1,2])) for _ in range(n)]
        u=[v+F(rng.randint(0,3),rng.choice([1,2])) for v in l]
        uu=[v+F(rng.randint(0,3),rng.choice([1,2])) for v in ll]
        got=greedy(p,q,l,u,ll,uu)
        expected=exhaustive([[a*b for b in q] for a in p],l,u,ll,uu)
        assert (got is None)==(expected is None)
        if got is None:
            infeasible+=1
        else:
            assert compare(got,expected)==0, (p,q,l,u,ll,uu,got,expected)
            feasible+=1
    special=[([3,1],[2,1],[1,0],[1,1],[1,0],[1,1],(F(3),F(8))),
             ([1,-2],[2,3],[0,0],[0,0],[0,0],[1,1],(F(0),F(0))),
             ([1],[1],[1],[1],[1],[1],(F(1),F(0)))]
    for *data,value in special:
        args=[[F(v) for v in row] for row in data]
        assert compare(greedy(*args),value)==0
    print(f'Passed 160 exact comparisons: {feasible} feasible, {infeasible} infeasible.')
    print('Passed irrational optimum, zero-only total, and singleton-total regressions.')
    print('Exact rational/radical comparisons; no numerical tolerances.')


if __name__=='__main__':
    main()
