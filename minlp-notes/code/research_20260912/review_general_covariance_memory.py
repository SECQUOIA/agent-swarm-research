"""Independent exact-rational checks of the covariance-decay memory theorem.

This is a theorem probe, not production certificate code. Covariances have
arbitrary signed blocks and rational, possibly large, diagonal additions.
The checks use direct selected covariance inverses and explicit residual maps.
"""

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform
from time import perf_counter

import numpy as np
import sympy as sp


Q = sp.Rational
HERE = Path(__file__).resolve().parent
COUNTS = {"models": 0, "subsets_windows": 0, "precision_psd_checks": 0,
          "regression_psd_checks": 0, "old_covariance_psd_checks": 0,
          "schur_floor_psd_checks": 0, "metric_congruence_checks": 0,
          "metric_promise_checks": 0, "geometric_identities": 0}


def psd(matrix):
    """Exact symmetric Schur elimination, including zero-pivot PSD cases."""
    assert matrix == matrix.T
    A = [list(matrix.row(i)) for i in range(matrix.rows)]
    for k in range(matrix.rows):
        pivot = A[k][k]
        if pivot < 0:
            return False
        if not pivot:
            if any(A[k][j] for j in range(k+1, matrix.rows)):
                return False
            continue
        for i in range(k+1, matrix.rows):
            for j in range(i, matrix.rows):
                value = A[i][j]-A[i][k]*A[k][j]/pivot
                A[i][j] = A[j][i] = value
    return True


def constants(m, C, rho, L):
    theta = (4*C*rho+m*rho*(1-rho))/(4*C*rho+m*(1-rho))
    B = 2*C*rho/(m*(theta-rho))
    Kold = C*(1+B*rho/(theta-rho))
    delta = 2*Kold/m*theta**(L+1)/(1-theta)*(1+B*theta*(1-theta**L)/(1-theta))
    assert rho < theta < 1
    assert 2*C*(rho/(theta-rho)-rho/(1-rho)) == m/2
    return theta, B, Kold, delta


def indices(dims):
    offsets, result = 0, []
    for d in dims:
        result.append(list(range(offsets, offsets+d)))
        offsets += d
    return result


def generated_covariance(dims, m, C, rho, scale, rng):
    ix = indices(dims)
    n, size = len(dims), sum(dims)
    R = sp.zeros(size)
    base = m+2*C*rho/(1-rho)
    for t, dim in enumerate(dims):
        G = sp.Matrix(rng.integers(-2, 3, size=(dim, dim)).tolist())
        diagonal = base*sp.eye(dim)+scale*(t+1)*(G @ G.T)
        for i, u in enumerate(ix[t]):
            for j, v in enumerate(ix[t]):
                R[u, v] = diagonal[i, j]
        for s in range(t):
            E = sp.Matrix(rng.integers(-1, 2, size=(dim, dims[s])).tolist())
            block = C*rho**(t-s)*E/max(dim, dims[s])
            for i, u in enumerate(ix[t]):
                for j, v in enumerate(ix[s]):
                    R[u, v] = R[v, u] = block[i, j]
            assert psd((C*rho**(t-s))**2*sp.eye(dim)-block @ block.T)
    assert psd(R-m*sp.eye(size))
    return R


def local_factor(R, dims, selected, L):
    original_ix = indices(dims)
    local_ix = indices([dims[t] for t in selected])
    flat = [i for t in selected for i in original_ix[t]]
    A, Dinv = sp.eye(len(flat)), sp.zeros(len(flat))
    blocks = {}
    for row, t in enumerate(selected):
        history = [s for s in selected[:row] if t-s <= L]
        hflat = [i for s in history for i in original_ix[s]]
        b = (R.extract(original_ix[t], hflat) @ R.extract(hflat, hflat).inv()
             if history else sp.zeros(dims[t], 0))
        D = R.extract(original_ix[t], original_ix[t])-b @ R.extract(hflat, original_ix[t])
        dinv = D.inv()
        for i, u in enumerate(local_ix[row]):
            for j, v in enumerate(local_ix[row]):
                Dinv[u, v] = dinv[i, j]
        offset = 0
        bblocks = {}
        for s in history:
            block = b[:, offset:offset+dims[s]]
            scol = selected.index(s)
            for i, u in enumerate(local_ix[row]):
                for j, v in enumerate(local_ix[scol]):
                    A[u, v] = -block[i, j]
            bblocks[s] = block
            offset += dims[s]
        blocks[t] = D, bblocks
    return A.T @ Dinv @ A, blocks, flat


def audit_model(R, dims, m, C, rho, metric_transform=None):
    n, ix = len(dims), indices(dims)
    for size in range(1, n+1):
        for selected in combinations(range(n), size):
            flat = [i for t in selected for i in ix[t]]
            exact_precision = R.extract(flat, flat).inv()
            for L in range(n):
                theta, B, Kold, delta = constants(m, C, rho, L)
                local_precision, blocks, _ = local_factor(R, dims, selected, L)
                if L >= n-1:
                    assert local_precision == exact_precision
                    delta = Q(0)
                assert psd(local_precision-(1-delta)*exact_precision)
                assert psd((1+delta)*exact_precision-local_precision)
                COUNTS["precision_psd_checks"] += 2
                for t, (D, regressions) in blocks.items():
                    assert psd(D-m*sp.eye(dims[t]))
                    COUNTS["schur_floor_psd_checks"] += 1
                    for s, block in regressions.items():
                        assert psd((B*theta**(t-s))**2*sp.eye(dims[t])-block @ block.T)
                        COUNTS["regression_psd_checks"] += 1
                    for j in selected:
                        if j >= t-L:
                            continue
                        old = R.extract(ix[t], ix[j])
                        for s, block in regressions.items():
                            old -= block @ R.extract(ix[s], ix[j])
                        assert psd((Kold*theta**(t-j))**2*sp.eye(dims[t])-old @ old.T)
                        COUNTS["old_covariance_psd_checks"] += 1
                if metric_transform is not None:
                    T = metric_transform.extract(flat, flat)
                    transformed = metric_transform @ R @ metric_transform.T
                    transformed_q, _, _ = local_factor(transformed, dims, selected, L)
                    assert T.T @ transformed_q @ T == local_precision
                    COUNTS["metric_congruence_checks"] += 1
                COUNTS["subsets_windows"] += 1
    COUNTS["models"] += 1


def main():
    started = perf_counter()
    rng = np.random.default_rng(9981043)
    configs = [([1]*5, Q(1), Q(1, 100), Q(1, 4), Q(0)),
               ([1, 2, 1, 2], Q(1), Q(1, 2), Q(2, 5), Q(0)),
               ([2, 1, 2, 1], Q(2), Q(3), Q(3, 5), Q(1000000)),
               ([1, 2, 2, 1], Q(1, 3), Q(1, 20), Q(1, 3), Q(1000000000))]
    for number, (dims, m, C, rho, scale) in enumerate(configs):
        R = generated_covariance(dims, m, C, rho, scale, rng)
        T = None
        if number == 1:
            blocks = []
            for t, d in enumerate(dims):
                block = sp.diag(*[Q(10)**((t+1)*(i+1)-3) for i in range(d)])
                if d > 1:
                    block[0, 1] = Q(3, 7)
                blocks.append(block)
            T = sp.diag(*blocks)
            transformed, V = T @ R @ T.T, T @ T.T
            assert psd(transformed-m*V)
            ix = indices(dims)
            for t in range(len(dims)):
                for s in range(t):
                    cross = transformed.extract(ix[t], ix[s])
                    promise = (C*rho**(t-s)*V.extract(ix[t], ix[t])).row_join(cross)
                    promise = promise.col_join(cross.T.row_join(C*rho**(t-s)*V.extract(ix[s], ix[s])))
                    assert psd(promise)
                    COUNTS["metric_promise_checks"] += 1
        audit_model(R, dims, m, C, rho, T)

    for theta in (Q(1, 7), Q(2, 5), Q(46, 55), Q(99, 100)):
        for L in range(20):
            far = theta**(L+1)/(1-theta)*(1+Q(3, 2)*sum(theta**(2*d) for d in range(1, L+1)))
            near = Q(3, 2)*sum(theta**h*sum(theta**(2*d) for d in range(L+1-h, L+1))
                               for h in range(1, L+1))
            claimed = theta**(L+1)/(1-theta)*(1+Q(3, 2)*theta*(1-theta**L)/(1-theta))
            assert far+near == claimed
            COUNTS["geometric_identities"] += 1
    note = HERE.parents[1] / "notes/research-20260912-general-covariance-memory-bound.md"
    report = {"status": "passed", "arithmetic": "exact SymPy rational arithmetic and symmetric Schur PSD tests",
              "counts": COUNTS, "seed": 9981043,
              "covariance_configurations": [{"dimensions": dims, "m": str(m), "C": str(C), "rho": str(rho),
                                               "diagonal_addition_scale": str(scale)}
                                              for dims, m, C, rho, scale in configs],
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "reviewed_note_sha256_at_run": sha256(note.read_bytes()).hexdigest(),
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__},
              "wall_seconds": perf_counter()-started}
    output = HERE / "results/general-covariance-memory-independent-review.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
