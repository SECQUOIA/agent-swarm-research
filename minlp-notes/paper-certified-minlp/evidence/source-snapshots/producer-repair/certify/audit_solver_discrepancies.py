"""Reproduce two historical discrepancy audits without trusting a solver or certificate.

Run from code/minlp_solver_lab: .venv/bin/python -m certify.audit_solver_discrepancies
Source equivalence means symbolic equivalence under exact binary64 literal
semantics. It does not verify GAMS's compiler or the historical runtime.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import re
import runpy
from fractions import Fraction
from pathlib import Path

import sympy as sp
from pyomo.environ import Constraint, Objective, Var, value

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/solver_discrepancy_audit"


def rational(number):
    return Fraction(number)


def listing_values(path):
    return {name: Fraction(0) if number == "." else Fraction(number)
            for name, number in re.findall(
                r"^---- VAR (\w+)\s+\S+\s+(\S+)", path.read_text(), re.M)}


def exact_value(expr, values):
    if not hasattr(expr, "is_expression_type"):
        return rational(expr)
    if expr.is_variable_type():
        return values[expr.name]
    if not expr.is_expression_type():
        return rational(value(expr))
    name = type(expr).__name__
    if name not in {"SumExpression", "LinearExpression", "MonomialTermExpression",
                    "ProductExpression", "NegationExpression", "PowExpression"}:
        raise ValueError(f"unsupported exact expression: {name}")
    args = [exact_value(a, values) for a in expr.args]
    if name == "PowExpression" and args[1].denominator != 1:
        raise ValueError("exact primal check supports integer powers only")
    result = expr._apply_operation(args)
    if not isinstance(result, (int, Fraction)):
        raise ValueError("non-rational evaluation")
    return Fraction(result)


def feasibility(model, values):
    failures = []
    for var in model.component_data_objects(Var):
        level = values[var.name]
        if var.lb is not None and level < rational(var.lb):
            failures.append([var.name, "lower", str(rational(var.lb) - level)])
        if var.ub is not None and level > rational(var.ub):
            failures.append([var.name, "upper", str(level - rational(var.ub))])
        if var.is_integer() and level.denominator != 1:
            failures.append([var.name, "integrality", str(level)])
    for row in model.component_data_objects(Constraint):
        level = exact_value(row.body, values)
        if row.lower is not None and level < rational(value(row.lower)):
            failures.append([row.name, "lower", str(rational(value(row.lower)) - level)])
        if row.upper is not None and level > rational(value(row.upper)):
            failures.append([row.name, "upper", str(level - rational(value(row.upper)))])
    return failures


def sym_number(number):
    q = rational(number)
    return sp.Rational(q.numerator, q.denominator)


def pyomo_symbolic(expr):
    if not hasattr(expr, "is_expression_type"):
        return sym_number(expr)
    if expr.is_variable_type():
        return sp.Symbol(expr.name)
    if not expr.is_expression_type():
        return sym_number(value(expr))
    return expr._apply_operation([pyomo_symbolic(a) for a in expr.args])


def source_equivalence(name, model):
    source = (ROOT / f"instances/gms/{name}.gms").read_text()
    def rename(var):
        if name == "risk2bpb" and var in {"x462", "x463", "x464"}:
            return f"x{int(var[1:])-1}"
        return var
    def convert(node):
        if isinstance(node, ast.Constant):
            return sym_number(node.value)
        if isinstance(node, ast.Name):
            return sp.Symbol(rename(node.id))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -convert(node.operand)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return convert(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = convert(node.left), convert(node.right)
            if isinstance(node.op, ast.Add): return a + b
            if isinstance(node.op, ast.Sub): return a - b
            if isinstance(node.op, ast.Mult): return a * b
            if isinstance(node.op, ast.Pow): return a ** b
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sqr":
            assert len(node.args) == 1
            return convert(node.args[0]) ** 2
        raise ValueError(ast.dump(node))
    def expression(text):
        return convert(ast.parse(" ".join(text.split()), mode="eval").body)
    equations = re.findall(r"\be(\d+)\.\.(.*?)=([ELG])=(.*?);", source, re.S)
    rows = list(model.component_data_objects(Constraint))
    assert len(equations) == len(rows) + 1
    for number, lhs, sense, rhs in equations:
        gams = expression(lhs) - expression(rhs)
        if number == "1":
            objvar = sp.Symbol("objvar")
            coefficient = gams.coeff(objvar)
            assert coefficient in (-1, 1)
            gams_objective = sp.expand(-(gams - coefficient * objvar) / coefficient)
            assert sp.expand(gams_objective - pyomo_symbolic(model.obj.expr)) == 0
            continue
        row = getattr(model, f"e{int(number)-1}")
        bound = row.upper if sense in ("E", "L") else row.lower
        assert (sense == "E") == row.equality
        assert (sense != "L" or row.has_ub()) and (sense != "G" or row.has_lb())
        expected = pyomo_symbolic(row.body) - sym_number(value(bound))
        assert sp.expand(gams - expected) == 0, (name, number)
    declared = re.search(r"(?m)^Variables\s+(.*?);", source, re.S).group(1)
    names = re.findall(r"\b(?:x\d+|b\d+|objvar)\b", declared)
    domains = {n: "R" for n in names}
    bounds = {n: [None, None] for n in names}
    for typ, variables in re.findall(r"(?m)^(Positive|Binary) Variables\s+(.*?);", source, re.S):
        for n in re.findall(r"\b(?:x\d+|b\d+)\b", variables):
            if typ == "Binary": domains[n] = "B"; bounds[n] = [Fraction(0), Fraction(1)]
            else: bounds[n][0] = Fraction(0)
    for n, kind, raw in re.findall(r"\b(\w+)\.(lo|up|fx)\s*=\s*([^;]+);", source):
        v = Fraction(expression(raw))
        if kind in ("lo", "fx"): bounds[n][0] = v
        if kind in ("up", "fx"): bounds[n][1] = v
    assert set(map(rename, set(names) - {"objvar"})) == {v.name for v in model.component_data_objects(Var)}
    for n in names:
        if n == "objvar": continue
        var = getattr(model, rename(n))
        assert domains[n] == ("B" if var.is_binary() else "R")
        assert bounds[n] == [None if var.lb is None else Fraction(var.lb),
                             None if var.ub is None else Fraction(var.ub)], (name, n)
    return {"constraints": len(rows), "variables": len(names)-1,
            "objective": "equal", "bounds_and_domains": "equal",
            "semantics": "exact binary64 literals in source expressions",
            "gams_row_mapping": "e(k+1) -> Pyomo e(k)",
            "gams_variable_mapping": "x462..x464 -> x461..x463" if name == "risk2bpb" else "identity"}


def verify_clay_optimality(viprchk):
    from certify.driver import check_certificate

    model_path = ROOT / "instances/py/clay0204m.py"
    certdir = ROOT / "results/cert/clay0204m"
    witness_path = OUT / "clay0204m_primal_witness.json"
    output_path = OUT / "clay0204m_optimality.json"
    paths = [model_path, ROOT / "instances/gms/clay0204m.gms", witness_path]
    paths += [certdir / name for name in ("lemma.json", "master.lp", "master_complete.vipr")]
    paths += sorted((ROOT / "certify").glob("*.py"))
    paths += sorted((ROOT / "lbesh").glob("*.py"))
    paths += [ROOT / "pyproject.toml", ROOT / "uv.lock"]
    if viprchk:
        paths.append(Path(viprchk).resolve())

    def fingerprints():
        return {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}

    before = fingerprints()
    witness = json.loads(witness_path.read_text())
    model = runpy.run_path(str(model_path))["model"]
    variables = {name: Fraction(q) for name, q in witness["variables"].items()}
    feasible = not feasibility(model, variables)
    objective = exact_value(model.obj.expr, variables)
    lower = check_certificate(str(model_path), str(certdir), viprchk=viprchk,
                              verbose=False, require_vipr=True)
    after = fingerprints()
    accepted = (feasible and lower.get("ok") is True and lower.get("sense") == 1
                and Fraction(lower["certified_bound_original_sense"]) == objective
                and before == after)
    record = {"instance": "clay0204m", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "status": "exact_optimum_verified" if accepted else "not_verified",
              "model_semantics": lower.get("model_semantics"),
              "source_sha256": before[str(model_path)],
              "input_and_checker_sha256": before,
              "inputs_and_checker_unchanged_during_check": before == after,
              "primal_witness": {"path": str(witness_path), "feasible_exactly": feasible,
                                 "objective": str(objective)},
              "complete_lower_bound_check": lower}
    if accepted:
        record["exact_optimum"] = str(objective)
    output_path.write_text(json.dumps(record, indent=2) + "\n")
    if not accepted:
        raise RuntimeError(f"exact optimality was not established; see {output_path}")
    print(f"clay0204m: complete lower-bound replay and exact primal witness establish optimum {objective}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-certificate", action="store_true",
                        help="also join complete clay0204m certificate replay with the exact primal witness")
    parser.add_argument("--viprchk", help="optional corroborating external VIPR checker executable")
    args = parser.parse_args()
    if args.viprchk and not args.verify_certificate:
        parser.error("--viprchk requires --verify-certificate")
    OUT.mkdir(exist_ok=True)
    report = {"scope": "saved 2026-09-12 outputs; source comparison and exact primal checks", "cases": {}}
    for name, solver in [("clay0204m", "sbb"), ("risk2bpb", "shot")]:
        model = runpy.run_path(str(ROOT / f"instances/py/{name}.py"))["model"]
        vals = listing_values(ROOT / f"baseline/lst/{name}.{solver}.lst")
        mapped = {v.name: vals[f"x{int(v.name[1:])+1}" if name == "risk2bpb" and v.name in {"x461", "x462", "x463"} else v.name]
                  for v in model.component_data_objects(Var)}
        failures = feasibility(model, mapped)
        case = {"source_equivalence": source_equivalence(name, model),
                "historical_status_csv": (ROOT / f"baseline/out/{name}.{solver}.txt").read_text().strip(),
                "printed_vector_failures": failures,
                "warning": "listing levels are rounded; small residuals do not establish solver infeasibility"}
        if name == "clay0204m":
            witness = listing_values(ROOT / "baseline/lst/clay0204m.baron.lst")
            witness = {v.name: Fraction(0) if abs(witness[v.name]) < Fraction(1, 10000) else witness[v.name]
                       for v in model.component_data_objects(Var)}
            assert not feasibility(model, witness)
            obj = exact_value(model.obj.expr, witness)
            assert obj == 6545
            artifact = {"instance": name, "semantics": "exact binary64 coefficients, rational variable values",
                        "source": "BARON printed levels, values below 1e-4 in absolute value replaced by zero",
                        "objective": str(obj), "variables": {n: str(x) for n, x in witness.items()}}
            (OUT / "clay0204m_primal_witness.json").write_text(json.dumps(artifact, indent=2) + "\n")
            case["exact_feasible_witness_objective"] = str(obj)
        case["source_sha256"] = {f"{kind}": hashlib.sha256((ROOT / f"instances/{kind}/{name}.{kind}").read_bytes()).hexdigest()
                                 for kind in ("gms", "py")}
        report["cases"][name] = case
    (OUT / "audit.json").write_text(json.dumps(report, indent=2) + "\n")
    for name, case in report["cases"].items():
        large = [r for r in case["printed_vector_failures"] if r[1] != "integrality" and Fraction(r[2]) > Fraction(1, 1000)]
        print(f"{name}: source equivalence passed; large printed-vector violations: {large}")
    print("clay0204m: exact feasible rational witness, objective 6545")
    if args.verify_certificate:
        verify_clay_optimality(args.viprchk)


if __name__ == "__main__":
    main()
