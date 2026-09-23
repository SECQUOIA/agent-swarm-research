"""Exact identities and PSD checks for the higher-order spatial-cover candidate.

The proof itself is elementary; numerical PSD is a supplementary regression
check. Falling-factorial identities and homogenization are checked exactly.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import random

import numpy as np


def falling(t, a):
    out = Q(1)
    for j in range(a):
        out *= t-j
    return out


def mu(s,t,a):
    return falling(t,a)/falling(Q(s),a)


def choose(t,a):
    return falling(t,a)/falling(Q(a),a)


def subsets(s,d):
    return [frozenset(S) for a in range(d+1) for S in combinations(range(s),a)]


def eigcheck(mat):
    eig = np.linalg.eigvalsh(np.array(mat,dtype=float))
    assert eig.min() >= -1e-9, eig.min()


def verify(s,t,r,rng):
    assert s >= 2*r and t >= 2*r-1 and s-t >= 2*r-1
    for ell in range(r+1):
        coeffs = [falling(t,2*r-j)*falling(s-t,j)/falling(Q(s),2*r)
                  for j in range(r+1)]
        assert all(c >= 0 for c in coeffs)
        assert mu(s,t,2*r-ell) == sum(comb(ell,j)*coeffs[j] for j in range(ell+1))
    base = subsets(s,r)
    moment = [[mu(s,t,len(I|J)) for J in base] for I in base]
    eigcheck(moment)
    homog = [frozenset(S) for S in combinations(range(s),r)]
    # Monomial homogenization, tested against arbitrary low-degree monomials.
    for _ in range(60):
        S,J = rng.choice(base),rng.choice(base)
        exact = sum(mu(s,t,len(T|J)) for T in homog if S <= T)
        exact /= choose(t-len(S),r-len(S))
        assert exact == mu(s,t,len(S|J))
    # All distinct slack-pattern sizes; symmetry covers index choices.
    for a in range(2*r+1):
        for b in range(2*r+1-a):
            v=a+b
            if v>s:
                continue
            pi=falling(t,a)*falling(s-t,b)/falling(Q(s),v)
            assert pi >= 0
            d=(2*r-v)//2
            rem=s-v
            localbase=subsets(rem,min(d,rem))
            # The fixed/slack sets are disjoint from the monomial basis.
            loc=[[falling(t,a+len(I|J))*falling(s-t,b)/falling(Q(s),v+len(I|J))
                  for J in localbase] for I in localbase]
            eigcheck(loc)
            if d:
                assert rem >= 2*d and t-a >= 2*d-1 and rem-(t-a)>=2*d-1
                for I in localbase:
                    for J in localbase:
                        direct=falling(t,a+len(I|J))*falling(s-t,b)/falling(Q(s),v+len(I|J))
                        assert direct == pi*mu(rem,t-a,len(I|J))
    return len(base)


def main():
    rng=random.Random(64157)
    dims=[]
    for s,t,r in [(2,Q(1),1),(3,Q(3,2),1),(6,Q(3),2),
                  (7,Q(7,2),2),(8,Q(3),2),(8,Q(4),2),
                  (10,Q(5),3),(11,Q(11,2),3),(11,Q(5),3)]:
        dims.append(verify(s,t,r,rng))
    print('All Gram decompositions, homogenization identities, conditioning identities,')
    print('and moment/localizer PSD checks passed; full moment dimensions:',dims)


if __name__ == '__main__':
    main()
