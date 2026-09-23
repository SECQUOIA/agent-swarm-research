"""Independent finite checks; these do not prove the manuscript's theorems."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb
from random import Random
import json

rng = Random(60301)

def matching(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, c in edges:
        adj[a].append((b, c))
        adj[b].append((a, c))
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        a = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << a)
        return min([solve(rest)] + [c + solve(rest ^ (1 << b))
            for b, c in adj[a] if rest >> b & 1])
    return solve((1 << n) - 1)

gadget_cases = 0
for _ in range(90):
    v = rng.randrange(2, 5)
    edges = [tuple(rng.sample(range(v), 2)) for _ in range(rng.randrange(0, 6))]
    costs = [rng.randrange(-7, 8) for _ in edges]
    deg = [sum(i in e for e in edges) for i in range(v)]
    tables = []
    for d in deg:
        increments = sorted(rng.randrange(-5, 7) for _ in range(d))
        table = [rng.randrange(-5, 6)]
        for inc in increments:
            table.append(table[-1] + inc)
        tables.append(table)
    brute = min(sum(tables[i][sum(z[j] for j,e in enumerate(edges) if i in e)]
        for i in range(v)) + sum(c*b for c,b in zip(costs,z))
        for z in product((0,1), repeat=len(edges)))
    m = len(edges)
    slots = []
    n = 2*m
    for d in deg:
        slots.append(list(range(n,n+d)))
        n += d
    gadget = []
    for j,(a,b) in enumerate(edges):
        gadget.append((2*j,2*j+1,0))
        for k,s in enumerate(slots[a]):
            gadget.append((2*j,s,tables[a][k+1]-tables[a][k]+costs[j]))
        for k,s in enumerate(slots[b]):
            gadget.append((2*j+1,s,tables[b][k+1]-tables[b][k]))
    bonus = 2*sum(abs(c) for a,b,c in gadget)+1
    augmented = [(a,b,c-bonus*((a<2*m)+(b<2*m))) for a,b,c in gadget]
    actual = matching(n,augmented)+2*m*bonus+sum(t[0] for t in tables)
    assert brute == actual, (edges,costs,tables,brute,actual)
    gadget_cases += 1

def choose(n,j):
    return comb(n,j) if 0 <= j <= n else 0

def moments(p,N):
    d = len(p)
    C = [sum(min((p[i] for i in A), default=F(1))
        for A in combinations(range(d),j)) for j in range(d+1)]
    P = []
    for j in range(d+1):
        value = F(0)
        for A in combinations(range(d),j):
            term = F(1)
            for i in A:
                term *= p[i]
            value += term
        P.append(value)
    s = sum(p)
    k = s.numerator//s.denominator
    V = [(1-(s-k))*choose(k,j)+(s-k)*choose(k+1,j) for j in range(d+1)]
    O = [F(0)]*(d+1)
    patterns = list(combinations(range(N),N//2))
    for pat in patterns:
        knots = sorted(set([F(0),F(1)] + [p[i] if i in pat else 1-p[i] for i in range(d)]))
        for lo,hi in zip(knots,knots[1:]):
            u = (lo+hi)/2
            K = sum(u<p[i] if i in pat else u>1-p[i] for i in range(d))
            for j in range(d+1):
                O[j] += (hi-lo)*choose(K,j)/len(patterns)
    return C,P,V,O

coefficient_cases = 0
regularity_cases = 0
for N in range(2,8):
    beta = F(N*(N-1),2*(N//2)*(N-N//2))
    for _ in range(25):
        d = rng.randrange(0,N+1)
        p = [F(rng.randrange(9),8) for _ in range(d)]
        C,P,V,O = moments(p,N)
        for j in range(d+2):
            cur = beta*C[j]+V[j]-P[j]-beta*O[j] if j<=d else F(0)
            if 0<=j-1<=d:
                cur += C[j-1]-P[j-1]
            assert cur >= 0, (N,p,j,cur)
            coefficient_cases += 1
        L = F(rng.randrange(5),2)
        a = [F(1)]*(d+1)
        for j in range(3,d+1):
            a[j] = a[j-1]*L*F(rng.randrange(5),4)
        cv,pv,vv,ov = [sum(x*y for x,y in zip(a,M)) for M in (C,P,V,O)]
        assert cv-vv <= (L+1)*(cv-pv)+beta*(cv-ov)
        regularity_cases += 1

print(json.dumps({'arithmetic':'exact integers and fractions',
    'matching_gadget_cases':gadget_cases,'coefficient_inequalities':coefficient_cases,
    'cardinality_mixture_cases':regularity_cases,'result':'PASS'},indent=2))
