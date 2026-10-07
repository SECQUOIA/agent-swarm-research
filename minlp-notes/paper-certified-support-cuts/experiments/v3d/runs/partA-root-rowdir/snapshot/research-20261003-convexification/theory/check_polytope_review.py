"""Independent analytic and adversarial checks of the polytope support oracle.

Expected optima come from analytic constructions or Boolean enumeration, never
from a second implementation of the oracle's active-face enumeration.
Run directly with the repository's SymPy-enabled Python environment.
"""

from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from random import Random

import sympy as sp

from quadratic_polytope import (
    EnumerationLimitError,
    coefficient_pairs,
    enumeration_size,
    polytope_vertices,
    replay_quadratic,
    support_quadratic,
)


CHECKS = []


def coefficients(expression, symbols):
    polynomial = sp.Poly(sp.expand(expression), *symbols)
    monomials = [sp.Integer(1), *symbols]
    monomials.extend(symbols[i] * symbols[j] for i, j in coefficient_pairs(len(symbols)))
    return tuple(F(str(polynomial.coeff_monomial(term))) for term in monomials)


def check_optimum(name, bounds, rows, terms, expected, point=None):
    result = support_quadratic(bounds, rows, terms)
    assert result["status"] == "complete", name
    assert F(result["bound"]) == expected, (name, result["bound"], expected)
    assert replay_quadratic(bounds, rows, terms, result), name
    if point is not None:
        assert tuple(map(F, result["minimizer"])) == tuple(map(F, point)), name
    CHECKS.append(name)
    return result


def run():
    x, y, z = xyz = sp.symbols("x y z")
    unit = [(0, 1)] * 3
    check_optimum("rank-one flat valley", unit, [],
                  coefficients((x + y + z - sp.Rational(1, 2)) ** 2, xyz), F(0))

    plane_rows = [(1, 2, -1, 0), (-1, -2, 1, 0)]
    bowl = (x - sp.Rational(1, 3)) ** 2 + (y - sp.Rational(2, 5)) ** 2
    check_optimum("skew plane with singular ambient Hessian", [(0, 1), (0, 1), (0, 3)],
                  plane_rows, coefficients(bowl, xyz), F(0), (F(1, 3), F(2, 5), F(17, 15)))
    check_optimum("skew plane with indefinite ambient Hessian", [(0, 1), (0, 1), (0, 3)],
                  plane_rows, coefficients(bowl - (z - x - 2 * y) ** 2, xyz),
                  F(0), (F(1, 3), F(2, 5), F(17, 15)))

    line_rows = [(1, -1, 0, 0), (-1, 1, 0, 0), (0, 1, -1, 0), (0, -1, 1, 0)]
    check_optimum("flat restriction of indefinite Hessian", [(-2, 3)] * 3, line_rows,
                  coefficients(x * x + y * y - 2 * z * z, xyz), F(0))
    assert polytope_vertices([(-2, 3)] * 3, line_rows) == ((F(-2),) * 3, (F(3),) * 3)

    point = (F(1, 3), F(1, 5), F(-2, 7))
    point_rows = []
    for normal in [(1, 1, 0), (0, 1, 1), (1, 0, 1)]:
        rhs = sum(a * v for a, v in zip(normal, point))
        point_rows.extend([(*normal, rhs), (*(-a for a in normal), -rhs)])
    expression = x * y - 3 * z * z + 2 * x - y + sp.Rational(2, 11)
    expected = F(str(expression.subs(dict(zip(xyz, map(sp.Rational, point))))))
    check_optimum("singleton with coupled equalities", [(-1, 1)] * 3, point_rows,
                  coefficients(expression, xyz), expected, point)

    # Map a simplex by an invertible rational affine transformation. Symbolic
    # substitution constructs data; the expected values use the original simplex.
    transform = sp.Matrix([[2, 1, 0], [1, -1, 1], [0, 1, 2]])
    shift = sp.Matrix([sp.Rational(1, 7), sp.Rational(-2, 5), sp.Rational(3, 11)])
    inverse = transform.inv()
    original = inverse * (sp.Matrix(xyz) - shift)
    original_vertices = [sp.zeros(3, 1)] + [sp.eye(3)[:, i] for i in range(3)]
    vertices = [transform * v + shift for v in original_vertices]
    bounds = [(F(str(min(v[i] for v in vertices))), F(str(max(v[i] for v in vertices))))
              for i in range(3)]
    rows = []
    for form in [*[-v for v in original], sum(original) - 1]:
        p = sp.Poly(sp.expand(form), *xyz)
        rows.append(tuple(F(str(p.coeff_monomial(v))) for v in xyz)
                    + (-F(str(p.coeff_monomial(1))),))
    # Add duplicates, scaled duplicates, and a vacuous zero row.
    rows.extend([rows[0], tuple(7 * v for v in rows[1]), (0, 0, 0, 0)])
    assert set(polytope_vertices(bounds, rows)) == {tuple(F(str(v)) for v in p) for p in vertices}
    u, v, w = original
    transformed_cases = [
        ("affine simplex interior", (u - sp.Rational(1, 7)) ** 2
         + (v - sp.Rational(2, 7)) ** 2 + (w - sp.Rational(1, 7)) ** 2
         + sp.Rational(5, 11), F(5, 11)),
        ("affine simplex face", (u - sp.Rational(1, 4)) ** 2
         + (v - sp.Rational(1, 3)) ** 2 + (w + sp.Rational(1, 5)) ** 2, F(1, 25)),
        ("affine simplex linear", u + 2 * v + 3 * w, F(0)),
        ("affine simplex concave", -u * u - 2 * v * v - 3 * w * w, F(-3)),
        ("affine simplex flat valley", (u + v - sp.Rational(1, 2)) ** 2, F(0)),
    ]
    for name, expression, expected in transformed_cases:
        check_optimum(name, bounds, rows, coefficients(expression, xyz), expected)

    rng = Random(20261003)
    for index in range(12):
        d = 3 if index < 6 else 4
        symbols = sp.symbols(f"t:{d}")
        edges = [(i, j, rng.randint(0, 5)) for i in range(d) for j in range(i + 1, d)]
        expression = -sum(weight * (symbols[i] - symbols[j]) ** 2 for i, j, weight in edges)
        expected = min(-sum(weight * (bits[i] - bits[j]) ** 2 for i, j, weight in edges)
                       for bits in product((0, 1), repeat=d))
        check_optimum(f"MaxCut Boolean comparison {index}", [(0, 1)] * d, [],
                      coefficients(expression, symbols), F(expected))

    tiny = F(1, 2 ** 200)
    terms = (0, 1, 0)
    check_optimum("exact thin interval", [(0, 1)], [(1, tiny), (-1, -tiny)], terms, tiny, (tiny,))
    for name, empty_bounds, empty_rows in [
        ("subnormal-scale inconsistent rows", [(0, 1)], [(1, tiny), (-1, -2 * tiny)]),
        ("contradictory zero row", [(0, 1)], [(0, -tiny)]),
        ("reversed bounds", [(1, 0)], []),
    ]:
        result = support_quadratic(empty_bounds, empty_rows, terms)
        assert result["status"] == "empty", name
        assert result["bound"] is None and result["minimizer"] is None, name
        assert result["candidates"] == [], name
        assert polytope_vertices(empty_bounds, empty_rows) == (), name
        assert replay_quadratic(empty_bounds, empty_rows, terms, result), name
        CHECKS.append(name)

    bounds, rows = [(0, 1)] * 2, [(1, 1, F(3, 2))]
    terms = coefficients((x - sp.Rational(1, 3)) ** 2 + (y - sp.Rational(2, 5)) ** 2, (x, y))
    witness = support_quadratic(bounds, rows, terms)
    mutations = {
        "bound": lambda v: v.update(bound="1"),
        "minimizer": lambda v: v.update(minimizer=["0", "0"]),
        "status": lambda v: v.update(status="empty"),
        "schema": lambda v: v.update(schema="untrusted"),
        "missing candidate": lambda v: v["candidates"].pop(),
        "candidate value": lambda v: v["candidates"][0].update(value="999"),
        "candidate point": lambda v: v["candidates"][0].update(point=["999", "999"]),
        "candidate active rows": lambda v: v["candidates"][0].update(active=[999]),
        "face count": lambda v: v["enumeration"].update(subsets=0),
        "embedded coefficient": lambda v: v["problem"]["coefficients"].__setitem__(0, "999"),
        "embedded bounds": lambda v: v["problem"]["bounds"][0].__setitem__(0, "999"),
        "embedded row": lambda v: v["problem"]["rows"][0].__setitem__(0, "999"),
    }
    for name, mutate in mutations.items():
        changed = deepcopy(witness)
        mutate(changed)
        assert not replay_quadratic(bounds, rows, terms, changed), name
        CHECKS.append("reject mutated " + name)
    assert not replay_quadratic([(0, 2), (0, 1)], rows, terms, witness)
    assert not replay_quadratic(bounds, [], terms, witness)
    assert not replay_quadratic(bounds, rows, (terms[0] + 1, *terms[1:]), witness)
    CHECKS.append("trusted-input binding")

    required = enumeration_size(2, 1)
    assert support_quadratic(bounds, rows, terms, max_faces=required) == witness
    try:
        support_quadratic(bounds, rows, terms, max_faces=required - 1)
    except EnumerationLimitError:
        pass
    else:
        raise AssertionError("partial enumeration must not export an optimum")
    assert not replay_quadratic(bounds, rows, terms, witness, max_faces=required - 1)
    CHECKS.append("enumeration budget boundary")

    return {
        "status": "passed",
        "diagnostic_count": len(CHECKS),
        "diagnostics": CHECKS,
        "source_sha256": sha256(Path(__file__).with_name("quadratic_polytope.py").read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
