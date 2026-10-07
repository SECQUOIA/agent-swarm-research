#!/usr/bin/env python3
"""R8: independent check of the Part U ablation (evidence/ablation-uncertified.json).

Standard library plus fractions only. No snapshot code, no SymPy, no solver.
Nothing under experiments/ is written. The result is printed as JSON on
stdout (progress on stderr).

A. Counts. Every per-part and per-family count of the ablation is re-derived
   from the JSON ``cuts``. The invalid/material flags are first recomputed
   exactly from the stored ``u1``/``u2`` (binary64 hex) and ``certified``
   (rational string). The counts are compared with the JSON ``summary`` and
   ``meta.key_counts`` and with the numbers stated in
   evidence/ablation-final-summary.md (hard-coded in CLAIMS below).

B. Rows at recorded feasible points (all materially invalid cuts, so every
   cut flagged as removing is covered, and non-removal is checked too).
   - The pool of feasible points is rebuilt from the records: every record of
     the 13 parts with ``original_values`` and ``primal_check.passed`` true,
     pooled by ``model_sha256``, plus the case file ``known_witness_exact``.
   - The exact eliminated row c^T v >= r of each cut is read from its own
     record (``row_certificate.exact``). c and r are re-derived from the
     binding (c = L - sum_j mu_j a_j, r = beta - sum_j mu_j b_j), and L, mu
     are compared with the recorded binary64 direction (a, lambda). This shows
     that r + (U - beta) is the eliminated row with support constant U.
   - The uncertified row c^T v >= r + (U - beta) is evaluated exactly at every
     point; removal means violation > 1e-6*max(1, ||c||_1). Removed sets are
     compared with the JSON. The certified exact row and the exported
     binary64 row are evaluated at the same points (control).
   - Broader control: the certified exact row and exported row of every
     recorded cut of all 13 parts (all 138,000 path cuts, not only the sample)
     at every pooled point of its model.
   - Export census and an independent safety check of every exported row:
     exported_rhs <= r + sum_i min(e_i*lo_i, e_i*hi_i), e = exported - exact,
     with the binding bounds.
   - Case witnesses of the path family: exact feasibility on the case model.

C. Certified minimizers. For a random.Random(2) sample of 100 materially
   invalid exact cuts (and, as an extension, for all of them): U > certified
   exactly; the recorded certified value equals the record's
   ``support_witness.lower_bound``; the certified minimizer lies in the box
   and satisfies the domain rows exactly; the exact objective
   a^T u + lambda^T g(u) at the minimizer, computed from the feature strings
   (Python ast + Fraction) and from the typed feature trees of the support
   witness, equals the certified value.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import ast
import collections
import hashlib
import json
import math
import random
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

P = Path((_PUBLIC_REPO + '/paper-certified-support-cuts'))
ABLATION = P / "evidence" / "ablation-uncertified.json"
MATERIAL = Q(1, 10**6)
VARIANTS = ("u1", "u2")
EXACT_METHODS = ("quadratic_polytope", "quadratic_polygon", "quadratic_star")

# Numbers stated in evidence/ablation-final-summary.md.
# (cuts, d, m, u1_inv, u1_mat, d, m, u1_rem, d, m, u2_inv, u2_mat, d, m, u2_rem, d, m, ctl)
CLAIMS_MINLPLIB = {
    "v3/partA-full": (149, 38, 9, 81, 72, 24, 4, 21, 7, 2, 18, 0, 0, 0, 0, 0, 0, 0),
    "v3/partA-root": (409, 360, 9, 313, 280, 256, 4, 55, 48, 4, 88, 0, 0, 0, 0, 0, 0, 0),
    "v3/partB": (845, 366, 25, 366, 191, 71, 4, 96, 33, 2, 239, 65, 26, 1, 51, 24, 1, 0),
    "v3d/partA-root-rowdir": (413, 360, 9, 313, 280, 256, 4, 55, 48, 4, 88, 0, 0, 0, 0, 0, 0, 0),
    "v3d/partB-root-rowdir": (529, 366, 25, 207, 108, 70, 4, 51, 32, 2, 140, 36, 25, 1, 30, 23, 1, 0),
    "v4/partB2": (1007, 455, 25, 427, 238, 109, 4, 75, 33, 2, 302, 76, 37, 2, 48, 24, 1, 0),
    "v4/partD-root": (1736, 897, 13, 1229, 772, 385, 4, 48, 24, 1, 734, 51, 26, 2, 1, 1, 1, 0),
    "v4/partD-full": (28, 14, 2, 28, 28, 14, 2, 4, 2, 1, 12, 2, 1, 1, 2, 1, 1, 0),
    "ALL": (5116, 1773, 47, 2964, 1969, 765, 12, 405, 105, 7, 1621, 230, 63, 4, 132, 25, 2, 0),
}
# (cuts, d, m, u1_inv, u1_mat, d, m, u1_rem, d, m, u1_kw,
#  u2_inv, u2_mat, d, m, u2_rem, d, m, u2_kw, ctl)
CLAIMS_PATH = {
    "v3/partC": (47, 47, 15, 47, 47, 47, 15, 25, 25, 13, 16, 37, 6, 6, 5, 2, 2, 2, 1, 0),
    "v3d/partC-rowdir": (235, 234, 20, 234, 234, 233, 20, 118, 117, 18, 94, 195, 17, 17, 10, 9, 9, 7, 5, 0),
    "v4/partC2": (170, 169, 19, 167, 166, 165, 19, 89, 89, 15, 67, 134, 15, 15, 8, 6, 6, 6, 2, 0),
    "v4/partC3": (208, 208, 20, 202, 199, 199, 20, 111, 111, 19, 82, 161, 15, 15, 10, 7, 7, 6, 2, 0),
    "v4/partC4": (340, 337, 20, 333, 330, 329, 20, 163, 163, 20, 145, 266, 20, 20, 14, 3, 3, 2, 3, 0),
    "ALL": (1000, 995, 60, 983, 976, 973, 60, 506, 505, 58, 404, 793, 73, 73, 37, 27, 27, 19, 13, 0),
}
CLAIMS_MODELS = {
    "u1_material": {"cvxnonsep_normcon20r": 460, "kall_ellipsoids_tc02b": 399,
                    "kall_ellipsoids_tc05a": 364, "nvs02": 194, "kall_circlespolygons_c1p12": 148,
                    "ex8_1_7": 102, "prob06": 93, "p_ball_10b_5p_2d_m": 87, "ex8_3_4": 46,
                    "ex4_1_8": 39, "kall_circlesrectangles_c6r1": 22, "kriging_peaks-full100": 15},
    "u1_removing": {"nvs02": 129, "prob06": 93, "cvxnonsep_normcon20r": 91,
                    "kall_ellipsoids_tc02b": 52, "ex8_3_4": 32, "ex4_1_8": 6, "p_ball_10b_5p_2d_m": 2},
    "u2_material": {"nvs02": 155, "kall_ellipsoids_tc05a": 32, "kall_circlespolygons_c1p12": 22,
                    "kall_ellipsoids_tc02b": 21},
    "u2_removing": {"nvs02": 129, "kall_ellipsoids_tc02b": 3},
}
CLAIMS_LOWER = {"cuts": 151, "distinct": 43, "models": 3, "arb": 142, "bernstein": 9,
                "u1_material": 151, "u2_material": 151, "u1_removing": 7, "u2_removing": 0,
                "u1_removing_models": ["ex4_1_8"], "control": 0}
CLAIMS_CENSUS = {"minlplib": {"rows": 5267, "rounded": 710, "nonzero_E": 432, "safe": 5267,
                              "max_abs_E": 8.48e-16, "max_rel_shift": 2.17e-16},
                 "path": {"rows": 138000, "rounded": 127678, "nonzero_E": 99862, "safe": 138000,
                          "max_abs_E": 2.12e-16, "max_rel_shift": 2.09e-16}}


def log(*args):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, file=sys.stderr, flush=True)


def hexq(h):
    return Q(float.fromhex(h))


def boundq(s):
    if s in ("inf", "+inf", "Infinity"):
        return math.inf
    if s in ("-inf", "-Infinity"):
        return -math.inf
    return Q(s)


def dkey(e):
    return (e["name"], tuple(e["variables"]), tuple(e["coefficients"]))


# ----------------------------------------------------------------------------
# Exact evaluation of features
# ----------------------------------------------------------------------------

class NotRational(Exception):
    pass


def eval_string(expr, env):
    """Evaluate a SymPy-printed polynomial string exactly (ast + Fraction)."""
    def ev(n):
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            if isinstance(n.op, ast.Mult):
                return a * b
            if isinstance(n.op, ast.Div):
                return a / b
            if isinstance(n.op, ast.Pow):
                if b.denominator != 1:
                    raise NotRational(f"non-integer exponent in {expr}")
                return a ** int(b)
        if isinstance(n, ast.UnaryOp):
            if isinstance(n.op, ast.USub):
                return -ev(n.operand)
            if isinstance(n.op, ast.UAdd):
                return ev(n.operand)
        if isinstance(n, ast.Constant) and type(n.value) is int:
            return Q(n.value)
        if isinstance(n, ast.Name):
            return env[n.id]
        raise NotRational(f"unsupported node {ast.dump(n)[:80]} in {expr}")
    return ev(ast.parse(expr, mode="eval").body)


def eval_tree(tree, point):
    """Evaluate a typed feature tree of the support witness exactly."""
    op = tree[0]
    if op == "variable":
        return point[tree[1]]
    if op == "rational":
        return Q(tree[1])
    if op == "add":
        return sum((eval_tree(t, point) for t in tree[1:]), Q(0))
    if op == "mul":
        out = Q(1)
        for t in tree[1:]:
            out *= eval_tree(t, point)
        return out
    if op == "pow":
        e = Q(tree[2])
        if e.denominator != 1:
            raise NotRational("non-integer power")
        return eval_tree(tree[1], point) ** int(e)
    raise NotRational(f"function {op}")


# ----------------------------------------------------------------------------
# Rows
# ----------------------------------------------------------------------------

def exact_row(cert):
    names = cert["binding"]["variables"]
    terms = [(n, Q(c)) for n, c in zip(names, cert["exact"]["coefficients"]) if c != "0"]
    return terms, Q(cert["exact"]["eliminated_rhs"])


def exported_row(cert):
    names = cert["binding"]["variables"]
    terms = [(n, Q(c)) for n, c in zip(names, cert["exported"]["coefficients"]) if c != 0.0]
    return terms, Q(cert["exported"]["rhs"])


def column_value(name, point):
    if name == "objective_epigraph":
        if point["objective"] is None:
            raise ValueError("no objective value")
        return Q(point["objective"])
    if not (name.startswith("x") and name[1:].isdigit()):
        raise ValueError(f"unknown column {name}")
    i = int(name[1:])
    vals = point["values"]
    if i >= len(vals) or vals[i] is None:
        raise ValueError(f"point lacks column {name}")
    return Q(vals[i])


def activity(terms, point):
    return sum((c * column_value(n, point) for n, c in terms), Q(0))


def binding_check(cut):
    """Re-derive the eliminated row from the binding; compare with the record
    and with the recorded binary64 direction. Returns a list of problems."""
    cert = cut["row_certificate"]
    b = cert["binding"]
    names = b["variables"]
    sup = b["support"]
    problems = []
    beta = Q(sup["rhs"])
    if beta != hexq(cut["support_witness"]["rhs"]):
        problems.append("binding.support.rhs != support_witness.rhs")
    L = {n: Q(v) for n, v in zip(names, sup["linear_coefficients"])}
    mu = [Q(v) for v in sup["multipliers"]]
    if len(mu) != len(b["sides"]):
        problems.append("multiplier count")
    c = dict(L)
    r = beta
    for m, side in zip(mu, b["sides"]):
        for n, a in side["affine_terms"]:
            c[n] = c.get(n, Q(0)) - m * Q(a)
        r -= m * Q(side["rhs"])
    exact = {n: Q(v) for n, v in zip(names, cert["exact"]["coefficients"])}
    if any(c.get(n, Q(0)) != exact.get(n, Q(0)) for n in set(c) | set(exact)):
        problems.append("c != L - sum mu a")
    if r != Q(cert["exact"]["eliminated_rhs"]):
        problems.append("r != beta - sum mu b")
    # direction: a at block variables, lambda = multipliers
    d = len(cut["variables"])
    coef = [Q(x) for x in cut["coefficients"]]
    block = {f"x{i}" for i in cut["variables"]}
    a_expected = {f"x{i}": coef[k] for k, i in enumerate(cut["variables"])}
    if any(L.get(n, Q(0)) != a_expected.get(n, Q(0)) for n in set(L) | block):
        problems.append("linear coefficients != recorded direction a")
    if mu != coef[d:]:
        problems.append("multipliers != recorded lambda")
    if [hexq(h) for h in cut["support_witness"]["model"]["coefficients"]] != coef:
        problems.append("support witness coefficients != cut coefficients")
    if cut["column_names"] != ["v" + n[1:] if n.startswith("x") else n for n in names]:
        problems.append("column names do not map to x<i>")
    return problems


def census_entry(cert):
    exact, exported = cert["exact"], cert["exported"]
    rounded = any(e != "0" for e in exact["rounding_errors"])
    r, E = Q(exact["eliminated_rhs"]), Q(exact["box_compensation"])
    rhs = Q(exported["rhs"])
    recorded_safe = Q(exact["compensated_rhs"]) == r + E and rhs <= r + E
    # independent: exported row implied by exact row on the binding box
    comp = Q(0)
    field_ok = True
    for cx, ex, err, (lo, hi) in zip(exact["coefficients"], exported["coefficients"],
                                     exact["rounding_errors"], cert["binding"]["bounds"]):
        if cx == "0" and ex == 0.0 and err == "0":
            continue
        e = Q(ex) - Q(cx)
        if e != Q(err):
            field_ok = False
        if e == 0:
            continue
        lo, hi = boundq(lo), boundq(hi)
        cand = [e * lo if lo not in (math.inf, -math.inf) else (-math.inf if (e > 0) else math.inf),
                e * hi if hi not in (math.inf, -math.inf) else (math.inf if (e > 0) else -math.inf)]
        m = min(cand)
        if m == -math.inf:
            comp = -math.inf
            break
        comp += m
    independent_safe = comp != -math.inf and rhs <= r + comp
    return {"rounded": rounded, "E": E, "nonzeroE": E != 0, "recorded_safe": recorded_safe,
            "independent_safe": independent_safe, "E_le_bound": comp != -math.inf and E <= comp,
            "field_ok": field_ok,
            "rel_shift": (r + E - rhs) / max(Q(1), abs(r))}


# ----------------------------------------------------------------------------
# Part A: counts from the JSON
# ----------------------------------------------------------------------------

def part_a(d):
    cuts = d["cuts"]
    out = {"flag_mismatches": [], "excess_string_mismatches": 0}
    for i, e in enumerate(cuts):
        if "error" in e:
            out["flag_mismatches"].append((i, "worker error"))
            continue
        cert = Q(e["certified"])
        scale = MATERIAL * max(Q(1), abs(cert))
        for v in VARIANTS:
            U = hexq(e[v])
            ex = U - cert
            if Q(e[f"{v}_excess"]) != ex:
                out["excess_string_mismatches"] += 1
            if (ex > 0) != e[f"{v}_invalid"] or (ex > scale) != e[f"{v}_material"]:
                out["flag_mismatches"].append((i, v))
            if e[f"{v}_material"] != (f"{v}_rows" in e):
                out["flag_mismatches"].append((i, v, "rows presence"))
    return out


def counts(entries, removed_of, ctl_of):
    """removed_of(e, v) -> list of removed sources or None; ctl_of(e, v) -> bool."""
    out = {"cuts": len(entries), "distinct": len({dkey(e) for e in entries}),
           "models": len({e["name"] for e in entries})}
    for v in VARIANTS:
        mat = [e for e in entries if e[f"{v}_material"]]
        rem = [e for e in mat if removed_of(e, v)]
        out[v] = {"invalid": sum(e[f"{v}_invalid"] for e in entries),
                  "material": len(mat), "material_d": len({dkey(e) for e in mat}),
                  "material_m": len({e["name"] for e in mat}),
                  "removing": len(rem), "removing_d": len({dkey(e) for e in rem}),
                  "removing_m": len({e["name"] for e in rem}),
                  "known_witness": sum(any("cases/" in s for s in removed_of(e, v)) for e in rem),
                  "control": sum(bool(ctl_of(e, v)) for e in mat),
                  "witnessed": sum(bool(e.get(f"{v}_witnessed")) for e in mat),
                  "material_by_model": dict(collections.Counter(e["name"] for e in mat)),
                  "removing_by_model": dict(collections.Counter(e["name"] for e in rem)),
                  "one_iteration": sum(max(x.get("nit", 0) for x in e["slsqp"]) <= 1 for e in mat),
                  "one_iteration_by_model": dict(collections.Counter(
                      e["name"] for e in mat if max(x.get("nit", 0) for x in e["slsqp"]) <= 1))}
    return out


def as_tuple_minlplib(c):
    return (c["cuts"], c["distinct"], c["models"],
            c["u1"]["invalid"], c["u1"]["material"], c["u1"]["material_d"], c["u1"]["material_m"],
            c["u1"]["removing"], c["u1"]["removing_d"], c["u1"]["removing_m"],
            c["u2"]["invalid"], c["u2"]["material"], c["u2"]["material_d"], c["u2"]["material_m"],
            c["u2"]["removing"], c["u2"]["removing_d"], c["u2"]["removing_m"],
            c["u1"]["control"] + c["u2"]["control"])


def as_tuple_path(c):
    return (c["cuts"], c["distinct"], c["models"],
            c["u1"]["invalid"], c["u1"]["material"], c["u1"]["material_d"], c["u1"]["material_m"],
            c["u1"]["removing"], c["u1"]["removing_d"], c["u1"]["removing_m"], c["u1"]["known_witness"],
            c["u2"]["invalid"], c["u2"]["material"], c["u2"]["material_d"], c["u2"]["material_m"],
            c["u2"]["removing"], c["u2"]["removing_d"], c["u2"]["removing_m"], c["u2"]["known_witness"],
            c["u1"]["control"] + c["u2"]["control"])


# ----------------------------------------------------------------------------
# Case witnesses: exact feasibility on the case model
# ----------------------------------------------------------------------------

def witness_feasibility(case):
    m = case["model"]
    x = [Q(v) for v in case["known_witness_exact"]]
    def num(t):
        return Q(float.fromhex(t["binary64"]))
    lb = json.loads(m["var_lb"]) if isinstance(m["var_lb"], str) else m["var_lb"]
    ub = json.loads(m["var_ub"]) if isinstance(m["var_ub"], str) else m["var_ub"]
    worst_bound = Q(0)
    for i, v in enumerate(x):
        lo, hi = float.fromhex(lb[i]["binary64"]), float.fromhex(ub[i]["binary64"])
        if math.isfinite(lo):
            worst_bound = max(worst_bound, Q(lo) - v)
        if math.isfinite(hi):
            worst_bound = max(worst_bound, v - Q(hi))
    integrality = sum(1 for i, t in enumerate(m["var_type"]) if t in ("I", "B") and x[i].denominator != 1)
    worst_row = Q(0)
    objective = None
    for ri, row in enumerate(m["rows"]):
        if row.get("nl") is not None:
            return {"error": "nonlinear row"}
        val = sum((num(c) * x[int(j)] for j, c in row["lin"].items()), Q(0))
        val += sum((num(c) * x[i] * x[j] for i, j, c in row["quad"]), Q(0))
        if ri == 0:
            objective = val + num(m["obj_const"])
            continue
        lo, hi = float.fromhex(row["lb"]["binary64"]), float.fromhex(row["ub"]["binary64"])
        if math.isfinite(lo):
            worst_row = max(worst_row, Q(lo) - val)
        if math.isfinite(hi):
            worst_row = max(worst_row, val - Q(hi))
    return {"max_bound_violation": worst_bound, "max_row_violation": worst_row,
            "integrality_violations": integrality, "objective": objective,
            "objective_equals_known": objective == Q(case["known_optimum_exact"]),
            "objective_minus_known": float(objective - Q(case["known_optimum_exact"]))}


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    t0 = time.time()
    d = json.load(open(ABLATION))
    cuts = d["cuts"]
    meta = d["meta"]
    result = {"ablation_json_sha256": hashlib.sha256(ABLATION.read_bytes()).hexdigest()}
    result["A_flags"] = part_a(d)
    log("part A flags done", result["A_flags"]["flag_mismatches"][:5])

    parts = meta["parts"]
    labels = [p["label"] for p in parts]
    family_of = {p["label"]: p["family"] for p in parts}
    need = collections.defaultdict(list)
    for i, e in enumerate(cuts):
        need[(e["part"], e["line"], e["cut"])].append(i)
    if any(len(v) != 1 for v in need.values()):
        raise SystemExit("duplicate cut references in JSON")

    pool = collections.defaultdict(list)       # model key -> points
    source_index = {}                           # source string -> point
    excluded = collections.Counter()            # records with values but primal check not passed
    duplicate_sources = []
    witnesses = {}                              # model key -> point (first part in order)
    witness_variants = collections.defaultdict(set)
    witness_checks = {}
    full = {}                                   # JSON index -> stored cut + record context
    compact = collections.Counter()             # (family, part, key, terms, r, eterms, erhs) -> count
    census = collections.defaultdict(list)
    sha = {}
    ref_problems = []
    record_meta = {}                            # source -> primal_check summary

    quick = "--quick" in sys.argv     # test mode: MINLPLib parts only
    for p in parts:
        label = p["label"]
        if quick and p["family"] != "minlplib":
            continue
        path = Path(p["records"])
        run_dir = path.parent
        h = hashlib.sha256()
        seen_names = set()
        ts = time.time()
        with open(path, "rb") as fh:
            for line_no, raw in enumerate(fh):
                h.update(raw)
                if not raw.strip():
                    continue
                rec = json.loads(raw)
                key = rec.get("model_sha256") or rec["name"]
                pc = rec.get("primal_check") or {}
                if rec.get("original_values") is not None:
                    if pc.get("passed") is True:
                        src = f"{label}:{rec.get('run_id', line_no)}"
                        point = {"source": src, "name": rec["name"], "values": rec["original_values"],
                                 "objective": pc.get("objective", rec.get("primal")), "key": key,
                                 "mode": rec.get("mode")}
                        if src in source_index:
                            duplicate_sources.append(src)
                        source_index[src] = point
                        pool[key].append(point)
                        record_meta[src] = {"passed": pc.get("passed"),
                                            "max_scaled_violation": pc.get("max_scaled_violation"),
                                            "tolerance": pc.get("tolerance"),
                                            "relative_objective_discrepancy": pc.get("relative_objective_discrepancy")}
                    else:
                        excluded[(label, rec["name"])] += 1
                if rec["name"] not in seen_names:
                    seen_names.add(rec["name"])
                    case_path = run_dir / "cases" / (rec["name"] + ".json")
                    if case_path.is_file():
                        case = json.loads(case_path.read_text())
                        w = case.get("known_witness_exact")
                        if w is not None:
                            if isinstance(w, str):
                                w = json.loads(w.replace("'", '"'))
                            witness_variants[key].add(json.dumps(w))
                            if key not in witnesses:
                                witnesses[key] = {"source": f"{label}:cases/{rec['name']}.json",
                                                  "name": rec["name"], "values": w,
                                                  "objective": case.get("known_optimum_exact"),
                                                  "key": key}
                                wf = witness_feasibility(case)
                                witness_checks[f"{label}:{rec['name']}"] = {
                                    k: (str(v) if isinstance(v, Q) else v) for k, v in wf.items()}
                for k, cut in enumerate(rec.get("cuts") or []):
                    cert = cut["row_certificate"]
                    census[label].append(census_entry(cert))
                    terms, r = exact_row(cert)
                    eterms, erhs = exported_row(cert)
                    compact[(family_of[label], label, key, rec["name"], tuple(terms), r,
                             tuple(eterms), erhs)] += 1
                    ref = (label, line_no, k)
                    if ref in need:
                        i = need[ref][0]
                        e = cuts[i]
                        if e["name"] != rec["name"] or e["run_id"] != rec.get("run_id"):
                            ref_problems.append((i, "name/run_id"))
                        sw = {kk: vv for kk, vv in cut["support_witness"].items() if kk != "proof"}
                        full[i] = {"key": key, "row_certificate": cert, "support_witness": sw,
                                   "support_stats": cut["support_stats"], "features": cut["features"],
                                   "symbols": cut["symbols"], "variables": cut["variables"],
                                   "box": cut["box"], "domain_rows": cut["domain_rows"],
                                   "coefficients": cut["coefficients"],
                                   "column_names": cut["column_names"]}
                del rec
        sha[label] = h.hexdigest()
        log(f"scanned {label} in {time.time() - ts:.0f}s; sha ok={sha[label] == p['records_sha256']}")

    # path-family sample: seed-0 indices, per-part split, cut counts per part
    smp = meta["sample"]
    idx = sorted(random.Random(smp["seed"]).sample(range(smp["population"]), smp["size"]))
    path_parts = [p for p in parts if p["family"] == "path"]
    offsets, off = {}, 0
    for p in path_parts:
        offsets[p["label"]] = off
        off += len(census[p["label"]]) if p["label"] in census else p["cuts_recorded"]
    per_part = {p["label"]: sum(offsets[p["label"]] <= j < offsets[p["label"]] + p["cuts_recorded"]
                                for j in idx) for p in path_parts}
    json_path_idx = sorted(e["index"] for e in cuts if e["family"] == "path")
    result["sample_check"] = {
        "indices_reproduced": idx == smp["indices"],
        "population_equals_scanned_path_cuts": off == smp["population"],
        "json_entry_indices_equal_sample": json_path_idx == idx,
        "per_part": per_part,
        "per_part_matches_meta": all(per_part[p["label"]] == p["cuts_analyzed"] for p in path_parts)}
    result["cuts_recorded_match"] = {p["label"]: len(census.get(p["label"], [])) == p["cuts_recorded"]
                                     for p in parts}
    result["records_sha256_match"] = {l: sha.get(l) == p["records_sha256"] for l, p in zip(labels, parts)}
    result["ref_problems"] = ref_problems
    result["cuts_found"] = (len(full), len(cuts))
    result["duplicate_sources"] = duplicate_sources
    result["excluded_records_with_values_not_passed"] = {f"{a}:{b}": n for (a, b), n in excluded.items()}
    result["witness_variants_per_key_max"] = max((len(v) for v in witness_variants.values()), default=0)
    result["witness_checks"] = witness_checks

    def points_for(key):
        pts = list(pool.get(key, []))
        if key in witnesses:
            pts.append(witnesses[key])
        return pts

    # points per model (path family) for the summary statement
    path_keys = {full[i]["key"] for i, e in enumerate(cuts) if e["family"] == "path" and i in full}
    pp = [len(points_for(k)) for k in path_keys]
    result["path_points_per_model"] = (min(pp), max(pp), len(pp)) if pp else None
    result["incumbents_per_model_match_json"] = all(
        len(pool.get(k, [])) == n for k, n in meta["incumbents_per_model"].items()) and \
        set(pool) == set(meta["incumbents_per_model"])

    # ---------------- Part B: rows of materially invalid cuts ----------------
    log("part B: rows")
    mine = {}           # (i, v) -> removed sources (independent)
    my_ctl = {}         # (i, v) -> certified row violated beyond threshold
    binding_problems = collections.Counter()
    removed_set_mismatch = []
    points_count_mismatch = []
    removal_details = []
    max_cert_violation_rel = None
    strict_cert_viol = 0
    exported_viol_beyond = 0
    eval_errors = collections.Counter()
    epigraph_removals = []
    for i, e in enumerate(cuts):
        if "error" in e or i not in full:
            continue
        f = full[i]
        cut_like = {"row_certificate": f["row_certificate"], "support_witness": f["support_witness"],
                    "variables": f["variables"], "coefficients": f["coefficients"],
                    "column_names": f["column_names"]}
        if not (e["u1_material"] or e["u2_material"]):
            continue
        for prob in binding_check(cut_like):
            binding_problems[prob] += 1
        cert = f["row_certificate"]
        terms, r = exact_row(cert)
        eterms, erhs = exported_row(cert)
        beta = Q(cert["binding"]["support"]["rhs"])
        norm = sum(abs(c) for _, c in terms)
        thr = MATERIAL * max(Q(1), norm)
        pts = points_for(f["key"])
        has_epi = any(n == "objective_epigraph" for n, _ in terms)
        for v in VARIANTS:
            if not e[f"{v}_material"]:
                continue
            U = hexq(e[v])
            r_u = r + (U - beta)
            removed, ctl = [], False
            for pt in pts:
                try:
                    act = activity(terms, pt)
                    eact = activity(eterms, pt)
                except ValueError as exc:
                    eval_errors[str(exc)] += 1
                    continue
                viol_u = r_u - act
                viol_c = r - act
                rel = viol_c / max(Q(1), norm)
                if max_cert_violation_rel is None or rel > max_cert_violation_rel:
                    max_cert_violation_rel = rel
                if viol_c > 0:
                    strict_cert_viol += 1
                if viol_c > thr:
                    ctl = True
                if erhs - eact > thr:
                    exported_viol_beyond += 1
                if viol_u > thr:
                    removed.append(pt["source"])
                    is_case = "cases/" in pt["source"]
                    rm = record_meta.get(pt["source"])
                    removal_details.append({
                        "i": i, "v": v, "part": e["part"], "name": e["name"], "run_id": e["run_id"],
                        "cut": e["cut"], "point": pt["source"], "point_mode": pt.get("mode", "case"),
                        "violation": viol_u, "threshold": thr,
                        "ratio": viol_u / thr, "certified_violation": viol_c,
                        "exported_violation": erhs - eact,
                        "passed": True if is_case else (rm or {}).get("passed"),
                        "max_scaled_violation": None if is_case else (rm or {}).get("max_scaled_violation"),
                        "epigraph": has_epi,
                        "t_slack_needed": (viol_u / dict(terms)["objective_epigraph"]) if has_epi else None})
                    if has_epi:
                        epigraph_removals.append((e["name"], v))
            mine[(i, v)] = removed
            my_ctl[(i, v)] = ctl
            js = e[f"{v}_rows"]
            if sorted(js["removed"]) != sorted(removed):
                removed_set_mismatch.append({"i": i, "v": v, "json": len(js["removed"]),
                                             "mine": len(removed)})
            if js["points"] != len(pts):
                points_count_mismatch.append((i, v, js["points"], len(pts)))
    result["B_binding_problems"] = dict(binding_problems)
    result["B_removed_set_mismatches"] = removed_set_mismatch
    result["B_points_count_mismatches"] = points_count_mismatch[:20]
    result["B_eval_errors"] = dict(eval_errors)
    result["B_cert_row_strictly_violated_point_evaluations"] = strict_cert_viol
    result["B_max_relative_certified_violation"] = float(max_cert_violation_rel or 0)
    result["B_exported_row_violated_beyond_threshold"] = exported_viol_beyond
    result["B_epigraph_removals"] = dict(collections.Counter(epigraph_removals))

    # removal detail summary: every (cut, variant, point) flagged
    rd = removal_details
    result["B_removal_pairs"] = len(rd)
    result["B_removal_cut_variants"] = len({(x["i"], x["v"]) for x in rd})
    result["B_removal_min_ratio"] = float(min(x["ratio"] for x in rd)) if rd else None
    result["B_removal_min_violation"] = float(min(x["violation"] for x in rd)) if rd else None
    result["B_removal_all_passed"] = all(x["passed"] is True for x in rd)
    result["B_removal_cert_row_max_violation"] = float(max(x["certified_violation"] for x in rd)) if rd else None
    result["B_removal_cert_row_beyond_threshold"] = sum(x["certified_violation"] > x["threshold"] for x in rd)
    result["B_removal_cert_row_strictly_positive"] = sum(x["certified_violation"] > 0 for x in rd)
    result["B_removal_exported_beyond_threshold"] = sum(x["exported_violation"] > x["threshold"] for x in rd)
    result["B_removal_max_scaled_violation_of_points"] = max(
        (x["max_scaled_violation"] for x in rd if x["max_scaled_violation"] is not None), default=None)
    best = {}
    for x in rd:
        k = (cuts[x["i"]]["family"], cuts[x["i"]]["exact_certificate"], x["v"], x["i"])
        best[k] = max(best.get(k, 0), x["ratio"])
    dist = collections.defaultdict(list)
    for (fam, ex, v, _), ratio in best.items():
        dist[f"{fam}/{'exact' if ex else 'lower'}/{v}"].append(ratio)
    result["B_removal_ratio_distribution"] = {
        k: {"n": len(xs), "min_of_max_ratio": float(min(xs)), "below_10": sum(x < 10 for x in xs),
            "below_100": sum(x < 100 for x in xs), "below_1000": sum(x < 1000 for x in xs)}
        for k, xs in sorted(dist.items())}
    by_cv = collections.defaultdict(set)
    for x in rd:
        by_cv[(cuts[x["i"]]["family"], cuts[x["i"]]["exact_certificate"], x["v"], x["i"])].add(x["point_mode"])
    src = collections.defaultdict(collections.Counter)
    for (fam, ex, v, _), modes in by_cv.items():
        scip = any(m not in ("gurobi", "case") for m in modes)
        src[f"{fam}/{'exact' if ex else 'lower'}/{v}"]["with_scip_point" if scip else
                                                        "only_" + "+".join(sorted(modes))] += 1
    # robustness: (ii) discount the point's own violation of the certified row,
    # (iii) a 10x larger threshold, (iv) points that satisfy the certified row exactly
    rob = collections.defaultdict(lambda: collections.Counter())
    for x in rd:
        k = f"{cuts[x['i']]['family']}/{'exact' if cuts[x['i']]['exact_certificate'] else 'lower'}/{x['v']}"
        cv = (x["i"], x["v"])
        rob[k][("protocol", cv)] = 1
        if x["violation"] - max(Q(0), x["certified_violation"]) > x["threshold"]:
            rob[k][("discount_certified_violation", cv)] = 1
        if x["violation"] > 10 * x["threshold"]:
            rob[k][("threshold_x10", cv)] = 1
        if x["certified_violation"] <= 0:
            rob[k][("point_satisfies_certified_row", cv)] = 1
    x10 = collections.defaultdict(set)
    for x in rd:
        if x["violation"] > 10 * x["threshold"]:
            e = cuts[x["i"]]
            x10[f"{e['family']}/{'exact' if e['exact_certificate'] else 'lower'}/{x['v']}"].add((e["name"], x["i"]))
    result["B_removal_threshold_x10_by_model"] = {
        k: dict(collections.Counter(name for name, _ in v)) for k, v in sorted(x10.items())
        if k.startswith("minlplib")}
    result["B_removal_threshold_x10_models"] = {k: len({name for name, _ in v}) for k, v in sorted(x10.items())}
    result["B_removal_robustness"] = {
        k: dict(collections.Counter(name for (name, _cv) in c)) for k, c in sorted(rob.items())}
    result["B_removal_point_sources"] = {k: dict(c) for k, c in src.items()}
    result["B_pool_modes"] = dict(collections.Counter(pt.get("mode") for pts in pool.values() for pt in pts))
    epi = [x for x in rd if x["epigraph"]]
    result["B_epigraph_min_t_slack_needed"] = float(min(x["t_slack_needed"] for x in epi)) if epi else None
    # seed-1 sample of 300 removing cut-variants (reported; all are checked above)
    rcv = sorted({(x["i"], x["v"]) for x in rd})
    s1 = random.Random(1).sample(rcv, min(300, len(rcv)))
    result["B_seed1_sample_size"] = len(s1)
    s1set = set(s1)
    s1rd = [x for x in rd if (x["i"], x["v"]) in s1set]
    result["B_seed1_min_ratio"] = float(min(x["ratio"] for x in s1rd)) if s1rd else None
    result["B_seed1_all_passed"] = all(x["passed"] is True for x in s1rd)
    result["B_seed1_cert_row_beyond_threshold"] = sum(x["certified_violation"] > x["threshold"] for x in s1rd)
    # cited-incumbent check: every source in the JSON removed lists is a passed record or a case witness
    cited = {s for e in cuts for v in VARIANTS for s in (e.get(f"{v}_rows") or {}).get("removed", [])}
    result["B_cited_sources"] = len(cited)
    result["B_cited_unresolved"] = sorted(s for s in cited if s not in source_index
                                          and not any(w["source"] == s for w in witnesses.values()))
    result["B_cited_not_passed"] = sorted(s for s in cited if s in record_meta
                                          and record_meta[s]["passed"] is not True)
    # specific claims
    def removal_summary(name_sub, part=None, v=None):
        sel = [x for x in rd if name_sub in x["name"] and (part is None or x["part"] == part)
               and (v is None or x["v"] == v)]
        out = collections.defaultdict(list)
        for x in sel:
            out[(x["part"], x["run_id"], x["cut"], x["v"])].append(x)
        return {f"{k[0]}|{k[1]}|cut{k[2]}|{k[3]}": {
            "points_removed": len(xs), "points_total": len(points_for(full[xs[0]["i"]]["key"])),
            "witness_removed": any("cases/" in x["point"] for x in xs),
            "max_violation": float(max(x["violation"] for x in xs))} for k, xs in out.items()}
    result["B_c4_u2_removals"] = removal_summary("interleaved_path_coupled", "v4/partC4", "u2")
    result["B_tc02b_u2_removals"] = removal_summary("kall_ellipsoids_tc02b", None, "u2")

    # ---------------- Part A counts: JSON-derived and independent ----------------
    log("part A counts")
    def json_removed(e, v):
        return (e.get(f"{v}_rows") or {}).get("removed", [])
    def json_ctl(e, v):
        return bool((e.get(f"{v}_rows") or {}).get("certified_row_violated"))
    def my_removed(e, v):
        return mine.get((e["_i"], v), [])
    def my_ctl_f(e, v):
        return my_ctl.get((e["_i"], v), False)
    for i, e in enumerate(cuts):
        e["_i"] = i
    A = {}
    for fam in ("minlplib", "path"):
        for exact in (True, False):
            group = [e for e in cuts if e["family"] == fam and e["exact_certificate"] == exact
                     and "error" not in e]
            if not group:
                continue
            tag = f"{fam}/{'exact' if exact else 'lower'}"
            A[tag] = {"ALL": {"json": counts(group, json_removed, json_ctl),
                              "mine": counts(group, my_removed, my_ctl_f)}}
            for label in labels:
                g = [e for e in group if e["part"] == label]
                if g:
                    A[tag][label] = {"json": counts(g, json_removed, json_ctl),
                                     "mine": counts(g, my_removed, my_ctl_f)}
    comparisons = []
    for label, claim in CLAIMS_MINLPLIB.items():
        for src in ("json", "mine"):
            got = as_tuple_minlplib(A["minlplib/exact"][label][src])
            if got != claim:
                comparisons.append({"family": "minlplib", "part": label, "source": src,
                                    "claimed": claim, "recomputed": got})
    for label, claim in CLAIMS_PATH.items():
        for src in ("json", "mine"):
            got = as_tuple_path(A["path/exact"][label][src])
            if got != claim:
                comparisons.append({"family": "path", "part": label, "source": src,
                                    "claimed": claim, "recomputed": got})
    result["A_table_mismatches"] = comparisons
    allm = A["minlplib/exact"]["ALL"]
    model_cmp = {}
    for src in ("json", "mine"):
        c = allm[src]
        model_cmp[src] = {
            "u1_material": c["u1"]["material_by_model"] == CLAIMS_MODELS["u1_material"],
            "u1_removing": c["u1"]["removing_by_model"] == CLAIMS_MODELS["u1_removing"],
            "u2_material": c["u2"]["material_by_model"] == CLAIMS_MODELS["u2_material"],
            "u2_removing": c["u2"]["removing_by_model"] == CLAIMS_MODELS["u2_removing"]}
    result["A_model_lists_match"] = model_cmp
    result["A_minlplib_u2_one_iteration"] = (allm["json"]["u2"]["one_iteration"],
                                             allm["json"]["u2"]["one_iteration_by_model"])
    result["A_witnessed_all"] = {tag: all(A[tag]["ALL"]["json"][v]["witnessed"] == A[tag]["ALL"]["json"][v]["material"]
                                          for v in VARIANTS) for tag in A if tag.endswith("exact")}
    low = A.get("minlplib/lower", {}).get("ALL", {})
    lower_methods = collections.Counter(e["method"] for e in cuts if not e["exact_certificate"])
    lower_rem_methods = collections.Counter(
        (e["method"], e["name"]) for e in cuts if not e["exact_certificate"] and mine.get((e["_i"], "u1")))
    result["A_lower"] = {
        "json": {k: low["json"][k] for k in ("cuts", "distinct", "models")} if low else None,
        "u1_material": low["json"]["u1"]["material"] if low else None,
        "u2_material": low["json"]["u2"]["material"] if low else None,
        "u1_removing_json": low["json"]["u1"]["removing"] if low else None,
        "u1_removing_mine": low["mine"]["u1"]["removing"] if low else None,
        "u2_removing_mine": low["mine"]["u2"]["removing"] if low else None,
        "control_mine": (low["mine"]["u1"]["control"] + low["mine"]["u2"]["control"]) if low else None,
        "methods": dict(lower_methods), "u1_removing_by_method_model": {f"{a}|{b}": n for (a, b), n in lower_rem_methods.items()}}
    # JSON summary and key_counts vs JSON cuts
    ks = []
    for tag, k in meta["key_counts"].items():
        if tag not in A:
            continue
        c = A[tag]["ALL"]["json"]
        if (k["cuts"], k["distinct_cuts"], k["models"]) != (c["cuts"], c["distinct"], c["models"]):
            ks.append((tag, "cuts"))
        for v in VARIANTS:
            x = k[v]
            if (x["invalid"], x["material"], x["material_distinct"], len(x["material_models"]),
                    x["removing"], x["removing_distinct"], len(x["removing_models"]),
                    x["removing_known_witness"], x["slsqp_one_iteration"]) != (
                    c[v]["invalid"], c[v]["material"], c[v]["material_d"], c[v]["material_m"],
                    c[v]["removing"], c[v]["removing_d"], c[v]["removing_m"],
                    c[v]["known_witness"], c[v]["one_iteration"]):
                ks.append((tag, v))
    result["A_key_counts_mismatches"] = ks
    sm = []
    for label, by_method in d["summary"].items():
        for method, s in by_method.items():
            g = [e for e in cuts if e["part"] == label and e["method"] == method and "error" not in e]
            for v in VARIANTS:
                mat = [e for e in g if e[f"{v}_material"]]
                rem = [e for e in mat if json_removed(e, v)]
                got = (sum(e[f"{v}_invalid"] for e in g), len(mat), len(rem),
                       sum(any("cases/" in s_ for s_ in json_removed(e, v)) for e in rem),
                       sum(json_ctl(e, v) for e in mat))
                exp = (s[v]["exceeds"], s[v]["material"], s[v]["removing_cuts"],
                       s[v]["removing_known_witness"], s[v]["certified_row_violated_cuts"])
                if got != exp:
                    sm.append((label, method, v, exp, got))
    result["A_summary_mismatches"] = sm
    below = {}
    for fam in ("minlplib", "path"):
        for v in VARIANTS:
            defs = [(Q(e["certified"]) - hexq(e[v])) / max(Q(1), abs(Q(e["certified"])))
                    for e in cuts if e["family"] == fam and e["exact_certificate"] and "error" not in e]
            neg = [x for x in defs if x > 0]
            below[f"{fam}/{v}"] = {"below_certified": len(neg),
                                   "max_relative_deficit": float(max(neg)) if neg else None}
    result["A_U_below_certified_exact"] = below
    result["A_reconstruction"] = {
        "ok": sum(1 for e in cuts if "error" not in e and all(e["reconstruction"].values())),
        "total": len(cuts),
        "exact_support_equal": sum(bool(e.get("certified_is_exact_support")) for e in cuts if e["exact_certificate"]),
        "exact_total": sum(1 for e in cuts if e["exact_certificate"])}
    result["A_counts"] = {tag: {lab: {src: {kk: vv for kk, vv in c.items()} for src, c in x.items()}
                                for lab, x in t.items()} for tag, t in A.items()}

    # ---------------- Broad control: every recorded row at every pooled point ----------------
    log(f"broad control over {len(compact)} distinct rows")
    broad = collections.defaultdict(lambda: {"rows": 0, "distinct_rows": 0, "point_evals": 0,
                                             "beyond": 0, "strict": 0, "exported_beyond": 0,
                                             "exported_strict": 0, "max_rel": None, "errors": 0,
                                             "rows_without_points": 0})
    broad_examples = []
    for (fam, label, key, name, terms, r, eterms, erhs), n in compact.items():
        b = broad[fam]
        b["rows"] += n
        b["distinct_rows"] += 1
        pts = points_for(key)
        if not pts:
            b["rows_without_points"] += n
        norm = sum(abs(c) for _, c in terms)
        thr = MATERIAL * max(Q(1), norm)
        for pt in pts:
            try:
                act = activity(terms, pt)
                eact = activity(eterms, pt)
            except ValueError:
                b["errors"] += 1
                continue
            b["point_evals"] += 1
            viol = r - act
            rel = viol / max(Q(1), norm)
            if b["max_rel"] is None or rel > b["max_rel"]:
                b["max_rel"] = rel
            if viol > thr:
                b["beyond"] += 1
                rm = record_meta.get(pt["source"]) or {}
                broad_examples.append({
                    "family": fam, "part": label, "model": name, "row_multiplicity": n,
                    "point": pt["source"], "violation": float(viol), "threshold": float(thr),
                    "ratio": float(viol / thr), "norm": float(norm),
                    "columns": [nm for nm, _ in terms],
                    "point_max_scaled_violation": rm.get("max_scaled_violation"),
                    "exported_violation": float(erhs - eact)})
            if viol > 0:
                b["strict"] += 1
            if erhs - eact > thr:
                b["exported_beyond"] += 1
            if erhs - eact > 0:
                b["exported_strict"] += 1
    result["broad_examples"] = broad_examples
    result["broad_control"] = {fam: {k: (float(v) if isinstance(v, Q) else v) for k, v in b.items()}
                               for fam, b in broad.items()}

    # ---------------- Census ----------------
    cen = {}
    for fam in ("minlplib", "path"):
        entries = [x for l in labels if family_of[l] == fam for x in census[l]]
        if not entries:
            continue
        per_part = {l: sum(x["rounded"] for x in census[l]) / len(census[l]) for l in labels
                    if family_of[l] == fam and census[l]}
        maxE = max((abs(x["E"]), l) for l in labels if family_of[l] == fam for x in census[l])
        cen[fam] = {"rows": len(entries), "rounded": sum(x["rounded"] for x in entries),
                    "nonzero_E": sum(x["nonzeroE"] for x in entries),
                    "recorded_safe": sum(x["recorded_safe"] for x in entries),
                    "independent_safe": sum(x["independent_safe"] for x in entries),
                    "E_le_box_bound": sum(x["E_le_bound"] for x in entries),
                    "rounding_field_ok": sum(x["field_ok"] for x in entries),
                    "max_abs_E": float(maxE[0]), "max_abs_E_part": maxE[1],
                    "max_rel_shift": float(max(x["rel_shift"] for x in entries)),
                    "rounded_share_per_part_min": min(per_part.values()),
                    "rounded_share_per_part_max": max(per_part.values()),
                    "rounded_share": sum(x["rounded"] for x in entries) / len(entries)}
    result["census"] = cen

    # ---------------- Part C: certified minimizers ----------------
    log("part C: minimizers")
    population = [i for i, e in enumerate(cuts) if e["exact_certificate"] and "error" not in e
                  and (e["u1_material"] or e["u2_material"]) and (i in full or not quick)]
    sample = sorted(random.Random(2).sample(population, 100))
    def check_minimizer(i):
        e, f = cuts[i], full[i]
        sw, ss = f["support_witness"], f["support_stats"]
        cert = Q(e["certified"])
        out = {"i": i, "part": e["part"], "name": e["name"], "cut": e["cut"]}
        out["certified_matches_record"] = Q(sw["lower_bound"]) == cert
        out["exact_support_matches"] = ss.get("exact_support") is not None and Q(ss["exact_support"]) == cert
        out["method_matches"] = ss["method"] == e["method"] == sw["method"]
        out["coefficients_match"] = (f["coefficients"] == e["coefficients"] and
                                     [float.fromhex(x) for x in sw["model"]["coefficients"]] == e["coefficients"])
        scale = MATERIAL * max(Q(1), abs(cert))
        for v in VARIANTS:
            if e[f"{v}_material"]:
                U = hexq(e[v])
                out[f"{v}_gt_certified"] = U > cert
                out[f"{v}_material"] = U - cert > scale
        mz = ss.get("minimizer")
        out["minimizer_present"] = mz is not None
        if mz is None:
            return out
        out["minimizer_matches_json"] = mz == e["certified_minimizer"]
        u = [Q(x) for x in mz]
        box = [(Q(lo), Q(hi)) for lo, hi in f["box"]]
        out["in_box"] = all(lo <= x <= hi for x, (lo, hi) in zip(u, box)) and len(u) == len(box)
        out["domain_rows_hold"] = all(sum(Q(a) * x for a, x in zip(row["coefficients"], u)) <= Q(row["rhs"])
                                      for row in f["domain_rows"])
        mb = sw["model"]
        out["witness_box_matches"] = [[Q(a), Q(b)] for a, b in mb["box"]] == [[a, b] for a, b in box]
        out["witness_rows_hold"] = all(sum(Q(a) * x for a, x in zip(coef, u)) <= Q(rhs)
                                       for coef, rhs in mb["rows"])
        env = {s: x for s, x in zip(f["symbols"], u)}
        try:
            val_s = sum((Q(c) * eval_string(fs, env) for c, fs in zip(f["coefficients"], f["features"])), Q(0))
            out["value_from_strings_equals_certified"] = val_s == cert
        except NotRational as exc:
            out["value_from_strings_equals_certified"] = None
            out["string_note"] = str(exc)
        try:
            val_t = sum((hexq(c) * eval_tree(t, u) for c, t in zip(mb["coefficients"], mb["features"])), Q(0))
            out["value_from_trees_equals_certified"] = val_t == cert
        except NotRational as exc:
            out["value_from_trees_equals_certified"] = None
            out["tree_note"] = str(exc)
        for v in VARIANTS:
            if e[f"{v}_material"]:
                out[f"{v}_witnessed"] = bool(out["in_box"] and out["domain_rows_hold"] and
                                             cert < hexq(e[v]) - scale)
        # U is (up to binary64 rounding) the value at its recorded point
        for v in VARIANTS:
            pt = e[f"{v}_point"]
            uq = [Q(x) for x in pt]
            envp = {s: x for s, x in zip(f["symbols"], uq)}
            try:
                val = sum((Q(c) * eval_string(fs, envp) for c, fs in zip(f["coefficients"], f["features"])), Q(0))
                out[f"{v}_point_rel_gap"] = float(abs(val - hexq(e[v])) / max(Q(1), abs(val)))
                out[f"{v}_point_box_excess"] = float(max([Q(0)] + [max(lo - x, x - hi) for x, (lo, hi) in zip(uq, box)]))
                out[f"{v}_point_row_excess"] = float(max([Q(0)] + [
                    (sum(Q(a) * x for a, x in zip(row["coefficients"], uq)) - Q(row["rhs"])) / max(Q(1), abs(Q(row["rhs"])))
                    for row in f["domain_rows"]]))
            except NotRational:
                pass
        return out

    sample_results = [check_minimizer(i) for i in sample]
    all_results = [check_minimizer(i) for i in population]

    def summarize_c(rs):
        keys = ["certified_matches_record", "exact_support_matches", "method_matches",
                "coefficients_match", "u1_gt_certified", "u1_material", "u2_gt_certified",
                "u2_material", "minimizer_present", "minimizer_matches_json", "in_box",
                "domain_rows_hold", "witness_box_matches", "witness_rows_hold",
                "value_from_strings_equals_certified", "value_from_trees_equals_certified",
                "u1_witnessed", "u2_witnessed"]
        out = {"n": len(rs), "families": dict(collections.Counter(cuts[r["i"]]["family"] for r in rs)),
               "u2_material_in_sample": sum(1 for r in rs if "u2_gt_certified" in r)}
        for k in keys:
            vals = [r[k] for r in rs if k in r]
            out[k] = {"true": sum(v is True for v in vals), "false": sum(v is False for v in vals),
                      "none": sum(v is None for v in vals)}
        for v in VARIANTS:
            gaps = [r[f"{v}_point_rel_gap"] for r in rs if f"{v}_point_rel_gap" in r]
            out[f"{v}_point_max_rel_gap"] = max(gaps) if gaps else None
            out[f"{v}_point_max_box_excess"] = max((r[f"{v}_point_box_excess"] for r in rs
                                                    if f"{v}_point_box_excess" in r), default=None)
            out[f"{v}_point_max_row_excess"] = max((r[f"{v}_point_row_excess"] for r in rs
                                                    if f"{v}_point_row_excess" in r), default=None)
        out["failures"] = [r for r in rs if any(r.get(k) is False for k in keys)][:10]
        return out
    result["C_population"] = len(population)
    result["C_sample_indices"] = sample
    result["C_sample"] = summarize_c(sample_results)
    result["C_all"] = summarize_c(all_results)
    result["elapsed_seconds"] = round(time.time() - t0, 1)

    def conv(x):
        if isinstance(x, Q):
            return str(x)
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [conv(v) for v in x]
        return x
    json.dump(conv(result), sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
