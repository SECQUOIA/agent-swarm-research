"""Independent dense KKT MILP comparison for the exact screening prototype.

Run: python code/bilevel_reopened/screening_milp_comparison.py
Reuses the published synthetic instances and screened implementation, but
constructs the comparison model and checks returned solutions separately.
"""
import json
import platform
import time
import warnings
from pathlib import Path
from unittest.mock import patch

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
import sympy as sp

import approximate_structure_checks as source


def dense_kkt_milp(Q, c, C, objective, upper_rows, lo=0, hi=1):
    """Build an independent MILP with x,z and lower/upper activity binaries.

    For g_i=Q_i*z+c_i+C_i*x, |g_i| is at most
    |c_i|+|C_i| max(|lo|,|hi|)+sum_j |Q_ij| on the box.
    The added unit slack avoids rounding a valid bound inward during binary64
    conversion on these bounded synthetic inputs.
    """
    n, nv = Q.rows, 1+3*Q.rows
    bounds_lo, bounds_hi = np.zeros(nv), np.ones(nv)
    bounds_lo[0], bounds_hi[0] = float(lo), float(hi)
    integrality = np.zeros(nv)
    integrality[1+n:] = 1
    cost = np.zeros(nv)
    cost[0] = float(objective[0])
    cost[1:1+n] = [float(v) for v in objective[1]]
    matrix, lower, upper = [], [], []
    big_m = []

    def add(coefficients, lb=-np.inf, ub=np.inf):
        matrix.append(coefficients)
        lower.append(lb)
        upper.append(ub)

    for i in range(n):
        zi, li, ui = 1+i, 1+n+i, 1+2*n+i
        M = 1+abs(c[i])+abs(C[i])*max(abs(lo), abs(hi))+sum(abs(Q[i,j]) for j in range(n))
        big_m.append(str(M))
        row = np.zeros(nv)
        row[zi], row[li] = 1, 1
        add(row, ub=1)                    # l_i=1 => z_i=0
        row = np.zeros(nv)
        row[zi], row[ui] = 1, -1
        add(row, lb=0)                    # u_i=1 => z_i=1
        row = np.zeros(nv)
        row[li], row[ui] = 1, 1
        add(row, ub=1)
        gradient = np.zeros(nv)
        gradient[0] = float(C[i])
        gradient[1:1+n] = [float(Q[i,j]) for j in range(n)]
        row = gradient.copy()
        row[li] = -float(M)
        add(row, ub=-float(c[i]))         # g_i <= M l_i
        row = gradient.copy()
        row[ui] = float(M)
        add(row, lb=-float(c[i]))         # g_i >= -M u_i
    for a, b, rhs in upper_rows:
        row = np.zeros(nv)
        row[0] = float(a)
        row[1:1+n] = [float(v) for v in b]
        add(row, ub=float(rhs))
    return dict(c=cost, integrality=integrality,
                bounds=Bounds(bounds_lo, bounds_hi),
                constraints=LinearConstraint(np.asarray(matrix), lower, upper)), big_m


def exact_check(Q, c, C, objective, rows, answer):
    value, x, z, _ = answer
    assert 0 <= x <= 1
    n = Q.rows
    for i in range(n):
        gradient = c[i]+C[i]*x+sum(Q[i,j]*z[j] for j in range(n))
        assert 0 <= z[i] <= 1
        assert gradient >= 0 if z[i] == 0 else gradient <= 0 if z[i] == 1 else gradient == 0
    slacks = [rhs-a*x-sum(b[i]*z[i] for i in range(n)) for a,b,rhs in rows]
    assert all(s >= 0 for s in slacks)
    assert value == objective[0]*x+sum(objective[1][i]*z[i] for i in range(n))
    return {"exact_box_KKT": True, "exact_upper_feasibility": True,
            "exact_objective_evaluation": True, "upper_slacks": list(map(str, slacks))}


def finite_or_none(value):
    return float(value) if value is not None and np.isfinite(value) else None


def tighten_numerical_comparison(model, exact_value):
    """One bounded follow-up when the default MILP differs by over 1e-7.

    The installed SciPy wrapper forwards these solver-specific settings to
    HiGHS and emits a warning; retain that warning in the saved evidence.
    """
    start = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = milp(**model, options={"time_limit": 30, "mip_rel_gap": 0,
                                       "mip_feasibility_tolerance": 1e-9,
                                       "primal_feasibility_tolerance": 1e-9})
    primal = finite_or_none(result.fun)
    dual = finite_or_none(getattr(result, "mip_dual_bound", None))
    report = {"solve_seconds": time.perf_counter()-start,
              "status_code": int(result.status), "message": result.message,
              "warnings": [str(w.message) for w in caught],
              "requested_mip_feasibility_tolerance": 1e-9,
              "requested_primal_feasibility_tolerance": 1e-9,
              "primal_objective": primal, "dual_bound": dual,
              "primal_minus_exact": None if primal is None else primal-exact_value,
              "exact_minus_dual": None if dual is None else exact_value-dual}
    if result.x is not None:
        lhs = model["constraints"].A@result.x
        report["max_linear_violation"] = float(max(0, np.max(model["constraints"].lb-lhs),
                                                    np.max(lhs-model["constraints"].ub)))
    return report


def run_case(n):
    start = time.perf_counter()
    Q, Qhat, c, C, objective, rows = source.dense_family(n)
    row = {"N": n, "seed": 101, "perturbation_scale": 10000,
           "generation_seconds": time.perf_counter()-start,
           "leader_objective_coefficient": str(objective[0]),
           "response_objective_coefficients": list(map(str, objective[1])),
           "upper_constraints": [{"leader": str(a), "response": list(map(str,b)), "rhs": str(rhs)}
                                 for a,b,rhs in rows]}
    start = time.perf_counter()
    cells = source.diagonal_cells([sp.Rational(1)]*n, c, C)
    row["surrogate_cover_seconds"] = time.perf_counter()-start
    timings = {"screening_seconds": 0.0, "recovery_seconds": 0.0}
    original_screen, original_recovery = source.screen, source.solve_status

    def timed_screen(*args, **kwargs):
        tick = time.perf_counter()
        try:
            return original_screen(*args, **kwargs)
        finally:
            timings["screening_seconds"] += time.perf_counter()-tick

    def timed_recovery(*args, **kwargs):
        tick = time.perf_counter()
        try:
            return original_recovery(*args, **kwargs)
        finally:
            timings["recovery_seconds"] += time.perf_counter()-tick

    answer = None
    start = time.perf_counter()
    try:
        with patch.object(source, "screen", timed_screen), patch.object(source, "solve_status", timed_recovery):
            answer, stats = source.optimize_screened(Q, Qhat, c, C, cells, objective, rows)
        row["screened_solver_seconds"] = time.perf_counter()-start
        row["screened_status"] = "optimal" if answer is not None else "infeasible"
        row["screened_counts"] = stats
        if answer is not None:
            row["exact_optimum"], row["exact_leader"] = str(answer[0]), str(answer[1])
            tick = time.perf_counter()
            row["exact_solution_checks"] = exact_check(Q, c, C, objective, rows, answer)
            row["exact_verification_seconds"] = time.perf_counter()-tick
    except Exception as exc:
        row["screened_solver_seconds"] = time.perf_counter()-start
        row["screened_status"] = "error"
        row["screened_error"] = f"{type(exc).__name__}: {exc}"
    row.update(timings)
    row["other_screened_solver_seconds"] = row["screened_solver_seconds"]-sum(timings.values())

    try:
        start = time.perf_counter()
        model, big_m = dense_kkt_milp(Q, c, C, objective, rows)
        row["milp_formulation_seconds"] = time.perf_counter()-start
        row["big_m_exact_rows"] = big_m
        start = time.perf_counter()
        result = milp(**model, options={"time_limit": 30, "mip_rel_gap": 0})
        row["milp_solve_seconds"] = time.perf_counter()-start
        row["milp_status_code"], row["milp_message"] = int(result.status), result.message
        row["milp_primal_objective"] = finite_or_none(result.fun)
        row["milp_dual_bound"] = finite_or_none(getattr(result, "mip_dual_bound", None))
        row["milp_relative_gap"] = finite_or_none(getattr(result, "mip_gap", None))
        nodes = getattr(result, "mip_node_count", None)
        row["milp_nodes"] = int(nodes) if nodes is not None else None
        if result.x is not None:
            lhs = model["constraints"].A@result.x
            row["milp_max_linear_violation"] = float(max(0, np.max(model["constraints"].lb-lhs),
                                                         np.max(lhs-model["constraints"].ub)))
            binary = result.x[1+n:]
            row["milp_max_integrality_violation"] = float(np.max(abs(binary-np.round(binary))))
        if answer is not None and row["screened_status"] == "optimal":
            exact_float = float(answer[0])
            primal, dual = row["milp_primal_objective"], row["milp_dual_bound"]
            row["numerical_primal_minus_exact"] = None if primal is None else primal-exact_float
            row["exact_minus_numerical_dual"] = None if dual is None else exact_float-dual
            row["absolute_objective_difference"] = None if primal is None else abs(primal-exact_float)
            row["agreement_within_1e_7"] = (result.status == 0 and primal is not None
                                             and abs(primal-exact_float) <= 1e-7)
            if primal is not None and abs(primal-exact_float) > 1e-7:
                row["tighter_tolerance_followup"] = tighten_numerical_comparison(model, exact_float)
    except Exception as exc:
        row["milp_status_code"] = "error"
        row["milp_error"] = f"{type(exc).__name__}: {exc}"
    return row


def main():
    report = {"description": "Independent dense KKT MILP versus exact screened recovery; synthetic single-run timings",
              "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "sympy": sp.__version__,
              "milp_time_limit_seconds": 30, "cases": []}
    path = Path(__file__).with_name("screening_milp_comparison.json")
    for n in (8, 12, 20, 40):
        row = run_case(n)
        report["cases"].append(row)
        path.write_text(json.dumps(report, indent=2)+"\n")
        print(json.dumps({k: row[k] for k in ("N", "screened_status", "screened_solver_seconds",
                                               "milp_status_code")}
                         | {k: row.get(k) for k in ("milp_solve_seconds", "absolute_objective_difference")}), flush=True)


if __name__ == "__main__":
    main()
