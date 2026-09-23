"""Exact rational checks of the pooling reduction at fixed compositions.

This enumerates vertices of the original three-flow LP (y1, y2, anchor),
including every input/output quality inequality. It does not assume either
output is full or that distinguished quality is attained at its upper bound.
It also checks compositions outside the encoded polytope and shifted qualities.
"""

from fractions import Fraction as Q
from itertools import combinations


def solve_three(rows, rhs):
    matrix = [list(row) + [bound] for row, bound in zip(rows, rhs)]
    for column in range(3):
        pivot = next((i for i in range(column, 3) if matrix[i][column]), None)
        if pivot is None:
            return None
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [v / scale for v in matrix[column]]
        for i in range(3):
            if i != column:
                scale = matrix[i][column]
                matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[column])]
    return tuple(matrix[i][3] for i in range(3))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def flow_lp(t, a_coeff, b_coeff, lower, upper, shifted=False, omit_row_output_one=False):
    a0, a1 = a_coeff
    b0, b1 = b_coeff
    z = (1 - t, t)
    b = dot(z, b_coeff)
    # Input qualities c0,c1,anchor; output upper bounds u1,u2.
    qualities = [
        (a0, a1, Q(0), Q(1), max(Q(0), a0, a1)),
        (Q(0), Q(1), upper, upper, upper),
        (Q(0), Q(-1), -lower, -lower, -lower),
    ]
    if shifted:
        qualities = [tuple(v + max(Q(0), -min(row)) + 1 for v in row) for row in qualities]
    rows = [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1)]
    rhs = [0, 0, 0, 1, 1, 1, 2, 1]
    for zi in z:
        rows.append((zi, zi, 0))
        rhs.append(2)
    for index, (c0, c1, anchor, u1, u2) in enumerate(qualities):
        pool_quality = c0 * z[0] + c1 * z[1]
        if index == 0 or not omit_row_output_one:
            rows.append((pool_quality - u1, 0, anchor - u1))
            rhs.append(0)
        rows.append((0, pool_quality - u2, 0))
        rhs.append(0)
    rows = [tuple(map(Q, row)) for row in rows]
    rhs = list(map(Q, rhs))
    best = Q(0)
    for basis in combinations(range(len(rows)), 3):
        flow = solve_three([rows[i] for i in basis], [rhs[i] for i in basis])
        if flow is not None and all(dot(row, flow) <= bound for row, bound in zip(rows, rhs)):
            best = max(best, b * (flow[0] + flow[1]))
    return best


def main():
    # Both fixtures have negative individual coefficients, but a>=1,b>=0
    # throughout the encoded interval. Their endpoints include a=1 or b=0.
    fixtures = [
        ((Q(-1), Q(7)), (Q(5), Q(-3)), Q(1, 4), Q(1, 2)),
        ((Q(5), Q(-3)), (Q(-2), Q(6)), Q(1, 4), Q(1, 2)),
        ((Q(1), Q(3)), (Q(0), Q(0)), Q(0), Q(1)),
    ]
    checks = invalid = 0
    for a_coeff, b_coeff, lower, upper in fixtures:
        for t in [Q(i, 12) for i in range(13)]:
            z = (1 - t, t)
            a, b = dot(z, a_coeff), dot(z, b_coeff)
            valid = lower <= t <= upper
            expected = b * (1 + 1 / a) if valid else Q(0)
            if valid:
                assert a >= 1 and b >= 0
            else:
                invalid += 1
            for shifted in [False, True]:
                obtained = flow_lp(t, a_coeff, b_coeff, lower, upper, shifted)
                assert obtained == expected, (a_coeff, b_coeff, t, shifted, obtained, expected)
                checks += 1
    # Exact symbolic scalar identity, with a=U-1 and b=K-V, at signed
    # coefficient mixtures and at source-threshold equality.
    threshold_checks = 0
    for u in [Q(2), Q(5, 2), Q(7)]:
        for k in [Q(1, 3), Q(2), Q(11)]:
            for v in [k / (2 * u), k / u, 2 * k / u, k]:
                assert ((k - v) * (1 + 1 / (u - 1)) >= k) == (u * v <= k)
                threshold_checks += 1
    a_coeff, b_coeff, lower, upper = fixtures[0]
    broken = flow_lp(Q(0), a_coeff, b_coeff, lower, upper, omit_row_output_one=True)
    assert broken == 5
    print(f"PASS: {checks} exact original-flow LP checks, including {invalid} excluded compositions in both shifted and unshifted form.")
    print(f"PASS: {threshold_checks} rational threshold-equivalence checks, including equality.")
    print("Includes negative individual a/b coefficients, a=1, b=0, inactive mixing pool, and strictly positive shifted quality data.")
    print("Negative control: removing output-1 polytope rows permits profit 5 at an excluded composition; correct profit is 0.")


if __name__ == "__main__":
    main()
