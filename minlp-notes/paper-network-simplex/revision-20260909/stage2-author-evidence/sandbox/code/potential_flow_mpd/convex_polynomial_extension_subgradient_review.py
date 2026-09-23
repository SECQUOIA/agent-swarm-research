"""Independent exact checks of perspective-extension subgradients at ties."""

from fractions import Fraction as F
from itertools import product
from random import Random


rng = Random(41029)
checks = 0
for k in range(1, 4):
    v_bound = F(17 + 7 * k + k * k + k * (k + 1) // 2)
    g_bound = F(16 + 3 * k)
    penalty = 1 + v_bound + k * g_bound
    lipschitz = g_bound + 1 + 2 * (v_bound + k * g_bound)

    def h(z):
        # Convex on the cube, but not globally convex.
        return -17 + sum(6 * x * x - x**4 + (i + 1) * x
                         for i, x in enumerate(z)) + sum(z)**2

    def dh(z):
        return [12 * x - 4 * x**3 + i + 1 + 2 * sum(z)
                for i, x in enumerate(z)]

    def extension(z):
        t = max(F(1), max(map(abs, z)))
        return t * h([x / t for x in z]) + penalty * (t - 1)

    targets = [tuple(F(rng.randrange(-15, 16), 3) for _ in range(k))
               for _ in range(20)]
    for point in product(map(F, (-3, -1, 0, 1, 3)), repeat=k):
        norm = max(map(abs, point))
        t = max(F(1), norm)
        w = [x / t for x in point]
        gradient = dh(w)
        radial = h(w) - sum(a * b for a, b in zip(gradient, w)) + penalty
        assert 1 <= radial <= 1 + 2 * (v_bound + k * g_bound)
        gauges = []
        if norm <= 1:
            gauges.append([F(0)] * k)
        if norm >= 1:
            for i, x in enumerate(point):
                if abs(x) == norm:
                    gauge = [F(0)] * k
                    gauge[i] = F(1 if x > 0 else -1)
                    gauges.append(gauge)
        for gauge in gauges:
            subgradient = [a + radial * b for a, b in zip(gradient, gauge)]
            assert all(abs(a) <= lipschitz for a in subgradient)
            for target in targets:
                support = extension(point) + sum(
                    a * (y - x) for a, x, y in zip(subgradient, point, target)
                )
                assert extension(target) >= support
                checks += 1

print(f"PASS: {checks} exact global supporting inequalities, including cube "
      "boundaries and tied maximum coordinates, in dimensions 1--3.")
