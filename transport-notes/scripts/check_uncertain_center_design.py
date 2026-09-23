"""Convex finite-volume optimization of mobility for an uncertain zero.

The mobility vanishes outside [-L,L]; its exterior reciprocal-potential
response is integrated exactly. Grid and parameter quadrature still need
refinement. Starting designs are uniform and do not use the analytic optimum.
"""
import json
import os
from pathlib import Path

# Dense SLSQP systems here are small; excessive BLAS threads slow them down.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import solve_banded
from scipy.optimize import minimize


def optimize(width, n=200, nq=24):
    extent = 6+width/2
    dx = 2*extent/n
    x = -extent+(np.arange(n)+0.5)*dx
    if width:
        points, weights = leggauss(nq)
        centers, weights = points*width/2, weights/2
        outside = 2/width*np.log((extent+width/2)/(extent-width/2))
    else:
        centers, weights = np.array([0.]), np.array([1.])
        outside = 2/extent
    potentials = [(x-center)**2 for center in centers]

    def objective(masses):
        conductance = masses/dx**3
        matrix = np.zeros((3, n))
        matrix[0, 1:] = matrix[2, :-1] = -conductance
        value = outside
        gradient = np.zeros(n-1)
        for potential, weight in zip(potentials, weights):
            matrix[1] = potential
            matrix[1, :-1] += conductance
            matrix[1, 1:] += conductance
            h = solve_banded((1, 1), matrix, np.ones(n))
            value += weight*dx*np.sum(h)
            gradient -= weight*(np.diff(h)/dx)**2
        return float(value), gradient

    initial = np.full(n-1, 1/(n-1))
    solution = minimize(objective, initial, jac=True, method="SLSQP",
                        bounds=[(0, None)]*(n-1),
                        constraints={"type": "eq", "fun": lambda p: p.sum()-1,
                                     "jac": lambda p: np.ones_like(p)},
                        options={"ftol": 2e-9, "maxiter": 600})
    value, gradient = objective(solution.x)
    # For a convex differentiable objective on the simplex, the tangent at
    # any feasible point supplies an independent global lower certificate.
    gap = float(gradient@solution.x-np.min(gradient))
    return {"uncertainty_width": width, "cells": n, "quadrature_nodes": len(centers),
            "half_domain_length": extent, "objective": value,
            "discrete_convex_lower_bound": value-gap,
            "discrete_primal_dual_gap": gap,
            "success": bool(solution.success), "message": solution.message,
            "iterations": solution.nit, "mass_error": float(solution.x.sum()-1),
            "symmetry_error": float(np.max(abs(solution.x-solution.x[::-1]))),
            "face_positions": (-extent+np.arange(1, n)*dx).tolist(),
            "face_mobility": (solution.x/dx).tolist()}


def recheck_quadrature(row, nq=384):
    n, extent, width = row["cells"], row["half_domain_length"], row["uncertainty_width"]
    dx = 2*extent/n
    x = -extent+(np.arange(n)+0.5)*dx
    conductance = np.array(row["face_mobility"])/dx**2
    points, weights = leggauss(nq)
    matrix = np.zeros((3, n))
    matrix[0, 1:] = matrix[2, :-1] = -conductance
    value = 2/width*np.log((extent+width/2)/(extent-width/2))
    for center, weight in zip(points*width/2, weights/2):
        matrix[1] = (x-center)**2
        matrix[1, :-1] += conductance
        matrix[1, 1:] += conductance
        h = solve_banded((1, 1), matrix, np.ones(n))
        value += weight*dx*np.sum(h)
    return {"width": width, "cells": n, "quadrature_nodes": nq,
            "fixed_design_objective": float(value),
            "relative_change": float(value/row["objective"]-1)}


def main():
    rows = []
    for width in [0, 0.5, 2, 8, 32]:
        row = optimize(width, nq=96 if width == 32 else 24)
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items()
                          if k not in ["face_positions", "face_mobility"]}), flush=True)
    refined = [optimize(width, n=400, nq=192 if width == 32 else 48)
               for width in [0, 2, 32]]
    result = {"optimizations": rows, "refinements": refined,
              "parameter_quadrature_recheck": recheck_quadrature(refined[-1]),
              "scope": "Finite-domain, finite-volume, finite-quadrature convex optima; the tangent gap certifies the discretized problem only."}
    Path("results/uncertain-center-design-checks.json").write_text(
        json.dumps(result, indent=2)+"\n")
    print(json.dumps({"refinements": [{k: v for k, v in row.items()
                                      if k not in ["face_positions", "face_mobility"]}
                                     for row in refined]}), flush=True)


if __name__ == "__main__":
    main()
