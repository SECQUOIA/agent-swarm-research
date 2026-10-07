#!/usr/bin/env python3
"""Reviewer's own exact checker (scip-bug review r1). Does not import any track code or SCIP.

Usage: rv_cip_exact.py MODEL.cip WITNESS.json [CLAIM ...]
Reads every decimal literal of the CIP file as an exact rational (Fraction of the decimal
text) and every witness value as Fraction(str). Checks: every variable has a value, bounds,
integrality of [binary]/[integer] variables, every constraint exactly. Prints the exact
objective and, for each CLAIM (decimal text), objective - claim (exact) and whether < 0.
"""
import json
import re
import sys
from fractions import Fraction as F

NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def num(s):
    s = s.strip()
    if s in ("+inf", "inf"):
        return None
    if s == "-inf":
        return None
    return F(s)


def parse_cip(path):
    lines = open(path).read().splitlines()
    sec = None
    var = {}
    order = []
    cons = []
    sense = None
    for ln in lines:
        t = ln.strip()
        if t in ("STATISTICS", "OBJECTIVE", "VARIABLES", "CONSTRAINTS", "END"):
            sec = t
            continue
        if not t:
            continue
        if sec == "OBJECTIVE":
            m = re.match(r"Sense\s*:\s*(\w+)", t)
            if m:
                sense = m.group(1)
            elif t.startswith("Offset"):
                raise SystemExit("objective offset not handled: " + t)
        elif sec == "VARIABLES":
            m = re.fullmatch(r"\[(\w+)\] <([^>]+)>: obj=(" + NUM + r"), original bounds=\[([^,]+),([^\]]+)\]", t)
            if not m:
                raise SystemExit("unparsed variable line: " + t)
            vtype, name, obj, lb, ub = m.groups()
            lbv = None if lb.strip() == "-inf" else F(lb)
            ubv = None if ub.strip() in ("+inf", "inf") else F(ub)
            if lb.strip() in ("+inf", "inf") or ub.strip() == "-inf":
                raise SystemExit("odd bound: " + t)
            var[name] = dict(type=vtype, obj=F(obj), lb=lbv, ub=ubv)
            order.append(name)
        elif sec == "CONSTRAINTS":
            m = re.fullmatch(r"\[(linear|nonlinear)\] <([^>]+)>:\s*(.*?)\s*(<=|>=|==)\s*(" + NUM + r");", t)
            if not m:
                raise SystemExit("unparsed constraint line: " + t)
            kind, cname, body, rel, rhs = m.groups()
            terms = []
            if kind == "linear":
                for tm in re.finditer(r"(" + NUM + r")<([^>]+)>", body):
                    terms.append((F(tm.group(1)), [tm.group(2)]))
                rest = re.sub(r"(" + NUM + r")<([^>]+)>", "", body).strip()
            else:
                for tm in re.finditer(r"(" + NUM + r")((?:\*<[^>]+>)+)", body):
                    names = re.findall(r"<([^>]+)>", tm.group(2))
                    terms.append((F(tm.group(1)), names))
                rest = re.sub(r"(" + NUM + r")((?:\*<[^>]+>)+)", "", body).strip()
            if rest:
                raise SystemExit("leftover text in constraint %s: %r" % (cname, rest))
            for _, ns in terms:
                for n in ns:
                    if n not in var:
                        raise SystemExit("unknown variable %s in %s" % (n, cname))
            cons.append((cname, kind, terms, rel, F(rhs)))
    if sense != "minimize":
        raise SystemExit("sense is not minimize: %r" % sense)
    return var, order, cons


def main():
    model, wit = sys.argv[1], sys.argv[2]
    claims = sys.argv[3:]
    var, order, cons = parse_cip(model)
    w = json.load(open(wit))
    x = {}
    for n in order:
        if n not in w:
            raise SystemExit("witness misses variable " + n)
        x[n] = F(str(w[n]))
    extra = sorted(set(w) - set(order))
    bad = []
    for n in order:
        v = var[n]
        if v["lb"] is not None and x[n] < v["lb"]:
            bad.append("bound lb %s: %s < %s" % (n, x[n], v["lb"]))
        if v["ub"] is not None and x[n] > v["ub"]:
            bad.append("bound ub %s: %s > %s" % (n, x[n], v["ub"]))
        if v["type"] in ("binary", "integer") and x[n].denominator != 1:
            bad.append("integrality %s = %s" % (n, x[n]))
        if v["type"] == "binary" and x[n] not in (0, 1):
            bad.append("binary %s = %s" % (n, x[n]))
        if v["type"] not in ("binary", "integer", "continuous"):
            bad.append("unknown type %s" % v["type"])
    tight = 0
    for cname, kind, terms, rel, rhs in cons:
        act = F(0)
        for c, ns in terms:
            p = c
            for n in ns:
                p *= x[n]
            act += p
        ok = {"<=": act <= rhs, ">=": act >= rhs, "==": act == rhs}[rel]
        if not ok:
            bad.append("constraint %s: %s %s %s violated by %s" % (cname, float(act), rel, float(rhs), float(act - rhs)))
        if act == rhs:
            tight += 1
    obj = sum((var[n]["obj"] * x[n] for n in order), F(0))
    print("model", model, "| vars", len(order), "| cons", len(cons), "(nonlinear %d)" % sum(1 for c in cons if c[1] == "nonlinear"))
    print("witness", wit, "| extra keys in witness:", extra[:5], len(extra))
    print("violations:", len(bad))
    for b in bad[:20]:
        print("  ", b)
    print("tight constraints:", tight)
    print("objective exact =", obj if obj.denominator < 10**6 else "(big fraction)", "~ %.15g" % float(obj))
    allok = not bad
    for c in claims:
        d = obj - F(c)
        print("  claim %s: objective - claim = %.6g  -> %s" % (c, float(d), "BELOW claim" if d < 0 else "NOT below"))
        allok = allok and d < 0
    print("RESULT:", "FEASIBLE and below all claims" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
