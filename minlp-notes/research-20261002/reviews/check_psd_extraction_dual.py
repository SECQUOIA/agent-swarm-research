"""Exact symbolic dual certificate for the universal PSD extraction bound."""

from itertools import combinations, product
from fractions import Fraction as Q
from pathlib import Path
import sys
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "new-direction"))
from check_geometric_copositive import grid


d = sp.Symbol("d", positive=True)
epsilon = sp.Rational(1, 100)
signs = sp.Matrix([1, -1, 1, -1, 1])
identity = sp.eye(5)
inverse_scale = sp.diag(1/d, 1, 1, 1, 1)
rays = sp.Matrix.hstack(*(inverse_scale * (identity[:, i] + identity[:, (i+1) % 5])
                         for i in range(5)))
dual_core = 5 * identity - signs * signs.T
assert dual_core * dual_core == 5 * dual_core
minors = 0
for size in range(1, 6):
    for indices in combinations(range(5), size):
        assert dual_core.extract(indices, indices).det() >= 0
        minors += 1
dual = d*d/4 * rays * dual_core * rays.T
claimed = 5*d*d/4 * rays * rays.T - identity[:, 0] * identity[:, 0].T
assert sp.simplify(dual - claimed) == sp.zeros(5)
ray_budget = sp.simplify(5*d*d/4 * epsilon * sum((rays[:, i].dot(rays[:, i])) for i in range(5)))
assert ray_budget == d*d/10 + sp.Rational(1, 40)
residual = sp.expand(d*d + epsilon - ray_budget)
assert sp.expand(residual - sp.Rational(177, 200)*d*d - sp.Rational(3, 200)*(d*d-1)) == 0
print(f"{minors} exact dual-core principal minors; universal symbolic factorization and ray-budget constants passed")

thresholds = 0
for scale, exponent in product((1, 2, 3, 7, 16, 2**20, 2**200), (1, 2, 3, 4, 8, 16, 20, 21, 100, 200, 201)):
    delta = Q(1, 2**exponent)
    smallest_curvature = Q(7, 4)*scale*scale
    smallest_sigma = smallest_curvature*delta*delta/8
    axis_upper = Q(101, 100) - Q(11, 5)*smallest_sigma
    if axis_upper > 0:
        assert 16/(delta*delta) > 7*scale*scale
        assert 1/delta > Q(scale, 2)
    if 1/delta <= Q(scale, 2):
        assert axis_upper < 0
    thresholds += 1
for delta in (Q(1, 2), Q(1, 4), Q(1, 8)):
    nodes = grid(5, delta)
    assert all(b-a <= delta for a, b in zip(nodes, nodes[1:]))
    assert len(nodes) >= 1 + 1/delta
print(f"{thresholds} exact axis-threshold checks; 3 actual common-grid interval/count checks passed")
