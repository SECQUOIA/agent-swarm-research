"""Targeted exact checks for the shifted secular-map construction.

These finite examples check discriminants and resultant normalization.
They do not prove the general monodromy or Hilbert irreducibility claims.
"""

import sympy as sp


lam, radius, value = sp.symbols("lam radius value")


def check_block(dimension):
    poles = list(range(1, dimension + 1))
    residues = list(range(1, dimension + 1))
    denominator = sp.prod(lam + pole for pole in poles)
    numerator = sum(
        residue**2
        * sp.prod((lam + other) ** 2 for other in poles if other != pole)
        for residue, pole in zip(residues, poles)
    )
    critical = sum(
        residue**2
        * sp.prod((lam + other) ** 3 for other in poles if other != pole)
        for residue, pole in zip(residues, poles)
    )
    first_powers = sum(
        residue**2 * sp.prod(lam + other for other in poles if other != pole)
        for residue, pole in zip(residues, poles)
    )
    rational_map = numerator / denominator**2
    assert sp.cancel(sp.diff(rational_map, lam) + 2 * critical / denominator**3) == 0

    if dimension > 1:
        branch = sp.Poly(
            sp.resultant(critical, numerator - radius * denominator**2, lam),
            radius,
        )
        assert branch.degree() == 3 * dimension - 3
        assert branch.eval(0) != 0
        assert sp.discriminant(branch.as_expr(), radius) != 0
        assert sp.discriminant(critical, lam) != 0

    secular = radius * denominator**2 - numerator
    raw_value = sp.Poly(
        sp.resultant(
            secular, (value + lam * radius) * denominator + first_powers, lam
        ),
        value,
    )
    constant = sp.resultant(secular, denominator, lam)
    assert constant != 0 and not constant.has(radius)
    assert raw_value.degree() == 2 * dimension
    assert raw_value.LC() == radius * constant
    assert raw_value.as_expr().subs(radius, 0) == 0
    normalized = sp.Poly(sp.cancel(raw_value.as_expr() / radius), radius, value)
    assert normalized.domain == sp.ZZ
    assert sp.Poly(normalized.as_expr(), value).LC() == constant

    beta = -first_powers / denominator - lam * rational_map
    assert sp.cancel(sp.diff(beta, lam) + lam * sp.diff(rational_map, lam)) == 0
    return dimension


if __name__ == "__main__":
    checked = [check_block(dimension) for dimension in (1, 2, 3, 4)]
    print(f"PASS: exact branch, derivative, and value-resultant checks for r={checked}")
