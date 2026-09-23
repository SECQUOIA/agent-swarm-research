"""Exact affine supports for fixed-interval polynomial extended RPD fields.

Implements the sign-selected rule of Ye and Scott (2023), Definitions 13–14.
Floating-point values only choose among globally valid affine pieces. All
returned coefficients are rational. This is a restricted research prototype,
not a general interval or automatic-differentiation library.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Callable

import numpy as np


def rational(value):
    """Decimal strings are recommended for intended decimal model constants."""
    if isinstance(value, bool) or not isinstance(value, (Q, int, str)):
        raise TypeError("Exact model constants must be int, str or Fraction")
    return value if isinstance(value, Q) else Q(value)


@dataclass(frozen=True)
class Affine:
    # Parameter and signed-state slopes, then the constant.
    coefficients: tuple[Q, ...]

    @classmethod
    def constant(cls, value, dimension):
        return cls((Q(0),) * dimension + (rational(value),))

    @classmethod
    def coordinate(cls, index, dimension):
        return cls(tuple(Q(i == index) for i in range(dimension)) + (Q(0),))

    def __add__(self, other):
        if not isinstance(other, Affine):
            other = Affine.constant(other, len(self.coefficients) - 1)
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Affine dimensions differ")
        return Affine(tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    __radd__ = __add__

    def __mul__(self, value):
        value = rational(value)
        return Affine(tuple(value * a for a in self.coefficients))

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def evaluate(self, point):
        if len(point) + 1 != len(self.coefficients):
            raise ValueError("Point dimension differs from affine support")
        return sum(float(a) * float(x) for a, x in zip(self.coefficients[:-1], point)) + float(self.coefficients[-1])


@dataclass
class Compiler:
    reference: np.ndarray

    def constant(self, value):
        return Affine.constant(value, len(self.reference))

    def maximum(self, *pieces):
        # Every candidate is a global support. A rounding-induced wrong choice
        # affects strength only. A fixed deterministic tie rule is sufficient.
        return max(pieces, key=lambda piece: piece.evaluate(self.reference))


@dataclass(frozen=True)
class MC:
    lower: Q
    upper: Q
    cv: Affine
    neg_cc: Affine
    compiler: Compiler

    def cut(self):
        return MC(self.lower, self.upper,
                  self.compiler.maximum(self.cv, self.compiler.constant(self.lower)),
                  self.compiler.maximum(self.neg_cc, self.compiler.constant(-self.upper)),
                  self.compiler)

    def constant(self, value):
        value = rational(value)
        return MC(value, value, self.compiler.constant(value),
                  self.compiler.constant(-value), self.compiler)

    def __add__(self, other):
        if not isinstance(other, MC):
            other = self.constant(other)
        a, b = self.cut(), other.cut()
        return MC(a.lower + b.lower, a.upper + b.upper,
                  a.cv + b.cv, a.neg_cc + b.neg_cc, self.compiler)

    __radd__ = __add__

    def __neg__(self):
        a = self.cut()
        return MC(-a.upper, -a.lower, a.neg_cc, a.cv, self.compiler)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, MC):
            other = self.constant(other)
        a, b = self.cut(), other.cut()

        def low(coefficient, node):
            return coefficient * node.cv if coefficient >= 0 else -coefficient * node.neg_cc

        def high(coefficient, node):
            return coefficient * node.neg_cc if coefficient >= 0 else -coefficient * node.cv

        bounds = (a.lower*b.lower, a.lower*b.upper,
                  a.upper*b.lower, a.upper*b.upper)
        cv = self.compiler.maximum(
            low(a.lower, b) + low(b.lower, a) - a.lower*b.lower,
            low(a.upper, b) + low(b.upper, a) - a.upper*b.upper)
        neg_cc = self.compiler.maximum(
            high(a.upper, b) + high(b.lower, a) + a.upper*b.lower,
            high(a.lower, b) + high(b.upper, a) + a.lower*b.upper)
        return MC(min(bounds), max(bounds), cv, neg_cc, self.compiler)

    __rmul__ = __mul__


@dataclass(frozen=True)
class PolynomialModel:
    parameter_box: tuple[tuple[Q, Q], ...]
    state_box: tuple[tuple[Q, Q], ...]
    rhs: Callable
    # Initial states affine in p; coefficients followed by constant.
    initial: tuple[tuple[Q, ...], ...]
    # Conservation rows: A x = b + D p.
    invariant_A: tuple[tuple[Q, ...], ...] = ()
    invariant_b: tuple[Q, ...] = ()
    invariant_D: tuple[tuple[Q, ...], ...] = ()

    def __post_init__(self):
        for name in ("parameter_box", "state_box", "initial", "invariant_A", "invariant_D"):
            object.__setattr__(self, name, tuple(tuple(rational(x) for x in row)
                                               for row in getattr(self, name)))
        object.__setattr__(self, "invariant_b", tuple(map(rational, self.invariant_b)))
        m, n, r = len(self.parameter_box), len(self.state_box), len(self.invariant_A)
        if not n or any(len(pair) != 2 or pair[0] > pair[1]
                        for pair in self.parameter_box + self.state_box):
            raise ValueError("Nonempty state dimension and ordered finite boxes required")
        if len(self.initial) != n or any(len(row) != m+1 for row in self.initial):
            raise ValueError("Initial affine coefficient dimensions differ from model")
        if (len(self.invariant_b) != r or len(self.invariant_D) != r
                or any(len(row) != n for row in self.invariant_A)
                or any(len(row) != m for row in self.invariant_D)):
            raise ValueError("Invariant dimensions differ from model")
        if not callable(self.rhs):
            raise TypeError("rhs must be callable")

    def initial_state(self, p):
        return np.array([sum(float(a)*float(t) for a, t in zip(row[:-1], p)) + float(row[-1])
                         for row in self.initial])

    def initial_signed_coefficients(self):
        return [list(row) for row in self.initial] + [[-a for a in row] for row in self.initial]

    def physical_rhs(self, p, x):
        return np.asarray(self.rhs(p, x), dtype=float)

    def supports(self, p, v, *, row_sweeps=0, self_exclude=True, bundles=None):
        """Return exact global affine minorants d+A*p+B*v, B Metzler.

        The interval parts stay fixed for this call and all parameter/state
        reference values. Invariant propagation uses a fixed number of sweeps.
        """
        m, n = len(self.parameter_box), len(self.state_box)
        point = np.asarray([*p, *v], dtype=float)
        if point.shape != (m + 2*n,) or not np.all(np.isfinite(point)):
            raise ValueError("Finite reference with expected dimension required")
        if isinstance(row_sweeps, bool) or not isinstance(row_sweeps, int) or row_sweeps < 0:
            raise ValueError("row_sweeps must be a nonnegative integer")
        compiler = Compiler(point)
        coordinates = [Affine.coordinate(j, len(point)) for j in range(len(point))]
        parameters = [MC(lo, hi, coordinates[j], -coordinates[j], compiler)
                      for j, (lo, hi) in enumerate(self.parameter_box)]
        rows = []
        for output in range(2*n):
            own = output % n
            lower, upper = list(coordinates[m:m+n]), list(coordinates[m+n:])
            if output < n:
                upper[own] = -lower[own]
            else:
                lower[own] = -upper[own]
            if row_sweeps:
                for j, (lo, hi) in enumerate(self.state_box):
                    if self_exclude and j == own:
                        continue
                    lower[j] = compiler.maximum(lower[j], compiler.constant(lo))
                    upper[j] = compiler.maximum(upper[j], compiler.constant(-hi))
                for _ in range(row_sweeps):
                    for a, b, d in zip(self.invariant_A, self.invariant_b, self.invariant_D):
                        for j, divisor in enumerate(a):
                            if divisor == 0 or (self_exclude and j == own):
                                continue
                            lo = compiler.constant(b/divisor)
                            hi = -lo
                            for coefficient, param in zip(d, coordinates[:m]):
                                lo = lo + (coefficient/divisor)*param
                                hi = hi - (coefficient/divisor)*param
                            for k, coefficient in enumerate(a):
                                if k == j:
                                    continue
                                coefficient = -coefficient/divisor
                                lo = lo + (coefficient*lower[k] if coefficient >= 0 else -coefficient*upper[k])
                                hi = hi + (coefficient*upper[k] if coefficient >= 0 else -coefficient*lower[k])
                            lower[j] = compiler.maximum(lower[j], lo)
                            upper[j] = compiler.maximum(upper[j], hi)
            if bundles is not None:
                # Evaluate every fixed bundle against the same refined input;
                # do not turn an incidental loop order into extra sweeps.
                previous_lower, previous_upper = list(lower), list(upper)
                for j in range(n):
                    if self_exclude and j == own:
                        continue
                    for sign, outputs in ((1, lower), (-1, upper)):
                        candidates = [outputs[j]]
                        for multipliers in bundles.get((j, sign), ()):
                            candidates.append(penalty_support(
                                self, j, sign, *multipliers, coordinates[:m],
                                previous_lower, previous_upper, compiler))
                        outputs[j] = compiler.maximum(*candidates)
            states = [MC(lo, hi, lower[j], upper[j], compiler)
                      for j, (lo, hi) in enumerate(self.state_box)]
            outputs = self.rhs(parameters, states)
            if len(outputs) != n:
                raise ValueError("RHS output dimension differs from state dimension")
            value = outputs[own]
            if not isinstance(value, MC):
                value = states[0].constant(value)
            selected = value.cv if output < n else value.neg_cc
            row = selected.coefficients
            if any(value < 0 for j, value in enumerate(row[m:-1]) if j != output):
                raise ArithmeticError("Compiled support is not cooperative")
            rows.append(row)
        return rows

    def relaxation_rhs(self, p, v, **options):
        point = [*p, *v]
        return np.array([Affine(row).evaluate(point) for row in self.supports(p, v, **options)])


def penalty_support(model, coordinate, sign, alpha, beta, q, parameters,
                    lower, neg_upper, compiler):
    """Exact affine support from any bounded feasible penalty dual tuple.

    Positive-part coefficients must be nonnegative. The finite bundle itself
    defines a valid refinement for any finite such coefficients and q; the
    common rho box is needed only to compare with a specified penalty LP.
    """
    n = len(model.state_box)
    alpha, beta, q = tuple(map(rational, alpha)), tuple(map(rational, beta)), tuple(map(rational, q))
    if sign not in (-1, 1) or not 0 <= coordinate < n:
        raise ValueError("Invalid signed coordinate")
    if len(alpha) != n or len(beta) != n or len(q) != len(model.invariant_A):
        raise ValueError("Multiplier dimensions differ from the model")
    if any(value < 0 for value in (*alpha, *beta)):
        raise ValueError("Endpoint penalty multipliers must be nonnegative")
    constant = -sum(qi*bi for qi, bi in zip(q, model.invariant_b))
    for j, (lo, hi) in enumerate(model.state_box):
        d = sign*Q(j == coordinate) - alpha[j] + beta[j]
        d += sum(qi*a[j] for qi, a in zip(q, model.invariant_A))
        constant += min(lo*d, hi*d)
    result = compiler.constant(constant)
    for a, b, c, u in zip(alpha, beta, lower, neg_upper):
        result = result + a*c + b*u
    for j, param in enumerate(parameters):
        result = result - sum(qi*d[j] for qi, d in zip(q, model.invariant_D))*param
    return result


def penalty_dual(model, coordinate, sign, p, v, rho=Q(2), denominator=1000000):
    """Get a feasible rational dual tuple; floating LP optimality is optional.

    Rounding and box clamping restore exact feasibility. The support intercept
    is later recomputed exactly; solver objective values are never certificates.
    """
    from scipy.optimize import linprog
    n, r = len(model.state_box), len(model.invariant_A)
    rho = rational(rho)
    if rho < 0 or sign not in (-1, 1) or not 0 <= coordinate < n:
        raise ValueError("Invalid penalty specification")
    width = 3*n+r
    objective = np.zeros(width)
    objective[:2*n] = -np.asarray(v)
    if r:
        objective[2*n:2*n+r] = [float(b)+sum(float(a)*float(t) for a,t in zip(d,p))
                                for b,d in zip(model.invariant_b,model.invariant_D)]
    objective[-n:] = -1
    rows, right = [], []
    for j, endpoints in enumerate(model.state_box):
        for bound in endpoints:
            row = np.zeros(width)
            row[j], row[n+j], row[2*n+r+j] = float(bound), -float(bound), 1
            row[2*n:2*n+r] = [-float(bound*a[j]) for a in model.invariant_A]
            rows.append(row)
            right.append(float(bound*sign*Q(j == coordinate)))
    solution = linprog(objective, A_ub=rows, b_ub=right,
                       bounds=[(0,float(rho))]*(2*n)+[(-float(rho),float(rho))]*r+[(None,None)]*n,
                       method="highs")
    if not solution.success:
        raise RuntimeError(f"Penalty dual LP: {solution.message}")
    def rounded(value, lo, hi):
        return min(hi, max(lo, Q(float(value)).limit_denominator(denominator)))
    alpha = tuple(rounded(a,Q(0),rho) for a in solution.x[:n])
    beta = tuple(rounded(a,Q(0),rho) for a in solution.x[n:2*n])
    q = tuple(rounded(a,-rho,rho) for a in solution.x[2*n:2*n+r])
    return alpha, beta, q


def dimerization():
    """Stylized closed 2A <-> B system; A+2B=1 proves the fixed tube."""
    def rhs(p, x):
        rate = p[0]*x[0]*x[0] - Q(1, 5)*x[1]
        return [-2*rate, rate]
    return PolynomialModel(
        ((Q(3, 10), Q(3, 2)),), ((Q(0), Q(1)), (Q(0), Q(1, 2))), rhs,
        ((Q(0), Q(1)), (Q(0), Q(0))),
        ((Q(1), Q(2)),), (Q(1),), ((Q(0),),))


def shift_methanation():
    """Stylized isothermal mass action, not fitted process kinetic data.

    CO+H2O <-> CO2+H2; CO+3H2 <-> CH4+H2O. Parameterized CO/H2O
    feeds in [1/2,3/2], initial H2=2. Nonnegativity and C/O/H conservation
    establish the box. Species order CO, H2O, CO2, H2, CH4.
    """
    def rhs(p, x):
        co, water, co2, h2, ch4 = x
        shift = Q(2, 5)*co*water - Q(1, 10)*co2*h2
        meth = Q(1, 50)*co*h2*h2*h2 - Q(1, 100)*ch4*water
        return [-shift-meth, -shift+meth, shift, shift-3*meth, meth]
    return PolynomialModel(
        ((Q(1, 2), Q(3, 2)),)*2,
        tuple((Q(0), u) for u in (Q(3, 2), Q(3), Q(3, 2), Q(7, 2), Q(3, 2))), rhs,
        tuple(tuple(map(Q, row)) for row in ((1,0,0),(0,1,0),(0,0,0),(0,0,2),(0,0,0))),
        tuple(tuple(map(Q, row)) for row in ((1,0,1,0,1),(1,1,2,0,0),(0,2,0,2,4))),
        (Q(0), Q(0), Q(4)), ((Q(1),Q(0)), (Q(1),Q(1)), (Q(0),Q(2))))
