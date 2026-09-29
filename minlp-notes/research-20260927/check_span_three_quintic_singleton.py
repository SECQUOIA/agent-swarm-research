"""Exact verification of a degree-five singleton cut out by three ellipsoids.

No numerical solver is used. Run with Python 3 and SymPy.
"""

import sympy as sp


def main():
    t = sp.Symbol("t")
    minimal_polynomial = sp.Poly(t**5 - 2, t)
    point = sp.Matrix([t, t**2, t**3, t**4])
    matrices = [
        sp.Matrix([
            [2614623632, -522768322, 104803068, -1017153954],
            [-522768322, 3799174020, -1671829550, -126985510],
            [104803068, -1671829550, 2862304974, -382898195],
            [-1017153954, -126985510, -382898195, 1869362838],
        ]),
        sp.Matrix([
            [2265538524, -718575346, 573734926, -809282652],
            [-718575346, 4076479140, -2230110528, -87667068],
            [573734926, -2230110528, 3054800858, -348343533],
            [-809282652, -87667068, -348343533, 2198392654],
        ]),
        sp.Matrix([
            [2, 1, 0, -1],
            [1, 4, -1, -2],
            [0, -1, 2, 1],
            [-1, -2, 1, 3],
        ]),
    ]
    linear = [
        sp.Matrix([-5216667908, -1083030852, -2693189032, -4008780156]),
        sp.Matrix([-5758933444, -872164392, -2959634616, -5223948992]),
        sp.Matrix([4, -6, -8, -4]),
    ]
    constants = [10755934016, 12157572720, 8]
    weights = [
        3 - t + 2*t**2 + t**3 - 3*t**4,
        -3 + t - t**2 + 3*t**4,
        sp.Integer(1319581982),
    ]

    def reduce(value):
        return sp.rem(sp.Poly(sp.expand(value), t), minimal_polynomial).as_expr()

    assert minimal_polynomial.is_irreducible
    for matrix, vector, constant in zip(matrices, linear, constants):
        assert matrix == matrix.T
        assert all(matrix[:j, :j].det() > 0 for j in range(1, 5))
        assert reduce((point.T * matrix * point)[0] + (vector.T * point)[0] + constant) == 0

    gradient = sp.zeros(4, 1)
    for weight, matrix, vector in zip(weights, matrices, linear):
        gradient += weight * (2 * matrix * point + vector)
    assert all(reduce(entry) == 0 for entry in gradient)

    flattened = sp.Matrix([[matrix[i, j] for i in range(4) for j in range(4)] for matrix in matrices])
    assert flattened.rank() == 3

    lower = sp.Rational(1148, 1000)
    upper = sp.Rational(1149, 1000)
    assert lower**5 < 2 < upper**5
    first_lower_bound = 3 - upper + 2*lower**2 + lower**3 - 3*upper**4
    second_lower_bound = -3 + lower - upper**2 + 3*lower**4
    assert first_lower_bound > 0
    assert second_lower_bound > 0
    assert weights[2] > 0

    print("PASS: all three matrices are positive definite; Hessian span is three")
    print("PASS: all three rows vanish at (alpha, alpha^2, alpha^3, alpha^4)")
    print("PASS: positive weighted gradient vanishes exactly modulo alpha^5 - 2")
    print("PASS: alpha^5 - 2 is irreducible; the singleton coordinate field has degree five")


if __name__ == "__main__":
    main()
