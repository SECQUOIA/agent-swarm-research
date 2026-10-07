"""Independent primal check: evaluate objective and constraint activities of an
OSIL instance at a point, straight from the OSIL data (linear, quadratic and
nonlinear-expression parts), and report the largest bound/constraint violation.

Uses the repository OSIL reader (research-20260922/scouting/minlplib-open-data/osil.py).
Evaluation is in mpmath with 50 digits, so the reported violations are those of
the given point (a float vector), not artifacts of float evaluation.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import math
import sys

import mpmath as mp

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
sys.path.insert(0, _REPO + "/research-20260922/scouting/minlplib-open-data")
import osil  # noqa: E402

OSIL_DIR = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil')
mp.mp.dps = 50


def load(name):
    return osil.read(f"{OSIL_DIR}/{name}.osil")


def _ev(t, x):
    op = t[0]
    if op == "num":
        return mp.mpf(t[1])
    if op == "var":
        return x[t[1]]
    k = [_ev(c, x) for c in t[1:]]
    if op == "sum":
        return mp.fsum(k)
    if op == "negate":
        return -k[0]
    if op == "times":
        r = mp.mpf(1)
        for v in k:
            r *= v
        return r
    if op == "divide":
        return k[0] / k[1]
    if op == "square":
        return k[0] ** 2
    if op == "sqrt":
        return mp.sqrt(k[0])
    if op == "power":
        return k[0] ** k[1]
    if op == "cos":
        return mp.cos(k[0])
    if op == "sin":
        return mp.sin(k[0])
    if op == "exp":
        return mp.exp(k[0])
    if op in ("ln", "log"):
        return mp.log(k[0])
    raise ValueError(f"unsupported op {op}")


def row_value(I, r, x):
    row = I["rows"][r]
    v = mp.fsum(mp.mpf(c) * x[j] for j, c in row["lin"].items())
    v += mp.fsum(mp.mpf(c) * x[i] * x[j] for i, j, c in row["quad"])
    if row["nl"] is not None:
        v += _ev(row["nl"], x)
    return v


def check(name, xvals, I=None):
    """xvals: sequence of floats in OSIL variable order. Returns dict with the
    objective value and max violations (absolute) of bounds and constraints."""
    I = I or load(name)
    x = [mp.mpf(float(v)) for v in xvals]
    n = len(I["vt"])
    assert len(x) == n
    bviol = mp.mpf(0)
    for j in range(n):
        lo, hi = I["lb"][j], I["ub"][j]
        if not math.isinf(lo):
            bviol = max(bviol, lo - x[j])
        if not math.isinf(hi):
            bviol = max(bviol, x[j] - hi)
    cviol, worst = mp.mpf(0), None
    for r in range(I["ncons"]):
        v = row_value(I, r, x)
        lo, hi = I["rows"][r]["lb"], I["rows"][r]["ub"]
        e = mp.mpf(0)
        if lo is not None and not math.isinf(lo):
            e = max(e, lo - v)
        if hi is not None and not math.isinf(hi):
            e = max(e, v - hi)
        if e > cviol:
            cviol, worst = e, I["rows"][r].get("name")
    obj = row_value(I, -1, x)
    return dict(obj=float(obj), obj_mp=obj, bound_viol=float(bviol), cons_viol=float(cviol), worst_row=worst)
