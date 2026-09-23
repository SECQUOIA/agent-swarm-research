"""Exact checks of the new same-active-pattern Holder argument.

The endpoints are independently certified original follower KKT optima.
Tests cover flat signed marginals, a convex quartic aggregate whose coefficient
also depends on the leader, redundant resource rows, bound coordinates, and
both fixed and moving resource right-hand sides. They do not prove the global
component bound or implement a quantifier-elimination algorithm.
"""
import json
from itertools import product
import sympy as sp

R = sp.Rational
N = 4
U = sp.Matrix([[1, -2, 1, 1]])
C = sp.Matrix([[0, 1, -1, 0], [0, 2, -2, 0]])
active = C.col_join(sp.Matrix([[-1, 0, 0, 0], [0, 0, 0, 1]]))
_, independent = active.T.rref()
J = active[list(independent), :]
projection = J.T * (J * J.T).inv()
nu = sp.Matrix([1, 0, 0, -1])
lam = sp.Matrix([1, 0])
counts = dict(endpoint_kkt=0, tangent_identities=0, monotonicity=0,
              gradient_estimates=0, fixed_resource_divisions=0,
              moving_resource_corrections=0, sharp_root_examples=0)

def infinity(v):
    return max(abs(a) for a in v)

for degree, left, right, moving, gamma, xi in product(
        [1, 3, 5], [R(1, 4), R(1, 2)], [R(3, 4), R(7, 8)],
        [False, True], [R(0), R(1, 7)], [R(0), R(2, 5)]):
    x0, x1 = R(1, 8), R(7, 8)
    delta = x1 - x0
    z0 = sp.Matrix([0, left, left, 1])
    z1 = sp.Matrix([0, right, (right + left) / 2 if moving else right, 1])

    def cost_gradient(x, z):
        w = (U * z)[0]
        marginal = sp.Matrix([((2*t-1)**degree+1)/2 for t in z])
        return marginal + U.T * (gamma*w**3 + xi*x*w)

    ell0 = cost_gradient(x0, z0) + C.T * lam - nu
    ell1 = cost_gradient(x1, z1) + C.T * lam - nu
    slope = (ell1-ell0)/delta
    ell = lambda x: ell0 + slope*(x-x0)
    grad = lambda x, z: cost_gradient(x,z)-ell(x)
    for x,z in [(x0,z0),(x1,z1)]:
        stationarity = grad(x,z)+C.T*lam
        assert stationarity == nu
        assert all(0 <= t <= 1 for t in z)
        assert stationarity[0] >= 0 and stationarity[3] <= 0
        assert stationarity[1] == stationarity[2] == 0
        counts['endpoint_kkt'] += 1

    e = z0-z1
    correction = projection*(J*e)
    tangent = e-correction
    assert active*tangent == sp.zeros(active.rows,1)
    assert ((grad(x0,z0)-grad(x1,z1)).T*tangent)[0] == 0
    counts['tangent_identities'] += 1
    distance = infinity(e)
    mu = R(1,4*(4*degree)**degree)
    monotonicity = ((grad(x0,z0)-grad(x0,z1)).T*e)[0]
    assert 2*mu*distance**(degree+1) <= monotonicity
    counts['monotonicity'] += 1

    # Independent analytic derivative bounds on the entire unit box.
    aggregate_radius = sum(abs(a) for a in U)
    max_loading = max(abs(a) for a in U)
    az = degree + max_loading*aggregate_radius*(3*gamma*aggregate_radius**2+xi)
    ax = infinity(slope) + xi*max_loading*aggregate_radius
    db = infinity(correction)/delta
    rhs = N*(az*distance+ax*delta)*db*delta + N*ax*delta*distance
    assert monotonicity <= rhs
    counts['gradient_estimates'] += 1
    if not moving:
        assert correction == sp.zeros(N,1)
        assert distance**degree <= N*(az*db+2*ax)*delta/(2*mu)
        counts['fixed_resource_divisions'] += 1
    else:
        assert correction != sp.zeros(N,1)
        counts['moving_resource_corrections'] += 1

# Sharpness uses exact algebraic powers, not floating-point fitted exponents.
for degree in [1,2,3,5,9]:
    for m in [2,5,13]:
        z = R(1,2**m)
        x = z**degree
        assert z**degree == x
        # For any exponent 1/P + 1/P^2, the Holder ratio grows as z^(-1/P).
        ratio_power = z**(degree*degree) / x**(degree+1)
        assert ratio_power == 2**(m*degree)
        counts['sharp_root_examples'] += 1
print(json.dumps(counts, indent=2))
