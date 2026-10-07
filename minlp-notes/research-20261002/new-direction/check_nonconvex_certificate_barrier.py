"""Targeted exact checks for nonconvex-certificate-barrier.md."""

from fractions import Fraction as Q
from itertools import product
from random import Random


def objective(x, y, u, v):
    return (x-y)**2 + u*u + v*v - 3*u*v + (u+v)/2 + (x-y)*(u-v)/4


def widths(grid):
    return {
        r: max(
            ([r-grid[j-1]] if j else [])
            + ([grid[j+1]-r] if j+1 < len(grid) else [])
        )
        for j, r in enumerate(grid)
    }


mesh = [Q(j, 8) for j in range(9)]
growth_checks = 0
for x, y, u, v in product(mesh, repeat=4):
    a, t, d = x-y, (u+v)/2, (u-v)/2
    m2 = min(t*t, (1-t)**2)
    distance2 = a*a/2 + min(u*u+v*v, (1-u)**2+(1-v)**2)
    remainder = Q(3, 4)*a*a + a*d/2 + 4*d*d + t*(1-t)-m2
    assert distance2 == a*a/2 + 2*m2 + 2*d*d
    assert objective(x, y, u, v) - distance2/2 == remainder >= 0
    assert (objective(x, y, u, v) == 0) == (
        x == y and (u, v) in ((0, 0), (1, 1))
    )
    growth_checks += 1

rng = Random(20261002)
witness_checks = 0
for _ in range(200):
    grids = [
        sorted({Q(0), Q(1)} | {Q(rng.randrange(1, 128), 128)
                              for _ in range(rng.randrange(0, 14))})
        for _ in range(4)
    ]
    lengths = [widths(grid) for grid in grids]
    for i, j in ((0, 1), (1, 0)):
        delta = max(lengths[i].values())
        point = [Q(0)]*4
        point[i] = max(grids[i], key=lengths[i].get)
        point[j] = min(grids[j], key=lambda r: abs(r-point[i]))
        assert (point[i]-point[j])**2 <= lengths[j][point[j]]**2/4
        corrected = objective(*point) - sum(
            lengths[k][point[k]]**2 for k in range(4)
        )/4
        assert corrected <= -delta*delta/4
        witness_checks += 1

print(f"Passed {growth_checks} growth identities and {witness_checks} arbitrary-grid witnesses.")
