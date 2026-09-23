"""Independent exact enumeration of the reduced profile normal universe."""
from itertools import combinations, product
from math import gcd, lcm
from functools import reduce
from pathlib import Path
import json
from sympy import Matrix

results = []
for m in range(1, 5):
    normals = sorted(set(product((0, 1), repeat=m)) - {(0,) * m}
                     | {tuple(-int(i == j) for i in range(m)) for j in range(m)}
                     | {(-1,) * m})
    circuits = []
    for size in range(2, m + 2):
        for support in combinations(normals, size):
            kernel = Matrix(support).T.nullspace()
            if len(kernel) != 1:
                continue
            v = kernel[0]
            if not (all(x > 0 for x in v) or all(x < 0 for x in v)):
                continue
            denom = lcm(*(int(x.q) for x in v))
            weights = [abs(int(x * denom)) for x in v]
            common = reduce(gcd, weights)
            weights = [x // common for x in weights]
            assert Matrix(support).T * Matrix(weights) == Matrix.zeros(m, 1)
            circuits.append({'normals': support, 'weights': weights})
    if m <= 3:
        assert len(circuits) == (1, 5, 16)[m - 1]
        assert max(max(c['weights']) for c in circuits) == (1, 1, 2)[m - 1]
    results.append({'labels': m, 'normals': len(normals), 'circuits': len(circuits),
                    'max_weight': max(max(c['weights']) for c in circuits),
                    'library': circuits})
    print({k: v for k, v in results[-1].items() if k != 'library'}, flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'status': 'PASS', 'results': results}, indent=2) + '\n')
