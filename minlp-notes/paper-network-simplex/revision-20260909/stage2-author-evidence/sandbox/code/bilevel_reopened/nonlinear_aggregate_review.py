"""Independent exact checks for nonlinear aggregate rational recovery.

The first family rounds across an irrational polynomial branch boundary.
The second has zero curvature in both local and aggregate costs.
No repository algorithm or floating-point optimization is used.
"""

from fractions import Fraction as F
import json


def cube_bracket(target, width):
    lo, hi = F(0), F(1)
    while hi-lo >= width:
        mid = (lo+hi)/2
        if mid**3 < target:
            lo = mid
        elif mid**3 > target:
            hi = mid
        else:
            raise AssertionError("Test boundary unexpectedly rational")
    assert lo**3 < target < hi**3
    return lo, hi


def is_integer_cube(n):
    lo, hi = 0, n+1
    while hi-lo > 1:
        mid = (lo+hi)//2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return lo**3 == n


def run():
    counts = dict(irrational_boundaries=0, recovered_points=0,
                  complementarity_terms=0, singular_quartic_cases=0)
    # F_x(z)=z^2/2-xz+z^4/4, 0<=z<=1, and the redundant row z<=1.
    # At x=17/64 the exact follower optimum is z0=1/4.
    z0 = F(1, 4)
    x = z0+z0**3
    assert z0+z0**3-x == 0
    for bits in [4, 8, 12, 20, 32]:
        eta = F(1, 2**bits)
        h = eta/128
        offset = eta**4
        target = z0**3+offset
        beta = z0-offset
        # w*^3=target, q*=x-w*^3=beta. The branch equality
        # a(v*)=beta is irrational in w, with x fixed rational.
        # A reduced rational cube must have integer-cube numerator
        # and denominator. Certify irrationality before bracketing.
        assert not (is_integer_cube(target.numerator)
                    and is_integer_cube(target.denominator))
        lo, hi = cube_bracket(target, h/4)
        assert beta > 0
        assert (beta+eta)**3 > target
        counts['irrational_boundaries'] += 1
        for w_hat in [lo, hi]:
            lambda_hat = F(0) if w_hat == lo else h/2
            q_hat = x-w_hat**3-lambda_hat
            assert 0 < q_hat < 1
            assert abs(q_hat-beta) < eta
            # Rounded auxiliary points lie on opposite sides of the
            # original nonlinear branch boundary, also after multiplier
            # perturbation; retaining its equality is impossible.
            if w_hat == lo:
                assert q_hat > beta
            else:
                assert q_hat < beta
            e_star, e_hat = beta-1, q_hat-1
            assert e_hat <= 4*eta
            assert abs(lambda_hat*e_hat) <= 5*eta
            assert abs(w_hat-q_hat) <= 4*eta
            first = lambda_hat*(e_hat-e_star)
            second = lambda_hat*e_star
            assert abs(first) <= 2*eta
            assert abs(second) <= eta
            assert first+second == lambda_hat*e_hat
            counts['complementarity_terms'] += 2
            # Use valid loose constants K=1,L=3,D=3,mu=1/16.
            # Verify (3) without extracting an approximate square root.
            error = abs(q_hat-z0)
            repair = 4*eta
            gap_bound = 3*repair+5*eta+3*(4*eta)
            assert max(F(0), error-repair)**2 <= gap_bound/F(1,16)
            counts['recovered_points'] += 1

    # g(z)=(z-1/2)^3+1/8; phi(w)=w^4/4; U=(1,-1).
    # The exact response at ell=(1/8,1/8) is (1/2,1/2).
    # For frozen w, the exact box response is (1/2-w,1/2+w).
    # Both local Hessians and the aggregate Hessian vanish at the optimum.
    mu = F(1,4)/(4*12**3)
    d_bound = F(24)  # W=[-2,2], L_phi=12, sum ||U_i||_1=2.
    for denominator in [8, 32, 256, 4096]:
        for numerator in [-3, -1, 0, 1, 3]:
            w = F(numerator, denominator)
            q = [F(1,2)-w, F(1,2)+w]
            assert all(0 <= z <= 1 for z in q)
            assert (q[0]-F(1,2))**3+F(1,8) == F(1,8)-w**3
            assert (q[1]-F(1,2))**3+F(1,8) == F(1,8)+w**3
            rho = abs(q[0]-q[1]-w)
            error = abs(w)
            assert mu*error**4 <= d_bound*rho
            # Sharper no-resource estimate retains one factor of error.
            assert mu*error**3 <= d_bound*rho
            counts['singular_quartic_cases'] += 1
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    run()
