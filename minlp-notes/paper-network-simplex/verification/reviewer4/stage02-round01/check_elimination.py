"""Independent exact checks of cycle restriction and all admissible pivots."""
import itertools
import json
from pathlib import Path
import sympy as sp


def rank_of_components(n, edges):
    parent = list(range(n))

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for a, b in edges:
        parent[root(a)] = root(b)
    return len(edges) - n + len({root(v) for v in range(n)})


models = [
    (1, [(0, 0)]),
    (2, [(0, 1), (1, 0), (0, 1), (1, 1)]),
    (3, [(0, 1), (2, 1), (2, 0)]),
    (4, [(a, b) for a in range(4) for b in range(a + 1, 4)]),
    (5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
    (6, [(0, v) for v in range(2, 6)] + [(v, 1) for v in range(2, 6)]),
]
counts = {"models": len(models), "observation_patterns": 0, "pivot_choices": 0,
          "checked_path_rows": 0}
for n, edges in models:
    incidence = sp.zeros(n, len(edges))
    for e, (a, b) in enumerate(edges):
        incidence[a, e] -= 1
        incidence[b, e] += 1
    reduced = incidence[:-1, :]
    tree = list(reduced.rref()[1])
    chords = [e for e in range(len(edges)) if e not in tree]
    r = len(chords)
    c = sp.zeros(len(edges), r)
    if tree:
        tree_part = -reduced[:, tree].inv() * reduced[:, chords]
        for i, e in enumerate(tree):
            c[e, :] = tree_part[i, :]
    for j, e in enumerate(chords):
        c[e, j] = 1
    assert incidence * c == sp.zeros(n, r)
    for mask in range(1 << len(edges)):
        obs = [e for e in range(len(edges)) if (mask >> e) & 1]
        unobs = [e for e in range(len(edges)) if e not in obs]
        obs_rows = c[obs, :]
        d = obs_rows.rank()
        assert r - d == rank_of_components(n, [edges[e] for e in unobs])
        counts["observation_patterns"] += 1
        independent = list(obs_rows.T.rref()[1])
        selected = obs_rows[independent, :]
        for pivots in itertools.combinations(range(r), d):
            pivots = list(pivots)
            free = [j for j in range(r) if j not in pivots]
            basis = selected[:, pivots]
            if basis.det() == 0:
                continue
            assert abs(basis.det()) == 1
            counts["pivot_choices"] += 1
            for p in range(len(edges)):
                w = c[p:p+1, pivots] * basis.inv()
                rem = c[p:p+1, free] - w * selected[:, free]
                assert all(v in (-1, 0, 1) for v in w)
                assert all(v in (-1, 0, 1) for v in rem)
                assert c[p:p+1, :] == w * selected + rem * sp.eye(r)[free, :]
                counts["checked_path_rows"] += 1
counts["status"] = "PASS"
Path(__file__).with_suffix('.json').write_text(json.dumps(counts, indent=2) + '\n')
print(json.dumps(counts))
