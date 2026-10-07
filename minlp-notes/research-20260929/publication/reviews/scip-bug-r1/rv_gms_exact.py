#!/usr/bin/env python3
"""Reviewer's own exact checker for the GAMS models (scip-bug review r1). No track code, no SCIP.

Usage: rv_gms_exact.py MODEL.gms WITNESS.json CIP_MODEL.cip [CLAIM ...]
- parses the restricted GAMS subset used by the track's .gms files (Variables / Binary
  Variables declarations, .lo/.up/.fx assignments, equations NAME.. expr =e=/=l=/=g= expr;
  sums of products of numbers, variables and power(var,int)), all numbers as exact rationals;
- objective: the variable named in 'Solve ... minimizing V', defined by the one =e= row that
  contains V (V = rest);
- checks the witness exactly (witness has no objective variable; it is computed);
- compares the model with the CIP file: same variables, types, bounds, objective
  coefficients, and every constraint as a polynomial (after moving everything to the left).
"""
import json
import re
import sys
from fractions import Fraction as F

sys.path.insert(0, __import__("os").path.dirname(__file__))
from rv_cip_exact import parse_cip  # reviewer's own CIP parser

TOK = re.compile(r"\s*(power\(|[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|[-+*(),])")


def tokens(s):
    out = []
    pos = 0
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            raise SystemExit("tokenize error at %r" % s[pos:pos + 30])
        out.append(m.group(1))
        pos = m.end()
    return out


def poly(expr):
    """Return dict: tuple(sorted var names with multiplicity) -> Fraction."""
    t = tokens(expr)
    i = 0
    res = {}
    first = True
    while i < len(t):
        sign = 1
        if t[i] in "+-":
            sign = -1 if t[i] == "-" else 1
            i += 1
        elif not first:
            raise SystemExit("expected sign in %r" % expr)
        first = False
        coef = F(sign)
        mono = []
        while True:
            tk = t[i]
            if tk == "power(":
                v = t[i + 1]
                assert t[i + 2] == ","
                k = int(t[i + 3])
                assert t[i + 4] == ")"
                mono += [v] * k
                i += 5
            elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", tk):
                mono.append(tk)
                i += 1
            else:
                coef *= F(tk)
                i += 1
            if i < len(t) and t[i] == "*":
                i += 1
                continue
            break
        key = tuple(sorted(mono))
        res[key] = res.get(key, F(0)) + coef
    return {k: v for k, v in res.items() if v != 0}


def parse_gms(path):
    txt = open(path).read()
    stmts = []
    for ln in txt.splitlines():
        if ln.startswith("*") or ln.startswith("$"):
            continue
        stmts.append(ln)
    body = "\n".join(stmts)
    parts = [p.strip() for p in body.split(";") if p.strip()]
    vars_, types, lb, ub, eqs = [], {}, {}, {}, []
    objvar = None
    for p in parts:
        p1 = " ".join(p.split())
        m = re.match(r"(?i)^(binary\s+variables?|variables?)\s+(.*)$", p1)
        if m:
            kind = "binary" if m.group(1).lower().startswith("binary") else "free"
            for n in m.group(2).split(","):
                n = n.strip()
                if n not in vars_:
                    vars_.append(n)
                types[n] = kind
            continue
        m = re.match(r"^([A-Za-z_]\w*)\.(lo|up|fx|l)\s*=\s*(\S+)$", p1)
        if m:
            n, a, v = m.groups()
            if a == "lo":
                lb[n] = F(v)
            elif a == "up":
                ub[n] = F(v)
            elif a == "fx":
                lb[n] = ub[n] = F(v)
            continue
        m = re.match(r"^([A-Za-z_]\w*)\.\.\s*(.*?)\s*=([elgELG])=\s*(.*)$", p1)
        if m:
            name, lhs, rel, rhs = m.groups()
            pl, pr = poly(lhs), poly(rhs)
            d = dict(pl)
            for k, v in pr.items():
                d[k] = d.get(k, F(0)) - v
            d = {k: v for k, v in d.items() if v != 0}
            eqs.append((name, d, rel.lower()))
            continue
        m = re.match(r"(?i)^solve\s+\w+\s+using\s+minlp\s+minimizing\s+(\w+)$", p1)
        if m:
            objvar = m.group(1)
            continue
        if re.match(r"(?i)^(equations?|model|m\.|option|display)", p1):
            continue
        raise SystemExit("unhandled statement: %r" % p1[:120])
    # objective row
    orows = [e for e in eqs if any(objvar in k for k in e[1])]
    assert len(orows) == 1, orows
    oname, od, orel = orows[0]
    assert orel == "e" and od.get((objvar,)) in (1, -1) and sum(1 for k in od if objvar in k) == 1
    s = od[(objvar,)]
    obj = {k: -v / s for k, v in od.items() if k != (objvar,)}
    assert all(len(k) == 1 for k in obj) and () not in obj
    cons = [e for e in eqs if e[0] != oname]
    bounds = {}
    for n in vars_:
        if n == objvar:
            continue
        if types[n] == "binary":
            lo, up = lb.get(n, F(0)), ub.get(n, F(1))
        else:
            lo, up = lb.get(n), ub.get(n)
        bounds[n] = (types[n], lo, up)
    return bounds, {k[0]: v for k, v in obj.items()}, cons


def main():
    gms, wit, cip = sys.argv[1:4]
    claims = sys.argv[4:]
    bounds, obj, cons = parse_gms(gms)
    w = {k: F(str(v)) for k, v in json.load(open(wit)).items()}
    bad = []
    for n, (t, lo, up) in bounds.items():
        x = w[n]
        if lo is not None and x < lo:
            bad.append("lb " + n)
        if up is not None and x > up:
            bad.append("ub " + n)
        if t == "binary" and x not in (0, 1):
            bad.append("bin " + n)
    for name, d, rel in cons:
        a = F(0)
        for k, c in d.items():
            p = c
            for n in k:
                p *= w[n]
            a += p
        if not {"e": a == 0, "l": a <= 0, "g": a >= 0}[rel]:
            bad.append("row %s %s %.3g" % (name, rel, float(a)))
    val = sum((c * w[n] for n, c in obj.items()), F(0))
    # structural comparison with the CIP model
    cvar, corder, ccons = parse_cip(cip)
    diff = []
    if set(cvar) != set(bounds):
        diff.append("variable sets differ: %s" % (set(cvar) ^ set(bounds)))
    for n in corder:
        if n not in bounds:
            continue
        t, lo, up = bounds[n]
        cv = cvar[n]
        ct = "binary" if cv["type"] == "binary" else "free"
        if (ct, cv["lb"], cv["ub"]) != (t, lo, up):
            diff.append("bounds/type %s: cip %s gms %s" % (n, (ct, cv["lb"], cv["ub"]), (t, lo, up)))
        if cv["obj"] != obj.get(n, F(0)):
            diff.append("obj %s: cip %s gms %s" % (n, cv["obj"], obj.get(n, F(0))))
    for n in obj:
        if n not in cvar:
            diff.append("obj var %s not in cip" % n)
    gmap = {name: (d, rel) for name, d, rel in cons}
    cnames = set()
    for cname, kind, terms, rel, rhs in ccons:
        cnames.add(cname)
        d = {}
        for c, ns in terms:
            k = tuple(sorted(ns))
            d[k] = d.get(k, F(0)) + c
        if rhs != 0:
            d[()] = d.get((), F(0)) - rhs
        d = {k: v for k, v in d.items() if v != 0}
        r = {"<=": "l", ">=": "g", "==": "e"}[rel]
        if cname not in gmap:
            diff.append("row %s missing in gms" % cname)
            continue
        gd, grel = gmap[cname]
        if (gd, grel) != (d, r):
            diff.append("row %s differs" % cname)
    if set(gmap) != cnames:
        diff.append("row name sets differ: %s" % (set(gmap) ^ cnames))
    print("gms", gms, "| vars", len(bounds), "| rows", len(cons))
    print("  witness violations:", len(bad), bad[:5])
    print("  objective exact ~ %.15g" % float(val))
    print("  structural differences gms vs cip:", len(diff), diff[:5])
    ok = not bad
    for c in claims:
        d = val - F(c)
        print("  claim %s: obj - claim = %.6g -> %s" % (c, float(d), "BELOW" if d < 0 else "NOT below"))
        ok = ok and d < 0
    print("  RESULT:", "FEASIBLE and below all claims" if ok else "FAIL", "| same model as CIP:", not diff)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
