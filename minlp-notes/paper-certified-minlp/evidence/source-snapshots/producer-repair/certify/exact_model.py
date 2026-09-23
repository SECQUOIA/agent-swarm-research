"""Exact interpretation of the expression tree supplied by Pyomo.

Numeric leaves denote their exact stored values (in particular, a Python
float denotes a binary rational). Arithmetic in an existing expression tree
is never evaluated in floating point. Arithmetic performed by the user's
Python code *before* constructing that tree cannot be recovered.

The polynomial extractor deliberately retains nonlinear subtrees, including
ones multiplied by zero: algebraic cancellation must not erase a domain
restriction. Curvature certification checks those original subtrees before
any symbolic simplification used to evaluate a cut.
"""
from fractions import Fraction
from types import SimpleNamespace

import pyomo.environ as pe
from pyomo.core.expr import numeric_expr as NE
from pyomo.core.expr.numvalue import native_numeric_types
from pyomo.common.numeric_types import RegisterNumericType

RegisterNumericType(Fraction)
from pyomo.core.expr.visitor import identify_variables
from pyomo.repn.standard_repn import StandardRepn


class ExactModelError(ValueError):
    """The loaded expression cannot be interpreted by this checker."""


def rational(value):
    if isinstance(value, Fraction):
        return value
    try:
        # Fraction preserves integers and binary floats without a float cast.
        return Fraction(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ExactModelError(f"not a finite rational constant: {value!r}") from exc


def _leaf(expr):
    # Pyomo combines explicit and domain bounds with constant min/max nodes.
    if isinstance(expr, (NE.NPV_MinExpression, NE.NPV_MaxExpression)):
        values = [exact_constant(arg) for arg in expr.args]
        return (min if isinstance(expr, NE.NPV_MinExpression) else max)(values)
    if expr.__class__ in native_numeric_types or isinstance(expr, Fraction):
        return rational(expr)
    if getattr(expr, 'is_parameter_type', lambda: False)():
        return rational(pe.value(expr))
    if getattr(expr, 'is_variable_type', lambda: False)() and expr.is_fixed():
        return rational(expr.value)
    # NumericConstant is a leaf, unlike constant-valued expression nodes.
    if getattr(expr, 'is_constant', lambda: False)() and not hasattr(expr, 'args'):
        return rational(pe.value(expr))
    return None


def exact_constant(expr):
    repn = exact_repn(expr)
    if repn.nonlinear_expr is not None or repn.linear_vars or repn.quadratic_vars:
        raise ExactModelError('expected an exactly rational constant expression')
    return repn.constant


def exact_repn(expr, quadratic=False, **_ignored):
    """StandardRepn interface, with rational polynomial arithmetic throughout.

    Unlike generate_standard_repn, this never computes a transcendental
    constant as a floating value. Such a node stays in nonlinear_expr.
    """
    degree = 2 if quadratic else 1
    variables = {}

    def add(a, b):
        out = dict(a)
        for key, coef in b.items():
            out[key] = out.get(key, Fraction(0)) + coef
        return {k: v for k, v in out.items() if v}

    def mul(a, b):
        out = {}
        for ka, ca in a.items():
            for kb, cb in b.items():
                key = tuple(sorted(ka + kb))
                if len(key) > degree:
                    return None
                out[key] = out.get(key, Fraction(0)) + ca * cb
        return {k: v for k, v in out.items() if v}

    def scale(pair, c):
        p, n = pair
        # Explicit nodes retain even 0*undefined rather than simplifying it.
        return {k: c*v for k, v in p.items() if c*v}, None if n is None else NE.ProductExpression((c, n))

    def walk(e):
        c = _leaf(e)
        if c is not None:
            return ({(): c} if c else {}), None
        if getattr(e, 'is_variable_type', lambda: False)():
            variables[id(e)] = e
            return {(id(e),): Fraction(1)}, None
        if getattr(e, 'is_named_expression_type', lambda: False)():
            return walk(e.expr)
        if isinstance(e, (NE.SumExpression, NE.LinearExpression)):
            p, ns = {}, []
            for arg in e.args:
                ap, an = walk(arg)
                p = add(p, ap)
                if an is not None:
                    ns.append(an)
            return p, None if not ns else ns[0] if len(ns) == 1 else NE.SumExpression(ns)
        if isinstance(e, NE.NegationExpression):
            return scale(walk(e.args[0]), Fraction(-1))
        if isinstance(e, (NE.ProductExpression, NE.MonomialTermExpression)):
            a, b = walk(e.args[0]), walk(e.args[1])
            if a[1] is None and not any(a[0]):
                return scale(b, a[0].get((), Fraction(0)))
            if b[1] is None and not any(b[0]):
                return scale(a, b[0].get((), Fraction(0)))
            if a[1] is None and b[1] is None:
                p = mul(a[0], b[0])
                if p is not None:
                    return p, None
        elif isinstance(e, NE.DivisionExpression):
            b = walk(e.args[1])
            if b[1] is None and not any(b[0]):
                c = b[0].get((), Fraction(0))
                if c == 0:
                    raise ExactModelError('division by zero in expression')
                return scale(walk(e.args[0]), 1/c)
        elif isinstance(e, NE.PowExpression):
            a, b = walk(e.args[0]), walk(e.args[1])
            if b[1] is None and not any(b[0]):
                power = b[0].get((), Fraction(0))
                if a[1] is None and not any(a[0]) and power.denominator == 1:
                    try:
                        value = a[0].get((), Fraction(0)) ** int(power)
                    except ZeroDivisionError as exc:
                        raise ExactModelError('negative power of zero') from exc
                    return ({(): value} if value else {}), None
                if power == 1:
                    return a
                if a[1] is None and power == 2 and degree == 2:
                    p = mul(a[0], a[0])
                    if p is not None:
                        return p, None
                # Retain power zero for nonconstant bases to keep restrictions.
        return {}, e

    p, n = walk(expr)
    repn = StandardRepn()
    repn.constant = p.get((), Fraction(0))
    linear = [(k, v) for k, v in p.items() if len(k) == 1]
    quad = [(k, v) for k, v in p.items() if len(k) == 2]
    repn.linear_vars = tuple(variables[k[0]] for k, _ in linear)
    repn.linear_coefs = tuple(v for _, v in linear)
    repn.quadratic_vars = tuple((variables[k[0]], variables[k[1]]) for k, _ in quad)
    repn.quadratic_coefs = tuple(v for _, v in quad)
    repn.nonlinear_expr = n
    repn.nonlinear_vars = () if n is None else tuple(identify_variables(n, include_fixed=False))
    return repn


def exact_sympy(expr, variables=None):
    """Return (symbols, expression) with rational leaves and real symbols.

    Construction is unevaluated where supported, so original-domain checks
    remain meaningful before differentiation. No Pyomo-to-SymPy float
    conversion or floating coefficient aggregation is used.
    """
    import sympy as sp
    if variables is None:
        variables = list(identify_variables(expr, include_fixed=False))
    symbols = [sp.Symbol(f'x{i}', real=True) for i in range(len(variables))]
    mapping = {id(v): s for v, s in zip(variables, symbols)}

    def visit(e):
        c = _leaf(e)
        if c is not None:
            return sp.Rational(c.numerator, c.denominator)
        if getattr(e, 'is_variable_type', lambda: False)():
            if id(e) not in mapping:
                raise ExactModelError(f'missing variable {e.name}')
            return mapping[id(e)]
        if getattr(e, 'is_named_expression_type', lambda: False)():
            return visit(e.expr)
        args = [visit(a) for a in getattr(e, 'args', ())]
        if isinstance(e, (NE.SumExpression, NE.LinearExpression)):
            return sp.Add(*args, evaluate=False)
        if isinstance(e, NE.NegationExpression):
            return sp.Mul(-1, args[0], evaluate=False)
        if isinstance(e, (NE.ProductExpression, NE.MonomialTermExpression)):
            return sp.Mul(*args, evaluate=False)
        if isinstance(e, NE.DivisionExpression):
            return sp.Mul(args[0], sp.Pow(args[1], -1, evaluate=False), evaluate=False)
        if isinstance(e, NE.PowExpression):
            return sp.Pow(*args, evaluate=False)
        if isinstance(e, NE.AbsExpression):
            return sp.Abs(args[0], evaluate=False)
        if isinstance(e, NE.UnaryFunctionExpression):
            functions = {'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt, 'abs': sp.Abs}
            name = e.getname()
            if name in functions:
                return functions[name](args[0], evaluate=False)
        raise ExactModelError(f'unsupported expression node {type(e).__name__}')

    return symbols, visit(expr)


def exact_constraint_rows(con):
    """Certified nonlinear rows, with the naming used by the OA producer."""
    from lbesh.structure import NLRow
    repn = exact_repn(con.body)
    if repn.nonlinear_expr is None:
        return []
    if con.lower is not None and con.upper is not None:
        raise ExactModelError(f'two-sided nonlinear constraint {con.name}')
    out = []
    for side, bound, sign in [('ub', con.upper, 1), ('lb', con.lower, -1)]:
        if bound is None:
            continue
        expr = repn.nonlinear_expr if sign == 1 else NE.NegationExpression((repn.nonlinear_expr,))
        # Only expr/vars are needed by SafeCutter and the replay checker.
        func = SimpleNamespace(expr=expr, vars=list(identify_variables(expr, include_fixed=False)))
        out.append(NLRow(f'{con.name}_{side}', func, list(repn.linear_vars),
                         [sign*c for c in repn.linear_coefs], sign*(repn.constant-exact_constant(bound))))
    return out
