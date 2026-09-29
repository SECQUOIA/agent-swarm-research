"""Independent exact checks for the rational circle minimizer construction.

This tests finite instances and identities, not the uniform bit-complexity proof.
Run: python research-20260927/check_rational_circle_minimizer_review.py
"""

from fractions import Fraction as Q

import sympy as sp


def dyadic_below(bound, square=False):
    step = 2 if square else 1
    denominator = 1
    while Q(1, denominator) > bound:
        denominator *= 2**step
    return Q(1, denominator)


def round_down(value, mesh):
    return (value // mesh) * mesh


def circle_chain(k):
    result = [(Q(3, 5), Q(4, 5))]
    for _ in range(k):
        a, b = result[-1]
        result.append((a*a-b*b, 2*a*b))
    return result


def matrix2_psd(a, b, c):
    return a >= 0 and c >= 0 and a*c-b*b >= 0


def rational(value):
    return sp.Rational(value.numerator, value.denominator)


def check_symbolic_identity():
    a, b, u, v, U, V = sp.symbols("a b u v U V")
    x, y = a+u, b+v
    A, B = a*a-b*b, 2*a*b
    X, Y = A+U, B+V
    r, s = X-x*x+y*y, Y-2*x*y
    exposer = X*X+Y*Y-1-2*A*r-2*B*s-2*(x*x+y*y-1)
    centered = U*U+V*V-4*(-b*u+a*v)**2
    remainder = sp.rem(sp.expand(exposer-centered), a*a+b*b-1, a)
    assert sp.expand(remainder) == 0
    Bmatrix = 2*sp.Matrix([[A-1, B], [B, -A-1]])
    tangent = sp.Matrix([-b, a])
    for entry in Bmatrix+4*tangent*tangent.T:
        assert sp.rem(sp.expand(entry), a*a+b*b-1, a) == 0
    # The integer complex numerator is an idempotent modulo five.
    assert ((3*3-4*4) % 5, (2*3*4) % 5) == (3, 4)


def build_and_check(k):
    n = 2*(k+1)
    Vbound = Q(4*n)
    nu = Vbound**(-(n-1))
    omega = [Q(1, 8**j) for j in range(k+1)]
    m, L = omega[-1]/2, Q(2)
    epsilon = dyadic_below(min(Q(1), m*m/(2*n),
        nu*nu*m*m/(36*n*(L+n*Vbound)**2)), square=True)
    eta = min(Q(1), omega[-1]/8, epsilon/(4*(k+1)*Vbound))
    mesh = dyadic_below(eta/(2*3**k))
    true = circle_chain(k)
    rounded = [true[0]]
    for _ in range(k):
        a, b = rounded[-1]
        rounded.append((round_down(a*a-b*b, mesh),
                        round_down(2*a*b, mesh)))

    H = [[Q(0) for _ in range(n)] for _ in range(n)]
    linear = [Q(0) for _ in range(n)]
    constant = sum(omega)
    H[0][0] = H[1][1] = Q(1)
    linear[0], linear[1] = -2*true[0][0], -2*true[0][1]
    for j in range(1, k+1):
        a, b = rounded[j]
        i, p = 2*j, 2*(j-1)
        w = omega[j]
        H[i][i] += w
        H[i+1][i+1] += w
        H[p][p] += 2*w*(a-1)
        H[p+1][p+1] += 2*w*(-a-1)
        H[p][p+1] += 2*w*b
        H[p+1][p] += 2*w*b
        linear[i], linear[i+1] = -2*w*a, -2*w*b

    point = [entry for pair in true for entry in pair]
    value = constant + sum(linear[i]*point[i] for i in range(n))
    value += sum(H[i][j]*point[i]*point[j]
                 for i in range(n) for j in range(n))
    assert value == 0  # Rounding never destroys exact vanishing.
    gradient = [linear[i]+2*sum(H[i][j]*point[j] for j in range(n))
                for i in range(n)]
    assert sum(g*g for g in gradient) <= epsilon*epsilon
    for j in range(k+1):
        i = 2*j
        assert matrix2_psd(H[i][i]-m, H[i][i+1], H[i+1][i+1]-m)
        assert matrix2_psd(L-H[i][i], -H[i][i+1], L-H[i+1][i+1])
        a, b = true[j]
        assert a*a+b*b == 1
        assert a.denominator == b.denominator == 5**(2**j)
        assert (a.numerator % 5, b.numerator % 5) == (3, 4)
        da, db = rounded[j][0]-a, rounded[j][1]-b
        assert da*da+db*db <= eta*eta/4

    J = sp.eye(n)
    for j in range(1, k+1):
        a, b = map(rational, true[j-1])
        J[2*j, 2*j-2], J[2*j, 2*j-1] = -2*a, 2*b
        J[2*j+1, 2*j-2], J[2*j+1, 2*j-1] = -2*b, -2*a
    assert J.det() == 1
    assert sum(entry*entry for entry in J) == 2+10*k
    assert 2+10*k <= Vbound*Vbound
    return n, true, H, linear, constant, epsilon, nu, m, L, Vbound


def check_full_gram():
    n, true, h, linear, constant, eps, nu, m, L, Vbound = build_and_check(1)
    epsilon = rational(eps)
    point = sp.Matrix([rational(q) for pair in true for q in pair])
    H = sp.Matrix([[rational(q) for q in row] for row in h])
    ell = sp.Matrix(list(map(rational, linear)))+2*H*point
    X = sp.Matrix(sp.symbols(f"x0:{n}"))
    v = sp.Matrix(sp.symbols(f"v0:{n}"))
    residuals = [X[0]-sp.Rational(3, 5), X[1]-sp.Rational(4, 5),
                 X[2]-X[0]**2+X[1]**2, X[3]-2*X[0]*X[1]]
    subs_point = dict(zip(X, point))
    gradients = [sp.Matrix([sp.diff(r, x) for x in X]).subs(subs_point)
                 for r in residuals]
    parts = [sp.hessian(r, X)/2 for r in residuals]

    def cross(b, T):
        return sp.Matrix(n, n*n,
            lambda i, col: 2*b[col//n]*T[i, col % n]
                          +4*b[i]*T[col//n, col % n])

    def fourth(T):
        vector = sp.Matrix(list(T))
        return 8*vector*vector.T+4*sp.kronecker_product(T, T)

    C = 2*ell*ell.T
    D, Qfour = cross(ell, H), fourth(H)
    for b, T in zip(gradients, parts):
        C += 2*epsilon*b*b.T
        D += epsilon*cross(b, T)
        Qfour += epsilon*fourth(T)
    M = C.row_join(D).col_join(D.T.row_join(Qfour))
    _, diagonal = M.LDLdecomposition(hermitian=False)
    assert all(diagonal[i, i] > 0 for i in range(M.rows))

    G = rational(constant)+(sp.Matrix(list(map(rational, linear))).dot(X))
    G += (X.T*H*X)[0]
    phi = G*G+epsilon*sum(r*r for r in residuals)
    shift = sp.eye(n).row_join(sp.zeros(n, n*n)).col_join(
        (-sp.kronecker_product(point, sp.eye(n))).row_join(sp.eye(n*n)))
    Mx = shift.T*M*shift
    z = list(v)+[X[i]*v[j] for i in range(n) for j in range(n)]
    vector = sp.Matrix(z)
    assert sp.expand((vector.T*Mx*vector)[0]-(v.T*sp.hessian(phi, X)*v)[0]) == 0

    # Round a Gram to short dyadics, then impose exact coefficient equations.
    q = 2*m*m
    s = Q(3, 2)*eps*nu*nu
    BD = 6*n*eps*(L+n*Vbound)
    mu = min(s, q)/((2+2*(BD/q)**2)*(2+n)**2)
    mesh = dyadic_below(mu/(8*Mx.rows))
    T = sp.zeros(Mx.rows)
    for i in range(Mx.rows):
        for j in range(i, Mx.cols):
            entry = Q(int(Mx[i, j].p), int(Mx[i, j].q))
            T[i, j] = T[j, i] = rational(round_down(entry, mesh))
    groups = {}
    for i in range(Mx.rows):
        for j in range(Mx.cols):
            key = sp.Poly(z[i]*z[j], *X, *v).monoms()[0]
            groups.setdefault(key, []).append((i, j))
    for cells in groups.values():
        correction = sum(Mx[i, j]-T[i, j] for i, j in cells)/len(cells)
        for i, j in cells:
            T[i, j] += correction
    assert T == T.T
    assert sum(entry*entry for entry in T-Mx) < rational(mu*mu/16)
    assert sp.expand((vector.T*T*vector)[0]-(v.T*sp.hessian(phi, X)*v)[0]) == 0

    # Taylor integration supplies a rational maximal-rank polynomial Gram.
    integrated = (C/2).row_join(D/6).col_join((D.T/6).row_join(Qfour/12))
    basis = [sp.Integer(1)]+list(X)
    basis += [X[i]*X[j] for i in range(n) for j in range(i, n)]
    centered = X-point
    factors = list(centered)+[centered[i]*centered[j]
                             for i in range(n) for j in range(n)]
    exponent_list = [sp.Poly(q, *X).monoms()[0] for q in basis]
    translation = sp.Matrix([[sp.Poly(q, *X).coeff_monomial(exponent)
                             for exponent in exponent_list] for q in factors])
    optimal_gram = translation.T*integrated*translation
    evaluation = sp.Matrix([q.subs(subs_point) for q in basis])
    assert optimal_gram*evaluation == sp.zeros(len(basis), 1)
    assert optimal_gram.rank() == len(basis)-1
    bvector = sp.Matrix(basis)
    assert sp.expand((bvector.T*optimal_gram*bvector)[0]-phi) == 0
    A, c = optimal_gram[1:, 1:], optimal_gram[1:, 0]
    assert A.inv()*(-c) == evaluation[1:, 0]
    exposer = sp.Rational(7, 11)*evaluation*evaluation.T
    assert exposer[0, 3]/exposer[0, 0] == point[2]
    assert point[2].q == 25


if __name__ == "__main__":
    check_symbolic_identity()
    for length in range(9):
        build_and_check(length)
    check_full_gram()
    print("PASS: symbolic circle identity; exact denominators, rounded exposers,")
    print("curvature margins and Jacobians for k=0,...,8; k=1 exact positive")
    print("Hessian Gram, affine translation, and rounded coefficient projection;")
    print("Taylor optimal Gram rank/kernel, rational recovery, and exposing ratios.")
