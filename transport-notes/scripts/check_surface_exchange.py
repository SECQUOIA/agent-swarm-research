"""Check singular surface exchange using independent sparse cell problems.

Run from the repository root: python scripts/check_surface_exchange.py
Outputs deterministic JSON. The bulk test is a reversible finite-volume strip
with one reactive wall; it tests the finite-bulk extension, not just the reduced
well-mixed model. No experimental parameters are used.
"""
from pathlib import Path
import json
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve
from scipy.special import gamma


def wall_integral(n, dsurf, delta=0.0):
    spacing = 2 * np.pi / n
    s = (np.arange(n) + 0.5) * spacing - np.pi
    k = delta + 2 * (1 - np.cos(s))
    rows = np.repeat(np.arange(n), 3)
    cols = np.column_stack(((np.arange(n)-1) % n, np.arange(n),
                            (np.arange(n)+1) % n)).ravel()
    values = np.column_stack((-np.ones(n), 2*np.ones(n), -np.ones(n)))
    lap = coo_matrix((values.ravel() / spacing**2, (rows, cols)),
                     shape=(n, n)).tocsr()
    h = dsurf * lap + diags(k)
    return float(spacing * np.sum(spsolve(h, np.ones(n))))


def bulk_dispersion(n, ny, dsurf, dbulk=1.0, affinity=0.7, height=1.0):
    spacing, dy = 2*np.pi/n, height/ny
    s = (np.arange(n)+0.5)*spacing-np.pi
    k = 2*(1-np.cos(s))
    count = n*(ny+1)
    row, col, data = [], [], []

    def edges(a, b, conductance):
        a, b = np.asarray(a), np.asarray(b)
        c = np.broadcast_to(conductance, a.shape)
        for aa, bb, cc in ((a, a, c), (b, b, c), (a, b, -c), (b, a, -c)):
            row.extend(aa.tolist()); col.extend(bb.tolist()); data.extend(cc.tolist())

    for j in range(ny):
        indices = j*n+np.arange(n)
        edges(indices, j*n+(np.arange(n)+1) % n, dbulk*dy/spacing)
        if j < ny-1:
            edges(indices, indices+n, dbulk*spacing/dy)
    wall = ny*n+np.arange(n)
    edges(wall, ny*n+(np.arange(n)+1) % n, affinity*dsurf/spacing)
    # Half-cell resistance gives a consistent Robin boundary at the wall.
    exchange = affinity*k*spacing/(1+affinity*k*dy/(2*dbulk))
    edges((ny-1)*n+np.arange(n), wall, exchange)
    operator = coo_matrix((data, (row, col)), shape=(count, count)).tocsr()
    weights = np.r_[np.full(n*ny, spacing*dy), np.full(n, affinity*spacing)]
    z = np.sum(weights)
    v = height/(height+affinity)
    g = np.r_[np.full(n*ny, 1-v), np.full(n, -v)]
    rhs = weights*g
    assert abs(np.sum(rhs)) < 1e-12
    chi = np.r_[0.0, spsolve(operator[1:, 1:], rhs[1:])]
    residual = np.max(np.abs(operator @ chi-rhs))
    value = float(np.dot(rhs, chi)/z)
    singular = v*v*affinity/z*wall_integral(n, dsurf)
    return {"n": n, "ny": ny, "surface_diffusivity": dsurf,
            "flow_dispersion": value, "reduced_singular_term": singular,
            "bulk_remainder": value-singular, "ratio": value/singular,
            "max_conservation_residual": float(residual)}


def main():
    c0 = float(np.pi/2*gamma(0.25)/gamma(0.75))
    wall = []
    for d in [1e-2, 1e-4, 1e-6, 1e-8]:
        for z in [0.0, 0.5, 2.0, 8.0]:
            exact = float(np.pi/2*gamma((z+1)/4)/gamma((z+3)/4))
            value = wall_integral(32768, d, z*np.sqrt(d))*d**0.25
            wall.append({"surface_diffusivity": d, "scaled_floor": z,
                         "scaled_integral": value, "oscillator_prediction": exact,
                         "relative_error": value/exact-1})
    bulk = [bulk_dispersion(n, ny, d) for n, ny in [(512, 8), (1024, 16), (2048, 32)]
            for d in [1e-2, 1e-4, 1e-6]]
    grid_check = [
        {"n": n, "scaled_integral": wall_integral(n, 1e-8)*1e-2}
        for n in [8192, 16384, 32768, 65536]
    ]
    for item in bulk:
        assert item["bulk_remainder"] >= 0
        assert item["max_conservation_residual"] < 1e-8
    assert abs(grid_check[-1]["scaled_integral"] / c0 - 1) < 1e-5
    result = {"quadratic_zero_constant": c0, "wall_crossover": wall,
              "finite_bulk_checks": bulk,
              "wall_grid_refinement_at_1e_8": grid_check,
              "predicted_limiting_bulk_remainder": 0.7**2/(3*1.7**3),
              "scope": "Numerical evidence; asymptotics and continuum assumptions require proof."}
    Path("results").mkdir(exist_ok=True)
    Path("results/surface-exchange-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
