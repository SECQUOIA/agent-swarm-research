"""Resolve mobility degeneracy on a geometric finite-volume grid.

Use symmetry to solve on [0, pi] with no flux at each end. A very small
first cell regularizes the zero-mobility endpoint. Changing that cell is
therefore essential to distinguish a finite integral from divergence.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_banded
from scipy.special import gammaln


def integral(epsilon, order, delta, smallest=1e-10, n=12000):
    edges = np.r_[0.0, np.geomspace(smallest, np.pi, n)]
    widths = np.diff(edges)
    centers = (edges[:-1]+edges[1:])/2
    k = 4*np.sin(centers/2)**2+delta
    mobility = epsilon*(4*np.sin(edges[1:-1]/2)**2)**(order/2)
    conductance = mobility/np.diff(centers)
    diag = k.copy()
    diag[:-1] += conductance/widths[:-1]
    diag[1:] += conductance/widths[1:]
    matrix = np.zeros((3, len(centers)))
    matrix[1] = diag
    matrix[0, 1:] = -conductance/widths[:-1]
    matrix[2, :-1] = -conductance/widths[1:]
    h = solve_banded((1, 1), matrix, np.ones(len(centers)))
    return float(2*np.dot(widths, h))


def crossover(z):
    nu = np.sqrt(0.25+z)
    return float(np.pi/2*np.exp(2*(gammaln(nu/2+0.25)-gammaln(nu/2+0.75))))


def main():
    rows = []
    for eps in [1e-2, 1e-4, 1e-6]:
        for z in [0.0, 0.5, 2.0, 8.0]:
            val = integral(eps, 2, eps*z, smallest=np.sqrt(eps)*1e-9)*np.sqrt(eps)
            rows.append({"epsilon": eps, "scaled_floor": z, "scaled_integral": val,
                         "prediction": crossover(z), "relative_error": val/crossover(z)-1})
    refinement = []
    for order in [2.0, 2.5, 3.0, 3.5, 4.0]:
        for small in [1e-4, 1e-6, 1e-8, 1e-10]:
            refinement.append({"mobility_order": order, "first_cell_width": small,
                               "integral": integral(0.1, order, 0, smallest=small)})
    grids = [{"n": n, "scaled_integral": integral(1e-6, 2, 0, smallest=1e-12, n=n)*1e-3}
             for n in [3000, 6000, 12000, 24000]]
    for r in rows:
        if r["epsilon"] == 1e-6:
            assert abs(r["relative_error"]) < 0.005
    result = {"quadratic_mobility_zero_constant": np.pi**2/2,
              "quadratic_crossover": rows, "endpoint_refinement": refinement,
              "grid_refinement": grids,
              "scope": "A finite endpoint cell cannot establish finiteness; the divergence classification requires the independent variational proof."}
    Path("results").mkdir(exist_ok=True)
    Path("results/degenerate-mobility-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
