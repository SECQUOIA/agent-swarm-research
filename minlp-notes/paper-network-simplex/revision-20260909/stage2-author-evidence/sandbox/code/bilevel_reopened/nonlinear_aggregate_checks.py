"""Exact diagnostics for the convex-aggregate response certificate.

Run: python code/bilevel_reopened/nonlinear_aggregate_checks.py
No floating-point optimizer or third-party dependency is used.
"""

from fractions import Fraction as Q
from itertools import product


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def clipped(t):
    return min(Q(1), max(Q(0), t))


def check_case(q, zstar, w, u, rows, rhs, lam, ell, cost, marginal, p, gend, lbound):
    """Check known KKT optimum, frozen-gradient inverse, and certificate.

    All cases use phi(w)=w²/2+w⁴/4, |w|<=R, and one equality
    z1=z2 when resource rows are present. Its repair is the midpoint.
    """
    n = len(q)
    r = max(Q(1), sum(abs(a) for a in u))
    assert abs(w) <= r
    phi = lambda a: a * a / 2 + a**4 / 4
    grad = lambda a: a + a**3
    aggregate = dot(u, q)
    astar = dot(u, zstar)
    for i in range(n):
        a = ell[i] - u[i] * grad(w) - sum(row[i] * lm for row, lm in zip(rows, lam))
        if q[i] == 0:
            assert a <= marginal(Q(0))
        elif q[i] == 1:
            assert a >= marginal(Q(1))
        else:
            assert a == marginal(q[i])
    assert all(dot(row, zstar) <= b for row, b in zip(rows, rhs))

    def objective(z):
        return sum(cost(v) - e * v for v, e in zip(z, ell)) + phi(dot(u, z))

    residual = [dot(row, q) - b for row, b in zip(rows, rhs)]
    delta = max([Q(0)] + residual)
    zeta = abs(dot(lam, residual))
    rho = abs(aggregate - w)
    d = (1 + 3 * r**2) * sum(abs(a) for a in u)
    assert objective(q) + dot(lam, residual) <= objective(zstar) + d * rho

    y = [(q[0] + q[1]) / 2] * 2 if rows else q
    k = Q(1)  # Valid infinity-norm repair bound for this equality.
    assert max(abs(a - b) for a, b in zip(y, q)) <= k * delta
    assert all(dot(row, y) <= b for row, b in zip(rows, rhs))
    gap_bound = lbound * k * delta + zeta + d * rho
    actual_gap = objective(y) - objective(zstar)
    assert Q(0) <= actual_gap <= gap_bound
    mu = gend / (4 * (4 * p) ** p)
    repaired_distance = max(abs(a - b) for a, b in zip(y, zstar))
    assert mu * repaired_distance ** (p + 1) <= (
        lbound * k * delta + zeta + d * rho * (k * delta + repaired_distance)
    )
    response_distance = max(abs(a - b) for a, b in zip(q, zstar))
    excess = max(Q(0), response_distance - k * delta)
    assert mu * excess ** (p + 1) <= gap_bound
    if not rows:
        assert mu * response_distance**p <= d * rho or response_distance == 0
    return 1


def quadratic_checks():
    count = 0
    # Interior and saturated exact optimizers, with signed aggregate columns.
    for u in [(Q(1), Q(-1)), (Q(1, 2), Q(1)), (Q(-1), Q(-1, 2))]:
        for zstar in product([Q(0), Q(1, 4), Q(1, 2), Q(1)], repeat=2):
            a = dot(u, zstar)
            ell = [zstar[i] + u[i] * (a + a**3) for i in range(2)]
            # Gradient at zstar is zero, including at box endpoints.
            for w in [Q(-1), Q(-1, 2), Q(0), Q(1, 3), Q(1)]:
                q = [clipped(ell[i] - u[i] * (w + w**3)) for i in range(2)]
                r = max(Q(1), sum(abs(v) for v in u))
                lbound = sum(Q(1) + abs(e) + abs(ui) * (r + r**3) for e, ui in zip(ell, u))
                count += check_case(q, zstar, w, u, [], [], [], ell,
                                    lambda z: z*z/2, lambda z: z, 1, Q(1), lbound)
    return count


def flat_curvature_resource_checks():
    count = 0
    # g(z)=(z-1/2)^3+1/8 has signed coefficients and g'(1/2)=0.
    g = lambda z: (z-Q(1, 2))**3 + Q(1, 8)
    f = lambda z: (z-Q(1, 2))**4/4 + z/8
    u = [Q(1), Q(-1)]
    rows = [u, [-a for a in u]]
    zstar = [Q(1, 2), Q(1, 2)]
    ell = [Q(1, 8)]*2
    for t in [Q(a, 16) for a in range(17)]:
        q = [t, 1-t]
        for w in [Q(a, 8) for a in range(-16, 17)]:
            signed = -(w+w**3) - (t-Q(1, 2))**3
            lam = [max(Q(0), signed), max(Q(0), -signed)]
            count += check_case(q, zstar, w, u, rows, [Q(0), Q(0)], lam, ell,
                                f, g, 3, Q(1, 4), Q(81, 4))
    return count


def rounding_ledger_checks():
    count = 0
    # Test transfer of the true complementarity residual, including large
    # negative slack, changing multipliers, and mixed row signs.
    eta = Q(1, 100)
    for e0, lm0, de, dl in product([Q(-100), Q(-1), Q(0), 2*eta],
                                  [Q(0), Q(1, 10000), Q(1)],
                                  [-2*eta, Q(0), 2*eta],
                                  [-eta/101, Q(0), eta/101]):
        if lm0*abs(e0) > 2*eta or not 0 <= lm0+dl <= 1:
            continue
        assert abs((lm0+dl)*(e0+de)) <= 5*eta
        count += 1
    return count


if __name__ == "__main__":
    counts = {
        "quadratic_local_quartic_aggregate": quadratic_checks(),
        "flat_curvature_signed_resource_equality": flat_curvature_resource_checks(),
        "rounding_complementarity_ledger": rounding_ledger_checks(),
    }
    for name, number in counts.items():
        print(f"PASS {name}: {number} exact cases")
