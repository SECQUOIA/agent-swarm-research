"""Independent finite Stage 3 checks; standard library exact rational arithmetic.

Run from any directory. No manuscript/author verifier imports. These finite tests
do not prove a universal inequality or validate a numerical optimization solver.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb
from collections import Counter
import json

def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0

def moments(p, N, fair=False):
    d = len(p)
    C = [Q(0)] * (d + 2)
    P = C.copy()
    O = C.copy()
    cuts = sorted({Q(0), Q(1), *p, *(1-x for x in p)})
    for mask in product((0, 1), repeat=d):
        prob = Q(1)
        for x, z in zip(p, mask):
            prob *= x if z else 1-x
        k = sum(mask)
        for j in range(d + 2):
            P[j] += prob * choose(k, j)
        orient_prob = Q(1, 2**d) if fair else Q(choose(N-d, N//2-k), comb(N, N//2))
        for a, b in zip(cuts, cuts[1:]):
            u = (a+b)/2
            ko = sum(u < x if z else u > 1-x for x, z in zip(p, mask))
            for j in range(d + 2):
                O[j] += orient_prob * (b-a) * choose(ko, j)
    for a, b in zip(cuts, cuts[1:]):
        k = sum((a+b)/2 < x for x in p)
        for j in range(d + 2):
            C[j] += (b-a) * choose(k, j)
    s = sum(p, Q(0))
    k = s.numerator // s.denominator
    V = [(1-s+k)*choose(k,j)+(s-k)*choose(k+1,j) for j in range(d+2)]
    return C, P, O, V

counts = Counter()
grid = [Q(i,4) for i in range(5)]
for N in range(2,8):
    beta = Q(N*(N-1), 2*(N//2)*(N-N//2))
    for d in range(0,min(N,5)+1):
        for p in combinations_with_replacement(grid,d):
            C,P,O,V = moments(p,N)
            assert C[0] == P[0] == O[0] == V[0] == 1
            for j in range(d+2):
                F = beta*(C[j]-O[j])+V[j]-P[j]
                if j: F += C[j-1]-P[j-1]
                assert F >= 0, (N,p,j,F)
                counts['coefficient_orders_exact'] += 1
            # Test full cardinality factors with vanishing coefficients and L=0.
            for L in [Q(0),Q(1,2),Q(3)]:
                coeff = [Q(2),Q(3)]+[L**(j-2) for j in range(2,d+2)]
                # truncate at d; out-of-range moments already vanish
                vals = [sum(coeff[j]*m[j] for j in range(d+1)) for m in (C,P,O,V)]
                c,pp,o,v = vals
                assert c-v <= (L+1)*(c-pp)+beta*(c-o)
                counts['cardinality_factors_exact'] += 1

# Check all affine cap inequalities at all breakpoints, and exact profile means.
for b in range(2,11):
    for L in range(2,31):
        M = {q:Q((L-q)*(b-1)+b,b**q) for q in range(1,L+1)}
        s = next(s for s in range(1,L) if M[s]>=1>=M[s+1])
        w = [Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
        mix = (1-M[s+1])/(M[s]-M[s+1])
        obj = Q(0)
        mean = Q(0)
        for l in range(L+1):
            cap = sum(b**j for j in range(1,max(0,l-s)+1))
            for r in [0]+[b**j for j in range(L+1)]:
                assert sum(min(b**j,r) for j in range(1,l+1)) <= s*r+cap
            for q,t in [(s,mix),(s+1,1-mix)]:
                r = b**(l-q+1) if l>=q else 0
                payoff = sum(min(b**j,r) for j in range(1,l+1))
                assert payoff == s*r+cap
                mean += w[l]*t*r
                obj += w[l]*t*payoff
        assert mean == 1
        assert obj == s+Q(L-s,b**s)
        assert sum(M[q] for q in range(s+1,L+1)) == Q(L-s,b**s)
        counts['radix_parameter_pairs_exact'] += 1

# Independent certificate of the six-bit factor obstruction.
types = Counter()
for z in product((0,1),repeat=6):
    ab,bc,ca = [z[i]==z[i+1] for i in (0,2,4)]
    g = (int(ab and ca),int(not ab and bc),int(not bc and not ca))
    assert sum(g)<=1
    types[str(g)] += 1
assert sorted(types.values()) == [16]*4
counts['parity_vertices_exact'] = 64

# Enumerate small integer PARTITION inputs and certify the reduction without LP.
for n in range(2,7):
    for raw in combinations_with_replacement(range(1,5),n):
        a = tuple(2*x for x in raw)
        A = sum(a)
        eps = Q(1,16*A**3)
        d0 = 1-eps**2*Q(A*A,8)
        pi = [eps*x+eps**2*Q(A*x-x*x,2) for x in a]
        yes = False
        minimum = None
        for z in product((0,1),repeat=n):
            S = sum(x*y for x,y in zip(a,z))
            yes |= 2*S==A
            C = Q(1)
            for x,y in zip(a,z): C *= 1+eps*x*y
            second = 1+eps*S+eps**2*Q(S*S-sum(x*x*y for x,y in zip(a,z)),2)
            R = C-second
            assert 0<=R<=eps**2/8
            weighted = C-sum(x*y for x,y in zip(pi,z))
            assert weighted == d0+eps**2*Q((S-A//2)**2,2)+R
            minimum = weighted if minimum is None else min(minimum,weighted)
            counts['hardness_vertices_exact'] += 1
        assert minimum <= d0+eps**2/8 if yes else minimum>=d0+eps**2/2
        counts['hardness_instances_exact'] += 1
        counts['partition_yes' if yes else 'partition_no'] += 1

print(json.dumps({'status':'PASS','counts':dict(counts),'parity_types':dict(types),
 'limits':'Finite exact tests, not universal proofs. Radix cap tests cover all piecewise-linear breakpoints for these parameter pairs.'},indent=2))
