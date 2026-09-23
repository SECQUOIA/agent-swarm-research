"""Independent exact checks of all pivots for three small cycle matrices."""
from itertools import combinations
import json
from pathlib import Path
import sympy as s

graphs = [
    (1, [(0, 0)], []),
    (2, [(0, 1), (1, 0), (0, 1), (1, 0)], [0]),
    (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], [0, 1, 2]),
]
counts = dict(graphs=0, square_minors=0, nonsingular_pivots=0, reconstructed_rows=0,
              observation_patterns=0)
for n, edges, tree in graphs:
    A = s.zeros(n, len(edges))
    for e, (u, v) in enumerate(edges):
        A[u, e] -= 1
        A[v, e] += 1
    chords = [e for e in range(len(edges)) if e not in tree]
    r = len(chords)
    C = s.zeros(len(edges), r)
    for j, e in enumerate(chords):
        C[e, j] = 1
    if tree:
        N = A[:-1, :]
        X = -N[:, tree].inv() * N[:, chords]
        for i, e in enumerate(tree):
            for j in range(r):
                C[e, j] = X[i, j]
    assert A * C == s.zeros(n, r)
    counts['graphs'] += 1
    for obs_count in range(len(edges) + 1):
        for observed in combinations(range(len(edges)), obs_count):
            unobserved = [e for e in range(len(edges)) if e not in observed]
            assert r - C[list(observed), :].rank() == len(unobserved) - A[:, unobserved].rank()
            counts['observation_patterns'] += 1
    for d in range(r + 1):
        for rows in combinations(range(len(edges)), d):
            D = C[list(rows), :]
            for cols in combinations(range(r), d):
                B = D[:, list(cols)]
                det = B.det()
                counts['square_minors'] += 1
                assert det in (-1, 0, 1)
                if not det:
                    continue
                counts['nonsingular_pivots'] += 1
                free = [j for j in range(r) if j not in cols]
                for i in range(len(edges)):
                    c = C[i, :]
                    W = c[:, list(cols)] * B.inv()
                    R = c[:, free] - W * D[:, free]
                    assert all(x in (-1, 0, 1) for x in list(W) + list(R))
                    counts['reconstructed_rows'] += 1
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(counts, indent=2) + '\n')
print(counts)
