"""Exact finite checks for the singular quadratic precision example."""

import sympy as sp


for k in range(1, 7):
    x = sp.Symbol("x")
    ys = sp.symbols(f"y1:{k + 1}")
    variables = ys + (x,)
    equations = (
        [ys[0] - x**2]
        + [ys[i] - ys[i - 1] ** 2 for i in range(1, k)]
        + [x * ys[-1]]
    )
    curve = {ys[i]: x ** (2 ** (i + 1)) for i in range(k)}
    assert all(sp.expand(f.subs(curve)) == 0 for f in equations[:-1])
    assert sp.expand(equations[-1].subs(curve)) == x ** (2**k + 1)
    jacobian = sp.Matrix(equations).jacobian(variables)
    assert jacobian.subs({v: 0 for v in variables}).rank() == k
    determinant = sp.factor(jacobian.det().subs(curve))
    assert sp.expand(determinant - (2**k + 1) * x ** (2**k)) == 0
    print(f"k={k}: elimination, rank, and determinant PASS")
