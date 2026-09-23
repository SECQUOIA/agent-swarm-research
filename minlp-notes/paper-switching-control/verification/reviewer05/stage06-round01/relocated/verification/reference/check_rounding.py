"""Independent direct-prefix checks of the one-switch optimization prototype."""
from fractions import Fraction as F
from itertools import product
from random import Random
from time import perf_counter
import argparse

from rounding import (optimal_one_switch, schedule_error, complete_with_one_block,
                      optimal_block_assignment, optimal_few_switches)


def brute(rows, dt, allowed=None, initial=None):
    n, N = len(rows[0]), len(rows)
    starts = range(n) if initial is None else [initial]
    switches = range(1, N) if allowed is None else allowed
    best = None
    for p in starts:
        schedules = [(p,) * N]
        schedules += [(p,) * k + (q,) * (N-k) for k in switches for q in range(n) if q != p]
        for schedule in schedules:
            value = schedule_error(rows, dt, schedule)
            best = value if best is None else min(best, value)
    return best


def check(rows, dt, allowed=None, initial=None):
    answer = optimal_one_switch(rows, dt, switch_indices=allowed, initial_mode=initial)
    assert answer.error == schedule_error(rows, dt, answer.schedule())
    assert answer.error == brute(rows, dt, allowed, initial), (rows, dt, allowed, initial, answer)
    assert sum(a != b for a, b in zip(answer.schedule(), answer.schedule()[1:])) <= 1
    if initial is not None:
        assert answer.schedule()[0] == initial
    return answer


def check_extensions():
    rng = Random(194791)
    prefix_cases = 0
    for _ in range(45):
        n, N = rng.randrange(2, 7), rng.randrange(2, 9)
        dt = [F(rng.randrange(1, 5), 3) for _ in range(N)]
        rows = []
        for d in dt:
            weights = [rng.randrange(1, 8) for _ in range(n)]
            rows.append([d * F(w, sum(weights)) for w in weights])
        prefix = tuple(rng.randrange(n) for _ in range(rng.randrange(N)))
        for required in (False, True):
            error, mode = complete_with_one_block(rows, dt, prefix, require_switch=required)
            eligible = [i for i in range(n) if not (required and prefix and i == prefix[-1])]
            reference = min(schedule_error(rows, dt, prefix + (i,) * (N-len(prefix))) for i in eligible)
            assert error == reference == schedule_error(rows, dt, prefix + (mode,) * (N-len(prefix)))
            prefix_cases += 1
    assert complete_with_one_block([[1], [1]], [1, 1], [0]) == (0, 0)
    # A repeated mode is necessary to attain zero, so distinct-mode shortcuts
    # would fail this test despite using exactly the same three boundaries.
    rows, dt = [[1, 0], [0, 1], [1, 0]], [1, 1, 1]
    assert optimal_block_assignment(rows, dt, [0, 1, 2, 3]).schedule() == (0, 1, 0)
    assert optimal_few_switches(rows, dt, 2).error == 0
    # Subdividing a run must not impose dwell on each artificial block.
    assert optimal_few_switches([[1], [1], [1]], [1,1,1], 2, minimum_dwell=[3]).error == 0
    assert optimal_few_switches([[1], [1]], [1,1], 1, minimum_dwell=[3]) is None
    def dwell_valid(schedule, dt, minimum):
        start = 0
        for end in range(1, len(schedule)+1):
            if end == len(schedule) or schedule[end] != schedule[start]:
                if sum(dt[start:end]) < minimum[schedule[start]]:
                    return False
                start = end
        return True
    few_cases = 0
    dwell_cases = 0
    for _ in range(22):
        n, N = rng.randrange(1, 5), rng.randrange(2, 6)
        dt = [F(rng.randrange(1, 6), 4) for _ in range(N)]
        rows = []
        for d in dt:
            weights = [rng.randrange(1, 7) for _ in range(n)]
            rows.append([d * F(w, sum(weights)) for w in weights])
        values = [(schedule, schedule_error(rows, dt, schedule),
                   sum(a != b for a,b in zip(schedule, schedule[1:])))
                  for schedule in product(range(n), repeat=N)]
        for budget in (0, 1, 2, N+2):
            answer = optimal_few_switches(rows, dt, budget)
            assert answer.error == min(value for _,value,changes in values if changes <= budget)
            assert schedule_error(rows, dt, answer.schedule()) == answer.error
            assert sum(a != b for a,b in zip(answer.schedule(), answer.schedule()[1:])) <= budget
            if budget == 1:
                assert optimal_one_switch(rows, dt).error == answer.error
            few_cases += 1
        boundaries = (0,) + tuple(k for k in range(1,N) if rng.randrange(2)) + (N,)
        answer = optimal_block_assignment(rows, dt, boundaries)
        allowed = set(boundaries[1:-1])
        reference = min(value for schedule,value,_ in values
                        if all(a == b or k in allowed for k,(a,b) in enumerate(zip(schedule,schedule[1:]), 1)))
        assert answer.error == reference == schedule_error(rows, dt, answer.schedule())
        few_cases += 1
        minimum = [F(rng.randrange(0, int(4*sum(dt))+5), 4) for _ in range(n)]
        for fixed in (False, True):
            answer = (optimal_block_assignment(rows, dt, boundaries, minimum_dwell=minimum) if fixed
                      else optimal_few_switches(rows, dt, 2, minimum_dwell=minimum))
            feasible = [value for schedule,value,changes in values
                        if dwell_valid(schedule,dt,minimum) and
                        (all(a == b or k in allowed for k,(a,b) in enumerate(zip(schedule,schedule[1:]),1))
                         if fixed else changes <= 2)]
            if not feasible:
                assert answer is None
            else:
                assert answer is not None and answer.error == min(feasible)
                assert dwell_valid(answer.schedule(),dt,minimum)
                assert schedule_error(rows,dt,answer.schedule()) == answer.error
            dwell_cases += 1
    print(f"PASS: {dwell_cases} exact per-mode dwell brute comparisons; merged-run and infeasibility regressions")
    print(f"PASS: {prefix_cases} arbitrary-prefix completion checks; {few_cases} exact block/few-switch brute comparisons; repeat regression")


def public_benchmark(path):
    """Verify a public Lotka-Volterra relaxed profile after documented quantization."""
    import hashlib
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == "1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883"
    data = [[F(x) for x in line.split()] for line in raw.decode().splitlines()[1:]]
    denominator = 10**6
    rows, dt = [], []
    normalization_change = F(0)
    for line, following in zip(data, data[1:]):
        d = following[0] - line[0]
        weights = line[3:]
        assert all(x >= 0 for x in weights) and sum(weights) > 0
        normalized = [x / sum(weights) for x in weights]
        scaled = [x * denominator for x in normalized]
        counts = [x.numerator // x.denominator for x in scaled]
        remainders = sorted(range(len(weights)), key=lambda i: scaled[i] - counts[i], reverse=True)
        for i in remainders[:denominator - sum(counts)]:
            counts[i] += 1
        assert all(abs(F(counts[i], denominator) - normalized[i]) < F(1, denominator)
                   for i in range(len(weights)))
        normalization_change = max(normalization_change, max(abs(x-y) for x,y in zip(weights, normalized)))
        rows.append([d * F(x, denominator) for x in counts])
        dt.append(d)
    before = perf_counter()
    answer = optimal_one_switch(rows, dt)
    elapsed = perf_counter() - before
    assert answer.error == schedule_error(rows, dt, answer.schedule())
    # Independent O(n^3*N) scan: directly evaluate all prefix errors of each
    # mode only at the switch boundary and horizon. This identity follows from
    # monotonicity within each constant block; it does not use total dominance.
    n, N = len(rows[0]), len(rows)
    totals = [sum(row[i] for row in rows) for i in range(n)]
    A, t, T = [F(0)] * n, F(0), sum(dt)
    independent = min(max(abs(totals[i] - (T if i == p else 0)) for i in range(n)) for p in range(n))
    for k in range(1, N):
        t += dt[k-1]
        A = [a+x for a,x in zip(A, rows[k-1])]
        for p in range(n):
            for q in range(n):
                if p == q:
                    continue
                error = max(max(abs(A[i] - (t if i == p else 0)),
                                abs(totals[i] - (t if i == p else T-t if i == q else 0)))
                            for i in range(n))
                independent = min(independent, error)
    assert independent == answer.error
    print(f"Public Lotka-Volterra profile: n={n}, N={N}, T={T}, {elapsed:.3f} s")
    print(f"  exact quantized optimum {answer.error} = {float(answer.error):.12g}")
    print(f"  modes {answer.initial_mode}->{answer.final_mode}, switch index {answer.switch_index}")
    print(f"  max rate normalization change {float(normalization_change):.6g}; rate quantization < 1e-6")
    print(f"  certified objective change versus row-normalized decimal source < {float(T/denominator):.6g}")
    # Preserve the integrated public profile exactly while restricting switches
    # to coarse boundaries. Interior relaxed variation is not interpolated.
    from itertools import combinations
    for coarse_N, budgets in [(24, (0, 1, 2)), (12, (3,))]:
        width = N // coarse_N
        coarse_rows = [[sum(rows[j][i] for j in range(left, left+width)) for i in range(n)]
                       for left in range(0, N, width)]
        coarse_dt = [sum(dt[left:left+width]) for left in range(0, N, width)]
        times = [F(0)]
        cumulative = [[F(0)] * n]
        for row, d in zip(coarse_rows, coarse_dt):
            times.append(times[-1] + d)
            cumulative.append([a+x for a,x in zip(cumulative[-1],row)])
        for budget in budgets:
            before = perf_counter()
            answer = optimal_few_switches(coarse_rows, coarse_dt, budget)
            elapsed = perf_counter() - before
            expanded = tuple(mode for mode in answer.schedule() for _ in range(width))
            assert schedule_error(rows, dt, expanded) == answer.error
            # Separate exhaustive mode-word and grid-boundary enumeration.
            k = min(budget+1, coarse_N)
            reference = None
            for interior in combinations(range(1, coarse_N), k-1):
                bounds = (0,) + interior + (coarse_N,)
                for modes in product(range(n), repeat=k):
                    service, error = [F(0)] * n, F(0)
                    for p,left,right in zip(modes,bounds,bounds[1:]):
                        service[p] += times[right]-times[left]
                        error = max(error, max(abs(a-b) for a,b in zip(cumulative[right],service)))
                    reference = error if reference is None else min(reference,error)
            assert reference == answer.error
            print(f"  coarse public N={coarse_N}, switches<={budget}: optimum={answer.error} ({float(answer.error):.9g}), {elapsed:.3f} s; blocks={answer.boundaries}, modes={answer.modes}")


def main(benchmark=False):
    count = 0
    # Exhaust all half-integral relaxed columns in tiny cases, including ties,
    # unused modes, vertices of the simplex, and several grid lengths.
    for n, N in [(1, 3), (2, 4), (3, 3), (4, 2)]:
        columns = [tuple(F(x, 2) for x in c) for c in product(range(3), repeat=n) if sum(c) == 2]
        for rows in product(columns, repeat=N):
            check(rows, [1] * N)
            count += 1
    rng = Random(73419)
    # Nonuniform rational grids; repeat with fixed initial mode and sparse
    # permitted switch boundaries, which model scheduling windows/dwell limits.
    for _ in range(65):
        n, N = rng.randrange(2, 7), rng.randrange(1, 10)
        dt = [F(rng.randrange(1, 8), rng.randrange(1, 5)) for _ in range(N)]
        rows = []
        for d in dt:
            weights = [rng.randrange(0, 9) for _ in range(n)]
            if sum(weights) == 0:
                weights[0] = 1
            rows.append([d * F(x, sum(weights)) for x in weights])
        check(rows, dt)
        check(rows, dt, [k for k in range(1, N) if rng.randrange(2)], rng.randrange(n))
        count += 2
    matrix = [[5,7,4,0,0,10,0,0,0], [5,0,0,1,10,0,0,0,0],
              [0,0,6,0,0,0,0,10,0], [0,0,0,6,0,0,10,0,0],
              [0,3,0,3,0,0,0,0,10]]
    rows = [tuple(F(matrix[i][k], 10) for i in range(5)) for k in range(9)]
    assert check(rows, [1] * 9).error == F(17, 5)
    assert check([[F(1, 5)] * 5 for _ in range(45)], [1] * 45).error == 16
    # Float rejection prevents silently certifying a binary approximation to
    # a user's intended decimal. Other malformed data must fail explicitly.
    for args, kwargs, exception in [
        (([[0.5, 0.5]], [1]), {}, TypeError),
        (([[1]], [0]), {}, ValueError),
        (([[1, 1]], [1]), {}, ValueError),
        (([[1]], [1]), {"initial_mode": 2}, ValueError),
        (([[1]], [1]), {"switch_indices": [1]}, ValueError),
        (([[1], [1]], [1, 1]), {"switch_indices": [1, True]}, ValueError),
    ]:
        try:
            optimal_one_switch(*args, **kwargs)
        except exception:
            pass
        else:
            raise AssertionError("malformed instance was accepted")
    print(f"PASS: {count + 2} exact optimizer/brute-force comparisons; input rejection checks")
    if benchmark:
        # Synthetic stress case, not a claim about a control application.
        # Vary dominant allocation smoothly by column; exact denominator 100.
        n, N = 100, 1000
        rows = []
        for k in range(N):
            row = [F(1, 2*n)] * n
            row[(k // 20) % n] += F(1, 2)
            rows.append(row)
        before = perf_counter()
        answer = optimal_one_switch(rows, [1] * N)
        elapsed = perf_counter() - before
        assert schedule_error(rows, [1] * N, answer.schedule()) == answer.error
        print(f"Synthetic exact-rational benchmark: n={n}, N={N}, {elapsed:.3f} s, error={answer.error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--public-benchmark", metavar="CSV_PATH")
    args = parser.parse_args()
    main(args.benchmark)
    check_extensions()
    if args.public_benchmark:
        public_benchmark(args.public_benchmark)
