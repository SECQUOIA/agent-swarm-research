"""Independent exact checks for the parameter-family SDP review.

This checks polynomial identities and a separating rational point. Cone
equalities, nonnegativity, and SDP equivalence are proved in the review note.
"""

import sympy as s


def main():
    x, y, z, h, d1, d2, d3, k = s.symbols("x y z h d1 d2 d3 k", real=True)
    p = (h - d1*x - d2*y + d3*z)**2 + 2*d3*k*z*(1-x-y) \
        + k*(2*(d1+d2-h)+k)*x*y
    certificate = (h-d1*x-d2*y+d3*z-k*x*y)**2 \
        + 2*d3*k*z*(1-x)*(1-y) + k*(2*d1+k)*x*y*(1-x) \
        + 2*k*d2*x*y*(1-y) + k**2*x**2*y*(1-y)
    assert s.expand(p - certificate) == 0

    mx, my, mz, a, b, c, r, t, u = s.symbols("mx my mz a b c r t u")
    moments = {1: 1, x: mx, y: my, z: mz,
               x*x: a, y*y: b, z*z: c, x*y: r, x*z: t, y*z: u}
    evaluation = sum(coef*moments[x**powers[0]*y**powers[1]*z**powers[2]]
                     for powers, coef in s.Poly(p, x, y, z).terms())
    beta = s.Matrix([-mx, -my, mz, -r])
    matrix = s.Matrix([[a, r, -t, r], [r, b, -u, r],
                       [-t, -u, c, mz-t-u], [r, r, mz-t-u, r]])
    v = s.Matrix([d1, d2, d3, k])
    assert s.expand(evaluation - h*h - 2*h*beta.dot(v)
                    - (v.T*matrix*v)[0]) == 0
    assert s.expand(evaluation.subs(h, -beta.dot(v))
                    - (v.T*(matrix-beta*beta.T)*v)[0]) == 0

    point = {mx: s.Rational(4041, 10000), my: s.Rational(4041, 10000),
             mz: s.Rational(1377, 10000), a: s.Rational(3392, 10000),
             b: s.Rational(3392, 10000), c: s.Rational(681, 10000),
             r: s.Rational(771, 10000), t: s.Rational(1025, 10000),
             u: s.Rational(1025, 10000)}
    parameters = {d1: 1, d2: 1, d3: 3, k: 1}
    original = evaluation.subs(point).subs(parameters).subs(h, s.Rational(1, 2))
    optimal_h = -beta.dot(v).subs(point).subs(parameters)
    stronger = evaluation.subs(point).subs(parameters).subs(h, optimal_h)
    assert original == -s.Rational(1, 40)
    assert optimal_h == s.Rational(2361, 5000)
    assert stronger == -s.Rational(644321, 25000000)
    print("PASS: nonnegative decomposition and moment-form identities.")
    print("Original rational violation:", original)
    print("Free-h minimizer:", optimal_h, "; violation:", stronger)


if __name__ == "__main__":
    main()
