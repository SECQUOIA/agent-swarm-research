"""Safe (rigorously valid) rational linear cuts for certified-convex rows.

A nonlinear row is  g(x) + l^T x + c <= 0  with g certified convex on the box.
Given a linearization point z (rational) and rational slopes a (close to
grad g(z) + l), the cut  a^T x + b <= 0  is valid on the box  B = [L, U]  whenever
    b <= min_{x in B} phi(x),   phi(x) = g(x) + l^T x + c - a^T x.
Since phi is convex,  phi(x) >= phi(z) + grad phi(z)^T (x - z), hence
    min_B phi >= phi(z) - sum_j max( d_j (z_j - L_j), d_j (z_j - U_j) )
with d = grad phi(z) = grad g(z) + l - a.  All quantities are enclosed with
mpmath interval arithmetic at high precision from the sympy form of g, and
the final b is a rational lower bound of the right-hand side.  The cut can
be reproduced and re-checked from (row expression, z, a, box) alone.
"""
from __future__ import annotations

from fractions import Fraction
import mpmath
from mpmath import iv

from .convexity import frac

PREC_DPS = 60
PREC_BITS = 200


def _iv_from_frac(q):
    q = Fraction(q)
    return iv.mpf(int(q.numerator)) / iv.mpf(int(q.denominator))


def _endpoint_tuple(x):
    """mpf tuple (sign, man, exp, bc) of an interval endpoint or an mpf."""
    if hasattr(x, "_mpi_"):
        a, b = x._mpi_
        if a != b:
            raise ValueError("not a point interval")
        return a
    return x._mpf_


def mpf_to_frac_down(x) -> Fraction:
    """Exact rational value of an mpf endpoint (dyadic), sign included, read
    from its internal tuple so no re-rounding to another precision occurs."""
    sign, man, exp, _ = _endpoint_tuple(x)
    if man == 0:
        if exp != 0:
            raise ValueError("non-finite mpf")
        return Fraction(0)
    val = Fraction(int(man)) * (Fraction(2) ** int(exp))
    return -val if sign else val


class _ivprec:
    """Context manager setting the precision of mpmath's interval context."""
    def __init__(self, bits):
        self.bits = bits
    def __enter__(self):
        self.old = iv.prec
        iv.prec = self.bits
    def __exit__(self, *a):
        iv.prec = self.old


def iv_eval(e, env):
    """Rigorous interval evaluation of a sympy expression tree (Add, Mul, Pow,
    exp, log, sqrt, numbers, symbols). Floats are converted to their exact
    rational values."""
    import sympy
    if e.is_Symbol:
        return env[e]
    if e.is_Integer:
        return iv.mpf(int(e))
    if e.is_Rational:
        return _iv_from_frac(Fraction(int(e.p), int(e.q)))
    if e.is_Float:
        return _iv_from_frac(Fraction(int(sympy.Rational(e).p), int(sympy.Rational(e).q)))
    if e.is_Add:
        out = iv.mpf(0)
        for a in e.args:
            out = out + iv_eval(a, env)
        return out
    if e.is_Mul:
        out = iv.mpf(1)
        for a in e.args:
            out = out * iv_eval(a, env)
        return out
    if e.is_Pow:
        base, ex = e.args
        b = iv_eval(base, env)
        if ex.is_Integer:
            n = int(ex)
            if n >= 0:
                return b ** n
            if b.a <= 0 <= b.b:
                raise ValueError("negative power at zero")
            return iv.mpf(1) / (b ** (-n))
        if ex.is_Rational or ex.is_Float:
            exact_exponent = sympy.Rational(ex)
            q = Fraction(int(exact_exponent.p), int(exact_exponent.q))
            if q == Fraction(1, 2):
                return iv.sqrt(b)
            if b.a <= 0:
                raise ValueError("fractional power of non-positive base")
            return iv.exp(_iv_from_frac(q) * iv.log(b))
        x = iv_eval(ex, env)
        if b.a <= 0:
            raise ValueError("power with non-positive base")
        return iv.exp(x * iv.log(b))
    if isinstance(e, sympy.exp):
        return iv.exp(iv_eval(e.args[0], env))
    if isinstance(e, sympy.log):
        v = iv_eval(e.args[0], env)
        if v.a <= 0:
            raise ValueError("log of non-positive")
        return iv.log(v)
    if isinstance(e, sympy.Abs):
        v = iv_eval(e.args[0], env)
        return iv.mpf([max(0, max(-v.b, v.a)) if not (v.a <= 0 <= v.b) else 0, max(abs(v.a), abs(v.b))])
    raise ValueError(f"unsupported sympy node {type(e).__name__}")


def enclosure_from_sympy(sexpr, symbols, z: list[Fraction]):
    """Evaluate a sympy expression and its gradient at rational z with interval
    arithmetic. Returns (f_interval, [grad intervals])."""
    import sympy
    with _ivprec(PREC_BITS):
        env = {s: _iv_from_frac(q) for s, q in zip(symbols, z)}
        return iv_eval(sexpr, env), [iv_eval(sympy.diff(sexpr, s), env) for s in symbols]


class SafeCutter:
    """Produce safe rational cuts for an NLRow (see lbesh.structure.NLRow).

    The row is g(x) + sum lin_coefs*lin_vars + const <= 0 with g = row.func.
    """

    def __init__(self, row, box: dict, sig_digits=12):
        import sympy
        from .exact_model import exact_sympy
        self.row = row
        from .convexity import validate_expression_domain
        validate_expression_domain(row.func.expr)
        self.symbols, sexpr = exact_sympy(row.func.expr, row.func.vars)
        self.sexpr = sexpr
        self.box = box  # id(var) -> (Fraction lb, Fraction ub)
        self.sig = sig_digits
        self.grad_syms = [sympy.diff(sexpr, s) for s in self.symbols]

    def clip_point(self, zvals) -> dict:
        """Rational point: exact value of the float, clipped into the box."""
        out = {}
        for v in self.row.all_vars():
            q = frac(zvals[id(v)])
            lb, ub = self.box[id(v)]
            lb = None if lb is None else Fraction(lb)
            ub = None if ub is None else Fraction(ub)
            if lb is not None and q < lb:
                q = lb
            if ub is not None and q > ub:
                q = ub
            out[id(v)] = q
        return out

    def _round_dir(self, q: Fraction, direction: int, sig=None) -> Fraction:
        """Round a rational to `sig` significant decimal digits towards
        -inf (direction -1) or +inf (direction +1)."""
        if q == 0:
            return Fraction(0)
        import math
        sig = self.sig if sig is None else sig
        magnitude = abs(q)
        e = len(str(magnitude.numerator)) - len(str(magnitude.denominator))
        if magnitude < Fraction(10) ** e:
            e -= 1
        e -= sig - 1
        scale = Fraction(10) ** e
        n = q / scale
        k = math.floor(n) if direction < 0 else math.ceil(n)
        r = Fraction(k) * scale
        if direction < 0 and r > q:
            r -= scale
        if direction > 0 and r < q:
            r += scale
        return r

    def _round(self, x: float) -> Fraction:
        # decimal rounding to sig significant digits (rational with power-of-10 denominator)
        if x == 0:
            return Fraction(0)
        s = f"{x:.{self.sig - 1}e}"
        return Fraction(s)

    def enclose(self, z: list[Fraction]):
        with _ivprec(PREC_BITS):
            env = {s: _iv_from_frac(q) for s, q in zip(self.symbols, z)}
            fv = iv_eval(self.sexpr, env)
            gv = [iv_eval(g, env) for g in self.grad_syms]
            for enclosure in [fv] + gv:
                mpf_to_frac_down(enclosure.a)
                mpf_to_frac_down(enclosure.b)
        return fv, gv

    def safe_cut(self, zvals: dict, coef_float: dict, const_float: float):
        """zvals: id(var)->float point; coef_float: id(var)->float slope (over
        all row vars incl. linear part). Returns (coef_rational dict, b_rational,
        margin_info) or None if the box is unbounded in a needed direction."""
        row = self.row
        zq = self.clip_point(zvals)   # exact rational point inside the box
        z = [zq[id(v)] for v in row.func.vars]
        a = {vid: self._round(c) for vid, c in coef_float.items()}
        fv, gv = self.enclose(z)
        # Half-line rule: on a coordinate without upper bound the cut is valid
        # only if d_j = grad phi_j >= 0, i.e. a_j <= grad g_j + l_j; choose the
        # rounded slope on the safe side of the enclosure (and symmetrically
        # for coordinates without lower bound).
        gidx0 = {id(v): i for i, v in enumerate(row.func.vars)}
        lcoef0 = {}
        for v, c in zip(row.lin_vars, row.lin_coefs):
            lcoef0[id(v)] = lcoef0.get(id(v), Fraction(0)) + frac(c)
        for vid in list(a.keys()):
            lb, ub = self.box[vid]
            if lb is not None and ub is not None:
                continue
            if vid in gidx0:
                gj = gv[gidx0[vid]]
                glo, ghi = mpf_to_frac_down(gj.a), mpf_to_frac_down(gj.b)
            else:
                glo = ghi = Fraction(0)
            lj = lcoef0.get(vid, Fraction(0))
            if ub is None and lb is None:
                # both sides unbounded: only an exact slope works
                if glo == ghi:
                    a[vid] = glo + lj
                continue
            if ub is None:
                a[vid] = min(a[vid], self._round_dir(glo + lj, -1))
            else:
                a[vid] = max(a[vid], self._round_dir(ghi + lj, +1))
        # phi(z) = g(z) + l^T z + c - a^T z   (interval)
        with _ivprec(PREC_BITS):
            phi = fv + _iv_from_frac(Fraction(row.const))
            lin_at_z = Fraction(0)
            for v, c in zip(row.lin_vars, row.lin_coefs):
                lin_at_z += frac(c) * zq[id(v)]
            a_at_z = Fraction(0)
            for vid, q in a.items():
                a_at_z += q * zq[vid]
            phi = phi + _iv_from_frac(lin_at_z - a_at_z)
            # d_j = grad g_j + l_j - a_j  for all vars of the row
            allvars = {}
            for v in row.func.vars: allvars[id(v)] = v
            for v in row.lin_vars: allvars[id(v)] = v
            lcoef = {}
            for v, c in zip(row.lin_vars, row.lin_coefs):
                lcoef[id(v)] = lcoef.get(id(v), Fraction(0)) + frac(c)
            gidx = {id(v): i for i, v in enumerate(row.func.vars)}
            worst = iv.mpf(0)
            for vid, v in allvars.items():
                d = iv.mpf(0)
                if vid in gidx:
                    d = d + gv[gidx[vid]]
                d = d + _iv_from_frac(lcoef.get(vid, Fraction(0)) - a.get(vid, Fraction(0)))
                zj = zq[vid]  # clipped rational point (same as used for phi)
                lb, ub = self.box[vid]
                lb = None if lb is None else Fraction(lb)
                ub = None if ub is None else Fraction(ub)
                # max( d*(z-L), d*(z-U) ) over the interval d
                if lb is None and ub is None:
                    if d.a == 0 and d.b == 0:
                        continue
                    return None
                if ub is None:
                    if d.a < 0:
                        return None
                    t1 = d * _iv_from_frac(zj - lb)   # d >= 0: minimum at x_j = lb
                    worst = worst + iv.mpf([t1.a, t1.b])
                    continue
                if lb is None:
                    if d.b > 0:
                        return None
                    t2 = d * _iv_from_frac(zj - ub)   # d <= 0: minimum at x_j = ub
                    worst = worst + iv.mpf([t2.a, t2.b])
                    continue
                t1 = d * _iv_from_frac(zj - lb)
                t2 = d * _iv_from_frac(zj - ub)
                worst = worst + iv.mpf([max(t1.a, t2.a), max(t1.b, t2.b)])
            lower = phi - worst  # interval; valid b <= lower.a
            b_lo = lower.a
        # round the rigorous bound down to 30 significant decimal digits: a
        # compact rational with a margin (1e-30 relative) far above the
        # differences between independent 200-bit interval evaluations, so
        # that a checker with its own enclosure re-derives b <= bound.
        b = mpf_to_frac_down(b_lo)
        b = self._round_dir(b, -1, sig=30)
        # cut: a^T x + const_cut <= 0  with const_cut = -b  (a^T x + b_cut <= 0 where b_cut = -min phi ... )
        # We have  a^T x + (l^T x + c - phi(x)) ... careful: phi = g + l x + c - a x >= b  =>  a x + b <= g + l x + c <= 0
        # so the safe cut is  a^T x + b <= 0 with b the rigorous lower bound of phi.
        return a, b, dict(phi_lo=str(phi.a), phi_hi=str(phi.b), shift=str(worst.b), float_const=const_float, z=zq)
