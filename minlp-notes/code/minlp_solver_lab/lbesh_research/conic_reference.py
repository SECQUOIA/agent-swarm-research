"""Exact cone references for five supported controlled families, solved numerically.

Independent CVXPY/Clarabel construction from generator coefficients; it does
not use Pyomo expressions, LB-ESH extraction, cuts, or epsilon perspectives.
``solve(name)`` solves the continuous hull root; ``enumerate_small(name)``
solves every fixed assignment using direct cones. Numerical dual objectives
are retained as estimates, not rigorous certificates. Supports exp, log,
reciprocal, quadratic, and logsumexp; other families are explicitly rejected.
Run in conic_reference_env.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import cvxpy as cp
import numpy as np

from .instances import MANIFEST, parameters


SUPPORTED_FAMILIES = ("exp", "log", "reciprocal", "quadratic", "logsumexp")


class UnsupportedConicReference(ValueError):
    """This reference has no verified cone formulation for the requested family."""


def _require_supported(name):
    family = MANIFEST[name]["family"]
    if family not in SUPPORTED_FAMILIES:
        raise UnsupportedConicReference(
            f"No verified cone formulation is implemented for family {family!r}; "
            f"supported families: {', '.join(SUPPORTED_FAMILIES)}")


def _phi_cone(z, y, law, constraints):
    """Epigraph of y*phi(z/y), with its closed value at y=z=0."""
    q = cp.Variable(nonneg=True)
    if law == "exp":
        constraints.append(cp.ExpCone(3*z, y, (math.exp(1.5)-1)*q+y))
    elif law == "log":
        constraints.append(cp.ExpCone(-math.log(2)*q, y, y-z))
    elif law == "reciprocal":
        # (q+y)(y-z) >= y^2, factors nonnegative.
        a, b = q+y, y-z
        constraints.append(cp.SOC(a+b, cp.hstack([2*y, a-b])))
    elif law == "quadratic":
        # q*y >= 4*z^2, factors nonnegative.
        constraints.append(cp.SOC(q+y, cp.hstack([4*z, q-y])))
    else:
        raise ValueError(law)
    return q


def _upper_cost(d, law):
    # Independently evaluate the generator's declared box-based epigraph bound.
    def phi(z):
        return {"exp": lambda: math.expm1(3*z)/math.expm1(1.5),
                "log": lambda: -math.log1p(-z)/math.log(2),
                "reciprocal": lambda: 1/(1-z)-1,
                "quadratic": lambda: 4*z*z}[law]()
    return 1.05*d["capacity"]*max(d["operating"][1:])*(sum(d["weight"])+d["cross"])*phi(1/1.1)


def _build(name, modes=None):
    _require_supported(name)
    info, data = MANIFEST[name], parameters(name)
    n, law = info["units"], info["family"]
    if modes is not None and (len(modes) != n or any(j not in (0, 1, 2) for j in modes)):
        raise ValueError("modes must have one member of {0,1,2} per unit")
    x = cp.Variable((n, 2), name="x")
    y = cp.Variable((n, 3), name="y") if modes is None else np.eye(3)[list(modes)]
    cons = [y >= 0, y <= 1, cp.sum(y, axis=1) == 1] if modes is None else []
    if law == "logsumexp":
        t = cp.Variable(name="t")
        cons += [x >= -2, x <= 2, t >= 0, t <= 9*n,
                 cp.sum(x[:, 0]) >= 0, cp.sum(x[:, 1]) >= .1*n,
                 cp.sum_squares(cp.hstack([x[i, 0]-.5*x[(i+1)%n, 1] for i in range(n)])) <= t,
                 cp.sum_squares(cp.hstack([x[i, p]-x[(i+1)%n, p] for i in range(n) for p in range(2)])) <= .55*n]
        for i, d in enumerate(data):
            parts = []
            for j in (range(3) if modes is None else [modes[i]]):
                u = cp.Variable(2) if modes is None else x[i, :]
                lam = y[i, j]
                if modes is None:
                    cons += [u >= -2*lam, u <= 2*lam]
                    parts.append(u)
                r = cp.Variable(4, nonneg=True)
                k = 0
                for p in range(2):
                    for sign in (-1, 1):
                        cons.append(cp.ExpCone(sign*d["scale"][j][p]*(u[p]-d["centers"][j][p]*lam), lam, r[k]))
                        k += 1
                cons.append(cp.sum(r) <= d["radius"][j]*lam)
            if modes is None:
                cons.append(x[i, :] == sum(parts))
        obj = sum(data[i]["price"][p]*x[i, p] for i in range(n) for p in range(2)) + .1*t + sum(data[i]["fixed"][j]*y[i, j] for i in range(n) for j in range(3))
    else:
        t = cp.Variable(n, name="t")
        witness = np.array([[.28*d["capacity"], .22*d["capacity"]] for d in data])
        resource = np.array([d["resource"] for d in data])
        cap = np.array([d["capacity"] for d in data])
        upper = np.array([_upper_cost(d, law) for d in data])
        congestion_limit = 1.08*sum(((witness[i, 0]+.35*witness[(i+1)%n, 1])/cap[i])**2 for i in range(n))
        cons += [x >= 0, x <= cap[:, None], cp.sum(x, axis=1) <= cap,
                 t >= 0, t <= upper, cp.sum(x, axis=0) >= np.sum(witness, axis=0),
                 cp.sum(cp.multiply(resource, x)) <= 1.08*np.sum(resource*witness),
                 cp.sum_squares(cp.hstack([(x[i, 0]+.35*x[(i+1)%n, 1])/cap[i] for i in range(n)])) <= congestion_limit]
        for i, d in enumerate(data):
            parts_x, parts_t = [], []
            for j in (range(3) if modes is None else [modes[i]]):
                lam = y[i, j]
                u = cp.Variable(2) if modes is None else x[i, :]
                v = cp.Variable() if modes is None else t[i]
                if modes is None:
                    cons += [u >= 0, u <= cap[i]*lam, v >= 0, v <= upper[i]*lam]
                    parts_x.append(u)
                    parts_t.append(v)
                cons.append(cp.sum(u) <= cap[i]*d["mode_capacity"][j]*lam)
                if j == 0:
                    cons.append(v == 0)
                else:
                    domain = 1.1*cap[i]
                    terms = [_phi_cone(u[p]/domain, lam, law, cons) for p in range(2)]
                    cross = _phi_cone(cp.sum(u)/(2*domain), lam, law, cons)
                    cons.append(cap[i]*d["operating"][j]*(sum(d["weight"][p]*terms[p] for p in range(2))+d["cross"]*cross) <= v)
            if modes is None:
                cons += [x[i, :] == sum(parts_x), t[i] == sum(parts_t)]
        obj = cp.sum(t)+sum(cap[i]*data[i]["fixed"][j]*y[i, j] for i in range(n) for j in range(3))
    return cp.Problem(cp.Minimize(obj), cons), x, t, y


def solve(name, *, modes=None, time_limit=300, tolerance=1e-9):
    """Numerically solve an exact cone hull root or fixed-assignment subproblem.

    All timings include CVXPY construction and canonicalization. ``lb`` is only
    a numerical dual estimate; ``bound_certified`` is always false. Fixed
    assignments use direct cones, avoiding zero-weight perspective degeneracy.
    """
    start = time.perf_counter()
    problem, x, t, y = _build(name, modes)
    problem.solve(solver="CLARABEL", verbose=False, max_threads=1,
                  time_limit=float(time_limit), max_iter=300,
                  tol_gap_abs=tolerance, tol_gap_rel=tolerance, tol_feas=tolerance)
    raw = problem._solver_cache["CLARABEL"].get_solution()
    info = problem._solver_cache["CLARABEL"].get_info()
    finite = lambda v: float(v) if v is not None and math.isfinite(v) else None
    solved = problem.status in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE)
    witness = {}
    if solved:
        n = MANIFEST[name]["units"]
        witness.update({f"x[{i},{p}]": float(x.value[i, p]) for i in range(n) for p in range(2)})
        if MANIFEST[name]["family"] == "logsumexp":
            witness["t"] = float(t.value)
        else:
            witness.update({f"t[{i}]": float(t.value[i]) for i in range(n)})
        values = y.value if modes is None else y
        witness.update({f"mode[{i},{j}].binary_indicator_var": float(values[i, j]) for i in range(n) for j in range(3)})
    # Canonical conic objectives omit objective constants at fixed assignments.
    data = parameters(name)
    offset = (sum(data[i]["fixed"][j] * (1. if MANIFEST[name]["family"] == "logsumexp"
                         else data[i]["capacity"]) for i, j in enumerate(modes))
              if modes is not None else 0.)
    return {"name": name, "method": "clarabel_exact_cone_root" if modes is None else "clarabel_fixed_assignment",
            "status": problem.status, "obj": finite(problem.value) if solved else None,
            "lb": finite(raw.obj_val_dual+offset) if solved else None,
            "bound_certified": False, "bound_kind": "floating_point_conic_dual_estimate",
            "witness": witness, "modes": None if modes is None else list(modes),
            "relax_integrality": modes is None, "time": time.perf_counter()-start,
            "solver_runtime": float(raw.solve_time), "iterations": int(raw.iterations),
            "raw_status": str(raw.status), "primal_residual": finite(raw.r_prim),
            "dual_residual": finite(raw.r_dual), "gap_abs": finite(info.gap_abs),
            "threads": int(info.linsolver.threads), "tolerance": tolerance,
            "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in (Path(__file__), Path(__file__).with_name("instances.py"))},
            "environment_lock_sha256": hashlib.sha256((Path(__file__).parent / "conic_reference_env" / "uv.lock").read_bytes()).hexdigest(),
            "versions": {p: importlib.metadata.version(p) for p in ("cvxpy", "clarabel", "numpy", "scipy", "pyomo")}}


def enumerate_small(name, *, time_limit=300, tolerance=1e-9):
    """Exhaust all 27 assignments; globality remains numerical, not rigorous."""
    _require_supported(name)
    if MANIFEST[name]["units"] > 3:
        raise ValueError("Exhaustive enumeration is restricted to at most 3 units")
    start = time.perf_counter()
    rows = [solve(name, modes=modes, time_limit=time_limit, tolerance=tolerance)
            for modes in itertools.product(range(3), repeat=MANIFEST[name]["units"])]
    feasible = [r for r in rows if r["status"] == "optimal"]
    unresolved = [r for r in rows if r["status"] not in ("optimal", "infeasible")]
    best = min(feasible, key=lambda r: r["obj"]) if feasible else None
    return {"name": name, "method": "clarabel_exhaustive_cone_enumeration",
            "status": "unresolved" if unresolved else "optimal" if best else "infeasible",
            "obj": best["obj"] if best else None,
            "lb": min(r["lb"] for r in feasible) if feasible and not unresolved else None,
            "bound_certified": False, "bound_kind": "floating_point_conic_dual_estimate",
            "witness": best["witness"] if best else {}, "modes": best["modes"] if best else None,
            "time": time.perf_counter()-start, "assignments": len(rows),
            "unresolved_assignments": len(unresolved), "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, choices=tuple(MANIFEST))
    parser.add_argument("--enumerate", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = (enumerate_small if args.enumerate else solve)(args.name)
    except UnsupportedConicReference as exc:
        result = {"name": args.name, "status": "unsupported", "reason": str(exc),
                  "obj": None, "lb": None, "witness": {}, "bound_certified": False}
    payload = json.dumps(result, indent=2, allow_nan=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
