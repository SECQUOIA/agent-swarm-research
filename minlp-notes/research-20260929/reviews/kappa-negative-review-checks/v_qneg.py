"""Reviewer's independent exact certificate for the q < 0 toy of kappa-negative.md Section 5.3
(k = 3, Phi = x - x^2, kappa_tau = -3), by a route that does not use calibrations at all:

1. H_tt = h^2 (h (N - 1 - t) + phi2) < 0 for every t (phi2 = -2, h (N - 1) < 2), so J is concave in each
   coordinate and f* = min over {-1, 1}^N (move coordinates to vertices one at a time).
2. Identity (x' = u, x_0 = 0): sum_t h k x_t u_t = (k/2) x_N^2 - (k/2) h^2 sum_t u_t^2, so
   J = Jc - (k/2) h^2 sum u_t^2 with Jc = h sum (x_t - a_t)^2 / 2 + phi1 x_N + (phi2 + k) x_N^2 / 2,
   strictly convex here (phi2 + k = 1).  On any box node, J >= Jc - (k/2) h^2 N.
3. Branch and bound: node = some coordinates fixed to +-1 (valid by 1.), bound = min Jc over the node
   box - (k/2) h^2 N (exact convex QP: a candidate from a pattern scan, accepted only if it satisfies
   the exact KKT conditions of the convex QP).  Branch on a fractional coordinate of the QP minimizer.
usage: OMP_NUM_THREADS=1 python3 v_qneg.py N [N ...]
"""
import json
import sys
import time
from fractions import Fraction as Fr

from vtoy import Toy, traj, H_entry, best_single_switch, kkt_check, node_bound

K = Fr(3)
PHI1, PHI2 = Fr(1), Fr(-2)


def jc_traj(N, u):
    h = Fr(2) / N
    x = [Fr(0)]
    for t in range(N):
        x.append(x[t] + h * u[t])
    a = [Fr(2) if Fr(t) * 2 / N < 1 else Fr(-1) for t in range(N)]
    Jc = sum(h * (x[t] - a[t]) ** 2 / 2 for t in range(N)) + PHI1 * x[N] + (PHI2 + K) * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = PHI1 + (PHI2 + K) * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t])
    g = [h * p[t + 1] for t in range(N)]          # dJc/du_t
    return dict(x=x, Jc=Jc, g=g, h=h)


def Hc(N, i, j):
    h = Fr(2) / N
    return h * h * (h * (N - 1 - max(i, j)) + PHI2 + K)


def qp_kkt(N, u, fixed, g):
    for t in range(N):
        if t in fixed:
            continue
        if u[t] == 1 and g[t] > 0:
            return False
        if u[t] == -1 and g[t] < 0:
            return False
        if -1 < u[t] < 1 and g[t] != 0:
            return False
    return True


def solve_node(N, fixed, m_guess):
    """min Jc over {u_t = fixed[t]} x [-1, 1]^(free): scan patterns (+1 before m, u_m free 1-D optimum,
    -1 after, fixed coordinates kept), then 2-D refinement on adjacent pairs; accept exact KKT only."""
    best = None
    for m in range(max(0, m_guess - 8), min(N, m_guess + 9)):
        u = [Fr(1) if t < m else Fr(-1) for t in range(N)]
        for t, v in fixed.items():
            u[t] = v
        cands = [u]
        if m not in fixed:
            u0 = list(u); u0[m] = Fr(0)
            T0 = jc_traj(N, u0)
            Hmm = Hc(N, m, m)
            v = min(Fr(1), max(Fr(-1), -T0["g"][m] / Hmm))
            u1 = list(u0); u1[m] = v
            cands.append(u1)
        for uu in cands:
            T = jc_traj(N, uu)
            if qp_kkt(N, uu, fixed, T["g"]):
                if best is None or T["Jc"] < best[0]:
                    best = (T["Jc"], uu)
    if best is None:
        # two fractional stages around a fixed coordinate: solve the 2-D QP on (m, m+1) for each m
        for m in range(max(0, m_guess - 8), min(N - 1, m_guess + 9)):
            for skip in (0, 1):
                i, j = m, m + 1 + skip
                if i in fixed or j in fixed or j >= N:
                    continue
                u = [Fr(1) if t < i else Fr(-1) for t in range(N)]
                for t, v in fixed.items():
                    u[t] = v
                u[i] = u[j] = Fr(0)
                T0 = jc_traj(N, u)
                a11, a12, a22 = Hc(N, i, i), Hc(N, i, j), Hc(N, j, j)
                b1, b2 = -T0["g"][i], -T0["g"][j]
                det = a11 * a22 - a12 * a12
                vi, vj = (b1 * a22 - a12 * b2) / det, (a11 * b2 - a12 * b1) / det
                if -1 <= vi <= 1 and -1 <= vj <= 1:
                    uu = list(u); uu[i], uu[j] = vi, vj
                    T = jc_traj(N, uu)
                    if qp_kkt(N, uu, fixed, T["g"]):
                        if best is None or T["Jc"] < best[0]:
                            best = (T["Jc"], uu)
    assert best is not None, ("no exact KKT point found", fixed)
    return best


def run(N):
    t0 = time.time()
    h = Fr(2) / N
    # identity check at a random-ish rational control
    toy = Toy(a_pts=((0, 2), (1, -1)), k_pts=((0, K),), phi1=PHI1, phi2=PHI2, R=3)
    ut = [Fr((7 * t) % 13 - 6, 6) for t in range(N)]
    ident = traj(toy, N, ut)["J"] - (jc_traj(N, ut)["Jc"] - K / 2 * h * h * sum(v * v for v in ut))
    assert ident == 0
    assert all(H_entry(toy, N, toy.data(N)[1], t, t) < 0 for t in (0, N // 2, N - 1))
    const = K / 2 * h * h * N
    m_guess = round(Fr(56, 100) / h)
    stack = [dict()]
    inc = None
    nodes = []
    while stack:
        fixed = stack.pop()
        Jc, u = solve_node(N, fixed, m_guess)
        bound = Jc - const
        frac = [t for t in range(N) if -1 < u[t] < 1]
        rec = dict(fixed={t: int(v) for t, v in fixed.items()}, frac=frac)
        if not frac:
            Jv = traj(toy, N, u)["J"]
            assert Jv == bound
            if inc is None or Jv < inc[0]:
                inc = (Jv, u)
            rec["leaf"] = "vertex"
            nodes.append(rec)
            continue
        if inc is not None and bound >= inc[0]:
            rec["leaf"] = "pruned"
            nodes.append(rec)
            continue
        t = frac[0]
        rec["branch"] = t
        nodes.append(rec)
        stack.append({**fixed, t: Fr(-1)})
        stack.append({**fixed, t: Fr(1)})
    # re-check pruned nodes against the final incumbent (they were pruned against a larger or equal one)
    fstar, ustar = inc
    sw = [t for t in range(1, N) if ustar[t] != ustar[t - 1]]
    # compare with the best single-switch KKT point of J and its plain calibration gap
    E = best_single_switch(toy, N)
    ok, frac = kkt_check(E)
    P = [-K] * (N + 1)
    lo = [Fr(-1)] * N; hi = [Fr(1)] * N
    B0, losses, LN = node_bound(toy, E, P, lo, hi)
    wst = sorted(((float(abs(E["sig"][t]) / h), t) for t in range(N)))[:3]
    print(json.dumps(dict(N=N, fstar=float(fstar), switch_stages=sw, n_nodes=len(nodes), nodes=nodes,
                          single_switch_kkt=ok, single_switch_frac=frac,
                          single_switch_J_minus_fstar_h2=float((E["J"] - fstar) / h ** 2),
                          plain_gap_h2=float((E["J"] - B0) / h ** 2),
                          smallest_margins_sig_over_h=wst, time=round(time.time() - t0, 1))), flush=True)


if __name__ == "__main__":
    for N in sys.argv[1:]:
        run(int(N))
