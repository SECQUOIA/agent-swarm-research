"""Reviewer runs for window-exactness.md, Section 7 (scalar toys).  usage: python3 rv_runs.py PART
PART in: verifier plus zero lb phase rmax.  Each part prints JSON lines and writes logs/<part>.json."""
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rv_toy import (VER, PLUS, ZERO, Toy, tau_of, kkt, exact_kkt, simulate, fam, stage_loss, terminal_loss,  # noqa: E402
                    window_problem, boxqp_min, boxqp_min_np)

OUT = []


def emit(rec):
    print(json.dumps(rec, default=float), flush=True)
    OUT.append(rec)


def dump(name):
    with open(os.path.join(HERE, "logs", f"{name}.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=float)


def window_min(toy, E, P, a, b, exact):
    g, H, lo, hi, states = window_problem(toy, E, P, a, b)
    if exact:
        val, v = boxqp_min(g, H, lo, hi, exact=True)
    else:
        val, v = boxqp_min_np([float(q) for q in g], [[float(q) for q in r] for r in H],
                              [float(q) for q in lo], [float(q) for q in hi])
        v = [Fr(float(q)) for q in v]
    xs = states([Fr(q) if not isinstance(q, Fr) else q for q in v])
    inside = all(-toy.R <= float(q) <= toy.R for q in xs)
    return val, v, inside


# ------------------------------------------------------------------------------------ verifier
def part_verifier():
    toy = VER
    tau = tau_of(toy)[0][0]
    lin = lambda t: 0.5 if t <= tau else 0.5 - 0.3 * (t - tau)
    for N in (500, 1000, 2000, 4000, 8000):
        t0 = time.time()
        kk = kkt(toy, N)
        E = exact_kkt(toy, N, kk["u"])
        P = fam(E, lin)
        losses = [stage_loss(toy, E, P, t) for t in range(N)]
        LN = terminal_loss(toy, E, P)
        gap = sum(losses, Fr(0)) + LN
        PB = fam(E, lambda t: 0.5)
        LBN = terminal_loss(toy, E, PB)
        rec = dict(N=N, s=kk["s"], inter=kk["inter"], u_inter=[float(E["u"][i]) for i in kk["inter"]], float_kkt_viol=kk["viol"],
                   lin_gap_exact=float(gap), lin_gap_is_zero=(gap == 0), lin_n_failing=sum(1 for q in losses if q > 0),
                   lin_terminal_loss=float(LN), famB_terminal_loss_exact=float(LBN), famB_terminal_closed_form=(2 + abs(float(E["x"][N]))) ** 2 / 4,
                   time=time.time() - t0)
        if N == 1000:
            rec["famB_stage_losses_max"] = float(max(stage_loss(toy, E, PB, t) for t in range(N)))
        emit(rec)


# ------------------------------------------------------------------------------------ plus
def part_plus():
    toy = PLUS
    k = toy.k
    for N in (500, 1000, 2000, 4000, 8000):
        t0 = time.time()
        kk = kkt(toy, N)
        E = exact_kkt(toy, N, kk["u"])
        h = E["h"]
        s = kk["s"]
        P = fam(E, lambda t: -k)
        near = {t - s: float(stage_loss(toy, E, P, t) / h ** 2) for t in range(s - 4, s + 5)}
        pred = {}
        for t in range(s - 4, s + 5):
            ub, sg = float(E["u"][t]), float(E["sig"][t] / h)
            if -1 < ub < 1:
                pred[t - s] = 0.5 * k * max(1 - ub, 1 + ub) ** 2
            else:
                pred[t - s] = max(0.0, 2 * k - 2 * abs(sg))   # (h^2 k Delta^2/2 - h|sig|Delta)/h^2, Delta = 2
        rec = dict(N=N, s=s, inter=kk["inter"], u_inter=[float(E["u"][i]) for i in kk["inter"]], float_kkt_viol=kk["viol"],
                   sig_over_h=[float(E["sig"][t] / h) for t in (s - 1, s, s + 1)],
                   stage_loss_over_h2={q: v for q, v in near.items() if v != 0}, pred_over_h2={q: v for q, v in pred.items() if v > 0},
                   far_stage_max_loss_float=None, windows=[])
        # all stages (float family on float data) to confirm that only near-switch stages fail
        Ef = simulate(toy, N, [float(q) for q in E["u"]], exact=False)
        Pf = fam(Ef, lambda t: -k)
        far = [stage_loss(toy, Ef, Pf, t) for t in range(1, N) if abs(t - s) > 4]
        rec["far_stage_max_loss_float"] = float(max(far))
        for K in range(0, 5):
            a, b = s - K, s + K + 1
            val, v, inside = window_min(toy, E, P, a, b, exact=False)
            row = dict(K=K, deficit_over_h2_float=float(-val / h ** 2), argmin_states_in_box=inside,
                       argmin_om=[round(float(q), 4) for q in v[1:]], argmin_da_over_h=float(v[0] / h))
            if K <= 2 and N in (1000, 4000):
                vx, _, _ = window_min(toy, E, P, a, b, exact=True)
                row["deficit_over_h2_exact"] = float(-vx / h ** 2)
            rec["windows"].append(row)
        # fixed-entry windows [0, b): smallest b - 1 - n with J_W(flip) >= J_W(zbar) (flip: farther bound)
        if kk["inter"]:
            n = kk["inter"][0]
            ub = E["u"][n]
            om = (1 if ub < 0 else -1) - ub
            hh = float(h)
            # J_W(flip) - J_W(zbar) for window [0,b) = -(k/2)h^2 om^2 [stage n] + sum_{t=n+1}^{b-1} rho_t increments
            # computed directly by simulation (float) for each b
            uu = [float(q) for q in E["u"]]
            u2 = list(uu)
            u2[n] += float(om)
            x1 = np.concatenate([[0.0], np.cumsum(hh * np.array(uu))])
            x2 = np.concatenate([[0.0], np.cumsum(hh * np.array(u2))])
            at = np.array(toy.a_list(N), float)
            L1 = hh * ((x1[:N] - at[:N]) ** 2 / 2 + k * x1[:N] * np.array(uu))
            L2 = hh * ((x2[:N] - at[:N]) ** 2 / 2 + k * x2[:N] * np.array(u2))
            cum = np.cumsum(L2 - L1)
            pf = np.array([float(q) for q in E["p"]])
            Pb = -k
            found = None
            for b in range(n + 1, N + 1):
                dS = pf[b] * (x2[b] - x1[b]) + Pb * (x2[b] - x1[b]) ** 2 / 2
                if cum[b - 1] + dS >= 0:
                    found = b - 1 - n
                    break
            rec["fixed_entry_min_post_stages"] = found
            rec["fixed_entry_duration"] = None if found is None else found * hh
        rec["time"] = time.time() - t0
        emit(rec)


# ------------------------------------------------------------------------------------ zero
def part_zero():
    toy = ZERO
    tau = tau_of(toy)[0][0]
    kink = lambda t: 0.0 if t <= tau else -0.3 * (t - tau)
    for N in (1000, 2000, 4000, 8000, 16000):
        t0 = time.time()
        kk = kkt(toy, N)
        E = exact_kkt(toy, N, kk["u"])
        h = E["h"]
        s = kk["s"]
        P = fam(E, kink)
        losses = {t: stage_loss(toy, E, P, t) for t in range(N)}
        fail = {t - s: float(v / h ** 3) for t, v in losses.items() if v > 0}
        P0 = fam(E, lambda t: 0.0)
        L0 = max(stage_loss(toy, E, P0, t) for t in range(s - 50, s + 50))
        rec = dict(N=N, s=s, inter=kk["inter"], u_inter=[float(E["u"][i]) for i in kk["inter"]],
                   P_next_over_h=float(P[s + 1] / h), failing_exact_over_h3=fail, terminal_loss=float(terminal_loss(toy, E, P)),
                   affine_near_switch_max_loss_exact=float(L0), windows=[])
        if kk["inter"]:
            n = kk["inter"][0]
            ub = float(E["u"][n])
            c = -float(P[n + 1] / h)
            om = max(1 - ub, 1 + ub)
            rec["pred_loss_over_h3"] = 0.5 * om * om * c / (1 - c)
        for K in range(0, 4):
            a, b = s - K, s + K + 1
            row = dict(K=K)
            if K <= 2 and N in (1000, 4000, 8000):
                vx, _, _ = window_min(toy, E, P, a, b, exact=True)
                row["exact_min"] = float(vx)
                row["exact_min_is_zero"] = (vx == 0)
                row["exact_deficit_over_h3"] = float(-vx / h ** 3)
            vf, _, _ = window_min(toy, E, P, a, b, exact=False)
            row["float_deficit_over_h3"] = float(-vf / h ** 3)
            rec["windows"].append(row)
        rec["time"] = time.time() - t0
        emit(rec)


# ------------------------------------------------------------------------------------ lb (global check of toy plus)
def zero_objective_and_grad(N, u):
    """J_zero(u) = J_plus(u) + (k/2) h^2 sum u^2 (exact identity for x0 = 0), and its gradient h sig_zero."""
    Z = simulate(ZERO, N, u, exact=True)
    return Z["J"], [Z["h"] * q for q in Z["sig"]]


def part_lb():
    """Rigorous lower bound on f*(plus): J_plus(u) = J_zero(u) - (k/2) h^2 sum u_t^2 >= J_zero(u) - (k/2) h^2 N,
    and J_zero is convex, so f*(plus) >= min J_zero - (k/2) h^2 N = J_zero(u_zero_KKT) - (k/2) h^2 N (exact KKT).
    Then a small branch and bound on the secant relaxation tightens it (node bounds by exact linearization)."""
    k = Fr(1, 2)
    for N in (50, 100, 150, 200, 1000, 4000):
        t0 = time.time()
        kp = kkt(PLUS, N)
        Ep = exact_kkt(PLUS, N, kp["u"])
        h = Ep["h"]
        # identity check at the plus KKT point
        Jz_at_p, _ = zero_objective_and_grad(N, Ep["u"])
        ident = Jz_at_p - k / 2 * h * h * sum(q * q for q in Ep["u"]) - Ep["J"]
        kz = kkt(ZERO, N)
        Ez = exact_kkt(ZERO, N, kz["u"])
        LB0 = Ez["J"] - k / 2 * h * h * N
        s = kp["s"]
        P = fam(Ep, lambda t: -0.5)
        win = {}
        for K in (0, 2):
            val, _, _ = window_min(PLUS, Ep, P, s - K, s + K + 1, exact=(N <= 1000 and K <= 2))
            win[K] = Fr(val) if not isinstance(val, Fr) else val
        rec = dict(N=N, inter=kp["inter"], zero_inter=kz["inter"], identity_residual=float(ident),
                   J_plus_kkt=float(Ep["J"]), root_LB_gap=float(Ep["J"] - LB0),
                   root_LB_gap_over_h2=float((Ep["J"] - LB0) / h ** 2),
                   window_K0_deficit=float(-win[0]), window_K2_deficit=float(-win[2]),
                   root_LB_above_window_K2_bound=bool(LB0 > Ep["J"] + win[2]),
                   root_LB_above_window_K0_bound=bool(LB0 > Ep["J"] + win[0]))
        if N <= 200:
            rec.update(bnb(N, Ep, h, k))
        rec["time"] = time.time() - t0
        emit(rec)


def bnb(N, Ep, h, k, tol=Fr(1, 10 ** 11), max_nodes=400):
    """Branch and bound on u in [-1,1]^N for J_plus = J_zero - (k/2) h^2 sum u^2 with secant underestimators.
    Node relaxation R(u) = J_zero(u) - (k/2) h^2 sum_i [(l_i + r_i) u_i - l_i r_i] (convex).  Its minimum is
    located by a float primal active-set method; the node bound is the exact linearization bound
    R(u0) + sum_i min(g_i (l_i - u0_i), g_i (r_i - u0_i)) <= min R (valid for any u0 since R is convex)."""
    hf = float(h)
    idx = np.arange(N)
    M = (N - 1 - np.maximum.outer(idx, idx)).astype(float)
    Hz = hf ** 3 * M + 0.5 * hf ** 2 * np.ones((N, N))       # Hessian of J_zero (for the float search only)
    UB = Ep["J"]

    def relax(lo, hi):
        lo_f, hi_f = np.array([float(q) for q in lo]), np.array([float(q) for q in hi])
        sec = -(float(k) / 2) * hf ** 2 * (lo_f + hi_f)
        # float gradient of J_zero at 0 (linear term)
        _, g0 = zero_objective_and_grad(N, [Fr(0)] * N)
        q = np.array([float(v) for v in g0]) + sec
        u = np.clip(np.array([float(v) for v in Ep["u"]]), lo_f, hi_f)
        W = set(i for i in range(N) if u[i] in (lo_f[i], hi_f[i]))
        for _ in range(4 * N):
            F = np.array(sorted(set(range(N)) - W), dtype=int)
            g = Hz @ u + q
            p = np.zeros(N)
            if len(F):
                p[F] = np.linalg.solve(Hz[np.ix_(F, F)], -g[F])
            if np.max(np.abs(p)) < 1e-14:
                mult = {i: g[i] if u[i] == lo_f[i] else -g[i] for i in W}
                bad = [i for i, m_ in mult.items() if m_ < -1e-14]
                if not bad:
                    break
                W.discard(min(bad, key=lambda i: mult[i]))
                continue
            alpha, blk = 1.0, None
            for i in F:
                if p[i] > 0 and u[i] + p[i] > hi_f[i]:
                    a_ = (hi_f[i] - u[i]) / p[i]
                    if a_ < alpha:
                        alpha, blk = a_, i
                elif p[i] < 0 and u[i] + p[i] < lo_f[i]:
                    a_ = (lo_f[i] - u[i]) / p[i]
                    if a_ < alpha:
                        alpha, blk = a_, i
            u = u + alpha * p
            if blk is not None:
                u[blk] = hi_f[blk] if p[blk] > 0 else lo_f[blk]
                W.add(blk)
        u0 = [min(max(Fr(float(v)), lo[i]), hi[i]) for i, v in enumerate(u)]
        Jz, gz = zero_objective_and_grad(N, u0)
        R = Jz - k / 2 * h * h * sum((lo[i] + hi[i]) * u0[i] - lo[i] * hi[i] for i in range(N))
        gR = [gz[i] - k / 2 * h * h * (lo[i] + hi[i]) for i in range(N)]
        LBn = R + sum(min(gR[i] * (lo[i] - u0[i]), gR[i] * (hi[i] - u0[i])) for i in range(N))
        # J_plus at u0 (upper bound candidate) and secant gaps
        Jp = simulate(PLUS, N, u0, exact=True)["J"]
        gaps = [(k / 2 * h * h * ((lo[i] + hi[i]) * u0[i] - lo[i] * hi[i] - u0[i] * u0[i]), i) for i in range(N)]
        return LBn, Jp, u0, max(gaps)
    one = Fr(1)
    nodes = [([-one] * N, [one] * N)]
    global_lb_open = []
    n_nodes = 0
    root_lb = None
    while nodes and n_nodes < max_nodes:
        lo, hi = nodes.pop()
        n_nodes += 1
        LBn, Jp, u0, (gmax, j) = relax(lo, hi)
        if root_lb is None:
            root_lb = LBn
        UB = min(UB, Jp)
        if LBn >= UB - tol:
            continue
        # branch at the relaxation value of u_j
        mid = u0[j]
        if not (lo[j] < mid < hi[j]):
            mid = (lo[j] + hi[j]) / 2
        l1, h1 = list(lo), list(hi)
        h1[j] = mid
        l2, h2 = list(lo), list(hi)
        l2[j] = mid
        nodes += [(l1, h1), (l2, h2)]
        global_lb_open.append(LBn)
    # remaining open nodes: their bounds (not refined)
    open_lbs = [relax(lo, hi)[0] for lo, hi in nodes]
    final_lb = min(open_lbs + [UB - tol]) if open_lbs else UB - tol
    return dict(bnb_nodes=n_nodes, bnb_open=len(nodes), bnb_root_lb_gap=float(Ep["J"] - root_lb),
                bnb_final_lb_gap=float(Ep["J"] - final_lb), bnb_UB_minus_Jkkt=float(UB - Ep["J"]))


# ------------------------------------------------------------------------------------ phase
def part_phase():
    for toy in (VER, PLUS, ZERO):
        Ns = list(range(101, 1101, 4))
        nint, ntwo, nviol, nexact = 0, 0, 0, 0
        for N in Ns:
            kk = kkt(toy, N)
            nint += len(kk["inter"]) >= 1
            ntwo += len(kk["inter"]) >= 2
            nviol += kk["viol"] > 1e-9
            if toy is PLUS:
                E = simulate(toy, N, list(kk["u"]), exact=False)
                P = fam(E, lambda t: -0.5)
                s = kk["s"]
                L = max(stage_loss(toy, E, P, t) for t in range(max(1, s - 6), s + 7))
                nexact += L <= 1e-14
        rec = dict(toy=toy.name, n=len(Ns), frac_interior=nint / len(Ns), two_interior=ntwo, kkt_violations=nviol)
        if toy is PLUS:
            rec["frac_stagewise_exact_near_switch"] = nexact / len(Ns)
        emit(rec)


# ------------------------------------------------------------------------------------ rmax
def part_rmax():
    for k in (0.5, 0.1):
        toy = Toy(f"k{k}", k=k, a2=-1, phi1=1, phi2=0)
        for N in (500, 1000, 2000, 4000, 8000, 16000, 32000):
            t0 = time.time()
            kk = kkt(toy, N)
            h, s, sig = kk["h"], kk["s"], kk["sig"]
            inter = set(kk["inter"])
            P = np.full(N + 1, np.nan)
            P[N] = toy.phi2
            brk = None
            for t in range(N - 1, -1, -1):
                beta = P[t + 1] + k             # F^T P b - w, w = -k, b = F = 1
                m = (0.0 if t in inter else abs(sig[t]) / h) + P[t + 1]   # 2|sig|/(h Delta) + b^T P b, Delta = 2
                if m <= 0:
                    brk = t
                    break
                P[t] = h + P[t + 1] - beta * beta / m
            rec = dict(k=k, N=N, s=s, inter=kk["inter"], kkt_viol=kk["viol"], break_rel=None if brk is None else brk - s,
                       eta_P_s1=float(P[s + 1] + k), eta_P_s2=float(P[s + 2] + k))
            if brk is None and N <= 4000:
                E = simulate(toy, N, list(kk["u"]), exact=False)
                Pl = [float(q) for q in P]
                rec["max_stage_loss_float"] = float(max(stage_loss(toy, E, Pl, t) for t in range(N)))
                rec["terminal_loss_float"] = float(terminal_loss(toy, E, Pl))
            rec["time"] = time.time() - t0
            emit(rec)


if __name__ == "__main__":
    part = sys.argv[1]
    dict(verifier=part_verifier, plus=part_plus, zero=part_zero, lb=part_lb, phase=part_phase, rmax=part_rmax)[part]()
    dump(part)
