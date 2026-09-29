"""Exact targeted checks for one-edge-obstructions.md; standard library only."""

from fractions import Fraction as F
from pathlib import Path
from runpy import run_path


def main():
    old_checker = Path(__file__).parents[2] / "research-20260927/check_stieltjes_majorants.py"
    helpers = run_path(str(old_checker))
    solve = helpers["solve"]
    optimum = helpers["optimum"]
    majorant = helpers["majorant"]
    q = [[F(v) for v in row] for row in
         ((2, 1, -1, 0), (1, 2, 0, -1),
          (-1, 0, 2, 0), (0, -1, 0, 2))]
    b = [F(3), F(3), F(0), F(0)]
    c = [F(0), F(0), F(3, 5), F(3, 5)]
    for eta, full_value, center_value in (
        (F(0), F(-36, 5), F(-6)),
        (F(1, 10), F(-342, 47), F(-1428, 235)),
    ):
        q[2][3] = q[3][2] = -eta
        values = []
        for optional, expected in (
            ((), F(-6)), ((2,), F(-27, 4)),
            ((3,), F(-27, 4)), ((2, 3), full_value),
        ):
            support = (0, 1) + optional
            xs = solve([[q[i][j] for j in support] for i in support],
                       [b[i] for i in support])
            assert all(0 <= xi <= 2 for xi in xs)
            value = -sum((b[i] * xi for i, xi in zip(support, xs)), F(0))
            assert value == expected, (eta, optional, value, expected)
            values.append(value)
        assert values[1] + values[2] < values[0] + values[3]
        value, x, _ = optimum(q, b, c)
        assert value == F(-123, 20)
        assert all(0 <= xi <= 2 for xi in x)
        for ratio, expected in ((F(1, 2), F(-123, 20)), (F(1), center_value),
                                (F(2), F(-123, 20))):
            qr = majorant(q, [(0, 1)], [ratio])
            value, x, _ = optimum(qr, b, c)
            assert value == expected, (eta, ratio, value, expected)
            assert all(0 <= xi <= 2 for xi in x)
    bound = -9 / (2 - 2 / (4 - F(1, 10) ** 2))
    assert bound == F(-3591, 598)
    assert bound > F(-1428, 235) > F(-123, 20)
    print("PASS: two instances, eight conditional values, two full optima, six ratio optima, and an endpoint-inactive bound (exact rationals).")


if __name__ == "__main__":
    main()
