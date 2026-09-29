"""Exact finite checks for the star epigraph exposed-face decomposition.

Run only this file for the associated research note. Fraction arithmetic checks
small instances and degeneracies; it does not establish the theorem or novelty.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def check_case(a, b, d, c, delta):
    n = len(b)
    assert a > sum((b[i] ** 2 / d[i] for i in range(n)), F(0))
    records = []
    for z in product((0, 1), repeat=n + 1):
        chosen = [i for i in range(n) if z[i + 1]]
        if z[0]:
            r = (c[0] - sum((b[i] * c[i + 1] / d[i] for i in chosen), F(0))) / (
                a - sum((b[i] ** 2 / d[i] for i in chosen), F(0))
            )
        else:
            r = F(0)
        x = (r,) + tuple(
            (c[i + 1] - b[i] * r) / d[i] if z[i + 1] else F(0)
            for i in range(n)
        )
        q = a * r**2 + sum(
            (2 * b[i] * r * x[i + 1] + d[i] * x[i + 1] ** 2 for i in range(n)),
            F(0),
        )
        cx = sum((c[i] * x[i] for i in range(n + 1)), F(0))
        assert q == cx
        value = sum((delta[i] * z[i] for i in range(n + 1)), F(0)) - cx
        records.append((z, x, q, value))

    minimum = min(record[3] for record in records)
    optimal = [record for record in records if record[3] == minimum]
    groups = {}
    for record in optimal:
        groups.setdefault((record[0][0], record[1][0]), []).append(record)
    assert len(groups) <= 2 * n + 2
    for (root_on, r), group in groups.items():
        gaps = [delta[i + 1] - (c[i + 1] - b[i] * r) ** 2 / d[i] for i in range(n)]
        choices = [(1,) if gap < 0 else (0,) if gap > 0 else (0, 1) for gap in gaps]
        expected = {(root_on,) + leaves for leaves in product(*choices)}
        actual = {record[0] for record in group}
        assert actual == expected
        if root_on:
            for i, gap in enumerate(gaps):
                if gap == 0 and b[i] != 0:
                    assert delta[i + 1] == 0
                    assert c[i + 1] - b[i] * r == 0
    return len(records), len(optimal), len(groups)


def main():
    rng = Random(20260925)
    cases = []
    for n in range(1, 7):
        for _ in range(12):
            b = [F(rng.randint(-2, 2), 3) for _ in range(n)]
            d = [F(rng.randint(1, 3)) for _ in range(n)]
            a = F(1) + sum((b[i] ** 2 / d[i] for i in range(n)), F(0))
            c = [F(rng.randint(-2, 2)) for _ in range(n + 1)]
            delta = [F(rng.randint(-2, 4), 2) for _ in range(n + 1)]
            cases.append((a, b, d, c, delta))

    # Every support ties at x=0, including root-on/root-off copies.
    cases.append((F(2), [F(1, 4)] * 5, [F(1)] * 5, [F(0)] * 6, [F(0)] * 6))
    # Nonzero continuous leaf values can vary in a tied cube when b_i=0.
    cases.append((F(1), [F(0)] * 5, [F(1)] * 5, [F(0)] + [F(1)] * 5, [F(0)] + [F(1)] * 5))
    # Two distinct globally minimizing center values, r=+/-4/15.
    cases.append((F(1), [F(1, 4)] * 2, [F(1)] * 2, [F(0), F(1), F(-1)], [F(0), F(1), F(1)]))
    # Four distinct center minima for two leaves: 0, 8/5, -4/5, 4.
    cases.append((F(9, 4), [F(1)] * 2, [F(1)] * 2, [F(0), F(-2), F(1)], [F(0), F(36, 5), F(9, 5)]))
    # Root-off minimizers can have a cube of nonzero tied leaf values.
    cases.append((F(2), [F(1, 4)] * 5, [F(1)] * 5, [F(0)] + [F(1)] * 5, [F(10)] + [F(1)] * 5))

    totals = [check_case(*case) for case in cases]
    print(f"PASS: {len(cases)} cases; {sum(row[0] for row in totals)} exact support checks")
    print(f"Maximum optimal supports in one case: {max(row[1] for row in totals)}")
    print(f"Maximum center/root groups in one case: {max(row[2] for row in totals)}")


if __name__ == "__main__":
    main()
