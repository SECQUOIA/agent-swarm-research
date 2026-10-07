"""Exact check of the witnesses against the GAMS model files in gams/ (third
author; independent of exact_check.py, spec_check.py and indep_check.py, and
of SCIP and GAMS).

GAMS/SCIP solved the .gms files, not the CIP files, so its wrong claims must be
refuted on the .gms models themselves.  For each .gms file this script

  1. reads the variable declarations, bounds (.lo/.up/.fx) and equations
     ("name.. lhs =e=|=l=|=g= rhs;"); every number literal becomes a Fraction
     of its decimal text, power(a,k) becomes a**k;
  2. sets the objective variable from its defining equation
     ("objvar =e= expr;") and takes all other values from the witness JSON;
  3. evaluates every equation, bound and binary integrality exactly;
  4. compares the exact objective with every claim GAMS/SCIP reported as
     optimal in gams/logs/scan_*.txt (and the tiny2 log).

usage: python3 gams_check.py
"""
import ast
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def ev(src, node, x):
    """Exact value of a restricted expression AST (numbers, names, + - * **)."""
    if isinstance(node, ast.Expression):
        return ev(src, node.body, x)
    if isinstance(node, ast.Constant):
        return Fraction(ast.get_source_segment(src, node))  # decimal text, not the float
    if isinstance(node, ast.Name):
        return x[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = ev(src, node.operand, x)
        return -v if isinstance(node.op, ast.USub) else v
    if isinstance(node, ast.BinOp):
        a, b = ev(src, node.left, x), ev(src, node.right, x)
        if isinstance(node.op, ast.Add):
            return a + b
        if isinstance(node.op, ast.Sub):
            return a - b
        if isinstance(node.op, ast.Mult):
            return a * b
        if isinstance(node.op, ast.Pow):
            assert b.denominator == 1 and b >= 0
            return a ** int(b)
    raise ValueError(f"unsupported expression: {ast.dump(node)[:80]}")


def to_py(e):
    e = re.sub(r"\bpower\(", "pw(", e, flags=re.I)
    # pw(a,k) -> ((a)**(k)); arguments in these files are a variable name and an integer
    e = re.sub(r"pw\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,\s*([0-9]+)\s*\)", r"((\1)**(\2))", e)
    assert "pw(" not in e, e
    return e


def parse(path):
    text = open(path).read()
    text = "\n".join(l for l in text.splitlines() if not l.startswith("*"))  # comment lines
    stmts = [s.strip() for s in text.split(";") if s.strip()]
    kind, lb, ub, eqs, objvar, sense = {}, {}, {}, [], None, None
    for s in stmts:
        s1 = " ".join(s.split())
        m = re.match(r"(?i)^(binary|positive|free|integer)?\s*variables?\s+(.*)$", s1)
        if m:
            k = (m.group(1) or "free").lower()
            for v in m.group(2).split(","):
                kind[v.strip()] = k
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\.(lo|up|fx|l)\s*=\s*(\S+)$", s1)
        if m:
            v, a, val = m.group(1), m.group(2), Fraction(m.group(3))
            if a in ("lo", "fx"):
                lb[v] = val
            if a in ("up", "fx"):
                ub[v] = val
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\.\.\s*(.*?)\s*=([egl])=\s*(.*)$", s1, flags=re.I)
        if m:
            eqs.append((m.group(1), to_py(m.group(2)), m.group(3).lower(), to_py(m.group(4))))
            continue
        m = re.match(r"(?i)^solve\s+\S+\s+using\s+\S+\s+(minimizing|maximizing)\s+(\S+)$", s1)
        if m:
            sense, objvar = m.group(1).lower(), m.group(2)
            continue
    for v, k in kind.items():
        if k == "binary":
            lb.setdefault(v, Fraction(0)); ub.setdefault(v, Fraction(1))
        elif k == "positive":
            lb.setdefault(v, Fraction(0))
    return kind, lb, ub, eqs, objvar, sense


def check(gms, witness, claims):
    kind, lb, ub, eqs, objvar, sense = parse(os.path.join(HERE, gms))
    assert sense == "minimizing"
    x = {k: Fraction(v) for k, v in json.load(open(os.path.join(HERE, witness))).items()}
    model_vars = set(kind) - {objvar}
    missing = model_vars - set(x)
    extra = set(x) - model_vars
    assert not missing, f"witness lacks {sorted(missing)[:5]}"
    # variables of the witness that the .gms file does not declare must be fixed in the CIP model;
    # report them (they are constants in the .gms file)
    defs = [e for e in eqs if e[1].strip() == objvar and e[2] == "e"]
    assert len(defs) == 1, "objective variable must have exactly one defining equation"
    x[objvar] = ev(defs[0][3], ast.parse(defs[0][3], mode="eval"), x)
    bad = []
    for name, l, s, r in eqs:
        a = ev(l, ast.parse(l, mode="eval"), x)
        b = ev(r, ast.parse(r, mode="eval"), x)
        if not (a == b if s == "e" else (a <= b if s == "l" else a >= b)):
            bad.append(name)
    for v in kind:
        if v in lb and x[v] < lb[v] or v in ub and x[v] > ub[v]:
            bad.append(v)
        if kind[v] in ("binary", "integer") and x[v].denominator != 1:
            bad.append(v)
    obj = x[objvar]
    print(f"{gms}: {len(kind)} variables, {len(eqs)} equations; witness variables not declared in the "
          f".gms file: {sorted(extra) or 'none'}; violated: {bad or 'none'}; objective = {float(obj):.12f}")
    ok = not bad
    for c in claims:
        d = obj - Fraction(c)
        ok &= d < 0
        print(f"    objective - GAMS/SCIP claim {c} = {float(d):+.9f}  ({'claim refuted' if d < 0 else 'NOT below claim'})")
    return ok


def claims_from_scan(key):
    out = []
    for line in open(os.path.join(HERE, "gams", "logs", f"scan_{key}.txt")):
        if "WRONG" in line:
            out.append(re.search(r"dual (\S+)", line).group(1))
    return out


def claim_from_log(tag):
    t = open(os.path.join(HERE, "gams", "logs", f"gams_{tag}.log")).read()
    st = re.search(r"SCIP Status\s*:\s*(.*)", t).group(1)
    db = re.search(r"Dual Bound\s*:\s*(\S+)", t).group(1)
    return st, db


if __name__ == "__main__":
    allok = True
    for key, wit in (("p0", "witness/p0.json"), ("p4", "witness/p4.json"), ("p5", "witness/p5.json"),
                     ("pair2236", "witness/pair2236.json"), ("pumps_default", "minimal/pumps_default_witness.json"),
                     ("fm336", "min/fm336_v1010.witness.json"), ("fm318", "min/fm318_master.witness.json")):
        allok &= check(f"gams/{key}.gms", wit, claims_from_scan(key))
    for tag in ("tiny2_heur_sepa_off", "tiny2_default"):
        st, db = claim_from_log(tag)
        print(f"gams/logs/gams_{tag}.log: SCIP status '{st}', dual bound {db}")
    st, db = claim_from_log("tiny2_heur_sepa_off")
    allok &= check("gams/tiny2.gms", "minimal/tiny2_witness.json", [db] if st.startswith("problem is solved [optimal") else [])
    print("ALL CHECKS PASSED (witnesses exactly feasible for the .gms models, below every wrong claim):", allok)
    sys.exit(0 if allok else 1)
