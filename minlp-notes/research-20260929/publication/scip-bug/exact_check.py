"""Exact feasibility check of a point for a CIP model file (no SCIP involved).

Reads the subset of the CIP format written by export_models.py / minimize.py:
  VARIABLES:   [binary|continuous] <name>: obj=c, original bounds=[lb,ub]
  CONSTRAINTS: [linear|nonlinear] <name>: (+|-)coef<v> ... or (+|-)coef*<v>*<w> ...  (==|>=|<=) rhs;
Every number in the file is a plain decimal string and is read exactly as a
Fraction.  The point is a JSON object {name: rational string}.  The check is
done in exact rational arithmetic: every row, every bound and integrality of
the binaries must hold with zero violation.

It also reports the largest violation when the coefficients are first rounded
to the nearest double (the model SCIP actually solves after parsing).

usage: python3 exact_check.py MODEL.cip POINT.json [CLAIM]
With CLAIM (SCIP's claimed optimal value, a decimal string) it reports
objective(point) - CLAIM exactly.
"""
import json
import re
import sys
from fractions import Fraction as F

TERM = re.compile(r"([+-](?:\d+(?:\.\d*)?|\.\d+))((?:\*?<[^>]+>)*)")
VAR = re.compile(r"<([^>]+)>")


def parse_cip(path):
    vars_, rows, sec = [], [], None
    for line in open(path):
        s = line.strip()
        if s in ("STATISTICS", "OBJECTIVE", "VARIABLES", "CONSTRAINTS", "END"):
            sec = s
            continue
        if not s:
            continue
        if sec == "OBJECTIVE":
            if s.startswith("Sense"):
                assert s.split(":")[1].strip() == "minimize", s
            continue
        if sec == "VARIABLES":
            m = re.fullmatch(r"\[(binary|continuous)\] <([^>]+)>: obj=([^,]+), original bounds=\[([^,]+),([^\]]+)\]", s)
            assert m, s
            typ, name, obj, lb, ub = m.groups()
            vars_.append(dict(name=name, type=typ, obj=F(obj),
                              lb=None if lb == "-inf" else F(lb), ub=None if ub == "+inf" else F(ub)))
        elif sec == "CONSTRAINTS":
            m = re.fullmatch(r"\[(linear|nonlinear)\] <([^>]+)>: (.*) (==|>=|<=) ([-+]?[\d.]+);", s)
            assert m, s
            kind, name, body, op, rhs = m.groups()
            terms = []
            pos = 0
            body = body.replace(" ", "")
            for t in TERM.finditer(body):
                assert t.start() == pos, (name, body[pos:pos + 40])
                pos = t.end()
                vs = VAR.findall(t.group(2))
                if kind == "linear":
                    assert len(vs) == 1, (name, t.group(0))
                terms.append((F(t.group(1)), vs))
            assert pos == len(body), (name, body[pos:])
            rows.append(dict(name=name, terms=terms, op=op, rhs=F(rhs)))
    return vars_, rows


def value(terms, x):
    s = F(0)
    for a, vs in terms:
        v = a
        for n in vs:
            v *= x[n]
        s += v
    return s


def check(path, point, claim=None, verbose=True):
    vars_, rows = parse_cip(path)
    x = {k: F(v) for k, v in point.items()}
    names = {v["name"] for v in vars_}
    missing = names - set(x)
    assert not missing, f"point lacks {sorted(missing)[:5]}"
    worst_row, worst_bnd, int_ok = (F(0), None), (F(0), None), True
    worst_dbl = F(0)
    for r in rows:
        lhs = value(r["terms"], x)
        if r["op"] == "==":
            viol = abs(lhs - r["rhs"])
        elif r["op"] == ">=":
            viol = max(F(0), r["rhs"] - lhs)
        else:
            viol = max(F(0), lhs - r["rhs"])
        if viol > worst_row[0]:
            worst_row = (viol, r["name"])
        # the same row with coefficients and right-hand side rounded to doubles
        lhs_d = value([(F(float(a)), vs) for a, vs in r["terms"]], x)
        rhs_d = F(float(r["rhs"]))
        vd = abs(lhs_d - rhs_d) if r["op"] == "==" else (max(F(0), rhs_d - lhs_d) if r["op"] == ">=" else max(F(0), lhs_d - rhs_d))
        worst_dbl = max(worst_dbl, vd)
    for v in vars_:
        xv = x[v["name"]]
        bv = max(F(0), (v["lb"] - xv) if v["lb"] is not None else F(0), (xv - v["ub"]) if v["ub"] is not None else F(0))
        if bv > worst_bnd[0]:
            worst_bnd = (bv, v["name"])
        if v["type"] == "binary" and xv not in (0, 1):
            int_ok = False
    obj = sum(v["obj"] * x[v["name"]] for v in vars_)
    feasible = worst_row[0] == 0 and worst_bnd[0] == 0 and int_ok
    out = dict(model=path, nvars=len(vars_), nrows=len(rows), objective=obj, feasible=feasible,
               max_row_violation=worst_row, max_bound_violation=worst_bnd, binaries_integral=int_ok,
               max_row_violation_double_coefs=worst_dbl)
    if claim is not None:
        out["objective_minus_claim"] = obj - F(claim)
    if verbose:
        print(f"model {path}: {len(vars_)} variables, {len(rows)} rows")
        print(f"  exact objective = {obj}  (~ {float(obj):.12f})")
        print(f"  max row violation (exact data) = {worst_row[0]} {worst_row[1] or ''}")
        print(f"  max bound violation = {worst_bnd[0]} {worst_bnd[1] or ''}; binaries integral: {int_ok}")
        print(f"  max row violation with double-rounded coefficients = {float(worst_dbl):.3e}")
        if claim is not None:
            d = out["objective_minus_claim"]
            print(f"  objective - claimed optimum ({claim}) = {float(d):.9f} (exact: {'< 0' if d < 0 else '>= 0'})")
        print(f"  EXACTLY FEASIBLE: {feasible}")
    return out


if __name__ == "__main__":
    pt = json.load(open(sys.argv[2]))
    r = check(sys.argv[1], pt, sys.argv[3] if len(sys.argv) > 3 else None)
    sys.exit(0 if r["feasible"] and (len(sys.argv) <= 3 or r["objective_minus_claim"] < 0) else 1)
