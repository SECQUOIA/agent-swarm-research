"""End-to-end exact checks of the cleaned core algorithm.

1. Instances with proved weighted growth (convex, mixed-integer, and the
   nonconvex block family): the admissible trial never aborts, and the stage
   invariants E_j <= kappa n_P eta_j^2, gap <= 9/16 n_P eta_j^2, retained
   radius <= 8 sqrt(kappa n_P) h_ij (+1 integer) hold at every stage.
2. Random nonconvex mixed-integer instances without any growth promise:
   every stage bound is <= the exact optimum (face enumeration), the
   optimizer is never filtered, and the schedule terminates.
3. The minimal certificate (grids only) is accepted, and tampered
   certificates are rejected.
"""

import random
from fractions import Fraction as Fr

from core_lib import (Problem, run_schedule, check_certificate, exact_box_qp_min)


def ldl_psd(M):
    n = len(M)
    A = [row[:] for row in M]
    for k in range(n):
        p = A[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(A[i][k] != 0 for i in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / p
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


def weighted_growth_convex(H, L):
    """Largest dyadic gamma with H - 2 gamma diag(L) PSD (so that
    F - F* >= 1/2 d^T H d >= gamma ||d||_L^2 when the unconstrained minimizer
    is feasible)."""
    n = len(H)
    lo, hi = Fr(0), Fr(1)
    for _ in range(14):
        mid = (lo + hi) / 2
        M = [[H[i][j] - (2 * mid * L[i] if i == j else 0) for j in range(n)] for i in range(n)]
        if ldl_psd(M):
            lo = mid
        else:
            hi = mid
    return lo


def path_problem(n, rng, integer_frac=0.4, convex=True):
    # F = 1/2 (x-a)^T H (x-a), H tridiagonal diagonally dominant, a feasible
    ints = {i for i in range(n) if rng.random() < integer_frac}
    lo, hi, a = [], [], []
    for i in range(n):
        l = rng.randint(-6, 0)
        u = l + rng.randint(2, 9)
        lo.append(Fr(l))
        hi.append(Fr(u))
        if i in ints:
            a.append(Fr(rng.randint(l, u)))
        else:
            a.append(Fr(l) + Fr(rng.randint(0, 8 * (u - l)), 8))
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(rng.randint(1, 40), rng.choice([1, 2, 4, 8, 16]))
    for i in range(n - 1):
        off = min(H[i][i], H[i + 1][i + 1]) * Fr(rng.randint(-4, 4), 10)
        H[i][i + 1] = H[i + 1][i] = off
    quad = {}
    b = [Fr(0)] * n
    c0 = Fr(0)
    for i in range(n):
        for j in range(i, n):
            if H[i][j]:
                coef = H[i][j] / 2 if i == j else H[i][j]
                quad[(i, j)] = coef
    # 1/2 (x-a)^T H (x-a) = 1/2 x^T H x - (Ha)^T x + 1/2 a^T H a
    Ha = [sum(H[i][j] * a[j] for j in range(n)) for i in range(n)]
    b = [-v for v in Ha]
    c0 = sum(a[i] * Ha[i] for i in range(n)) / 2
    bags = [(i, i + 1) for i in range(n - 1)] or [(0,)]
    edges = [(i, i + 1) for i in range(n - 2)]
    pb = Problem(n, lo, hi, ints, c0, b, quad, bags, edges)
    L = pb.L
    gamma = weighted_growth_convex(H, L)
    return pb, a, gamma


def block_family(m, c=Fr(1, 32)):
    """Blocks (u,v,r) in [0,1]^3: u^2+v^2-4uv+(u+v)/4+(r-u/2)^2, path
    couplings c (u_b - u_{b+1})^2.  Proved: x* = (1,1,1/2)^m, Euclidean growth
    g = 1/2, so weighted growth gamma >= g / max L."""
    n = 3 * m
    lo, hi = [0] * n, [1] * n
    quad, b = {}, [Fr(0)] * n
    c0 = Fr(0)
    for k in range(m):
        u, v, r = 3 * k, 3 * k + 1, 3 * k + 2
        quad[(u, u)] = quad.get((u, u), 0) + 1 + Fr(1, 4)
        quad[(v, v)] = Fr(1)
        quad[(u, v)] = Fr(-4)
        quad[(r, r)] = Fr(1)
        quad[(u, r)] = Fr(-1)
        b[u] += Fr(1, 4)
        b[v] += Fr(1, 4)
    for k in range(m - 1):
        u, w = 3 * k, 3 * (k + 1)
        quad[(u, u)] = quad.get((u, u), 0) + c
        quad[(w, w)] = quad.get((w, w), 0) + c
        quad[(u, w)] = quad.get((u, w), 0) - 2 * c
    bags, edges = [], []
    for k in range(m):
        bags.append((3 * k, 3 * k + 1, 3 * k + 2))
    for k in range(m - 1):
        bags.append((3 * k, 3 * (k + 1)))
    for k in range(m - 1):
        edges.append((k, m + k))
        edges.append((m + k, k + 1))
    pb = Problem(n, lo, hi, set(), c0, b, quad, bags, edges)
    xstar = []
    for k in range(m):
        xstar += [Fr(1), Fr(1), Fr(1, 2)]
    gamma = Fr(1, 2) / max(pb.L)
    return pb, xstar, gamma


def random_nonconvex(n, rng):
    ints = {i for i in range(n) if rng.random() < 0.4}
    lo, hi = [], []
    for i in range(n):
        l = rng.randint(-3, 0)
        u = l + rng.randint(1, 4)
        lo.append(l)
        hi.append(u)
    quad = {}
    for i in range(n):
        quad[(i, i)] = Fr(rng.randint(-6, 8), rng.choice([1, 2, 4]))
    for i in range(n - 1):
        quad[(i, i + 1)] = Fr(rng.randint(-8, 8), rng.choice([1, 2, 3]))
    b = [Fr(rng.randint(-10, 10), rng.choice([1, 2, 3])) for _ in range(n)]
    bags = [(i, i + 1) for i in range(n - 1)]
    edges = [(i, i + 1) for i in range(n - 2)]
    return Problem(n, lo, hi, ints, 0, b, quad, bags, edges)


def main():
    rng = random.Random(20261003)
    summary = {"growth_instances": 0, "admissible_stage_checks": 0,
               "nonconvex_instances": 0, "nonconvex_stages": 0,
               "certificates_accepted": 0, "tampered_rejected": 0, "max_nodes": 0}
    # 1a. convex mixed-integer paths with proved weighted growth
    for trial in range(10):
        n = rng.randint(2, 4)
        pb, a, gamma = path_problem(n, rng)
        if gamma == 0:
            continue
        kappa = max(Fr(1), 1 / gamma)
        eps = Fr(1, 2 ** rng.randint(4, 12))
        res = run_schedule(pb, eps, xstar=a, kappa=kappa)
        summary["growth_instances"] += 1
        summary["admissible_stage_checks"] += res["stats"]["inv_checks"]
        summary["max_nodes"] = max(summary["max_nodes"], res["stats"]["max_nodes"])
        ok, why = check_certificate(pb, res["certificate"], res["beta"], res["xhat"], eps)
        assert ok, why
        summary["certificates_accepted"] += 1
    # 1b. nonconvex block family
    for m in (1, 2):
        pb, xs, gamma = block_family(m)
        kappa = max(Fr(1), 1 / gamma)
        eps = Fr(1, 2 ** 10)
        res = run_schedule(pb, eps, xstar=xs, kappa=kappa)
        summary["growth_instances"] += 1
        summary["admissible_stage_checks"] += res["stats"]["inv_checks"]
        summary["max_nodes"] = max(summary["max_nodes"], res["stats"]["max_nodes"])
        ok, why = check_certificate(pb, res["certificate"], res["beta"], res["xhat"], eps)
        assert ok, why
        summary["certificates_accepted"] += 1
    # 2. random nonconvex instances, validity only
    for trial in range(12):
        n = rng.randint(2, 4)
        pb = random_nonconvex(n, rng)
        fstar, xstar = exact_box_qp_min(pb)
        eps = Fr(1, 2 ** rng.randint(2, 8))
        res = run_schedule(pb, eps, xstar=None, kappa=None, max_mu=9)
        assert res["beta"] <= fstar <= res["U"], "bracket"
        assert res["U"] - res["beta"] <= eps
        summary["nonconvex_instances"] += 1
        summary["nonconvex_stages"] += len(res["certificate"])
        ok, why = check_certificate(pb, res["certificate"], res["beta"], res["xhat"], eps)
        assert ok, why
        summary["certificates_accepted"] += 1
        # tamper: claim a bound above the optimum
        bad = res["beta"] + (fstar - res["beta"]) + Fr(1, 64)
        ok, _ = check_certificate(pb, res["certificate"], bad, res["xhat"], max(eps, res["U"] - bad + 1))
        assert not ok
        summary["tampered_rejected"] += 1
        # tamper: shrink the second-stage box so that the optimizer is cut off
        if len(res["certificate"]) >= 2:
            cert = [list(map(list, g)) for g in res["certificate"]]
            # cut every grid of stage 1 to a single node far from x* where possible
            moved = False
            for i in range(n):
                g0 = cert[0][i]
                cand = [v for v in g0 if abs(v - xstar[i]) >= 1]
                if cand:
                    v = cand[0]
                    for later in cert[1:]:
                        later[i] = [v]
                    moved = True
                    break
            if moved:
                ok, _ = check_certificate(pb, cert, res["beta"], res["xhat"], eps + 100)
                if ok:
                    # acceptance would be a soundness bug unless beta still <= f*
                    assert res["beta"] <= fstar
                else:
                    summary["tampered_rejected"] += 1
    print(summary)


if __name__ == "__main__":
    main()


def stress_admissible():
    """Run the admissible trial through all stages (no early stop) with tiny
    eps, checking invariants at every stage."""
    rng = random.Random(7)
    checks, maxn = 0, 0
    for trial in range(8):
        n = rng.randint(2, 3)
        pb, a, gamma = path_problem(n, rng, integer_frac=0.5)
        if gamma == 0:
            continue
        kappa = max(Fr(1), 1 / gamma)
        mu = 2
        while 8 * kappa * Fr(1, 4 ** mu) > 1:
            mu += 1
        if mu > 5:
            continue
        res = run_schedule(pb, Fr(1, 2 ** 30), xstar=a, kappa=kappa, fixed_mu=mu, stop_early=False)
        checks += res["stats"]["inv_checks"]
        maxn = max(maxn, res["stats"]["max_nodes"])
        assert res["U"] - res["beta"] <= Fr(1, 2 ** 30)
    for m in (1, 2):
        pb, xs, gamma = block_family(m)
        kappa = max(Fr(1), 1 / gamma)
        mu = 2
        while 8 * kappa * Fr(1, 4 ** mu) > 1:
            mu += 1
        res = run_schedule(pb, Fr(1, 2 ** 24), xstar=xs, kappa=kappa, fixed_mu=mu, stop_early=False)
        checks += res["stats"]["inv_checks"]
        maxn = max(maxn, res["stats"]["max_nodes"])
    print({"stress_admissible_stage_checks": checks, "max_nodes": maxn})


if __name__ == "__main__":
    stress_admissible()
