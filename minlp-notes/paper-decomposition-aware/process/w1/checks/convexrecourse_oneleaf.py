"""Exact check of the one-leaf ladder (growth 1/3 at the unique minimizer
u=y=a1, v=0) and of its instability: adding eps*sum(y) creates a clipped
piece on which the reduced curvature of u_i includes 2*M0."""
import random
from fractions import Fraction as Fr

random.seed(5)
a, eta = Fr(1, 3), Fr(1, 16)


def F(m, M0, u, v, y, eps=Fr(0)):
    tot = Fr(0)
    for i in range(m):
        tot += (u[i] - a) ** 2 - (u[i] - a) * v[i] - v[i] ** 2 + 3 * v[i] + M0 * (y[i] - u[i]) ** 2 + eps * y[i]
    for i in range(m - 1):
        tot += eta * ((u[i + 1] - u[i]) ** 2 + (v[i + 1] - v[i]) ** 2)
    return tot


n = 0
for m in [1, 2, 4]:
    for M0 in [Fr(1), Fr(37), Fr(10 ** 5)]:
        assert F(m, M0, [a] * m, [Fr(0)] * m, [a] * m) == 0
        for _ in range(500):
            r = lambda: Fr(random.randint(0, 600), 600)
            u, v, y = [r() for _ in range(m)], [r() for _ in range(m)], [r() for _ in range(m)]
            if random.random() < 0.5:
                u = [a + Fr(random.randint(-30, 30), 600) for _ in range(m)]
                y = [a + Fr(random.randint(-30, 30), 600) for _ in range(m)]
                v = [Fr(random.randint(0, 30), 600) for _ in range(m)]
            d2 = sum((u[i] - a) ** 2 + v[i] ** 2 + (y[i] - a) ** 2 for i in range(m))
            assert F(m, M0, u, v, y) >= d2 / 3
            n += 1
# instability: scalar value of min_y M0(y-u)^2 + eps*y on u in [0, eps/(2M0)]
for M0 in [Fr(2), Fr(1000)]:
    eps = Fr(1, 100)
    def val(u):
        y = max(Fr(0), min(Fr(1), u - eps / (2 * M0)))
        return M0 * (y - u) ** 2 + eps * y
    w = eps / (2 * M0)
    hs = w / 8
    d2 = (val(w / 2 + hs) - 2 * val(w / 2) + val(w / 2 - hs)) / hs ** 2
    assert d2 == 2 * M0
print(f"one-leaf ladder growth checks: {n}; instability checks passed")
