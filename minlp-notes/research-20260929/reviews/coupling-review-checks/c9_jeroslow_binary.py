"""Jeroslow's binary instance  max x_1 s.t. 2 sum x_i = n (n odd), x binary,
solved by LP-based B&B with variable fixing (any order). The LP relaxation
with a ones and b zeros fixed is feasible iff a <= m and b <= m (m=(n-1)/2)
and never integral, so a node is a leaf iff a = m+1 or b = m+1. This counts
leaves by explicit recursion, for comparison with Theorem 5.1's C(n+1,(n+1)/2).

Usage: python3 c9_jeroslow_binary.py
"""
from math import comb
from functools import lru_cache

def leaves(n):
    m = (n - 1) // 2
    @lru_cache(None)
    def L(a, b):
        if a >= m + 1 or b >= m + 1:
            return 1
        return L(a + 1, b) + L(a, b + 1)
    return L(0, 0)

for n in range(3, 26, 2):
    print(n, leaves(n), comb(n + 1, (n + 1) // 2), 2 ** ((n + 1) // 2))
