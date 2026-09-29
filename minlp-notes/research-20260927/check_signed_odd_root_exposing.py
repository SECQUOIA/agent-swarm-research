"""Exact local checks for the signed odd-root circuit quartic lift.

These checks support identities and indexing for finitely many degrees.
They do not prove the general spectral or bit-complexity estimates.
"""

import sympy as s


for d in [3, 5, 7, 9, 11]:
    n = (d + 1) // 2
    alpha, b, v = s.symbols("alpha b v")
    x = (s.Integer(1),) + s.symbols(f"x1:{n+1}")
    u = (s.Integer(0),) + s.symbols(f"u1:{n+1}")
    ell = s.Matrix([x[j+1] - alpha*x[j] for j in range(n)])
    T = s.diag(*[alpha**(d-1-2*j) for j in range(n)])
    for j in range(n-1):
        T[j, j+1] = T[j+1, j] = alpha**(d-2-2*j)/2
    exposing = s.expand((ell.T*T*ell)[0])
    power_curve = {x[j]: alpha**j for j in range(1, n+1)}
    assert exposing.subs(power_curve) == 0

    def representative(weight):
        if weight == 0:
            return s.Integer(1)
        if weight <= n:
            return x[weight]
        return x[n]*x[weight-n]

    relations = 0
    total_coefficient_norm = 0
    for exponent, coefficient in s.Poly(exposing, x[1:]).terms():
        monomial = s.prod(x[j+1]**exponent[j] for j in range(n))
        weight = sum((j+1)*exponent[j] for j in range(n))
        relations += coefficient*(monomial-representative(weight))
        pc = s.Poly(coefficient, alpha)
        total_coefficient_norm += sum(abs(c) for c in pc.all_coeffs())
        assert pc.degree() <= 2*n
    assert total_coefficient_norm <= 8*n
    S = x[n]**2-b*x[1]
    terminal = x[n-1]*x[n]-b
    E = s.expand(S-alpha*terminal+relations)
    assert s.expand(E-exposing-(alpha-x[1])*(b-alpha**d)) == 0

    H = s.hessian(exposing, x[1:])/2
    shift = {x[j]: alpha**j+u[j] for j in range(1, n+1)}
    shifted = E.subs(shift).subs(b, alpha**d+v)
    um = s.Matrix(u[1:])
    assert s.expand(shifted-(um.T*H*um)[0]+u[1]*v) == 0

    residuals = [x[1]*x[j]-x[j+1] for j in range(1, n)] + [terminal]
    jacobian = s.Matrix(residuals).jacobian(x[1:]).subs(power_curve)
    assert s.factor(jacobian.det()-d*alpha**(d-1)) == 0

    for av in [s.Integer(1), s.Rational(3, 2), s.Integer(2)]:
        local_T = T.subs(alpha, av)
        margin_T = local_T-s.eye(n)/((n+1)**2)
        _, diagonal = margin_T.LDLdecomposition(hermitian=False)
        assert all(diagonal[j, j] > 0 for j in range(n))
        h0 = 1/(s.Integer(n)**2*(n+1)**2*av**(2*n))
        _, diagonal = (H.subs(alpha, av)-h0*s.eye(n)).LDLdecomposition(hermitian=False)
        assert all(diagonal[j, j] > 0 for j in range(n))
    print(f"PASS degree {d}: exact exposing identity, coefficient bound, Jacobian, sample LDL margins")
