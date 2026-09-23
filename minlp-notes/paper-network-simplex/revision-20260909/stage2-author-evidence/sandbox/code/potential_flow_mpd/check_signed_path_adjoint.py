"""Exact checks of the signed-path refinement's new proof obligation."""
from fractions import Fraction as Q
from random import Random


def main():
    rng = Random(9052026)
    paths = levels = returning = zeros = 0
    for sign in (-1, 1):
        for length in range(2, 18):
            for mode in range(6):
                resistance = [Q(rng.randrange(1, 12), rng.randrange(1, 9)) for _ in range(length)]
                source = [sign * Q(rng.randrange(0, 6), 7) for _ in range(length - 1)]
                zeros += source.count(0)
                delta = Q(1, 13)
                offset = [Q(0)]
                for value in source:
                    offset.append(offset[-1] + value + sign * delta)
                if mode == 0:
                    initial = -sum(r * o for r, o in zip(resistance, offset)) / sum(resistance)
                    returning += 1
                elif mode == 1:
                    initial = -offset[len(offset) // 2]
                else:
                    initial = Q(rng.randrange(-20, 21), 9)
                current = [initial + value for value in offset]
                potential = [Q(0)]
                for r, j in zip(resistance, current):
                    potential.append(potential[-1] - r * j)
                if mode == 0:
                    assert potential[-1] == potential[0]
                for i, value in enumerate(source):
                    assert current[i + 1] - current[i] == value + sign * delta
                internal = potential[1:-1]
                knots = sorted(set(internal))
                thresholds = knots + [(a + b) / 2 for a, b in zip(knots, knots[1:])]
                thresholds += [knots[0] - 1, knots[-1] + 1]
                for threshold in thresholds:
                    assert internal.count(threshold) <= 2
                    middle = [i for i, value in enumerate(internal) if sign * (value - threshold) > 0]
                    assert not middle or middle == list(range(middle[0], middle[-1] + 1))
                    levels += 1
                paths += 1
    print(f"PASS: {paths} signed paths; {returning} returning paths; {zeros} zero source coefficients; {levels} exact threshold checks")


if __name__ == "__main__":
    main()
