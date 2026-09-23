"""Independent exact checks of the Stage 2 cycle-elimination identities."""
from itertools import combinations
import json
from pathlib import Path
import sympy as s

edges = list(combinations(range(4), 2))
A = s.zeros(4, 6)
for e, (u, v) in enumerate(edges):
    A[u, e], A[v, e] = -1, 1
# The first three K4 arcs are a star spanning tree.
N = A[1:, :]
C = (-N[:, :3].inv() * N[:, 3:]).col_join(s.eye(3))
assert A * C == s.zeros(4, 3)
checks = 0
for d in range(4):
    for selected in combinations(range(6), d):
        D = C.extract(selected, range(3))
        if D.rank() != d:
            continue
        for pivots in combinations(range(3), d):
            B = D.extract(range(d), pivots)
            if not B.det():
                continue
            free = [i for i in range(3) if i not in pivots]
            for row in range(6):
                ci = C.extract([row], pivots)
                W = ci * B.inv()
                R = C.extract([row], free) - W * D.extract(range(d), free)
                assert all(v in (-1, 0, 1) for v in list(W) + list(R))
                checks += 1

patterns = 0
for count in range(7):
    for observed in combinations(range(6), count):
        unobserved = [i for i in range(6) if i not in observed]
        nullity = len(unobserved) - A[:, unobserved].rank()
        assert 3 - C.extract(observed, range(3)).rank() == nullity
        patterns += 1

# Exact arithmetic for the concrete forest-complement gap.
x = [s.Rational(1, 2), s.Rational(1, 4), s.Rational(1, 4),
     s.Rational(1, 4), s.Rational(1, 4), s.Rational(1, 2)]
y, z = s.Rational(1, 2), s.Rational(1, 5)
assert A * s.Matrix(x) == s.Matrix([-1, 0, 0, 1])
for edge in (1, 2, 4):
    assert 0 <= z <= y and z <= x[edge] and z >= x[edge] - (1-y)
assert 3*z > y
out = {"status": "PASS", "exact_schur_row_checks": checks,
       "exact_observation_nullity_patterns": patterns,
       "k4_gap_exactly_checked": True}
Path(__file__).with_name("check-output.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out))
