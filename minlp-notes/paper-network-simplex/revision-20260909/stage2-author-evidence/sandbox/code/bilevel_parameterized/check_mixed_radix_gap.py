"""Exact independent diagnostics for the attributed diagonal-follower proof."""
from fractions import Fraction as F
from itertools import combinations, product


def clip(t):
    return max(F(0), min(F(1), t))


def distance(t, n):
    return min(abs(t-a) for a in range(n))


def main():
    n = k = 3
    pairs = list(combinations(range(n), 2))
    grid = [F(i, 2) for i in range(2*n-1)]
    checked = 0
    for mask in range(1 << len(pairs)):
        edges = {p for j,p in enumerate(pairs) if mask >> j & 1}
        table = [F(int(u == v or tuple(sorted((u,v))) not in edges))
                 for v in range(n) for u in range(n)]
        def phi(s):
            return table[0] + sum((table[a+1]-table[a])*clip(s-a)
                                  for a in range(n*n-1))
        has_clique = len(edges) == 3
        for t in product(grid, repeat=k):
            D = sum(distance(ti,n) for ti in t)
            value = 2*n*D + 2*sum(phi(t[i]+n*t[j]) for i,j in pairs)
            assert value >= 0
            if not has_clique:
                assert value >= 2
            checked += 1
        for t in product(range(n), repeat=k):
            value = 2*sum(phi(F(t[i]+n*t[j])) for i,j in pairs)
            valid = len(set(t)) == k and all(tuple(sorted((t[i],t[j]))) in edges for i,j in pairs)
            assert (value == 0) == valid
    triangles = 0
    for n in range(2,8):
        for denominator in range(1,8):
            for numerator in range((n-1)*denominator+1):
                t = F(numerator,denominator)
                value = sum((-1)**a*clip(2*t-a) for a in range(2*n-2))
                assert value == 2*distance(t,n)
                triangles += 1
        R = 2*n*n
        for h in [F(j,3) for j in range(-3*R,3*R+1)]:
            assert clip(h) == R*(clip(h/R)-clip((h-1)/R))
    print(f'PASS: {checked} exact continuous clique-gap samples; {triangles} triangle checks; normalized ramp identities')


if __name__ == '__main__':
    main()
