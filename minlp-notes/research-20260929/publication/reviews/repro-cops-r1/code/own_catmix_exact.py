"""Verifier's own exact evaluation of catmix primal points from the cached OSIL model.

Independent of the track's and the reviewers' code. Parses the OSIL file (quadratic model:
linear coefficients + qTerms), fixes the controls to the doubles of a .npy control vector
(each double taken exactly as a Fraction), solves the remaining equality rows for the states
exactly (rational arithmetic, propagation over rows whose unknowns form 1- or 2-sets), checks
every row exactly, checks all variable bounds exactly, and prints the exact objective
(floor/ceil at 25 decimal places).
usage: own_catmix_exact.py N file.npy [file.npy ...]   (npy read from git blob c3514f03 if it
       starts with 'git:', else from disk)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import io, os, re, subprocess, sys, time
import xml.etree.ElementTree as ET
from fractions import Fraction as F
import numpy as np

NS = "{os.optimizationservices.org}"
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/catmix%d.osil")
INF = {"INF", "+INF", "inf", "Infinity"}

def expand(elem, is_int=True):
    out = []
    for el in elem.findall(NS + "el"):
        mult = int(el.get("mult", "1")); incr = el.get("incr")
        v = int(el.text) if is_int else F(el.text)
        if incr is None:
            out += [v] * mult
        else:
            inc = int(incr) if is_int else F(incr)
            out += [v + k * inc for k in range(mult)]
    return out

def load(N):
    root = ET.parse(OSIL % N).getroot()
    d = root.find(NS + "instanceData")
    vs = d.find(NS + "variables").findall(NS + "var")
    lb, ub = [], []
    for v in vs:
        a = v.get("lb", "0"); b = v.get("ub", "INF")
        lb.append(None if a in ("-INF", "-inf", "-Infinity") else F(a))
        ub.append(None if b in INF else F(b))
        assert v.get("type", "C") == "C"
    obj = d.find(NS + "objectives").find(NS + "obj")
    assert obj.get("maxOrMin") == "min"
    oc = {int(c.get("idx")): F(c.text) for c in obj.findall(NS + "coef")}
    ocon = F(obj.get("constant", "0"))
    cons = d.find(NS + "constraints").findall(NS + "con")
    clb = [F(c.get("lb")) for c in cons]; cub = [F(c.get("ub")) for c in cons]
    assert all(c.get("constant") is None for c in cons)
    lcc = d.find(NS + "linearConstraintCoefficients")
    start = expand(lcc.find(NS + "start")); col = expand(lcc.find(NS + "colIdx"))
    val = expand(lcc.find(NS + "value"), is_int=False)
    rows = [dict(lin={}, quad=[]) for _ in cons]
    for r in range(len(cons)):
        for k in range(start[r], start[r + 1]):
            rows[r]["lin"][col[k]] = rows[r]["lin"].get(col[k], 0) + val[k]
    q = d.find(NS + "quadraticCoefficients")
    for t in q.findall(NS + "qTerm"):
        i = int(t.get("idx"))
        assert i >= 0, "quadratic objective not expected"
        rows[i]["quad"].append((int(t.get("idxOne")), int(t.get("idxTwo")), F(t.get("coef"))))
    assert d.find(NS + "nonlinearExpressions") is None
    return lb, ub, oc, ocon, clb, cub, rows

def evaluate(N, u):
    lb, ub, oc, ocon, clb, cub, rows = load(N)
    n = len(lb)
    assert n == 3 * (N + 1) and len(u) == N + 1
    x = [None] * n
    for i in range(N + 1):
        x[i] = F(float(u[i]))
    for i in range(n):
        if lb[i] is not None and ub[i] is not None and lb[i] == ub[i]:
            assert x[i] is None or x[i] == lb[i]
            x[i] = lb[i]
    # each row is linear in the unknowns once x[0..N] (controls) are fixed; check that
    for r in rows:
        for (a, b, c) in r["quad"]:
            assert (a <= N) != (b <= N), "qTerm not of the form control*state"
    def linform(r):
        coef = {}; const = F(0)
        for j, c in r["lin"].items():
            if x[j] is None: coef[j] = coef.get(j, 0) + c
            else: const += c * x[j]
        for (a, b, c) in r["quad"]:
            if x[a] is not None and x[b] is not None: const += c * x[a] * x[b]
            elif x[a] is not None: coef[b] = coef.get(b, 0) + c * x[a]
            elif x[b] is not None: coef[a] = coef.get(a, 0) + c * x[b]
            else: raise AssertionError("bilinear in two unknowns")
        return {j: c for j, c in coef.items() if c != 0}, const
    for r, (a, b) in enumerate(zip(clb, cub)):
        assert a == b, "only equality rows expected"
    pending = set(range(len(rows)))
    while pending:
        progress = False
        bykey = {}
        for r in sorted(pending):
            coef, const = linform(rows[r])
            if not coef:
                continue
            key = tuple(sorted(coef))
            if len(key) == 1:
                j = key[0]; x[j] = (clb[r] - const) / coef[j]; pending.discard(r); progress = True; break
            if len(key) == 2:
                if key in bykey:
                    r0, c0, k0 = bykey[key]
                    (j1, j2) = key
                    a11, a12, b1 = c0[j1], c0[j2], clb[r0] - k0
                    a21, a22, b2 = coef[j1], coef[j2], clb[r] - const
                    det = a11 * a22 - a12 * a21
                    assert det != 0
                    x[j1] = (b1 * a22 - a12 * b2) / det
                    x[j2] = (a11 * b2 - a21 * b1) / det
                    pending.discard(r); pending.discard(r0); progress = True; break
                bykey[key] = (r, coef, const)
        if not progress:
            # all remaining rows fully determined?
            rem = [r for r in pending if not linform(rows[r])[0]]
            if len(rem) == len(pending): break
            raise AssertionError("propagation stuck with %d rows" % len(pending))
    assert all(v is not None for v in x), "undetermined variables"
    # exact feasibility check of every row and bound
    maxres = 0
    for r, row in enumerate(rows):
        s = sum(c * x[j] for j, c in row["lin"].items()) + sum(c * x[a] * x[b] for a, b, c in row["quad"])
        assert clb[r] <= s <= cub[r], ("row", r)
    for i in range(n):
        if lb[i] is not None: assert x[i] >= lb[i], ("lb", i)
        if ub[i] is not None: assert x[i] <= ub[i], ("ub", i)
    J = ocon + sum(c * x[j] for j, c in oc.items())
    return J

def dec(q, digits=25):
    s = 10 ** digits
    fl = q.numerator * s // q.denominator
    ce = -((-q.numerator * s) // q.denominator)
    return "%s / %s" % (fmt(fl, digits), fmt(ce, digits))

def fmt(k, digits):
    sgn = "-" if k < 0 else ""; k = abs(k)
    return "%s%d.%0*d" % (sgn, k // 10 ** digits, digits, k % 10 ** digits)

if __name__ == "__main__":
    N = int(sys.argv[1])
    for spec in sys.argv[2:]:
        t0 = time.time()
        if spec.startswith("git:"):
            b = subprocess.run(["git", "-C", (_PUBLIC_REPO), "show", "c3514f03:" + spec[4:]],
                               capture_output=True, check=True).stdout
            u = np.load(io.BytesIO(b))
        else:
            u = np.load(spec)
        J = evaluate(N, u)
        print("N=%d %s: exact feasible (all rows equal exactly, all bounds hold); J floor/ceil 1e-25: %s ; float %r (%.1fs)"
              % (N, spec, dec(J), float(J), time.time() - t0), flush=True)
