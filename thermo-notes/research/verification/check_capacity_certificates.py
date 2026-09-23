"""Deterministic independent numerical checks of conditional capacity bounds.

Run from the repository root: python research/verification/check_capacity_certificates.py
Outputs JSON and a standalone PNG beside this script. Requires NumPy, SciPy,
and Matplotlib. FEM convergence is numerical evidence, not a continuum proof.
"""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


HERE = Path(__file__).resolve().parent


def graph_check(seed=8163, cases=120):
    """Compare exact full capacity to a coarse solve plus internal-flow repair."""
    rng = np.random.default_rng(seed)
    max_violation = 0.0
    ratios = []
    for _ in range(cases):
        # Four interior blocks of three states, with single-state terminals.
        block = np.r_[0, np.repeat(np.arange(1, 5), 3), 5]
        n = len(block)
        conductance = np.exp(rng.uniform(-4, 4, (n, n)))
        conductance = np.triu(conductance, 1)
        conductance += conductance.T
        lap = np.diag(conductance.sum(axis=1)) - conductance
        h = np.zeros(n)
        h[-1] = 1
        h[1:-1] = np.linalg.solve(lap[1:-1, 1:-1], -lap[1:-1, -1])
        capacity = h @ lap @ h
        indicator = np.eye(6)[block]
        coarse_lap = indicator.T @ lap @ indicator
        coarse_h = np.zeros(6)
        coarse_h[-1] = 1
        coarse_h[1:-1] = np.linalg.solve(coarse_lap[1:-1, 1:-1], -coarse_lap[1:-1, -1])
        f = indicator @ coarse_h
        upper = f @ lap @ f
        source = lap @ f
        cost = 0.0
        gap_cost = 0.0
        for b in range(1, 5):
            ii = np.flatnonzero(block == b)
            c = conductance[np.ix_(ii, ii)]
            internal_lap = np.diag(c.sum(axis=1)) - c
            r = source[ii]
            assert abs(r.sum()) < 2e-11
            cost += r @ np.linalg.pinv(internal_lap) @ r
            gap = np.linalg.eigvalsh(internal_lap)[1]
            gap_cost += r @ r / gap
        lower = upper**2 / (upper + cost)
        gap_lower = upper**2 / (upper + gap_cost)
        max_violation = max(max_violation, lower / capacity - 1, capacity / upper - 1,
                            gap_lower / lower - 1)
        assert max_violation < 2e-10
        ratios.append([lower / capacity, capacity / upper])
    return {"cases": cases, "seed": seed, "max_relative_violation": max_violation,
            "min_lower_over_exact": min(x[0] for x in ratios),
            "min_exact_over_upper": min(x[1] for x in ratios)}


def fem_capacity(nx, nz, stiffness, slope, barrier=6.0):
    """Linear conforming FEM on a sheared Gaussian strip, z in [-6,6].

    Physical y = slope*x + sigma*z. Energy in (x,z) is
    rho(x)*phi(z) * [(u_x-slope/sigma*u_z)^2+(u_z/sigma)^2].
    Dirichlet at x=+-1 and natural reflecting conditions at z=+-6.
    Three-point triangle quadrature; there is quadrature and mesh error.
    """
    x, z = np.meshgrid(np.linspace(-1, 1, nx), np.linspace(-6, 6, nz), indexing="ij")
    xy = np.column_stack([x.ravel(), z.ravel()])
    ind = np.arange(nx * nz).reshape(nx, nz)
    p, q, r, s = (a.ravel() for a in (ind[:-1, :-1], ind[1:, :-1],
                                      ind[:-1, 1:], ind[1:, 1:]))
    triangles = np.concatenate([np.column_stack([p, q, s]), np.column_stack([p, s, r])])
    vertices = xy[triangles]
    dx = 2 / (nx - 1)
    dz = 12 / (nz - 1)
    area = dx * dz / 2
    # Gradients of affine barycentric functions: solve [1,x,z] coefficients.
    affine = np.concatenate([np.ones((*vertices.shape[:2], 1)), vertices], axis=2)
    gradients = np.linalg.inv(affine)[:, 1:, :]
    sigma = stiffness**-0.5
    metric = np.array([[1, -slope / sigma], [-slope / sigma, (1 + slope**2) / sigma**2]])
    bary = np.array([[2 / 3, 1 / 6, 1 / 6], [1 / 6, 2 / 3, 1 / 6],
                     [1 / 6, 1 / 6, 2 / 3]])
    points = np.einsum("qv,tvd->tqd", bary, vertices)
    weight = np.exp(-barrier * (1 - points[:, :, 0]**2)**2 - points[:, :, 1]**2 / 2)
    weight /= np.sqrt(2 * np.pi)
    local = np.einsum("tdi,de,tej->tij", gradients, metric, gradients)
    local *= (area * weight.mean(axis=1))[:, None, None]
    row = np.broadcast_to(triangles[:, :, None], local.shape).ravel()
    col = np.broadcast_to(triangles[:, None, :], local.shape).ravel()
    matrix = coo_matrix((local.ravel(), (row, col)), shape=(nx * nz, nx * nz)).tocsr()
    unknown = ind[1:-1, :].ravel()
    end = ind[-1, :].ravel()
    h = np.zeros(nx * nz)
    h[end] = 1
    h[unknown] = spsolve(matrix[unknown][:, unknown], -np.asarray(matrix[unknown][:, end].sum(axis=1)).ravel())
    capacity = h @ (matrix @ h)
    residual = np.max(np.abs((matrix @ h)[unknown]))
    upper = 1 / quad(lambda v: np.exp(barrier * (1 - v * v)**2), -1, 1, epsabs=1e-10)[0]
    lower = upper / (1 + slope**2)
    return {"nx": nx, "nz": nz, "stiffness": stiffness, "slope": slope,
            "capacity": float(capacity), "upper": upper, "lower": lower,
            "relative_to_upper": float(capacity / upper),
            "relative_to_lower": float(capacity / lower), "solve_residual": float(residual)}


def main():
    results = {"graph": graph_check(), "diffusion": [], "refinement": []}
    for slope in (0.0, 0.5, 1.0, 2.0):
        for stiffness in (1.0, 4.0, 16.0, 64.0, 256.0):
            result = fem_capacity(161, 101, stiffness, slope)
            results["diffusion"].append(result)
            print(f"slope={slope:g}, stiffness={stiffness:g}: C/U={result['relative_to_upper']:.6f}", flush=True)
    for nx, nz in ((81, 61), (161, 101), (321, 201)):
        results["refinement"].append(fem_capacity(nx, nz, 256.0, 2.0))
    (HERE / "capacity-numerical-results.json").write_text(json.dumps(results, indent=2) + "\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 4.2), constrained_layout=True)
    for slope in (0.0, 0.5, 1.0, 2.0):
        rows = [r for r in results["diffusion"] if r["slope"] == slope]
        line, = ax.semilogx([r["stiffness"] for r in rows], [r["relative_to_upper"] for r in rows],
                           "o-", label=f"path slope {slope:g}")
        ax.axhline(1 / (1 + slope**2), color=line.get_color(), linestyle=":", alpha=0.6)
    ax.set(xlabel="Transverse stiffness", ylabel="Capacity / projected upper bound", ylim=(0, 1.08),
           title="Fast conditional relaxation can retain a rate error")
    ax.legend(fontsize=9)
    fig.savefig(HERE / "capacity-stiffness.png", dpi=180)
    print(json.dumps({"graph": results["graph"], "refinement": results["refinement"]}, indent=2))


if __name__ == "__main__":
    main()
