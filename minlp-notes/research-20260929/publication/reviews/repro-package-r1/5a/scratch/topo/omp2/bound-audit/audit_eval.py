"""High-precision evaluation of MINLPLib points on the OSIL model.

Parsing: reviews/open-instances-verification/osilx.py (keeps every constant as
its decimal string; records <obj constant> and row `constant` attributes).
Evaluation: mpmath at DPS digits, starting from the exact decimals of the OSIL
file and of the .sol file. Variables missing from a .sol file are 0 (MINLPLib
omits zeros).

evaluate() returns the objective (with its constant), the largest absolute
row violation, variable-bound violation and integrality violation, and the
rows/variables where they occur. This is numerical (high precision, not
interval) evaluation; rigorous checks are in verify.py.
"""
import os
import sys

import mpmath
from mpmath import mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reviews", "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
SOL = os.path.join(HERE, "sol")
DPS = 40


class DomainError(Exception):
    pass


def _real(v):
    if isinstance(v, mpmath.mpc):
        if v.imag != 0:
            raise DomainError("complex value")
        return v.real
    return v


def _power(a, b):
    if a < 0 and b != mpmath.floor(b):
        raise DomainError("negative base, fractional exponent")
    if a == 0 and b < 0:
        raise DomainError("0 ** negative")
    return _real(a ** b)


def _log(a):
    if a <= 0:
        raise DomainError("log of nonpositive")
    return mpmath.log(a)


def _log10(a):
    if a <= 0:
        raise DomainError("log10 of nonpositive")
    return mpmath.log10(a)


def _sqrt(a):
    if a < 0:
        raise DomainError("sqrt of negative")
    return mpmath.sqrt(a)


def _signpower(a, b):
    return mpmath.sign(a) * abs(a) ** b


FNS = {"ln": _log, "log10": _log10, "exp": mpmath.exp, "sqrt": _sqrt, "sin": mpmath.sin,
       "cos": mpmath.cos, "abs": abs, "power": _power, "signpower": _signpower,
       "tanh": mpmath.tanh, "erf": mpmath.erf, "min": min, "max": max, "gammaFn": mpmath.gamma}


def num(s):
    return mpmath.mpf(s)


_cache = {}


def load(name):
    if name not in _cache:
        _cache.clear()
        _cache[name] = osilx.read(os.path.join(OSIL, name + ".osil"))
    return _cache[name]


def read_sol(path):
    out = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and not line.startswith("#"):
            out[p[0]] = p[1]
    return out


def obj_value(m, x):
    o = m["obj"]
    assert o["weight"] in ("1", "1.0"), o["weight"]
    s = num(o["constant"])
    for j, c in o["lin"].items():
        s += num(c) * x[j]
    for i, j, c in o["quad"]:
        s += num(c) * x[i] * x[j]
    if o["nl"] is not None:
        s += osilx.ev_tree(o["nl"], x, num, FNS)
    return s


def row_viol(c, v):
    lo = -mpmath.inf if osilx.isinf(c["lb"]) else num(c["lb"])
    hi = mpmath.inf if osilx.isinf(c["ub"]) else num(c["ub"])
    return max(lo - v, v - hi, mpmath.mpf(0))


def evaluate(m, vals, dps=DPS):
    """vals: dict name -> decimal string (missing names are 0)."""
    with mp.workdps(dps):
        names = m["names"]
        x = [num(vals.get(n, "0")) for n in names]
        unknown = [k for k in vals if k not in set(names)]
        bv, bj = mpmath.mpf(0), None
        iv_, ij = mpmath.mpf(0), None
        for j in range(len(names)):
            lb, ub = m["lb"][j], m["ub"][j]
            v = max(num(lb) - x[j] if not osilx.isinf(lb) else 0, x[j] - num(ub) if not osilx.isinf(ub) else 0, 0)
            if v > bv:
                bv, bj = v, names[j]
            if m["vt"][j] in ("B", "I"):
                d = abs(x[j] - mpmath.nint(x[j]))
                if d > iv_:
                    iv_, ij = d, names[j]
        rv, rj, dom = mpmath.mpf(0), None, []
        for r, c in enumerate(m["cons"]):
            try:
                v = osilx.ev_row(c, x, num, FNS)
                v = _real(v)
                vv = row_viol(c, v)
            except (DomainError, ZeroDivisionError) as e:
                dom.append((c["name"], str(e)))
                continue
            if vv > rv:
                rv, rj = vv, c["name"]
        try:
            f = _real(obj_value(m, x))
        except (DomainError, ZeroDivisionError) as e:
            f = None
            dom.append(("objective", str(e)))
        return dict(obj=f, row_viol=rv, worst_row=rj, bound_viol=bv, worst_var=bj, int_viol=iv_,
                    worst_int=ij, domain_errors=dom, unknown_names=unknown[:5], n_unknown=len(unknown),
                    sense=m["obj"]["sense"])


def evaluate_tag(tag):
    """Evaluate sol/<tag>.sol; objective as a 30-digit string, violations as floats."""
    name = tag.rsplit(".", 1)[0]
    m = load(name)
    vals = read_sol(os.path.join(SOL, tag + ".sol"))
    res = evaluate(m, vals)
    out = {k: (mpmath.nstr(v, 30) if isinstance(v, mpmath.mpf) else v) for k, v in res.items()}
    out["max_viol"] = float(max(res["row_viol"], res["bound_viol"], res["int_viol"]))
    out["objvar_in_sol"] = vals.get("objvar")
    out["nvars"], out["ncons"] = len(m["names"]), len(m["cons"])
    out["n_sos"] = 0
    return out


if __name__ == "__main__":
    import json
    import time
    for tag in sys.argv[1:]:
        t0 = time.time()
        try:
            out = evaluate_tag(tag)
        except Exception as e:  # recorded, not fatal for the audit
            out = dict(error=repr(e)[:300])
        out["sec"] = round(time.time() - t0, 1)
        os.makedirs(os.path.join(HERE, "logs", "eval"), exist_ok=True)
        json.dump(out, open(os.path.join(HERE, "logs", "eval", tag + ".json"), "w"), indent=1)
        print(tag, out.get("obj"), out.get("max_viol"), out.get("error"), out["sec"], flush=True)
