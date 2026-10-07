"""Exact small-instance checks of the core-box refinement algorithm.

The independent oracle enumerates active faces. It is a verification oracle,
not the polynomial forest oracle in the theorem.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def solve(a, b):
    n = len(b)
    aug = [[F(v) for v in row] + [F(bi)] for row, bi in zip(a, b)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        d = aug[j][j]
        aug[j] = [v / d for v in aug[j]]
        for i in range(n):
            if i != j:
                d = aug[i][j]
                aug[i] = [u - d * v for u, v in zip(aug[i], aug[j])]
    return [aug[i][-1] for i in range(n)]


def value(a, b, x):
    return sum((b[i] * x[i] for i in range(len(x))), F(0)) + sum(
        (x[i] * a[i][j] * x[j] / 2
         for i in range(len(x)) for j in range(len(x))), F(0))


def face_oracle(a, b, bounds, fixed=None):
    fixed = dict(fixed or {})
    rest = [i for i in range(len(b)) if i not in fixed]
    best = None
    for face in product((-1, 0, 1), repeat=len(rest)):
        assigned = dict(fixed)
        free = []
        for i, state in zip(rest, face):
            if state:
                assigned[i] = bounds[i][0 if state < 0 else 1]
            else:
                free.append(i)
        solution = solve([[a[i][j] for j in free] for i in free],
                         [-b[i] - sum(a[i][j] * xj for j, xj in assigned.items())
                          for i in free])
        if solution is None:
            continue
        assigned.update(zip(free, solution))
        x = tuple(assigned[i] for i in range(len(b)))
        if not all(lo <= xi <= hi for xi, (lo, hi) in zip(x, bounds)):
            continue
        vx = value(a, b, x)
        if best is None or vx < best[0]:
            best = vx, x
    assert best is not None
    return best


def split(box, lower, step):
    choices = []
    for (lo, hi), origin in zip(box, lower):
        # Global dyadic planes, not midpoint bisection of a clipped interval.
        first = (lo - origin) // step + 1
        cut = origin + first * step
        choices.append([(lo, cut), (cut, hi)] if cut < hi else [(lo, hi)])
    return list(product(*choices))


def check_instance(a, b, bounds, r, eps):
    optimum, _ = face_oracle(a, b, bounds)
    curvatures = [max(F(0), a[i][i]) for i in range(r)]
    active = [tuple(bounds[:r])]
    lower = [lo for lo, _ in bounds[:r]]
    step = max(hi - lo for lo, hi in bounds[:r])
    cache = {}
    incumbent = None
    boxes_seen = max_active = 0
    history = []
    for level in range(40):
        scored = []
        for box in active:
            boxes_seen += 1
            corner_values = []
            for corner in product(*box):
                if corner not in cache:
                    cache[corner] = face_oracle(a, b, bounds, enumerate(corner))
                vx, point = cache[corner]
                corner_values.append(vx)
                if incumbent is None or vx < incumbent[0]:
                    incumbent = vx, point
            error = sum((curvature * (hi - lo) ** 2 / 8
                         for curvature, (lo, hi) in zip(curvatures, box)), F(0))
            scored.append((min(corner_values) - error, box))
        active = [box for lb, box in scored if lb < incumbent[0]]
        lb = min([incumbent[0]] + [bound for bound, box in scored
                                  if bound < incumbent[0]])
        assert lb <= optimum <= incumbent[0]
        assert incumbent[0] - lb <= max(curvatures) * r * step ** 2 / 8
        max_active = max(max_active, len(active))
        history.append((level, len(active), incumbent[0] - lb))
        if incumbent[0] - lb <= eps:
            assert value(a, b, incumbent[1]) == incumbent[0]
            return boxes_seen, len(cache), max_active, history
        step /= 2
        active = [child for box in active for child in split(box, lower, step)]
    raise AssertionError(("failed to meet target", history))


def main():
    rng = Random(20261002)
    totals = [0, 0]
    count = 0
    # Random fan slices: the residual induced graph is a path.
    for r in (1, 2):
        n = r + 2
        for case in range(6):
            a = [[F(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if i < r or j == i + 1:
                        a[i][j] = a[j][i] = F(rng.choice([-2, -1, 1, 2]), 5)
            for i in range(n):
                a[i][i] = 1 + sum(abs(a[i][j]) for j in range(n))
            b = [F(rng.randrange(-8, 9), 7) for _ in range(n)]
            bounds = [(F(-1), F(1)) for _ in range(n)]
            if case % 3 == 0:
                # Nonconvex residual coordinate forced to its lower bound.
                a[-1][-1] = F(-1)
                b[-1] = F(5)
                bounds[-1] = (F(0), F(1))
            if r == 2 and case == 5:
                bounds[1] = (F(0), F(1, 1024))
            stats = check_instance(a, b, bounds, r, F(1, 4096))
            totals[0] += stats[0]
            totals[1] += stats[1]
            count += 1

    # Unique optimal core; every residual value is globally optimal at it.
    a = [[F(2), F(0)], [F(0), F(0)]]
    b = [F(-2, 3), F(0)]
    stats = check_instance(a, b, [(F(0), F(1))] * 2, 1, F(1, 4096))
    totals[0] += stats[0]
    totals[1] += stats[1]
    count += 1

    # Endpoint-only core curvature: the root lower bound is already exact.
    a = [[F(-1), F(1, 4)], [F(1, 4), F(2)]]
    stats = check_instance(a, [F(0), F(1, 3)],
                           [(F(-1), F(1))] * 2, 1, F(0))
    assert len(stats[3]) == 1 and stats[3][0][2] == 0
    totals[0] += stats[0]
    totals[1] += stats[1]
    count += 1
    print(f"PASS: {count} adaptive core-refinement instances; "
          f"{totals[0]} generated boxes; {totals[1]} exact residual calls.")
    print("PASS: every level's lower/upper interval and mesh-error bound; "
          "nonconvex slices, clipped anisotropic domain, flat recourse, "
          "and endpoint-only root certificate.")


if __name__ == "__main__":
    main()
