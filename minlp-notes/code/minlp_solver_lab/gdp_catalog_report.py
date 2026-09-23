"""Write notes/gdp-instance-catalog-<date>.md from gdp_catalog.json and
gdp_solve_results.json."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent.parent / "notes"

CAT = json.load(open(HERE / "gdp_catalog.json"))
SOL = json.load(open(HERE / "gdp_solve_results.json")) if (HERE / "gdp_solve_results.json").exists() else {}

# Hand-written notes for instances whose classification deserves context.
NOTES_BY_NAME = {
    "pyomo.eight_process.model": "Duran-Grossmann Ex. 3 (8PP). Nonlinear relations are equalities exp(x)-1 == y; the classic convex GDP uses <=.",
    "pyomo.eight_process.logical": "8PP with LogicalConstraints; same equality-form nonlinearities as .model.",
    "pyomo.nine_process": "Equality-form exp/log stage relations; convex if written as inequalities.",
    "pyomo.nine_process.nonexclusive": "As pyomo.nine_process, with non-exclusive disjunctions.",
    "gdplib.biofuel": "Only nonconvexity: cost == sqrt(dx^2+dy^2) distance equalities in disjuncts (convex if ==  -> >=).",
    "gdplib.modprodnet.Growth": "Only nonconvexity: cost == base*(size/25)^0.6 equality (concave cost curve).",
    "gdplib.modprodnet.Dip": "As Growth.",
    "gdplib.modprodnet.Decay": "As Growth.",
    "gdplib.spectralog": "Nonlinear equalities eq1 (log-linear regressions).",
    "gdplib.pandemic": "SEIR ODE collocation with u*s*i trilinear terms; genuinely nonconvex.",
    "gdplib.grid": "12500 disjunctions / 47.5k vars; LP disjuncts. Too large for 120 s runs.",
    "pyomo.farm_layout.FLay02": "area/width - length <= 0 is convex on width > 0 (Var lb 0); MINLPLib treats FLay as convex.",
    "gdplib.ex1_linan_2023": "Six-hump camel polynomial objective (degree 6): nonconvex objective, linear disjuncts.",
    "gdplib.reverse_electrodialysis": "Built with solve_stack=False (skips GAMS/IPOPTH pre-solve).",
    "pyomo.two_rxn_lee.mccormick": "McCormick-relaxed variant: linear GDP (relaxation of the bilinear model).",
    "gdplib.mod_hens.conventional": "LMTD (Chen/Cafaro) equalities plus area^0.6 cost; nonconvex.",
    "pyomo_tests.four_stage_dynamic": "Discretised ODE with mode disjunctions; nonlinear equalities and concave objective.",
    "pyomo.constrained_layout.CLay0203.l1": "l1 objective (linear) with convex quadratic circle constraints inside disjuncts; matches MINLPLib clay*m.",
    "pyomo.constrained_layout.CLay0203.l2": "l2 objective sum of Euclidean norms (convex) + quadratic disjunct constraints.",
    "gdplib.stranded_gas.base": "45k integer vars; learning-factor equality with fractional power. Too large for 120 s.",
}


def fmt(x, nd=6):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.{nd}g}"
    return str(x)


def agree(a, b, sense):
    va, vb = a.get("objective"), b.get("objective")
    if va is None or vb is None:
        return "n/a"
    tol = 1e-4 * max(1.0, abs(va), abs(vb))
    if abs(va - vb) <= tol:
        return "yes"
    # LOA is a local method: a worse LOA value is consistent, a better one is not
    better = (va < vb - tol) if sense == "min" else (va > vb + tol)
    if better:
        return "no (LOA better)"
    return "no (LOA worse)"


def short_tc(r):
    if r is None:
        return "not run"
    if "error" in r:
        e = r["error"]
        if "hard timeout" in e:
            return "killed@600s"
        return "error"
    tc = r.get("termination", "?")
    return {"optimal": "opt", "maxTimeLimit": "tlim", "feasible": "feas", "infeasible": "infeas",
            "locallyOptimal": "locopt", "maxIterations": "iter", "unbounded": "unbdd",
            "noSolution": "nosol", "other": "other", "unknown": "unk"}.get(tc, tc)


def main():
    today = date.today().isoformat() if len(sys.argv) < 2 else sys.argv[1]
    out = NOTES / f"gdp-instance-catalog-{today.replace('-', '')}.md"
    names = list(CAT)
    built = [n for n in names if not CAT[n].get("build_error")]
    failed = [n for n in names if CAT[n].get("build_error")]
    by_cls = {}
    for n in built:
        by_cls.setdefault(CAT[n]["classification"], []).append(n)
    src = lambda n: n.split(".")[0]

    L = []
    L.append(f"# Convex GDP instance catalog ({today})\n")
    L.append("Purpose: inventory of Pyomo GDP test instances on this machine for benchmarking the new logic-based "
             "decomposition algorithm, with size, convexity classification, and reference solves.\n")
    L.append("Code: `code/minlp_solver_lab/gdp_instances.py` (loader, `INSTANCES`, `convex_instances()`), "
             "`gdp_catalog_analyze.py` (sizes + convexity), `gdp_catalog_solve.py` (reference solves), "
             "`gdp_catalog_report.py` (this note). Raw results: `gdp_catalog.json`, `gdp_solve_results.json`, "
             "`gdp_catalog_results/`.\n")
    L.append("## Sources\n")
    L.append("- `gdplib.*`: GDPlib editable install at `instances/gdplib_src` (all 24 packages, plus documented case variants).")
    L.append("- `pyomo.*`: Pyomo `examples/gdp` from a sparse git checkout of tag 6.10.1 at "
             "`instances/pyomo_examples_src` (the pip wheel does not ship the examples directory). "
             "AbstractModel examples are instantiated with the `.dat` files next to them.")
    L.append("- `pyomo_tests.*`: models defined inside `pyomo.contrib.gdpopt.tests` (`four_stage_dynamic_model`). "
             "`pyomo/gdp/tests/models.py` only holds unit-test toys (1-4 variable boxes/circles) and was not cataloged.\n")
    L.append("## Method\n")
    L.append("- Sizes: `pyomo.util.model_size.build_model_size_report` (activated counts; binaries include disjunct indicator variables). "
             "Constraints are split into global (outside any disjunct) and inside active disjuncts.")
    L.append("- Convexity: each nonlinear constraint body is classified by a DCP-style walk of the Pyomo expression tree "
             "(degree-2 bodies via Hessian eigenvalues from the quadratic standard repn; exp/log/sqrt/abs/power/norm/c-over-x rules with FBBT bounds). "
             "A constraint is convex when the body is convex for `body <= ub`, concave for `body >= lb`. Nonlinear equalities and nonlinear ranged "
             "constraints are nonconvex. Unknown curvature is treated as nonconvex. Model classes: `linear` (no nonlinear constraints, linear objective), "
             "`convex` (all nonlinear constraints convex in their direction and convex objective), `nonconvex`.")
    L.append("- Reference solves (120 s each, 2 threads per solve, 4 solves in parallel = 8 threads): "
             "GDPopt LOA (nlp ipopt, mip gurobi; MINLP subproblems to GAMS/DICOPT) and GAMS/BARON on `core.logical_to_linear` + `gdp.bigm` "
             "(optcr 1e-4, optca 1e-6). Each solve runs in a subprocess killed after 600 s wall. BARON lower bound = OBJEST, objective = OBJVAL.")
    L.append("- Agreement: `yes` if both objective values are within 1e-4 relative; LOA is a local method so `no (LOA worse)` is expected on nonconvex models.\n")

    L.append("## Summary\n")
    L.append(f"- Registered {len(names)} instances; {len(built)} build, {len(failed)} fail.")
    for cls in ("convex", "linear", "nonconvex"):
        L.append(f"- {cls}: {len(by_cls.get(cls, []))}")
    L.append("")
    L.append("Convex GDP instances (`convex_instances()`):\n")
    for n in by_cls.get("convex", []):
        d = CAT[n]
        L.append(f"- `{n}`: {d['n_vars']} vars ({d['n_binary']} bin), {d['n_cons']} cons, {d['n_disjunctions']} disjunctions, "
                 f"{d['n_nl']} nonlinear cons ({d['n_nl_disjunct']} in disjuncts), objective {d['obj_class']}")
    L.append("")
    L.append("Linear GDP instances (no nonlinear constraints; useful as sanity checks): " +
             ", ".join(f"`{n}`" for n in by_cls.get("linear", [])) + "\n")

    if failed:
        L.append("## Build failures\n")
        for n in failed:
            L.append(f"- `{n}`: {CAT[n]['build_error']}")
        L.append("")

    L.append("## Table 1: size and convexity\n")
    L.append("vars/bin/int = activated variables, binaries (incl. indicator vars), integers; cons = active constraints; "
             "disj = disjunctions; djct = disjuncts; nl = nonlinear constraints (global + in-disjunct); ncvx = nonlinear constraints not convex in their direction.\n")
    L.append("| instance | vars | bin | int | cons | disj | djct | nl (glob/disj) | ncvx | objective | class | note |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
    for n in names:
        d = CAT[n]
        if d.get("build_error"):
            L.append(f"| `{n}` | | | | | | | | | | BUILD FAIL | {d['build_error'][:80]} |")
            continue
        note = NOTES_BY_NAME.get(n, "")
        L.append(f"| `{n}` | {d['n_vars']} | {d['n_binary']} | {d['n_integer']} | {d['n_cons']} | {d['n_disjunctions']} | {d['n_disjuncts']} | "
                 f"{d['n_nl']} ({d['n_nl_global']}/{d['n_nl_disjunct']}) | {d['n_nonconvex']} | {d['obj_class']} | **{d['classification']}** | {note} |")
    L.append("")

    L.append("## Table 2: reference solves (120 s limit)\n")
    L.append("LOA: GDPopt LOA objective, status, wall s. BARON: objective (incumbent), lower bound, status, solver s, transformation. "
             "Status codes: opt = optimal, tlim = time limit, locopt = locally optimal, feas = feasible, infeas = infeasible, killed@600s = subprocess hard timeout, error = exception (see JSON).\n")
    L.append("| instance | class | LOA obj | LOA status | LOA s | BARON obj | BARON lb | BARON status | BARON s | transf. | agree |")
    L.append("|---|---|---:|---|---:|---:|---:|---|---:|---|---|")
    for n in names:
        d = CAT[n]
        if d.get("build_error"):
            continue
        s = SOL.get(n, {})
        a, b = s.get("loa"), s.get("baron")
        sense = (a or b or {}).get("sense", "min")
        tr = ""
        if b and b.get("transformation"):
            tr = "bigm" if b["transformation"] == "gdp.bigm" else "hull*"
        L.append(f"| `{n}` | {d['classification']} | {fmt((a or {}).get('objective'))} | {short_tc(a)} | {fmt((a or {}).get('wall_time'), 4)} | "
                 f"{fmt((b or {}).get('objective'))} | {fmt((b or {}).get('lower_bound'))} | {short_tc(b)} | {fmt((b or {}).get('solver_time'), 4)} | {tr} | "
                 f"{agree(a or {}, b or {}, sense) if a and b else 'n/a'} |")
    L.append("")
    L.append("`hull*` = `gdp.bigm` raised (missing M values) and `gdp.hull` was used instead; see `transformation` in the JSON for the error.\n")

    errs = [(n, m, r["error"]) for n in names for m in ("loa", "baron") for r in [SOL.get(n, {}).get(m)] if r and "error" in r]
    if errs:
        L.append("## Solve errors\n")
        for n, m, e in errs:
            L.append(f"- `{n}` {m}: {e[:200]}")
        L.append("")

    L.append("## Caveats\n")
    L.append("- Classification is syntactic and conservative: `unknown` curvature counts as nonconvex, so a model marked nonconvex may still be convex under a reformulation. "
             "Nonlinear equalities that are convex-in-one-direction (8PP, nine_process, biofuel, modprodnet, spectralog) are flagged in the notes; relaxing them to inequalities is a modelling decision, not done here.")
    L.append("- `c/x` terms are accepted as convex when the variable lower bound is 0 (domain x > 0), the MINLPLib convention for FLay.")
    L.append("- Sizes count active components on the untransformed GDP; the fixed indicator variables of deactivated disjuncts (e.g. gdp_col partial condenser) are excluded.")
    L.append("- LOA time limits are checked between iterations; subsolver limits (gurobi TimeLimit, ipopt max_cpu_time, GAMS reslim) are set to 120 s but a single slow subproblem can push wall time past 120 s.")
    out.write_text("\n".join(L) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
