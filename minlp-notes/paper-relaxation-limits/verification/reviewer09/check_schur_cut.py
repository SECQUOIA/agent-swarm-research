"""Exact finite checks of the combinatorial Schur-to-cut transfer, n=4.
This does not verify the external Schur/Grothendieck norm theorems.
"""
from itertools import combinations, product
from fractions import Fraction

n = 4
edges = list(combinations(range(n), 2))
subsets = [set(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
signs = list(product((-1, 1), repeat=n))
patterns = 0
for bits in product((0, 1), repeat=len(edges)):
    es = [e for e, flag in zip(edges, bits) if flag]
    rho = max(Fraction(sum(i in w and j in w for i, j in es), len(w)) for w in subsets if w)
    beta = max(Fraction(sum((i in r and j in c) + (j in r and i in c) for i, j in es), len(r)+len(c)) for r in subsets for c in subsets if r or c)
    assert rho == beta
    patterns += 1
weighted = 0
sharp_example = None
for a in product((-1, 0, 1), repeat=len(edges)):
    q = lambda s: sum(w*s[i]*s[j] for (i,j),w in zip(edges,a))
    vals = [q(s) for s in signs]
    osc = max(vals) - min(vals)
    cutnorm = 0
    fullnorm = 0
    for s in signs:
        for t in signs:
            p = tuple((u+v)//2 for u,v in zip(s,t))
            z = tuple((u-v)//2 for u,v in zip(s,t))
            bilinear = sum(w*(s[i]*t[j]+s[j]*t[i]) for (i,j),w in zip(edges,a))
            assert bilinear == 2*(q(p)-q(z))
            fullnorm = max(fullnorm,bilinear)
    assert fullnorm <= 2*osc
    for r in subsets:
        for s in signs:
            cutnorm=max(cutnorm,sum(w*s[i]*s[j] for (i,j),w in zip(edges,a) if (i in r)!=(j in r)))
    assert 2*cutnorm == osc
    if a == (1,0,-1,1,0,1):
        sharp_example = (sum(abs(w) for w in a), Fraction(osc,2))
    weighted += 1
print(f'PASS: {patterns} patterns: beta=rho; {weighted} coefficient vectors: exact polarization and infinity-to-one <= 4R.')
print(f'Frustrated C4 (L,R): {sharp_example}')
