"""Targeted exact checks for the arbitrary-prime SOS field construction.

Finite checks supplement the universal proof in arbitrary-prime-strict-sos-field.md.
No numerical eigenvalue or SDP calculation is used.
"""

import sympy as s


def canonical_blocks(d, b, T):
    n = len(b)
    C = 2*b*b.T + 4*d*T
    D = s.Matrix(n, n*n, lambda i, kj:
                 2*b[kj//n]*T[i, kj % n]
                 + 4*b[i]*T[kj//n, kj % n])
    vec = s.Matrix([T[k, j] for k in range(n) for j in range(n)])
    Q = 8*vec*vec.T + 4*s.kronecker_product(T, T)
    return C.row_join(D).col_join(D.T.row_join(Q))


def square_gram(q, x):
    origin = dict.fromkeys(x, 0)
    return canonical_blocks(q.subs(origin),
                            s.Matrix([s.diff(q, t).subs(origin) for t in x]),
                            s.hessian(q, x)/2)


def scaled_power_floor(k, p, denominator):
    target = (denominator**p) * (2**k)
    lo, hi = 0, 4*denominator+1
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**p <= target:
            lo = mid
        else:
            hi = mid
    assert lo**p <= target < (lo+1)**p
    return lo


def check_translation():
    d, b0, b1, t00, t01, t11, c0, c1 = s.symbols(
        "d b0 b1 t00 t01 t11 c0 c1")
    b = s.Matrix([b0, b1])
    c = s.Matrix([c0, c1])
    T = s.Matrix([[t00, t01], [t01, t11]])
    M = canonical_blocks(d, b, T)
    shift = s.eye(6)
    shift[2:, :2] = -s.kronecker_product(c, s.eye(2))
    shifted = canonical_blocks(d-(b.T*c)[0]+(c.T*T*c)[0], b-2*T*c, T)
    assert all(s.expand(t) == 0 for t in shift.T*M*shift-shifted)
    print("PASS: generic two-variable canonical Gram translation identity")


def check_bounds():
    for n in range(3, 81):
        N = 2**20*n**8
        eps = s.Rational(1, N*N)
        denominator = 64*(n+1)*N*N
        m = s.Rational(1, 4*n**4)
        nu = s.Rational(1, 8*n)
        coefficient_bound = 40+8*n
        assert coefficient_bound <= 24*n
        assert eps <= min(1, m*m/(2*n),
                          nu*nu*m*m/(36*n*coefficient_bound**2))
        assert 1152*n**10*eps < 1
        beta = eps/(256*n*n)
        assert denominator**2*beta > 64*n+1
    print("PASS: all stated regularization and perturbation inequalities, n=3,...,80")


def check_prime(p):
    half = (p-1)//2
    n = half+1
    x = s.symbols("x:"+str(n))
    v = s.symbols("v:"+str(n))
    a, t = s.symbols("a t")
    point = {x[i]: a**(half+i) for i in range(n)}

    def reduce_a(f):
        return s.rem(s.expand(f), a**p-2, a)

    def at_point(f):
        return reduce_a(f.subs(point))

    exposing_quadrics = [x[0]**2-x[half], x[half]**2-2*x[half-1],
                         x[0]*x[1]-2]
    exposing_quadrics += [x[i]**2-x[i-1]*x[i+1] for i in range(1, half)]
    weights = [2*a, a*a, s.Integer(-2)]
    weights += [a**(2*half-2*i+2) for i in range(1, half)]
    exposer = sum(w*q for w, q in zip(weights, exposing_quadrics))
    residuals = [x[0]**2-x[half], x[0]*x[1]-2]
    residuals += [x[0]*x[i]-x[1]*x[i-1] for i in range(2, half+1)]
    unused = x[1]*x[half]-2*x[0]
    assert all(at_point(q) == 0 for q in exposing_quadrics+residuals+[unused])
    assert all(s.Poly(q, x).coeff_monomial(x[0]) == 0
               for q in exposing_quadrics+residuals)

    G = s.zeros(n)
    for i in range(n):
        G[i, i] = a**(2*half-2*i)
        if i < half:
            G[i, i+1] = G[i+1, i] = a**(2*half-2*i-1)/2
    linear = s.Matrix([x[i+1]-a*x[i] for i in range(half)] + [2-a*x[half]])
    assert reduce_a((linear.T*G*linear)[0]-exposer) == 0
    curve = {x[i]: t**(half+i) for i in range(n)}
    assert reduce_a(exposer.subs(curve)-(t**p-2)*(a*a*t**(p-2)-2)) == 0

    # The integer map on scaled tangent coordinates has determinant p.
    tangent = s.symbols("h:"+str(n))
    rows = [2*tangent[0]-tangent[half], tangent[0]+tangent[1]]
    rows += [tangent[0]+tangent[i]-tangent[1]-tangent[i-1]
             for i in range(2, half+1)]
    normalized_jacobian = s.Matrix(rows).jacobian(tangent)
    assert normalized_jacobian.det() == p
    row_scales = [a**(2*half), s.Integer(2)]
    row_scales += [a**(2*half+i) for i in range(2, half+1)]
    claimed_jacobian = (s.diag(*row_scales)*normalized_jacobian
                        *s.diag(*[a**(p-half-i)/2 for i in range(n)]))
    actual_jacobian = s.Matrix(residuals).jacobian(x).subs(point)
    assert all(reduce_a(entry) == 0 for entry in actual_jacobian-claimed_jacobian)

    N = 2**20*n**8
    denominator = 64*(n+1)*N*N
    integer_weights = [scaled_power_floor(p+1, p, denominator),
                       scaled_power_floor(2, p, denominator), -2*denominator]
    integer_weights += [scaled_power_floor(2*half-2*i+2, p, denominator)
                        for i in range(1, half)]
    A = s.expand(sum(w*q for w, q in zip(integer_weights, exposing_quadrics)))
    scale = denominator//N
    assert scale*N == denominator
    F = s.expand(A*A+scale**2*sum(q*q for q in residuals)-unused*unused)
    assert at_point(F) == 0
    assert all(at_point(s.diff(F, q)) == 0 for q in x)
    coefficients = s.Poly(F, x)
    assert coefficients.coeff_monomial(x[half])+coefficients.coeff_monomial(x[0]**2) == -4

    M = square_gram(A, x)
    M += scale**2*sum((square_gram(q, x) for q in residuals), s.zeros(n+n*n))
    M -= square_gram(unused, x)
    assert all(entry.q == 1 for entry in M)
    lower, diagonal = (M-s.eye(n+n*n)).LDLdecomposition(hermitian=False)
    assert all(diagonal[i, i] > 0 for i in range(n+n*n))
    assert lower*diagonal*lower.T == M-s.eye(n+n*n)
    basis = s.Matrix(list(v)+[x[k]*v[j] for k in range(n) for j in range(n)])
    actual = (s.Matrix(v).T*s.hessian(F, x)*s.Matrix(v))[0]
    claimed = (basis.T*M*basis)[0]
    assert s.Poly(s.expand(actual-claimed), x+v).is_zero
    print("PASS prime", p, ": exposing identity, Jacobian, zero, stationarity, obstruction")
    print("PASS prime", p, ": integer Hessian Gram identity and exact positive LDL of M-I")
    print("  variables", n, "monomials", len(coefficients.terms()),
          "coefficient bits", max(abs(int(c)).bit_length() for c in coefficients.coeffs()),
          "Gram bits", max(abs(int(c)).bit_length() for c in M))


if __name__ == "__main__":
    check_translation()
    check_bounds()
    for prime in [5, 7]:
        check_prime(prime)
