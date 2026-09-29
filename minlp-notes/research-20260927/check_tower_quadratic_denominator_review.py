"""Independent exact check of the quadratic-denominator block identity.

This deliberately uses a positive quadratic part, nonzero linear part,
and negative constant. It checks the general block construction, not the
tower's separate Hessian or coefficient-field theorem.
"""

import sympy as sp


def main():
    x, y, z = variables = sp.symbols("x y z")
    X = sp.Matrix(variables)
    H = sp.diag(1, 2, 3)
    ell = sp.Matrix([1, -2, 3])
    c = -4
    nu, tau = sp.Rational(2), sp.Rational(3)
    G = (X.T * H * X)[0] + (ell.T * X)[0] + c
    residuals = [x*x-y, x*y-z, y*z-2]
    q = [G/(tau*nu), *(r/nu for r in residuals)]
    multipliers = [1, x, y, z]
    w = sp.Matrix([m*f for m in multipliers for f in q])
    d, n = len(w), len(X)
    a = sp.zeros(d, 1)
    a[4 + 2] = nu      # x times the second residual / nu
    a[8 + 1] = -nu     # y times the first residual / nu
    U = sp.zeros(d, n)
    for j in range(n):
        U[4*(j+1), j] = tau*nu
    T = sp.Matrix([[0, 0, -sp.Rational(1, 2)], [0, 1, 0],
                   [-sp.Rational(1, 2), 0, 0]])
    R = y*y-x*z
    b = X*R
    v = w.col_join(b)
    C = (a*ell.T-U*T)/2
    K = (c*a*a.T).row_join(C).col_join(C.T.row_join(H))
    Delta = sp.diag(a*a.T, sp.eye(n))
    h = 1 + (X.T*X)[0]
    F0 = sum(f*f for f in q)

    def zero(polynomial):
        assert sp.Poly(sp.expand(polynomial), variables).is_zero

    zero((a.T*w)[0]-R)
    assert all(sp.expand(t) == 0 for t in U.T*w-X*G)
    zero((v.T*K*v)[0])
    zero((w.T*w)[0]-h*F0)
    zero((v.T*Delta*v)[0]-h*R*R)

    a2 = (a.T*a)[0]
    C2 = sum(t*t for t in C)
    mu_H = H.det()/sp.trace(H)**(n-1)
    epsilon = min(sp.Rational(1), 1/(2*(1+abs(c)*a2)),
                  mu_H/(4*(1+C2)))
    Q = sp.diag(sp.eye(d), sp.zeros(n)) + epsilon*K
    lower, pivots = Q.LDLdecomposition(hermitian=False)
    assert lower*pivots*lower.T == Q
    assert all(pivots[j, j] > 0 for j in range(d+n))
    mu_Q = Q.det()/sp.trace(Q)**(d+n-1)
    scale = sp.ceiling((2+a2)/mu_Q)
    Gram = scale*Q-Delta
    lower, pivots = (Gram-sp.eye(d+n)).LDLdecomposition(hermitian=False)
    assert lower*pivots*lower.T == Gram-sp.eye(d+n)
    assert all(pivots[j, j] > 0 for j in range(d+n))
    zero((v.T*Gram*v)[0]-h*(scale*F0-R*R))
    print("PASS: syzygy, zero Gram relation, multiplier identity, and exact PSD margins")


if __name__ == "__main__":
    main()
