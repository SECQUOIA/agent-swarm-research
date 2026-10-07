"""Targeted regressions for HNF, exact shortening, flags and Proposition C(c)."""
import random
from fractions import Fraction as F
from unittest.mock import patch

from sympy import Matrix

import lattice

rng = random.Random(20261003)
count = 0
for r in range(1, 5):
    for _ in range(10):
        n = r + 3
        while True:
            M = Matrix([[rng.randint(-20, 20) for _ in range(n)] for _ in range(r)])
            if M.rank() == r:
                break
        H, U = lattice.col_hnf(M.tolist())
        H, U = Matrix(H), Matrix(U)
        assert abs(U.det()) == 1
        assert M * U == H.row_join(Matrix.zeros(r, n - r))
        assert all(H[i, i] > 0 for i in range(r))
        assert all(H[i, j] == 0 for i in range(r) for j in range(i + 1, r))
        assert all(0 <= H[i, j] < H[i, i] for i in range(r) for j in range(i))
        count += 1
print('Reduced HNF, unimodularity and full kernel:', count, 'passed')

large = 10**350
K = [[large, 1], [1, 0], [0, 1]]
short = [2, 3, -1]
v = [short[i] + large * K[i][0] - (large + 7) * K[i][1] for i in range(3)]
reduced = lattice.shorten_mod_kernel(v, K)
# The kernel is exactly the kernel of [1, -large, -1].
assert reduced[0] - large * reduced[1] - reduced[2] == short[0] - large * short[1] - short[2]
assert sum(a * a for a in reduced) <= sum(a * a for a in short)
print('350-digit kernel and 701-digit representative: exact coset preserved and shortened')

X = [[F(1), F(1, 2)], [F(1, 2), F(1, 4)]]
original = lattice.cvp_enum
def capped_second(*args, **kwargs):
    z, val, nodes, complete, found = original(*args, **kwargs)
    return z, val, nodes, False, found
with patch.object(lattice, 'cvp_enum', side_effect=capped_second):
    result = lattice.thm3_exact(X)
assert result['first_complete'] and not result['second_complete'] and not result['complete']
assert result['q'] == -F(1, 4) and result['optimum_certified']
assert lattice.q_exact(X, result['v']) == result['q']
print('Second enumeration cap retained; exact -1/4 optimality certificate kept separately')

def late_minimum(*args, **kwargs):
    # In this rank-1 image lattice, z=-1 attains -1/4; z=0 is unviolated.
    return None, None, 201, True, [(0.25, [0])] * 200 + [(0.0, [-1])]
with patch.object(lattice, 'cvp_enum_c', return_value=([0], 0.25, 1, True)), \
        patch.object(lattice, 'cvp_enum', side_effect=late_minimum):
    result = lattice.thm3_exact(X)
assert result['complete'] and result['q'] == -F(1, 4)
assert lattice.q_exact(X, result['v']) == result['q']
print('Candidate 201 checked exactly; no hidden 200-candidate truncation')

def capped_without_minimizer(*args, **kwargs):
    # A nonempty capped collection omits the C search's exact minimizer.
    return None, None, 1, False, [(0.25, [0])]
with patch.object(lattice, 'cvp_enum', side_effect=capped_without_minimizer):
    result = lattice.thm3_exact(X)
assert result['first_complete'] and not result['second_complete'] and not result['complete']
assert result['q'] == -F(1, 4) and result['optimum_certified']
assert lattice.q_exact(X, result['v']) == result['q']
print('Nonempty capped collection retains the first minimizer for exact verification')

for D in range(2, 9):
    x = F(D - 1, D)
    X = [[F(1), x], [x, x * x]]
    a = D // 2
    elementary = -lattice.q_exact(X, [-1, 1])
    raw = -lattice.q_exact(X, [-a, a])
    assert raw == F(D * D // 4, D * D)
    assert (raw / (a * a) == elementary) if D < 4 else (raw / (a * a) < elementary)
print('Proposition C(c), D=2..8: equality at 2,3 and strict domination at 4..8')
print('ALL REVISION REGRESSION CHECKS PASSED')
