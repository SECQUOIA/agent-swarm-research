"""Rigorous check that an exactly feasible point exists near a MINLPLib point,
and an enclosure of its objective value.

Two routes:

A. exact check (no polishing). Every row is evaluated at the exact decimals of
   the point: in exact rational arithmetic (Fraction) when the row is a
   polynomial with integer exponents, otherwise in outward-rounded interval
   arithmetic (mpmath iv). Equality rows need exact arithmetic; inequality rows
   and bounds may use intervals. Integer variables must be exact integers.

B. polish + Krawczyk. Integer variables are rounded; continuous variables within
   `tb` of a bound are put on the bound; the remaining continuous variables that
   occur in active rows (equalities, and inequalities within `ta` of a side or
   violated) are candidates. A basis of |active rows| candidates is chosen by
   QR with column pivoting on the Jacobian (columns weighted by distance to the
   bounds); the other candidates stay at their exact decimals. Newton on the
   square system (residuals at 40 digits), then a Krawczyk test on a box X
   around the Newton point proves that X contains a solution of the square
   system. Every other row, all bounds of the basic variables, and the
   objective are then enclosed over X. If all rows and bounds hold on X, the
   solution in X is exactly feasible and its objective lies in the enclosure.

The Krawczyk operator is the midpoint-radius form of
reviews/wave2-small-verification/krawczyk.py (same error bounds):
    beta = |R Fc| + |R| Fr + |I - R Jc| r + |R| Jr r  <  r   (componentwise).
Assumptions: mpmath iv encloses exp, log, sqrt, sin, cos correctly; numpy/BLAS
double arithmetic is IEEE. tanh and erf (not used by any case in this audit)
are rejected.
"""
import math
from fractions import Fraction

import mpmath
import numpy as np
import scipy.linalg
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from mpmath import iv

import audit_eval as A
import osilx

U_ROUND = 2.0 ** -53
SAFE = 1 + 1e-6
TINY = 1e-300
iv.dps = 40


class NotSupported(Exception):
    pass


# ------------------------------------------------------------------ interval AD
class AD:
    __slots__ = ("v", "d")

    def __init__(self, v, d=None):
        self.v = v
        self.d = d if d is not None else {}

    @staticmethod
    def lift(o):
        return o if isinstance(o, AD) else AD(o)

    def __add__(a, b):
        b = AD.lift(b)
        if not b.d:
            return AD(a.v + b.v, a.d)
        d = dict(a.d)
        for k, x in b.d.items():
            d[k] = d[k] + x if k in d else x
        return AD(a.v + b.v, d)

    __radd__ = __add__

    def __neg__(a):
        return AD(-a.v, {k: -x for k, x in a.d.items()})

    def __sub__(a, b):
        return a + (-AD.lift(b))

    def __rsub__(a, b):
        return AD.lift(b) + (-a)

    def __mul__(a, b):
        b = AD.lift(b)
        d = {k: x * b.v for k, x in a.d.items()}
        for k, x in b.d.items():
            d[k] = d[k] + a.v * x if k in d else a.v * x
        return AD(a.v * b.v, d)

    __rmul__ = __mul__

    def __truediv__(a, b):
        b = AD.lift(b)
        if 0 in b.v:
            raise ZeroDivisionError("divisor interval contains 0")
        q = a.v / b.v
        d = {k: x / b.v for k, x in a.d.items()}
        for k, x in b.d.items():
            t = -q * x / b.v
            d[k] = d[k] + t if k in d else t
        return AD(q, d)

    def chain(self, val, der):
        return AD(val, {k: der * x for k, x in self.d.items()})


_NUM = {}


def ivn(s):
    if s not in _NUM:
        _NUM[s] = iv.mpf(s)  # decimal string, enclosed outward
    return _NUM[s]


def _ipow(v, k):
    return v ** k  # mpmath iv integer power (handles even powers of sign-changing intervals)


def ad_power(a, b, bconst):
    if bconst is not None and Fraction(bconst).denominator == 1:
        k = int(Fraction(bconst))
        if k == 0:
            return AD(iv.mpf(1))
        return a.chain(_ipow(a.v, k), k * _ipow(a.v, k - 1) if k != 1 else iv.mpf(1))
    if not a.v.a > 0:
        raise NotSupported("fractional power needs a positive base interval")
    la = iv.log(a.v)
    if bconst is not None:
        e = ivn(bconst)
        val = iv.exp(e * la)
        return a.chain(val, e * val / a.v)
    val = iv.exp(b.v * la)
    out = AD(val, {})
    for k, x in a.d.items():
        out.d[k] = val * b.v / a.v * x
    for k, x in b.d.items():
        t = val * la * x
        out.d[k] = out.d[k] + t if k in out.d else t
    return out


def ev(t, x):
    op = t[0]
    if op == "num":
        return AD(ivn(t[1]))
    if op == "var":
        v = x[t[1]]
        return v if t[2] == "1" else v * ivn(t[2])
    if op == "power":
        a = ev(t[1], x)
        bconst = t[2][1] if t[2][0] == "num" else None
        b = None if bconst is not None else ev(t[2], x)
        return ad_power(a, b, bconst)
    if op == "signpower":
        a = ev(t[1], x)
        assert t[2][0] == "num"
        p = ivn(t[2][1])
        if a.v.a > 0:
            val = iv.exp(p * iv.log(a.v))
            return a.chain(val, p * val / a.v)
        if a.v.b < 0:
            val = iv.exp(p * iv.log(-a.v))
            return a.chain(-val, p * val / (-a.v))
        raise NotSupported("signpower at 0")
    a = [ev(c, x) for c in t[1:]]
    if op in ("sum", "plus"):
        s = a[0]
        for b in a[1:]:
            s = s + b
        return s
    if op in ("product", "times"):
        s = a[0]
        for b in a[1:]:
            s = s * b
        return s
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "square":
        return a[0].chain(a[0].v ** 2, 2 * a[0].v)
    if op == "exp":
        e = iv.exp(a[0].v)
        return a[0].chain(e, e)
    if op == "ln":
        if not a[0].v.a > 0:
            raise NotSupported("log of interval not > 0")
        return a[0].chain(iv.log(a[0].v), 1 / a[0].v)
    if op == "log10":
        if not a[0].v.a > 0:
            raise NotSupported("log10 of interval not > 0")
        l10 = iv.log(iv.mpf(10))
        return a[0].chain(iv.log(a[0].v) / l10, 1 / (a[0].v * l10))
    if op == "sqrt":
        if not a[0].v.a > 0:
            raise NotSupported("sqrt of interval not > 0")
        s = iv.sqrt(a[0].v)
        return a[0].chain(s, 1 / (2 * s))
    if op == "sin":
        return a[0].chain(iv.sin(a[0].v), iv.cos(a[0].v))
    if op == "cos":
        return a[0].chain(iv.cos(a[0].v), -iv.sin(a[0].v))
    if op == "abs":
        v = a[0].v
        if v.a >= 0:
            return a[0]
        if v.b <= 0:
            return -a[0]
        return a[0].chain(iv.mpf([0, max(-v.a, v.b)]), iv.mpf([-1, 1]))
    raise NotSupported(op)


def row_ad(row, x):
    s = AD(ivn(row["constant"]))
    for j, c in row["lin"].items():
        s = s + x[j] * ivn(c)
    for i, j, c in row["quad"]:
        s = s + x[i] * x[j] * ivn(c)
    if row["nl"] is not None:
        s = s + ev(row["nl"], x)
    return s


def obj_ad(o, x):
    return row_ad(dict(constant=o["constant"], lin=o["lin"], quad=o["quad"], nl=o["nl"]), x)


# ------------------------------------------------------------------ exact rational rows
class NotPolynomial(Exception):
    pass


def ev_frac(t, x):
    op = t[0]
    if op == "num":
        return Fraction(t[1])
    if op == "var":
        return x[t[1]] * Fraction(t[2])
    if op == "power":
        if t[2][0] != "num" or Fraction(t[2][1]).denominator != 1:
            raise NotPolynomial("power")
        return ev_frac(t[1], x) ** int(Fraction(t[2][1]))
    a = [ev_frac(c, x) for c in t[1:]]
    if op in ("sum", "plus"):
        return sum(a, Fraction(0))
    if op in ("product", "times"):
        s = Fraction(1)
        for b in a:
            s *= b
        return s
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "square":
        return a[0] * a[0]
    if op == "abs":
        return abs(a[0])
    raise NotPolynomial(op)


def row_frac(row, x):
    s = Fraction(row["constant"])
    for j, c in row["lin"].items():
        s += Fraction(c) * x[j]
    for i, j, c in row["quad"]:
        s += Fraction(c) * x[i] * x[j]
    if row["nl"] is not None:
        s += ev_frac(row["nl"], x)
    return s


def row_ok_frac(row, v):
    lo = None if osilx.isinf(row["lb"]) else Fraction(row["lb"])
    hi = None if osilx.isinf(row["ub"]) else Fraction(row["ub"])
    return (lo is None or v >= lo) and (hi is None or v <= hi)


def row_ok_iv(row, I):
    """True if the enclosure I lies inside [lb, ub] (strict inequality not needed)."""
    if not osilx.isinf(row["lb"]):
        if not (I.a >= ivn(row["lb"]).b):
            return False
    if not osilx.isinf(row["ub"]):
        if not (I.b <= ivn(row["ub"]).a):
            return False
    return True


# ------------------------------------------------------------------ helpers
def vars_of_tree(t, out):
    if t[0] == "var":
        out.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            vars_of_tree(c, out)


def row_vars(row):
    s = set(row["lin"])
    for a, b, _ in row["quad"]:
        s |= {a, b}
    if row["nl"] is not None:
        vars_of_tree(row["nl"], s)
    return s


def to_float_enclosure(I):
    with mpmath.workprec(300):
        a, b = mpmath.mpf(I.a), mpmath.mpf(I.b)
        c = float((a + b) / 2)
        rad = max(b - mpmath.mpf(c), mpmath.mpf(c) - a)
    return c, float(np.nextafter(float(rad), np.inf)) if rad > 0 else 0.0


def exact_iv(v):
    """exact value (Fraction or decimal string) -> enclosing interval"""
    if isinstance(v, str):
        return ivn(v)
    if v.denominator == 1:
        return iv.mpf(v.numerator)
    return iv.mpf(v.numerator) / iv.mpf(v.denominator)


def sol_fraction(s):
    return Fraction(s)


def is_polynomial(row):
    if row["nl"] is None:
        return True
    try:
        ev_frac(row["nl"], _ZeroX())
        return True
    except NotPolynomial:
        return False
    except ZeroDivisionError:
        return True


class _ZeroX:
    def __getitem__(self, k):
        return Fraction(1)


# ------------------------------------------------------------------ exact polynomials in the basic variables
class TooBig(Exception):
    pass


def _padd(p, q, sgn=1):
    out = dict(p)
    for k, c in q.items():
        v = out.get(k, 0) + sgn * c
        if v:
            out[k] = v
        else:
            out.pop(k, None)
    return out


def _pmul(p, q):
    out = {}
    for k1, c1 in p.items():
        for k2, c2 in q.items():
            k = tuple(sorted(k1 + k2))
            v = out.get(k, 0) + c1 * c2
            if v:
                out[k] = v
            else:
                out.pop(k, None)
    if len(out) > 20000:
        raise TooBig()
    return out


def ev_poly(t, xs):
    """exact polynomial (dict monomial -> Fraction) in the basic variables; xs[j] is a Fraction
    (fixed) or ("b", k) (basic variable k)."""
    op = t[0]
    if op == "num":
        c = Fraction(t[1])
        return {(): c} if c else {}
    if op == "var":
        v, c = xs[t[1]], Fraction(t[2])
        if isinstance(v, tuple):
            return {(v[1],): c}
        return {(): v * c} if v * c else {}
    if op == "power":
        if t[2][0] != "num" or Fraction(t[2][1]).denominator != 1 or Fraction(t[2][1]) < 0:
            raise NotPolynomial("power")
        base, out = ev_poly(t[1], xs), {(): Fraction(1)}
        for _ in range(int(Fraction(t[2][1]))):
            out = _pmul(out, base)
        return out
    a = [ev_poly(c, xs) for c in t[1:]]
    if op in ("sum", "plus"):
        out = {}
        for b in a:
            out = _padd(out, b)
        return out
    if op in ("product", "times"):
        out = {(): Fraction(1)}
        for b in a:
            out = _pmul(out, b)
        return out
    if op == "minus":
        return _padd(a[0], a[1], -1)
    if op == "negate":
        return {k: -c for k, c in a[0].items()}
    if op == "square":
        return _pmul(a[0], a[0])
    if op == "divide":
        if set(a[1]) - {()} or not a[1]:
            raise NotPolynomial("division by a nonconstant")
        d = a[1][()]
        return {k: c / d for k, c in a[0].items()}
    raise NotPolynomial(op)


def row_poly(row, xs):
    p = {(): Fraction(row["constant"])} if Fraction(row["constant"]) else {}
    for j, c in row["lin"].items():
        p = _padd(p, ev_poly(("var", j, c), xs))
    for i, j, c in row["quad"]:
        p = _padd(p, _pmul(ev_poly(("var", i, c), xs), ev_poly(("var", j, "1"), xs)))
    if row["nl"] is not None:
        p = _padd(p, ev_poly(row["nl"], xs))
    return p


def poly_on_box(p, X):
    s = iv.mpf(0)
    for k, c in p.items():
        t = exact_iv(c)
        i = 0
        while i < len(k):
            e = 1
            while i + e < len(k) and k[i + e] == k[i]:
                e += 1
            t = t * X[k[i]] ** e
            i += e
        s = s + t
    return s


def _exact(x):
    """exact rational value of an mpf / interval endpoint (copied at 400 bits)"""
    with mpmath.workprec(400):
        sign, man, exp, _ = mpmath.mpf(x)._mpf_
    v = Fraction(man) * Fraction(2) ** exp
    return -v if sign else v


def outward_decimals(I, digits=30):
    """(lo, hi) decimal strings with lo <= I.a and hi >= I.b (exact endpoint copies)"""
    out = []
    for v, up in ((_exact(I.a), False), (_exact(I.b), True)):
        k = digits + max(0, -len(str(abs(v.numerator) // v.denominator)) + 1) + 20  # decimals kept
        q = v * 10 ** k
        n = -((-q.numerator) // q.denominator) if up else q.numerator // q.denominator
        sgn = "-" if n < 0 else ""
        t = str(abs(n)).rjust(k + 1, "0")
        out.append(f"{sgn}{t[:-k]}.{t[-k:]}".rstrip("0").rstrip("."))
    return tuple(out)


# ------------------------------------------------------------------ route A
def exact_check(m, vals):
    """Route A. Returns dict(ok, reason, obj_enclosure)."""
    names = m["names"]
    xF = [Fraction(vals.get(n, "0")) for n in names]
    for j in range(len(names)):
        lb, ub = m["lb"][j], m["ub"][j]
        if not osilx.isinf(lb) and xF[j] < Fraction(lb):
            return dict(ok=False, reason="bound %s" % names[j])
        if not osilx.isinf(ub) and xF[j] > Fraction(ub):
            return dict(ok=False, reason="bound %s" % names[j])
        if m["vt"][j] in ("B", "I") and xF[j].denominator != 1:
            return dict(ok=False, reason="integrality %s" % names[j])
    xI = None
    for row in m["cons"]:
        if is_polynomial(row):
            try:
                v = row_frac(row, xF)
            except ZeroDivisionError:
                return dict(ok=False, reason="division by zero in %s" % row["name"])
            if not row_ok_frac(row, v):
                return dict(ok=False, reason="row %s (exact value off by %.3g)" % (
                    row["name"], float(v - Fraction(row["lb"] if not osilx.isinf(row["lb"]) else row["ub"]))))
        else:
            if row["lb"] == row["ub"]:
                return dict(ok=False, reason="nonpolynomial equality %s" % row["name"])
            if xI is None:
                xI = [AD(exact_iv(vals.get(n, "0"))) for n in names]
            try:
                I = row_ad(row, xI).v
            except (NotSupported, ZeroDivisionError) as e:
                return dict(ok=False, reason="row %s: %s" % (row["name"], e))
            if not row_ok_iv(row, I):
                return dict(ok=False, reason="row %s (interval)" % row["name"])
    if xI is None:
        xI = [AD(exact_iv(vals.get(n, "0"))) for n in names]
    fo = obj_ad(m["obj"], xI).v
    lo, hi = outward_decimals(fo)
    return dict(ok=True, reason="exactly feasible as listed", obj_lo=lo, obj_hi=hi)


# ------------------------------------------------------------------ route B
def build_x(nvar, fixed, B, XB, with_ad):
    x = [None] * nvar
    for j, v in fixed.items():
        x[j] = AD(exact_iv(v))
    for k, j in enumerate(B):
        x[j] = AD(XB[k], {k: iv.mpf(1)}) if with_ad else AD(XB[k])
    return x


def target(row, side):
    return ivn(row["lb"] if side == "lb" else row["ub"])


def resid_jac(m, rows, sides, B, xB, fixed, XB=None, want_jac=True):
    """F(x) enclosure at the double point xB (or over box XB), Jacobian enclosure."""
    n = len(B)
    if XB is None:
        XB = [iv.mpf(float(v)) for v in xB]
    x = build_x(len(m["names"]), fixed, B, XB, want_jac)
    Fc, Fr = np.zeros(len(rows)), np.zeros(len(rows))
    ri, ci, jc, jr = [], [], [], []
    for i, r in enumerate(rows):
        row = m["cons"][r]
        s = row_ad(row, x)
        Fc[i], Fr[i] = to_float_enclosure(s.v - target(row, sides[i]))
        if want_jac:
            for k, I in s.d.items():
                c, rr = to_float_enclosure(I)
                ri.append(i); ci.append(k); jc.append(c); jr.append(rr)
    Jc = sp.csr_matrix((jc, (ri, ci)), shape=(len(rows), n)) if want_jac else None
    Jr = sp.csr_matrix((jr, (ri, ci)), shape=(len(rows), n)) if want_jac else None
    return Fc, Fr, Jc, Jr


def krawczyk(m, rows, sides, B, xt, r, fixed):
    n = len(B)
    lo = np.nextafter(xt - r, -np.inf)
    hi = np.nextafter(xt + r, np.inf)
    X = [iv.mpf([float(lo[k]), float(hi[k])]) for k in range(n)]
    r_in, r_out = np.zeros(n), np.zeros(n)
    with mpmath.workprec(200):
        for k in range(n):
            dl = mpmath.mpf(float(xt[k])) - mpmath.mpf(float(lo[k]))
            dh = mpmath.mpf(float(hi[k])) - mpmath.mpf(float(xt[k]))
            r_in[k] = np.nextafter(float(min(dl, dh)), -np.inf)
            r_out[k] = np.nextafter(float(max(dl, dh)), np.inf)
    Fc, Fr, Jp, _ = resid_jac(m, rows, sides, B, xt, fixed)
    _, _, Jc, Jr = resid_jac(m, rows, sides, B, xt, fixed, XB=X)
    Jc, Jr, Jp = Jc.toarray(), Jr.toarray(), Jp.toarray()
    R = np.linalg.inv(Jp)
    gam = n * U_ROUND / (1 - n * U_ROUND)
    aR = np.abs(R)
    a1 = np.abs(R @ Fc) + gam * (aR @ np.abs(Fc))
    a2 = aR @ Fr
    E = np.eye(n) - R @ Jc
    a3 = np.abs(E) @ r_out + gam * (aR @ (np.abs(Jc) @ r_out))
    a4 = aR @ (Jr @ r_out)
    beta = SAFE * SAFE * (a1 + a2 + a3 + a4) + TINY
    return dict(ok=bool(np.all(beta < r_in)), worst_ratio=float((beta / r_in).max()),
                max_resid=float(np.abs(Fc).max())), X


def newton(m, rows, sides, B, x0, fixed, iters=8):
    x = np.array(x0, float)
    hist = []
    for _ in range(iters):
        Fc, _, Jc, _ = resid_jac(m, rows, sides, B, x, fixed)
        hist.append(float(np.abs(Fc).max()))
        if hist[-1] < 1e-15 * max(1.0, float(np.abs(x).max())) and len(hist) > 1:
            break
        dx = spla.spsolve(Jc.tocsc(), Fc)
        x = x - dx
        if not np.all(np.isfinite(x)):
            break
    Fc, _, _, _ = resid_jac(m, rows, sides, B, x, fixed, want_jac=False)
    hist.append(float(np.abs(Fc).max()))
    return x, hist


def dist_to_bounds(m, j, v):
    d = math.inf
    if not osilx.isinf(m["lb"][j]):
        d = min(d, v - float(m["lb"][j]))
    if not osilx.isinf(m["ub"][j]):
        d = min(d, float(m["ub"][j]) - v)
    return d


def verify_point(m, vals, log=print, **kw):
    """Route B with retries: basic variables that end up on a bound are fixed at that bound
    (up to 3 rounds); then the snap-first variant. Returns the first proved result, else the
    last failure."""
    snap = set()
    tried = []
    for it in range(4):
        r = polish_and_verify(m, vals, snap_fix=tuple(snap), log=log, **kw)
        r["attempt"] = "snap-nonbasic, round %d" % it
        tried.append(r)
        if r.get("status") == "proved":
            r["attempt"] = "snap-nonbasic, round %d" % it
            return r
        new = set(r.get("basic_at_bound", [])) - snap
        if not new:
            break
        snap |= new
    r = polish_and_verify(m, vals, snap_first=True, log=log, **kw)
    r["attempt"] = "snap-first"
    if r.get("status") == "proved":
        return r
    tried.append(r)
    kc = {k: v for k, v in kw.items() if k in ("extra_fix", "rhos", "max_n")}
    r = verify_point_shift(m, vals, log=log, **kc)
    r["attempt"] = "shift (route C)"
    if r.get("status") == "proved":
        return r
    tried.append(r)
    reasons = ["%s: %s" % (t.get("attempt", "snap-nonbasic"), t.get("reason", "")[:120]) for t in tried]
    # report the most informative failure (one that reached the Krawczyk stage, if any)
    for t in tried:
        if "obj_hi" in t or "polished_obj" in t:
            t["all_attempts"] = reasons
            return t
    tried[0]["all_attempts"] = reasons
    return tried[0]


def polish_and_verify(m, vals, tb=1e-7, ta=1e-7, rhos=(1e-12, 1e-10, 1e-8), max_n=4000,
                      extra_fix=(), snap_fix=(), snap_first=False, log=print):
    """Route B. Returns a result dict (see keys below)."""
    names = m["names"]
    nv = len(names)
    x0 = [float(Fraction(vals.get(n, "0"))) for n in names]
    fixed, why = {}, {}
    for j in range(nv):
        if m["vt"][j] in ("B", "I"):
            fixed[j] = Fraction(round(Fraction(vals.get(names[j], "0"))))
            why[j] = "int"
        elif m["lb"][j] == m["ub"][j]:
            fixed[j] = m["lb"][j]
            why[j] = "fixed"
        elif names[j] in extra_fix:
            fixed[j] = vals.get(names[j], "0")
            why[j] = "held"

    def snap(j):
        """exact value for a non-basic continuous variable: its bound if within tb, else its decimal"""
        lb, ub = m["lb"][j], m["ub"][j]
        sc = tb * max(1.0, abs(x0[j]))
        if not osilx.isinf(lb) and x0[j] - float(lb) <= sc:
            why[j] = "at lb"
            return lb
        if not osilx.isinf(ub) and float(ub) - x0[j] <= sc:
            why[j] = "at ub"
            return ub
        return vals.get(names[j], "0")

    for j in range(nv):
        if names[j] in snap_fix and j not in fixed:
            fixed[j] = snap(j)
    if snap_first:
        for j in range(nv):
            if j not in fixed:
                v = snap(j)
                if why.get(j, "").startswith("at"):
                    fixed[j] = v
    # row activity at x0 (30 digits; only used to classify rows)
    with mpmath.workdps(30):
        xm = [mpmath.mpf(vals.get(n, "0")) for n in names]
        act, sides = [], []
        for r, row in enumerate(m["cons"]):
            try:
                v = float(osilx.ev_row(row, xm, A.num, A.FNS))
            except (A.DomainError, ZeroDivisionError):
                return dict(status="fail", reason="domain error at x0 in %s" % row["name"])
            sc = ta * max(1.0, abs(v))
            if row["lb"] == row["ub"]:
                act.append(r); sides.append("lb")
            elif not osilx.isinf(row["lb"]) and v - float(row["lb"]) <= sc:
                act.append(r); sides.append("lb")
            elif not osilx.isinf(row["ub"]) and float(row["ub"]) - v <= sc:
                act.append(r); sides.append("ub")
    rv = [row_vars(m["cons"][r]) for r in range(len(m["cons"]))]
    E1, S1, E0 = [], [], []
    for r, s in zip(act, sides):
        if rv[r] - set(fixed):
            E1.append(r); S1.append(s)
        else:
            E0.append(r)
    # E0 rows involve only fixed variables: they must hold exactly
    xF = {j: (Fraction(v) if isinstance(v, str) else v) for j, v in fixed.items()}
    for r in E0:
        row = m["cons"][r]
        if is_polynomial(row):
            full = [xF.get(j, Fraction(0)) for j in range(nv)]
            if not row_ok_frac(row, row_frac(row, full)):
                return dict(status="fail", reason="row %s over fixed/integer variables fails exactly" % row["name"])
        else:
            xE = [AD(exact_iv(fixed[j])) if j in fixed else None for j in range(nv)]
            try:
                I = row_ad(row, xE).v
            except (NotSupported, ZeroDivisionError) as e:
                return dict(status="fail", reason="row %s over fixed variables: %s" % (row["name"], e))
            if not row_ok_iv(row, I):
                return dict(status="fail", reason="nonpolynomial active row %s over fixed variables not verified" % row["name"])
    cand = sorted(set().union(*[rv[r] for r in E1]) - set(fixed)) if E1 else []
    log(f"  fixed {len(fixed)} (int {sum(1 for w in why.values() if w == 'int')}), "
        f"active rows {len(E1)}, candidates {len(cand)}")
    if len(E1) > max_n:
        return dict(status="fail", reason=f"too large for dense Krawczyk ({len(E1)})")
    if E1 and cand:
        # rows whose gradient w.r.t. all candidates vanishes at x0 cannot be solved for;
        # they are removed from the system and must be verified on X like inactive rows
        fx = dict(fixed)
        for j in range(nv):
            if j not in fx and j not in set(cand):
                fx[j] = vals.get(names[j], "0")
        _, _, J0, _ = resid_jac(m, E1, S1, cand, np.array([x0[j] for j in cand]), fx)
        nzr = np.abs(J0).max(axis=1).toarray().ravel() if J0.nnz else np.zeros(len(E1))
        keep = [i for i in range(len(E1)) if nzr[i] > 0]
        if len(keep) < len(E1):
            log(f"  {len(E1) - len(keep)} active rows with zero gradient moved to the X-check")
            E1 = [E1[i] for i in keep]
            S1 = [S1[i] for i in keep]
            cand = sorted(set().union(*[rv[r] for r in E1]) - set(fixed)) if E1 else []
    if len(E1) > len(cand):
        return dict(status="fail", reason=f"overdetermined: {len(E1)} active rows, {len(cand)} candidates")
    if len(E1) > max_n:
        return dict(status="fail", reason=f"too large for dense Krawczyk ({len(E1)})")
    for j in range(nv):
        if j not in fixed and j not in set(cand):
            fixed[j] = snap(j)
    B = []
    if E1:
        # Jacobian of active rows w.r.t. candidates at x0 (double); near-bound columns get small weight
        fx = dict(fixed)
        Fc, _, J, _ = resid_jac(m, E1, S1, cand, np.array([x0[j] for j in cand]), fx)
        J = J.toarray()
        w = np.array([min(1.0, max(dist_to_bounds(m, j, x0[j]), 0.0) / (1e-3 * max(1.0, abs(x0[j]))))
                      for j in cand])
        Q, Rq, piv = scipy.linalg.qr(J * np.maximum(w, 1e-3), pivoting=True, mode="economic")
        d = np.abs(np.diag(Rq))
        rank = int(np.sum(d > 1e-12 * d.max())) if d.size else 0
        if rank < len(E1):
            return dict(status="fail", reason=f"active Jacobian rank {rank} < {len(E1)} rows")
        B = [cand[k] for k in piv[:len(E1)]]
        Bs = set(B)
        for j in cand:
            if j not in Bs:
                fixed[j] = snap(j)
    log(f"  square system n={len(B)}")
    res = dict(n=len(B), n_fixed_int=sum(1 for w in why.values() if w == "int"),
               n_at_bound=sum(1 for w in why.values() if w.startswith("at")), n_active_ineq=sum(
                   1 for r in E1 if m["cons"][r]["lb"] != m["cons"][r]["ub"]))
    ok, xt, X = solve_and_box(m, E1, S1, B, np.array([x0[j] for j in B]), fixed, rhos, res)
    if not ok:
        return res
    check_on_box(m, fixed, B, X, set(E1) | set(E0), res)
    res["xt"] = [repr(float(v)) for v in xt]
    return res


def solve_and_box(m, rows, sides, B, xstart, fixed, rhos, res):
    """Newton on the square system, then Krawczyk with growing radius. Fills res."""
    nv = len(m["names"])
    xt = np.array(xstart, float)
    X = []
    if not B:
        return True, xt, X
    xt, hist = newton(m, rows, sides, B, xt, fixed)
    res["newton"] = [float("%.3g" % h) for h in hist]
    if not np.all(np.isfinite(xt)) or hist[-1] > 1e-8 * max(1.0, float(np.abs(xt).max())):
        res.update(status="fail", reason="Newton did not converge")
        return False, xt, X
    res["max_move"] = float(np.max(np.abs(xt - np.array(xstart, float))))
    for rho in rhos:
        r = rho * np.maximum(1.0, np.abs(xt))
        kt, X = krawczyk(m, rows, sides, B, xt, r, fixed)
        res["krawczyk"] = dict(rho=rho, **kt)
        if kt["ok"]:
            return True, xt, X
    xI = build_x(nv, fixed, B, [iv.mpf(float(v)) for v in xt], False)
    fo = obj_ad(m["obj"], xI).v
    res.update(status="fail", reason="Krawczyk test failed", polished_obj=float(mpmath.mpf(fo.a)))
    return False, xt, X


def check_on_box(m, fixed, B, X, skip, res):
    """Bounds of the basic variables on X, every row not in `skip` over X (exact polynomial
    arithmetic where possible, else intervals), objective enclosure. Fills res."""
    names = m["names"]
    nv = len(names)
    bad = []
    for k, j in enumerate(B):
        lb, ub = m["lb"][j], m["ub"][j]
        if (not osilx.isinf(lb) and not X[k].a >= ivn(lb).b) or (not osilx.isinf(ub) and not X[k].b <= ivn(ub).a):
            bad.append("bound " + names[j])
            res.setdefault("basic_at_bound", []).append(names[j])
    xI = build_x(nv, fixed, B, X, False)
    Bpos = {j: k for k, j in enumerate(B)}
    xs = [("b", Bpos[j]) if j in Bpos else (Fraction(fixed[j]) if isinstance(fixed[j], str) else fixed[j])
          for j in range(nv)]
    # every non-basic variable: bounds and integrality, exactly
    for j in range(nv):
        if j in Bpos:
            continue
        v = xs[j]
        lb, ub = m["lb"][j], m["ub"][j]
        if (not osilx.isinf(lb) and v < Fraction(lb)) or (not osilx.isinf(ub) and v > Fraction(ub)):
            bad.append("bound " + names[j])
        if m["vt"][j] in ("B", "I") and v.denominator != 1:
            bad.append("integrality " + names[j])
    for r, row in enumerate(m["cons"]):
        if r in skip:
            continue
        if is_polynomial(row):
            try:
                p = row_poly(row, xs)
            except (NotPolynomial, TooBig, ZeroDivisionError):
                p = None
            if p is not None:
                if not (set(p) - {()}):  # constant: decide exactly
                    if not row_ok_frac(row, p.get((), Fraction(0))):
                        bad.append("row " + row["name"])
                    continue
                if row["lb"] == row["ub"]:
                    pz = _padd(p, {(): Fraction(row["lb"])}, -1)
                    if not pz:
                        continue
                if row_ok_iv(row, poly_on_box(p, X)):
                    continue
                bad.append("row " + row["name"])
                continue
        try:
            I = row_ad(row, xI).v
        except (NotSupported, ZeroDivisionError) as e:
            bad.append("row %s (%s)" % (row["name"], e))
            continue
        if not row_ok_iv(row, I):
            bad.append("row " + row["name"])
    fo = obj_ad(m["obj"], xI).v
    lo, hi = outward_decimals(fo)
    res.update(obj_lo=lo, obj_hi=hi, bad=bad[:10], n_bad=len(bad))
    res["status"] = "proved" if not bad else "fail"
    if bad:
        res["reason"] = "rows/bounds not verified on X: " + ", ".join(bad[:5])
    res["B"] = [names[j] for j in B]
    cen = []
    for j in range(nv):
        if j in Bpos:
            with mpmath.workprec(300):
                cen.append(mpmath.nstr((mpmath.mpf(X[Bpos[j]].a) + mpmath.mpf(X[Bpos[j]].b)) / 2, 25))
        else:
            v = xs[j]
            with mpmath.workdps(60):
                cen.append(str(v.numerator) if v.denominator == 1 else mpmath.nstr(mpmath.mpf(v.numerator) / v.denominator, 45))
    res["_center"] = cen


# ------------------------------------------------------------------ route C (shift into the interior)
class _Subst:
    """variable lookup for ev_poly: fixed values as Fractions, the listed free ones as symbols"""

    def __init__(self, fixed, free):
        self.fixed, self.free = fixed, free

    def __getitem__(self, k):
        if k in self.free:
            return ("b", k)
        v = self.fixed[k]
        return Fraction(v) if isinstance(v, str) else v


def implied_fix(m, fixed, x0, rv, log):
    """Fix continuous variables that a row linear in its only free variable determines exactly
    (after substituting the fixed values); repeat until nothing changes. Returns #fixed."""
    names, cons = m["names"], m["cons"]
    n = 0
    for _ in range(20):
        changed = False
        for r, row in enumerate(cons):
            free = [j for j in rv[r] if j not in fixed]
            if not free or len(free) > 40 or not is_polynomial(row):
                continue
            try:
                p = row_poly(row, _Subst(fixed, set(free)))
            except (NotPolynomial, TooBig, ZeroDivisionError, KeyError):
                continue
            pv = {a for k in p for a in k}
            if len(pv) != 1 or any(len(k) > 1 for k in p):
                continue
            j = next(iter(pv))
            a, c = p.get((j,), Fraction(0)), p.get((), Fraction(0))
            if a == 0:
                continue
            lo = None if osilx.isinf(m["lb"][j]) else Fraction(m["lb"][j])
            hi = None if osilx.isinf(m["ub"][j]) else Fraction(m["ub"][j])
            rl = None if osilx.isinf(row["lb"]) else (Fraction(row["lb"]) - c) / a
            ru = None if osilx.isinf(row["ub"]) else (Fraction(row["ub"]) - c) / a
            if a < 0:
                rl, ru = ru, rl
            if rl is not None and (lo is None or rl > lo):
                lo = rl
            if ru is not None and (hi is None or ru < hi):
                hi = ru
            if lo is not None and hi is not None and lo >= hi:
                v = lo if lo == hi else (lo + hi) / 2
                if lo > hi and lo - hi > Fraction(1, 10 ** 9) * max(1, abs(lo)):
                    continue  # inconsistent: leave it to the general machinery
                if abs(float(v) - x0[j]) <= 1e-5 * max(1.0, abs(x0[j])) and lo == hi:
                    fixed[j] = v
                    n += 1
                    changed = True
        if not changed:
            break
    return n


def exact_decimal(f):
    """exact decimal string of a double"""
    fr = Fraction(float(f))
    return str(fr.numerator) if fr.denominator == 1 else repr(float(f)) if Fraction(repr(float(f))) == fr else None


def verify_point_shift(m, vals, ta=1e-6, tb=1e-6, ts=None, rhos=(1e-12, 1e-10, 1e-8), max_n=4000,
                       extra_fix=(), log=print):
    """Route C: fix integers, fix variables determined by singleton rows, then find a direction
    (LP) that keeps the linearized equalities and strictly improves as many active inequalities
    and active bounds as possible, preferring small objective change. The ones that cannot be
    improved are implicit equalities (kept in the square system / fixed at the bound). Step
    t along the direction, then Newton + Krawczyk on the square system, then all other rows and
    bounds on the box X. t is increased until the check succeeds."""
    from scipy.optimize import linprog
    names = m["names"]
    nv = len(names)
    x0 = [float(Fraction(vals.get(n, "0"))) for n in names]
    sense = 1 if m["obj"]["sense"] == "min" else -1
    fixed = {}
    for j in range(nv):
        if m["vt"][j] in ("B", "I"):
            fixed[j] = Fraction(round(Fraction(vals.get(names[j], "0"))))
        elif m["lb"][j] == m["ub"][j]:
            fixed[j] = m["lb"][j]
        elif names[j] in extra_fix:
            fixed[j] = vals.get(names[j], "0")
    rv = [row_vars(m["cons"][r]) for r in range(len(m["cons"]))]
    nimp = implied_fix(m, fixed, x0, rv, log)
    for j, v in fixed.items():
        x0[j] = float(Fraction(v) if isinstance(v, str) else v)
    # activity at x0 (with the fixed values substituted)
    with mpmath.workdps(30):
        xm = [mpmath.mpf(Fraction(fixed[j]).numerator) / Fraction(fixed[j]).denominator if j in fixed
              else mpmath.mpf(vals.get(names[j], "0")) for j in range(nv)]
        E, E0, I, Isig, viol = [], [], [], [], 0.0
        for r, row in enumerate(m["cons"]):
            free = rv[r] - fixed.keys()
            try:
                v = float(osilx.ev_row(row, xm, A.num, A.FNS))
            except (A.DomainError, ZeroDivisionError):
                return dict(status="fail", reason="domain error at x0 in %s" % row["name"])
            if row["lb"] == row["ub"]:
                if free and len(free) <= 40 and is_polynomial(row):
                    try:
                        p = row_poly(row, _Subst(fixed, set(free)))
                        if not (set(p) - {()}):
                            free = set()  # identically constant: decided exactly (E0)
                    except (NotPolynomial, TooBig, ZeroDivisionError):
                        pass
                (E if free else E0).append(r)
                continue
            if not free:
                continue  # checked exactly in check_on_box
            lb = None if osilx.isinf(row["lb"]) else float(row["lb"])
            ub = None if osilx.isinf(row["ub"]) else float(row["ub"])
            if lb is not None and v - lb <= ta * max(1.0, abs(lb)):
                I.append(r); Isig.append(+1); viol = max(viol, (lb - v) / max(1.0, abs(lb)))
            elif ub is not None and ub - v <= ta * max(1.0, abs(ub)):
                I.append(r); Isig.append(-1); viol = max(viol, (v - ub) / max(1.0, abs(ub)))
    # E0 rows (equalities over fixed variables only) must hold exactly
    for r in E0:
        row = m["cons"][r]
        ok = False
        if is_polynomial(row):
            try:
                p = row_poly(row, _Subst(fixed, set(rv[r] - fixed.keys())))
                ok = not (set(p) - {()}) and row_ok_frac(row, p.get((), Fraction(0)))
            except (NotPolynomial, TooBig, ZeroDivisionError):
                ok = False
        if not ok:
            return dict(status="fail", reason="equality %s over fixed variables fails exactly" % row["name"])
    C = sorted(set().union(*[rv[r] for r in E + I]) - fixed.keys()) if (E or I) else []
    Cpos = {j: k for k, j in enumerate(C)}
    Bd, Bsig = [], []
    for j in C:
        sc = tb * max(1.0, abs(x0[j]))
        if not osilx.isinf(m["lb"][j]) and x0[j] - float(m["lb"][j]) <= sc:
            Bd.append(j); Bsig.append(+1); viol = max(viol, (float(m["lb"][j]) - x0[j]) / max(1.0, abs(x0[j])))
        elif not osilx.isinf(m["ub"][j]) and float(m["ub"][j]) - x0[j] <= sc:
            Bd.append(j); Bsig.append(-1); viol = max(viol, (x0[j] - float(m["ub"][j])) / max(1.0, abs(x0[j])))
    # variables outside C: keep their decimal, or the bound if they violate it
    for j in range(nv):
        if j in fixed or j in Cpos:
            continue
        v = vals.get(names[j], "0")
        if not osilx.isinf(m["lb"][j]) and Fraction(v) < Fraction(m["lb"][j]):
            v = m["lb"][j]
        if not osilx.isinf(m["ub"][j]) and Fraction(v) > Fraction(m["ub"][j]):
            v = m["ub"][j]
        fixed[j] = v
    log(f"  route C: fixed {len(fixed)} (implied {nimp}), equalities {len(E)}, active ineq {len(I)}, "
        f"active bounds {len(Bd)}, candidates {len(C)}, scaled violation {viol:.2g}")
    res = dict(route_c=True, n_implied_fixed=nimp, n_eq=len(E), n_active_ineq=len(I), n_active_bounds=len(Bd),
               n_cand=len(C))
    if not C:
        check_on_box(m, fixed, [], [], set(E0), res)
        return res
    if len(E) > max_n:
        res.update(status="fail", reason=f"too large ({len(E)} equalities)")
        return res
    xC = np.array([x0[j] for j in C])
    fx = dict(fixed)
    _, _, JE, _ = resid_jac(m, E, ["lb"] * len(E), C, xC, fx) if E else (None, None, sp.csr_matrix((0, len(C))), None)
    _, _, JI, _ = resid_jac(m, I, ["lb"] * len(I), C, xC, fx) if I else (None, None, sp.csr_matrix((0, len(C))), None)
    # objective gradient (numerical, only for the LP's secondary goal)
    og = build_x(nv, {j: v for j, v in fixed.items()}, C, [iv.mpf(float(v)) for v in xC], True)
    g = np.zeros(len(C))
    for k, I_ in obj_ad(m["obj"], og).d.items():
        g[k] = float(I_.mid)
    cs = np.maximum(1.0, np.abs(xC))
    nI, nB = len(I), len(Bd)
    ns = nI + nB
    n = len(C)
    # LP variables: y (n), s (ns). dx = cs * y.
    rowsI = []
    if nI:
        rs = np.array([max(1.0, abs(float(m["cons"][r]["lb" if sg > 0 else "ub"]))) for r, sg in zip(I, Isig)])
        A1 = -sp.diags(np.array(Isig) / rs) @ JI @ sp.diags(cs)
        rowsI.append(sp.hstack([A1, sp.eye(nI, ns)]))
    if nB:
        A2 = sp.csr_matrix((-np.array(Bsig, float), (range(nB), [Cpos[j] for j in Bd])), shape=(nB, n))
        rowsI.append(sp.hstack([A2, sp.eye(nB, ns, k=nI)]))
    A_ub = sp.vstack(rowsI).tocsr() if rowsI else None
    A_eq = sp.hstack([JE @ sp.diags(cs), sp.csr_matrix((len(E), ns))]).tocsr() if E else None
    gs = g * cs
    gn = np.abs(gs).sum() or 1.0
    c = np.concatenate([1e-3 * sense * gs / gn, -np.ones(ns)])
    lp = linprog(c, A_ub=A_ub, b_ub=np.zeros(ns) if ns else None, A_eq=A_eq,
                 b_eq=np.zeros(len(E)) if E else None,
                 bounds=[(-1, 1)] * n + [(0, 1)] * ns, method="highs")
    if lp.status != 0:
        res.update(status="fail", reason="direction LP failed: " + lp.message[:80])
        return res
    y, sv = lp.x[:n], lp.x[n:]
    impl_rows = [(r, "lb" if sg > 0 else "ub") for r, sg, s_ in zip(I, Isig, sv[:nI]) if s_ < 1e-6]
    impl_vars = [(j, "lb" if sg > 0 else "ub") for j, sg, s_ in zip(Bd, Bsig, sv[nI:]) if s_ < 1e-6]
    theta = float(min([s_ for s_ in sv if s_ >= 1e-6], default=1.0))
    # phase 2: same improvable set with rate >= theta, the others not worsened; minimize objective change
    if ns:
        lo = np.where(sv >= 1e-6, theta, 0.0)
        lp2 = linprog(np.concatenate([sense * gs / gn, np.zeros(ns)]), A_ub=A_ub, b_ub=np.zeros(ns), A_eq=A_eq,
                      b_eq=np.zeros(len(E)) if E else None,
                      bounds=[(-1, 1)] * n + [(l_, l_) for l_ in lo], method="highs")
        if lp2.status == 0:
            y = lp2.x[:n]
    dx = cs * y
    res["obj_rate"] = float(sense * g @ dx)
    res.update(n_implicit_rows=len(impl_rows), n_implicit_bounds=len(impl_vars), lp_min_s=float(sv.min()) if ns else None)
    log(f"  LP: implicit equalities {len(impl_rows)} rows, {len(impl_vars)} bounds")
    # implicit bounds: the variable stays exactly on its bound
    if impl_vars:
        old_pos = dict(Cpos)
        for j, s_ in impl_vars:
            fixed[j] = m[s_][j]
        C = [j for j in C if j not in fixed]
        Cpos = {j: k for k, j in enumerate(C)}
        xC = np.array([x0[j] for j in C])
        dx = np.array([dx[old_pos[j]] for j in C])
        impl_vars = []
    rows = E + [r for r, _ in impl_rows]
    sides = ["lb"] * len(E) + [s_ for _, s_ in impl_rows]
    # rows without free variables now are decided exactly in check_on_box (equalities must hold)
    keep = [i for i, r in enumerate(rows) if rv[r] - fixed.keys()]
    if len(keep) < len(rows):
        res["n_rows_all_fixed"] = len(rows) - len(keep)
        rows = [rows[i] for i in keep]
        sides = [sides[i] for i in keep]
    if rows:
        # rows with a vanishing gradient at x0 cannot be solved for: check them on X instead.
        # Implicit inequality rows of this kind (e.g. sum of squares <= 0) keep their free
        # variables at the listed decimals, so that the X-check can be exact.
        _, _, J0, _ = resid_jac(m, rows, sides, C, xC, dict(fixed))
        nz = np.abs(J0).max(axis=1).toarray().ravel() if J0.nnz else np.zeros(len(rows))
        keep = [i for i in range(len(rows)) if nz[i] > 0]
        if len(keep) < len(rows):
            log(f"  {len(rows) - len(keep)} system rows with zero gradient moved to the X-check")
            res["n_zero_grad_rows"] = len(rows) - len(keep)
            hold = set()
            for i in range(len(rows)):
                if nz[i] == 0 and m["cons"][rows[i]]["lb"] != m["cons"][rows[i]]["ub"]:
                    hold |= rv[rows[i]] - fixed.keys()
            for j in hold:
                fixed[j] = vals.get(names[j], "0")
            res["n_held_zero_grad"] = len(hold)
            rows = [rows[i] for i in keep]
            sides = [sides[i] for i in keep]
            if hold:
                old_pos = dict(Cpos)
                C = [j for j in C if j not in hold]
                Cpos = {j: k for k, j in enumerate(C)}
                xC = np.array([x0[j] for j in C])
                dx = np.array([dx[old_pos[j]] for j in C])
                impl_vars = [(j, s_) for j, s_ in impl_vars if j not in hold]
    skip = set(rows) | set(E0)
    if ts is None:
        t0 = max(1e-10, 3 * viol) / theta
        ts = [t0 * 10 ** k for k in range(0, 6) if t0 * 10 ** k <= 1e-2] or [t0]
    best = None
    for t in ts:
        fx = dict(fixed)
        for j, s_ in impl_vars:
            fx[j] = m[s_][j]
        cand = [j for j in C if j not in fx]
        x1 = {j: x0[j] + t * dx[Cpos[j]] for j in cand}
        if len(rows) > len(cand):
            res.update(status="fail", reason=f"overdetermined after LP: {len(rows)} rows, {len(cand)} candidates")
            return res
        B = []
        if rows:
            fx2 = dict(fx)
            for j in cand:
                fx2.setdefault(j, None)
            xs_ = np.array([x1[j] for j in cand])
            tmp = {j: v for j, v in fx.items()}
            _, _, J, _ = resid_jac(m, rows, sides, cand, xs_, tmp)
            J = J.toarray()
            w = np.array([min(1.0, max(dist_to_bounds(m, j, x1[j]), 0.0) / (1e-3 * max(1.0, abs(x1[j]))))
                          for j in cand])
            _, Rq, piv = scipy.linalg.qr(J * np.maximum(w, 1e-3), pivoting=True, mode="economic")
            dd = np.abs(np.diag(Rq))
            rank = int(np.sum(dd > 1e-12 * dd.max())) if dd.size else 0
            if rank < len(rows):
                _, R2, piv2 = scipy.linalg.qr(J.T, pivoting=True, mode="economic")
                d2 = np.abs(np.diag(R2))
                rk2 = int(np.sum(d2 > 1e-12 * d2.max()))
                res.update(status="fail", reason=f"system rank {rank} < {len(rows)} rows",
                           dependent_rows=[m["cons"][rows[k]]["name"] for k in piv2[rk2:]][:30])
                return res
            B = [cand[k] for k in piv[:len(rows)]]
        Bs = set(B)
        for j in cand:
            if j not in Bs:
                d = exact_decimal(x1[j])
                fx[j] = d if d is not None else Fraction(float(x1[j]))
        r_ = dict(res, t=t, n=len(B))
        ok, xt, X = solve_and_box(m, rows, sides, B, np.array([x1[j] for j in B]), fx, rhos, r_)
        if ok:
            check_on_box(m, fx, B, X, skip, r_)
            r_["xt"] = [repr(float(v)) for v in xt]
        log(f"  t={t:.1e}: {r_.get('status')} {r_.get('reason', '')[:80]} newton {r_.get('newton')} "
            f"kraw {r_.get('krawczyk', {}).get('worst_ratio')}")
        if r_.get("status") == "proved":
            return r_
        if best is None or "obj_hi" in r_:
            best = r_
    return best if best is not None else dict(res, status="fail", reason="no step size tried")
