"""Independent review of spacing-aware noisy-Markov spectral bounds.

The reference forms dense rational covariance matrices and solves their local
normal equations directly. Pair and row majorants are checked by enumerating
separated sets, independently of the author's arithmetic progressions and DP.
"""

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from time import perf_counter

import numpy as np

from noisy_markov_spacing_bound import spacing_bound, spacing_mask_count


HERE = Path(__file__).resolve().parent


@lru_cache(None)
def separated_sets(n, gap):
    return tuple(s for k in range(n + 1) for s in combinations(range(n), k)
                 if all(b - a >= gap for a, b in zip(s, s[1:])))


def dense_solve(matrix, rhs):
    """Plain exact elimination; no Kalman recursion or author helpers."""
    m = len(rhs)
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for j in range(m):
        pivot = rows[j][j]
        assert pivot > 0  # Each leading principal block is positive definite.
        for k in range(j, m + 1):
            rows[j][k] /= pivot
        for i in range(j + 1, m):
            factor = rows[i][j]
            for k in range(j, m + 1):
                rows[i][k] -= factor * rows[j][k]
    answer = [Q(0)] * m
    for i in reversed(range(m)):
        answer[i] = rows[i][m] - sum(
            (rows[i][j] * answer[j] for j in range(i + 1, m)), Q(0))
    return tuple(answer)


class DenseReference:
    def __init__(self, n, rho, latent, nugget):
        self.n, self.rho, self.P, self.r = n, rho, latent, nugget
        self.R = tuple(tuple(latent * rho ** abs(i-j)
                             + (nugget if i == j else 0)
                             for j in range(n)) for i in range(n))

    @lru_cache(None)
    def conditional(self, ages):
        if not ages:
            return (), self.P + self.r
        covariance = tuple(tuple(self.P * self.rho ** abs(i-j)
                                 + (self.r if i == j else 0)
                                 for j in ages) for i in ages)
        cross = tuple(self.P * self.rho ** i for i in ages)
        coefficient = dense_solve(covariance, cross)
        variance = self.P + self.r - sum(
            (x * y for x, y in zip(coefficient, cross)), Q(0))
        return coefficient, variance

    def residual_covariance(self, selected, window):
        size = len(selected)
        transform, variances = [], []
        for i, t in enumerate(selected):
            history = tuple(j for j in range(i) if t-selected[j] <= window)
            ages = tuple(t-selected[j] for j in history)
            coefficient, variance = self.conditional(ages)
            row = [Q(0)] * size
            row[i] = Q(1)
            for j, value in zip(history, coefficient):
                row[j] = -value
            transform.append(row)
            variances.append(variance)
        AR = [[sum((transform[i][k] * self.R[selected[k]][selected[j]]
                    for k in range(size)), Q(0))
               for j in range(size)] for i in range(size)]
        covariance = [[sum((AR[i][k] * transform[j][k] for k in range(size)), Q(0))
                       for j in range(size)] for i in range(size)]
        assert all(covariance[i][i] == variances[i] for i in range(size))
        return covariance, variances


def enumerated_pair_majorants(n, window, gap, rho, latent, nugget):
    """Enumerate possible distances instead of using geometric placements."""
    magnitude = abs(rho)
    gain = latent / (latent + nugget)
    histories = [tuple(d+gap for d in positions)
                 for positions in separated_sets(max(0, window-gap+1), gap)]
    phi = [Q(0)] * n
    for h in range(gap, n):
        if h > window:
            maximum = max(sum((magnitude ** (2*d) for d in distances), Q(0))
                          for distances in histories)
            phi[h] = latent * magnitude ** h * (1 + gain * maximum)
        else:
            # Orthogonality removes d <= window-h; enumerate the remainder.
            maximum = max(sum((magnitude ** (2*d) for d in distances
                               if d > window-h), Q(0))
                          for distances in histories)
            phi[h] = latent * gain * magnitude ** h * maximum
    return phi


def main():
    started = perf_counter()
    counts = dict(exact_models=0, local_variances=0, residual_pairs=0,
                  exact_raw_rows=0, numerical_normalized_rows=0,
                  spectral_checks=0, exact_floors=0, row_pricing_cases=0,
                  pair_pricing_checks=0, mask_count_checks=0,
                  invalid_inputs=0, cooldown_witnesses=0)
    worst = dict(spectral_to_bound=0.0, normalized_row_to_bound=0.0,
                 raw_row_to_majorant=0.0)
    witness = {}
    parameters = [
        (Q(1, 2), Q(1), Q(1)),
        (Q(-2, 3), Q(2), Q(1, 3)),
        (Q(99, 100), Q(1), Q(1, 100)),
        (Q(0), Q(1), Q(1)),
        (Q(9, 10), Q(0), Q(1)),
        (Q(1, 10), Q(1, 20), Q(3)),
    ]
    for n in range(1, 8):
        for rho, latent, nugget in parameters:
            reference = DenseReference(n, rho, latent, nugget)
            for gap in range(1, n+2):
                subsets = separated_sets(n, gap)
                for supplied_window in range(n+2):
                    window = min(supplied_window, n-1)
                    result = spacing_bound(n, supplied_window, gap,
                                           rho, latent, nugget)
                    floor = reference.conditional(tuple(
                        range(gap, window+1, gap)))[1]
                    assert floor == result['innovation_floor']
                    assert floor >= nugget
                    counts['exact_floors'] += 1
                    phi = enumerated_pair_majorants(
                        n, window, gap, rho, latent, nugget)
                    # Directly verify the author's closed pair formulas.
                    gain = latent / (latent+nugget)
                    for h in range(gap, n):
                        d = (range(gap, window+1, gap) if h > window else
                             range(max(gap, window+1-h), window+1, gap))
                        formula = latent * abs(rho)**h * (
                            (1 if h > window else 0)
                            + gain * sum((abs(rho)**(2*j) for j in d), Q(0)))
                        assert phi[h] == formula
                        counts['pair_pricing_checks'] += 1
                    direct_rows = [Q(0)] * n
                    for selected in subsets:
                        for anchor in selected:
                            direct_rows[anchor] = max(direct_rows[anchor], sum(
                                (phi[abs(anchor-j)] for j in selected if j != anchor), Q(0)))
                    shortcut = not rho or not latent or window >= n-1 or gap >= n
                    expected_row = Q(0) if shortcut else max(direct_rows)
                    assert expected_row == result['row_majorant']
                    assert expected_row / floor == result['delta']
                    if not shortcut:
                        assert direct_rows[result['worst_anchor']] == expected_row
                    counts['row_pricing_cases'] += 1
                    for selected in subsets:
                        if not selected:
                            continue
                        covariance, variances = reference.residual_covariance(selected, window)
                        size = len(selected)
                        assert all(d >= floor for d in variances)
                        counts['local_variances'] += size
                        for i in range(size):
                            raw_row = sum((abs(covariance[i][j]) for j in range(size)
                                           if j != i), Q(0))
                            assert raw_row <= expected_row
                            counts['exact_raw_rows'] += 1
                            if expected_row:
                                worst['raw_row_to_majorant'] = max(
                                    worst['raw_row_to_majorant'], float(raw_row/expected_row))
                            for j in range(i):
                                assert abs(covariance[i][j]) <= phi[selected[i]-selected[j]]
                                counts['residual_pairs'] += 1
                        matrix = np.array([[float(x) for x in row] for row in covariance])
                        scale = np.sqrt(np.array([float(x) for x in variances]))
                        normalized = matrix / scale[:, None] / scale[None, :]
                        np.fill_diagonal(normalized, 0.0)
                        row_norm = float(np.max(np.sum(abs(normalized), axis=1)))
                        spectral = float(np.max(abs(np.linalg.eigvalsh(normalized))))
                        delta = float(result['delta'])
                        assert row_norm <= delta * (1+1e-12) + 1e-13
                        assert spectral <= delta * (1+1e-12) + 1e-13
                        if delta and spectral/delta > worst['spectral_to_bound']:
                            worst['spectral_to_bound'] = spectral/delta
                            witness = dict(n=n, L=supplied_window, gap=gap,
                                           rho=str(rho), latent=str(latent), nugget=str(nugget),
                                           selected=list(selected), spectral=spectral, delta=delta)
                        if delta:
                            worst['normalized_row_to_bound'] = max(
                                worst['normalized_row_to_bound'], row_norm/delta)
                        counts['numerical_normalized_rows'] += size
                        counts['spectral_checks'] += 1
                        counts['exact_models'] += 1
        print(json.dumps({'completed_horizon': n, 'counts': counts}), flush=True)

    for window in range(15):
        for gap in range(1, window+4):
            assert spacing_mask_count(window, gap) == len(separated_sets(window, gap))
            counts['mask_count_checks'] += 1
            if window < gap-1:
                # Selecting at 0 and window+1 looks allowed after the earlier
                # selection leaves an L-bit information window, but is infeasible.
                assert window+1 < gap
                counts['cooldown_witnesses'] += 1

    bad_calls = [
        lambda: spacing_bound(True, 1, 1, 0, 1, 1),
        lambda: spacing_bound(3.0, 1, 1, 0, 1, 1),
        lambda: spacing_bound(0, 1, 1, 0, 1, 1),
        lambda: spacing_bound(3, -1, 1, 0, 1, 1),
        lambda: spacing_bound(3, 1, 0, 0, 1, 1),
        lambda: spacing_bound(3, 1, 1, 1, 1, 1),
        lambda: spacing_bound(3, 1, 1, -1, 1, 1),
        lambda: spacing_bound(3, 1, 1, 0, -1, 1),
        lambda: spacing_bound(3, 1, 1, 0, 1, 0),
        lambda: spacing_bound(3, 1, 1, .5, 1, 1),
        lambda: spacing_bound(3, 1, 1, 'nan', 1, 1),
        lambda: spacing_mask_count(-1, 1),
        lambda: spacing_mask_count(1, 0),
        lambda: spacing_mask_count(True, 1),
        lambda: spacing_mask_count(1, 1.0),
    ]
    for call in bad_calls:
        try:
            call()
        except (TypeError, ValueError):
            counts['invalid_inputs'] += 1
        else:
            raise AssertionError('Malformed input was accepted')

    record = dict(status='passed', counts=counts, worst_ratios=worst,
                  spectral_ratio_witness=witness,
                  exact_parameters=[[str(x) for x in row] for row in parameters],
                  elapsed_seconds=perf_counter()-started,
                  author_sha256=sha256((HERE/'noisy_markov_spacing_bound.py').read_bytes()).hexdigest(),
                  author_dependency_sha256=sha256((HERE/'certify_noisy_markov.py').read_bytes()).hexdigest(),
                  reviewer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitations=['Normalized row sums and eigenvalues use floating arithmetic; '
                               'raw covariance, pair, floor, and priced-row inequalities use exact rationals.',
                               'This review checks the bound helper, not a spacing-constrained design solver.'])
    output = HERE/'results'/'noisy-markov-spacing-independent-review.json'
    output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record), flush=True)


if __name__ == '__main__':
    main()
