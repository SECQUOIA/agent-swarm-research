"""Exact convex box-QP response certificates for one retained parameter.

The constructor enumerates 3**m active patterns and requires a positive
definite private Hessian. The verifier allows positive semidefinite Hessians.
This is a small exact component, not a complete sparse global optimizer.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import re


def rational(x):
    if not isinstance(x, (int, Q)) or isinstance(x, bool):
        raise ValueError("coefficients must be exact integers or Fractions")
    return Q(x)


def solve_linear(matrix, rhs):
    n = len(rhs)
    rows = [[Q(x) for x in row] + [Q(rhs[i])]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            raise ValueError("singular linear system")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows)


def is_psd(matrix, strict=False):
    """Exact Schur-complement test; zero PSD pivots require zero rows."""
    a = [list(map(Q, row)) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        return False
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    for k in range(n):
        if a[k][k] < 0:
            return False
        if a[k][k] == 0:
            if strict or any(a[k][j] for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / a[k][k]
                a[j][i] = a[i][j]
    return True


@dataclass(frozen=True)
class Block:
    C: tuple
    cross: tuple
    linear: tuple
    lower: tuple
    upper: tuple
    parameter_lower: Q
    parameter_upper: Q
    retained_hessian: Q = Q(0)
    retained_linear: Q = Q(0)
    constant: Q = Q(0)

    def __post_init__(self):
        for name in ("C",):
            object.__setattr__(self, name,
                               tuple(tuple(rational(x) for x in r)
                                     for r in getattr(self, name)))
        for name in ("cross", "linear", "lower", "upper"):
            object.__setattr__(self, name,
                               tuple(rational(x) for x in getattr(self, name)))
        for name in ("parameter_lower", "parameter_upper", "retained_hessian",
                     "retained_linear", "constant"):
            object.__setattr__(self, name, rational(getattr(self, name)))
        n = len(self.lower)
        if any(len(getattr(self, name)) != n
               for name in ("C", "cross", "linear", "upper")):
            raise ValueError("inconsistent block dimensions")
        if any(len(row) != n for row in self.C):
            raise ValueError("inconsistent Hessian dimensions")
        if any(a >= b for a, b in zip(self.lower, self.upper)):
            raise ValueError("substitute fixed private coordinates first")
        if self.parameter_lower >= self.parameter_upper:
            raise ValueError("parameter interval must have positive width")

    def objective(self, y, z):
        y = tuple(rational(x) for x in y)
        z = rational(z)
        if len(y) != len(self.lower):
            raise ValueError("incorrect private point dimension")
        return (sum((self.C[i][j] * y[i] * y[j]
                     for i in range(len(y)) for j in range(len(y))), Q(0)) / 2
                + sum((d * z + c) * yi
                      for d, c, yi in zip(self.cross, self.linear, y))
                + self.retained_hessian * z * z / 2
                + self.retained_linear * z + self.constant)


@dataclass(frozen=True)
class Piece:
    lower: Q
    upper: Q
    intercept: tuple
    slope: tuple
    lower_multiplier_intercept: tuple
    lower_multiplier_slope: tuple
    upper_multiplier_intercept: tuple
    upper_multiplier_slope: tuple
    # Value is c0 + c1*z + c2*z*z; c2 is half the Hessian.
    value: tuple

    def response(self, z):
        return tuple(a + b * z for a, b in zip(self.intercept, self.slope))

    def evaluate(self, z):
        return self.value[0] + z * (self.value[1] + z * self.value[2])


def _value_coefficients(block, a, b):
    n = len(a)
    c0 = block.constant + sum(c * x for c, x in zip(block.linear, a))
    c1 = block.retained_linear + sum(c * x + d * y for c, x, d, y
                                   in zip(block.linear, b, block.cross, a))
    c2 = block.retained_hessian / 2 + sum(d * x for d, x in zip(block.cross, b))
    for i in range(n):
        for j in range(n):
            c0 += block.C[i][j] * a[i] * a[j] / 2
            c1 += block.C[i][j] * (a[i] * b[j] + b[i] * a[j]) / 2
            c2 += block.C[i][j] * b[i] * b[j] / 2
    return c0, c1, c2


def _restrict(interval, intercept, slope):
    lo, hi = interval
    if slope > 0:
        lo = max(lo, -intercept / slope)
    elif slope < 0:
        hi = min(hi, -intercept / slope)
    elif intercept < 0:
        return None
    return (lo, hi) if lo < hi else None


def construct(block, max_patterns=100000, budget_check=None):
    """Complete exact scalar partition; raises if budget or PD promise fails."""
    if budget_check is not None:
        budget_check()
    n = len(block.lower)
    if not is_psd(block.C, strict=True):
        raise ValueError("automatic construction requires positive definiteness")
    if 3 ** n > max_patterns:
        raise ValueError("active-pattern budget exceeded")
    candidates = []
    for status in product((-1, 0, 1), repeat=n):
        if budget_check is not None:
            budget_check()
        free = [i for i in range(n) if status[i] == 0]
        fixed = [i for i in range(n) if status[i] != 0]
        a, b = [Q(0)] * n, [Q(0)] * n
        for i in fixed:
            a[i] = block.lower[i] if status[i] == -1 else block.upper[i]
        mat = [[block.C[i][j] for j in free] for i in free]
        afree = solve_linear(mat, [-block.linear[i]
                            - sum(block.C[i][j] * a[j] for j in fixed)
                            for i in free])
        bfree = solve_linear(mat, [-block.cross[i] for i in free])
        for i, ai, bi in zip(free, afree, bfree):
            a[i], b[i] = ai, bi
        ga = [block.linear[i] + sum(block.C[i][j] * a[j] for j in range(n))
              for i in range(n)]
        gb = [block.cross[i] + sum(block.C[i][j] * b[j] for j in range(n))
              for i in range(n)]
        lower_a = tuple(ga[i] if status[i] == -1 else Q(0) for i in range(n))
        lower_b = tuple(gb[i] if status[i] == -1 else Q(0) for i in range(n))
        upper_a = tuple(-ga[i] if status[i] == 1 else Q(0) for i in range(n))
        upper_b = tuple(-gb[i] if status[i] == 1 else Q(0) for i in range(n))
        interval = (block.parameter_lower, block.parameter_upper)
        constraints = []
        for i in range(n):
            constraints.extend(((a[i] - block.lower[i], b[i]),
                                (block.upper[i] - a[i], -b[i]),
                                (lower_a[i], lower_b[i]),
                                (upper_a[i], upper_b[i])))
        for c, d in constraints:
            interval = _restrict(interval, c, d)
            if interval is None:
                break
        if interval:
            candidates.append(Piece(*interval, tuple(a), tuple(b), lower_a,
                                    lower_b, upper_a, upper_b,
                                    _value_coefficients(block, a, b)))
    cuts = sorted({block.parameter_lower, block.parameter_upper,
                   *(p.lower for p in candidates), *(p.upper for p in candidates)})
    partition = []
    for lo, hi in zip(cuts, cuts[1:]):
        if budget_check is not None:
            budget_check()
        chosen = next((p for p in candidates if p.lower <= lo and p.upper >= hi), None)
        if chosen is None:
            raise AssertionError("active patterns failed to cover parameter interval")
        partition.append(Piece(lo, hi, chosen.intercept, chosen.slope,
                               chosen.lower_multiplier_intercept,
                               chosen.lower_multiplier_slope,
                               chosen.upper_multiplier_intercept,
                               chosen.upper_multiplier_slope, chosen.value))
    verify(block, partition, budget_check=budget_check)
    return tuple(partition)


def verify(block, pieces, budget_check=None):
    """Check exact coverage/KKT/value coefficients without solving any QP."""
    if budget_check is not None:
        budget_check()
    if not is_psd(block.C):
        raise ValueError("private Hessian is not positive semidefinite")
    if not pieces:
        raise ValueError("empty partition")
    n = len(block.lower)
    expected_lower = block.parameter_lower
    for piece in pieces:
        if budget_check is not None:
            budget_check()
        for field in ("intercept", "slope", "lower_multiplier_intercept",
                      "lower_multiplier_slope", "upper_multiplier_intercept",
                      "upper_multiplier_slope"):
            if len(getattr(piece, field)) != n:
                raise ValueError("incorrect certificate dimension")
        data = (piece.lower, piece.upper, *piece.intercept, *piece.slope,
                *piece.lower_multiplier_intercept, *piece.lower_multiplier_slope,
                *piece.upper_multiplier_intercept, *piece.upper_multiplier_slope,
                *piece.value)
        for x in data:
            rational(x)
        if len(piece.value) != 3:
            raise ValueError("value must have three coefficients")
        if piece.lower != expected_lower or piece.lower >= piece.upper:
            raise ValueError("partition contains a gap, overlap, or empty interval")
        expected_lower = piece.upper
        if piece.upper > block.parameter_upper:
            raise ValueError("partition exceeds parameter domain")
        for i in range(n):
            if budget_check is not None:
                budget_check()
            ai, bi = piece.intercept[i], piece.slope[i]
            la, lb = piece.lower_multiplier_intercept[i], piece.lower_multiplier_slope[i]
            ua, ub = piece.upper_multiplier_intercept[i], piece.upper_multiplier_slope[i]
            gradient_a = block.linear[i] + sum(block.C[i][j] * piece.intercept[j]
                                              for j in range(n))
            gradient_b = block.cross[i] + sum(block.C[i][j] * piece.slope[j]
                                             for j in range(n))
            if gradient_a != la - ua or gradient_b != lb - ub:
                raise ValueError("stationarity identity fails")
            for c, d, e, f in ((la, lb, ai - block.lower[i], bi),
                               (ua, ub, block.upper[i] - ai, -bi)):
                if (c * e, c * f + d * e, d * f) != (0, 0, 0):
                    raise ValueError("complementarity identity fails")
            for z in (piece.lower, piece.upper):
                if not block.lower[i] <= ai + bi * z <= block.upper[i]:
                    raise ValueError("response violates private box")
                if min(la + lb * z, ua + ub * z) < 0:
                    raise ValueError("negative multiplier")
        if tuple(piece.value) != _value_coefficients(block, piece.intercept, piece.slope):
            raise ValueError("incorrect value polynomial")
    if expected_lower != block.parameter_upper:
        raise ValueError("partition does not cover upper domain")
    for first, second in zip(pieces, pieces[1:]):
        if first.evaluate(first.upper) != second.evaluate(second.lower):
            raise ValueError("inconsistent interface values")
    return max(2 * piece.value[2] for piece in pieces)


_SCALAR_FIELDS = ("lower", "upper")
_VECTOR_FIELDS = ("intercept", "slope", "lower_multiplier_intercept",
                  "lower_multiplier_slope", "upper_multiplier_intercept",
                  "upper_multiplier_slope", "value")
_PIECE_FIELDS = frozenset(_SCALAR_FIELDS + _VECTOR_FIELDS)


def pack_pieces(pieces):
    """Encode piece maps as JSON-safe dictionaries of rational strings.

    Serialization is not certificate verification; call verify against the
    original Block before trusting the encoded maps.
    """
    records = []
    for piece in pieces:
        record = {name: str(rational(getattr(piece, name)))
                  for name in _SCALAR_FIELDS}
        record.update({name: [str(rational(x)) for x in getattr(piece, name)]
                       for name in _VECTOR_FIELDS})
        records.append(record)
    return records


def _parse_rational(value):
    if isinstance(value, str):
        if re.fullmatch(r"[+-]?\d+(?:/[1-9]\d*)?", value) is None:
            raise ValueError("expected an integer or rational-fraction string")
        return Q(value)
    return rational(value)


def unpack_pieces(records):
    """Decode exact piece records, rejecting floats, booleans, and schema drift.

    This checks the serialization schema, not KKT validity or coverage.
    Pass the result to verify with a Block reconstructed from original data.
    """
    if not isinstance(records, (list, tuple)):
        raise ValueError("piece records must be a list or tuple")
    pieces = []
    for record in records:
        if not isinstance(record, dict) or set(record) != _PIECE_FIELDS:
            raise ValueError("piece record has missing or unexpected fields")
        parsed = {name: _parse_rational(record[name]) for name in _SCALAR_FIELDS}
        for name in _VECTOR_FIELDS:
            values = record[name]
            if not isinstance(values, (list, tuple)):
                raise ValueError("piece vector field must be a list or tuple")
            parsed[name] = tuple(_parse_rational(x) for x in values)
        if len(parsed["value"]) != 3:
            raise ValueError("value must have three coefficients")
        pieces.append(Piece(**parsed))
    return tuple(pieces)


def evaluate(pieces, z):
    z = rational(z)
    for piece in pieces:
        if piece.lower <= z <= piece.upper:
            return piece.evaluate(z), piece.response(z)
    raise ValueError("parameter outside certified partition")
