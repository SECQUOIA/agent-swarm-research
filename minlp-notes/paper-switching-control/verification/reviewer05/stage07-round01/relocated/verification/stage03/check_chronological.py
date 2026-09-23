"""Exact audit of the old witness and one strengthened chronological chamber."""
from pathlib import Path
from fractions import Fraction as Q
from random import Random
import json

from chronological_program import chronological_program, weighted_triple_relaxation
from general_reach_research import verify_relaxation_witness

HERE = Path(__file__).resolve().parent


def verify_certificate(program, cert):
    size, ub, eq, obj = program
    y = [Q(v) for v in cert['inequality_dual']]
    z = [Q(v) for v in cert['equality_dual']]
    assert len(y) == len(ub) == 4038 and len(z) == len(eq) == 64
    assert max(y) <= 0
    residual = [Q(obj.get(i, 0)) for i in range(size)]
    for values, (row, rhs) in zip(y, ub):
        for i, a in row.items():
            residual[i] -= values*a
    for values, (row, rhs) in zip(z, eq):
        for i, a in row.items():
            residual[i] -= values*a
    assert min(residual) >= 0
    bound = (sum(v*rhs for v, (_, rhs) in zip(y, ub))
             + sum(v*rhs for v, (_, rhs) in zip(z, eq)))
    assert bound == Q(13104, 125)
    x = [Q(v) for v in cert['primal']]
    assert len(x) == size and min(x) >= 0
    for row, rhs in ub:
        assert sum(a*x[i] for i, a in row.items()) <= rhs
    for row, rhs in eq:
        assert sum(a*x[i] for i, a in row.items()) == rhs
    assert sum(a*x[i] for i, a in obj.items()) == bound
    # The saved primal is uniform at all event allocations, a real trajectory.
    assert all(x[7+7*j+i] == x[6+7*j]/6 for j in range(64) for i in range(6))
    assert x[:6] == [Q(6, 5)]*6
    assert {x[6+7*j] for j in range(42)} == {Q(66, 25)}
    assert {x[6+7*j] for j in range(42, 64)} == {Q(546, 125)}
    return bound, sum(v != 0 for v in y) + sum(v != 0 for v in z)


def check_row_order_independence(order, cert, expected):
    """The same indexed dual must work after arbitrary builder-row reorderings."""
    size, ub, eq, obj = weighted_triple_relaxation()
    rng = Random(20260907)
    for name in ('reversed', 'shuffled'):
        permuted = []
        for rows in (ub, eq):
            # Also reverse sparse dictionary insertion order, and include an
            # explicit zero coefficient to exercise normalization of row keys.
            rows = [(dict(reversed(list(row.items()))), rhs) for row, rhs in rows]
            for row, _ in rows:
                absent = next(i for i in range(size) if i not in row)
                row[absent] = 0
            if name == 'reversed':
                rows.reverse()
            else:
                rng.shuffle(rows)
            permuted.append(rows)
        candidate = chronological_program(order, (size, *permuted, obj))
        assert candidate == expected, name
        # Check the unchanged saved dual, not a dual permuted with this input.
        assert verify_certificate(candidate, cert) == (Q(13104, 125), 254)
    print('Canonical rows and unchanged certificate pass reversed/shuffled input-row audits.')


def check():
    if not __debug__:
        raise RuntimeError('Run without -O')
    print(verify_relaxation_witness())
    old = [Q(v) for v in json.loads(
        (HERE.parent/'reference'/'general_reach_relaxation_witness.json').read_text()
    )['variables']]
    cert = json.loads((HERE/'chronological_chamber_certificate.json').read_text())
    order = sorted(range(64), key=lambda j: (old[6+7*j], j))
    assert cert['order'] == order
    violations = [(a, b, i, old[7+7*a+i]-old[7+7*b+i])
                  for ai, a in enumerate(order) for b in order[ai+1:]
                  for i in range(6) if old[7+7*a+i] > old[7+7*b+i]]
    program = chronological_program(order)
    bound, nonzero = verify_certificate(program, cert)
    check_row_order_independence(order, cert, program)
    print({'chronological_decreases': len(violations),
           'maximum_decrease': str(max(v[-1] for v in violations)),
           'new_chamber_constraints': 378, 'exact_chamber_minimum': str(bound),
           'nonzero_dual_rows': nonzero, 'uniform_primal': 'passed'})
    return bound


if __name__ == '__main__':
    check()
