"""Independent exact checks for shrinking-circle local Hessian bounds.

Run: python research-20260927/check_circle_local_conditioning_review.py
"""

from fractions import Fraction as Q

import sympy as sp

from check_rational_circle_minimizer_review import (
    circle_chain, dyadic_below, matrix2_psd, rational, round_down,
)


def check_symbolic():
    a, b, R, u, v, U, V = sp.symbols("a b R u v U V", nonzero=True)
    x, y = R*a+u, R*b+v
    A, B = R*(a*a-b*b)/2, R*a*b
    X, Y = A+U, B+V
    c = 1/(2*R)
    r, s = X-c*(x*x-y*y), Y-2*c*x*y
    E = X*X+Y*Y-R*R/4-2*A*r-2*B*s-(x*x+y*y-R*R)/2
    target = U*U+V*V-(-b*u+a*v)**2
    difference = sp.cancel(E-target)
    assert sp.rem(sp.expand(difference), a*a+b*b-1, a) == 0
    derivative = sp.Matrix([[a, -b], [b, a]])
    for entry in derivative.T*derivative-sp.eye(2):
        assert sp.rem(sp.expand(entry), a*a+b*b-1, a) == 0


def check_instance(k):
    n = 2*(k+1)
    radii = [Q(1, 2**j) for j in range(k+1)]
    weights = [Q(k+1-j) for j in range(k+1)]
    C = max(Q(1), Q(2)**(k-2))
    Vbound, nu = 2/C, 1/(C*(k+1))
    m, L = Q(1, 2), Q(k+2)
    eps = dyadic_below(min(Q(1), m*m/(2*n),
        nu*nu*m*m/(36*n*(L+n*Vbound)**2)), square=True)
    eta = min(Q(1), 1/(8*C*(k+1)), eps/(8*(k+1)**2))
    mesh = dyadic_below(eta/(2*3**k))
    unit = circle_chain(k)
    point_pairs = [(r*a, r*b) for r, (a, b) in zip(radii, unit)]
    approx_unit = [unit[0]]
    for _ in range(k):
        a, b = approx_unit[-1]
        approx_unit.append((round_down(a*a-b*b, mesh),
                            round_down(2*a*b, mesh)))
    approx = [(r*a, r*b) for r, (a, b) in zip(radii, approx_unit)]
    H = [[Q(0) for _ in range(n)] for _ in range(n)]
    linear = [Q(0) for _ in range(n)]
    constant = sum(w*r*r for w, r in zip(weights, radii))
    H[0][0] = H[1][1] = weights[0]
    linear[0], linear[1] = -2*weights[0]*Q(3, 5), -2*weights[0]*Q(4, 5)
    J = sp.eye(n)
    rotations = [sp.eye(2)]
    for j in range(1, k+1):
        i, prev = 2*j, 2*j-2
        c, w = Q(2)**(j-2), weights[j]
        a, b = approx[j]
        H[i][i] += w
        H[i+1][i+1] += w
        H[prev][prev] += w*(2*c*a-Q(1, 2))
        H[prev+1][prev+1] += w*(-2*c*a-Q(1, 2))
        H[prev][prev+1] += 2*w*c*b
        H[prev+1][prev] += 2*w*c*b
        linear[i], linear[i+1] = -2*w*a, -2*w*b
        pa, pb = map(rational, point_pairs[j-1])
        block = 2*rational(c)*sp.Matrix([[pa, -pb], [pb, pa]])
        assert block.T*block == sp.eye(2)
        J[i:i+2, prev:prev+2] = -block
        rotations.append(block*rotations[-1])
        assert c/C <= 1
    diagonal_rotation = sp.diag(*rotations)
    scalar = sp.eye(k+1)
    for j in range(1, k+1):
        scalar[j, j-1] = -1
    assert diagonal_rotation.T*J*diagonal_rotation == sp.kronecker_product(scalar, sp.eye(2))
    lower = (k+1)**2*scalar.T*scalar-sp.eye(k+1)
    upper = 4*sp.eye(k+1)-scalar.T*scalar
    if k:
        _, diagonal = lower.LDLdecomposition(hermitian=False)
        assert all(diagonal[i, i] > 0 for i in range(k+1))
    else:
        assert lower == sp.zeros(1)
    _, diagonal = upper.LDLdecomposition(hermitian=False)
    assert all(diagonal[i, i] > 0 for i in range(k+1))

    point = [q for pair in point_pairs for q in pair]
    assert sum(q*q for q in point) < Q(4, 3)
    assert point[-1].denominator % (5**(2**k)) == 0
    assert point[-2].denominator % (5**(2**k)) == 0
    Gvalue = constant+sum(a*x for a, x in zip(linear, point))
    Gvalue += sum(H[i][j]*point[i]*point[j] for i in range(n) for j in range(n))
    assert Gvalue == 0
    ell = [linear[i]+2*sum(H[i][j]*point[j] for j in range(n)) for i in range(n)]
    ellnorm = sum(q*q for q in ell)
    assert ellnorm <= eps*eps
    assert 2*ellnorm/(eps*nu*nu) <= 2*eps/(nu*nu) < 1
    for j in range(k+1):
        i = 2*j
        assert matrix2_psd(H[i][i]-m, H[i][i+1], H[i+1][i+1]-m)
        assert matrix2_psd(L-H[i][i], -H[i][i+1], L-H[i+1][i+1])
        assert max(abs(approx[j][t]-point_pairs[j][t]) for t in (0, 1)) <= eta
    if k >= 4:
        assert Vbound < 1

    # Independently differentiate the actual output quartic at small sizes.
    if k <= 2:
        X = sp.Matrix(sp.symbols(f"x0:{n}"))
        G = rational(constant)+sp.Matrix(list(map(rational, linear))).dot(X)
        G += (X.T*sp.Matrix([[rational(q) for q in row] for row in H])*X)[0]
        residuals = [X[0]-sp.Rational(3, 5), X[1]-sp.Rational(4, 5)]
        for j in range(1, k+1):
            c = rational(Q(2)**(j-2))
            residuals.extend([X[2*j]-c*(X[2*j-2]**2-X[2*j-1]**2),
                              X[2*j+1]-2*c*X[2*j-2]*X[2*j-1]])
        F = G*G/rational(eps*nu*nu)+(k+1)**2*sum(r*r for r in residuals)
        point_subs = dict(zip(X, map(rational, point)))
        hessian = sp.hessian(F, X).subs(point_subs)
        ellv = sp.Matrix(list(map(rational, ell)))
        expected = 2*ellv*ellv.T/rational(eps*nu*nu)+2*(k+1)**2*J.T*J
        assert hessian == expected


if __name__ == "__main__":
    check_symbolic()
    for length in range(9):
        check_instance(length)
    print("PASS: symbolic shrinking-circle exposer and orthogonal gate derivative;")
    print("k=0,...,8 exact denominators, rounded zeros, quadratic margins, Jacobian")
    print("bounds and local Hessian bounds, including V<1; direct Hessians at k=0,1,2.")
