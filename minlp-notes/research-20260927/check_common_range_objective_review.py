"""Exact illustrations for the common-range objective projection review.

These calculations check the singular KKT identity and two examples. They
do not certify the radius theorem, bit bounds, or the full FPT algorithm.
"""

import random

import sympy as sp


def main():
    u, v = sp.symbols("u v", real=True)
    # min v^2 subject to v >= u^2 has value u^4. A quadratic chart would
    # therefore be insufficient for this active-set elimination.
    assert sp.expand((v**2).subs(v, u**2)) == u**4
    assert sp.expand(2 * v - 2 * u**2).subs(v, u**2) == 0

    # A particular solution to a singular stationarity system need not
    # satisfy the fiber inequalities: v_2 >= 1, objective v_1^2.
    Q = sp.diag(2, 0)
    assert Q * sp.Matrix([0, 0]) == sp.zeros(2, 1)
    assert Q * sp.Matrix([0, 1]) == sp.zeros(2, 1)
    assert sp.Matrix([0, -1]).dot(sp.Matrix([0, 0])) > -1
    assert sp.Matrix([0, -1]).dot(sp.Matrix([0, 1])) <= -1

    rng = random.Random(281)
    cases = 0
    null_vectors = 0
    for n in range(1, 7):
        for m in range(n + 2):
            for rank in range(n + 1):
                A = sp.Matrix(rank, n, lambda i, j: rng.randrange(-2, 3))
                Q = A.T * A
                C = sp.Matrix(m, n, lambda i, j: rng.randrange(-2, 3))
                K = Q.row_join(C.T).col_join(
                    C.row_join(sp.zeros(m, m))
                )
                base_v = sp.Matrix(n, 1, lambda i, j: rng.randrange(-3, 4))
                base_lam = sp.Matrix(m, 1, lambda i, j: rng.randrange(-3, 4))
                linear = -Q * base_v - C.T * base_lam
                for delta in K.nullspace():
                    dv = delta[:n, 0]
                    assert C * dv == sp.zeros(m, 1)
                    assert Q * dv == sp.zeros(n, 1)
                    shifted_v = base_v + dv
                    base_value = (base_v.T * Q * base_v)[0] / 2 + linear.dot(base_v)
                    shifted_value = (shifted_v.T * Q * shifted_v)[0] / 2 + linear.dot(shifted_v)
                    assert sp.expand(shifted_value - base_value) == 0
                    null_vectors += 1
                cases += 1
    print(f"Passed 2 examples and {cases} exact KKT systems ({null_vectors} null vectors).")


if __name__ == "__main__":
    main()
