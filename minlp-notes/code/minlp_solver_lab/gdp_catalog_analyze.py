"""Size and convexity analysis for the GDP instance catalog.

Usage:
    uv run python gdp_catalog_analyze.py --name NAME      # one instance, JSON to stdout
    uv run python gdp_catalog_analyze.py --all [--jobs 4] # all instances -> gdp_catalog.json

Convexity rules (DCP-style walk over the Pyomo expression tree):
  * degree-2 expressions: Hessian from the standard quadratic repn, PSD/NSD by
    numpy eigenvalues;
  * exp(convex) convex; log/sqrt(concave) concave; |affine| convex;
  * x**p with p even integer convex for affine x; p>1 convex for x>=0;
    0<p<1 concave for x>=0; p<0 convex for x>0 (bounds via FBBT);
  * a**x convex for constant a>0; c/x convex for c>0 on x>=0 (domain x>0).
Anything else is "unknown" and treated as nonconvex.  Nonlinear equalities and
nonlinear ranged constraints are nonconvex.  The model is a convex GDP when
every nonlinear constraint (global and inside active disjuncts) is convex in
its required direction and the objective is convex (min) / concave (max).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
import traceback

SINGLE_THREAD_ENV = {"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
os.environ.update(SINGLE_THREAD_ENV)
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

HERE = Path(__file__).resolve().parent
RESULT_DIR = HERE / "gdp_catalog_results" / "analyze"

CONST, AFFINE, CONVEX, CONCAVE, UNKNOWN = "const", "affine", "convex", "concave", "unknown"


def _bounds(expr):
    from pyomo.contrib.fbbt.fbbt import compute_bounds_on_expr

    try:
        lb, ub = compute_bounds_on_expr(expr)
    except Exception:
        return -math.inf, math.inf
    return (-math.inf if lb is None else lb, math.inf if ub is None else ub)


def _neg(c):
    return {CONVEX: CONCAVE, CONCAVE: CONVEX}.get(c, c)


def _scale(c, k):
    if k == 0:
        return CONST
    return c if k > 0 else _neg(c)


def _sum(cs):
    cs = [c for c in cs if c != CONST]
    if not cs:
        return CONST
    if all(c == AFFINE for c in cs):
        return AFFINE
    if all(c in (AFFINE, CONVEX) for c in cs):
        return CONVEX
    if all(c in (AFFINE, CONCAVE) for c in cs):
        return CONCAVE
    return UNKNOWN


def quadratic_curvature(expr):
    """Curvature of a polynomial of degree <= 2 via Hessian eigenvalues."""
    import numpy as np
    from pyomo.repn import generate_standard_repn

    repn = generate_standard_repn(expr, quadratic=True, compute_values=True)
    if repn.nonlinear_expr is not None:
        return UNKNOWN
    if not repn.quadratic_vars:
        return AFFINE if repn.linear_vars else CONST
    idx = {}
    for v1, v2 in repn.quadratic_vars:
        for v in (v1, v2):
            idx.setdefault(id(v), len(idx))
    n = len(idx)
    H = np.zeros((n, n))
    for (v1, v2), c in zip(repn.quadratic_vars, repn.quadratic_coefs):
        i, j = idx[id(v1)], idx[id(v2)]
        if i == j:
            H[i, i] += 2.0 * c
        else:
            H[i, j] += c
            H[j, i] += c
    eig = np.linalg.eigvalsh(H)
    tol = 1e-9 * max(1.0, float(np.abs(H).max()))
    if eig.min() >= -tol:
        return CONVEX
    if eig.max() <= tol:
        return CONCAVE
    return "indefinite"


def norm_convex(arg):
    """True if sqrt(arg) is convex because arg = ||affine map||^2, i.e. the
    augmented matrix [[A, b/2], [b/2, c]] of the quadratic arg is PSD."""
    import numpy as np
    from pyomo.repn import generate_standard_repn

    pd = arg.polynomial_degree()
    if pd is None or pd > 2:
        return False
    repn = generate_standard_repn(arg, quadratic=True, compute_values=True)
    if repn.nonlinear_expr is not None:
        return False
    idx = {}
    for v1, v2 in repn.quadratic_vars:
        for v in (v1, v2):
            idx.setdefault(id(v), len(idx))
    for v in repn.linear_vars:
        idx.setdefault(id(v), len(idx))
    n = len(idx)
    M = np.zeros((n + 1, n + 1))
    for (v1, v2), c in zip(repn.quadratic_vars, repn.quadratic_coefs):
        i, j = idx[id(v1)], idx[id(v2)]
        if i == j:
            M[i, i] += c
        else:
            M[i, j] += c / 2
            M[j, i] += c / 2
    for v, c in zip(repn.linear_vars, repn.linear_coefs):
        i = idx[id(v)]
        M[i, n] += c / 2
        M[n, i] += c / 2
    M[n, n] = repn.constant
    tol = 1e-9 * max(1.0, float(np.abs(M).max()))
    return bool(np.linalg.eigvalsh(M).min() >= -tol)


def curvature(node):
    import pyomo.core.expr as EXPR
    from pyomo.core.expr.numeric_expr import (
        AbsExpression,
        DivisionExpression,
        LinearExpression,
        MonomialTermExpression,
        NegationExpression,
        PowExpression,
        ProductExpression,
        SumExpression,
        UnaryFunctionExpression,
    )
    from pyomo.core.expr.numvalue import is_potentially_variable, value

    if not is_potentially_variable(node):
        return CONST
    if node.is_variable_type():
        return CONST if node.fixed else AFFINE
    if node.is_named_expression_type():
        return curvature(node.expr)
    if not node.is_expression_type():
        return UNKNOWN
    if isinstance(node, MonomialTermExpression):
        return _scale(curvature(node.args[1]), value(node.args[0]))
    if isinstance(node, (LinearExpression, SumExpression)):
        return _sum([curvature(a) for a in node.args])
    if isinstance(node, NegationExpression):
        return _neg(curvature(node.args[0]))
    if isinstance(node, ProductExpression):
        a, b = node.args
        ca, cb = curvature(a), curvature(b)
        if ca == CONST:
            return _scale(cb, value(a))
        if cb == CONST:
            return _scale(ca, value(b))
        pd = node.polynomial_degree()
        if pd is not None and pd <= 2:
            q = quadratic_curvature(node)
            return q if q in (CONST, AFFINE, CONVEX, CONCAVE) else UNKNOWN
        return UNKNOWN
    if isinstance(node, DivisionExpression):
        num, den = node.args
        cn, cd = curvature(num), curvature(den)
        if cd == CONST:
            d = value(den)
            return _scale(cn, 1.0 / d) if d != 0 else UNKNOWN
        if cn == CONST:
            c = value(num)
            lb, ub = _bounds(den)
            # c/x is convex on the natural domain x > 0 (and concave on
            # x < 0); a zero bound is accepted as the domain boundary, the
            # same convention MINLPLib uses for e.g. the FLay instances.
            if lb >= 0 and cd in (AFFINE, CONCAVE):
                return CONVEX if c > 0 else CONCAVE if c < 0 else CONST
            if ub <= 0 and cd in (AFFINE, CONVEX):
                return CONCAVE if c > 0 else CONVEX if c < 0 else CONST
        return UNKNOWN
    if isinstance(node, PowExpression):
        base, expo = node.args
        if not is_potentially_variable(expo):
            p = value(expo)
            cb = curvature(base)
            if p == 0 or cb == CONST:
                return CONST
            if p == 1:
                return cb
            lb, ub = _bounds(base)
            if p == int(p) and int(p) % 2 == 0 and p > 0:
                if cb == AFFINE or (cb == CONVEX and lb >= 0) or (cb == CONCAVE and ub <= 0):
                    return CONVEX
                pd = node.polynomial_degree()
                if pd is not None and pd <= 2:
                    q = quadratic_curvature(node)
                    return q if q in (CONVEX, CONCAVE, AFFINE, CONST) else UNKNOWN
                return UNKNOWN
            if p > 1:
                return CONVEX if (cb in (AFFINE, CONVEX) and lb >= 0) else UNKNOWN
            if 0 < p < 1:
                if cb in (AFFINE, CONCAVE) and lb >= 0:
                    return CONCAVE
                if p == 0.5 and norm_convex(base):
                    return CONVEX
                return UNKNOWN
            if p < 0:
                if lb > 0 and cb in (AFFINE, CONCAVE):
                    return CONVEX
                if p == int(p) and int(p) % 2 == 0 and ub < 0 and cb in (AFFINE, CONVEX):
                    return CONVEX
                return UNKNOWN
            return UNKNOWN
        if not is_potentially_variable(base):
            a = value(base)
            ce = curvature(expo)
            if a > 0 and ce in (AFFINE, CONVEX):
                return CONVEX
            if a == 1:
                return CONST
            return UNKNOWN
        return UNKNOWN
    if isinstance(node, AbsExpression):
        return CONVEX if curvature(node.args[0]) == AFFINE else UNKNOWN
    if isinstance(node, UnaryFunctionExpression):
        ca = curvature(node.args[0])
        name = node.getname()
        if name == "exp":
            return CONVEX if ca in (AFFINE, CONVEX) else UNKNOWN
        if name in ("log", "log10"):
            return CONCAVE if ca in (AFFINE, CONCAVE) else UNKNOWN
        if name == "sqrt":
            if ca in (AFFINE, CONCAVE):
                return CONCAVE
            return CONVEX if norm_convex(node.args[0]) else UNKNOWN
        return UNKNOWN
    return UNKNOWN


def body_curvature(expr):
    pd = expr.polynomial_degree()
    if pd is not None and pd <= 1:
        return AFFINE if pd == 1 else CONST
    if pd == 2:
        return quadratic_curvature(expr)
    return curvature(expr)


def classify_constraint(con):
    """Return (is_nonlinear, is_convex, curvature, kind)."""
    from pyomo.core.expr.numvalue import value

    body = con.body
    pd = body.polynomial_degree()
    if pd is not None and pd <= 1:
        return False, True, AFFINE, "linear"
    curv = body_curvature(body)
    if con.equality:
        return True, False, curv, "nonlinear-equality"
    lb = con.lower
    ub = con.upper
    has_lb = lb is not None and math.isfinite(value(lb))
    has_ub = ub is not None and math.isfinite(value(ub))
    if has_lb and has_ub:
        return True, False, curv, "nonlinear-ranged"
    if has_ub:
        return True, curv in (CONVEX, AFFINE, CONST), curv, "body<=ub"
    if has_lb:
        return True, curv in (CONCAVE, AFFINE, CONST), curv, "body>=lb"
    return True, True, curv, "unbounded"


def analyze(m):
    from pyomo.core import BooleanVar, Constraint, Objective, Var, Block, LogicalConstraint
    from pyomo.gdp import Disjunct, Disjunction
    from pyomo.util.model_size import build_model_size_report

    rep = build_model_size_report(m)
    out = {
        "n_vars": rep.activated.variables,
        "n_binary": rep.activated.binary_variables,
        "n_integer": rep.activated.integer_variables,
        "n_continuous": rep.activated.continuous_variables,
        "n_vars_overall": rep.overall.variables,
        "n_cons": rep.activated.constraints,
        "n_disjunctions": rep.activated.disjunctions,
        "n_disjuncts": rep.activated.disjuncts,
        "n_boolean": sum(1 for _ in m.component_data_objects(BooleanVar, descend_into=(Block, Disjunct))),
        "n_logical_cons": sum(1 for _ in m.component_data_objects(LogicalConstraint, active=True, descend_into=(Block, Disjunct))),
    }
    nonconvex_examples = []
    stats = {"global": [0, 0, 0], "disjunct": [0, 0, 0]}  # [cons, nonlinear, nonconvex]
    curv_hist = {}

    def visit(cons, where):
        for c in cons:
            nl, cvx, curv, kind = classify_constraint(c)
            stats[where][0] += 1
            if nl:
                stats[where][1] += 1
                curv_hist[curv] = curv_hist.get(curv, 0) + 1
                if not cvx:
                    stats[where][2] += 1
                    if len(nonconvex_examples) < 8:
                        nonconvex_examples.append(f"{c.name} [{where}] {kind} curv={curv}")

    visit(m.component_data_objects(Constraint, active=True, descend_into=Block), "global")
    for d in m.component_data_objects(Disjunct, active=True, descend_into=(Block, Disjunct)):
        visit(d.component_data_objects(Constraint, active=True, descend_into=Block), "disjunct")

    objs = list(m.component_data_objects(Objective, active=True, descend_into=(Block, Disjunct)))
    if len(objs) != 1:
        obj_class, obj_ok = f"{len(objs)} objectives", False
    else:
        o = objs[0]
        pd = o.expr.polynomial_degree()
        if pd is not None and pd <= 1:
            obj_class, obj_ok = "linear", True
        else:
            curv = body_curvature(o.expr)
            need = CONVEX if o.is_minimizing() else CONCAVE
            obj_ok = curv in (need, AFFINE, CONST)
            obj_class = f"nonlinear {curv} ({'min' if o.is_minimizing() else 'max'})"
    out.update(
        n_cons_global=stats["global"][0],
        n_cons_disjunct=stats["disjunct"][0],
        n_nl=stats["global"][1] + stats["disjunct"][1],
        n_nl_global=stats["global"][1],
        n_nl_disjunct=stats["disjunct"][1],
        n_nonconvex=stats["global"][2] + stats["disjunct"][2],
        n_nonconvex_global=stats["global"][2],
        n_nonconvex_disjunct=stats["disjunct"][2],
        nl_curvature_hist=curv_hist,
        obj_class=obj_class,
        obj_convex=obj_ok,
        nonconvex_examples=nonconvex_examples,
    )
    if out["n_nl"] == 0 and obj_class == "linear":
        cls = "linear"
    elif out["n_nonconvex"] == 0 and obj_ok:
        cls = "convex"
    else:
        cls = "nonconvex"
    out["classification"] = cls
    return out


def analyze_one(name):
    import gdp_instances

    t0 = time.time()
    m = gdp_instances.INSTANCES[name]()
    build_time = time.time() - t0
    t0 = time.time()
    res = analyze(m)
    res["build_time"] = round(build_time, 2)
    res["analyze_time"] = round(time.time() - t0, 2)
    return res


def run_all(jobs, timeout):
    import gdp_instances

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    names = list(gdp_instances.INSTANCES)

    def work(name):
        out = RESULT_DIR / f"{name}.json"
        if out.exists():
            return name
        env = dict(os.environ, MPLBACKEND="Agg", **SINGLE_THREAD_ENV)
        try:
            p = subprocess.run(
                [sys.executable, __file__, "--name", name],
                capture_output=True, text=True, timeout=timeout, env=env, cwd=HERE,
            )
            if p.returncode == 0:
                lines = [l for l in p.stdout.splitlines() if l.startswith("{")]
                res = json.loads(lines[-1])
            else:
                res = {"build_error": (p.stderr.strip().splitlines() or ["?"])[-1][:300]}
        except subprocess.TimeoutExpired:
            res = {"build_error": f"timeout after {timeout}s"}
        out.write_text(json.dumps(res, indent=1))
        print(name, res.get("classification", res.get("build_error")), flush=True)
        return name

    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(work, names))
    catalog = {n: json.loads((RESULT_DIR / f"{n}.json").read_text()) for n in names}
    (HERE / "gdp_catalog.json").write_text(json.dumps(catalog, indent=1))
    print("wrote gdp_catalog.json with", len(catalog), "entries")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    if a.name:
        try:
            print(json.dumps(analyze_one(a.name)))
        except Exception:
            traceback.print_exc()
            sys.exit(1)
    elif a.all:
        run_all(a.jobs, a.timeout)
