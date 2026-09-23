"""Exact finite checks; they do not prove the universal theorems."""
from fractions import Fraction as F
from itertools import combinations, product


def cut_data(n, weights, vertex_mask=None):
    if vertex_mask is None:
        vertex_mask=(1 << n)-1
    edges=[(i,j,a) for (i,j),a in weights.items()
           if a and vertex_mask >> i & 1 and vertex_mask >> j & 1]
    values=[sum(a*s[i]*s[j] for i,j,a in edges)
            for s in product((-1,1), repeat=n)]
    return sum(abs(a) for _,_,a in edges), F(max(values)-min(values), 2)

n=4
pairs=list(combinations(range(n),2))
for coeff in product((-1,0,1), repeat=len(pairs)):
    weights=dict(zip(pairs,coeff))
    support=[e for e,a in weights.items() if a]
    L,R=cut_data(n,weights)
    cross_max=max(sum(a*s[i]*s[j] for (i,j),a in weights.items()
                      if bool(mask >> i & 1) != bool(mask >> j & 1))
                  for mask in range(1<<n)
                  for s in product((-1,1),repeat=n))
    assert R==cross_max
    rho=max(F(sum(bool(mask>>i&1 and mask>>j&1) for i,j in support),
                  mask.bit_count()) for mask in range(1,1<<n))
    beta=max(F(sum(int(bool(r>>i&1 and c>>j&1))+
                        int(bool(r>>j&1 and c>>i&1)) for i,j in support),
                   r.bit_count()+c.bit_count())
             for r in range(1<<n) for c in range(1<<n) if r or c)
    assert rho==beta
    if L:
        assert R>0 and L**2 <= 16*rho*R**2

# The gap factor is discontinuous when a separate bad component disappears.
for eps in [F(1),F(1,10),F(1,100),F(0)]:
    weights={(0,1):eps,(1,2):eps,(2,3):eps,(0,3):-eps,(4,5):F(1)}
    ratios=[]
    for mask in range(1<<6):
        L,R=cut_data(6,weights,mask)
        ratios.append(L/R if R else F(0))
    assert max(ratios)==(2 if eps else 1)
    L,R=cut_data(6,weights)
    assert L/R==(1+4*eps)/(1+2*eps)

# A relative target falls with a worse incumbent outside theta <= 1.
theta=F(2)
assert (1-theta)*2 < (1-theta)*1
print('PASS: 729 exact K4 coefficient cases; 4 rational support-limit cases; target counterexample.')
