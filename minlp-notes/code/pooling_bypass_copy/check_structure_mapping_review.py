"""Independent exact symbolic check of the structural pooling mapping.

This checks ownership and residual identities, not quantifier elimination.
Run with the project's minlp-notes Python environment (SymPy required).
"""

import sympy as sp


def check_case(covered_inputs, covered_outputs, rank):
    inputs = range(3)
    outputs = range(3)
    pools = range(2)
    attributes = range(4)
    ai, bj = set(covered_inputs), set(covered_outputs)
    # Vertices 1 form an internal component; vertex 2 is isolated unless covered.
    edges = {
        (i, j) for i in inputs for j in outputs
        if i in ai or j in bj or (i == 1 and j == 1)
    }
    remaining = {("i", i) for i in inputs if i not in ai}
    remaining |= {("j", j) for j in outputs if j not in bj}
    components = []
    while remaining:
        frontier = [remaining.pop()]
        comp = set(frontier)
        while frontier:
            side, node = frontier.pop()
            neighbors = ({("j", j) for i, j in edges if i == node}
                         if side == "i" else
                         {("i", i) for i, j in edges if j == node})
            found = neighbors & remaining
            remaining -= found
            comp |= found
            frontier.extend(found)
        components.append(comp)

    # Omit two pool arcs to exercise missing-arc conventions.
    y = {(i, ell): sp.Symbol(f"y{i}_{ell}") for i in inputs for ell in pools
         if (i, ell) != (2, 1)}
    v = {(ell, j): sp.Symbol(f"v{ell}_{j}") for ell in pools for j in outputs
         if (ell, j) != (1, 2)}
    z = {(i, j): sp.Symbol(f"z{i}_{j}") for i, j in edges}
    q = {(ell, s): sp.Symbol(f"q{ell}_{s}") for ell in pools for s in range(rank)}
    coordinates = {(i, s): sp.Rational((i + 1) ** (s + 1) - 3, s + 2)
                   for i in inputs for s in range(rank)}
    basis = {(s, a): sp.Rational((a + 1) ** (s + 1), a + s + 2)
             for s in range(rank) for a in attributes}
    origin = {a: sp.Rational(a - 2, a + 1) for a in attributes}
    quality = {(i, a): origin[a] + sum(coordinates[i, s] * basis[s, a]
                                     for s in range(rank))
               for i in inputs for a in attributes}
    poolquality = {(ell, a): origin[a] + sum(q[ell, s] * basis[s, a]
                                            for s in range(rank))
                   for ell in pools for a in attributes}

    core = {value for (i, _), value in y.items() if i in ai}
    core |= {value for (_, j), value in v.items() if j in bj}
    core |= {value for (i, j), value in z.items() if i in ai and j in bj}
    blocks = []
    for comp in components:
        ii = {i for side, i in comp if side == "i"}
        jj = {j for side, j in comp if side == "j"}
        block = {value for (i, _), value in y.items() if i in ii}
        block |= {value for (_, j), value in v.items() if j in jj}
        block |= {value for (i, j), value in z.items()
                  if (i in ii and j in jj) or (i in ai and j in jj)
                  or (i in ii and j in bj)}
        blocks.append(block)
        for i in ii:
            assert {f for (u, _), f in y.items() if u == i} <= block
            assert {f for (u, _), f in z.items() if u == i} <= block
        for j in jj:
            assert {f for (_, w), f in v.items() if w == j} <= block
            assert {f for (_, w), f in z.items() if w == j} <= block
    owners = [core] + blocks
    allflows = set(y.values()) | set(v.values()) | set(z.values())
    assert set().union(*owners) == allflows
    assert sum(map(len, owners)) == len(allflows)

    checks = 1
    for ell in pools:
        mass = sum(y.get((i, ell), 0) for i in inputs) - sum(
            v.get((ell, j), 0) for j in outputs)
        compressed = {
            s: sum(coordinates[i, s] * y.get((i, ell), 0) for i in inputs)
            - q[ell, s] * sum(v.get((ell, j), 0) for j in outputs)
            for s in range(rank)
        }
        for a in attributes:
            physical = sum(quality[i, a] * y.get((i, ell), 0) for i in inputs)
            physical -= poolquality[ell, a] * sum(v.get((ell, j), 0) for j in outputs)
            assert sp.expand(physical - origin[a] * mass - sum(
                basis[s, a] * compressed[s] for s in range(rank))) == 0
            checks += 1
        for s in range(rank):
            left = sum(coordinates[i, s] * y.get((i, ell), 0)
                       for i in inputs if i not in ai)
            left -= q[ell, s] * sum(v.get((ell, j), 0)
                                    for j in outputs if j not in bj)
            right = q[ell, s] * sum(v.get((ell, j), 0) for j in bj)
            right -= sum(coordinates[i, s] * y.get((i, ell), 0) for i in ai)
            assert sp.expand(left - right - compressed[s]) == 0
            checks += 1

    for j in outputs:
        throughput = sum(v.get((ell, j), 0) for ell in pools)
        throughput += sum(z.get((i, j), 0) for i in inputs)
        coordinate_mass = {
            s: sum(q[ell, s] * v.get((ell, j), 0) for ell in pools)
            + sum(coordinates[i, s] * z.get((i, j), 0) for i in inputs)
            for s in range(rank)
        }
        for a in attributes:
            bound = sp.Symbol(f"bound{j}_{a}")
            physical = sum((poolquality[ell, a] - bound) * v.get((ell, j), 0)
                           for ell in pools)
            physical += sum((quality[i, a] - bound) * z.get((i, j), 0)
                            for i in inputs)
            compressed = (origin[a] - bound) * throughput
            compressed += sum(basis[s, a] * coordinate_mass[s] for s in range(rank))
            assert sp.expand(physical - compressed) == 0
            checks += 1
        if j in bj:
            left = sum(z.get((i, j), 0) for i in inputs if i not in ai)
            right = throughput - sum(v.get((ell, j), 0) for ell in pools)
            right -= sum(z.get((i, j), 0) for i in ai)
            assert sp.expand(left - right) == 0
            checks += 1
            for s in range(rank):
                left = sum(coordinates[i, s] * z.get((i, j), 0)
                           for i in inputs if i not in ai)
                right = coordinate_mass[s] - sum(q[ell, s] * v.get((ell, j), 0)
                                                 for ell in pools)
                right -= sum(coordinates[i, s] * z.get((i, j), 0) for i in ai)
                assert sp.expand(left - right) == 0
                checks += 1
    return checks


if __name__ == "__main__":
    partitions = [({0}, {0}), ({0}, set()), (set(), {0}),
                  (set(), set()), ({0, 1, 2}, {0, 1, 2})]
    count = sum(check_case(ai, bj, rank) for ai, bj in partitions for rank in (0, 1, 2))
    print(f"PASS: 15 symbolic mappings; {count} exact ownership and residual checks")
