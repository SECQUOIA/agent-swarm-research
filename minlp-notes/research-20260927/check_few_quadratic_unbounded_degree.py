"""Exact, targeted checks for the three-ellipsoid companion construction."""

import sympy as sp


def positive_definite(matrix):
    """Certify positive definiteness by exact rational Schur pivots."""
    work = matrix.copy()
    for j in range(work.rows):
        pivot = work[j, j]
        assert pivot > 0, (j, pivot)
        for k in range(j + 1, work.rows):
            for ell in range(j + 1, work.rows):
                work[k, ell] -= work[k, j] * work[j, ell] / pivot


def root_interval(radicand, degree, denominator):
    numerator, exact = sp.integer_nthroot(radicand * denominator**degree, degree)
    assert not exact
    lo = sp.Rational(numerator, denominator)
    hi = lo + sp.Rational(1, denominator)
    assert lo**degree < radicand < hi**degree
    return lo, hi


def quadratic_remainder(matrix, degree, radicand):
    result = [sp.S.Zero] * degree
    for j in range(degree):
        for k in range(degree):
            result[(j + k) % degree] += matrix[j, k] * radicand ** ((j + k) // degree)
    return result


def check_block(degree, radicand):
    assert degree >= 3 and degree % 2 == 1
    side = sp.Rational(1, 100 * radicand**5 * degree**2)
    denominator = 1
    while sp.Rational(1, denominator) > side / (32 * radicand * degree**2):
        denominator *= 2
    alpha_lo, alpha_hi = root_interval(radicand, degree, denominator)
    square_lo, square_hi = root_interval(radicand**2, degree, denominator)
    assert alpha_hi - alpha_lo < side / 16
    assert square_hi - square_lo < side / 16

    # Approximate the explicit real target on a common rational grid.
    grid = 32 * degree * radicand**2
    rounded = sp.zeros(degree)
    for j in range(degree):
        for k in range(degree):
            target = (int(j == k) - sp.Rational(1, degree)) * alpha_lo ** (-j - k)
            rounded[j, k] = sp.floor(grid * target + sp.Rational(1, 2)) / grid
    assert rounded == rounded.T

    # The remainder rows have disjoint supports, so this is their exact
    # Frobenius orthogonal projection onto the rational relation space.
    matrix = rounded.copy()
    for residue in range(degree):
        row = sp.zeros(degree)
        for j in range(degree):
            for k in range(degree):
                if (j + k) % degree == residue:
                    row[j, k] = radicand ** ((j + k) // degree)
        norm_squared = sum(entry**2 for entry in row)
        assert norm_squared == residue + 1 + (degree - residue - 1) * radicand**2
        inner = sum(row[j, k] * rounded[j, k] for j in range(degree) for k in range(degree))
        matrix -= row * inner / norm_squared
    assert matrix == matrix.T
    assert quadratic_remainder(matrix, degree, radicand) == [0] * degree

    companion = sp.zeros(degree)
    for j in range(degree - 1):
        companion[j, j + 1] = 1
    companion[degree - 1, 0] = radicand
    pencil = [companion.T * matrix * companion, -(companion.T * matrix + matrix * companion), matrix]
    for coefficient in pencil:
        assert quadratic_remainder(coefficient, degree, radicand) == [0] * degree

    # The triangle contains (alpha, alpha**2) strictly. The inequalities
    # follow from the two exact isolating intervals, without floating point.
    vertices = [(alpha_lo - side, square_lo - side),
                (alpha_lo + 2 * side, square_lo - side),
                (alpha_lo - side, square_lo + 2 * side)]
    assert alpha_hi - alpha_lo + square_hi - square_lo < side
    quadrics = [pencil[0] + first * pencil[1] + second * pencil[2] for first, second in vertices]
    for quadric in quadrics:
        positive_definite(quadric[1:, 1:])
        assert quadratic_remainder(quadric, degree, radicand) == [0] * degree
    assert sp.Matrix([list(quadric[1:, 1:]) for quadric in quadrics]).rank() == 3

    # Stationarity of Q0 + alpha Q1 + alpha**2 Q2 at v(alpha).
    for j in range(degree):
        remainder = [sp.S.Zero] * degree
        for exponent, coefficient in enumerate(pencil):
            for k in range(degree):
                power = exponent + k
                remainder[power % degree] += coefficient[j, k] * radicand ** (power // degree)
        assert remainder == [0] * degree
    return max(max(abs(value.p).bit_length(), value.q.bit_length()) for quadric in quadrics for value in quadric)


def main():
    for degree in (3, 5, 7, 9):
        for radicand in (2, 3):
            bits = check_block(degree, radicand)
            print(f"PASS: d={degree}, radicand={radicand}, three positive definite Hessians; max coefficient bits={bits}")
    variable = sp.Symbol('T')
    polynomial = sp.Poly(sp.minpoly(sp.real_root(2, 3) + sp.real_root(3, 3), variable), variable)
    assert polynomial.degree() == 9 and polynomial.is_irreducible
    print("PASS: the sum of the two cubic block coordinates has degree nine")
    # The integer translation exceeds the modulus of every conjugate.
    translated = sp.Poly(polynomial.as_expr().subs(variable, variable - 7), variable)
    assert all((-1)**index * coefficient > 0
               for index, coefficient in enumerate(translated.all_coeffs()))
    print("PASS: the translated degree-nine minimal polynomial has ten nonzero coefficients")


if __name__ == '__main__':
    main()
