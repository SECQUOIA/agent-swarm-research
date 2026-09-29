"""Independent local first-jet check using symbolic substitution and division."""

import sympy as sp


def main():
    x, y, z, t, b = sp.symbols("x y z t b")
    groups = [
        (1, y * z, x**2 * z, x * y**2),
        (x, z**2, x * y * z, y**3),
        (y, x**2, x * z**2, y**2 * z),
        (z, x * y, x**3, y * z**2),
        (x * z, y**2, x**2 * y, z**3),
    ]
    monomials = {
        x**i * y**j * z**ell
        for i in range(4)
        for j in range(4 - i)
        for ell in range(4 - i - j)
    }
    assert len(monomials) == 20
    assert {sp.sympify(monomial) for group in groups for monomial in group} == monomials
    expected_blocks = [
        sp.Matrix([[1, b, b, b], [0, 0, 2, 1], [0, 1, 0, 2], [0, 1, 1, 0]]),
        sp.Matrix([[1, b, b, b], [1, 0, b, 0], [0, 0, 1, 3], [0, 2, 1, 0]]),
        sp.Matrix([[1, 1, b, b], [0, 2, b, 0], [1, 0, 0, 2 * b], [0, 0, 2, 1]]),
        sp.Matrix([[1, 1, 1, b], [0, 1, 3, 0], [0, 1, 0, b], [1, 0, 0, 2 * b]]),
        sp.Matrix([[1, 1, 1, b], [1, 0, 2, 0], [0, 2, 1, 0], [1, 0, 0, 3 * b]]),
    ]
    expected_determinants = [5, 5 * b, -5 * b, -5 * b, -5 * b]
    determinants = []
    for residue, group in enumerate(groups):
        powers = [residue, (residue - 1) % 5, (residue - 2) % 5, (residue - 3) % 5]
        block = sp.zeros(4)
        for column, monomial in enumerate(group):
            polynomial = sp.sympify(monomial)
            jet = [polynomial, *(sp.diff(polynomial, variable) for variable in (x, y, z))]
            for row, component in enumerate(jet):
                substituted = component.subs({x: t, y: t**2, z: t**3})
                reduced = sp.rem(substituted, t**5 - b, t).expand()
                coefficient = reduced.coeff(t, powers[row])
                assert reduced == coefficient * t ** powers[row]
                block[row, column] = coefficient
        assert block == expected_blocks[residue]
        determinant = sp.factor(block.det())
        assert determinant == expected_determinants[residue]
        determinants.append(determinant)
        print(f"PASS: residue {residue}, determinant {determinant}")

    determinant = sp.factor(sp.prod(determinants))
    assert determinant == -3125 * b**4
    print(f"PASS: grouped full first-jet determinant {determinant}")


if __name__ == "__main__":
    main()
