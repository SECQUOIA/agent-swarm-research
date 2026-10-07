"""Replay polynomial boundary certificates without running face discovery."""

from fractions import Fraction as F

from certified_grid import rational


class BoundaryCertificateError(ValueError):
    pass


def _require(value, message):
    if not value:
        raise BoundaryCertificateError(message)


def _strict_psd(matrix, check):
    work = [list(row) for row in matrix]
    for k in range(len(work)):
        check()
        pivot = work[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, len(work)):
            for j in range(i, len(work)):
                work[i][j] -= work[i][k] * work[k][j] / pivot
                work[j][i] = work[i][j]
    return True


def verify_certificate(certificate, problem=None, *, max_table_states=1000000, check=None):
    """Certify a rational point or an exact implicit unique convex-face minimizer.

    A patch artifact gives its polynomial objective and rational face bounds;
    it does not claim an explicit rational optimizer or exact rational value.
    Weak reductions preserve minimum value and at least one original optimum.
    """
    from polynomial_grid import PolynomialBox
    from verify_polynomial import polynomial_interval, verify_polynomial as verify_grid
    check = check or (lambda: None)
    try:
        _require(certificate["schema"] == "polynomial-boundary-v1", "unknown schema")
        model = PolynomialBox.from_dict(certificate["problem"])
        if problem is not None:
            _require(model.to_dict() == problem.to_dict(), "certificate binds a different problem")
        grid = certificate["grid_certificate"]
        checked = verify_grid(grid, max_table_states=max_table_states,
                              expected_problem=model, check=check)
        if certificate["kind"] == "grid_point":
            point = tuple(map(rational, certificate["point"]))
            value = rational(certificate["value"])
            _require(model.feasible(point) and model.value(point) == value,
                     "invalid exact grid point")
            _require(rational(checked["lower"]) == value == rational(checked["upper"]),
                     "grid point lacks an exact global lower certificate")
            return {"valid": True, "kind": "grid_point", "point": point, "value": value}
        bounds = [tuple(map(rational, pair)) for pair in checked["retained_bounds"]]
        _require(all(bounds[i][0] == bounds[i][1] for i in model.integers), "integer labels not fixed")
        for reduction in certificate["reductions"]:
            check()
            i = reduction["coordinate"]
            _require(type(i) is int and 0 <= i < len(bounds) and i not in model.integers,
                     "invalid reduction coordinate")
            lo, hi = bounds[i]
            _require(lo < hi, "duplicate/fixed-coordinate reduction")
            endpoint = rational(reduction["endpoint"])
            lower, upper = polynomial_interval(model, bounds, (i,))
            _require(rational(reduction["derivative_lower"]) == lower and
                     rational(reduction["derivative_upper"]) == upper, "incorrect derivative interval")
            _require((endpoint == lo == model.bounds[i][0] and lower >= 0) or
                     (endpoint == hi == model.bounds[i][1] and upper <= 0),
                     "unsupported monotone endpoint reduction")
            bounds[i] = (endpoint, endpoint)
        recorded = tuple(tuple(map(rational, pair)) for pair in certificate["face_bounds"])
        _require(recorded == tuple(bounds), "incorrect reduced face")
        free = tuple(i for i, (lo, hi) in enumerate(bounds) if lo != hi)
        _require(certificate["free"] == list(free), "incorrect free coordinates")
        if certificate["kind"] == "point":
            _require(not free, "point descriptor has free coordinates")
            point = tuple(map(rational, certificate["point"]))
            _require(point == tuple(lo for lo, _ in bounds), "incorrect point descriptor")
            value = rational(certificate["value"])
            _require(model.value(point) == value, "incorrect exact value")
            return {"valid": True, "kind": "point", "point": point, "value": value,
                    "face_bounds": tuple(bounds)}
        _require(certificate["kind"] == "strongly_convex_patch" and free,
                 "invalid patch kind or dimension")
        midpoint = tuple((lo + hi) / 2 for lo, hi in bounds)
        _require(tuple(map(rational, certificate["midpoint"])) == midpoint, "incorrect midpoint")
        center_box = tuple((x, x) for x in midpoint)
        matrix = [[polynomial_interval(model, center_box, (i, j))[0]
                   for j in free] for i in free]
        _require([list(map(rational, row)) for row in certificate["hessian"]] == matrix,
                 "incorrect midpoint Hessian")
        delta = F(0)
        for row, i in enumerate(free):
            check()
            row_error = F(0)
            for column, j in enumerate(free):
                lower, upper = polynomial_interval(model, bounds, (i, j))
                row_error += max(abs(lower - matrix[row][column]), abs(upper - matrix[row][column]))
            delta = max(delta, row_error)
        _require(rational(certificate["hessian_error"]) == delta, "incorrect uniform Hessian error")
        shifted = [[value - (delta if i == j else 0) for j, value in enumerate(row)]
                   for i, row in enumerate(matrix)]
        _require(_strict_psd(shifted, check), "restricted Hessian is not uniformly positive definite")
        return {"valid": True, "kind": "strongly_convex_patch", "face_bounds": tuple(bounds),
                "free": free, "guarantee": "unique restricted minimizer is an original global optimizer"}
    except BoundaryCertificateError:
        raise
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as exc:
        raise BoundaryCertificateError("malformed or invalid polynomial boundary certificate") from exc
