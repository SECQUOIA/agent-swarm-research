"""Independent exact checks for support-preserving uniform-grid transfer.

Run from any directory: python3 path/to/check_grid_transfer_review.py
Only Python's standard library is used. This checker does not implement the
candidate's flow algorithm: it enumerates or uses dynamic programming over
integer prefix counts. These checks complement, rather than replace, its proof.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random


def switches(word):
    return sum(a != b for a, b in zip(word, word[1:]))


def compress(word):
    return tuple(x for k, x in enumerate(word) if k == 0 or x != word[k-1])


def subsequence(small, large):
    it = iter(large)
    return all(any(x == y for y in it) for x in small)


def exhaustive_microgrids():
    """Every original word, every supported selection, exact scaled integers."""
    cases = witnesses = 0
    for n, N, q in ((2, 1, 5), (2, 3, 3), (2, 4, 2),
                    (3, 2, 3), (3, 3, 2), (3, 4, 2)):
        for original in product(range(n), repeat=N*q):
            cases += 1
            cells = [original[j*q:(j+1)*q] for j in range(N)]
            support = [tuple(sorted(set(cell))) for cell in cells]
            found = False
            for chosen in product(*support):
                assert switches(chosen) <= switches(original)
                assert subsequence(compress(chosen), compress(original))
                occupancy = [0]*n
                selected = [0]*n
                valid = True
                endpoint_error = 0
                for cell, mode in zip(cells, chosen):
                    for i in cell:
                        occupancy[i] += 1
                    selected[mode] += 1
                    for i in range(n):
                        valid &= occupancy[i]//q <= selected[i] <= (occupancy[i]+q-1)//q
                        endpoint_error = max(endpoint_error, abs(q*selected[i]-occupancy[i]))
                if not valid:
                    continue
                found = True
                witnesses += 1
                assert endpoint_error < q
                delta = [0]*n
                entire_error = 0
                for j, old in enumerate(original):
                    delta[chosen[j//q]] += 1
                    delta[old] -= 1
                    entire_error = max(entire_error, *map(abs, delta))
                # Both controls are constant between these exhaustive breakpoints.
                assert entire_error == endpoint_error
            assert found, (n, N, q, original)
    return cases, witnesses


def masses(blocks, ends, n):
    rows = []
    for left, right in zip(ends, ends[1:]):
        row = [Q(0)]*n
        for a, b, i in blocks:
            row[i] += max(Q(0), min(right, b)-max(left, a))
        rows.append(tuple(x/(right-left) for x in row))
    return rows


def prefix_dp(rows):
    """Find a supported prefix-rounded witness independently of flow integrality."""
    n = len(rows[0])
    prefixes = [Q(0)]*n
    states = {(0,)*n: ()}
    for row in rows:
        prefixes = [a+b for a, b in zip(prefixes, row)]
        lower = [x.numerator//x.denominator for x in prefixes]
        upper = [-((-x.numerator)//x.denominator) for x in prefixes]
        next_states = {}
        for state, word in states.items():
            for i, x in enumerate(row):
                if not x:
                    continue
                next_state = list(state)
                next_state[i] += 1
                if all(lo <= k <= hi for lo, k, hi in zip(lower, next_state, upper)):
                    next_states.setdefault(tuple(next_state), word+(i,))
        states = next_states
        assert states
    return next(iter(states.values()))


def error_at_breakpoints(blocks, ends, chosen, n):
    points = sorted(set(ends) | {x for a, b, _ in blocks for x in (a, b)})
    error = Q(0)
    for t in points:
        old = [Q(0)]*n
        new = [Q(0)]*n
        for a, b, i in blocks:
            old[i] += max(Q(0), min(t, b)-a)
        for a, b, i in zip(ends, ends[1:], chosen):
            new[i] += max(Q(0), min(t, b)-a)
        error = max(error, *(abs(a-b) for a, b in zip(old, new)))
    return error


def rational_cases():
    rng = Random(20260907)
    for _ in range(500):
        n, N = rng.randint(1, 6), rng.randint(1, 15)
        spacing = Q(rng.randint(1, 11), rng.randint(1, 13))
        T = N*spacing
        cuts = sorted({Q(0), T} | {T*Q(rng.randint(1, 1008), 1009)
                                          for _ in range(rng.randint(0, 30))})
        blocks = [(a, b, rng.randrange(n)) for a, b in zip(cuts, cuts[1:])]
        ends = [j*spacing for j in range(N+1)]
        rows = masses(blocks, ends, n)
        chosen = prefix_dp(rows)
        original = [i for _, _, i in blocks]
        assert switches(chosen) <= switches(original)
        assert subsequence(compress(chosen), compress(original))
        assert all(rows[j][i] > 0 for j, i in enumerate(chosen))
        assert error_at_breakpoints(blocks, ends, chosen, n) < spacing
        if n == 2:
            x, previous, nearest = Q(0), 0, []
            for row in rows:
                x += row[0]
                z = x+Q(1, 2)
                current = z.numerator//z.denominator
                assert current-previous in (0, 1)
                nearest.append(0 if current-previous else 1)
                previous = current
            assert all(rows[j][i] > 0 for j, i in enumerate(nearest))
            assert switches(nearest) <= switches(original)
            assert error_at_breakpoints(blocks, ends, nearest, n) <= spacing/2
    # Binary half-cell switch proves the sharper constant cannot be reduced.
    blocks = [(Q(0), Q(1, 2), 0), (Q(1, 2), Q(1), 1)]
    assert all(error_at_breakpoints(blocks, [Q(0), Q(1)], [i], 2) == Q(1, 2)
               for i in (0, 1))
    return 500


def binary_nonuniform_cases():
    rng = Random(139)
    for _ in range(200):
        ends = sorted({Q(0), Q(1)} | {Q(rng.randint(1, 100), 101)
                                     for _ in range(rng.randint(1, 20))})
        cuts = sorted({Q(0), Q(1)} | {Q(rng.randint(1, 96), 97)
                                     for _ in range(rng.randint(1, 30))})
        blocks = [(a, b, rng.randrange(2)) for a, b in zip(cuts, cuts[1:])]
        rows = masses(blocks, ends, 2)
        D = max(b-a for a, b in zip(ends, ends[1:]))
        error = Q(0)
        chosen = []
        for left, right, row in zip(ends, ends[1:], rows):
            d = right-left
            a = d*row[0]
            if a == 0:
                active = 1
            elif a == d:
                active = 0
            else:
                active = 0 if abs(error+d-a) < abs(error-a) else 1
            error += (d if active == 0 else 0)-a
            chosen.append(active)
            assert abs(error) <= D/2
            assert row[active] > 0
        assert switches(chosen) <= switches([i for _, _, i in blocks])
        assert error_at_breakpoints(blocks, ends, chosen, 2) <= D/2
    return 200


def sharpness_family():
    """Exact integration of the grid-constant relaxed-input sharpness family."""
    for n in range(2, 9):
        for m in range(1, 9):
            N = n*m+1
            word = tuple(range(n))*m
            blocks = [(Q(k, n*m), Q(k+1, n*m), i) for k, i in enumerate(word)]
            blocks.append((Q(1), Q(N), n-1))
            assert switches([i for _, _, i in blocks]) == n*m-1
            error = Q(0)
            for t in sorted({x for a, b, _ in blocks for x in (a, b)}):
                occupation = [Q(0)]*n
                for a, b, i in blocks:
                    occupation[i] += max(Q(0), min(t, b)-a)
                relaxed = [min(t, Q(1))/n for _ in range(n)]
                relaxed[n-1] += max(Q(0), t-1)
                error = max(error, *(abs(a-b) for a, b in zip(occupation, relaxed)))
            assert error == Q(n-1, n*n*m)
            # Any grid schedule chooses one mode throughout its first cell.
            first_cell_errors = [max(abs(Q(int(i == active))-Q(1, n))
                                     for i in range(n)) for active in range(n)]
            assert set(first_cell_errors) == {Q(n-1, n)}
            # All-final-mode schedule attains this lower bound through the horizon.
            for t in (Q(0), Q(1), Q(N)):
                relaxed = [min(t, Q(1))/n for _ in range(n)]
                relaxed[n-1] += max(Q(0), t-1)
                assert max(abs(Q(t if i == n-1 else 0)-relaxed[i])
                           for i in range(n)) <= Q(n-1, n)
            gap_lower = Q(n-1, n)-error
            assert gap_lower == Q(n-1, n)*(1-Q(1, n*m))
    assert Q(3, 4)*(1-Q(1, 16)) == Q(45, 64) > Q(1, 2)
    return 56


if __name__ == '__main__':
    cases, witnesses = exhaustive_microgrids()
    random_cases = rational_cases()
    sharpness_cases = sharpness_family()
    nonuniform_cases = binary_nonuniform_cases()
    print(f'PASS: {cases} exhaustive original controls; {witnesses} supported prefix witnesses; '
          f'{random_cases} exact-rational randomized controls; {sharpness_cases} sharpness-family cases; '
          f'{nonuniform_cases} binary nonuniform controls; binary sharpness example.')
