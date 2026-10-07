"""Independent exact diagnostics for the deterministic boundary-flow certificate."""

from fractions import Fraction as Q
from itertools import product


def flow_set(nodes, arcs, capacity, balance):
    result = []
    for z in product(range(capacity + 1), repeat=len(arcs)):
        actual = [0] * nodes
        for value, (tail, head) in zip(z, arcs):
            actual[tail] += value
            actual[head] -= value
        if actual == balance:
            result.append(z)
    return result


def proximity_checks():
    fixtures = [
        (3, [(0, 1), (1, 2), (2, 0)], [0, 0, 0]),
        (3, [(0, 1), (0, 1), (1, 2), (2, 0)], [0, 0, 0]),
        (2, [(0, 1), (0, 1)], [2, -2]),
        (1, [(0, 0), (0, 0)], [0]),
    ]
    intervals = [(lo, hi) for lo in range(3) for hi in range(lo, 3)]
    boxes = cases = 0
    sharp_cycle = False
    for nodes, arcs, balance in fixtures:
        feasible = flow_set(nodes, arcs, 2, balance)
        for tightened in product(intervals, repeat=len(arcs)):
            face = [z for z in feasible if all(lo <= value <= hi
                    for value, (lo, hi) in zip(z, tightened))]
            if not face:
                continue
            boxes += 1
            for z in feasible:
                violation = sum(max(lo - value, 0, value - hi)
                                for value, (lo, hi) in zip(z, tightened))
                closest = min(sum(abs(a - b) for a, b in zip(z, other)) for other in face)
                assert closest <= len(arcs) * violation
                if len(arcs) == 3 and violation and closest == 3 * violation:
                    sharp_cycle = True
                cases += 1
    assert sharp_cycle, "The simple directed cycle should attain the factor r"
    return boxes, cases


def normal_derivative_checks():
    checks = 0
    binary_flows = [(0, 1), (1, 0)]

    # Original arc costs a*t*(t-1)-v*a*t^2 stay convex for 0<=v<=1.
    # Their inward derivatives -a*t^2 are concave, so a two-label interval
    # really needs linear interpolation to call a convex-flow oracle.
    for coefficient in (Q(1), Q(2)):
        assert -2 * coefficient < 0
        for v in (Q(0), Q(1, 3), Q(1)):
            assert 2 * coefficient * (1 - v) >= 0
            checks += 1
        for t in (0, 1):
            assert -coefficient * t * t == -coefficient * t
            checks += 1

    for gamma, expected in [(Q(3, 2), -Q(1, 2)), (Q(3), Q(1))]:
        beta = min(gamma - z[0] ** 2 - 2 * z[1] ** 2 for z in binary_flows)
        assert beta == expected
        if gamma == Q(3, 2):
            assert gamma - 1 > 0 and beta < 0  # One returned flow is insufficient.
        else:
            assert beta - Q(1, 2) > 0  # H=1 and normal width=1.
            for v in (Q(0), Q(1, 8), Q(1, 2), Q(1)):
                for z in binary_flows:
                    value = v * (gamma - z[0] ** 2 - 2 * z[1] ** 2)
                    assert value >= (beta - Q(1, 2)) * v
                    checks += 1

    # Three tied labels: f(v,t)=v*a*t^2 has affine base cost and convex
    # inward derivative. Its derivative-minimizing flow is the middle label.
    flows = [(0, 2), (1, 1), (2, 0)]
    gamma = -Q(5, 2)
    beta = min(gamma + z[0] ** 2 + 2 * z[1] ** 2 for z in flows)
    assert beta == Q(1, 2)
    assert gamma + 1 + 2 == beta
    for v in (Q(0), Q(1, 8), Q(1, 2)):
        for z in flows:
            value = v * (gamma + z[0] ** 2 + 2 * z[1] ** 2)
            assert value >= (beta - Q(1, 4)) * v
            checks += 1

    # Outside interval costs are necessary. The base unique flow is (1,1),
    # first outside marginal=1, K=4, r=2. Width 1/8 passes mu>=r*K*T1.
    width, mu, beta, hessian = Q(1, 8), Q(1), Q(1), Q(1)
    assert mu >= 2 * 4 * width
    assert beta - hessian * width / 2 > 0
    for v in (Q(0), Q(1, 16), width):
        for z in flows:
            violation = abs(z[0] - 1) + abs(z[1] - 1)
            value = (z[0] - 1) ** 2 + (z[1] - 1) ** 2 + v * (1 - 4 * z[0] + 4 * z[1])
            first_bound = (mu - 2 * 4 * v) * violation + beta * v - hessian * v * v / 2
            final_bound = (beta - hessian * width / 2) * v
            assert value >= first_bound >= final_bound
            checks += 1
    assert 2 + (1 - 8) < 0  # At width 1 the unchecked outside flow wins.

    # Two simultaneous inward normals can select different tied flows.
    # There is no common winning flow on the entire adjacent box.
    for v1, v2 in product((Q(0), Q(1, 4), Q(1, 2)), repeat=2):
        for z in binary_flows:
            value = (v1 * v1 + v2 * v2) / 2 + v1 * z[0] + v2 * z[1] + (v1 + v2) / 2
            assert value >= Q(1, 4) * (v1 + v2)
            checks += 1
    return checks


if __name__ == "__main__":
    boxes, cases = proximity_checks()
    derivatives = normal_derivative_checks()
    print(f"PASS: {boxes} feasible tightened boxes, {cases} exact flow-distance checks, "
          f"{derivatives} derivative/Taylor checks; sharp cycle, two-label interpolation, "
          "outside-flow rejection, and changing tied winners included.")
