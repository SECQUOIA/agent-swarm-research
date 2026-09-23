"""Independent adversarial review of quadratic_solver.py.

Run: python code/bilevel_reopened/quadratic_review_checks.py
The comparator builds dense box-KKT LPs in (x,z) and enumerates active faces.
It does not call the solver's pattern enumeration, elimination, or clipping.
Numerical LP comparisons supplement, rather than replace, exact checks.
"""
from fractions import Fraction as F
from itertools import product
import json
import random
from unittest.mock import patch

import numpy as np
from scipy.optimize import linprog, minimize, OptimizeResult

from quadratic_solver import (Problem, Segment, optimize_path, optimize_aligned_rank_one, recover_segment,
                              solve_response_path, verify_path, verify_segment)


def dense_q(p):
    n, k = len(p.d), len(p.H)
    return [[(p.d[i] if i == j else F(0)) + sum(
        (p.U[i][a] * p.H[a][b] * p.U[j][b]
         for a in range(k) for b in range(k)), F(0))
             for j in range(n)] for i in range(n)]


def dense_kkt_check(p, segment):
    """Full-matrix arithmetic, independent of qmul and small-system solves."""
    q = dense_q(p)
    for x in {segment.lo, segment.hi, (segment.lo + segment.hi) / 2}:
        z = tuple(a + b*x for a, b in zip(segment.intercept, segment.slope))
        assert all(isinstance(v, F) for v in z)
        for i, zi in enumerate(z):
            gi = sum((q[i][j] * z[j] for j in range(len(z))), F(0)) + p.c[i] + p.C[i]*x
            assert 0 <= zi <= 1
            assert gi >= 0 if zi == 0 else gi <= 0 if zi == 1 else gi == 0


def dense_global_lp(p, ox, oz, constraints, oxx=0, oxz=None):
    """Enumerate dense KKT graph faces and optimize each with HiGHS LP."""
    n, q = len(p.d), np.asarray(dense_q(p), dtype=float)
    best = None
    oxz = (0,)*n if oxz is None else oxz
    def value(v):
        return (float(ox)*v[0] + np.asarray(oz, float)@v[1:]
                + float(oxx)*v[0]**2 + v[0]*(np.asarray(oxz, float)@v[1:]))
    for states in product((0, 1, 2), repeat=n):
        eq, beq, ub, bub = [], [], [], []
        bounds = [(float(p.lo), float(p.hi))] + [(0, 1)] * n
        for i, state in enumerate(states):
            row = [float(p.C[i]), *q[i]]
            if state == 1:
                eq.append(row)
                beq.append(-float(p.c[i]))
            else:
                bounds[i+1] = (0, 0) if state == 0 else (1, 1)
                sign = -1 if state == 0 else 1
                ub.append([sign*v for v in row])
                bub.append(-sign*float(p.c[i]))
        for cx, cz, rhs in constraints:
            ub.append([float(cx), *map(float, cz)])
            bub.append(float(rhs))
        def solve(cost):
            return linprog(cost, A_ub=ub or None, b_ub=bub or None,
                           A_eq=eq or None, b_eq=beq or None,
                           bounds=bounds, method="highs")
        result = solve([float(ox), *map(float, oz)])
        assert result.status in (0, 2), result.message
        if result.success:
            candidate = result.fun
            if oxx or any(oxz):
                # The dense KKT face is a line segment because the response
                # is unique. Find its endpoints with LP and fit the objective
                # from three independent evaluations along that segment.
                left, right = solve([1]+[0]*n), solve([-1]+[0]*n)
                assert left.success and right.success
                f0, f1 = value(left.x), value(right.x)
                fm = value((left.x+right.x)/2)
                qa = 2*(f0+f1-2*fm)
                qb = f1-f0-qa
                candidate = min(f0, f1)
                if qa > 1e-12:
                    t = -qb/(2*qa)
                    if 0 < t < 1:
                        candidate = min(candidate, value((1-t)*left.x+t*right.x))
            if best is None or candidate < best:
                best = candidate
    return best


def compare(p, ox, oz, constraints=()):
    path = solve_response_path(p)
    assert verify_path(p, path)
    for s in path:
        dense_kkt_check(p, s)
    exact = optimize_path(p, path, ox, oz, constraints)
    independent = dense_global_lp(p, ox, oz, constraints)
    assert (exact is None) == (independent is None)
    if exact is not None:
        assert abs(float(exact["objective"]) - independent) < 1e-7
        x, z = exact["x"], exact["z"]
        assert all(cx*x + sum((a*b for a, b in zip(cz, z)), F(0)) <= rhs
                   for cx, cz, rhs in constraints)
    # Direct SLSQP solves check responses at interior points, independently of
    # which dense KKT face the global LP comparison selected.
    if p.d:
        q = np.asarray(dense_q(p), dtype=float)
        for t in (F(1, 7), F(2, 5), F(6, 7)):
            x = p.lo + (p.hi-p.lo)*t
            s = next(s for s in path if s.lo <= x <= s.hi)
            z = np.asarray(s.response(x), float)
            c = np.asarray(p.c, float) + float(x)*np.asarray(p.C, float)
            result = minimize(lambda v: .5*v@q@v + c@v,
                              np.full(len(z), .5), jac=lambda v: q@v+c,
                              bounds=[(0, 1)]*len(z), method="SLSQP",
                              options={"ftol": 1e-13, "maxiter": 1000})
            assert result.success, result.message
            assert np.linalg.norm(z-result.x, np.inf) < 3e-6
    return path, exact


def exact_solution_check(p, answer, ox, oz, constraints=(), oxx=0, oxz=None):
    assert answer is not None
    x, z = answer["x"], answer["z"]
    oxz = (0,)*len(z) if oxz is None else oxz
    assert isinstance(x, F) and all(isinstance(v, F) for v in z)
    assert p.lo <= x <= p.hi
    q = dense_q(p)
    for i, zi in enumerate(z):
        gi = sum((q[i][j]*z[j] for j in range(len(z))), F(0)) + p.c[i] + p.C[i]*x
        assert 0 <= zi <= 1
        assert gi >= 0 if zi == 0 else gi <= 0 if zi == 1 else gi == 0
    assert all(cx*x + sum((a*b for a, b in zip(cz, z)), F(0)) <= rhs
               for cx, cz, rhs in constraints)
    value = ox*x + sum((a*b for a, b in zip(oz, z)), F(0)) + oxx*x*x
    value += x*sum((a*b for a, b in zip(oxz, z)), F(0))
    assert value == answer["objective"]


def quadratic_and_aligned_checks():
    # Hand-computed revenue optimum, interior quadratic minimum, concave
    # endpoint minimum, exact cancellation to a linear objective, and equality.
    p = Problem((1,), ((1,),), ((0,),), (-1,), (1,))
    path = solve_response_path(p)
    cases = [
        (0, (0,), 0, (-1,), (), F(1, 2), -F(1, 4)),
        (-F(2, 3), (0,), 1, (0,), (), F(1, 3), -F(1, 9)),
        (F(1, 2), (0,), -1, (0,), (), F(1), -F(1, 2)),
        (0, (0,), 1, (1,), (), F(0), F(0)),
        (0, (0,), 1, (-1,), ((0, (1,), F(3, 5)),
                             (0, (-1,), -F(3, 5))), F(2, 5), -F(2, 25)),
    ]
    for ox, oz, oxx, oxz, constraints, want_x, want_value in cases:
        for solve in (lambda: optimize_path(p, path, ox, oz, constraints,
                                           objective_xx=oxx, objective_xz=oxz),
                      lambda: optimize_aligned_rank_one(p, ox, oz, constraints,
                                                       objective_xx=oxx, objective_xz=oxz)):
            answer = solve()
            assert answer["x"] == want_x and answer["objective"] == want_value
            exact_solution_check(p, answer, ox, oz, constraints, oxx, oxz)

    rng = random.Random(81723)
    for trial in range(24):
        n = 1 + trial % 4
        u = tuple(rng.randint(-2, 2) for _ in range(n))
        h = F((-1, 0, 1)[trial % 3], 8*n)
        gamma = (F(1), F(3, 2), F(2, 3))[trial % 3]
        q = Problem(tuple(rng.randint(1, 3) for _ in range(n)),
                    tuple((ui,) for ui in u), ((h,),),
                    tuple(F(rng.randint(-3, 2), 2) for _ in range(n)),
                    tuple(gamma*ui for ui in u), -1, 2)
        ox, oxx = rng.randint(-2, 2), rng.randint(-2, 2)
        oz = tuple(rng.randint(-2, 2) for _ in range(n))
        oxz = tuple(rng.randint(-2, 2) for _ in range(n))
        constraints = tuple((rng.randint(-2, 2), tuple(rng.randint(-2, 2) for _ in range(n)),
                             F(rng.randint(-4, 5), 2)) for _ in range(2))
        answer = optimize_aligned_rank_one(q, ox, oz, constraints,
                                          objective_xx=oxx, objective_xz=oxz, gamma=gamma)
        reference = dense_global_lp(q, ox, oz, constraints, oxx, oxz)
        general = optimize_path(q, solve_response_path(q), ox, oz, constraints,
                                objective_xx=oxx, objective_xz=oxz)
        assert (answer is None) == (reference is None) == (general is None)
        if answer is not None:
            assert abs(float(answer["objective"])-reference) < 1e-7
            assert (answer["objective"], answer["x"]) == (general["objective"], general["x"])
            assert answer["response_intervals_visited"] <= 2*n+1
            assert answer["thresholds"] <= 2*n
            exact_solution_check(q, answer, ox, oz, constraints, oxx, oxz)

    # The complete sweep must not depend on NumPy/SciPy or floating range.
    # Include simultaneous events, zero loadings, a singleton domain, almost
    # singular negative coupling, and input beyond binary64's exponent range.
    special = [
        Problem((1, 1, 1), ((1,), (-1,), (0,)), ((-F(1, 8),),), (-1, 0, -F(1, 3)), (1, -1, 0), -2, 2),
        Problem((1,), ((0,),), ((-100,),), (-F(1, 3),), (0,), 2, 2),
        Problem((), (), ((-3,),), (), (), -1, 1),
        Problem((1,), ((1,),), ((-1+F(1, 10**60),),), (-F(1, 3),), (1,)),
        Problem((10**500,), ((1,),), ((1,),), (-F(10**500, 3),), (1,)),
    ]
    with patch("scipy.optimize.minimize", side_effect=AssertionError("Numerical solver called")):
        for q in special:
            answer = optimize_aligned_rank_one(q, 0, (0,)*len(q.d), objective_xz=(-1,)*len(q.d))
            exact_solution_check(q, answer, 0, (0,)*len(q.d), oxz=(-1,)*len(q.d))

    for call in (
        lambda: optimize_aligned_rank_one(p, 0, (0,), gamma=0),
        lambda: optimize_aligned_rank_one(p, 0, (0,), gamma=2),
        lambda: optimize_aligned_rank_one(p, 0, (0,), objective_xz=(0, 0)),
        lambda: optimize_path(p, path, 0, (0,), objective_xx=1.0),
    ):
        try:
            call()
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError("Invalid quadratic/sweep input accepted")
    return {"quadratic_hand_cases": len(cases), "quadratic_dense_face_comparisons": 24,
            "aligned_exact_boundary_cases": len(special)}


def run():
    counts = {"dense_lp_comparisons": 0, "random_seed": 260906}
    # Disconnected feasible leader set; its equality boundary is isolated.
    p = Problem((1, 1), ((), ()), (), (0, 1), (-1, -2))
    path, result = compare(p, -1, (0, 0), ((0, (1, -1), F(1, 4)),))
    assert result["x"] == 1
    assert set(result["feasible_intervals"]) == {(F(0), F(1, 4)), (F(3, 4), F(1))}
    _, result = compare(p, 3, (2, 7), ((0, (-1, 1), -F(1, 2)),))
    assert result["x"] == F(1, 2) and result["z"] == (F(1, 2), F(0))
    _, result = compare(p, 0, (0, 0), ((0, (1, 0), F(2, 5)),
                                      (0, (-1, 0), -F(2, 5))))
    assert result["x"] == F(2, 5)
    _, result = compare(p, 0, (0, 0), ((0, (0, 0), -1),))
    assert result is None
    counts["dense_lp_comparisons"] += 4

    # Upper feasibility is exact even on scales that numerical LP tolerances
    # cannot resolve. These cases use hand-computed responses, not HiGHS.
    tiny = F(1, 10**60)
    target = F(1, 3)
    narrow = ((0, (-1, 0), -target), (0, (1, 0), target+tiny))
    answer = optimize_path(p, path, -1, (0, 0), narrow)
    assert answer["x"] == target+tiny
    impossible = ((0, (-1, 0), -target-tiny), (0, (1, 0), target))
    assert optimize_path(p, path, 0, (0, 0), impossible) is None

    # Fixed leader domain at simultaneous clipping boundaries; persistent
    # zero gradients; empty follower; zero, redundant and indefinite ranks.
    special = [
        Problem((1, 1, 1), ((), (), ()), (), (0, -1, -F(1, 2)), (-2, 2, 0), 0, 0),
        Problem((1, 1, 1), ((), (), ()), (), (0, -1, -F(1, 2)), (-2, 2, 0), -1, 1),
        Problem((), (), (), (), (), -2, 3),
        Problem((2, 2), ((1,), (1,)), ((-F(1, 2),),), (-1, 0), (-1, 1)),
        Problem((2,), ((1, 0, 0),), ((0, 0, 0), (0, 2, 0), (0, 0, -3)), (-1,), (-1,)),
    ]
    for p2 in special:
        compare(p2, 1, (0,)*len(p2.d))
        counts["dense_lp_comparisons"] += 1

    rng = random.Random(counts["random_seed"])
    for trial in range(24):
        n, k = 2 + trial % 3, trial % 3
        u = tuple(tuple(F(rng.randint(-2, 2), 3) for _ in range(k)) for _ in range(n))
        # Indefinite H is allowed; large diagonal makes Q strictly dominant.
        h = tuple(tuple(F((-1 if trial % 2 else 1) if i == j else 0)
                        for j in range(k)) for i in range(k))
        p2 = Problem((4,)*n, u, h,
                     tuple(rng.randint(-7, 3) for _ in range(n)),
                     tuple(rng.randint(-6, 6) for _ in range(n)), -1, 2)
        constraints = tuple((rng.randint(-2, 2),
                             tuple(rng.randint(-2, 2) for _ in range(n)),
                             F(rng.randint(-4, 5), 2)) for _ in range(2))
        compare(p2, rng.randint(-2, 2), tuple(rng.randint(-3, 3) for _ in range(n)), constraints)
        counts["dense_lp_comparisons"] += 1

    # Corrupt a valid certificate, omit a whole interval, and break coverage.
    assert not verify_path(p, [path[0]])
    s = path[0]
    assert not verify_segment(p, Segment(s.lo, s.hi, (F(17), F(0)), s.slope, s.pattern))
    assert not verify_segment(p, Segment(-2, -1, s.intercept, s.slope, s.pattern))
    fractional = Problem((1,), ((),), (), (-F(1, 3),), (0,))
    try:
        forged = Segment(0, 1, (1/3,), (0,), (1,))
        assert not verify_segment(fractional, forged), "Rounded float accepted as exact certificate"
    except TypeError:
        pass

    # Force a failed numerical proposal. With exhaustive recovery disabled,
    # only an explicit error is acceptable; with it enabled, recover exactly.
    fake = OptimizeResult(x=np.array([0.0]))
    with patch("scipy.optimize.minimize", return_value=fake):
        try:
            recover_segment(fractional, F(1, 2), exhaustive_limit=0)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Uncertified numerical pattern returned")
        exact = recover_segment(fractional, F(1, 2), exhaustive_limit=1)
        assert exact.response(F(1, 2)) == (F(1, 3),)
    try:
        solve_response_path(p, max_segments=0)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Segment resource cap silently ignored")

    invalid = [
        lambda: Problem((1,), ((1,),), ((-1,),), (0,), (0,)),  # Q singular
        lambda: Problem((1,), ((1,),), ((-2,),), (0,), (0,)),  # Q negative
        lambda: Problem((1,), ((1, 2),), ((1, 1), (0, 1)), (0,), (0,)),
        lambda: Problem((1,), ((1,),), ((1,),), (0, 1), (0,)),
        lambda: Problem((1.0,), ((),), (), (0,), (0,)),
        lambda: optimize_path(p, path, 0, (0,)),
    ]
    for construct in invalid:
        try:
            construct()
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError("Invalid input accepted")
    counts.update(quadratic_and_aligned_checks())
    counts["status"] = "passed"
    return counts


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
