"""Verifier: own OSiL reader and evaluator. Compares two OSiL files that should
describe the same model (e.g. the cached MINLPLib OSIL and a GAMS 54.3
Convert OSiL of the current .gms):
  * variables by name: type and bounds, exactly (Fraction);
  * constraints by name: bounds (after moving the row constant), exactly;
  * every row and the objective: value at K random points in 60-digit mpmath
    (same point for both files, mapped by variable name). A row "differs" if
    |fa - fb - shift| > 1e-45 * max(1, |fa|, |fb|) at some point. The
    largest absolute and relative differences are reported.
This is numerical evidence about equality of the row functions, not a proof.

Usage: python3 osil_eval_cmp.py A.osil B.osil [K]
"""
import random
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction

import mpmath
from mpmath import mp

mp.dps = 60
INF = {"INF", "inf", "Infinity", "1e+20", "1e20", "1E20", "1E+20"}


def tag(e):
    return e.tag.split("}")[-1]


def fr(s, default):
    if s is None:
        return default
    if s in INF or s.lstrip("+") in INF:
        return None
    if s.startswith("-") and s[1:] in INF:
        return None
    return Fraction(s)


def read(path):
    root = ET.parse(path).getroot()
    d = next(c for c in root if tag(c) == "instanceData")
    M = {"vars": [], "lb": [], "ub": [], "type": [], "cons": [], "clb": [], "cub": [], "cconst": [],
         "lin": {}, "quad": {}, "nl": {}, "obj": None}
    for sec in d:
        t = tag(sec)
        if t == "variables":
            for v in sec:
                M["vars"].append(v.get("name"))
                M["type"].append(v.get("type", "C"))
                lb = v.get("lb")
                M["lb"].append(Fraction(0) if lb is None else (None if lb.lstrip("-") in INF else Fraction(lb)))
                ub = v.get("ub")
                M["ub"].append(None if ub is None or ub.lstrip("+") in INF else Fraction(ub))
        elif t == "objectives":
            o = sec[0]
            coef = {}
            for c in o:
                coef[int(c.get("idx"))] = Fraction(c.text)
            M["obj"] = dict(sense=o.get("maxOrMin", "min"), const=Fraction(o.get("constant", "0")), lin=coef)
        elif t == "constraints":
            for c in sec:
                M["cons"].append(c.get("name"))
                lb, ub = c.get("lb"), c.get("ub")
                M["clb"].append(None if lb is None or lb.lstrip("-") in INF else Fraction(lb))
                M["cub"].append(None if ub is None or ub.lstrip("+") in INF else Fraction(ub))
                M["cconst"].append(Fraction(c.get("constant", "0")))
        elif t == "linearConstraintCoefficients":
            parts = {tag(p): p for p in sec}
            start = expand(parts["start"])
            val = [Fraction(x) for x in expand(parts["value"], conv=str)]
            if "rowIdx" in parts:
                idx = expand(parts["rowIdx"])
                for j in range(len(start) - 1):
                    for k in range(start[j], start[j + 1]):
                        M["lin"].setdefault(idx[k], {})[j] = M["lin"].get(idx[k], {}).get(j, 0) + val[k]
            else:
                idx = expand(parts["colIdx"])
                for i in range(len(start) - 1):
                    for k in range(start[i], start[i + 1]):
                        M["lin"].setdefault(i, {})[idx[k]] = M["lin"].get(i, {}).get(idx[k], 0) + val[k]
        elif t == "quadraticCoefficients":
            for q in sec:
                i = int(q.get("idx"))
                M["quad"].setdefault(i, []).append((int(q.get("idxOne")), int(q.get("idxTwo")), Fraction(q.get("coef", "1"))))
        elif t == "nonlinearExpressions":
            for nl in sec:
                i = int(nl.get("idx"))
                M["nl"][i] = nl[0]
    return M


def expand(el, conv=int):
    """OSiL arrays: <el mult= incr=>v</el> or <i ...>"""
    out = []
    for e in el:
        mult = int(e.get("mult", "1"))
        incr = e.get("incr")
        v = e.text.strip()
        if conv is int:
            v0 = int(v)
            inc = int(incr) if incr else 0
            out.extend(v0 + k * inc for k in range(mult))
        else:
            out.extend([v] * mult)
    return out


def ev(e, x):
    t = tag(e)
    ch = list(e)
    if t == "number":
        return mpmath.mpf(Fraction(e.get("value")).numerator) / Fraction(e.get("value")).denominator
    if t == "variable":
        c = Fraction(e.get("coef", "1"))
        return (mpmath.mpf(c.numerator) / c.denominator) * x[int(e.get("idx"))]
    a = [ev(c, x) for c in ch]
    if t in ("sum", "plus"):
        return mpmath.fsum(a)
    if t == "minus":
        return a[0] - a[1]
    if t == "negate":
        return -a[0]
    if t in ("times", "product"):
        r = mpmath.mpf(1)
        for v in a:
            r *= v
        return r
    if t == "divide":
        return a[0] / a[1]
    if t == "power":
        return mpmath.power(a[0], a[1])
    if t == "square":
        return a[0] ** 2
    if t == "sqrt":
        return mpmath.sqrt(a[0])
    if t == "exp":
        return mpmath.exp(a[0])
    if t == "ln":
        return mpmath.log(a[0])
    if t == "log10":
        return mpmath.log10(a[0])
    if t == "abs":
        return abs(a[0])
    if t == "sin":
        return mpmath.sin(a[0])
    if t == "cos":
        return mpmath.cos(a[0])
    if t == "tanh":
        return mpmath.tanh(a[0])
    if t == "max":
        return max(a)
    if t == "min":
        return min(a)
    raise ValueError("node " + t)


def mpf(f):
    return mpmath.mpf(f.numerator) / f.denominator


def row_value(M, i, x):
    """i = -1 objective; returns value without the row constant/bounds"""
    v = mpmath.mpf(0)
    lin = M["obj"]["lin"] if i == -1 else M["lin"].get(i, {})
    for j, c in lin.items():
        v += mpf(c) * x[j]
    for (p, q, c) in M["quad"].get(i, []):
        v += mpf(c) * x[p] * x[q]
    if i in M["nl"]:
        v += ev(M["nl"][i], x)
    return v


def main(pa, pb, K=3):
    A, B = read(pa), read(pb)
    ia = {n: j for j, n in enumerate(A["vars"])}
    ib = {n: j for j, n in enumerate(B["vars"])}
    print("vars", len(ia), len(ib), "same names:", set(ia) == set(ib))
    vd = [n for n in ia if n in ib and (A["type"][ia[n]], A["lb"][ia[n]], A["ub"][ia[n]]) !=
          (B["type"][ib[n]], B["lb"][ib[n]], B["ub"][ib[n]])]
    print("variable type/bound differences:", len(vd), vd[:5])
    ca = {n: i for i, n in enumerate(A["cons"])}
    cb = {n: i for i, n in enumerate(B["cons"])}
    print("cons", len(ca), len(cb), "same names:", set(ca) == set(cb))
    print("obj sense", A["obj"]["sense"], B["obj"]["sense"])
    rng = random.Random(7)
    pts = []
    for k in range(K):
        x = {}
        for n in ia:
            lo, hi = A["lb"][ia[n]], A["ub"][ia[n]]
            if lo is not None and hi is not None:
                v = float(lo) + rng.random() * float(hi - lo)
            elif lo is not None:
                v = float(lo) + rng.uniform(0.1, 2.0)
            elif hi is not None:
                v = float(hi) - rng.uniform(0.1, 2.0)
            else:
                v = rng.uniform(-2, 2)
            x[n] = mpmath.mpf(v)
        pts.append(x)
    xa = [[p[n] for n in A["vars"]] for p in pts]
    xb = [[p[n] for n in B["vars"]] for p in pts]
    worst_abs, worst_rel, ndiff, nbound, nskip = mpmath.mpf(0), mpmath.mpf(0), 0, 0, 0
    examples = []
    rows = [("objective", -1, -1)] + [(n, ca[n], cb[n]) for n in ca if n in cb]
    for name, i, j in rows:
        if i == -1:
            sa, sb = mpf(A["obj"]["const"]), mpf(B["obj"]["const"])
        else:
            # move constants into bounds; bounds must match up to one shift
            la, ua = A["clb"][i], A["cub"][i]
            lb_, ub_ = B["clb"][j], B["cub"][j]
            ka, kb = A["cconst"][i], B["cconst"][j]
            ba = (None if la is None else la - ka, None if ua is None else ua - ka)
            bb = (None if lb_ is None else lb_ - kb, None if ub_ is None else ub_ - kb)
            if (ba[0] is None) != (bb[0] is None) or (ba[1] is None) != (bb[1] is None):
                nbound += 1
                examples.append((name, "bound sides", ba, bb))
                continue
            shifts = {p - q for p, q in zip(ba, bb) if p is not None}
            if len(shifts) > 1:
                nbound += 1
                examples.append((name, "bounds", ba, bb))
                continue
            sh = shifts.pop() if shifts else Fraction(0)
            sa, sb = mpf(sh), mpmath.mpf(0)
        for k in range(K):
            try:
                fa = row_value(A, i, xa[k]) + (sa if i == -1 else 0)
                fb = row_value(B, j, xb[k]) + (sb if i == -1 else 0)
            except (ValueError, ZeroDivisionError):
                nskip += 1
                continue
            if isinstance(fa, mpmath.mpc) or isinstance(fb, mpmath.mpc):
                nskip += 1
                continue
            d = abs(fa - fb - (0 if i == -1 else sa))
            rel = d / max(1, abs(fa), abs(fb))
            if d > worst_abs:
                worst_abs = d
            if rel > worst_rel:
                worst_rel = rel
            if rel > mpmath.mpf("1e-45"):
                ndiff += 1
                if len(examples) < 6:
                    examples.append((name, mpmath.nstr(d, 4), mpmath.nstr(rel, 4)))
                break
    print(f"rows compared {len(rows)}; rows with differences {ndiff}; bound mismatches {nbound}; "
          f"evaluations skipped {nskip}; worst abs {mpmath.nstr(worst_abs, 4)}; worst rel {mpmath.nstr(worst_rel, 4)}")
    for e in examples[:6]:
        print("  ", e)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3)
