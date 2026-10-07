"""Core-only finite-noise flow-chart closure with persistent integer ties.

A chain has m stages, each with two unit-capacity arcs. Only the first
stage has costs (v-1/4)^2 and (v-3/4)^2; later arcs cost zero.
The core term is 2(v-1/2)^2-sigma*v, with noise gamma*v.
There are 2^m feasible flows and 2^(m-1) tied conditional optimizers.
All calculations are rational; no feasible-flow enumeration is used.
"""

from collections import deque
from fractions import Fraction as Q


ZERO = (Q(0), Q(0), Q(0))
SIGMA = Q(1, 4)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def evaluate(p, v):
    return p[0]+p[1]*v+p[2]*v*v


def minimum(p, lo, hi):
    candidates = [lo, hi]
    if p[2] > 0:
        critical = -p[1]/(2*p[2])
        if lo <= critical <= hi:
            candidates.append(critical)
    return min((evaluate(p, v), v) for v in candidates)


def arc_polynomial(stage, choice):
    if stage:
        return ZERO
    anchor = Q(1, 4) if choice == 0 else Q(3, 4)
    return (anchor*anchor, -2*anchor, Q(1))


def core_polynomial(gamma):
    return (Q(1, 2), -2-SIGMA+gamma, Q(2))


def solve_flow(v, stages, gamma):
    choice = min(range(2), key=lambda j: (evaluate(arc_polynomial(0, j), v), j))
    labels = [choice]+[0]*(stages-1)
    p = add(core_polynomial(gamma), arc_polynomial(0, choice))
    return evaluate(p, v), labels


def chart(v, labels):
    stages = len(labels)
    root = stages+1
    node_count = stages+2
    arcs = []
    for stage, selected in enumerate(labels):
        for choice in range(2):
            cost = arc_polynomial(stage, choice)
            if choice == selected:
                arcs.append((stage+1, stage, neg(cost)))
            else:
                arcs.append((stage, stage+1, cost))
    arcs += [(root, node, ZERO) for node in range(stages+1)]
    distances = [None]*node_count
    distances[root] = Q(0)
    for _ in range(node_count-1):
        changed = False
        for tail, head, cost in arcs:
            if distances[tail] is None:
                continue
            candidate = distances[tail]+evaluate(cost, v)
            if distances[head] is None or candidate < distances[head]:
                distances[head] = candidate
                changed = True
        if not changed:
            break
    assert all(value is not None for value in distances)
    assert all(distances[head] <= distances[tail]+evaluate(cost, v)
               for tail, head, cost in arcs)
    # An actual arborescence of the tight graph, not possibly cyclic
    # independently chosen shortest-path predecessors.
    tight = [[] for _ in range(node_count)]
    for tail, head, cost in arcs:
        if distances[head] == distances[tail]+evaluate(cost, v):
            tight[tail].append((head, cost))
    potentials = [None]*node_count
    potentials[root] = ZERO
    queue = deque([root])
    while queue:
        tail = queue.popleft()
        for head, cost in tight[tail]:
            if potentials[head] is None:
                potentials[head] = add(potentials[tail], cost)
                queue.append(head)
    assert all(p is not None for p in potentials)
    assert all(evaluate(p, v) == distance
               for p, distance in zip(potentials, distances))
    reduced = [add(cost, add(potentials[tail], neg(potentials[head])))
               for tail, head, cost in arcs]
    assert all(evaluate(p, v) >= 0 for p in reduced)
    return reduced


def true_optimum(gamma):
    return min(minimum(add(core_polynomial(gamma), arc_polynomial(0, j)), Q(0), Q(1))
               for j in range(2))


def run(stages, gamma, cutoff=14):
    # The core face derivatives stay inward by at least two for every noise.
    for choice in range(2):
        p = add(core_polynomial(gamma), arc_polynomial(0, choice))
        assert p[1] <= -2 and p[1]+2*p[2] >= 2
        assert 2*p[2] == 6
    true_value, _ = true_optimum(gamma)
    cells = [(Q(0), Q(1))]
    calls = signs = identities = max_retained = 0
    for level in range(cutoff+1):
        h, error = Q(1, 2**level), Q(3, 4**level)/4
        corners = sorted({v for cell in cells for v in cell})
        values = {v: solve_flow(v, stages, gamma) for v in corners}
        calls += len(values)
        c = min(corners, key=lambda v: (values[v][0], v))
        upper, labels = values[c]
        assert true_value <= upper <= true_value+error
        kept = [cell for cell in cells
                if min(values[cell[0]][0], values[cell[1]][0])-error <= upper]
        max_retained = max(max_retained, len(kept))
        lo, hi = min(a for a, _ in kept), max(b for _, b in kept)
        reduced = chart(c, labels)
        signs += len(reduced)
        identities += sum(p == ZERO for p in reduced)
        if all(minimum(p, lo, hi)[0] >= 0 for p in reduced):
            returned = minimum(add(core_polynomial(gamma), arc_polynomial(0, labels[0])), Q(0), Q(1))
            assert returned[0] == true_value
            assert gamma < SIGMA
            # Test whole-hull optimality directly using both first-stage costs.
            for competitor in range(2):
                difference = add(arc_polynomial(0, competitor), neg(arc_polynomial(0, labels[0])))
                assert minimum(difference, lo, hi)[0] >= 0
            return level, calls, signs, identities, max_retained, False
        cells = [(a, (a+b)/2) for a, b in kept]+[((a+b)/2, b) for a, b in kept]
    # This grid contains an endpoint atom gamma=sigma with two optimal core
    # points. Exact analytic comparison of the two cost classes checks the
    # fallback value; it does not implement enumeration of all 2^stages flows.
    assert gamma == SIGMA
    left = minimum(add(core_polynomial(gamma), arc_polynomial(0, 0)), Q(0), Q(1))
    right = minimum(add(core_polynomial(gamma), arc_polynomial(0, 1)), Q(0), Q(1))
    assert left[0] == right[0] == true_value and left[1] < Q(1, 2) < right[1]
    return cutoff, calls, signs, identities, max_retained, True


def main():
    M = 8
    atoms = [-SIGMA+2*SIGMA*Q(j, M-1) for j in range(M)]
    for stages in (1, 80):
        results = [run(stages, gamma) for gamma in atoms]
        assert sum(row[-1] for row in results) == 1
        print("PASS:", {"stages": stages, "draws": M,
                        "largest_regular_level": max(row[0] for row in results if not row[-1]),
                        "oracle_queries": sum(row[1] for row in results),
                        "polynomial_sign_checks": sum(row[2] for row in results),
                        "identical_zero_checks": sum(row[3] for row in results),
                        "max_retained": max(row[4] for row in results),
                        "exceptional_endpoint_atoms": sum(row[-1] for row in results)})
    print("No feasible-flow enumeration, general algebraic sign solver, or full cutoff-budget computation was used.")


if __name__ == "__main__":
    main()
