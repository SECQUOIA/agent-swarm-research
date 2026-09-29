"""Independent exact checks of the smoothed-penalty claims.

Finite cases corroborate the algebra, not the general convex-body theorem.
"""
from fractions import Fraction as F
from itertools import product
from random import Random

rng = Random(250925)


def knots(lo, hi, lines):
    out = {lo, hi}
    for a, b in lines:
        for c, d in lines:
            if a != c and lo < (d-b)/(a-c) < hi:
                out.add((d-b)/(a-c))
    return out


def value(lines, x):
    return max(a*x+b for a, b in lines)


penalty_cases = 0
for _ in range(600):
    slices = []
    for _ in range(rng.randint(1, 5)):
        lo = F(rng.randint(-8, 3), 4)
        hi = lo + F(rng.randint(1, 12), 4)
        lines = [(F(rng.randint(-6, 6)), F(rng.randint(-6, 6)))
                 for _ in range(rng.randint(1, 4))]
        slices.append((lo, hi, lines))
    b = F(rng.randint(-12, 16), 8)
    distances = [abs(b-x) for lo, hi, _ in slices for x in (lo, hi)]
    if not min(distances):
        continue
    feasible = [value(lines, b) for lo, hi, lines in slices if lo <= b <= hi]
    if not feasible:
        continue
    p = min(feasible)
    d = min(distances)/2
    all_values = [value(lines, x) for lo, hi, lines in slices
                  for x in knots(lo, hi, lines)]
    M = max(all_values)-min(all_values)
    for rho, strict in ((M/d, False), (M/d+1, True)):
        penalties = []
        for lo, hi, lines in slices:
            candidates = knots(lo, hi, lines)
            if lo <= b <= hi:
                candidates.add(b)
            for x in candidates:
                v = value(lines, x)+rho*abs(x-b)
                penalties.append(v)
                assert v >= p
                if strict and x != b:
                    assert v > p
        assert min(penalties) == p
    penalty_cases += 1


def boundary_distance(x, lo, hi):
    outside = max(max(l-v, F(0), v-u) for v, l, u in zip(x, lo, hi))
    return outside if outside else min(min(v-l, u-v) for v, l, u in zip(x, lo, hi))


grid_cases = 0
for m in (1, 2, 3):
    for _ in range(50):
        N = rng.randint(2, 11)
        sigma = F(rng.randint(1, 4), 2)
        center = [F(rng.randint(-2, 2)) for _ in range(m)]
        axes = [[c-sigma+sigma*F(2*j+1, N) for j in range(N)] for c in center]
        lo = [F(rng.randint(-8, 4), 4) for _ in range(m)]
        hi = [l+F(rng.randint(0, 12), 4) for l in lo]
        d = F(rng.randint(0, 5), 12)
        bad = sum(boundary_distance(x, lo, hi) <= d for x in product(*axes))
        assert F(bad, N**m) <= 2*m*(d/sigma+F(1, N))
        grid_cases += 1

sharpness_cases = 0
for K in range(2, 18):
    atoms = [F(j, K) for j in range(1, K)]
    for n in range(1, 80):
        b = F(n, 80)
        if b in atoms:
            continue
        left = [b-a for a in atoms if a < b]
        right = [a-b for a in atoms if a > b]
        left_req = 1/min(left) if left else F(0)
        right_req = 1/min(right) if right else F(0)
        rho = (left_req+right_req)/2
        lam = (right_req-left_req)/2
        assert -rho <= lam <= rho
        assert all(-1+lam*(a-b)+rho*abs(a-b) >= 0 for a in atoms)
        t = min(abs(a-b) for a in atoms)
        assert rho >= 1/(2*t)
        sharpness_cases += 1
    for T in (K, 2*K, 7*K):
        radius = F(1, 2*T)
        intervals = [(a-radius, a+radius) for a in atoms]
        assert intervals[0][0] >= 0 and intervals[-1][1] <= 1
        assert all(a[1] <= z[0] for a, z in zip(intervals, intervals[1:]))
        assert sum(z-a for a, z in intervals) == F(K-1, T)

print(f'PASS: {penalty_cases} exact piecewise-linear penalty cases; '
      f'{grid_cases} exact box/grid tube cases; '
      f'{sharpness_cases} exact optimized-penalty sharpness cases.')
