"""Recheck the constants of saved cuts after the outward-rounding fix in Curve._piece_lower (no solver).

For every cut (c0, c) in the given files, rebuild the curve from the recorded funcs, l and u, and compute
  c0_new = -certified_min(c) with the corrected code (same parameters as in Curve.separate), and
  c0_old = the same with the earlier round-to-nearest subtraction (checks that the saved c0 is reproduced).
A saved cut is certified by the corrected code if c0_saved >= c0_new.  Otherwise the corrected code is
asked for a lower bound of c.phi over [l, u] of at least -c0_saved (bisection with target -c0_saved, tol 0);
if it returns one, the saved cut is certified as well.  Cuts that still fail are checked with 200-bit
interval arithmetic (mpmath.iv): branch and bound on [l, u] with the natural interval extension and a
second-order Taylor bound of g = c0 + c.phi, all constants converted exactly from the recorded floats.
python cuts_rounding_check.py <cuts file> ...   (one JSON line per file)"""
import json
import os
import sys

import numpy as np
import sympy as sp
from mpmath import iv

from curvehull import T, Curve


class OldCurve(Curve):
    """Curve with the pre-fix _piece_lower (final subtraction rounded to nearest)."""

    def _piece_lower(self, c, a, b, enc_a, enc_b, piece):
        Flo, Fhi, Dlo, Dhi = piece
        direct = self._lin_lower(c, Flo, Fhi)
        ga = self._lin_lower(c, *enc_a)
        gb = self._lin_lower(c, *enc_b)
        d2hi = -self._lin_lower(-c, Dlo, Dhi)
        h = b - a
        with np.errstate(invalid="ignore"):
            m = np.maximum(0.0, d2hi) * (h * h / 8.0) * (1 + 1e-15)
            taylor = np.minimum(ga, gb) - m
        taylor = np.where(np.isnan(taylor), -np.inf, taylor)
        out = np.maximum(direct, taylor)
        return np.where(np.isnan(out), -np.inf, out)


def _iv(e, X):
    """mpmath.iv enclosure of the sympy expression e(T) over the interval X."""
    if e == T:
        return X
    if e.is_Rational:
        return iv.mpf(int(e.p)) / int(e.q)
    if e.is_Add or e.is_Mul:
        out = _iv(e.args[0], X)
        for a in e.args[1:]:
            out = out + _iv(a, X) if e.is_Add else out * _iv(a, X)
        return out
    if e.is_Pow:
        b, q = e.args
        if q.is_Integer:
            return _iv(b, X) ** int(q)
        return iv.exp(_iv(q, X) * iv.log(_iv(b, X)))
    f = {sp.exp: iv.exp, sp.log: iv.log, sp.sin: iv.sin, sp.cos: iv.cos}[e.func]
    return f(_iv(e.args[0], X))


def mp_certify(cut, max_pieces=100000):
    """True if 200-bit interval arithmetic proves c0 + c.phi(t) >= 0 on [l, u]."""
    iv.prec = 200
    fs = [T] + [sp.sympify(s, locals={"t": T}) for s in cut["funcs"]]
    fs = [f.xreplace({x: sp.Rational(x) for x in f.atoms(sp.Float)}) for f in fs]  # exact from here on
    g = sp.Rational(cut["c0"]) + sum(sp.Rational(ci) * f for ci, f in zip(cut["c"], fs))
    g1, g2 = sp.diff(g, T), sp.diff(g, T, 2)
    stack, done = [(iv.mpf(cut["l"]), iv.mpf(cut["u"]))], 0  # pieces [a, b], a and b point intervals
    while stack:
        a, b = stack.pop()
        X = iv.mpf([a, b])
        lower = _iv(g, X).a
        if lower < 0:
            m = X.mid
            r = iv.mpf(max((m - a).b, (b - m).b))
            gm, p, M = _iv(g, m), _iv(g1, m), _iv(g2, X).a  # g(m + d) >= g(m) + p d + M d^2 / 2, |d| <= r
            qmin = None
            for pe in (p.a, p.b):
                cands = [pe * (-r) + M * r * r / 2, pe * r + M * r * r / 2]
                if M > 0 and abs(pe) <= (M * r).b:  # vertex -pe / M possibly in [-r, r]
                    cands.append(-pe * pe / (2 * M))
                q = min(c.a for c in cands)
                qmin = q if qmin is None else min(qmin, q)
            lower = max(lower, (gm + qmin).a)
        done += 1
        if lower >= 0:
            continue
        if done > max_pieces:
            return False
        stack += [(a, X.mid), (X.mid, b)]
    return True


def check(path):
    cuts = json.load(open(path))
    curves = {}
    n_same = n_weaker = n_stronger = n_old_repr = 0
    max_diff = max_rel = 0.0  # max of c0_new - c0_saved (> 0: saved cut stronger than the corrected constant)
    stronger_cert = stronger_fail = mp_cert = 0
    for cut in cuts:
        key = (tuple(cut["funcs"]), cut["l"], cut["u"])
        if key not in curves:
            fs = [sp.sympify(s, locals={"t": T}) for s in cut["funcs"]]
            curves[key] = (Curve(fs, cut["l"], cut["u"]), OldCurve(fs, cut["l"], cut["u"]))
        C, Cold = curves[key]
        c = np.array(cut["c"], float)
        c0 = cut["c0"]
        c0_new = -C.certified_min(c)
        n_old_repr += -Cold.certified_min(c) == c0
        scale = 1.0 + np.abs(c) @ np.maximum(np.abs(C.rlo), np.abs(C.rhi))
        d = c0_new - c0
        if d == 0:
            n_same += 1
        elif d < 0:
            n_weaker += 1
        else:
            n_stronger += 1
            if C.certified_min(c, target=-c0, tol=0.0) >= -c0:
                stronger_cert += 1
            elif mp_certify(cut):
                mp_cert += 1
            else:
                stronger_fail += 1
        max_diff, max_rel = max(max_diff, d), max(max_rel, d / scale)
    return {"file": os.path.relpath(path, os.path.dirname(os.path.abspath(__file__))), "ncuts": len(cuts),
            "curves": len(curves), "saved_c0_reproduced_by_old_code": n_old_repr,
            "new_equal": n_same, "saved_weaker": n_weaker, "saved_stronger": n_stronger,
            "max_c0_new_minus_saved": max_diff, "max_rel": max_rel,
            "stronger_certified_at_saved_c0": stronger_cert, "stronger_certified_200bit": mp_cert,
            "stronger_not_certified": stronger_fail}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(check(p)), flush=True)
