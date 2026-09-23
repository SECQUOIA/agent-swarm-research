"""Exact diagnostics for the response-constraint extension; standard library only.

These checks target the counterexamples and constants, not a surrogate solver.
"""
from fractions import Fraction as Q
from math import isqrt


def g(z):
    return z + z*z*(z-Q(1, 2))


def main():
    counts = {}
    # Monotonicity certificate and inverse-order characterization, independently
    # checked with rational bisection rather than taking the claimed inverse.
    n = 0
    for i in range(101):
        x = Q(i, 100)
        derivative = 1+3*x*x-x
        assert derivative == 3*(x-Q(1, 6))**2+Q(11, 12)
        assert derivative >= Q(11, 12)
        predicted = x == 0 or x >= Q(1, 2)
        assert (g(x) >= x) == predicted
        if x not in (0, Q(1, 2)):
            lo, hi = Q(0), Q(1)
            for _ in range(120):
                mid = (lo+hi)/2
                if g(mid) < x:
                    lo = mid
                else:
                    hi = mid
            assert (hi < x) if predicted else (lo > x)
        n += 1
    counts['strong_convexity_and_inverse_feasibility'] = n

    # Equality sqrt(x)=x+1/8 gives x^2-3x/4+1/64=0.
    # Its discriminant is 1/2, which is not a square in Q.
    discriminant = Q(3, 4)**2-4*Q(1, 64)
    assert discriminant == Q(1, 2)
    assert (isqrt(discriminant.numerator)**2 != discriminant.numerator or
            isqrt(discriminant.denominator)**2 != discriminant.denominator)
    # Exact sign brackets locate both positive roots inside (0,1); x+1/8>0
    # ensures that the squared equation introduces no extraneous root.
    poly = lambda x: x*x-Q(3, 4)*x+Q(1, 64)
    assert poly(Q(0)) > 0 > poly(Q(1, 8))
    assert poly(Q(1, 2)) < 0 < poly(Q(7, 8))
    counts['irrational_feasible_set'] = 1

    # A real reserve model: response z=sqrt(u), upper z-s-1/4<=0,
    # s in [0,1], safe reserve 1 with uniform margin 1/4.
    # Use rational squares so every response and check is exact.
    n = 0
    for i in range(41):
        z = Q(i, 40)
        u = z*z
        s = max(Q(0), z-Q(1, 4))
        assert z-s-Q(1, 4) <= 0
        for j in range(1, 41):
            theta = Q(j, 40)
            tightened = Q(1, 4)*theta
            st = (1-theta)*s+theta
            assert z-st-Q(1, 4) <= -tightened
            before = -u+Q(1, 2)*s
            after = -u+Q(1, 2)*st
            assert after-before <= Q(1, 2)*theta
            n += 1
    counts['reserve_interpolation'] = n

    # Error-ledger extremizers: A*rho is the worst signed response error;
    # enumerate unrelated scales to catch incorrectly shared tolerances.
    n = 0
    for objective_bits in (0, 1, 4, 16, 64):
        eps = Q(1, 2**objective_bits)
        for constraint_bits in (0, 2, 7, 23, 80):
            delta = Q(1, 2**constraint_bits)
            for A in (Q(1), Q(7, 3), Q(2**40)):
                rho = min(Q(1, 4), eps/(8*A), delta/(8*A))
                outer_violation = 2*A*rho+delta/4
                objective_loss = 2*A*rho+eps/4
                inner_violation = -delta/2+delta/8+A*rho
                assert outer_violation <= delta/2
                assert objective_loss <= eps/2
                assert inner_violation <= -delta/4
                n += 1
    counts['independent_error_ledgers'] = n
    # Polynomial upper functions on the enlarged response box, including tariff
    # revenue and cross-response terms. Check x and response Lipschitz constants
    # separately so cancellation in a combined bound cannot hide an error.
    polynomials = [
        [(Q(-1), 1, (1, 0)), (Q(1, 2), 2, (0, 0))],
        [(Q(3, 2), 0, (1, 1)), (Q(-5, 7), 1, (2, 0)),
         (Q(2), 2, (0, 3))],
        [(Q(7), 0, (0, 0)), (Q(-2), 3, (0, 0))],
    ]
    x_grid = (Q(0), Q(1, 2), Q(1))
    z_grid = [(Q(a), Q(b)) for a in (-1, 0, 1, 2)
              for b in (-1, 0, 1, 2)]
    n = 0
    for terms in polynomials:
        def evaluate(x, z):
            return sum(a*x**alpha*z[0]**beta[0]*z[1]**beta[1]
                       for a, alpha, beta in terms)
        lx = sum(abs(a)*alpha*2**sum(beta) for a, alpha, beta in terms)
        lz = sum(abs(a)*sum(beta)*2**sum(beta) for a, alpha, beta in terms)
        for x in x_grid:
            for z in z_grid:
                for zp in z_grid:
                    distance = max(abs(z[i]-zp[i]) for i in (0, 1))
                    assert abs(evaluate(x, z)-evaluate(x, zp)) <= lz*distance
                    n += 1
        for z in z_grid:
            for x in x_grid:
                for xp in x_grid:
                    assert abs(evaluate(x, z)-evaluate(xp, z)) <= lx*abs(x-xp)
                    n += 1
    counts['polynomial_upper_lipschitz_on_enlarged_box'] = n
    print(counts)
    print('PASS:', sum(counts.values()), 'exact diagnostic cases')


if __name__ == '__main__':
    main()
