"""Checks the block-tensor moments and relative-gap example.

Affine identities/objective bounds use rational arithmetic. Full moment and
sampled localizing matrix PSD checks supplement the tensor proof.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
import random

import numpy as np

from check_higher_sos import falling


def monomials(n,d):
    return [tuple(I) for a in range(d+1) for I in combinations_with_replacement(range(n),a)]


def verify(t,r,restricted,rng):
    size=3*t
    G=len(restricted)
    n=G*size
    q0=t-2*r+2
    p=Q(1,2*t)
    K=Q(2*t+1,2)
    w=[Q(1)]*t+[p]*t+[Q(0)]*t
    bounds=[]
    for R in restricted:
        for i in range(size):
            if i not in R:
                bounds.append((Q(0),Q(1)))
            elif w[i]==1:
                bounds.append((Q(1,2),Q(1)))
            elif w[i]==0:
                bounds.append((Q(0),Q(1,2)))
            else:
                bounds.append((p/2,(1+p)/2))

    def block_moment(b,indices):
        R=set(restricted[b])
        if len(R)>=q0:
            val=Q(1)
            for i in indices:
                val*=w[i]
            return val
        U=set(range(size))-R
        residual=K-sum(w[i] for i in R)
        val=Q(1)
        for i in indices:
            if i in R:
                val*=w[i]
        support=len(set(indices)&U)
        return val*falling(residual,support)/falling(Q(len(U)),support)

    def moment(indices):
        parts=[[] for _ in range(G)]
        for i in indices:
            parts[i//size].append(i%size)
        val=Q(1)
        for b in range(G):
            val*=block_moment(b,parts[b])
        return val

    basis=monomials(n,r)
    M=np.array([[moment(I+J) for J in basis] for I in basis],dtype=float)
    assert np.linalg.eigvalsh(M).min()>-1e-9
    for b in range(G):
        for _ in range(30):
            I=tuple(rng.randrange(n) for _ in range(rng.randrange(2*r)))
            assert sum(moment(I+(b*size+i,)) for i in range(size))==K*moment(I)
    penalty=sum(moment((i,))-moment((i,i)) for i in range(n))
    assert penalty<=Q(sum(map(len,restricted)),2*q0)
    # Localizers for products of actual box slacks, including cross-block ones.
    for count in range(1,2*r+1):
        for _ in range(4):
            # Polynomial represented by monomial/constant coefficient terms.
            terms={():Q(1)}
            for _ in range(count):
                i=rng.randrange(n)
                a,b=bounds[i]
                choices=[((i,),Q(1)),((),-a)] if rng.randrange(2) else [((i,),Q(-1)),((),b)]
                nxt={}
                for I,c in terms.items():
                    for J,e in choices:
                        IJ=tuple(sorted(I+J))
                        nxt[IJ]=nxt.get(IJ,Q(0))+c*e
                terms=nxt
            localbasis=monomials(n,(2*r-count)//2)
            L=np.array([[sum(c*moment(I+J+S) for S,c in terms.items())
                         for J in localbasis] for I in localbasis],dtype=float)
            assert np.linalg.eigvalsh(L).min()>-1e-9
    return len(basis)


def main():
    rng=random.Random(63815)
    dims=[]
    for t,r,R in [(2,1,[[],[0]]),(3,2,[[],[0]]),(4,2,[[0],[5,10]])]:
        dims.append(verify(t,r,R,rng))
    tau=Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)
    assert tau==Q(17,128) and 2*tau/6==Q(17,384)
    print('Block tensor and cross-block localizer checks passed; moment dimensions:',dims)
    print('Relative-gap example constants verified exactly: tau=17/128, exponent=17n/384.')


if __name__=='__main__':
    main()
