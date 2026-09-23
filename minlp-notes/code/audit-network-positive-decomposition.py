"""Independent exact tests of the theta-block suffix decomposition.

Generates feasible sums directly, then checks the proposed decomposition against
the original six inequalities of every state. No LP solver is used.
"""

from fractions import Fraction as F
from random import Random


def supports(bounds):
    (ls, us), (lt, ut), (ld, ud) = bounds
    return (
        (max(ls, ld - ut), min(us, ud - lt)),
        (max(lt, ld - us), min(ut, ud - ls)),
        (max(ld, ls + lt), min(ud, us + ut)),
    )


def feasible(point, bounds):
    s, t = point
    return all(lo <= value <= hi for value, (lo, hi) in zip((s, t, s + t), bounds))


def decompose(total, polygons):
    suffix = [[(F(0), F(0))] * 3 for _ in range(len(polygons) + 1)]
    for i in range(len(polygons) - 1, -1, -1):
        tight = supports(polygons[i])
        suffix[i] = [(lo + suffix[i + 1][h][0], hi + suffix[i + 1][h][1])
                     for h, (lo, hi) in enumerate(tight)]
    remaining = tuple(total)
    result = []
    for i, bounds in enumerate(polygons):
        rs, rt = remaining
        residuals = (rs, rt, rs + rt)
        intersection = [
            (max(lo, residuals[h] - suffix[i + 1][h][1]),
             min(hi, residuals[h] - suffix[i + 1][h][0]))
            for h, (lo, hi) in enumerate(bounds)
        ]
        (ls, us), (lt, ut), (ld, ud) = intersection
        s = max(ls, ld - ut)
        t = max(lt, ld - s)
        assert feasible((s, t), intersection)
        assert feasible((s, t), bounds)
        result.append((s, t))
        remaining = (rs - s, rt - t)
    assert remaining == (0, 0)
    assert tuple(sum(point[h] for point in result) for h in range(2)) == tuple(total)
    return result


def main():
    rng = Random(20260904)
    states = 0
    for case in range(400):
        polygons, witnesses = [], []
        for _ in range(rng.randrange(1, 9)):
            if rng.randrange(7) == 0:
                point = (F(0), F(0))
                bounds = [(F(0), F(0))] * 3
            else:
                point = tuple(F(rng.randrange(-8, 9), rng.randrange(1, 5)) for _ in range(2))
                bounds = [
                    (value - F(rng.randrange(4), rng.randrange(1, 5)),
                     value + F(rng.randrange(4), rng.randrange(1, 5)))
                    for value in (point[0], point[1], sum(point))
                ]
            assert feasible(point, bounds)
            polygons.append(bounds)
            witnesses.append(point)
        total = tuple(sum(point[h] for point in witnesses) for h in range(2))
        decompose(total, polygons)
        states += len(polygons)
    print(f"Passed 400 exact theta decomposition instances containing {states} states.")


if __name__ == "__main__":
    main()
