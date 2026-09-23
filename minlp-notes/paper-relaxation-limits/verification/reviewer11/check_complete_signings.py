"""Exact finite center ratios; switching reduces enumeration, integer arithmetic."""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np


def check(n):
    edges = list(combinations(range(n), 2))
    m = len(edges)
    # Switching a_ij to a_ij*t_i*t_j permutes vertex-sign values of Q.
    # Every full signing has a representative with every 0-j edge positive.
    free = [k for k, (i, j) in enumerate(edges) if i != 0]
    vertex_signs = np.array([(1,) + s for s in product((-1, 1), repeat=n-1)], dtype=np.int64)
    chars = np.array([vertex_signs[:, i] * vertex_signs[:, j] for i, j in edges])
    best_osc = 2*m + 1
    witness = None
    count = 1 << len(free)
    for first in range(0, count, 1024):
        idx = np.arange(first, min(first + 1024, count), dtype=np.int64)
        coeff = np.ones((len(idx), m), dtype=np.int64)
        coeff[:, free] = 2*((idx[:, None] >> np.arange(len(free))) & 1)-1
        values = coeff @ chars
        oscillations = values.max(axis=1)-values.min(axis=1)
        k = int(oscillations.argmin())
        if int(oscillations[k]) < best_osc:
            best_osc = int(oscillations[k])
            witness = coeff[k].tolist()
    ratio = Fraction(2*m, best_osc)
    expected = {3: Fraction(3,2), 4: Fraction(3,2), 5: Fraction(5,2), 6: Fraction(3), 7: Fraction(21,8)}
    assert ratio == expected[n]
    return dict(n=n, switching_representatives=count, edges=edges,
                max_center_ratio=str(ratio), witness=witness, min_Q_oscillation=best_osc)


if __name__ == '__main__':
    rows = [check(n) for n in range(3,8)]
    result = json.dumps(rows, indent=2)
    Path(__file__).with_name('complete_signings.json').write_text(result+'\n')
    print(result)
