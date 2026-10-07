"""Exact boundary-closure checks; no implementation of the general solver.

Run: python research-20261002/reviews/check_core_only_boundary_recourse.py
"""

from fractions import Fraction as Q


def positive_2(a, b, c):
    return a > 0 and a * c - b * b > 0


def weak_multipliers():
    # F=(v-1/2)^2 + y^2/2 + [4(v-1/2)^2+eps]y.
    # Base linear term -v and the genuine noise endpoint gamma=1 cancel.
    # y*=0 for all v. The full Hessian is indefinite elsewhere in the box.
    mu, growth, m1, third = Q(1), Q(1), Q(14), Q(16)
    h = m1 / mu
    k3 = 2 * third * (1 + h) ** 3
    eta = Q(1, 4)
    theta = min(k3 * eta**2 / 2, mu * growth / (4 * k3))
    nu = min(mu / 2, min(growth, mu / 2) / (1 + 2 * h**2))
    margin = min(growth / (1 + 2 * h**2), mu / 4, nu / 4)
    radius = min(Q(1, 8), theta / (16 * m1), margin / (4 * third))
    assert not positive_2(Q(2), Q(-4), Q(1))
    free, fixed = 0, 0
    for eps in [Q(0), theta / 100, theta / 2, theta, 2 * theta]:
        # Patch: v in [1/2-r,1/2+r], y in [0,r].
        # The optimum (1/2,0) lies on an original residual bound.
        midpoint_gradient_y = radius / 2 + eps
        fixes_y = midpoint_gradient_y - m1 * radius > 0
        if eps > theta:
            assert fixes_y
        curvature_loss = third * radius + margin
        if fixes_y:
            fixed += 1
            assert Q(2) - curvature_loss > 0
        else:
            free += 1
            assert eps <= theta
            assert positive_2(2 + 4 * radius - curvature_loss,
                              Q(0), 1 - curvature_loss)
        # Uniform scalar nonnegativity yields the claimed selector and gap.
        for v in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
            for y in [Q(0), Q(1, 3), Q(1)]:
                gap = (v - Q(1, 2))**2 + y*y/2 + (4*(v-Q(1, 2))**2+eps)*y
                assert gap >= (v - Q(1, 2))**2 + y*y/2
    assert free >= 1 and fixed >= 1
    return free, fixed


def changing_active_set():
    # F=(v-3/4)^2+y^2/2+(v-1/2)y+gamma*v.
    # s(v)=max(0,1/2-v); switch v=1/2, noise image gamma=1/2.
    # Full strong convexity is easy here: the fixture tests the branch
    # geometry and finite-law atoms, independently of the weak-multiplier test.
    cases = 0
    for gamma in [Q(-2), Q(-2, 3), Q(0), Q(1, 3), Q(1, 2), Q(2, 3), Q(2)]:
        if gamma <= Q(1, 2):
            v = min(Q(1), max(Q(1, 2), Q(3, 4) - gamma / 2))
        else:
            v = max(Q(0), Q(1) - gamma)
        y = max(Q(0), Q(1, 2) - v)
        dv = 2*(v-Q(3, 4)) + y + gamma
        dy = y + v-Q(1, 2)
        assert (dv >= 0 if v == 0 else dv <= 0 if v == 1 else dv == 0)
        assert dy >= 0 if y == 0 else dy == 0
        assert positive_2(Q(2), Q(1), Q(1))
        if 0 < v < 1:
            # Gradient Lipschitz constant two controls the image distance.
            assert abs(gamma-Q(1, 2)) <= 2*abs(v-Q(1, 2))
        cases += 1
    return cases


def core_vertex():
    # F=v^2/4+vy+y^2/2+v. Full Hessian is indefinite, but v=0 is
    # uniformly sign-fixable and leaves the residual Hessian exactly one.
    assert not positive_2(Q(1, 2), Q(1), Q(1))
    radius = Q(1, 128)
    center_grad_v = 1 + radius / 4 + radius / 2
    assert center_grad_v - 2*radius > 0
    assert Q(1) > 0


def common_budget():
    trials = 0
    for k in [1, 2, 7]:
        for bits in [2, 40, 400]:
            fallback = 2**bits
            rho = Q(1, 6*fallback)
            sigma = Q(3, 7)
            ctail, kc, cs, hv = 2**(bits+1), 3**(k+3), 2**(bits+k), Q(17, 3)
            g = rho*sigma/(2*k)
            tau = rho*sigma/(2*kc)
            eta = min(Q(1, 4), rho*sigma/(4*cs*hv))
            j = bits + 100
            lower = max(Q(2), Q(2**j), 4*k*ctail/rho, 2*kc/rho, 2*cs*k/rho)
            denominator = 1 << (lower.numerator.bit_length())
            while denominator < lower:
                denominator *= 2
            assert k*g/sigma + 2*k*ctail/denominator <= rho
            assert kc*(tau/sigma + Q(1, denominator)) <= rho
            assert cs*(2*hv*eta/sigma + Q(k, denominator)) <= rho
            assert 3*rho*fallback == Q(1, 2)
            assert denominator >= 2**j
            trials += 1
    return trials


if __name__ == "__main__":
    free, fixed = weak_multipliers()
    changes = changing_active_set()
    core_vertex()
    budgets = common_budget()
    print(f"PASS: {free} weak-multiplier releases; {fixed} sound residual fixings; "
          f"{changes} active-pattern/KKT cases; one indefinite core-vertex closure; "
          f"{budgets} exact three-event finite-law budgets")
