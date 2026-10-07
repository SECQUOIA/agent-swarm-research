"""Small independent exact-optimum and interruption checks for solver review."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import random
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import certified_grid as solver
from verify_certificate import verify_certificate


def exact_candidates(problem):
    """Complete candidate set for a two-dimensional continuous or mixed box QP.

    Continuous minima occur at a corner, an edge stationary point, or an
    interior stationary point. A singular interior stationary affine set
    reaches a box boundary at the same objective value. Integer coordinates
    can instead be enumerated on this deliberately tiny box.
    """
    A, b, bounds = problem.A, problem.b, problem.bounds
    if problem.integers:
        choices = [tuple(map(F, range(int(lo), int(hi) + 1)))
                   if i in problem.integers else (None,)
                   for i, (lo, hi) in enumerate(bounds)]
        candidates = []
        for state in product(*choices):
            if len(problem.integers) == 2:
                candidates.append(state)
                continue
            i = next(i for i in range(2) if i not in problem.integers)
            j = 1 - i
            lo, hi = bounds[i]
            values = [lo, hi]
            if A[i][i] > 0:
                values.append(max(lo, min(hi, -(b[i] + A[i][j] * state[j]) / A[i][i])))
            for value in values:
                point = list(state)
                point[i] = value
                candidates.append(tuple(point))
        return candidates
    candidates = list(product(*bounds))
    for i in range(2):
        j = 1 - i
        if not A[i][i]:
            continue
        for endpoint in bounds[j]:
            value = -(b[i] + A[i][j] * endpoint) / A[i][i]
            if bounds[i][0] <= value <= bounds[i][1]:
                point = [F(0), F(0)]
                point[i], point[j] = value, endpoint
                candidates.append(tuple(point))
    determinant = A[0][0] * A[1][1] - A[0][1] ** 2
    if determinant:
        point = ((-A[1][1] * b[0] + A[0][1] * b[1]) / determinant,
                 (A[0][1] * b[0] - A[0][0] * b[1]) / determinant)
        if problem.feasible(point):
            candidates.append(point)
    return candidates


def finite_optimum_comparisons():
    rng = random.Random(90210)
    completed_stages = 0
    for case in range(32):
        diagonal = [rng.randint(-3, 5) for _ in range(2)]
        coupling = rng.choice([-4, -3, -1, 1, 3, 4])
        A = [[diagonal[0], coupling], [coupling, diagonal[1]]]
        b = [F(rng.randint(-5, 5), 3) for _ in range(2)]
        integers = [i for i in range(2) if (case % 4) & (1 << i)]
        problem = solver.BoxQP(A, b, [(F(-3, 2), F(5, 2)), (-1, 2)],
                              integers, [(0, 1)], [], constant=F(2, 7))
        candidates = exact_candidates(problem)
        optimum = min(map(problem.value, candidates))
        minimizers = [point for point in candidates if problem.value(point) == optimum]
        certificate = solver.solve(problem, epsilon=F(1, 50), max_stages=4,
                                   time_limit=2, convex_presolve=False)
        assert F(certificate['lower']) <= optimum <= F(certificate['upper'])
        assert verify_certificate(certificate)['valid']
        for stage in certificate['stages']:
            retained = tuple(tuple(map(F, pair)) for pair in stage['next_bounds'])
            assert any(problem.feasible(point, retained) for point in minimizers)
        completed_stages += len(certificate['stages'])
    return {'exact_two_variable_instances': 32, 'completed_stages': completed_stages}


def interrupted_proofs():
    problem = solver.BoxQP([[2, -3], [-3, 2]], [0, 0], [(0, 1)] * 2,
                           [], [(0, 1)], [])
    original_polish = solver.polish
    calls = 0

    def interrupt_after_initial_starts(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls > 3:
            raise solver.BudgetExceeded('time_limit')
        return original_polish(*args, **kwargs)

    with patch.object(solver, 'polish', interrupt_after_initial_starts):
        certificate = solver.solve(problem, epsilon=0, max_stages=1,
                                   convex_presolve=False)
    assert calls == 4 and len(certificate['stages']) == 1
    assert verify_certificate(certificate)['valid']

    problem_with_initial_improvement = solver.BoxQP(
        [[2, -3], [-3, 2]], [-1, 0], [(0, 1)] * 2, [], [(0, 1)], [])
    calls = 0

    def interrupt_second_initial_start(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise solver.BudgetExceeded('time_limit')
        return original_polish(*args, **kwargs)

    with patch.object(solver, 'polish', interrupt_second_initial_start):
        certificate = solver.solve(problem_with_initial_improvement,
                                   epsilon=0, convex_presolve=False)
    assert certificate['status'] == 'time_limit'
    assert not certificate['stages']
    assert F(certificate['upper']) < problem_with_initial_improvement.value((F(0), F(0)))
    assert verify_certificate(certificate)['valid']

    original_grid = solver.coordinate_grid
    calls = 0

    def abort_first_trial(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise solver.BudgetExceeded('trial_grid_limit')
        return original_grid(*args, **kwargs)

    with patch.object(solver, 'coordinate_grid', abort_first_trial):
        certificate = solver.solve(problem, epsilon=F(1, 1000), max_stages=2,
                                   convex_presolve=False)
    assert len(certificate['stages']) == 1
    assert certificate['stages'][0]['trial'] == 3
    assert certificate['stages'][0]['restart']
    assert verify_certificate(certificate)['valid']
    return {'completed_dp_survives_polish_interruption': True,
            'initial_improvement_survives_interruption': True,
            'aborted_trial_consumes_attempt_and_restarts': True}


if __name__ == '__main__':
    print(finite_optimum_comparisons())
    print(interrupted_proofs())
