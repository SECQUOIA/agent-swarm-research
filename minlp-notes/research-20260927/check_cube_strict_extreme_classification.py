"""Exact finite cube-graph checks for the strict-regime classification.

This checks the 24 five-edge symmetry orbits and the asserted slack identities.
It does not formalize the continuous perturbation argument or prove novelty.
"""
from itertools import combinations, permutations, product

VERTICES = list(product((0, 1), repeat=3))
VI = {v: i for i, v in enumerate(VERTICES)}
EDGES = [
    (VI[v], VI[tuple(v[j] + int(j == k) for j in range(3))], k)
    for v in VERTICES for k in range(3) if v[k] == 0
]
EI = {tuple(sorted((a, b))): e for e, (a, b, _) in enumerate(EDGES)}
TRANSFORMS = []
for perm in permutations(range(3)):
    for complement in VERTICES:
        vertex_map = [
            VI[tuple(v[perm[j]] ^ complement[j] for j in range(3))]
            for v in VERTICES
        ]
        TRANSFORMS.append([
            EI[tuple(sorted((vertex_map[a], vertex_map[b])))]
            for a, b, _ in EDGES
        ])

def canonical(edges):
    return min(tuple(sorted(t[e] for e in edges)) for t in TRANSFORMS)

def three_on_face(edges):
    return any(
        sum(VERTICES[EDGES[e][0]][k] == value
            and VERTICES[EDGES[e][1]][k] == value for e in edges) >= 3
        for k in range(3) for value in (0, 1)
    )

def has_star(edges):
    return any(sum(v in EDGES[e][:2] for e in edges) == 3 for v in range(8))

ORBIT_REPS = sorted({canonical(edges) for edges in combinations(range(12), 5)})
assert len(ORBIT_REPS) == 24
# Coefficients of ell_e = s_a + s_b - d_direction.
SLACK_ROWS = []
for a, b, k in EDGES:
    row = [0] * 11
    row[a] = row[b] = 1
    row[8 + k] = -1
    SLACK_ROWS.append(row)
IDENTITIES = {
    'A': {1: -1, 2: 1, 3: -1, 5: 1, 10: 1, 11: -1},
    'B': {0: -1, 1: 1, 6: -1, 7: 1, 9: 1, 10: -1},
    'C': {0: 1, 1: -1, 6: 1, 7: -1, 9: -1, 10: 1},
}
for identity in IDENTITIES.values():
    assert all(sum(c * SLACK_ROWS[e][j] for e, c in identity.items()) == 0
               for j in range(11))
FORCING = {10: 'A', 19: 'B', 20: 'A', 22: 'A', 23: 'C'}
counts = {'face': 0, 'star': 0, 'forced_face': 0, 'cycle': 0, 'family': 0}
for index, edges in enumerate(ORBIT_REPS):
    edge_set = set(edges)
    if three_on_face(edges):
        counts['face'] += 1
        continue
    if has_star(edges):
        assert index == 7
        counts['star'] += 1
        continue
    if index == 16:
        assert canonical((0, 1, 6, 9, 11)) == edges
        counts['family'] += 1
        continue
    assert index in FORCING
    identity = IDENTITIES[FORCING[index]]
    # All negative terms vanish, so every positive term must vanish.
    assert all(e in edge_set for e, c in identity.items() if c < 0)
    expanded = edge_set | {e for e, c in identity.items() if c > 0}
    if index == 23:
        assert expanded == {0, 1, 6, 7, 9, 10}
        assert not three_on_face(expanded)
        assert all(sum(v in EDGES[e][:2] for e in expanded) in (0, 2)
                   for v in range(8))
        counts['cycle'] += 1
    else:
        assert three_on_face(expanded)
        counts['forced_face'] += 1
assert counts == {'face': 17, 'star': 1, 'forced_face': 4, 'cycle': 1, 'family': 1}
print('PASS: all 792 five-edge subsets reduce to 24 symmetry orbits.')
print('PASS: 17 face, 1 star, 4 forced-face, 1 six-cycle, 1 family orbit.')
print('PASS: all three edge-slack identities hold exactly.')
