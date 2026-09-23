"""Reproducible checks of transport and branching calculations.

Numerical checks supplement the proofs; they do not certify novelty or replace
uniform error estimates. Run from the repository root with Python, NumPy, SciPy.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def antithetic(p, scores):
    order = np.argsort(scores, kind="stable")
    edges = np.r_[0.0, np.cumsum(p[order])]
    edges[-1] = 1.0
    c = np.zeros((len(p), len(p)))
    for a, j in enumerate(order):
        for b, k in enumerate(order):
            c[j, k] = max(0.0, min(edges[a + 1], 1 - edges[b])
                          - max(edges[a], 1 - edges[b + 1]))
    return c


def extinction(b, couplings=None, p=None, tol=2e-14):
    q = np.zeros(len(b))
    for iteration in range(2_000_000):
        cs = couplings if couplings is not None else [antithetic(row, q) for row in p]
        nxt = 1 - b + b * np.einsum("ijk,j,k->i", cs, q, q)
        if np.max(np.abs(nxt - q)) < tol:
            # A small residual alone is not a certified error bound.
            return nxt, iteration + 1
        q = nxt
    raise RuntimeError("Iteration limit reached; no convergence claim.")


def perron(m):
    ev, vr = np.linalg.eig(m)
    v = vr[:, np.argmin(abs(ev - 1))].real
    ev, ul = np.linalg.eig(m.T)
    u = ul[:, np.argmin(abs(ev - 1))].real
    u /= sum(u)
    v /= u @ v
    assert np.all(u > 0) and np.all(v > 0)
    return u, v


def main():
    rng = np.random.default_rng(9062026)
    max_transport_error = 0.0
    for m in range(2, 8):
        constraints = np.zeros((2 * m, m * m))
        for j in range(m):
            constraints[j, j * m:(j + 1) * m] = 1
            constraints[m + j, j::m] = 1
        for _ in range(20):
            p = rng.dirichlet(np.ones(m))
            z = rng.random(m)
            c = antithetic(p, z)
            assert np.max(abs(c.sum(0) - p)) < 1e-14
            assert np.max(abs(c - c.T)) < 1e-14
            lp = linprog(np.outer(z, z).ravel(), A_eq=constraints,
                         b_eq=np.r_[p, p], bounds=(0, None), method="highs")
            assert lp.success
            err = abs(np.sum(c * np.outer(z, z)) - lp.fun)
            max_transport_error = max(max_transport_error, err)
            assert err < 1e-10

    # Two equal leading reproductive values, split at the next asymptotic order.
    p = np.array([[.6, .3, .1], [.1, .5, .4], [.2, .3, .5]])
    raw_v = np.array([1., 1., 2.])
    b0 = raw_v / (2 * (p @ raw_v))
    m0 = 2 * b0[:, None] * p
    u, v = perron(m0)
    # Use the exact prescribed tie instead of eigensolver roundoff to sort it.
    v = raw_v / (u @ raw_v)
    initial_cs = np.array([antithetic(row, v) for row in p])
    h = b0 * np.einsum("ijk,j,k->i", initial_cs, v, v)
    d = u @ h
    a = 1 / d
    r = np.linalg.solve(np.eye(3) - m0 + np.outer(v, u), a * v - a * a * h)
    lex_order = sorted(range(3), key=lambda j: (raw_v[j], r[j]))
    scores = np.empty(3)
    scores[lex_order] = np.arange(3)
    cs = np.array([antithetic(row, scores) for row in p])
    c_scalar = -a - 2 * a * (u @ (b0 * np.einsum("ijk,j,k->i", cs, v, r)))
    second = r + c_scalar * v
    rows = []
    for eps in [.04, .02, .01, .005, .0025]:
        b = (1 + eps) * b0
        qopt, nopt = extinction(b, p=p)
        qfixed, nfixed = extinction(b, couplings=cs)
        qmax, _ = extinction(b, couplings=np.array([np.diag(row) for row in p]))
        assert np.max(abs(qopt - qfixed)) < 2e-10
        assert np.all(qmax >= qopt - 1e-10)
        survival = 1 - qopt
        first_error = np.max(abs(survival - eps * a * v))
        second_error = np.max(abs(survival - eps * a * v - eps**2 * second))
        rows.append(dict(epsilon=eps, survival=survival.tolist(),
                         first_error_over_eps2=first_error / eps**2,
                         second_error_over_eps3=second_error / eps**3,
                         optimum_fixed_difference=float(np.max(abs(qopt-qfixed))),
                         iterations=nopt))

    result = dict(transport_cases=120, max_transport_lp_error=max_transport_error,
                  model=dict(p=p.tolist(), b0=b0.tolist(), u=u.tolist(), v=v.tolist()),
                  D=d, transverse_second_order=r.tolist(), lex_order=lex_order,
                  couplings=cs.tolist(), near_critical=rows,
                  caution="Floating-point checks, not certified fixed-point enclosures.")
    target = Path(__file__).with_name("extinction_coupling_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
