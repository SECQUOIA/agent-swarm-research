"""Independent checks of exact supporting bounds and nonsmooth abstention."""
from fractions import Fraction as F

import pyomo.environ as pe
import pytest

from certify.convexity import CONVEX, UNKNOWN, certify
from certify.driver import _verify_given_cut
from certify.exact_model import exact_constraint_rows
from certify.safecut import SafeCutter


@pytest.mark.parametrize('side', ['lower', 'upper', 'free'])
def test_omitted_linear_slope_still_contributes_to_support_bound(side):
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-2, 2))
    bounds, coefficient = {
        'lower': ((-3, None), 3),
        'upper': ((None, 3), -3),
        'free': ((None, None), 3),
    }[side]
    m.y = pe.Var(bounds=bounds)
    m.c = pe.Constraint(expr=m.x**2 + coefficient*m.y + 5 <= 0)
    row, = exact_constraint_rows(m.c)
    cutter = SafeCutter(row, {id(m.x): (F(-2), F(2)), id(m.y): bounds})
    result = _verify_given_cut(cutter, row,
        {id(m.x): F(1), id(m.y): F(1)}, {'x': F(2)},
        {'x': m.x, 'y': m.y})
    if side == 'free':
        assert result is None  # The omitted y slope is zero, leaving residual 3.
    else:
        # phi = (x-1)^2 + coefficient*y + 4 has exact minimum -5.
        # Both endpoint orientations must produce this same support bound.
        assert result == -5


def test_norm_origin_abstains_despite_existence_of_finite_subgradients():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-1, 1))
    m.y = pe.Var(bounds=(-1, 1))
    m.c = pe.Constraint(expr=pe.sqrt(m.x*m.x + m.y*m.y) <= 1)
    assert certify(m.c.body).curv == CONVEX
    row, = exact_constraint_rows(m.c)
    cutter = SafeCutter(row, {id(m.x): (F(-1), F(1)), id(m.y): (F(-1), F(1))})
    # A zero subgradient exists, but the implemented gradient route cannot
    # infer it by replacing the undefined symbolic derivative with zero.
    with pytest.raises(ValueError):
        _verify_given_cut(cutter, row, {id(m.x): F(0), id(m.y): F(0)},
            {}, {'x': m.x, 'y': m.y})


@pytest.mark.parametrize('xbounds,ybounds,expected', [
    ((1, None), (2, 3), (2, None)),
    ((None, -1), (-3, -2), (2, None)),
    ((1, None), (-3, -2), (None, -2)),
    ((None, -1), (2, 3), (None, -2)),
    ((-2, 3), (-4, 5), (-12, 15)),
    ((-1, None), (0, None), (None, None)),
])
def test_product_domain_range_does_not_claim_product_curvature(xbounds, ybounds, expected):
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=xbounds)
    m.y = pe.Var(bounds=ybounds)
    result = certify(m.x*m.y)
    # Product sign can justify a surrounding function's domain without
    # making this bilinear function convex or concave on any of these boxes.
    assert result.curv == UNKNOWN
    assert (result.lo, result.hi) == expected
