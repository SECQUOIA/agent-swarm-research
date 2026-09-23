"""Checkable finite bounds for convex MINLP under exact expression semantics.

The numerical OA solver proposes points and slopes. The producer reconstructs
rows from the exact loaded expression tree, rounds valid supporting cuts, and
writes a rational MILP. The checker independently reconstructs those objects,
checks every cut and master identity, and replays the discrete proof using
certify.vipr. External viprchk is optional corroboration. Only a complete
successful check exposes a certified bound; partial checks have a separate
status. See notes/certified-minlp-soundness.md for hypotheses and trust scope.
"""
from __future__ import annotations

import json, math, os, re, sys, time, hashlib, importlib.util
from fractions import Fraction
from collections import OrderedDict
from types import SimpleNamespace

import pyomo.environ as pe

from .convexity import certify_constraint, certify, frac, AFFINE, CONVEX, CONCAVE
from .safecut import SafeCutter
from .exact_model import exact_repn, exact_constant, exact_constraint_rows

INF = float("inf")


def load_instance(path):
    """Load a MINLPLib Pyomo file. Some converted files contain a spurious
    indentation before a top-level assignment (e.g. batch.py); such lines
    are dedented before execution."""
    import re
    sys.setrecursionlimit(100000)
    src = open(path).read()
    src = re.sub(r"^[ \t]+(m\.\w+ = )", r"\1", src, flags=re.M)
    ns = {"__name__": "inst_" + hashlib.md5(path.encode()).hexdigest()[:8]}
    code = compile(src, path, "exec")
    exec(code, ns)
    return ns["m"]


def var_list(m):
    return list(m.component_data_objects(pe.Var, active=True, descend_into=True))


def linear_rows_exact(m):
    """Exact rational linear rows (name, {varname: coef}, lb, ub) and the
    list of nonlinear constraints."""
    rows, nl = [], []
    for con in m.component_data_objects(pe.Constraint, active=True, descend_into=True):
        repn = exact_repn(con.body, quadratic=False)
        if repn.is_nonlinear():
            nl.append(con)
            continue
        c0 = frac(repn.constant)
        lb = None if con.lower is None else exact_constant(con.lower) - c0
        ub = None if con.upper is None else exact_constant(con.upper) - c0
        coefs = OrderedDict()
        for v, c in zip(repn.linear_vars, repn.linear_coefs):
            coefs[v.name] = coefs.get(v.name, Fraction(0)) + frac(c)
        coefs = OrderedDict((v, c) for v, c in coefs.items() if c)
        rows.append((con.name, coefs, lb, ub))
    return rows, nl


def rational_bounds(m, rows, rounds=20):
    """Exact interval propagation of the linear rows on the rational box."""
    vars_ = {v.name: v for v in var_list(m)}
    box = {}
    for name, v in vars_.items():
        lb = None if v.lower is None else exact_constant(v.lower)
        ub = None if v.upper is None else exact_constant(v.upper)
        if v.is_fixed():
            lb = ub = frac(v.value)
        if v.is_binary():
            lb = max(lb, Fraction(0)) if lb is not None else Fraction(0)
            ub = min(ub, Fraction(1)) if ub is not None else Fraction(1)
        box[name] = [lb, ub]
    for _ in range(rounds):
        changed = False
        for name, coefs, lb, ub in rows:
            if not coefs:
                continue
            los, his = {}, {}
            for vn, c in coefs.items():
                if c == 0:
                    continue
                l, u = box[vn]
                if l is None or u is None:
                    a = -INF if (c > 0 and l is None) or (c < 0 and u is None) else (c * (l if c > 0 else u))
                    b = INF if (c > 0 and u is None) or (c < 0 and l is None) else (c * (u if c > 0 else l))
                    los[vn], his[vn] = a, b
                else:
                    a, b = c * l, c * u
                    los[vn], his[vn] = min(a, b), max(a, b)
            slo = sum(los.values()) if all(x != -INF for x in los.values()) else -INF
            shi = sum(his.values()) if all(x != INF for x in his.values()) else INF
            n_inf_lo = sum(1 for x in los.values() if x == -INF)
            n_inf_hi = sum(1 for x in his.values() if x == INF)
            for vn, c in coefs.items():
                if c == 0:
                    continue
                v = vars_[vn]
                # rest_lo = sum of los except vn
                if los[vn] == -INF:
                    rest_lo = slo if n_inf_lo > 1 else (sum(x for k, x in los.items() if k != vn))
                    rest_lo = -INF if n_inf_lo > 1 else rest_lo
                else:
                    rest_lo = -INF if n_inf_lo > 0 else slo - los[vn]
                if his[vn] == INF:
                    rest_hi = INF if n_inf_hi > 1 else (sum(x for k, x in his.items() if k != vn))
                else:
                    rest_hi = INF if n_inf_hi > 0 else shi - his[vn]
                l, u = box[vn]
                if ub is not None and rest_lo != -INF:
                    val = (ub - rest_lo) / c
                    if c > 0 and (u is None or val < u):
                        if v.is_integer(): val = Fraction(math.floor(val))
                        box[vn][1] = val; changed = True
                    elif c < 0 and (l is None or val > l):
                        if v.is_integer(): val = Fraction(math.ceil(val))
                        box[vn][0] = val; changed = True
                l, u = box[vn]
                if lb is not None and rest_hi != INF:
                    val = (lb - rest_hi) / c
                    if c > 0 and (l is None or val > l):
                        if v.is_integer(): val = Fraction(math.ceil(val))
                        box[vn][0] = val; changed = True
                    elif c < 0 and (u is None or val < u):
                        if v.is_integer(): val = Fraction(math.floor(val))
                        box[vn][1] = val; changed = True
        if not changed:
            break
    return box


def prepare_model(m):
    """Extract the one exact model used to construct and to check every cut.

    The numerical OA solver receives a separate model and supplies proposals
    only. No coefficients or row decompositions from that solver are trusted.
    """
    from lbesh.structure import NLRow
    from pyomo.core.expr import numeric_expr as NE
    from pyomo.core.expr.visitor import identify_variables
    from pyomo.gdp import Disjunct, Disjunction
    for ctype in (Disjunct, Disjunction, pe.LogicalConstraint, pe.SOSConstraint):
        if any(True for _ in m.component_data_objects(ctype, active=True, descend_into=True)):
            raise ValueError(f"unsupported active component: {ctype.__name__}")
    objs = list(m.component_data_objects(pe.Objective, active=True))
    if len(objs) != 1:
        raise ValueError("exactly one active objective is required")
    variables = var_list(m)
    names = [v.name for v in variables]
    if len(names) != len(set(names)):
        raise ValueError("duplicate variable names")
    for name in names:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"unsupported LP variable name: {name}")
    if "_lbesh_epigraph" in names or "objconst" in names:
        raise ValueError("variable name collides with a reserved master variable")
    rows, nlcons = linear_rows_exact(m)
    for name, coefs, lb, ub in rows:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"unsupported LP row name: {name}")
        if not coefs and ((lb is not None and lb > 0) or (ub is not None and ub < 0)):
            raise ValueError(f"infeasible constant row: {name}; no finite-bound certificate produced")
    nlrows = {}
    for con in nlcons:
        kind, c = certify_constraint(con)
        if kind not in ("convex_row", "concave_row", "affine"):
            raise ValueError(f"uncertified row {con.name}: {kind}: {c.why}")
        for row in exact_constraint_rows(con):
            if row.name in nlrows:
                raise ValueError(f"duplicate nonlinear row name: {row.name}")
            nlrows[row.name] = row
    sense = 1 if objs[0].sense == pe.minimize else -1
    oc = certify(objs[0].expr)
    allowed = (AFFINE, CONVEX) if sense == 1 else (AFFINE, CONCAVE)
    if oc.curv not in allowed:
        raise ValueError(f"uncertified objective: {oc.why}")
    repn = exact_repn(objs[0].expr)
    epi = None
    if repn.is_nonlinear():
        epi = pe.Var(initialize=0)
        m.add_component("_lbesh_epigraph", epi)
        expr = repn.nonlinear_expr if sense == 1 else NE.NegationExpression((repn.nonlinear_expr,))
        func = SimpleNamespace(expr=expr, vars=list(identify_variables(expr, include_fixed=False)))
        nlrows["objective_epi"] = NLRow("objective_epi", func,
            list(repn.linear_vars) + [epi],
            [sense*c for c in repn.linear_coefs] + [Fraction(-1)], sense*repn.constant)
        obj_coefs = OrderedDict([(epi.name, Fraction(1))])
        obj_const = Fraction(0)
    else:
        obj_coefs = OrderedDict((v.name, sense*c) for v, c in zip(repn.linear_vars, repn.linear_coefs) if c)
        obj_const = sense*repn.constant
    box = rational_bounds(m, rows)
    for name, (lb, ub) in box.items():
        if lb is not None and ub is not None and lb > ub:
            raise ValueError(f"empty rational box at {name}; no finite-bound certificate produced")
    return SimpleNamespace(model=m, rows=rows, nlrows=nlrows, box=box,
        sense=sense, epi=epi, obj_coefs=obj_coefs, obj_const=obj_const,
        variables=var_list(m))


def fstr(q: Fraction) -> str:
    """Exact decimal string of a rational with denominator 2^a 5^b; else 'p/q'."""
    d = q.denominator
    a = b = 0
    while d % 2 == 0:
        d //= 2; a += 1
    while d % 5 == 0:
        d //= 5; b += 1
    if d != 1:
        return f"{q.numerator}/{q.denominator}"
    k = max(a, b)
    scale = 10 ** k
    n = q.numerator * (scale // q.denominator)
    sign = "-" if n < 0 else ""
    n = abs(n)
    s = str(n).rjust(k + 1, "0")
    if k == 0:
        return sign + s
    return sign + s[:-k] + "." + s[-k:]


def write_lp(path, varnames, vtypes, box, rows, cuts, obj_coefs, obj_const):
    """rows: list of (name, {var: Fraction}, lb, ub); cuts: list of (name, {var: Fraction}, b) meaning sum a x + b <= 0."""
    L = ["\\ certified rational master MILP", "Minimize", " obj: " + " ".join(f"{'+' if c >= 0 else '-'} {fstr(abs(c))} {v}" for v, c in obj_coefs.items()) + (f" + {fstr(obj_const)} objconst" if obj_const != 0 else ""), "Subject To"]
    for name, coefs, lb, ub in rows:
        terms = " ".join(f"{'+' if c >= 0 else '-'} {fstr(abs(c))} {v}" for v, c in coefs.items())
        if not coefs:
            continue
        if lb is not None and ub is not None and lb == ub:
            L.append(f" {name}: {terms} = {fstr(lb)}")
        else:
            if lb is not None:
                L.append(f" {name}_lb: {terms} >= {fstr(lb)}")
            if ub is not None:
                L.append(f" {name}_ub: {terms} <= {fstr(ub)}")
    for name, coefs, b in cuts:
        terms = " ".join(f"{'+' if c >= 0 else '-'} {fstr(abs(c))} {v}" for v, c in coefs.items())
        L.append(f" {name}: {terms} <= {fstr(-b)}")
    L.append("Bounds")
    for v in varnames:
        lb, ub = box[v]
        lo = "-inf" if lb is None else fstr(lb)
        hi = "+inf" if ub is None else fstr(ub)
        L.append(f" {lo} <= {v} <= {hi}")
    if obj_const != 0:
        L.append(" objconst = 1")
    gen = [v for v in varnames if vtypes[v] == "I"]
    bins = [v for v in varnames if vtypes[v] == "B"]
    if gen:
        L.append("General"); L.append(" " + " ".join(gen))
    if bins:
        L.append("Binary"); L.append(" " + " ".join(bins))
    L.append("End")
    text = "\n".join(L) + "\n"
    if path is not None:
        with open(path, "w") as f:
            f.write(text)
    return text


def build_certificate(inst_path, outdir, time_limit=300, threads=4, verbose=False, sig_digits=12):
    """Use numerical cut proposals to construct a master for the exact model."""
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    exact = prepare_model(load_instance(inst_path))
    summary = dict(instance=os.path.basename(inst_path), time_limit=time_limit,
                   convexity={"certified": True}, model_semantics="pyomo-expression-rationals-v1")
    # Numerical search has its own model; its extraction and arithmetic are untrusted.
    numerical = load_instance(inst_path)
    for v in var_list(numerical):
        lb, ub = exact.box[v.name]
        if lb is not None:
            fl = float(lb)
            if Fraction(fl) > lb:
                fl = math.nextafter(fl, -INF)
            if v.lb is None or fl > v.lb:
                v.setlb(fl)
        if ub is not None:
            fu = float(ub)
            if Fraction(fu) < ub:
                fu = math.nextafter(fu, INF)
            if v.ub is None or fu < v.ub:
                v.setub(fu)
    from lbesh.solver import LBESH
    solver = LBESH(numerical, formulation="hull", nlp_solver="ipopt", threads=threads,
                   time_limit=time_limit, verbose=verbose)
    st = solver.solve(single_tree=False)
    summary["oa"] = dict(status=st.status, lb=st.lb, ub=st.ub, cuts=st.cuts,
                         nlps=st.nlp_solves, time=st.time_total)
    exact_vars = {v.name: v for v in exact.variables}
    numerical_names = {id(v): v.name for v in solver.prob.variables}
    boxid = {id(v): tuple(exact.box[v.name]) for v in exact.variables}
    cutters, lemmas, cuts, seen = {}, [], [], set()
    failed = 0
    for _, _, _, proposed_row, coef, const, point in solver.cut_log:
        row = exact.nlrows.get(proposed_row.name)
        if row is None:
            failed += 1
            continue
        try:
            z = {id(exact_vars[numerical_names[vid]]): val for vid, val in point.items()
                 if vid in numerical_names and numerical_names[vid] in exact_vars}
            row_ids = {id(v) for v in row.all_vars()}
            slopes = {id(exact_vars[numerical_names[vid]]): val for vid, val in coef.items()
                      if vid in numerical_names and numerical_names[vid] in exact_vars
                      and id(exact_vars[numerical_names[vid]]) in row_ids}
            key = (row.name, tuple((v.name, str(z[id(v)])) for v in row.all_vars()))
            if key in seen:
                continue
            seen.add(key)
            if row.name not in cutters:
                cutters[row.name] = SafeCutter(row, boxid, sig_digits=sig_digits)
            result = cutters[row.name].safe_cut(z, slopes, const)
            if result is None:
                failed += 1
                continue
        except (ValueError, TypeError, KeyError, ArithmeticError):
            failed += 1
            continue
        a, b, info = result
        name = f"cut{len(cuts)+1}"
        coefs = OrderedDict((v.name, a[id(v)]) for v in row.all_vars() if a.get(id(v), 0))
        cuts.append((name, coefs, b))
        lemmas.append(dict(name=name, row=row.name,
            z={v.name: str(info["z"][id(v)]) for v in row.all_vars()},
            a={vn: str(c) for vn, c in coefs.items()}, b=str(b)))
    summary["cuts"] = dict(total_logged=len(solver.cut_log), unique=len(seen), safe=len(cuts), failed=failed)
    varnames = [v.name for v in exact.variables]
    vtypes = {v.name: ("B" if v.is_binary() else "I" if v.is_integer() else "C") for v in exact.variables}
    lp = write_lp(os.path.join(outdir, "master.lp"), varnames, vtypes, exact.box,
                  exact.rows, cuts, exact.obj_coefs, exact.obj_const)
    summary.update(lp_sha256=hashlib.sha256(lp.encode()).hexdigest(), sense=exact.sense,
        rows_linear=len(exact.rows), rows_nonlinear=len(exact.nlrows), status="master_written",
        time_total=time.time()-t0)
    with open(os.path.join(outdir, "lemma.json"), "w") as f:
        json.dump(dict(instance=os.path.basename(inst_path), sig_digits=sig_digits,
            model_semantics="pyomo-expression-rationals-v1",
            source_sha256=hashlib.sha256(open(inst_path, "rb").read()).hexdigest(),
            epigraph=exact.epi is not None, lemmas=lemmas), f, indent=0)
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, default=str)
    return summary


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("instance"); ap.add_argument("outdir"); ap.add_argument("--timelimit", type=float, default=300)
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    s = build_certificate(a.instance, a.outdir, a.timelimit, a.threads, a.v)
    print(json.dumps({k: s[k] for k in s if k != "convexity"}, default=str))


# ---------------------------------------------------------------------------
# Checker
# ---------------------------------------------------------------------------
def _unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_certificate(inst_path, certdir, viprchk=None, verbose=True, vipr_path=None,
                      require_vipr=True):
    """Check a finite bound, or explicitly request nonlinear/master checks only.

    `ok` is true only after complete exact proof replay. With require_vipr=False,
    `partial_ok` reports the weaker check and no certified bound is returned.
    An optional external viprchk is corroboration, never the proof authority.
    Malformed/unsupported certificates fail closed. Saved artifacts are read-only.
    """
    report = dict(instance=os.path.basename(inst_path), checks=[], ok=False,
                  partial_ok=False, status="rejected", model_semantics="pyomo-expression-rationals-v1")
    try:
        _check_certificate(inst_path, certdir, viprchk, vipr_path, require_vipr, report)
    except Exception as exc:
        report["ok"] = False
        report["status"] = "rejected"
        report["checks"].append(("input_or_check", "", "FAIL", f"{type(exc).__name__}: {exc}"[:1000]))
        for key in ("certified_master_lb", "certified_bound_original_sense", "verified_range"):
            report.pop(key, None)
    if verbose:
        for check in report["checks"]:
            print(check)
    return report


def _check_certificate(inst_path, certdir, viprchk, vipr_path, require_vipr, report):
    with open(os.path.join(certdir, "lemma.json")) as f:
        lemma = json.load(f, object_pairs_hook=_unique_json)
    if not isinstance(lemma, dict) or not isinstance(lemma.get("lemmas"), list):
        raise ValueError("lemma file must contain a list of lemmas")
    sig = lemma.get("sig_digits")
    if type(sig) is not int or sig < 1:
        raise ValueError("sig_digits must be a positive integer")
    if lemma.get("model_semantics", report["model_semantics"]) != report["model_semantics"]:
        raise ValueError("unsupported model semantics")
    if "source_sha256" in lemma:
        with open(inst_path, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != lemma["source_sha256"]:
                raise ValueError("source model hash differs")
    exact = prepare_model(load_instance(inst_path))
    report["sense"] = exact.sense
    report["checks"].append(("convexity_and_model", "all", "OK", "exact expression semantics"))
    by_name = {v.name: v for v in exact.variables}
    boxid = {id(v): tuple(exact.box[v.name]) for v in exact.variables}
    cutters, cuts, names = {}, [], set()
    for entry in lemma["lemmas"]:
        name = entry["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) or name in names:
            raise ValueError("invalid or duplicate cut name")
        names.add(name)
        row = exact.nlrows.get(entry["row"])
        if row is None:
            raise ValueError(f"unknown nonlinear row: {entry['row']}")
        rowvars = {v.name for v in row.all_vars()}
        if not set(entry["a"]) <= rowvars or not rowvars <= set(entry["z"]) or not set(entry["z"]) <= set(by_name):
            raise ValueError(f"cut {name}: variable mismatch")
        z = {id(by_name[vn]): Fraction(val) for vn, val in entry["z"].items()}
        a = {vn: Fraction(val) for vn, val in entry["a"].items()}
        b = Fraction(entry["b"])
        if row.name not in cutters:
            cutters[row.name] = SafeCutter(row, boxid, sig_digits=sig)
        bound = _verify_given_cut(cutters[row.name], row, z, a, by_name)
        if bound is None or b > bound:
            raise ValueError(f"cut {name}: intercept or supporting-point conditions fail")
        cuts.append((name, OrderedDict((vn, c) for vn, c in a.items() if c), b))
    report["checks"].append(("lemmas", f"{len(cuts)} cuts", "OK", ""))
    varnames = list(by_name)
    vtypes = {v.name: ("B" if v.is_binary() else "I" if v.is_integer() else "C") for v in exact.variables}
    regenerated = write_lp(None, varnames, vtypes, exact.box, exact.rows, cuts, exact.obj_coefs, exact.obj_const)
    with open(os.path.join(certdir, "master.lp")) as f:
        same = regenerated == f.read()
    report["checks"].append(("lp_regeneration", "byte-identical", "OK" if same else "FAIL", ""))
    if not same:
        return
    report["partial_ok"] = True
    if not require_vipr:
        report["status"] = "partial"
        return
    path = vipr_path or os.path.join(certdir, "master_complete.vipr")
    if not os.path.isfile(path):
        raise ValueError("complete verification requires a VIPR proof")
    problems = vipr_compare(path, varnames, vtypes, exact.box, exact.rows, cuts, exact.obj_coefs, exact.obj_const)
    report["checks"].append(("vipr_problem_matches_master", "", "OK" if not problems else "FAIL", "; ".join(problems)[:1000]))
    if problems:
        return
    from .vipr import validate_vipr, check_vipr_output
    proof = validate_vipr(path)
    report["proof"] = proof
    report["checks"].append(("vipr_exact_replay", "", "OK" if proof["ok"] else "FAIL", proof.get("error", "")))
    if not proof["ok"]:
        return
    if proof.get("sense") != "min" or proof.get("lower_bound") in (None, "-inf", "inf"):
        raise ValueError("a finite minimization lower bound is required")
    lo = Fraction(proof["lower_bound"])
    if viprchk is not None:
        import subprocess
        result = subprocess.run([viprchk, path], capture_output=True, text=True)
        accepted, diagnostic = check_vipr_output(result.returncode, result.stdout, proof)
        report["checks"].append(("external_viprchk", "", "OK" if accepted else "FAIL", diagnostic))
        if not accepted:
            return
    report.update(ok=True, status="verified", certified_master_lb=str(lo),
                  certified_bound_original_sense=str(exact.sense*lo),
                  verified_range=[str(lo), proof.get("upper_bound")])


def vipr_parse_problem(path):
    from .vipr import parse_problem
    return parse_problem(path)


def vipr_compare(vipr_path, varnames, vtypes, box, rows, cuts, obj_coefs, obj_const):
    """Multiset comparison of the VIPR problem section with the rational
    master (rows, cuts, bounds, objective, integrality). Returns a list of
    discrepancies (empty when identical)."""
    from collections import Counter
    names, ints, sense, obj, cons = vipr_parse_problem(vipr_path)
    problems = []
    if sense != "min":
        problems.append("objective sense")
    expected_names = set(varnames) | ({"objconst"} if obj_const != 0 else set())
    if set(names) != expected_names:
        # SCIP's transformed problem adds one prefix to every variable.
        # Preserve genuine source names beginning with t_ and require a bijection.
        if all(n.startswith("t_") for n in names):
            names = [n[2:] for n in names]
    if len(names) != len(set(names)):
        return ["duplicate or ambiguous variable names"]
    if set(names) != expected_names:
        problems.append(f"variable set differs: {sorted(set(names) ^ expected_names)[:5]}")
        return problems
    ints_names = {names[i] for i in ints}
    exp_ints = {v for v in varnames if vtypes[v] in ("I", "B")}
    if ints_names != exp_ints:
        problems.append(f"integer set differs: {sorted(ints_names ^ exp_ints)[:5]}")
    objv = {names[i]: c for i, c in obj.items() if c != 0}
    expobj = {v: c for v, c in obj_coefs.items() if c != 0}
    if obj_const != 0:
        expobj["objconst"] = obj_const
    if objv != expobj:
        problems.append("objective differs")
    def normalize(sgn, rhs, items):
        """Scale-invariant form of a row (SCIP may scale rows on input): divide
        by the absolute value of the first coefficient in sorted variable order.
        Positive scaling keeps the sense; a negative scale would flip it, which is
        only value-preserving for equalities, so L/G rows are normalized by the
        absolute value and keep their sense (a negatively scaled L row would
        appear as a different G row and not match)."""
        if not items:
            return (sgn, rhs, ())
        s0 = abs(items[0][1])
        norm = tuple((v, c / s0) for v, c in items)
        return (sgn, rhs / s0, norm)
    def canon(sgn, rhs, coefs):
        items = tuple(sorted((names[i], c) for i, c in coefs.items() if c != 0))
        return normalize(sgn, rhs, items)
    got = Counter(canon(sgn, rhs, coefs) for (_, sgn, rhs, coefs) in cons)
    exp = Counter()
    for name, coefs, lb, ub in rows:
        if not coefs:
            continue
        items = tuple(sorted((v, c) for v, c in coefs.items() if c != 0))
        if lb is not None and ub is not None and lb == ub:
            exp[normalize("E", lb, items)] += 1
        else:
            if lb is not None: exp[normalize("G", lb, items)] += 1
            if ub is not None: exp[normalize("L", ub, items)] += 1
    for name, coefs, b in cuts:
        items = tuple(sorted((v, c) for v, c in coefs.items() if c != 0))
        exp[normalize("L", -b, items)] += 1
    for v in varnames:
        lb, ub = box[v]
        if lb is not None: exp[normalize("G", lb, ((v, Fraction(1)),))] += 1
        if ub is not None: exp[normalize("L", ub, ((v, Fraction(1)),))] += 1
    if obj_const != 0:
        exp[normalize("G", Fraction(1), (("objconst", Fraction(1)),))] += 1
        exp[normalize("L", Fraction(1), (("objconst", Fraction(1)),))] += 1
    missing = exp - got; extra = got - exp
    if missing:
        problems.append(f"{sum(missing.values())} master constraints missing from VIPR")
    if extra:
        problems.append(f"{sum(extra.values())} VIPR constraints not in master")
    return problems


def _verify_given_cut(sc: SafeCutter, row, zvals, a_by_name, vars_by_name):
    """Rigorous lower bound of phi(x) = g(x) + l^T x + c - a^T x over the box
    for the given rational slopes a (dict by var name). Returns Fraction or None."""
    import mpmath
    from mpmath import iv
    from .safecut import _iv_from_frac, mpf_to_frac_down, PREC_DPS
    # the linearization point must lie in the box (convexity gives the
    # supporting inequality only there)
    for v in row.all_vars():
        lb, ub = sc.box[id(v)]
        q = Fraction(zvals[id(v)])
        if (lb is not None and q < Fraction(lb)) or (ub is not None and q > Fraction(ub)):
            return None
    z = [Fraction(zvals[id(v)]) for v in row.func.vars]  # exact rationals
    fv, gv = sc.enclose(z)
    a = {id(vars_by_name[vn]): q for vn, q in a_by_name.items()}
    from .safecut import _ivprec, PREC_BITS
    with _ivprec(PREC_BITS):
        phi = fv + _iv_from_frac(Fraction(row.const))
        lin_at_z = Fraction(0)
        for v, c in zip(row.lin_vars, row.lin_coefs):
            lin_at_z += frac(c) * Fraction(zvals[id(v)])
        a_at_z = Fraction(0)
        for vid, q in a.items():
            a_at_z += q * Fraction(zvals[vid])
        phi = phi + _iv_from_frac(lin_at_z - a_at_z)
        allvars = {}
        for v in row.func.vars: allvars[id(v)] = v
        for v in row.lin_vars: allvars[id(v)] = v
        lcoef = {}
        for v, c in zip(row.lin_vars, row.lin_coefs):
            lcoef[id(v)] = lcoef.get(id(v), Fraction(0)) + frac(c)
        gidx = {id(v): i for i, v in enumerate(row.func.vars)}
        worst = iv.mpf(0)
        for vid, v in allvars.items():
            d = iv.mpf(0)
            if vid in gidx:
                d = d + gv[gidx[vid]]
            d = d + _iv_from_frac(lcoef.get(vid, Fraction(0)) - a.get(vid, Fraction(0)))
            zj = Fraction(zvals[vid])
            lb, ub = sc.box[vid]
            lb = None if lb is None else Fraction(lb)
            ub = None if ub is None else Fraction(ub)
            if lb is None and ub is None:
                if d.a == 0 and d.b == 0:
                    continue
                return None
            if ub is None:
                if d.a < 0:
                    return None
                t1 = d * _iv_from_frac(zj - lb)
                worst = worst + iv.mpf([t1.a, t1.b])
                continue
            if lb is None:
                if d.b > 0:
                    return None
                t2 = d * _iv_from_frac(zj - ub)
                worst = worst + iv.mpf([t2.a, t2.b])
                continue
            t1 = d * _iv_from_frac(zj - lb)
            t2 = d * _iv_from_frac(zj - ub)
            worst = worst + iv.mpf([max(t1.a, t2.a), max(t1.b, t2.b)])
        lower = phi - worst
        return mpf_to_frac_down(lower.a)
