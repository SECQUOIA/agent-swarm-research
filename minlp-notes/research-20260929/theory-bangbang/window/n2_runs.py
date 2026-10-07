"""Two-state runs for window-exactness.md (float screening).

usage: python3 n2_runs.py windows | rmax | azero
  windows: examples A (kappa_tau = +0.3), Aminus (-0.3), Azero (0) of n2win.py with the transferred
           linear-rate tangential family of extension-n2.md (eps = 0.02, delta1 = 0.1): stage losses
           over the reachable box, predicted leading-order losses, and window minima (all faces
           enumerated) for windows {s-K, ..., s+K}, K = 0..3, entry = reachable box.
  rmax:    discrete maximal recursion (extension-n2.md, Lemma 10, eps = 0) on Aminus: break stage and
           eta_hat = b.P_t b - b.w at t = s + K' (same index as toy_runs.py rmax, so that an interior
           stage s is exact iff kappa_tau + eta_hat[1] > 0), compared with the leading-order log law.
           (Revised: the first version used b.(Fx^T P_{t+1} b - w), one stage later; kept as b_beta.)
  azero:   degenerate example: single-direction bound and Schur certificate for larger windows.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from n2win import EXAMPLES, B, dz, transferred, window_quad, box_min_full  # noqa: E402
from model import find_switch, solve_arcs, switch_quantities  # noqa: E402

LOG = os.path.join(HERE, "logs")


def dump(name, obj):
    with open(os.path.join(LOG, f"n2_{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def pred_loss(kk, kap, t):
    """Leading-order stage loss / h^2: min over om of [sig om / h + kap om^2 / 2] (Delta = 2)."""
    h, u, sig = kk["h"], kk["u"], kk["sig"]
    if kap >= 0:
        return 0.0
    if t in kk["fracset"]:
        om = max(1 - u[t], 1 + u[t])
        return 0.5 * abs(kap) * om * om
    return max(0.0, -(2 * abs(sig[t]) / h + 0.5 * kap * 4))


def part_windows():
    out = []
    for name in ("A", "Aminus", "Azero"):
        p = EXAMPLES[name]
        th = find_switch(p)[0]
        sq = switch_quantities(p, solve_arcs(p, th))
        kap = float(B @ p.w)
        head = dict(example=name, tau=th, kappa_tau=kap, eta_L=sq["eta_L"], D=sq["D"], gamma=abs(sq["sigdot"]),
                    Fpp=sq["Fpp_formula"])
        print(json.dumps(head, default=float), flush=True)
        for N in (500, 1000, 2000, 4000, 8000):
            t0 = time.time()
            kk = dz.solve_kkt(p, N)
            h, s = kk["h"], kk["m"]
            Ps, dg = transferred(p, kk, 0.02, 0.1)
            loss, lossN = dz.stage_losses(p, kk, Ps)
            fail = {int(t) - s: float(loss[t] / h ** 2) for t in np.where(loss > 1e-14)[0]}
            pred = {t - s: pred_loss(kk, kap, t) for t in range(s - 3, s + 4)}
            rec = dict(head, N=N, s=s, frac=sorted(kk["fracset"]), u_frac=[float(kk["u"][t]) for t in sorted(kk["fracset"])],
                       kkt_viol=kk["kkt_viol"], pre_blowup=dg["pre_blowup"],
                       sig_over_h=[float(v) for v in kk["sig"][s - 2:s + 3] / h],
                       failing_loss_over_h2=fail, predicted_over_h2={q: v for q, v in pred.items() if v > 0},
                       max_loss_over_h3=float(loss.max() / h ** 3), terminal_loss=float(lossN), windows=[])
            for K in range(0, 4):
                a, b = s - K, s + K + 1
                g, H, lo, hi = window_quad(p, kk, Ps, a, b)
                val, v = box_min_full(g, H, lo, hi)
                rec["windows"].append(dict(K=K, deficit_over_h2=float(-val / h ** 2),
                                           stage_sum_over_h2=float(loss[a:b].sum() / h ** 2),
                                           argmin_om=[float(q) for q in v[2:]]))
            rec["time"] = time.time() - t0
            print(json.dumps(rec, default=float), flush=True)
            out.append(rec)
    dump("windows", out)


def part_rmax():
    out = []
    p = EXAMPLES["Aminus"]
    th = find_switch(p)[0]
    sq = switch_quantities(p, solve_arcs(p, th))
    gam = abs(sq["sigdot"])
    kap = float(B @ p.w)
    for N in (500, 1000, 2000, 4000, 8000, 16000, 32000):
        t0 = time.time()
        kk = dz.solve_kkt(p, N)
        h, s = kk["h"], kk["m"]
        Ps, brk, ms = dz.fam_rmax(p, kk, 0.0)
        F = dz.fx(h)
        eta, b_beta = {}, {}
        for Kp in (1, 4, 16, 64, 256):
            t = s + Kp
            if t <= N and not np.isnan(Ps[t]).any():
                eta[Kp] = float(B @ Ps[t] @ B - B @ p.w)
            if t + 1 <= N and not np.isnan(Ps[t + 1]).any():
                b_beta[Kp] = float(B @ (F.T @ Ps[t + 1] @ B - p.w))
        law = {Kp: 1.0 / (1.0 / sq["eta_L"] + (1.0 / gam) * np.log(1.0 / (Kp * h))) for Kp in (1, 4, 16, 64, 256)}
        rec = dict(N=N, s=s, frac=sorted(kk["fracset"]), break_stage=None if brk is None else int(brk - s),
                   eta_hat=eta, b_beta=b_beta, eta_law=law, kappa_tau=kap, time=time.time() - t0)
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    dump("rmax", out)


def certify_window(g, H, lo, hi, free):
    """Sufficient condition (float) for v = 0 to minimize g.v + v^T H v / 2 over the box, with g_F = 0
    on the free coordinates F (entry state and the failing control) and one-signed box ranges with
    g_t v_t = |g_t| |v_t| on the remaining (locked vertex) coordinates L:
      H_FF positive definite, and  |g_t| >= lam_minus * w_t / 2  for all t in L,
    where S = H_LL - H_LF H_FF^{-1} H_FL, lam_minus = max(0, -lambda_min(S)), w_t = box width.
    Then, minimizing over v_F in R^|F| first, the objective is >= sum_t |v_t| (|g_t| - lam_minus |v_t| / 2) >= 0.
    Returns a dict with the ingredients."""
    n = len(g)
    L = [i for i in range(n) if i not in free and hi[i] > lo[i]]
    F = list(free)
    HFF = H[np.ix_(F, F)]
    eF = float(np.linalg.eigvalsh(HFF).min())
    out = dict(HFF_min_eig=eF, gF_max=float(np.abs(g[F]).max()))
    if eF <= 0:
        out["certified"] = False
        return out
    S = H[np.ix_(L, L)] - H[np.ix_(L, F)] @ np.linalg.solve(HFF, H[np.ix_(F, L)])
    lam = max(0.0, -float(np.linalg.eigvalsh(S).min()))
    wid = np.array([hi[i] - lo[i] for i in L])
    onesided = all(lo[i] >= -1e-15 or hi[i] <= 1e-15 for i in L)
    ratio = float(np.min(np.abs(g[L]) / np.maximum(lam * wid / 2, 1e-300)))
    out.update(lam_minus=lam, min_margin_ratio=ratio, onesided=onesided, certified=bool(onesided and ratio >= 1.0))
    return out


def part_azero():
    """Degenerate example (kappa_tau = 0): the single stage n that fails does so at order h^3; the
    window {n-K, ..., n+K} repairs it once K exceeds a threshold that scales like 1 / eps
    (the strictness of the transferred family is M = 2 eps on the last arc).  The full window is
    certified with certify_window (entry box constraint relaxed, which only lowers the value)."""
    out = []
    p = EXAMPLES["Azero"]
    for eps in (0.1, 0.02):
        for N in (1000, 4000):
            kk = dz.solve_kkt(p, N)
            h, s = kk["h"], kk["m"]
            Ps, dg = transferred(p, kk, eps, 0.1)
            loss, lossN = dz.stage_losses(p, kk, Ps)
            n = int(np.argmax(loss))
            rec = dict(eps=eps, N=N, s=s, n_minus_s=n - s, frac=sorted(kk["fracset"]), pre_blowup=dg["pre_blowup"],
                       loss_n_over_h3=float(loss[n] / h ** 3), second_largest_loss=float(np.sort(loss)[-2]),
                       terminal_loss=float(lossN), windows=[])
            for K in (0, 1, 2, 4, 8, 16, 32, 64):
                g, H, lo, hi = window_quad(p, kk, Ps, n - K, n + K + 1)
                idx = [0, 1, 2 + K]
                val, _ = box_min_full(g[idx], H[np.ix_(idx, idx)], lo[idx], hi[idx])
                cert = certify_window(g, H, lo, hi, idx)
                rec["windows"].append(dict(K=K, one_direction_deficit_over_h3=float(-val / h ** 3), certificate=cert))
            print(json.dumps(rec, default=float), flush=True)
            out.append(rec)
    dump("azero", out)

if __name__ == "__main__":
    parts = dict(windows=part_windows, rmax=part_rmax, azero=part_azero)
    for q in sys.argv[1:]:
        print(f"==== {q}", flush=True)
        parts[q]()
