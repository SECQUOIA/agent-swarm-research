"""Exact examples for the quadratic-fractional value proof.

These symbolic identities test specific boundaries and singular charts.
They do not establish the general complexity or quantifier-elimination claims.
"""

import sympy as sp


def main():
    u, z, s = sp.symbols("u z s", real=True)

    # A falling numerator alone does not imply a ratio tending to -infinity.
    ratio = -s / (s + 1)
    assert sp.cancel(ratio + 1) == 1 / (s + 1)
    assert sp.limit(ratio, s, sp.oo) == -1

    # The full continuous column detects the cross term missed by the xx block.
    native_hessian = sp.hessian(4 - 4 * z * s, (z, s))
    assert native_hessian[1, 1] == 0
    assert native_hessian[:, 1].rank() == 1

    # For a joint PSD matrix, every vv-kernel vector kills the cross block.
    factor = sp.Matrix([[1, 2, 0, 1, 0, 1], [0, 1, 1, 0, 1, 2]])
    full_q = factor.T * factor
    qvv = full_q[2:, 2:]
    qav = full_q[:2, 2:]
    assert len(qvv.nullspace()) == 2
    for direction in qvv.nullspace():
        assert qav * direction == sp.zeros(2, 1)

    # A singular KKT chart must retain a zero-multiplier active constraint.
    # Minimize v1^2+(v2-z)^2 with v1>=u^2 and v3>=1; v4 is free.
    q = sp.diag(2, 2, 0, 0)
    c = sp.Matrix([[-1, 0, 0, 0], [0, 0, -1, 0]])
    rhs = sp.Matrix([-u**2, -1])
    linear = sp.Matrix([0, -2 * z, 0, 0])
    kkt = q.row_join(c.T).col_join(c.row_join(sp.zeros(2)))
    chart = kkt.pinv() * (-linear).col_join(rhs)
    assert chart == sp.Matrix([u**2, z, 1, 0, 2 * u**2, 0])
    assert kkt.det() == 0
    assert c * chart[:4, :] == rhs
    value = sp.expand(chart[0] ** 2 + (chart[1] - z) ** 2)
    assert value == u**4
    assert sp.Poly(value, z, u).total_degree() == 4

    # The rational pseudoinverse formula used in the manuscript is exact.
    kernel = sp.Matrix.hstack(*kkt.nullspace())
    invertible = kkt + kernel * kernel.T
    assert invertible.inv() * kkt * invertible.inv() == kkt.pinv()

    # An inconsistent empty-active-set chart can still be a valid witness.
    # For min v over v>=-1, it returns v=0; the active chart returns v=-1.
    empty_chart = (sp.zeros(1).pinv() * sp.Matrix([-1]))[0]
    active_kkt = sp.Matrix([[0, -1], [-1, 0]])
    active_chart = (active_kkt.inv() * sp.Matrix([-1, 1]))[0]
    assert empty_chart == 0 and active_chart == -1
    assert -empty_chart <= 1 and -active_chart <= 1
    assert empty_chart > -sp.Rational(1, 2) >= active_chart

    # Arbitrary PSD numerator rank does not prevent a low-degree finite value.
    # On s>=0, (s^2+1+sum(v_i^2))/(s+1) has the displayed global minimum.
    theta = 2 * sp.sqrt(2) - 2
    optimizer = sp.sqrt(2) - 1
    extra = sp.symbols("v1:9", real=True)
    numerator = s**2 + 1 + sum(v**2 for v in extra)
    certificate = (s - optimizer) ** 2 + sum(v**2 for v in extra)
    assert sp.expand(numerator - theta * (s + 1) - certificate) == 0
    assert sp.expand(theta**2 + 4 * theta - 4) == 0
    assert sp.hessian(numerator, (s,) + extra).rank() == 9

    print("PASS: denominator retention, cross-aware kernel, PSD cross annihilation,")
    print("singular and inconsistent charts, quartic degree, and irrational ratio value")


if __name__ == "__main__":
    main()
