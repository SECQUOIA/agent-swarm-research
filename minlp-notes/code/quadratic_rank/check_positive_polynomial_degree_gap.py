"""Exact selected-monomial midpoint gaps for the degree-gap example."""
from fractions import Fraction as Q

checks = 0
for M in range(2, 13):
    epsilon = Q(1,512*M)
    for j in range(1,M):
        k = 2**j
        x = 1-Q(1,k)
        for ell in range(j+1,M+1):
            y = 1-Q(1,2**ell)
            gap = (x**k+y**k)/2-((x+y)/2)**k
            assert gap >= Q(1,256)
            assert gap/M > epsilon
            checks += 1
print(f'PASS: {checks} exact parity-incompatible point pairs, through degree 2048')
