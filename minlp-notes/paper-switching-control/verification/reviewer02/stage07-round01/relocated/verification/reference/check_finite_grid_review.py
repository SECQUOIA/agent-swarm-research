"""Independent finite-grid review using the original cumulative-error definition.

Run normally (not python -O). MILP upper bounds below are numerical cross-checks;
all reported theorem LP bounds are separately checked with Fraction arithmetic.
The MILP never uses the author's cutoff regions or schedule identity.
"""
from fractions import Fraction as F
from itertools import permutations
import argparse
import importlib.util
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

SPEC = importlib.util.spec_from_file_location(
    "author_finite_grid", Path(__file__).with_name("finite_grid_research.py"))
author = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(author)
FORMULA_SPEC = importlib.util.spec_from_file_location(
    "author_minimax", Path(__file__).with_name("minimax.py"))
formula = importlib.util.module_from_spec(FORMULA_SPEC)
FORMULA_SPEC.loader.exec_module(formula)


def original_schedules(n, N):
    """All distinct grid schedules with at most one switch, including constants."""
    for p in range(n):
        yield (p,) * N
    for p, q in permutations(range(n), 2):
        for k in range(1, N):
            yield (p,) * k + (q,) * (N - k)


def original_error(matrix, grid):
    """Compute max absolute cumulative error directly, all coordinates/times."""
    n, N = len(matrix), len(grid) - 1
    assert all(len(row) == N for row in matrix)
    assert all(x >= 0 for row in matrix for x in row)
    assert all(sum(matrix[i][k] for i in range(n)) == 1 for k in range(N))
    best = grid[-1]
    best_schedule = None
    for schedule in original_schedules(n, N):
        cumulative = [F(0)] * n
        value = F(0)
        for k, mode in enumerate(schedule):
            dt = grid[k + 1] - grid[k]
            for i in range(n):
                cumulative[i] += (F(i == mode) - matrix[i][k]) * dt
                value = max(value, abs(cumulative[i]))
        if value <= best:
            best, best_schedule = value, schedule
    return best, best_schedule


def original_minimax_milp(n, grid):
    """Direct max_alpha min_schedule max_coordinate,time |integer - relaxed|.

    beta[i,k] are relaxed *increments*, with sum_i beta[i,k] = dt_k.
    Each schedule has one disjunction selecting any original signed error.
    Only switch and terminal times need be used: on each fixed-mode segment,
    each coordinate's cumulative discrepancy is monotone.
    """
    N, T = len(grid) - 1, float(grid[-1])
    continuous = n * N + 1
    e_index = continuous - 1
    forms = []
    for schedule in original_schedules(n, N):
        knot_indices = [k for k in range(1, N) if schedule[k] != schedule[k - 1]] + [N]
        schedule_forms = []
        for k in knot_indices:
            integer = [sum(grid[j + 1] - grid[j] for j in range(k)
                           if schedule[j] == i) for i in range(n)]
            for i in range(n):
                for sign in [-1, 1]:
                    # sign * (integer - relaxed). Discard terms <=0 everywhere.
                    if sign == 1 and integer[i] == 0:
                        continue
                    if sign == -1 and integer[i] == grid[k]:
                        continue
                    schedule_forms.append((i, k, sign, float(sign * integer[i])))
        forms.append(schedule_forms)
    binaries = sum(map(len, forms))
    count = continuous + binaries
    rows = N + (n - 1) + len(forms) + binaries
    matrix = lil_matrix((rows, count), dtype=float)
    lower, upper = np.full(rows, -np.inf), np.full(rows, np.inf)
    r = 0
    for k in range(N):
        for i in range(n):
            matrix[r, i * N + k] = 1
        lower[r] = upper[r] = float(grid[k + 1] - grid[k])
        r += 1
    # Relabeling mode totals loses no adversarial input and reduces symmetry.
    for i in range(n - 1):
        for k in range(N):
            matrix[r, i * N + k] = 1
            matrix[r, (i + 1) * N + k] = -1
        lower[r] = 0
        r += 1
    z = continuous
    for schedule_forms in forms:
        matrix[r, z:z + len(schedule_forms)] = 1
        lower[r] = upper[r] = 1
        r += 1
        for i, k, sign, constant in schedule_forms:
            # E <= sign*(S-A) + 2*T*(1-z).
            matrix[r, e_index] = 1
            for j in range(k):
                matrix[r, i * N + j] = sign
            matrix[r, z] = 2 * T
            upper[r] = constant + 2 * T
            r += 1
            z += 1
    c = np.zeros(count)
    c[e_index] = -1
    bounds_upper = np.ones(count)
    bounds_upper[:continuous] = T
    integrality = np.zeros(count)
    integrality[continuous:] = 1
    result = milp(c, integrality=integrality,
                  bounds=Bounds(np.zeros(count), bounds_upper),
                  constraints=LinearConstraint(matrix.tocsr(), lower, upper),
                  options={"time_limit": 60, "mip_rel_gap": 0, "presolve": False})
    assert result.success, result.message
    return -result.fun, -result.mip_dual_bound


def independently_check_region(n, grid, a, b, kind, x):
    """Verify explicit theorem constraints without the author's row builder."""
    u, v, m, error = x[:3], x[3:6], x[6:9], x[9]
    weight = [1, 1, n - 2]
    T, ta, tb = grid[-1], grid[a], grid[b]
    assert all(0 <= uj <= vj <= mj for uj, vj, mj in zip(u, v, m))
    assert sum(w * y for w, y in zip(weight, u)) == ta
    assert sum(w * y for w, y in zip(weight, v)) == tb
    assert sum(w * y for w, y in zip(weight, m)) == T
    assert m[0] >= m[1] >= m[2]
    assert error >= T / 3
    assert T - ta <= error + m[0] <= T - grid[a - 1]
    assert T - tb <= error + m[1] <= T - grid[b - 1]
    assert u[1] + error <= ta and v[0] + error <= tb
    assert u[2] + error <= ta if kind == "low" else m[1] >= error


def independently_reconstruct(n, grid, a, b, x):
    """Expand all endpoint states, then interpolate each original grid cell."""
    states = {F(0): [F(0)] * n}
    for time, block in [(grid[a], x[:3]), (grid[b], x[3:6]), (grid[-1], x[6:9])]:
        value = block[:2] + [block[2]] * (n - 2)
        if time in states:
            assert states[time] == value
        states[time] = value
    times = sorted(states)
    result = [[] for _ in range(n)]
    for left, right in zip(grid, grid[1:]):
        start = max(t for t in times if t <= left)
        end = min(t for t in times if t >= right)
        assert end > start
        for i in range(n):
            result[i].append((states[end][i] - states[start][i]) / (end - start))
    return result


def audit_regions(n, grid):
    """Each author-certified primal must be a valid original adversarial control."""
    best, winner = formula.minimax(n, grid)
    a, b, kind, x = winner
    independently_check_region(n, grid, a, b, kind, x)
    formula_matrix = independently_reconstruct(n, grid, a, b, x)
    assert original_error(formula_matrix, grid)[0] == best
    feasible = empty = ties = degenerate = 0
    N = len(grid) - 1
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            for kind in ["low", "high"]:
                data = author.region(n, grid, a, b, kind)
                solution = author.solve_certified(data, 9)
                if solution is None:
                    empty += 1
                    # Author's universal certificate covers these too.
                    assert author.certify_region_upper(data, best)
                    continue
                feasible += 1
                error, x = solution
                assert error <= best
                independently_check_region(n, grid, a, b, kind, x)
                matrix = independently_reconstruct(n, grid, a, b, x)
                original, _ = original_error(matrix, grid)
                assert original >= error
                if error == best:
                    assert original == best
                assert matrix == author.witness_matrix(n, grid, (a, b, kind, x))
                assert original == author.exact_schedule_error(matrix, grid)
                ties += int(x[9] + x[6] in [grid[-1] - grid[a], grid[-1] - grid[a - 1]]
                            or x[9] + x[7] in [grid[-1] - grid[b], grid[-1] - grid[b - 1]])
                degenerate += int(a == b or b == N)
    print(f"n={n}, grid={[str(t) for t in grid]}, value={best}; "
          f"feasible={feasible}, numerically empty={empty}, ties={ties}, "
          f"degenerate={degenerate}, returned witness={winner is not None}")
    return best


def check_formula_random_controls():
    """Original objective comparison on rational data, ties and zero allocations."""
    import random
    rng = random.Random(20260907)
    count = 0
    for n in range(3, 7):
        for N in range(1, 6):
            for _ in range(5):
                grid = [F(0)]
                for k in range(N):
                    grid.append(grid[-1] + F(rng.randint(1, 5), rng.randint(1, 5)))
                matrix = [[] for _ in range(n)]
                for k in range(N):
                    weights = [rng.randint(0, 5) for i in range(n)]
                    if sum(weights) == 0:
                        weights[0] = 1
                    for i in range(n):
                        matrix[i].append(F(weights[i], sum(weights)))
                expected, _ = original_error(matrix, grid)
                actual = author.exact_schedule_error(matrix, grid)
                assert actual == expected
                count += 1
    print(f"Original objective verified on {count} random rational controls.")


def compressed_original_error(n, grid, winner):
    """Original signed discrepancies for compressed types, no expansion in n.

    Distinguish constant schedules from two distinct modes of the same type.
    Omitted modes retain their own cumulative discrepancy, not their sum.
    """
    a, b, _, x = winner
    raw = [(F(0), [F(0)] * 3), (grid[a], x[:3]),
           (grid[b], x[3:6]), (grid[-1], x[6:9])]
    states = {}
    for time, value in raw:
        if time in states:
            assert states[time] == value
        states[time] = value
    cumulative = []
    for time in grid:
        lo = max(k for k in states if k <= time)
        hi = min(k for k in states if k >= time)
        cumulative.append(states[lo] if lo == hi else [
            states[lo][j] + (time-lo)/(hi-lo)*(states[hi][j]-states[lo][j])
            for j in range(3)])
    multiplicities = [1, 1, n-2]
    best = grid[-1]
    for p in range(3):
        error = F(0)
        for time, state in zip(grid, cumulative):
            error = max(error, abs(time-state[p]))
            for g in range(3):
                if multiplicities[g] > (g == p):
                    error = max(error, state[g])
        best = min(best, error)
        for q in range(3):
            if p == q and multiplicities[p] < 2:
                continue
            for cut in grid:
                error = F(0)
                for time, state in zip(grid, cumulative):
                    error = max(error, abs(min(time,cut)-state[p]),
                                abs(max(F(0),time-cut)-state[q]))
                    for g in range(3):
                        if multiplicities[g] > ((g == p) + (g == q)):
                            error = max(error, state[g])
                best = min(best, error)
    return best


def check_formula_extreme_arithmetic():
    """Inputs beyond floating-point rational reconstruction, compressed output."""
    cases = []
    for n in [3, 4, 100000000, 10**100 + 7]:
        for T in [F(1), F(7, 10**30 + 57), F(10**50 + 151, 97)]:
            grid = [F(0), T]
            value, witness = formula.minimax(n, grid)
            assert value == F(n-1, n) * T
            cases.append((n, grid, value, witness))
    for n in [3, 5, 100000000, 10**100 + 7]:
        for grid in [[F(0), F(1, 10**30 + 57), F(1)],
                     [F(0), F(1,3), F(1,2), F(2,3), F(1)],
                     [F(0), F(1,3)-F(1,10**40), F(1,3)+F(1,10**40), F(1)]]:
            value, witness = formula.minimax(n, grid)
            cases.append((n, grid, value, witness))
    for n, grid, value, witness in cases:
        a, b, kind, x = witness
        independently_check_region(n, grid, a, b, kind, x)
        assert compressed_original_error(n, grid, witness) == value
    print(f"Extreme exact arithmetic: {len(cases)} cases passed, modes up to 10**100+7.")


def check_formula_against_certified_lp():
    import random
    rng = random.Random(160907)
    cases = [(n, list(map(F, range(N+1)))) for n in range(3,9) for N in range(1,9)]
    for _ in range(50):
        n, N = rng.randrange(3, 11), rng.randrange(1, 8)
        grid = [F(0)]
        for k in range(N):
            grid.append(grid[-1]+F(rng.randrange(1,12),rng.randrange(1,12)))
        cases.append((n,grid))
    cases.append((9,list(map(F,[0,"19/2","61/6","265/24","481/24","2669/120"]))))
    for n,grid in cases:
        value,witness = formula.minimax(n,grid)
        assert value == author.minimax_lp(n,grid)[0]
        a,b,kind,x = witness
        independently_check_region(n,grid,a,b,kind,x)
        assert compressed_original_error(n,grid,witness) == value
    print(f"Explicit formula agrees with rational-certified LPs on {len(cases)} cases.")


def check_public_validation():
    """Explicit checks remain active under python -O."""
    invalid = [
        (True, [0, 1], TypeError), (3.0, [0, 1], TypeError),
        ("3", [0, 1], TypeError), (2, [0, 1], ValueError),
        (0, [0, 1], ValueError), (-3, [0, 1], ValueError),
        (3, [], ValueError), (3, [0], ValueError), (3, [1, 2], ValueError),
        (3, [0, 0], ValueError), (3, [0, 1, 1], ValueError),
        (3, [0, 2, 1], ValueError), (3, [0, -1], ValueError),
        (3, [0, True], TypeError), (3, [False, 1], TypeError),
        (3, [0, 1.0], TypeError), (3, [0, "bad"], ValueError),
        (3, [0, None], TypeError),
    ]
    for n, grid, expected_error in invalid:
        try:
            formula.minimax(n, grid)
        except expected_error:
            pass
        else:
            raise RuntimeError(f"Expected {expected_error.__name__}: {(n, grid)}")
    valid = [
        (3, [0, 1], F(2, 3)),
        (3, ["0", "1/3", "2/3", "1"], F(1, 3)),
        (5, [0, F(1, 4), F(3, 2)], F(19, 20)),
        (10**100+7, [0, F(1, 10**30+57)],
         F(10**100+6, (10**100+7)*(10**30+57))),
    ]
    for n, grid, expected in valid:
        value, witness = formula.minimax(n, grid)
        if value != expected or witness is None:
            raise RuntimeError(f"Unexpected valid result: {value} != {expected}")
    print(f"Public validation: {len(invalid)} invalid and {len(valid)} valid cases passed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-milp", action="store_true")
    parser.add_argument("--validation-only", action="store_true")
    args = parser.parse_args()
    check_public_validation()
    if args.validation_only:
        return
    check_formula_random_controls()
    check_formula_extreme_arithmetic()
    check_formula_against_certified_lp()
    cases = [(n, list(map(F, range(N + 1))))
             for n, N in [(3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (5, 2)]]
    cases += [(3, list(map(F, [0, "1/5", "2/3", 1]))),
              (4, list(map(F, [0, "2/7", 1]))),
              (5, list(map(F, [0, "1/4", "3/2"])))]
    for n, grid in cases:
        value = audit_regions(n, grid)
        if not args.skip_milp:
            primal, upper = original_minimax_milp(n, grid)
            assert abs(primal - float(value)) < 1e-7
            assert abs(upper - float(value)) < 1e-7
            print(f"  Original MILP primal={primal:.12g}, upper={upper:.12g}")
    assert audit_regions(5, list(map(F, range(10)))) == F(17, 5)
    print("All independent checks passed.")


if __name__ == "__main__":
    main()
