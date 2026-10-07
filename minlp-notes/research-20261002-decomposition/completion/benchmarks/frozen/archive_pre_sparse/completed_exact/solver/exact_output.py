"""Finite rational-height recovery for general bounded rational box QP.

Exactness uses a feasible rational candidate and a replayable lower bound,
not a floating-point tolerance or an assumed growth constant. Capped runs
retain their certified approximation. See ../completion/exact-output.md.
"""

from fractions import Fraction as F
from math import lcm
from time import perf_counter

from certified_grid import BoxQP, Budget, BudgetExceeded, rational, solve


def rational_heights(problem):
    """Bounds for a rational optimizer and optimal value, including ties.

    Let D clear Q=A/2, b, constant, and original endpoints. In u=D*x,
    stationary equations on a minimum-dimensional optimal face have integer
    matrix D*A. Every nonsingular principal minor is bounded by the product
    of max(1, continuous row 1-norm). No refined endpoints enter this bound.
    """
    denominators = [problem.constant.denominator]
    denominators.extend(v.denominator for v in problem.b)
    denominators.extend((v / 2).denominator for row in problem.A for v in row)
    denominators.extend(v.denominator for pair in problem.bounds for v in pair)
    denominator = lcm(*denominators)
    continuous = [i for i, (lo, hi) in enumerate(problem.bounds)
                  if i not in problem.integers and lo < hi]
    determinant = 1
    for i in continuous:
        row_norm = sum(abs(denominator * problem.A[i][j]) for j in continuous)
        assert row_norm.denominator == 1
        determinant *= max(1, row_norm.numerator)
    coordinate = denominator * determinant
    return {"denominator": denominator, "stationary_det_bound": determinant,
            "coordinate": coordinate, "value": denominator * coordinate ** 2}


def _stationary_candidate(problem, point, heights, budget, max_pivots):
    """Recover one active-face stationary point; this is an untrusted proposal.

    Singular faces use an exact bounded linear-feasibility problem. The
    subsequent value-separation gate, not stationarity, establishes globality.
    """
    tau = F(1, 4 * len(point) * heights["coordinate"])
    candidate, free = list(point), []
    for i, (lo, hi) in enumerate(problem.bounds):
        if i in problem.integers or lo == hi:
            continue
        if point[i] - lo <= tau:
            candidate[i] = lo
        elif hi - point[i] <= tau:
            candidate[i] = hi
        else:
            free.append(i)
    fixed = [i for i in range(len(point)) if i not in free]
    if not free:
        return tuple(candidate)
    matrix = [[problem.A[i][j] for j in free] for i in free]
    rhs = [-problem.b[i] - sum((problem.A[i][j] * candidate[j] for j in fixed), F(0))
           for i in free]
    rows = [row[:] + [value] for row, value in zip(matrix, rhs)]
    pivots, rank = [], 0
    for column in range(len(free)):
        budget.check(force=True)
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [entry / divisor for entry in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][column]:
                multiple = rows[r][column]
                rows[r] = [entry - multiple * value
                           for entry, value in zip(rows[r], rows[rank])]
        pivots.append((rank, column))
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return None
    if rank == len(free):
        values = [F(0)] * len(free)
        for row, column in pivots:
            values[column] = rows[row][-1]
    else:
        from rational_optimization import solve_lp
        budget.check(force=True)
        result = solve_lp([F(0)] * len(free), A_eq=matrix, b_eq=rhs,
                          bounds=[problem.bounds[i] for i in free], max_pivots=max_pivots,
                          check=lambda: budget.check(force=True))
        budget.check(force=True)
        if result.status != "optimal":
            return None
        values = result.x
    for i, value in zip(free, values):
        candidate[i] = value
    candidate = tuple(candidate)
    return candidate if problem.feasible(candidate) else None


def _candidates(problem, point, heights, budget, max_pivots):
    # Each source is only a proposal. Even a wrong face or a bad reconstruction
    # cannot pass unless its feasible objective meets the global exact gate.
    yield "incumbent", point
    radius = F(1, 4 * heights["coordinate"] ** 2)
    recovered = tuple(x if i in problem.integers else x.limit_denominator(heights["coordinate"])
                      for i, x in enumerate(point))
    if all(abs(x - y) <= radius for x, y in zip(point, recovered)):
        yield "coordinate_reconstruction", recovered
    stationary = _stationary_candidate(problem, point, heights, budget, max_pivots)
    if stationary is not None:
        yield "face_stationarity", stationary


def solve_exact(problem, max_rounds=8, max_stages=256, time_limit=30.0,
                max_table_states=100000, initial_precision=4, max_pivots=10000,
                **grid_options):
    """Return exact optimum if proved, otherwise certified bounds and a limit.

    Each round starts from the original problem at accuracy 2**(-q), with q
    doubled after a certified round. Stage and wall-clock caps apply across
    all rounds. The grid engine has cooperative time checks; a single exact
    rational arithmetic operation or LP pivot may finish after the time cap.
    Safety holds for every rational box QP. Eventual recovery follows from
    the core unique-optimizer growth theorem when resource caps are removed;
    no unrestricted nonunique-set complexity claim is made.
    """
    if (type(max_rounds) is not int or max_rounds < 1
            or type(max_stages) is not int or max_stages < 0
            or type(initial_precision) is not int or initial_precision < 1
            or type(max_pivots) is not int or max_pivots < 0
            or time_limit < 0):
        raise ValueError("invalid exact-output resource limit")
    if "epsilon" in grid_options:
        raise ValueError("exact output chooses its accuracy; omit epsilon")
    budget = Budget(time_limit)
    heights = rational_heights(problem)
    result = {"schema": "certified-grid-qp-exact-v1", "problem": problem.to_dict(),
              "heights": {key: str(value) for key, value in heights.items()},
              "options": {"initial_precision": initial_precision,
                          "max_rounds": max_rounds, "max_stages": max_stages,
                          "max_pivots": max_pivots}, "rounds": [], "feasible_proposals": []}
    precision, attempted = initial_precision, 0
    lower, upper, point = None, None, None
    status, proof = "round_limit", None
    candidate_attempts = 0
    for round_number in range(max_rounds):
        remaining_time = max(0.0, time_limit - (perf_counter() - budget.started))
        round_options = dict(grid_options)
        if point is not None:
            round_options["warm_start"] = point
        certificate = solve(problem, epsilon=F(1, 2 ** precision),
                            max_stages=max_stages - attempted, time_limit=remaining_time,
                            max_table_states=max_table_states, **round_options)
        result["rounds"].append(certificate)
        attempted += certificate["stats"].get("attempted_stages", len(certificate["stages"]))
        bound = rational(certificate["lower"])
        value = rational(certificate["upper"])
        lower = bound if lower is None else max(lower, bound)
        if upper is None or value < upper:
            upper, point = value, tuple(map(rational, certificate["point"]))
        # Direct equality is already an exact proof, even at a resource limit.
        if lower == upper:
            proof = {"kind": "equal_bounds", "source": "incumbent",
                     "point": list(map(str, point)), "value": str(upper)}
            status = "exact"
            break
        try:
            budget.check(force=True)
            for source, candidate in _candidates(problem, point, heights, budget, max_pivots):
                candidate_attempts += 1
                if not problem.feasible(candidate):
                    continue
                candidate_value = problem.value(candidate)
                if candidate_value < upper:
                    result["feasible_proposals"].append(
                        {"after_round": round_number, "point": list(map(str, candidate))})
                    upper, point = candidate_value, candidate
                if (lower <= candidate_value <= upper
                        and candidate_value - lower < F(1, heights["value"] * candidate_value.denominator)):
                    proof = {"kind": "rational_value_separation", "source": source,
                             "point": list(map(str, candidate)), "value": str(candidate_value)}
                    upper, point, status = candidate_value, candidate, "exact"
                    break
        except BudgetExceeded:
            status = "time_limit"
            break
        if proof is not None:
            break
        if certificate["status"] != "certified":
            status = certificate["status"]
            break
        if attempted >= max_stages:
            status = "stage_limit"
            break
        precision *= 2
    if proof is not None:
        result["proof"] = proof
        lower = upper
    result.update(status=status, point=list(map(str, point)), lower=str(lower),
                  upper=str(upper), gap=str(upper - lower),
                  stats={"elapsed_seconds": perf_counter() - budget.started,
                         "attempted_stages": attempted,
                         "completed_stages": sum(len(c["stages"]) for c in result["rounds"]),
                         "completed_table_states": sum(c["stats"]["completed_table_states"]
                                                       for c in result["rounds"]),
                         "rounds": len(result["rounds"]),
                         "candidate_attempts": candidate_attempts})
    return result
