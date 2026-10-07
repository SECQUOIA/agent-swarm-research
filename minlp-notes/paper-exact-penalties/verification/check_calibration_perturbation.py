"""Exact finite checks for calibration and RHS perturbations (standard library).

These check enumerated scalar balanced mixtures and small rational interval/
box examples, not NP-hardness, arbitrary convex geometry, or Gaussian measures.
"""
from fractions import Fraction as F
from itertools import combinations, product


def mixture_dual(points, rho):
    points = set(points)  # (residual, cost)
    values = [cost for residual, cost in points if residual == 0]
    for (a, fa), (b, fb) in product(points, repeat=2):
        if a > 0 > b:
            pa, pb = -b/(a-b), a/(a-b)
            values.append(pa*(fa+rho*a)+pb*(fb-rho*b))
    assert values
    return min(values)


def fixed_value(points, rho, lam):
    return min(cost+rho*abs(residual)+lam*residual for residual, cost in points)


box_cases = 0
zero_multiplier_cases = 0
for items in [(1,), (2,), (1, 3), (2, 4), (1, 2, 5), (2, 3, 6), (1, 3, 4, 8)]:
    for target in range(1, sum(items)+2):
        sums = {sum(a*x for a, x in zip(items+(target+1,), bits))
                for bits in product((0, 1), repeat=len(items)+1)}
        yes = target in sums
        for K in (2, 4, 7):
            native = [(F(K*s-(K*target+1)*q), F(-q))
                      for s, q in product(sums, (0, 1))]
            assert [(r, c) for r, c in native if r == 0] == [(0, 0)]
            dm, dp = K*(target-max(s for s in sums if s <= target))+1, K-1
            threshold = (F(1, dm)+F(1, dp))/2
            for rho in (F(0), F(1, 3), threshold, threshold+F(1, 7)):
                expected = min(F(0), -1+rho*F(2*dm*dp, dm+dp))
                lam = rho*F(dm-dp, dm+dp)
                assert mixture_dual(native, rho) == expected
                assert fixed_value(native, rho, lam) == expected
                box_cases += 1
            assert fixed_value(native, F(1), F(0)) == 0
            zero_threshold = max(F(1, dm), F(1, dp))
            assert fixed_value(native, zero_threshold, F(0)) == 0
            assert fixed_value(native, zero_threshold/2, F(0)) < 0
            assert all(cost+(zero_threshold+F(1, 7))*abs(residual) > 0
                       for residual, cost in native if residual)
            if K >= 3:
                assert zero_threshold == (F(1) if yes else F(1, K-1))
            zero_multiplier_cases += 1
            if K == 4:
                assert mixture_dual(native, F(1, 3)) == (F(-1, 2) if yes else F(0))


graph_cases = 0
for n in range(1, 5):
    edges = list(combinations(range(n), 2))
    for chosen in product((0, 1), repeat=len(edges)):
        edge_set = [edge for edge, selected in zip(edges, chosen) if selected]
        native = []
        alpha = 0
        for bits in product((0, 1), repeat=n):
            if any(bits[u]+bits[v] > 1 for u, v in edge_set):
                continue
            alpha = max(alpha, sum(bits))
            for pp, pm in ((0, 0), (1, 0), (0, 1)):
                if all(x <= pp+pm for x in bits):
                    native.append((F(pp-pm), F(-sum(bits))))
        for rho in (F(0), F(alpha, 2), F(alpha), F(alpha+1)):
            assert mixture_dual(native, rho) == min(F(0), rho-alpha)
            for lam in (F(-2), F(0), F(3, 2)):
                assert fixed_value(native, rho, lam) == min(F(0), rho-alpha-abs(lam))
            graph_cases += 1


def clipped_length(interval, clip=(F(-1), F(1))):
    a, b = interval
    return max(F(0), min(b, clip[1])-max(a, clip[0]))


fiber_cases = 0
for a, b in combinations([F(i, 2) for i in range(-4, 5)], 2):
    for radius in (F(0), F(1, 4), F(1, 2), F(1), F(2)):
        before = clipped_length((a, b))
        expanded = clipped_length((a-radius, b+radius))
        eroded = clipped_length((a+radius, b-radius))
        assert 0 <= expanded-before <= 2*radius
        assert 0 <= before-eroded <= 2*radius
        fiber_cases += 1


def box_boundary_distance(point, intervals):
    outside = max(max(a-x, x-b, F(0)) for x, (a, b) in zip(point, intervals))
    if outside:
        return outside
    return min(min(x-a, b-x) for x, (a, b) in zip(point, intervals))


def box_volume(intervals):
    result = F(1)
    for interval in intervals:
        result *= clipped_length(interval)
    return result


grid_cases = 0
intervals_to_check = [(F(-1, 2), F(1, 2)), (F(-2), F(2)),
                      (F(0), F(0)), (F(1, 3), F(2, 3))]
for m in (1, 2):
    for intervals in product(intervals_to_check, repeat=m):
        for d in (F(0), F(1, 8), F(1, 2)):
            outer = [(a-d, b+d) for a, b in intervals]
            inner = [(a+d, b-d) for a, b in intervals]
            tube_probability = (box_volume(outer)-box_volume(inner))/2**m
            assert 0 <= tube_probability <= min(F(1), 2*m*d)
            for q in (1, 2, 4, 8):
                centers = [-1+F(2*j+1, q) for j in range(q)]
                hits = sum(box_boundary_distance(point, intervals) <= d
                           for point in product(centers, repeat=m))
                assert F(hits, q**m) <= min(F(1), 2*m*(d+F(1, q)))
                endpoints = [-1+F(2*j, q) for j in range(q+1)]
                hits = sum(box_boundary_distance(point, intervals) <= d
                           for point in product(endpoints, repeat=m))
                assert F(hits, (q+1)**m) <= min(F(1), 2*m*(d+F(1, q))/(1+F(1, q)))
                grid_cases += 1

# The exact atomic correction is attained by a nondegenerate interval.
atomic_correction_cases = 0
for q in (2, 4, 8):
    grid = [-1+F(2*j+1, q) for j in range(q)]
    interval = [(grid[0], grid[-1])]
    hits = sum(box_boundary_distance((x,), interval) == 0 for x in grid)
    assert F(hits, q) == F(2, q)
    atomic_correction_cases += 1

# Selected finer grids ensure that the inequalities are nonvacuous (<1)
# in both dimensions, including a lower-dimensional box.
fine_grid_cases = 0
for intervals in [[(F(-1, 2), F(1, 2))],
                  [(F(-1, 2), F(1, 2)), (F(1, 3), F(2, 3))],
                  [(F(0), F(0)), (F(-1, 2), F(1, 2))]]:
    m = len(intervals)
    for q in (16, 32, 64):
        for d in (F(0), F(1, 64)):
            bound = 2*m*(d+F(1, q))
            assert bound < 1
            centers = [-1+F(2*j+1, q) for j in range(q)]
            hits = sum(box_boundary_distance(point, intervals) <= d
                       for point in product(centers, repeat=m))
            assert F(hits, q**m) <= bound
            endpoints = [-1+F(2*j, q) for j in range(q+1)]
            hits = sum(box_boundary_distance(point, intervals) <= d
                       for point in product(endpoints, repeat=m))
            assert F(hits, (q+1)**m) <= bound/(1+F(1, q))
            fine_grid_cases += 1

# Deterministic repair tested on affine-cost intervals (including M=0).
repair_cases = 0
families = [((F(-1), F(1), F(1), F(0)), (F(2), F(3), F(0), F(-1))),
            ((F(-1), F(1), F(0), F(2)), (F(2), F(3), F(0), F(2))),
            ((F(-2), F(2), F(-1), F(0)), (F(0), F(1), F(2), F(-2)))]
for slices in families:
    low = min(slope*x+intercept for a, b, slope, intercept in slices for x in (a, b))
    high = max(slope*x+intercept for a, b, slope, intercept in slices for x in (a, b))
    for rhs in [F(i, 8) for i in range(-7, 8)]:
        if any(rhs in (a, b) for a, b, _, _ in slices):
            continue
        feasible = [slope*rhs+intercept for a, b, slope, intercept in slices if a <= rhs <= b]
        if not feasible:
            continue
        margin = min(min(abs(rhs-a), abs(rhs-b)) for a, b, _, _ in slices)
        rho = (high-low)/(margin/2)
        points = [(x-rhs, slope*x+intercept)
                  for a, b, slope, intercept in slices
                  for x in ({a, b, rhs} if a <= rhs <= b else {a, b})]
        assert fixed_value(points, rho, F(0)) == min(feasible)
        assert all(cost+(rho+1)*abs(residual) > min(feasible)
                   for residual, cost in points if residual)
        repair_cases += 1

sharp_cases = 0
for b in [F(i, 32) for i in range(-31, 32) if i]:
    native = [(F(-1)-b, F(0)), (F(1)-b, F(0)), (F(0), F(0)), (-b, F(-1))]
    threshold = 1/(2*abs(b))
    assert mixture_dual(native, threshold) == 0
    assert mixture_dual(native, threshold/2) < 0
    lam = -threshold*(1 if b > 0 else -1)
    assert fixed_value(native, threshold, lam) == 0
    assert fixed_value(native, 2*threshold, F(0)) == 0
    sharp_cases += 1
for J in range(1, 10):
    for numerator in range(1, 10):
        u = F(numerator, 10*J)
        v = F(1, J)-u
        pa, pb = v/(u+v), u/(u+v)
        assert pa*u-pb*v == 0
        residual_average = pa*u+pb*v
        assert 1/residual_average >= 2*J
        sharp_cases += 1
for K in range(2, 10):
    for T in [F(K), F(3*K, 2), F(2*K)]:
        intervals = [(F(j, K)-1/(2*T), F(j, K)+1/(2*T)) for j in range(1, K)]
        assert all(0 <= a < b <= 1 for a, b in intervals)
        assert all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:]))
        assert sum(b-a for a, b in intervals) == (K-1)/T
        sharp_cases += 1

grid_tail_cases = 0
for K in range(2, 10):
    for multiple in (2, 3, 4):
        q = multiple*K
        centers = [F(2*j+1, 2*q) for j in range(q)]
        atoms = [F(j, K) for j in range(1, K)]
        adjacent = [b for b in centers if min(abs(b-a) for a in atoms) == F(1, 2*q)]
        assert len(adjacent) == 2*(K-1)
        for b in adjacent:
            native = [(-b, F(0)), (1-b, F(0)), (F(0), F(0))]
            native += [(a-b, F(-1)) for a in atoms]
            # A negative dual value below q verifies the threshold lower bound
            # at these centers independently of the distance count.
            assert mixture_dual(native, F(q)-F(1, 2)) < 0
        assert F(len(adjacent), q) == F(2*(K-1), q)
        grid_tail_cases += 1

atom_cases = 0
# A centered grid meeting the theorem's resolution requirement still has
# a zero atom: b0=0, sigma=1, m=1, K=2, epsilon=1/2.
atom_q = 17
assert atom_q >= 4*1*2/F(1, 2)
atom_grid = [-1+F(2*j+1, atom_q) for j in range(atom_q)]
assert F(sum(b == 0 for b in atom_grid), len(atom_grid)) == F(1, atom_q)
for rho in (F(0), F(1, 10), F(1), F(10), F(1000)):
    u = 1/(4*(rho+1))
    cost, residual = -u, u*u
    pa, pb = 1/(1+residual), residual/(1+residual)
    assert 0 < u <= 1 and u*u <= 1
    assert pa*residual-pb == 0
    assert pa*cost+rho*(pa*residual+pb) < 0
    assert (-pa*cost)/(pa*residual+pb) == 1/(2*u)
    atom_cases += 1

# Feasibility transfer (Section 7): if B uniform on Q=[-sigma,sigma] is
# feasible with probability p0, the centered grid is feasible with probability
# at least p0-2mK/q (here m=K=1, image an interval inside or overlapping Q),
# and running the construction with eps*p0/2 bounds the conditional failure.
feasibility_cases = 0
sigma = F(1)
for lo, hi in [(F(0), F(1, 1000)), (F(-1, 3), F(2, 7)), (F(1, 5), F(3)),
               (F(-5, 2), F(-9, 10)), (F(-1, 7), F(1, 7))]:
    p0 = (min(hi, sigma) - max(lo, -sigma)) / (2 * sigma)
    if p0 <= 0:
        continue
    for q in (1, 2, 3, 9, 17, 73, 128, 1001):
        grid = [-sigma + F(2 * j + 1, q) * sigma for j in range(q)]
        pg = F(sum(lo <= b <= hi for b in grid), q)
        assert pg >= p0 - F(2, q)
        feasibility_cases += 1
    for eps in (F(1, 2), F(1, 10), F(9, 10)):
        q = -(-8 // (eps * p0))  # ceil(4mK/(eps*p0/2)) with m=K=1
        grid = [-sigma + F(2 * j + 1, q) * sigma for j in range(q)]
        pg = F(sum(lo <= b <= hi for b in grid), q)
        assert pg >= p0 * (1 - eps / 4)
        assert (eps * p0 / 2) / pg <= eps / (2 - eps / 2) < eps
        feasibility_cases += 1

# Finite-grid quantile (Example ex:tail): with K dividing q, q >= 4K/eps and
# eps <= (K-1)/(2K), the centred grid on [0,1] has Pr{rho_*[G] > T} > eps for
# T=(K-1)/(2 eps), using the mixture lower bound rho_* >= 1/(2 t).
quantile_cases = 0
for K in (2, 3, 4, 7):
    for eps in (F(1, 20), F(1, 10), F(K - 1, 2 * K)):
        if eps > F(K - 1, 2 * K):
            continue
        q0 = -(-(4 * K) // eps)  # ceil(4K/eps)
        q = K * -(-q0 // K)  # least multiple of K that is >= q0
        assert q % K == 0 and q >= 4 * K / eps
        T = F(K - 1) / (2 * eps)
        assert K <= T <= q
        centres = [F(2 * i + 1, 2 * q) for i in range(q)]
        hits = 0
        for b in centres:
            t = min(abs(b - F(j, K)) for j in range(1, K))
            assert t > 0
            if 1 / (2 * t) > T:
                hits += 1
        frac = F(hits, q)
        assert frac >= (K - 1) * (1 / T - F(1, q))
        assert frac > eps
        quantile_cases += 1

print(f'PASS: {box_cases} binary-box and {graph_cases} unit-data graph dual cases;')
print(f'      {zero_multiplier_cases} fixed-zero-multiplier threshold cases;')
print(f'      {fiber_cases} clipped-fiber, {grid_cases} centered/endpoint-grid,')
print(f'      {fine_grid_cases} finer nonvacuous grid and {atomic_correction_cases} atomic-correction cases;')
print(f'      {repair_cases} deterministic-margin, {sharp_cases} tail/two-slice/adjacent-mixture,')
print(f'      {grid_tail_cases} finite-grid tail cases, and {atom_cases} infinite-threshold')
print('      witnesses at the zero atom of a concrete grid, and')
print(f'      {feasibility_cases} grid feasibility-transfer and {quantile_cases} grid-quantile cases, all exact rational.')
print('Not checked: general complexity reductions, arbitrary convex sets or Gaussian tube bounds.')
