"""Exact formula witnesses checked against the original cumulative discrepancy.

This standard-library check is supplementary to the analytic proof. It expands
small controls and enumerates all one-switch schedules, without using the
three-term error identity for the evaluation.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from random import Random
import sys

if not __debug__:
    raise RuntimeError('Exact checks require Python without -O.')
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'reference'))
from minimax import minimax


def reconstruct(n, grid, winner):
    a,b,family,z = winner
    anchors = [(Q(0), [Q(0)]*3), (grid[a],z[:3]),
               (grid[b],z[3:6]), (grid[-1],z[6:9])]
    points = []
    for t,A in anchors:
        if points and t == points[-1][0]:
            assert A == points[-1][1]
        else:
            points.append((t,A))
    cumulative=[]
    for t in grid[1:]:
        left,right=next((p,q) for p,q in zip(points,points[1:]) if p[0] <= t <= q[0])
        A=[left[1][i]+(t-left[0])/(right[0]-left[0])*(right[1][i]-left[1][i]) for i in range(3)]
        cumulative.append(A[:2]+[A[2]]*(n-2))
    last=[Q(0)]*n
    for t,A in zip(grid[1:],cumulative):
        assert sum(A)==t and all(a>=b for a,b in zip(A,last))
        last=A
    return cumulative


def direct(cumulative,grid):
    n,N=len(cumulative[0]),len(cumulative)
    best=grid[-1]
    for p,q,switch in product(range(n),range(n),range(N+1)):
        W=[Q(0)]*n; peak=Q(0)
        for j,A in enumerate(cumulative):
            W[p if j<switch else q]+=grid[j+1]-grid[j]
            peak=max(peak,max(abs(a-w) for a,w in zip(A,W)))
        best=min(best,peak)
    return best


def run():
    rng=Random(40291); cases=0
    for n in range(3,9):
        for N in range(1,13):
            grid=list(map(Q,range(N+1)))
            value,winner=minimax(n,grid)
            assert direct(reconstruct(n,grid,winner),grid)==value
            if n==3:
                k,r=divmod(N,3)
                expected=Q(2,3) if N==1 else Q(k)+(Q(0),Q(1,2),Q(3,4))[r]
                assert value==expected
            cases+=1
    for _ in range(100):
        n,N=rng.randrange(3,10),rng.randrange(1,8)
        grid=[Q(0)]
        for j in range(N):grid.append(grid[-1]+Q(rng.randrange(1,35),rng.randrange(1,23)))
        value,winner=minimax(n,grid)
        assert direct(reconstruct(n,grid,winner),grid)==value
        # Scaling checks input units and complete witness reconstruction.
        scale=Q(17,29); scaled=[t*scale for t in grid]
        v,w=minimax(n,scaled)
        assert v==scale*value and direct(reconstruct(n,scaled,w),scaled)==v
        cases+=1
    n=9;grid=list(map(Q,['0','19/2','61/6','265/24','481/24','2669/120']));T=grid[-1]
    incomplete=max(min(((n-2)*grid[a]+grid[b])/n,
                  ((n-1)*T-grid[a-1]-(n-1)*grid[b-1])/n)
                  for a in range(1,len(grid)) for b in range(a,len(grid)))
    value,winner=minimax(n,grid)
    assert incomplete==Q(2077,216) and value==Q(2593,270)
    assert winner[2]=='low' and direct(reconstruct(n,grid,winner),grid)==value
    assert minimax(5,list(range(10)))[0]==Q(17,5)
    # Compact arithmetic remains exact with huge mode counts and narrow cells.
    for n in (10**100+7,10**200+3):
        eps=Q(1,10**100)
        grid=[Q(0),Q(1)-eps,Q(1),Q(1)+eps,Q(3)]
        value,winner=minimax(n,grid)
        assert Q(1)<=value<Q(3)
    print(f'{cases} expanded exact formula witnesses verified by direct schedule enumeration.')
    print('All three-mode residues through N=12; scaling, nonuniform failure, n=5,N=9 and huge arithmetic passed.')


if __name__=='__main__':run()
