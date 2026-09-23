"""Exact finite checks; not a proof for arbitrary graphs or coefficients."""
from fractions import Fraction
from itertools import combinations, product

n = 4
edges = list(combinations(range(n), 2))
signs = list(product((-1, 1), repeat=n))
checks = 0
for a in product((-1, 0, 1), repeat=len(edges)):
    active = [(i, j, w) for (i, j), w in zip(edges, a) if w]
    L = sum(abs(w) for i, j, w in active)
    values = [sum(w*s[i]*s[j] for i, j, w in active) for s in signs]
    R = Fraction(max(values)-min(values), 2)
    polarized = max(sum(w*s[i]*s[j] for i,j,w in active if ((S>>i)&1) != ((S>>j)&1)) for S in range(1<<n) for s in signs)
    assert R == polarized
    if not active:
        assert L == R == 0
        continue
    rho = max(Fraction(sum(1 for i,j,w in active if (S>>i)&1 and (S>>j)&1), S.bit_count()) for S in range(1, 1<<n))
    degrees = [sum(i==v or j==v for i,j,w in active) for v in range(n)]
    assert L*L <= 16*rho*R*R
    assert L*L <= 4*max(degrees)*R*R
    for S in range(1<<n):
        if all(((S>>i)&1) != ((S>>j)&1) for i,j,w in active):
            d1 = max(degrees[i] for i in range(n) if (S>>i)&1)
            d2 = max(degrees[i] for i in range(n) if not (S>>i)&1)
            assert L*L <= 2*min(d1,d2)*R*R
    # R=L iff positive and negative edge sets each coincide with a cut.
    each_sign_is_cut = all(any(all((((S>>i)&1) != ((S>>j)&1)) == (w == wanted) for i,j,w in active) for S in range(1<<n)) for wanted in (-1,1))
    assert (R == L) == each_sign_is_cut
    checks += 1
print(f'PASS: 729 coefficient vectors on K4 (including the zero vector); {checks} nonzero cases. Exact rational checks of polarization, density, degree, bipartite constants, and cut exactness.')
