"""Rule-based (DCP-style) convexity certification of Pyomo expressions with
exact rational parameter checks.

certify(expr) returns a Certificate with curvature in {'affine','convex',
'concave','unknown'} and a human-readable derivation. Variable bounds are used
for sign/domain information (rational, taken from the Pyomo bounds).
Quadratic forms are certified via an exact LDL^T factorization over the
rationals (PSD <=> factorization with nonnegative pivots, with pivoting on
zero pivots handled by the standard rational algorithm).
"""
from __future__ import annotations

from fractions import Fraction
import math
from dataclasses import dataclass

import pyomo.environ as pe
from pyomo.core.expr import numeric_expr as NE
from pyomo.core.expr.numvalue import is_constant, value as pvalue, native_numeric_types
from .exact_model import exact_repn as generate_standard_repn, exact_constant, rational, ExactModelError


AFFINE, CONVEX, CONCAVE, UNKNOWN = "affine", "convex", "concave", "unknown"


def frac(x) -> Fraction:
    return rational(x)


@dataclass
class Cert:
    curv: str
    lo: Fraction | None = None      # rigorous range lower bound (rational) or None
    hi: Fraction | None = None
    why: str = ""

    @property
    def nonneg(self):
        return self.lo is not None and self.lo >= 0

    @property
    def nonpos(self):
        return self.hi is not None and self.hi <= 0

    @property
    def positive(self):
        return self.lo is not None and self.lo > 0


def _neg(c: Cert, why):
    curv = {AFFINE: AFFINE, CONVEX: CONCAVE, CONCAVE: CONVEX, UNKNOWN: UNKNOWN}[c.curv]
    lo = None if c.hi is None else -c.hi
    hi = None if c.lo is None else -c.lo
    return Cert(curv, lo, hi, why)


def _scale(c: Cert, k: Fraction, why):
    if k == 0:
        return Cert(AFFINE, Fraction(0), Fraction(0), why)
    if k > 0:
        lo = None if c.lo is None else k * c.lo
        hi = None if c.hi is None else k * c.hi
        return Cert(c.curv, lo, hi, why)
    cc = _neg(c, why)
    return _scale(cc, -k, why)


def _add(a: Cert, b: Cert, why):
    if a.curv == AFFINE:
        curv = b.curv
    elif b.curv == AFFINE:
        curv = a.curv
    elif a.curv == b.curv:
        curv = a.curv
    else:
        curv = UNKNOWN
    lo = None if (a.lo is None or b.lo is None) else a.lo + b.lo
    hi = None if (a.hi is None or b.hi is None) else a.hi + b.hi
    return Cert(curv, lo, hi, why)


def _var_cert(v):
    lb = None if v.lb is None else exact_constant(v.lower)
    ub = None if v.ub is None else exact_constant(v.upper)
    if v.is_fixed():
        lb = ub = frac(v.value)
    return Cert(AFFINE, lb, ub, f"var {v.name}")


def _const_cert(x):
    k = frac(x)
    return Cert(AFFINE, k, k, f"const {k}")


def _interval_mul(a: Cert, b: Cert):
    if None in (a.lo, a.hi, b.lo, b.hi):
        if a.nonneg and b.nonneg:
            return a.lo*b.lo, None if a.hi is None or b.hi is None else a.hi*b.hi
        if a.nonpos and b.nonpos:
            return a.hi*b.hi, None if a.lo is None or b.lo is None else a.lo*b.lo
        if a.nonneg and b.nonpos:
            return None if a.hi is None or b.lo is None else a.hi*b.lo, a.lo*b.hi
        if a.nonpos and b.nonneg:
            return None if a.lo is None or b.hi is None else a.lo*b.hi, a.hi*b.lo
        return None, None
    prods = [a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi]
    return min(prods), max(prods)


def _pow_cert(base: Cert, p: Fraction, why):
    # base ** p with constant rational p
    lo = hi = None
    if base.lo is not None and base.hi is not None and base.lo >= 0:
        # monotone on nonnegative domain
        if p >= 0:
            lo, hi = _rpow(base.lo, p, "down"), _rpow(base.hi, p, "up")
        elif base.lo > 0:
            lo, hi = _rpow(base.hi, p, "down"), _rpow(base.lo, p, "up")
    if p.denominator == 1 and p.numerator % 2 == 0 and p >= 2:
        # even power: convex for affine base; convex if base convex and nonneg, or concave and nonpos
        if base.curv == AFFINE:
            lo2 = Fraction(0)
            if base.lo is not None and base.hi is not None:
                if base.lo >= 0:
                    lo2, hi = base.lo ** p.numerator, base.hi ** p.numerator
                elif base.hi <= 0:
                    lo2, hi = base.hi ** p.numerator, base.lo ** p.numerator
                else:
                    lo2, hi = Fraction(0), max(base.lo ** p.numerator, base.hi ** p.numerator)
            return Cert(CONVEX, lo2, hi, why + " even power of affine")
        if base.curv == CONVEX and base.nonneg:
            return Cert(CONVEX, lo, hi, why + " even power of nonneg convex")
        if base.curv == CONCAVE and base.nonpos:
            return Cert(CONVEX, lo if lo is not None else Fraction(0), hi, why + " even power of nonpos concave")
        return Cert(UNKNOWN, Fraction(0) if p.denominator == 1 else None, None, why + " even power, sign unknown")
    if p >= 1 and base.nonneg:
        if base.curv in (AFFINE, CONVEX):
            return Cert(CONVEX, lo, hi, why + f" power p={p}>=1 of nonneg convex")
        return Cert(UNKNOWN, lo, hi, why)
    if 0 < p < 1 and base.nonneg:
        if base.curv in (AFFINE, CONCAVE):
            return Cert(CONCAVE, lo, hi, why + f" power 0<p={p}<1 of nonneg concave")
        return Cert(UNKNOWN, lo, hi, why)
    if p < 0 and base.positive:
        if base.curv in (AFFINE, CONCAVE):
            return Cert(CONVEX, lo, hi, why + f" power p={p}<0 of positive concave")
        return Cert(UNKNOWN, lo, hi, why)
    if p == 1:
        return Cert(base.curv, base.lo, base.hi, why + " power 1")
    if p == 0:
        return Cert(AFFINE, Fraction(1), Fraction(1), why + " power 0")
    return Cert(UNKNOWN, lo, hi, why + " power: domain/sign not certified")


def _rpow(x: Fraction, p: Fraction, direction):
    """Rational bound of x**p (x >= 0) rounded outward, computed with
    interval arithmetic (exact for integer p)."""
    if x == 0:
        return Fraction(0)
    if p.denominator == 1:
        n = int(p)
        return x ** n if n >= 0 else Fraction(1) / (x ** (-n))
    from mpmath import iv
    old = iv.prec
    try:
        iv.prec = 128
        xi = iv.mpf(int(x.numerator)) / iv.mpf(int(x.denominator))
        pi = iv.mpf(int(p.numerator)) / iv.mpf(int(p.denominator))
        r = iv.exp(pi * iv.log(xi))
        end = r.a if direction == "down" else r.b
        sign, man, exp, _ = end._mpi_[0] if hasattr(end, "_mpi_") else end._mpf_
        if man == 0 and exp != 0:
            raise ExactModelError("non-finite interval endpoint")
        val = Fraction(int(man)) * (Fraction(2) ** int(exp))
        return -val if sign else val
    finally:
        iv.prec = old


def _iv_frac_bound(q: Fraction, fn, direction):
    from mpmath import iv
    old = iv.prec
    try:
        iv.prec = 128
        r = fn(iv.mpf(int(q.numerator)) / iv.mpf(int(q.denominator)))
        end = r.a if direction == "down" else r.b
        sign, man, exp, _ = end._mpi_[0] if hasattr(end, "_mpi_") else end._mpf_
        if man == 0 and exp != 0:
            raise ExactModelError("non-finite interval endpoint")
        val = Fraction(int(man)) * (Fraction(2) ** int(exp))
        return -val if sign else val
    finally:
        iv.prec = old


def _exp_range(c: Cert):
    from mpmath import iv
    lo = None if c.lo is None else _iv_frac_bound(c.lo, iv.exp, "down")
    hi = None if c.hi is None else _iv_frac_bound(c.hi, iv.exp, "up")
    if lo is not None and lo < 0:
        lo = Fraction(0)
    return lo, hi


def _log_range(c: Cert):
    from mpmath import iv
    lo = None if (c.lo is None or c.lo <= 0) else _iv_frac_bound(c.lo, iv.log, "down")
    hi = None if (c.hi is None or c.hi <= 0) else _iv_frac_bound(c.hi, iv.log, "up")
    return lo, hi


def validate_expression_domain(expr):
    """Reject unsupported nodes and domains not certified on variable bounds.

    Inspect the original tree before simplification. This deliberately rejects
    some valid expressions whose domain cannot be established by these rules.
    """
    if expr.__class__ in native_numeric_types or isinstance(expr, Fraction):
        rational(expr)
        return
    if getattr(expr, "is_variable_type", lambda: False)():
        _var_cert(expr)
        return
    if getattr(expr, "is_parameter_type", lambda: False)():
        rational(pvalue(expr))
        return
    if getattr(expr, "is_named_expression_type", lambda: False)():
        validate_expression_domain(expr.expr)
        return
    if is_constant(expr) and not hasattr(expr, "args"):
        rational(pvalue(expr))
        return
    supported = (NE.SumExpression, NE.LinearExpression, NE.NegationExpression,
                 NE.ProductExpression, NE.MonomialTermExpression,
                 NE.DivisionExpression, NE.PowExpression, NE.UnaryFunctionExpression,
                 NE.AbsExpression)
    if not isinstance(expr, supported):
        raise ExactModelError(f"unsupported expression node {type(expr).__name__}")
    for arg in expr.args:
        validate_expression_domain(arg)
    if isinstance(expr, NE.DivisionExpression):
        den = _certify(expr.args[1])
        if not (den.positive or (den.hi is not None and den.hi < 0)):
            raise ExactModelError("denominator not certified away from zero")
    elif isinstance(expr, NE.PowExpression):
        base, exponent = expr.args
        b, p = _certify(base), _certify(exponent)
        if p.lo is not None and p.lo == p.hi:
            q = p.lo
            if q.denominator == 1:
                if q < 0 and not (b.positive or (b.hi is not None and b.hi < 0)):
                    raise ExactModelError("negative power base not certified away from zero")
            elif not (b.positive if q < 0 else b.nonneg):
                raise ExactModelError("fractional power domain not certified")
        elif not b.positive:
            raise ExactModelError("variable power base not certified positive")
    elif isinstance(expr, NE.UnaryFunctionExpression):
        name = expr.getname()
        c = _certify(expr.args[0])
        if name == "log" and not c.positive:
            raise ExactModelError("log argument not certified positive")
        if name == "sqrt" and not c.nonneg and _sqrt_quadratic(expr.args[0]) is None:
            raise ExactModelError("sqrt argument not certified nonnegative")
        if name not in ("exp", "log", "sqrt", "abs"):
            raise ExactModelError(f"unsupported unary function {name}")


def certify(expr) -> Cert:
    try:
        validate_expression_domain(expr)
        return _certify(expr)
    except (ExactModelError, ValueError, ZeroDivisionError, OverflowError) as exc:
        return Cert(UNKNOWN, None, None, f"domain or exact evaluation: {exc}")


def _certify(expr) -> Cert:
    """Certify curvature after checking the original expression domain."""
    if expr.__class__ in native_numeric_types or isinstance(expr, Fraction):
        return _const_cert(expr)
    if is_constant(expr) and not hasattr(expr, "args"):
        return _const_cert(pvalue(expr))
    if isinstance(expr, pe.Var.__mro__[0]) or hasattr(expr, "is_variable_type") and expr.is_variable_type():
        return _var_cert(expr)
    if hasattr(expr, "is_parameter_type") and expr.is_parameter_type():
        return _const_cert(pvalue(expr))
    if isinstance(expr, NE.NegationExpression):
        return _neg(certify(expr.args[0]), "negation")
    if isinstance(expr, (NE.SumExpression, NE.LinearExpression)):
        q = _try_quadratic(expr)
        if q is not None:
            return q
        out = Cert(AFFINE, Fraction(0), Fraction(0), "sum")
        for a in expr.args:
            out = _add(out, certify(a), "sum")
        return out
    if isinstance(expr, NE.MonomialTermExpression):
        k, v = expr.args
        return _scale(certify(v), exact_constant(k), "monomial")
    if isinstance(expr, NE.ProductExpression):
        a, b = expr.args
        mono = _monomial(expr)
        if mono is not None:
            mc = _monomial_cert(mono)
            if mc.curv != UNKNOWN:
                return mc
        ca, cb = certify(a), certify(b)
        if ca.lo is not None and ca.lo == ca.hi:
            return _scale(cb, ca.lo, "product by constant")
        if cb.lo is not None and cb.lo == cb.hi:
            return _scale(ca, cb.lo, "product by constant")
        # Curvature and range are separate facts: even an indefinite
        # product can be nonnegative on the box (needed for sqrt(x*y)).
        out = _quadratic_or_unknown(expr)
        out.lo, out.hi = _interval_mul(ca, cb)
        return out
    if isinstance(expr, NE.DivisionExpression):
        a, b = expr.args
        cb = certify(b)
        if cb.lo is not None and cb.lo == cb.hi and cb.lo != 0:
            return _scale(certify(a), 1 / cb.lo, "division by constant")
        ca = certify(a)
        if ca.lo is not None and ca.lo == ca.hi:
            # k / g with g positive concave: 1/g is convex, so k/g is convex
            # for k > 0 and concave for k < 0.
            k = ca.lo
            if cb.positive and cb.curv in (AFFINE, CONCAVE):
                if k > 0:
                    lo, hi = (k / cb.hi if cb.hi else None), k / cb.lo
                    return Cert(CONVEX, lo, hi, "positive const / positive concave")
                if k < 0:
                    lo, hi = k / cb.lo, (k / cb.hi if cb.hi else None)
                    return Cert(CONCAVE, lo, hi, "negative const / positive concave")
        lf = _linear_fractional(a, b)
        if lf is not None:
            return lf
        return Cert(UNKNOWN, None, None, "division")
    if isinstance(expr, NE.PowExpression):
        base, exponent = expr.args
        ce = certify(exponent)
        if ce.lo is not None and ce.lo == ce.hi:
            return _pow_cert(certify(base), ce.lo, "pow")
        cbse = certify(base)
        if cbse.lo is not None and cbse.lo == cbse.hi and cbse.lo > 0:
            k = cbse.lo
            # k ** g = exp(g ln k)
            if ce.curv == AFFINE:
                return Cert(CONVEX, Fraction(0), None, "const>0 ** affine")
            if k > 1 and ce.curv == CONVEX:
                return Cert(CONVEX, Fraction(0), None, "const>1 ** convex")
            if k < 1 and ce.curv == CONCAVE:
                return Cert(CONVEX, Fraction(0), None, "const<1 ** concave")
        return Cert(UNKNOWN, None, None, "pow with variable exponent")
    if isinstance(expr, NE.UnaryFunctionExpression):
        name = expr.getname()
        c = certify(expr.args[0])
        if name == "exp":
            lo, hi = _exp_range(c)
            if c.curv in (AFFINE, CONVEX):
                return Cert(CONVEX, lo if lo is not None else Fraction(0), hi, "exp of convex")
            return Cert(UNKNOWN, Fraction(0), hi, "exp of non-convex")
        if name == "log":
            lo, hi = _log_range(c)
            if c.curv in (AFFINE, CONCAVE) and c.positive:
                return Cert(CONCAVE, lo, hi, "log of positive concave")
            return Cert(UNKNOWN, lo, hi, "log: argument not certified positive concave")
        if name == "sqrt":
            mono = _monomial(expr)
            if mono is not None:
                mc = _monomial_cert(mono)
                if mc.curv != UNKNOWN:
                    return mc
            qn = _sqrt_quadratic(expr.args[0])
            if qn is not None:
                return qn
            if c.curv in (AFFINE, CONCAVE) and c.nonneg:
                lo = None if c.lo is None else _rpow(c.lo, Fraction(1, 2), "down")
                hi = None if c.hi is None else _rpow(c.hi, Fraction(1, 2), "up")
                return Cert(CONCAVE, lo, hi, "sqrt of nonneg concave")
            return Cert(UNKNOWN, Fraction(0), None, "sqrt: argument not certified")
        if name == "abs":
            if c.curv == AFFINE:
                hi = None if (c.lo is None or c.hi is None) else max(abs(c.lo), abs(c.hi))
                return Cert(CONVEX, Fraction(0), hi, "abs of affine")
            return Cert(UNKNOWN, Fraction(0), None, "abs of non-affine")
        return Cert(UNKNOWN, None, None, f"unary {name}")
    if isinstance(expr, NE.AbsExpression):
        c = certify(expr.args[0])
        if c.curv == AFFINE:
            return Cert(CONVEX, Fraction(0), None, "abs of affine")
        return Cert(UNKNOWN, Fraction(0), None, "abs")
    if isinstance(expr, NE.Expr_ifExpression):
        return Cert(UNKNOWN, None, None, "expr_if")
    if hasattr(expr, "is_named_expression_type") and expr.is_named_expression_type():
        return certify(expr.expr)
    return Cert(UNKNOWN, None, None, f"unhandled {type(expr).__name__}")


def _quadratic_or_unknown(expr):
    """Try to certify a product expression as part of a quadratic form."""
    try:
        repn = generate_standard_repn(expr, compute_values=True, quadratic=True)
    except Exception:
        return Cert(UNKNOWN, None, None, "product: repn failed")
    if repn.nonlinear_expr is not None:
        return Cert(UNKNOWN, None, None, "product: non-quadratic")
    return quadratic_cert(repn)


def quadratic_cert(repn):
    """Certify a quadratic standard repn: convex iff Q PSD (exact LDL^T)."""
    vars_ = {}
    for (v1, v2) in repn.quadratic_vars:
        vars_.setdefault(id(v1), v1); vars_.setdefault(id(v2), v2)
    idx = {vid: i for i, vid in enumerate(vars_)}
    n = len(idx)
    Q = [[Fraction(0)] * n for _ in range(n)]
    for (v1, v2), c in zip(repn.quadratic_vars, repn.quadratic_coefs):
        i, j = idx[id(v1)], idx[id(v2)]
        c = frac(pvalue(c))
        if i == j:
            Q[i][i] += c
        else:
            Q[i][j] += c / 2
            Q[j][i] += c / 2
    psd = is_psd(Q)
    nsd = is_psd([[-x for x in row] for row in Q])
    if psd and nsd:
        curv = AFFINE
    elif psd:
        curv = CONVEX
    elif nsd:
        curv = CONCAVE
    else:
        curv = UNKNOWN
    return Cert(curv, None, None, f"quadratic form n={n}: psd={psd} nsd={nsd}")


def is_psd(Q):
    """Exact PSD test by symmetric Gaussian elimination over the rationals."""
    n = len(Q)
    A = [row[:] for row in Q]
    for k in range(n):
        # find pivot
        if A[k][k] == 0:
            # if diagonal is zero, the whole row/col must be zero for PSD
            if any(A[k][j] != 0 for j in range(k, n)):
                return False
            continue
        if A[k][k] < 0:
            return False
        p = A[k][k]
        for i in range(k + 1, n):
            if A[i][k] == 0:
                continue
            f = A[i][k] / p
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True


def certify_constraint(con):
    """Return (kind, cert) where kind in {'convex_row','concave_row','affine','unknown','equality'}.
    For body <= ub we need convex body; for body >= lb we need concave body."""
    body = con.body
    c = certify(body)
    lower = con.lower is not None
    upper = con.upper is not None
    if c.curv == AFFINE:
        return "affine", c
    if lower and upper:
        return "equality_or_range", c
    if upper:
        return ("convex_row" if c.curv == CONVEX else "unknown"), c
    if lower:
        return ("concave_row" if c.curv == CONCAVE else "unknown"), c
    return "free", c


def _try_quadratic(expr):
    """If expr is a (non-affine) quadratic polynomial, certify it by PSD."""
    try:
        repn = generate_standard_repn(expr, compute_values=True, quadratic=True)
    except Exception:
        return None
    if repn.nonlinear_expr is not None or not repn.quadratic_vars:
        return None
    return quadratic_cert(repn)


def _sqrt_quadratic(arg):
    """sqrt(q(x)) with q quadratic: a sufficient convexity test is that the homogenized matrix
    [[Q, b/2],[b^T/2, c]] is PSD (then q = ||Lx+d||^2 + e, e>=0)."""
    try:
        repn = generate_standard_repn(arg, compute_values=True, quadratic=True)
    except Exception:
        return None
    if repn.nonlinear_expr is not None or not repn.quadratic_vars:
        return None
    vars_ = {}
    for (v1, v2) in repn.quadratic_vars:
        vars_.setdefault(id(v1), v1); vars_.setdefault(id(v2), v2)
    for v in repn.linear_vars:
        vars_.setdefault(id(v), v)
    idx = {vid: i for i, vid in enumerate(vars_)}
    n = len(idx)
    M = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    for (v1, v2), c in zip(repn.quadratic_vars, repn.quadratic_coefs):
        i, j = idx[id(v1)], idx[id(v2)]
        c = frac(pvalue(c))
        if i == j:
            M[i][i] += c
        else:
            M[i][j] += c / 2; M[j][i] += c / 2
    for v, c in zip(repn.linear_vars, repn.linear_coefs):
        i = idx[id(v)]
        c = frac(pvalue(c))
        M[i][n] += c / 2; M[n][i] += c / 2
    M[n][n] += frac(pvalue(repn.constant))
    if is_psd(M):
        return Cert(CONVEX, Fraction(0), None, f"sqrt of PSD-homogenized quadratic n={n}")
    return None


def _monomial(expr):
    """Decompose a product/power tree into {id(var): (var, exponent)} and a
    constant factor, or return None if not a monomial with constant exponents."""
    factors = {}
    const = Fraction(1)

    def visit(e, sign_exp):
        nonlocal const
        if e.__class__ in native_numeric_types or (is_constant(e) and not hasattr(e, "args")):
            k = exact_constant(e)
            if sign_exp == 1:
                const *= k
            else:
                if k == 0:
                    raise ValueError
                const /= k
            return
        if hasattr(e, "is_variable_type") and e.is_variable_type():
            vid = id(e)
            v, p = factors.get(vid, (e, Fraction(0)))
            factors[vid] = (v, p + sign_exp)
            return
        if isinstance(e, NE.ProductExpression):
            visit(e.args[0], sign_exp); visit(e.args[1], sign_exp); return
        if isinstance(e, NE.DivisionExpression):
            visit(e.args[0], sign_exp); visit(e.args[1], -sign_exp); return
        if isinstance(e, NE.MonomialTermExpression):
            visit(e.args[0], sign_exp); visit(e.args[1], sign_exp); return
        if isinstance(e, NE.PowExpression):
            b, ex = e.args
            if ex.__class__ in native_numeric_types or is_constant(ex):
                p = exact_constant(ex)
                if p.denominator != 1:
                    # fractional power: base must be a positive monomial; scale exponents
                    sub = _monomial(b)
                    if sub is None or sub[0] <= 0:
                        raise ValueError
                    c0, f0 = sub
                    if any(not _var_cert(v).nonneg for v, q in f0.values()):
                        raise ValueError
                    if c0 != 1:
                        raise ValueError  # fractional powers retain exact unit constants only
                    for vid, (v, q) in f0.items():
                        vv, qq = factors.get(vid, (v, Fraction(0)))
                        factors[vid] = (vv, qq + sign_exp * p * q)
                    return
                sub = _monomial(b)
                if sub is None:
                    raise ValueError
                c0, f0 = sub
                k = c0 ** int(p) if p >= 0 else Fraction(1) / (c0 ** int(-p))
                if sign_exp == 1:
                    const *= k
                else:
                    const /= k
                for vid, (v, q) in f0.items():
                    vv, qq = factors.get(vid, (v, Fraction(0)))
                    factors[vid] = (vv, qq + sign_exp * p * q)
                return
            raise ValueError
        if isinstance(e, NE.UnaryFunctionExpression) and e.getname() == "sqrt":
            sub = _monomial(e.args[0])
            if sub is None or sub[0] != 1:
                raise ValueError
            if any(not _var_cert(v).nonneg for v, q in sub[1].values()):
                raise ValueError
            for vid, (v, q) in sub[1].items():
                vv, qq = factors.get(vid, (v, Fraction(0)))
                factors[vid] = (vv, qq + sign_exp * q / 2)
            return
        raise ValueError
    try:
        visit(expr, 1)
    except ValueError:
        return None
    return const, factors


def _monomial_cert(mono):
    """c * prod x_i^{a_i} on the positive orthant: convex iff all a_i <= 0,
    or exactly one a_i > 0 with sum a_i >= 1 and the rest <= 0 (Lundell and
    Westerlund's conditions); concave iff all a_i >= 0 and sum a_i <= 1."""
    const, factors = mono
    if const == 0:
        return Cert(AFFINE, Fraction(0), Fraction(0), "zero monomial")
    pairs = [(v, p) for (v, p) in factors.values() if p != 0]
    vars_ = [v for v, _ in pairs]
    exps = [p for _, p in pairs]
    # domain: need positive variables for fractional/negative exponents
    positive = all(v.lb is not None and exact_constant(v.lower) > 0 for v in vars_)
    nonneg = all(v.lb is not None and exact_constant(v.lower) >= 0 for v in vars_)
    if not exps:
        return Cert(AFFINE, const, const, "constant")
    if len(exps) == 1 and exps[0] == 1:
        return _scale(_var_cert(vars_[0]), const, "linear monomial")
    convex = False
    concave = False
    if positive or (nonneg and all(p > 0 for p in exps)):
        pos = [p for p in exps if p > 0]
        if all(p <= 0 for p in exps):
            convex = True
        elif len(pos) == 1 and sum(exps) >= 1:
            convex = True
        if all(p >= 0 for p in exps) and sum(exps) <= 1:
            concave = True
    why = f"monomial exps={[str(p) for p in exps]} const={const} positive={positive}"
    if convex and not concave:
        curv = CONVEX
    elif concave and not convex:
        curv = CONCAVE
    elif convex and concave:
        curv = AFFINE
    else:
        return Cert(UNKNOWN, None, None, why + " not certified")
    c = Cert(curv, Fraction(0) if nonneg else None, None, why)
    return _scale(c, const, why)


def _linear_fractional(num, den):
    """(alpha v + beta)/(gamma v + delta) in a single variable v with the
    denominator of certified constant sign on the box."""
    try:
        rn = generate_standard_repn(num, compute_values=True, quadratic=False)
        rd = generate_standard_repn(den, compute_values=True, quadratic=False)
    except Exception:
        return None
    if not (rn.is_linear() and rd.is_linear()) or len(rd.linear_vars) != 1:
        return None
    v = rd.linear_vars[0]
    if len(rn.linear_vars) > 1 or (len(rn.linear_vars) == 1 and rn.linear_vars[0] is not v):
        return None
    gamma, delta = frac(pvalue(rd.linear_coefs[0])), frac(pvalue(rd.constant))
    alpha = frac(pvalue(rn.linear_coefs[0])) if rn.linear_vars else Fraction(0)
    beta = frac(pvalue(rn.constant))
    if gamma == 0:
        return None
    cd = certify(den)
    if cd.positive:
        sign = 1
    elif cd.hi is not None and cd.hi < 0:
        sign = -1
    else:
        return None
    # a/b = alpha/gamma + (beta - alpha*delta/gamma)/(gamma v + delta)
    k = beta - alpha * delta / gamma
    # 1/(w) with w>0 convex decreasing; k/w convex if k>0 (w>0) ; if w<0: 1/w concave -> k/w concave for k>0
    if k == 0:
        return Cert(AFFINE, alpha / gamma, alpha / gamma, "linear-fractional reduces to constant")
    if (k > 0 and sign > 0) or (k < 0 and sign < 0):
        return Cert(CONVEX, None, None, "linear-fractional single variable: convex")
    return Cert(CONCAVE, None, None, "linear-fractional single variable: concave")
