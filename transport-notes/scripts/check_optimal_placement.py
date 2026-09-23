"""Check localized mobility design and an independent discrete convex dual.

The whole-line model has a=1, R=1, budget M=3/80. Truncating at ±L
subtracts 2/L from its optimal integral because mobility vanishes outside R.
The compact periodic test compares admissible localized and uniform designs
at the same total mobility budget; it does not numerically optimize that wall.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve


def dual_check(n=240, extent=4.0):
    dx = 2*extent/n
    x = -extent+(np.arange(n)+0.5)*dx
    potential = x*x
    budget = 3/80
    initial_h = np.where(abs(x) <= 1, 9-8*abs(x), 1/(x*x))
    initial = np.r_[initial_h, 8.0]

    def fun(z):
        h, t = z[:-1], z[-1]
        return dx*np.dot(potential, h*h)-2*dx*np.sum(h)+budget*t*t

    def jac(z):
        return np.r_[2*dx*(potential*z[:-1]-1), 2*budget*z[-1]]

    # All finite differences are bounded by the common Lipschitz constant.
    constraints = np.zeros((2*(n-1), n+1))
    i = np.arange(n-1)
    constraints[i, i], constraints[i, i+1], constraints[i, -1] = -1, 1, -dx
    constraints[n-1+i, i], constraints[n-1+i, i+1], constraints[n-1+i, -1] = 1, -1, -dx
    result = minimize(fun, initial, jac=jac, method="SLSQP",
                      constraints=[LinearConstraint(constraints, -np.inf, 0)],
                      bounds=Bounds(np.zeros(n+1), np.full(n+1, np.inf)),
                      options={"ftol": 1e-10, "maxiter": 250})
    assert result.success, result.message
    return {"n": n, "extent": extent, "discrete_dual_value": float(-result.fun),
            "continuum_value": 12-2/extent, "optimal_lipschitz_constant": float(result.x[-1]),
            "predicted_lipschitz_constant": 8,
            "max_constraint_violation": float(np.max(constraints@result.x)),
            "iterations": int(result.nit)}


def periodic_check(budget, n=32768):
    spacing = 2*np.pi/n
    centers = -np.pi+(np.arange(n)+0.5)*spacing
    faces = -np.pi+(np.arange(n)+1)*spacing
    k = 4*np.sin(centers/2)**2
    radius = (80*budget/3)**0.2
    y = abs(faces)/radius
    design = np.where(y < 1, radius**4/8*y*(1-y)**2*(1+2*y), 0)
    # Enforce the exact same discrete budget in the two comparisons.
    design *= budget/(spacing*np.sum(design))

    def solve(d):
        i = np.arange(n)
        j = (i+1) % n
        rows = np.r_[i, j, i, j]
        cols = np.r_[i, j, j, i]
        values = np.r_[d, d, -d, -d]/spacing**2
        operator = coo_matrix((values, (rows, cols)), shape=(n, n)).tocsr()+diags(k)
        return float(spacing*np.sum(spsolve(operator, np.ones(n))))

    local = solve(design)
    uniform = solve(np.full(n, budget/(2*np.pi)))
    prediction = 12/radius
    return {"budget": budget, "n": n, "support_radius": radius,
            "localized_integral": local, "uniform_integral": uniform,
            "asymptotic_optimal_integral": prediction,
            "localized_to_asymptotic_ratio": local/prediction,
            "localized_to_uniform_ratio": local/uniform,
            "scaled_localized_integral": local*budget**0.2,
            "predicted_scaled_constant": 12*(3/80)**0.2}


def main():
    dual = [dual_check(n) for n in [120, 240]]
    designs = [periodic_check(m) for m in [1e-3, 1e-5, 1e-7, 1e-9]]
    assert abs(dual[-1]["discrete_dual_value"]/dual[-1]["continuum_value"]-1) < 0.001
    assert all(r["localized_integral"] < r["uniform_integral"] for r in designs)
    result = {"independent_discrete_dual": dual, "periodic_design_comparison": designs,
              "scope": "The independent variational certificate proves optimality; finite-grid optimization and admissible-design comparisons provide separate numerical checks."}
    Path("results").mkdir(exist_ok=True)
    Path("results/optimal-placement-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
