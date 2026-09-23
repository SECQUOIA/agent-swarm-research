"""Exact checks of the recorded point-packing moment constructions.

PSD follows analytically from projection/diagonal covariance blocks. These
finite rational checks verify all RLT inequalities and all pair distances.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


def construction(n, symmetry):
    nx, ny = (n + 1) // 2, (n + 3) // 4
    bounds, means, matrices = [], [], []
    for axis in range(2):
        restricted = (nx if axis == 0 else ny) if symmetry else 0
        low = [Q(1, 2) if i < restricted else Q(0) for i in range(n)]
        mean = [(a + 1) / 2 for a in low]
        var = [(1 - a) ** 2 / 4 for a in low]
        matrix = [[mean[i] * mean[j] for j in range(n)] for i in range(n)]
        k = ny if symmetry else n
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] += var[i]
                elif i < k and j < k:
                    matrix[i][j] -= var[i] / (k - 1)
        bounds.append(low)
        means.append(mean)
        matrices.append(matrix)
    target = Q(n, n - 1) if not symmetry else Q(ny, 4 * (ny - 1))
    inequalities = 0
    for low, x, X in zip(bounds, means, matrices):
        for i in range(n):
            for j in range(n):
                assert X[i][j] >= low[i] * x[j] + low[j] * x[i] - low[i] * low[j]
                assert X[i][j] >= x[i] + x[j] - 1
                assert X[i][j] <= low[i] * x[j] + x[i] - low[i]
                assert X[i][j] <= x[j] + low[j] * x[i] - low[j]
                inequalities += 4
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distance = sum(X[i][i] - 2 * X[i][j] + X[j][j] for X in matrices)
            assert distance >= target
            distances.append(distance)
    assert min(distances) == target
    return dict(n=n, symmetry=symmetry, target=str(target), rlt_inequalities=inequalities,
                pair_distances=len(distances))


if __name__ == '__main__':
    cases = [construction(n, False) for n in range(2, 31)]
    cases += [construction(n, True) for n in range(5, 31)]
    result = {'status': 'PASS', 'arithmetic': 'exact rational', 'cases': cases,
              'limit': 'PSD is the analytic projection-block argument, not a numerical test.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'cases': len(cases),
                      'rlt_inequalities': sum(c['rlt_inequalities'] for c in cases)}))
