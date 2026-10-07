"""Certified affine convex recourse and an original-model solve pipeline.

Recognition solves one central convex box QP and one rational LP. The
bounded reference backends may return resource_limit; successful selectors
are accepted only after exact whole-box KKT checks. Candidate discovery is
a heuristic, never a completeness or width guarantee.
"""

from __future__ import annotations

from fractions import Fraction as F
from time import perf_counter

from certified_grid import BoxQP, BudgetExceeded, rational, solve


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def _psd(matrix):
    a = [list(row) for row in matrix]
    for k in range(len(a)):
        if a[k][k] < 0 or (not a[k][k] and any(a[i][k] for i in range(k + 1, len(a)))):
            return False
        if a[k][k]:
            for i in range(k + 1, len(a)):
                for j in range(i, len(a)):
                    a[i][j] -= a[i][k] * a[k][j] / a[k][k]
                    a[j][i] = a[i][j]
    return True


def _range(a, row, bounds):
    return (a + sum((b * (lo if b >= 0 else hi) for b, (lo, hi) in zip(row, bounds)), F(0)),
            a + sum((b * (hi if b >= 0 else lo) for b, (lo, hi) in zip(row, bounds)), F(0)))


def _indices(problem, private):
    private = tuple(private)
    if (len(set(private)) != len(private) or not private
            or any(type(i) is not int or i < 0 or i >= len(problem.b) for i in private)):
        raise ValueError("private indices must be distinct valid coordinates")
    if any(i in problem.integers for i in private):
        raise ValueError("convex private coordinates must be continuous")
    return private, tuple(i for i in range(len(problem.b)) if i not in private)


def recognize_affine(problem, private, max_pivots=10000, max_faces=10000, check=None):
    """Recognize a globally affine private optimizer, including singular PSD.

    Fixed coordinates must first be substituted (the pipeline does this).
    A no_affine_selector result requires certified LP infeasibility. A
    resource_limit result makes no assertion about existence.
    """
    from rational_optimization import (solve_lp, solve_convex_box_qp,
                                       verify_lp_result, verify_convex_box_qp_result)
    private, retained = _indices(problem, private)
    if any(lo == hi for lo, hi in problem.bounds):
        raise ValueError("substitute fixed coordinates before affine recognition")
    attachments = tuple(j for j in retained if any(problem.A[i][j] for i in private))
    C = [[problem.A[i][j] for j in private] for i in private]
    if not _psd(C):
        return {"status": "nonconvex_private_block"}
    D = [[problem.A[i][j] for j in attachments] for i in private]
    center = [(problem.bounds[j][0] + problem.bounds[j][1]) / 2 for j in attachments]
    radius = [(problem.bounds[j][1] - problem.bounds[j][0]) / 2 for j in attachments]
    h = [problem.b[i] + _dot(row, center) for i, row in zip(private, D)]
    ybounds = [problem.bounds[i] for i in private]
    central = solve_convex_box_qp(C, h, ybounds, max_faces=max_faces, max_pivots=max_pivots, check=check)
    if central.status != "optimal":
        return {"status": "resource_limit", "reason": central.reason}
    if not verify_convex_box_qp_result(C, h, ybounds, central):
        raise ArithmeticError("central convex QP certificate failed")
    gradient = [_dot(row, central.x) + b for row, b in zip(C, h)]
    r, k = len(private), len(attachments)
    # Variables a, B, |B|, |CB+D|; parameters are centered.
    count = r + 3 * r * k
    bi = lambda i, j: r + i * k + j
    vi = lambda i, j: r + r * k + i * k + j
    si = lambda i, j: r + 2 * r * k + i * k + j
    inequalities, rhs, equalities, erhs = [], [], [], []

    def row(entries):
        values = [F(0)] * count
        for pos, value in entries:
            values[pos] += value
        return values

    def le(entries, bound):
        inequalities.append(row(entries)); rhs.append(bound)

    def eq(entries, bound):
        equalities.append(row(entries)); erhs.append(bound)

    for i, (lo, hi) in enumerate(ybounds):
        if check:
            check()
        for j in range(k):
            le([(bi(i, j), 1), (vi(i, j), -1)], 0)
            le([(bi(i, j), -1), (vi(i, j), -1)], 0)
        le([(i, 1)] + [(vi(i, j), radius[j]) for j in range(k)], hi)
        le([(i, -1)] + [(vi(i, j), radius[j]) for j in range(k)], -lo)
        if not gradient[i]:
            eq([(t, C[i][t]) for t in range(r)], -h[i])
            for j in range(k):
                eq([(bi(t, j), C[i][t]) for t in range(r)], -D[i][j])
        else:
            eq([(i, 1)], lo if gradient[i] > 0 else hi)
            for j in range(k):
                eq([(bi(i, j), 1)], 0)
                le([(bi(t, j), C[i][t]) for t in range(r)] + [(si(i, j), -1)], -D[i][j])
                le([(bi(t, j), -C[i][t]) for t in range(r)] + [(si(i, j), -1)], D[i][j])
            sign = 1 if gradient[i] > 0 else -1
            le([(t, -sign * C[i][t]) for t in range(r)]
               + [(si(i, j), radius[j]) for j in range(k)], sign * h[i])
    objective = [F(0)] * count
    lp = solve_lp(objective, A_ub=inequalities, b_ub=rhs,
                  A_eq=equalities, b_eq=erhs, max_pivots=max_pivots, check=check)
    if lp.status not in ("optimal", "infeasible"):
        return {"status": "resource_limit", "reason": lp.reason}
    if not verify_lp_result(objective, lp, A_ub=inequalities, b_ub=rhs,
                            A_eq=equalities, b_eq=erhs):
        raise ArithmeticError("selector LP certificate failed")
    if lp.status == "infeasible":
        return {"status": "no_affine_selector"}
    B = [[lp.x[bi(i, j)] for j in range(k)] for i in range(r)]
    a = [lp.x[i] - _dot(B[i], center) for i in range(r)]
    proof = {"kind": "affine", "private": list(private), "attachments": list(attachments),
             "a": list(map(str, a)), "B": [list(map(str, row)) for row in B]}
    from verify_recourse import verify_selector
    verify_selector(problem, proof)
    return {"status": "affine", "proof": proof,
            "central_faces": getattr(central, "faces", None), "lp_pivots": lp.pivots}


def _decomposition(A):
    """Use the solver's discovered decomposition, or a valid single bag."""
    try:
        from decomposition import build_decomposition
    except ImportError:
        return [list(range(len(A)))], []
    scopes = [(i,) for i in range(len(A))] + [
        (i, j) for i in range(len(A)) for j in range(i + 1, len(A)) if A[i][j]]
    result = build_decomposition(len(A), scopes)
    return result["bags"], result["edges"]


def transform(problem, proof):
    """Substitute a checked affine response; callers verify it before use."""
    private = tuple(proof["private"])
    retained = tuple(i for i in range(len(problem.b)) if i not in private)
    positions = {i: j for j, i in enumerate(retained)}
    n, m = len(problem.b), len(retained)
    offset = [F(0)] * n
    matrix = [[F(0)] * m for _ in range(n)]
    for j, i in enumerate(retained):
        matrix[i][j] = F(1)
    for i, a, row in zip(private, proof["a"], proof["B"]):
        offset[i] = rational(a)
        for j, value in zip(proof["attachments"], row):
            matrix[i][positions[j]] = rational(value)
    h_times_map = [[sum((problem.A[i][t] * matrix[t][k] for t in range(n)), F(0))
                    for k in range(m)] for i in range(n)]
    A = [[sum((matrix[i][j] * h_times_map[i][k] for i in range(n)), F(0))
          for k in range(m)] for j in range(m)]
    gradient = [problem.b[i] + _dot(problem.A[i], offset) for i in range(n)]
    b = [sum((matrix[i][j] * gradient[i] for i in range(n)), F(0)) for j in range(m)]
    constant = problem.value(offset)
    if not m:
        return None, constant
    bags, edges = _decomposition(A)
    reduced = BoxQP(A, b, [problem.bounds[i] for i in retained],
                    [positions[i] for i in retained if i in problem.integers],
                    bags, edges, constant, name=problem.name + ":recourse")
    return reduced, constant


def lift(problem, proof, reduced_point):
    private = tuple(proof["private"])
    retained = tuple(i for i in range(len(problem.b)) if i not in private)
    point = [F(0)] * len(problem.b)
    for i, x in zip(retained, reduced_point):
        point[i] = rational(x)
    for i, a, row in zip(private, proof["a"], proof["B"]):
        point[i] = rational(a) + sum((rational(b) * point[j]
                    for j, b in zip(proof["attachments"], row)), F(0))
    return tuple(point)


def discover_candidates(problem, max_block_size=12):
    """Try continuous nonnegative-diagonal components, leaf bags and scalars."""
    eligible = {i for i in range(len(problem.b))
                if i not in problem.integers and problem.A[i][i] >= 0
                and problem.bounds[i][0] < problem.bounds[i][1]}
    candidates = set()
    unseen = set(eligible)
    while unseen:
        pending = [min(unseen)]; unseen.remove(pending[0])
        for i in pending:
            new = sorted(j for j in unseen if problem.A[i][j])
            unseen.difference_update(new); pending.extend(new)
        if len(pending) <= max_block_size:
            candidates.add(tuple(sorted(pending)))
        # A component may contain its own (nonconvex) attachment variable.
        # Removing one candidate attachment discovers useful private blocks
        # even when a valid supplied decomposition consists of a single bag.
        if 1 < len(pending) <= max_block_size + 1:
            candidates.update(tuple(sorted(set(pending) - {i})) for i in pending)
    for t, bag in enumerate(problem.bags):
        if len(problem.neighbors[t]) == 1:
            neighbor = problem.bags[problem.neighbors[t][0]]
            private = set(bag) - set(neighbor)
            if private and private <= eligible and len(private) <= max_block_size:
                candidates.add(tuple(sorted(private)))
    candidates.update((i,) for i in eligible)
    return sorted(candidates, key=lambda x: (-len(x), x))


def discover_convex_blocks(problem, max_block_size=12):
    """Choose PSD private blocks with no cross-block interactions.

    This bounded-size structural heuristic supplies candidates for conditional
    convex value search. Its output is checked again by that backend.
    """
    blocks, used = [], set()
    for block in discover_candidates(problem, max_block_size):
        if used.intersection(block) or any(problem.A[i][j] for i in block for j in used):
            continue
        if _psd([[problem.A[i][j] for j in block] for i in block]):
            blocks.append(block)
            used.update(block)
    return blocks


def solve_with_recourse(problem, epsilon=F(1, 1000), blocks=None, discover=True,
                        backend="auto", exact=False, max_block_size=12,
                        max_candidates=32, max_pivots=10000, max_faces=10000,
                        max_core=4, max_queries=10000, max_cuts=100, **solve_options):
    """Preprocess, solve the reduced problem, and lift a bound to the original.

    Supplied blocks use ORIGINAL coordinate indices and are checked exactly.
    Rejected candidates remain in the model. All limits are explicit; selector
    simplex/face budgets are operation caps, not wall-clock guarantees.
    """
    if backend not in ("auto", "grid", "mincut", "convex", "submodular"):
        raise ValueError("unknown recourse backend")
    epsilon = rational(epsilon)
    if type(exact) is not bool or type(discover) is not bool:
        raise ValueError("exact and discover must be Boolean")
    if epsilon < 0 or any(type(v) is not int or v < 0 for v in
                         (max_block_size, max_candidates, max_pivots, max_faces, max_core, max_queries, max_cuts)) or max_queries < 1:
        raise ValueError("invalid tolerance or recourse budget")
    started = perf_counter()
    time_limit = solve_options.get("time_limit", 10.0)
    if time_limit < 0:
        raise ValueError("negative time limit")

    def check():
        if perf_counter() - started >= time_limit:
            raise BudgetExceeded("time_limit")

    current, labels, history, attempts = problem, list(range(len(problem.b))), [], []
    fixed = [i for i, (lo, hi) in enumerate(current.bounds) if lo == hi]
    if fixed:
        proof = {"kind": "fixed", "private": fixed, "attachments": [],
                 "a": [str(current.bounds[i][0]) for i in fixed], "B": [[] for _ in fixed]}
        history.append((current, proof))
        current, constant = transform(current, proof)
        labels = [i for i in labels if i not in fixed]
    supplied = [tuple(block) for block in (blocks or ())]
    if any(len(set(block)) != len(block) or any(type(i) is not int or not 0 <= i < len(problem.b) for i in block)
           for block in supplied):
        raise ValueError("invalid supplied private block")
    requested_blocks = tuple(supplied)
    count = 0
    while backend != "convex" and current is not None and count < max_candidates:
        candidates = []
        while supplied:
            block = supplied.pop(0)
            mapped = tuple(labels.index(i) for i in block if i in labels)
            if mapped:
                candidates.append(mapped)
                break
        if not candidates and discover:
            candidates = discover_candidates(current, max_block_size)
        if not candidates:
            break
        accepted = False
        for private in candidates:
            if count >= max_candidates:
                break
            count += 1
            if len(private) > max_block_size:
                attempts.append({"private": [labels[i] for i in private], "status": "block_size_limit"})
                continue
            try:
                result = recognize_affine(current, private, max_pivots=max_pivots,
                                          max_faces=max_faces, check=check)
            except BudgetExceeded:
                result = {"status": "resource_limit"}
                count = max_candidates
            attempts.append({"private": [labels[i] for i in private], "status": result["status"]})
            if result["status"] == "affine":
                history.append((current, result["proof"]))
                current, constant = transform(current, result["proof"])
                labels = [label for i, label in enumerate(labels) if i not in private]
                accepted = True
                break
        if not accepted and not supplied:
            break
    inner = None
    if current is None:
        point, lower, upper, status, method = (), constant, constant, "exact", "constant"
    else:
        if backend == "convex":
            from convex_recourse import solve_convex_recourse
            conditional_blocks = ([tuple(labels.index(i) for i in block if i in labels)
                                   for block in requested_blocks] if blocks is not None else
                                  discover_convex_blocks(current, max_block_size))
            conditional_blocks = [block for block in conditional_blocks if block]
            inner = solve_convex_recourse(current, conditional_blocks, epsilon=epsilon,
                        exact=exact, max_levels=solve_options.get("max_stages", 24),
                        max_table_states=solve_options.get("max_table_states", 100000),
                        max_faces=max_faces, max_pivots=max_pivots,
                        time_limit=max(0.0, time_limit - (perf_counter() - started)))
            method = "convex"
        if backend == "submodular" or (backend == "auto" and any(current.A[i][i] > 0
                                                                  for i in range(len(current.b)))):
            from submodular_recourse import solve_submodular
            try:
                check()
                inner = solve_submodular(current, epsilon=epsilon, exact=exact,
                            max_queries=max_queries, max_faces=max_faces, max_cuts=max_cuts,
                            max_pivots=max_pivots, check=check)
                if inner["status"] == "unsupported":
                    inner = None
                else:
                    method = "submodular"
            except BudgetExceeded:
                inner = None
        if inner is None and backend in ("auto", "mincut") and (epsilon > 0 or exact):
            from mincut_adapter import solve_mincut
            try:
                check()
                inner = solve_mincut(current, epsilon=epsilon, max_core=max_core,
                                     max_queries=max_queries,
                                     max_levels=solve_options.get("max_stages", 12), exact=exact,
                                     check=check)
                if inner["status"] == "unsupported":
                    inner = None
                else:
                    method = "mincut"
            except BudgetExceeded:
                inner = None
        if inner is None:
            solve_options["time_limit"] = max(0.0, time_limit - (perf_counter() - started))
            if exact:
                from exact_output import solve_exact
                inner = solve_exact(current, **solve_options)
            else:
                inner = solve(current, epsilon=epsilon, **solve_options)
            method = "grid"
        point = tuple(map(rational, inner["point"]))
        lower, upper, status = rational(inner["lower"]), rational(inner["upper"]), inner["status"]
    for before, proof in reversed(history):
        point = lift(before, proof, point)
    if not problem.feasible(point) or problem.value(point) != upper:
        raise ArithmeticError("recourse lift is inconsistent with original model")
    return {"schema": "recourse-qp-v1", "problem": problem.to_dict(),
            "epsilon": str(epsilon), "exact_requested": bool(exact),
            "steps": [proof for _, proof in history], "method": method, "inner": inner,
            "point": list(map(str, point)), "lower": str(lower), "upper": str(upper),
            "gap": str(upper - lower), "status": status,
            "stats": {"elapsed_seconds": perf_counter() - started,
                      "removed_coordinates": len(problem.b) - len(labels),
                      "remaining_coordinates": len(labels), "attempts": attempts}}


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epsilon", default="1/1000")
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--backend", choices=("auto", "grid", "mincut", "convex", "submodular"), default="auto")
    parser.add_argument("--time-limit", type=float, default=10.0)
    parser.add_argument("--max-stages", type=int, default=24)
    parser.add_argument("--max-table-states", type=int, default=100000)
    parser.add_argument("--max-candidates", type=int, default=32)
    parser.add_argument("--max-core", type=int, default=4)
    parser.add_argument("--max-queries", type=int, default=10000)
    args = parser.parse_args()
    problem = BoxQP.from_dict(json.loads(args.problem.read_text()))
    result = solve_with_recourse(problem, epsilon=args.epsilon, exact=args.exact,
            backend=args.backend, time_limit=args.time_limit, max_stages=args.max_stages,
            max_table_states=args.max_table_states, max_candidates=args.max_candidates,
            max_core=args.max_core, max_queries=args.max_queries)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "lower", "upper", "gap", "stats")}))


if __name__ == "__main__":
    main()
