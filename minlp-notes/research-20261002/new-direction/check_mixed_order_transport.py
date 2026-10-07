"""Exact checks of mixed-order transport and the finite-grid count.

Model: 0 <= v <= w <= z <= 1, with z binary, and
F0=(w-v/2)^2-v^2/2+z/3. The full Hessian is bounded above by 3I.
The bag being counted is {v}; its true outside recourse is computed exactly.
This checks neither the full sparse DP nor its algebraic fallback.
"""

from fractions import Fraction as Q
from itertools import product


def objective(v, w, z, noise):
    gv, gw, gz = noise
    return (w-v/2)**2-v*v/2+z/3+gv*v+gw*w+gz*z


def feasible(v, w, z):
    return z in (0, 1) and 0 <= v <= w <= z <= 1


def global_minimum(noise):
    """All stationary faces of the z=1 triangle, plus the z=0 point."""
    gv, gw, _ = noise
    points = [(Q(0), Q(0), Q(0)),
              (Q(0), Q(0), Q(1)),
              (Q(0), Q(1), Q(1)),
              (Q(1), Q(1), Q(1))]
    candidates = [(Q(0), -gw/2), (2*(gv-1), Q(1)),
                  (2*(gv+gw), 2*(gv+gw)),
                  (gv+gw/2, gv/2-gw/4)]
    points += [(v, w, Q(1)) for v, w in candidates
               if feasible(v, w, Q(1))]
    return min((objective(v, w, z, noise), (v, w, z))
               for v, w, z in points)


def recourse(v, noise):
    """Value excludes bag noise gv*v, as in the conditional count."""
    _, gw, _ = noise
    w = min(Q(1), max(v, (v-gw)/2))
    points = [(w, Q(1))]
    if v == 0:
        points.append((Q(0), Q(0)))
    return min((objective(v, w, z, noise)-noise[0]*v, (w, z))
               for w, z in points)


def transport(v, target, coordinate):
    assert 0 < v < 1 and 0 <= target <= 1
    if coordinate <= v:
        return coordinate*target/v
    return target+(coordinate-v)*(1-target)/(1-v)


def main():
    # Hessian on (v,w) is [[-1/2,-1],[-1,2]]. Its 3I complement
    # has positive leading entry 7/2 and determinant 5/2.
    assert Q(7, 2) > 0 and Q(7, 2)*1-1 == Q(5, 2)
    sigma, atoms = Q(2), tuple(Q(k, 2) for k in range(-4, 5))
    M, N, H = len(atoms), 2, Q(3)
    eta = N*H/4
    central_checks = near_tuples = interval_checks = 0
    expectation_checks = 0
    endpoint_jump = recourse(Q(0), (Q(0),)*3)[0]
    interior_limit_constant = Q(1, 3)
    assert endpoint_jump == 0 < interior_limit_constant
    for r in (2, 4, 8):
        h = Q(1, r)
        count_sum = 0
        for noise in product(atoms, repeat=3):
            optimum, point = global_minimum(noise)
            assert feasible(*point)
            count = 0
            for i in range(r+1):
                v = i*h
                value, (w, z) = recourse(v, noise)
                assert feasible(v, w, z)
                assert value+noise[0]*v >= optimum
                is_near = value+noise[0]*v <= optimum+eta*h*h
                count += is_near
                near_tuples += is_near
                if i in (0, r):
                    continue
                plus_v, minus_v = v+h, v-h
                plus_w = transport(v, plus_v, w)
                minus_w = transport(v, minus_v, w)
                assert transport(v, plus_v, z) == z
                assert transport(v, minus_v, z) == z
                assert feasible(plus_v, plus_w, z)
                assert feasible(minus_v, minus_w, z)
                plus_support = objective(plus_v, plus_w, z, noise)-noise[0]*plus_v
                minus_support = objective(minus_v, minus_w, z, noise)-noise[0]*minus_v
                plus_value = recourse(plus_v, noise)[0]
                minus_value = recourse(minus_v, noise)[0]
                assert plus_support >= plus_value
                assert minus_support >= minus_value
                assert plus_support+minus_support-2*value <= N*H*h*h
                assert plus_value+minus_value-2*value <= N*H*h*h
                central_checks += 1
                if is_near:
                    # Both original feasible comparison points have value >=f*.
                    lo = (value-plus_value-eta*h*h)/h
                    hi = (minus_value-value+eta*h*h)/h
                    assert lo <= noise[0] <= hi
                    assert hi-lo <= (N*H+2*eta)*h
                    interval_checks += 1
            count_sum += count
        expected_count = Q(count_sum, M**3)
        A_h = (N*H+2*eta)/(2*sigma)+1/(M*h)
        # For one continuous coordinate: two vertices and one open edge.
        assert expected_count <= 2+A_h
        assert M*h >= 1
        assert expected_count <= 2*(2+Q(3)*N*H/(4*sigma))
        expectation_checks += 1
    # Feasible rounding fixes binary coordinates even when all continuous
    # coordinates use the same threshold and lie on equality boundaries.
    rounding_checks = 0
    for v, w, z in product((Q(i, 8) for i in range(9)),
                           (Q(i, 8) for i in range(9)), (Q(0), Q(1))):
        if not feasible(v, w, z):
            continue
        for h in (Q(1), Q(1, 2), Q(1, 4)):
            cuts = {Q(0), Q(1)}
            for x in (v, w, z):
                scaled = x/h
                cuts.add(scaled-scaled.numerator//scaled.denominator)
            cuts = sorted(cuts)
            mean = [Q(0), Q(0), Q(0)]
            for left, right in zip(cuts, cuts[1:]):
                threshold = (left+right)/2
                rounded = []
                for x in (v, w, z):
                    scaled = x/h
                    lower = scaled.numerator//scaled.denominator
                    rounded.append(h*(lower+(threshold < scaled-lower)))
                assert feasible(*rounded) and rounded[2] == z
                for j in range(3):
                    mean[j] += (right-left)*rounded[j]
            assert mean == [v, w, z]
            rounding_checks += 1
    print(f"PASS: {M**3 * 3} exact sampled triangle minima; "
          f"{central_checks} transported central differences; "
          f"{interval_checks} near-optimal interval tests; "
          f"{near_tuples} near-optimal tuples; "
          f"{expectation_checks} complete-law count bounds; "
          f"{rounding_checks} common-threshold checks; one endpoint jump")


if __name__ == "__main__":
    main()
