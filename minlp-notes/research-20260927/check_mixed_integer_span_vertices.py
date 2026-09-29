"""Check the relaxed tent-chain LP by exact vertex enumeration on small cases.

This challenges the lift projection claim, independently of checking the
interpolation formula. It is finite evidence, not a proof for arbitrary depth.
Requires SymPy. Run directly from the repository root.
"""

from itertools import combinations

import sympy as sp


def check_chain_vertices():
    samples = sorted({sp.Rational(j, p) for p in (5, 7, 11) for j in range(p + 1)})
    tests = 0
    for depth in range(1, 5):
        # Encode A g <= b + c*s, including the first layer's dependence on s.
        rows = []
        for j in range(depth):
            row = [0] * depth
            row[j] = -1
            rows.append((row, 0, 0))
            row = [0] * depth
            row[j] = 1
            if j:
                row[j - 1] = -2
            rows.append((row, 0, 2 if j == 0 else 0))
            row = [0] * depth
            row[j] = 1
            if j:
                row[j - 1] = 2
            rows.append((row, 2, -2 if j == 0 else 0))
        matrix = sp.Matrix([row[0] for row in rows])
        constant = sp.Matrix([row[1] for row in rows])
        slope = sp.Matrix([row[2] for row in rows])
        vertices = []
        for basis in combinations(range(3 * depth), depth):
            basis_matrix = matrix[list(basis), :]
            if basis_matrix.det() == 0:
                continue
            inverse = basis_matrix.inv()
            vertices.append(
                (inverse * constant[list(basis), :], inverse * slope[list(basis), :])
            )
        for value in samples:
            optimum = None
            for intercept, derivative in vertices:
                point = intercept + value * derivative
                if any(v < 0 for v in constant + value * slope - matrix * point):
                    continue
                objective = sum(point[j] / 4 ** (j + 1) for j in range(depth))
                optimum = objective if optimum is None else max(optimum, objective)
            tent_value = value
            expected = 0
            for j in range(1, depth + 1):
                tent_value = min(2 * tent_value, 2 * (1 - tent_value))
                expected += tent_value / 4**j
            assert optimum == expected, (depth, value, optimum, expected)
            tests += 1
        print(
            f"PASS depth {depth}: {len(samples)} rational inputs, "
            f"all {len(vertices)} invertible vertex bases"
        )
    print(f"PASS relaxed chain LP objective equals tent formula on {tests} exact instances")


if __name__ == "__main__":
    check_chain_vertices()
