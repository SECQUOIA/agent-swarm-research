"""Independent finite checks; no finite result proves a universal theorem."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, prod
import json
from pathlib import Path


def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0


def moment(p, j, patterns):
    endpoints = sorted({Q(0), Q(1), *p, *(1-x for x in p)})
    value = Q(0)
    for coins in patterns:
        for a, b in zip(endpoints, endpoints[1:]):
            u = (a+b)/2
            k = sum(u < p[i] if coins[i] else u > 1-p[i] for i in range(len(p)))
            value += (b-a)*choose(k, j)
    return value/len(patterns)


def moments(p, ambient, fair=False):
    d = len(p)
    if fair:
        patterns = list(product((0, 1), repeat=d))
        beta = Q(2)
    else:
        patterns = [tuple(int(i in s) for i in range(d))
                    for s in combinations(range(ambient), ambient//2)]
        beta = Q(ambient*(ambient-1), 2*(ambient//2)*(ambient-ambient//2))
    s = sum(p)
    k = s.numerator//s.denominator
    theta = s-k
    C, P, O, V = [], [], [], []
    for j in range(d+2):
        C.append(moment(p, j, [tuple([1]*d)]))
        P.append(sum((prod(p[i] for i in subset) for subset in combinations(range(d), j)), Q(0)))
        O.append(moment(p, j, patterns))
        V.append((1-theta)*choose(k,j)+theta*choose(k+1,j))
    F = [beta*C[j]+V[j]-P[j]-beta*O[j]+(C[j-1]-P[j-1] if j else 0)
         for j in range(d+2)]
    return C, P, O, V, F, beta


def run():
    cases = 0
    for ambient in range(2, 8):
        for d in range(2, ambient+1):
            for p in [tuple(Q(i+1, d+2) for i in range(d)),
                      tuple(Q(i % 3, 2) for i in range(d)),
                      tuple([Q(1,2)]*d)]:
                C,P,O,V,F,beta = moments(p, ambient)
                assert min(F) >= 0
                for L in (Q(0), Q(1,3), Q(2)):
                    coeff = [Q(0), Q(0)]+[L**(j-2) for j in range(2,d+1)]
                    weighted = lambda values: sum(a*v for a,v in zip(coeff,values))
                    assert weighted(C)-weighted(V) <= (L+1)*(weighted(C)-weighted(P))+beta*(weighted(C)-weighted(O))
                cases += 1
    p = tuple(map(Q, ['2/5','7/10','24/25','97/100']))
    p2 = tuple(map(Q, ['2/5','7/10','959/1000','971/1000']))
    f1, f2 = moments(p,4,True)[4][3], moments(p2,4,True)[4][3]
    assert f1 == Q(6201,12500) and f2 == Q(4961031,10000000)
    assert f2-f1 == Q(231,10000000)
    radix_cases = 0
    for b in range(2,8):
        for L in range(2,13):
            M = lambda q: Q((L-q)*(b-1)+b,b**q)
            s = next(s for s in range(1,L) if M(s+1)<=1<=M(s))
            mix = (1-M(s+1))/(M(s)-M(s+1))
            weights = [Q(b-1,b**(l+1)) if l<L else Q(1,b**L) for l in range(L+1)]
            val = Q(0)
            for q,prob in [(s,mix),(s+1,1-mix)]:
                counts = [b**(l-q+1) if l>=q else 0 for l in range(L+1)]
                assert sum(w*r for w,r in zip(weights,counts)) == M(q)
                val += prob*sum(w*sum(min(b**j,r) for j in range(1,l+1))
                                for l,(w,r) in enumerate(zip(weights,counts)))
            assert val == s+Q(L-s,b**s)
            assert sum((M(q) for q in range(s+1,L+1)),Q(0)) == Q(L-s,b**s)
            radix_cases += 1
    parity_counts = {}
    for z in product((0,1),repeat=6):
        ab,bc,ca = z[0]==z[1], z[2]==z[3], z[4]==z[5]
        payoff = (int(ab and ca),int(not ab and bc),int(not bc and not ca))
        parity_counts[str(payoff)] = parity_counts.get(str(payoff),0)+1
        assert sum(payoff)<=1
    assert sorted(parity_counts.values()) == [16]*4
    return {'arithmetic':'exact rational/integer', 'coefficient_vectors':cases,
            'regularity_inequalities':3*cases, 'radix_pairs':radix_cases,
            'spreading_difference':str(f2-f1), 'parity_states':parity_counts,
            'result':'PASS', 'limit':'finite checks only; proofs reviewed separately'}


if __name__ == '__main__':
    out = run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
