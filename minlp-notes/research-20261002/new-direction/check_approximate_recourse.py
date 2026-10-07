"""Targeted exact-rational checks for approximate and mixed quartic recourse."""

from fractions import Fraction as Q
from random import Random


def value(spec, x, shifted):
    lam, mu, _, lo, hi, integer = spec
    return lam * x**4 + mu * x**2 / 2 + shifted * x


def coordinate(spec, shifted, eta):
    lam, mu, _, lo, hi, integer = spec
    if integer:
        lo, hi = int(lo), int(hi)
        left, right = lo, hi
        while left < right:
            mid = (left + right) // 2
            delta = value(spec, Q(mid + 1), shifted) - value(spec, Q(mid), shifted)
            if delta >= 0:
                right = mid
            else:
                left = mid + 1
        x = Q(left)
        if x > lo:
            assert value(spec, x, shifted) <= value(spec, x - 1, shifted)
        if x < hi:
            assert value(spec, x, shifted) <= value(spec, x + 1, shifted)
        return x, Q(0)

    def derivative(x):
        return 4 * lam * x**3 + mu * x + shifted

    if derivative(lo) >= 0:
        return lo, Q(0)
    if derivative(hi) <= 0:
        return hi, Q(0)
    curvature = 12 * lam * max(abs(lo), abs(hi))**2 + mu
    while curvature * (hi - lo)**2 / 8 > eta:
        mid = (lo + hi) / 2
        if derivative(mid) <= 0:
            lo = mid
        else:
            hi = mid
    assert derivative(lo) <= 0 <= derivative(hi)
    return (lo + hi) / 2, curvature * (hi - lo)**2 / 8


def oracle(specs, row, alpha, a, eta):
    points, errors = [], []
    upper = alpha * a * a / 2
    for spec, coefficient in zip(specs, row):
        shifted = spec[2] - alpha * a * coefficient
        x, error = coordinate(spec, shifted, eta / len(specs))
        points.append(x)
        errors.append(error)
        upper += value(spec, x, shifted)
    assert sum(errors) <= eta
    return upper - sum(errors), upper, points


def original(specs, row, alpha, point):
    projection = sum(t * x for t, x in zip(row, point))
    return sum(value(s, x, s[2]) for s, x in zip(specs, point)) - alpha * projection**2 / 2


def refine(specs, row, alpha, bounds, optimum, levels, target=None):
    cells = [bounds]
    width = bounds[1] - bounds[0]
    incumbent = None
    witness = None
    calls = 0
    counts = []
    for level in range(levels):
        mesh = width / 2**level
        delta = alpha * mesh**2 / 8
        eta = min(Q(1), delta)
        evaluated = []
        for left, right in cells:
            lows = []
            for corner in (left, right):
                lower, upper, point = oracle(specs, row, alpha, corner, eta)
                assert original(specs, row, alpha, point) <= upper
                if incumbent is None or upper < incumbent:
                    incumbent, witness = upper, point
                lows.append(lower)
                calls += 1
            evaluated.append((left, right, min(lows) - alpha * (right - left)**2 / 8))
        kept = [cell for cell in evaluated if cell[2] < incumbent]
        lower = min([incumbent] + [cell[2] for cell in kept])
        assert lower <= optimum <= original(specs, row, alpha, witness) <= incumbent
        assert incumbent - lower <= delta + eta
        counts.append(len(kept))
        if target is not None and incumbent - lower < target:
            return calls, counts, witness, incumbent - lower
        if not kept:
            return calls, counts, witness, Q(0)
        cells = [child for lo, hi, _ in kept for child in ((lo, (lo + hi) / 2), ((lo + hi) / 2, hi))]
    return calls, counts, witness, incumbent - lower


random = Random(261002)
for _ in range(100):
    lo = random.randint(-8, 0)
    hi = random.randint(0, 9)
    spec = (Q(random.randint(0, 3)), Q(random.randint(0, 4)), Q(0), Q(lo), Q(hi), True)
    shifted = Q(random.randint(-30, 30), random.randint(1, 5))
    x, error = coordinate(spec, shifted, Q(1, 100))
    assert error == 0
    assert value(spec, x, shifted) == min(value(spec, Q(z), shifted) for z in range(lo, hi + 1))

# Dense rank-one interaction, one integer and one continuous coordinate.
# F=x^4+4x+y^4-(x+y)^2, x in {0,1,2,3}, y in [0,1].
# x>=1 costs at least 2 more than x=0; optimum is -1/4 at (0,1/sqrt(2)).
mixed = [(Q(1), Q(0), Q(4), Q(0), Q(3), True),
         (Q(1), Q(0), Q(0), Q(0), Q(1), False)]
calls, counts, point, gap = refine(mixed, [Q(1), Q(1)], Q(2), (Q(0), Q(4)), Q(-1, 4), 10)
assert gap <= Q(1, 2**12)
assert point[0] == 0
print('PASS: mixed quartic refinement:', calls, 'oracle calls; retained:', counts)

# A huge integer interval is searched logarithmically. D=3 and gap<1/3
# certify exact optimality for F=x^4-x^2-x/3, whose integer optimum is x=1.
integer = [(Q(1), Q(0), Q(-1, 3), Q(0), Q(2**40), True)]
calls, counts, point, gap = refine(integer, [Q(1)], Q(2), (Q(0), Q(2**40)), Q(-1, 3), 45, Q(1, 3))
assert gap < Q(1, 3) and point == [Q(1)]
print('PASS: pure integer exact gap recovery:', calls, 'oracle calls;', len(counts), 'levels; 2^40+1 feasible integers')
print('PASS: 100 integer oracle comparisons against exhaustive small-domain minima')
