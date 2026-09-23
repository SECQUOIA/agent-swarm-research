"""Bounded numerical probe of arbitrary diagonal virtual-noise splits.

Run with uv --with cvxpy==1.9.2 --with clarabel==0.11.1. This exploratory
module writes numerical witnesses only; it does not issue exact certificates.
"""

import importlib.metadata
import argparse
import json
from fractions import Fraction
from pathlib import Path
from time import perf_counter

import cvxpy as cp
import numpy as np
from scipy.optimize import minimize


def point_value_gradient(R, F, prior, z, a):
    selected = z > 0
    h = (1-z[selected])/z[selected]
    virtual = R[np.ix_(selected, selected)]+np.diag(h*a[selected])
    V = np.linalg.solve(virtual, F[selected])
    J = prior+F[selected].T@V
    value = np.linalg.slogdet(J)[1]
    gradient = np.zeros(len(z))
    gradient[selected] = -h*np.einsum("ij,ji->i", V, np.linalg.solve(J, V.T))
    return float(value), gradient


def solve_probe(R, F, prior, z, method="slsqp"):
    started = perf_counter()
    n, p = F.shape
    if method == "slsqp":
        def eigvalues(a):
            return np.linalg.eigvalsh(R-np.diag(a))
        def eig_jacobian(a):
            return -np.linalg.eigh(R-np.diag(a))[1].T**2
        problem = minimize(lambda a: point_value_gradient(R, F, prior, z, a),
                           np.full(n, .99*np.linalg.eigvalsh(R)[0]), jac=True,
                           method="SLSQP", bounds=[(0., x) for x in np.diag(R)],
                           constraints={"type": "ineq", "fun": eigvalues, "jac": eig_jacobian},
                           options={"maxiter": 1000, "ftol": 1e-12})
        point, status, objective = problem.x, str(problem.message), problem.fun
    else:
        selected = np.flatnonzero(z > 0)
        h = (1-z[selected])/z[selected]
        B = np.linalg.solve(np.linalg.cholesky(prior), F[selected].T).T
        a = cp.Variable(n, nonneg=True)
        Z = cp.Variable((p, p), symmetric=True)
        S = R[np.ix_(selected, selected)]+cp.diag(cp.multiply(h, a[selected]))
        constraints = [R-cp.diag(a) >> 0,
                       cp.bmat([[np.eye(p)-Z, B.T], [B, S+B@B.T]]) >> 0]
        problem = cp.Problem(cp.Minimize(-cp.log_det(Z)+np.linalg.slogdet(prior)[1]), constraints)
        problem.solve(solver="CLARABEL", tol_gap_abs=1e-9, tol_feas=1e-9,
                      tol_gap_rel=1e-9, max_iter=200)
        point, status, objective = a.value, problem.status, problem.value
    value, gradient = point_value_gradient(R, F, prior, z, point)
    Y = cp.Variable((n, n), symmetric=True)
    dual = cp.Problem(cp.Minimize(cp.sum(cp.multiply(R, Y))),
                      [Y >> 0, cp.diag(Y) >= -gradient])
    dual.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_feas=1e-10,
               tol_gap_rel=1e-10, max_iter=200)
    lower = value-gradient@point-dual.value
    return {"method": method, "status": status, "objective": objective,
            "recomputed_point_value": value, "a": point.tolist(),
            "split_min_eigenvalue": float(np.linalg.eigvalsh(R-np.diag(point))[0]),
            "gradient": gradient.tolist(), "dual_status": dual.status,
            "dual_objective": dual.value, "Y": Y.value.tolist(),
            "dual_min_eigenvalue": float(np.linalg.eigvalsh(Y.value)[0]),
            "dual_diagonal_min_slack": float(np.min(np.diag(Y.value)+gradient)),
            "numerical_all_diagonal_lower_bound": lower,
            "numerical_duality_gap": value-lower,
            "seconds": perf_counter()-started}


def main():
    directory = Path(__file__).parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=directory/"results/dense-design-exact-certificates.json")
    parser.add_argument("--memory", type=Path, default=directory/"results/noisy-markov-extended-certificate-0.json")
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--output", type=Path, default=directory/"results/diagonal-split-probe.json")
    args = parser.parse_args()
    source_path = args.input
    source = json.loads(source_path.read_text())["results"][args.case]
    data = source["problem_data"]
    number = lambda x: float(Fraction(x))
    F = np.array([[number(x) for x in row] for row in data["F"]])
    prior = np.array([[number(x) for x in row] for row in data["prior"]])
    z = np.array([number(x) for x in source["tangent_z"]])
    rho, latent, nugget = [number(data[x]) for x in ("rho", "latent_variance", "nugget_variance")]
    R = latent*rho**np.abs(np.subtract.outer(np.arange(len(z)), np.arange(len(z))))+nugget*np.eye(len(z))
    toy = solve_probe(np.array([[2., 1.], [1., 2.]]), np.array([[1.], [-1.]]),
                      np.ones((1, 1)), np.array([.5, .5]))
    print(json.dumps({"toy": {k: toy[k] for k in ("status", "recomputed_point_value", "numerical_all_diagonal_lower_bound", "seconds")}}), flush=True)
    benchmark = solve_probe(R, F, prior, z)
    memory = json.loads(args.memory.read_text())
    memory_upper = number(memory["upper_bound"])
    benchmark["memory_upper_bound"] = memory_upper
    benchmark["numerical_separation"] = benchmark["numerical_all_diagonal_lower_bound"]-memory_upper
    report = {"scope": "Numerical probe only, no exact feasibility or bound certificate",
              "versions": {name: importlib.metadata.version(name) for name in ("cvxpy", "clarabel", "numpy", "scipy")},
              "source": str(source_path), "case": args.case,
              "memory_source": str(args.memory),
              "problem_data": data, "z": source["tangent_z"], "toy": toy,
              "benchmark": benchmark}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: benchmark[k] for k in ("status", "recomputed_point_value", "numerical_all_diagonal_lower_bound", "numerical_separation", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
