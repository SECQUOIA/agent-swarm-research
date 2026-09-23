"""Independent spot checks for stage 1; no manuscript implementation imported."""
from fractions import Fraction as F
from itertools import product
import sympy as s


def check_cyclic_decomposition():
    # Two source inputs, a nontrivial positive pool cycle, two products.
    # Pool equations are 4 qa - qb = 0, 5 qb - 3 qa = 4.
    qa, qb = F(4, 17), F(16, 17)
    flow = {('i0', 'a'): F(3), ('i1', 'b'): F(2),
            ('a', 'b'): F(3), ('b', 'a'): F(1),
            ('a', 'j0'): F(1), ('b', 'j0'): F(1),
            ('b', 'j1'): F(3)}
    quality = {'i0': F(0), 'i1': F(2), 'a': qa, 'b': qb}
    h0 = {'a': F(8, 17), 'b': F(5, 17), 'j0': F(1), 'j1': F(0)}
    h1 = {v: 1 - w for v, w in h0.items()}
    components = [{(u, v): f * h[v] for (u, v), f in flow.items()}
                  for h in (h0, h1)]
    for component in [flow] + components:
        for pool in ('a', 'b'):
            incoming = sum(f for (u, v), f in component.items() if v == pool)
            outgoing = sum(f for (u, v), f in component.items() if u == pool)
            mass = sum(quality[u] * f for (u, v), f in component.items() if v == pool)
            assert incoming == outgoing and mass == outgoing * quality[pool]
    assert all(components[0][e] + components[1][e] == flow[e] for e in flow)
    assert all(0 <= c[e] <= flow[e] for c in components for e in flow)
    assert components[0]['b', 'j1'] == components[1]['a', 'j0'] == 0
    assert components[1]['b', 'j0'] == 0
    # Algebraic closed circulation, then near-singular source-connected cycle.
    eps, lam = s.symbols('eps lam')
    matrix = s.Matrix([[1, -(1 - eps)], [-1, 1]])
    assert matrix.det() == eps
    assert s.simplify(matrix * s.Matrix([lam, lam]) - s.Matrix([eps * lam, 0])) == s.zeros(2, 1)
    assert s.simplify(matrix * s.Matrix([lam + 1, lam + 1]) - s.Matrix([eps * lam, 0])) == s.Matrix([eps, 0])
    assert matrix.subs(eps, 0).rank() == 1


def check_gadgets():
    # Both endpoint inputs and interior inputs; reciprocal emission and flip.
    vals = [F(1, 2), F(2, 3), F(1), F(3, 2), F(2)]
    for a in vals:
        B = 7
        outlet = 1 / a
        assert a / B * outlet == F(1, B)
        assert outlet + (2 - outlet) == 2
        assert 0 <= 2 - outlet <= 2
        assert (2 - (2 - outlet)) == outlet
        assert B - 2 * outlet >= 3
    # Addition and inversion identities, including identical inversion names.
    count = 0
    for x, y in product(vals, repeat=2):
        if x * y == 1:
            by = F(5, 2) - y
            assert x * (F(5, 2) - by) == 1
            t1, t2 = y, 1 / y
            assert x * t1 == t1 * t2 == y * t2 == 1
            count += 1
        z = x + y
        if F(1, 2) <= z <= 2:
            bz = F(5, 2) - z
            assert (F(5, 2) - x - y) / bz == 1
            tau = 2 / z
            assert z * tau == (x + y) * tau == 2
            assert 1 <= tau <= 2
            count += 1
    assert count > 10


def check_faces_and_conic_example():
    # C=[0,1], nonface F=[1/3,2/3], all capacities one.
    # A feasible mixed unit has cost -1; integral feasible flows all cost zero.
    y0 = y1 = F(1, 2)
    assert F(1, 3) <= y1 / (y0 + y1) <= F(2, 3)
    integral_costs = []
    for a, b, v in product((0, 1), repeat=3):
        if a + b == v and F(1, 3) * v <= b <= F(2, 3) * v:
            integral_costs.append(-a-b)
    assert integral_costs == [0] and -y0-y1 == -1
    # Pure endpoints: one physical pool cannot simultaneously serve both.
    assert not any(q == 0 and q == 1 for q in (F(0), F(1)))
    # Sum of the two pure unit solutions has legal margins but total delivery 2.
    assert sum((1, 1)) == 2


def check_basis_and_irrational_example():
    eta = s.symbols('eta')
    C = s.Matrix([[eta, 1], [1, eta + 1]])
    d = s.Matrix([1, 2])
    Delta, U = C.det(), C.adjugate() * d
    A, b = s.Matrix([[2, -1]]), 3
    verifier = ((A * U)[0] - b * Delta) * Delta
    original = (A * (C.inv() * d))[0] - b
    assert s.simplify(verifier - original * Delta**2) == 0
    for e in [-3, -1, 0, 1, 3]:
        if Delta.subs(eta, e) != 0:
            assert bool(verifier.subs(eta, e) <= 0) == bool(original.subs(eta, e) <= 0)
    t0 = (1 + s.sqrt(3)) / 2
    h = lambda t: t / (t - 1) - 2*t
    assert s.simplify(h(t0) - 1) == 0
    a, bflow = 1, (s.sqrt(3)-1)/2
    assert s.simplify(2*bflow**2 + 2*bflow - 1) == 0
    assert s.simplify(3*a + bflow - (5+s.sqrt(3))/2) == 0


for check in (check_cyclic_decomposition, check_gadgets,
              check_faces_and_conic_example, check_basis_and_irrational_example):
    check()
    print(check.__name__ + ': PASS')
