"""Exact interpretations at the source-tree / PySCIPOpt model boundary.

PySCIPOpt performs binary64 arithmetic while assembling expressions. A source
tree containing two binary64 coefficients can therefore denote a different
real function from the assembled expression. Certificates must be bound to an
expression whose stored coefficients have actually been checked.

These helpers interpret coefficients exactly; they do not certify SCIP's
later presolve transformations or its floating point feasibility decisions.
Original native expressions must still enforce their domain restrictions:
SymPy's algebraic simplifications are not a replacement for those constraints.
"""
from __future__ import annotations

import math
from fractions import Fraction
from numbers import Real

import sympy as sp


_UNARY = {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt,
          "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}
_ARITHMETIC = {"sum", "times", "negate", "divide", "power", "square"}
_NOT_CONSTANT = object()


def _binary64(value):
    """The exact real value of a finite stored binary64 number."""
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("nonfinite expression constant")
    return sp.Rational(value)


def _apply(op, args):
    if op == "sum":
        return sp.Add(*args)
    if op == "times":
        return sp.Mul(*args)
    if op == "negate":
        return -args[0]
    if op == "divide":
        if args[1] == 0:
            raise ValueError("zero expression denominator")
        return args[0] / args[1]
    if op == "power":
        return args[0] ** args[1]
    if op == "square":
        return args[0] ** 2
    if op in _UNARY:
        return _UNARY[op](args[0])
    raise ValueError(f"unsupported source operator: {op}")


def source_expression(tree, symbols):
    """Real interpretation of the binary64 leaves in an OSiL source tree."""
    op = tree[0]
    if op == "num":
        return _binary64(tree[1])
    if op == "var":
        return symbols[tree[1]]
    return _apply(op, [source_expression(c, symbols) for c in tree[1:]])


def _constant_arithmetic(tree):
    """Evaluate constant arithmetic exactly, before any representability test.

    Intermediate values need not be representable: (1e16 + 1) - 1e16 is
    exactly one. Elementary functions retain their original native nodes.
    """
    op = tree[0]
    if op == "num":
        return _binary64(tree[1])
    if op not in _ARITHMETIC:
        return _NOT_CONSTANT
    args = [_constant_arithmetic(c) for c in tree[1:]]
    if any(value is _NOT_CONSTANT for value in args):
        return _NOT_CONSTANT
    value = _apply(op, args)
    if value.is_real is not True or value.is_finite is not True:
        raise ValueError("undefined or nonreal constant arithmetic")
    return value


def normalize_constant_trees(tree):
    """Fold constant arithmetic only when its exact value is a finite float.

    Nonrepresentable and undefined constant subtrees remain unchanged. They
    must not silently become rounded exact coefficients in a certificate.
    Admission requires separately comparing ``source_expression`` with
    ``native_expression``. Variable-bearing operations are never simplified,
    so this normalization does not remove their source domain restrictions.
    """
    if tree is None or tree[0] in ("num", "var", "uni"):
        return tree
    try:
        value = _constant_arithmetic(tree)
    except (ValueError, ZeroDivisionError, OverflowError):
        # Keep the entire invalid subtree: simplifying its children must not
        # accidentally erase a domain error in the original constant tree.
        return tree
    if value is not _NOT_CONSTANT:
        if value.is_Rational:
            try:
                candidate = float(value)
                if math.isfinite(candidate) and sp.Rational(candidate) == value:
                    return ("num", candidate)
            except (ValueError, OverflowError):
                pass
        return tree
    return (tree[0], *(normalize_constant_trees(c) for c in tree[1:]))


def native_expression(expr, var_symbols):
    """Interpret a constructed PySCIPOpt expression using exact coefficients.

    ``var_symbols`` maps native variable names to SymPy symbols. Both the
    polynomial ``Expr.terms`` representation and generic expression nodes are
    supported. Unknown variables, operators, malformed nodes, and nonfinite
    stored numbers fail closed with ``ValueError``.
    """
    if isinstance(expr, Real):
        return _binary64(expr)
    terms = getattr(expr, "terms", None)
    if terms is not None:
        summands = []
        for variables, coefficient in terms.items():
            try:
                factors = [var_symbols[v.name] for v in variables]
            except (KeyError, AttributeError) as error:
                raise ValueError("unbound native variable") from error
            summands.append(_binary64(coefficient) * sp.Mul(*factors))
        return sp.Add(*summands)
    try:
        op = expr.getOp()
    except AttributeError as error:
        raise ValueError("unsupported native expression object") from error
    if op == "const":
        return _binary64(expr.number)
    children = getattr(expr, "children", None)
    if children is None:
        raise ValueError("native expression has no children")
    args = [native_expression(c, var_symbols) for c in children]
    if op == "var":
        if len(args) != 1:
            raise ValueError("malformed native variable")
        return args[0]
    if op == "sum":
        if len(expr.coefs) != len(args):
            raise ValueError("malformed native sum")
        return _binary64(expr.constant) + sp.Add(*(
            _binary64(c) * a for c, a in zip(expr.coefs, args)))
    if op == "prod":
        return _binary64(expr.constant) * sp.Mul(*args)
    if op == "**":
        if len(args) != 1:
            raise ValueError("malformed native power")
        return args[0] ** _binary64(expr.expo)
    if op in _UNARY and len(args) == 1:
        return _UNARY[op](args[0])
    raise ValueError(f"unsupported native operator: {op}")


def same_expression(source, native):
    """A conservative exact algebraic check, with no numerical tolerance.

    Equality concerns values on the native source domain. It does not assert
    equality of domains. Avoid heuristic transcendental equality routines;
    false negatives merely decline a candidate auxiliary/certificate.
    """
    difference = sp.expand(source - native)
    return difference == 0


def assert_source_domains(tree, bounds):
    """Prove every original source domain restriction on the declared box.

    This intentionally ignores constraints that could shrink that box. Natural
    rational interval arithmetic can be inconclusive; an inconclusive domain
    check refuses import with ``ValueError``. Traversal precedes algebraic
    simplification and visits children of zero products and zero powers too.
    Unrestricted nodes need no finite enclosure unless a parent needs one.
    """
    q = Fraction
    artificial = sp.Symbol("_source_domain_argument", real=True)

    def require(interval, condition, op, description):
        if interval is None or not condition(*interval):
            raise ValueError(f"source {op} domain is not established on the "
                             f"declared box: {description}")

    def multiply(a, b):
        values = [u*v for u in a for v in b]
        return min(values), max(values)

    def integer_power(a, exponent):
        if abs(exponent) > 1024:
            return None  # Bound work; no domain conclusion depends on this.
        lo, hi = a
        if exponent == 0:
            return q(1), q(1)
        if exponent < 0:
            positive = integer_power(a, -exponent)
            return q(1)/positive[1], q(1)/positive[0]
        if exponent % 2:
            return lo**exponent, hi**exponent
        return (q(0) if lo <= 0 <= hi else min(lo**exponent, hi**exponent),
                max(lo**exponent, hi**exponent))

    def elementary(op, interval, exponent=None):
        if interval is None:
            return None
        from .certified import elementary_interval
        expression = (artificial ** sp.Rational(exponent.numerator,
                                                exponent.denominator)
                      if op == "power" else _UNARY[op](artificial))
        try:
            return elementary_interval(expression, artificial, interval)
        except (ValueError, ArithmeticError, ImportError):
            return None

    def visit(node, need_interval):
        op = node[0]
        if op == "num":
            try:
                value = q(_binary64(node[1]))
            except (ValueError, OverflowError) as error:
                raise ValueError("nonfinite source constant") from error
            return (value, value) if need_interval else None
        if op == "var":
            if not need_interval:
                return None
            try:
                lo, hi = (q(v) for v in bounds[node[1]])
            except (ValueError, OverflowError):
                return None
            if lo > hi:
                raise ValueError("reversed source variable bounds")
            return lo, hi

        if op == "power":
            # Even exponent zero must not hide invalid operations in its base.
            base = visit(node[1], True)
            exponent_interval = visit(node[2], True)
            exponent = (exponent_interval[0] if exponent_interval is not None
                        and exponent_interval[0] == exponent_interval[1]
                        else None)
            if exponent is None:
                require(base, lambda lo, hi: lo > 0, op,
                        "variable exponent requires a strictly positive base")
                return None
            if exponent.denominator != 1:
                require(base, lambda lo, hi: lo > 0 if exponent < 0 else lo >= 0,
                        op, "fractional exponent requires a nonnegative base "
                        "(strictly positive for negative exponents)")
            elif exponent < 0:
                require(base, lambda lo, hi: hi < 0 or lo > 0, op,
                        "negative exponent requires a nonzero base")
            if not need_interval or base is None:
                return None
            if exponent.denominator == 1:
                return integer_power(base, exponent.numerator)
            return elementary(op, base, exponent)

        args = [visit(child, need_interval or op in ("log", "sqrt", "divide"))
                for child in node[1:]]
        if op in ("log", "sqrt"):
            require(args[0], lambda lo, hi: lo > 0 if op == "log" else lo >= 0,
                    op, "argument must be strictly positive" if op == "log"
                    else "argument must be nonnegative")
        if op == "divide":
            require(args[1], lambda lo, hi: hi < 0 or lo > 0, op,
                    "denominator must exclude zero")
        if not need_interval or any(a is None for a in args):
            return None
        if op == "sum":
            return sum((a for a, _ in args), q(0)), sum((b for _, b in args), q(0))
        if op == "times":
            value = (q(1), q(1))
            for a in args:
                value = multiply(value, a)
            return value
        if op == "negate":
            return -args[0][1], -args[0][0]
        if op == "divide":
            return multiply(args[0], (q(1)/args[1][1], q(1)/args[1][0]))
        if op == "square":
            return integer_power(args[0], 2)
        if op == "abs":
            lo, hi = args[0]
            return (q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)),
                    max(abs(lo), abs(hi)))
        if op in _UNARY:
            return elementary(op, args[0])
        return None

    if tree is not None:
        visit(tree, False)
