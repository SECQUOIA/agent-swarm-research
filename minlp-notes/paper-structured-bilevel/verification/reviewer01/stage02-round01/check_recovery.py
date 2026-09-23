"""Independent finite checks of the support-tuple reconstruction claim.

The oracle enumerates every original Cartesian tuple. It does not run QE or
claim to verify asymptotic complexity. All decisions use exact Q(sqrt(2)).
"""
from itertools import combinations, product
import json
from pathlib import Path
import sympy as s

root = s.sqrt(2)
field = s.QQ.algebraic_field(root)


def clean(v):
    return tuple(s.expand(s.radsimp(x)) for x in v)


def add(points):
    return clean(sum((s.Matrix(p) for p in points), s.zeros(2, 1)))


def nonnegative(x):
    x = s.simplify(x)
    assert x.is_nonnegative is not None, x
    return bool(x.is_nonnegative)


def support_tuples(blocks):
    rays = {(s.Integer(1), s.Integer(0)), (s.Integer(0), s.Integer(1))}
    for block in blocks:
        for a, b in combinations(block, 2):
            delta = clean(s.Matrix(a) - s.Matrix(b))
            if delta != (0, 0):
                rays.add((-delta[1], delta[0]))
    rays |= {(-p[0], -p[1]) for p in list(rays)}
    # In two dimensions, adjacent ray sums meet each open angular chamber.
    directions = rays | {add((a, b)) for a, b in combinations(rays, 2)} | {(0, 0)}
    selected = set()
    for v in directions:
        ids = []
        for block in blocks:
            best = 0
            for i in range(1, len(block)):
                diff = s.Matrix(v).dot(s.Matrix(block[i]) - s.Matrix(block[best]))
                if diff != 0 and nonnegative(diff):
                    best = i
            ids.append(best)
        selected.add(tuple(ids))
    return sorted(selected), len(directions)


def recover(aggregates, target):
    rhs = s.Matrix((*target, 1))
    for count in (1, 2, 3):
        for ids in combinations(range(len(aggregates)), count):
            mat = s.Matrix.hstack(*(s.Matrix((*aggregates[j], 1)) for j in ids))
            if mat.rank() != count:
                continue
            for rows in combinations(range(3), count):
                square = mat[list(rows), :]
                if square.det() == 0:
                    continue
                weights = square.inv() * rhs[list(rows), :]
                if any(s.simplify(v) != 0 for v in mat * weights - rhs):
                    break
                if all(nonnegative(v) for v in weights):
                    for v in weights:
                        field.from_sympy(s.simplify(v))
                    return ids, weights
                break
    raise AssertionError((aggregates, target))


cases = {
    "algebraic_zonotope": [
        [(0, 0), (root, 1)],
        [(0, 0), (-1, root)],
        [(root, -1), (root, -1)],
    ],
    "triangles_and_segment": [
        [(0, 0), (1, root), (root, -1)],
        [(-1, 0), (0, 2), (1, 0)],
        [(0, 0), (1, -root)],
    ],
    "lower_dimensional": [
        [(0, 0), (root, 2 * root)],
        [(1, 2), (2, 4)],
        [(0, 0)],
    ],
    "singletons": [[(root, 1)], [(-root, -1)]],
    "no_blocks": [],
}
report = {}
for name, blocks in cases.items():
    tuples, direction_count = support_tuples(blocks)
    aggregates = [add(blocks[b][j] for b, j in enumerate(ids)) for ids in tuples]
    original = [add(p) for p in product(*blocks)]
    targets = original[:]
    if len(original) >= 2:
        weight = root / 2
        targets.append(clean(weight * s.Matrix(original[0]) + (1 - weight) * s.Matrix(original[-1])))
        targets.append(clean(sum((s.Matrix(p) for p in original), s.zeros(2, 1)) / len(original)))
    max_count = 0
    for target in targets:
        ids, weights = recover(aggregates, target)
        recovered = []
        for b in range(len(blocks)):
            recovered.append(clean(sum((weights[j] * s.Matrix(blocks[b][tuples[i][b]]) for j, i in enumerate(ids)), s.zeros(2, 1))))
        assert add(recovered) == clean(target)
        assert s.simplify(sum(weights) - 1) == 0
        max_count = max(max_count, len(ids))
    report[name] = {"cartesian_tuples": len(original), "support_tuples": len(tuples), "directions": direction_count, "targets_recovered": len(targets), "maximum_support": max_count}

print(json.dumps(report, indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
