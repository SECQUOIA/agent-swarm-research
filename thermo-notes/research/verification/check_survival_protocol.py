"""Check endpoint and whole-cycle survival-conditioned work in a three-state model."""
import json
import numpy as np
from scipy.integrate import solve_ivp, simpson, quad
from scipy.linalg import eigh
from scipy.special import softmax

A = np.array([[111 / 55, -1., 0.], [-1., 2., -1.], [0., -1., 1.]])
RADIUS = 0.3


def energies(s):
    return np.array([RADIUS * np.cos(2 * np.pi * s),
                     RADIUS * np.sin(2 * np.pi * s), 0.])


def derivative(s):
    return np.array([-2 * np.pi * RADIUS * np.sin(2 * np.pi * s),
                     2 * np.pi * RADIUS * np.cos(2 * np.pi * s), 0.])


def stationary(s):
    w = np.exp(-energies(s))
    eigenvalues, h = eigh(A, np.diag(w))
    h = h[:, 0]
    if h.sum() < 0:
        h = -h
    qsd = w * h
    qsd /= qsd.sum()
    bulk = w * h**2
    bulk /= bulk.sum()
    return eigenvalues[0], qsd, bulk


def generator(s):
    return -np.diag(np.exp(energies(s))) @ A


def main():
    sgrid = np.linspace(0, 1, 2001)
    dE = np.array([derivative(s) for s in sgrid])
    qsd = np.array([stationary(s)[1] for s in sgrid])
    bulk = np.array([stationary(s)[2] for s in sgrid])
    report = {"radius": RADIUS,
              "fixed_parameter_endpoint_line_integral": float(simpson(np.sum(qsd*dE, axis=1), x=sgrid)),
              "fixed_parameter_bulk_line_integral": float(simpson(np.sum(bulk*dE, axis=1), x=sgrid)),
              "driven_cycles": []}
    for duration in [20, 100, 500, 2000]:
        def forward(s, y):
            p = softmax(np.r_[y, 0.])
            ratio = (generator(s).T @ p) / p
            return duration * (ratio[:2] - ratio[2])
        def backward(s, y):
            b = softmax(np.r_[y, 0.])
            ratio = (generator(s) @ b) / b
            return -duration * (ratio[:2] - ratio[2])
        p0 = stationary(0)[1]
        p = solve_ivp(forward, (0, 1), np.log(p0[:2]/p0[2]), method="Radau",
                      rtol=2e-10, atol=2e-12, dense_output=True)
        b = solve_ivp(backward, (1, 0), np.zeros(2), method="Radau",
                      rtol=2e-10, atol=2e-12, dense_output=True)
        assert p.success and b.success
        pt = softmax(np.column_stack([p.sol(sgrid).T, np.zeros(len(sgrid))]), axis=1)
        bt = softmax(np.column_stack([b.sol(sgrid).T, np.zeros(len(sgrid))]), axis=1)
        final_survivors = pt * bt
        final_survivors /= final_survivors.sum(axis=1)[:, None]
        def work_at(s, whole_cycle):
            ps = softmax(np.r_[p.sol(s), 0.])
            if whole_cycle:
                ps *= softmax(np.r_[b.sol(s), 0.])
                ps /= ps.sum()
            return ps @ derivative(s)
        endpoint_work = quad(lambda s: work_at(s, False), 0, 1,
                             epsabs=1e-10, points=[.01, .99])[0]
        final_work = quad(lambda s: work_at(s, True), 0, 1,
                         epsabs=1e-10, points=[.01, .99])[0]
        middle = (sgrid > .25) & (sgrid < .75)
        report["driven_cycles"].append({
            "duration": duration,
            "instantaneously_surviving_ensemble_integral": float(endpoint_work),
            "mean_mechanical_work_conditioned_on_final_survival": float(final_work),
            "maximum_bulk_tv_error_middle_half": float(np.max(np.sum(np.abs(final_survivors[middle]-bulk[middle]), axis=1)/2)),
        })
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
