"""Targeted checks for the revision of window-exactness.md after review (float screening).

usage: python3 revision_checks.py PART [PART ...]   PART in rmaxidx sh om lb
  rmaxidx: toy plus (k = 0.5), maximal recursion (eps = 0): b^T Phat_{s+1} b - b^T w (the tabulated
           eta_hat_1) against b^T (F^T Phat_{s+2} b - w) (the formula printed in Section 7.6 before the
           revision).  For the toy F = 1, b = 1, w = -k.
  sh:      isotropic (H3)/(W5) margin of (SH) for the families of Sections 7.1 and 7.5:
           (SH) needs one mu > 0 with grad_x^2 r >= mu I and |sigma| > Delta |beta|^2 / (2 mu) (t != tau),
           i.e. sup_t Delta |beta|^2 / (2 |sigma|) < inf_t lambda_min(M).  Also reports the anisotropic
           (global-form) margin lambda_min(M - 2 eps I - (Delta / (2|sigma|)) beta beta^T).
  om:      Osmolovskii-Maurer switch term: (D - Delta^2 kappa_tau) + Delta^2 b^T Q(tau+) b against F''(tau)
           by finite differences of the continuous cost J(theta) ([E] examples A, A-, A0').
  lb:      toy plus: exact identity J_plus(u) = J_zero(u) - (k/2) h^2 sum u_t^2, and the convexification
           bound f*_plus >= min J_zero - (k/2) h^2 N, compared with the K = 2 window bound.
Writes logs/revision_<part>.json.
"""
import json
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "n2"))
from toy import VERIFIER, TOYPLUS, TOYZERO, kkt, fam_rmax, simulate  # noqa: E402
from toy_cont import switch, sigma as toy_sigma  # noqa: E402
from model import A, B, continuous_family, find_switch, solve_arcs, switch_quantities, Fpp_fd  # noqa: E402
from n2win import EXAMPLES  # noqa: E402

warnings.filterwarnings("ignore")
LOG = os.path.join(HERE, "logs")


def dump(name, obj):
    with open(os.path.join(LOG, f"revision_{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def tau_of(toy):
    return [r for r in switch(toy) if r["pmp_viol"] < 1e-9][0]["tau"]


# ------------------------------------------------------------------------------------------ rmaxidx
def part_rmaxidx():
    out = []
    k = TOYPLUS.k
    for N in (500, 1000, 2000, 4000, 8000):
        kk = kkt(TOYPLUS, N)
        s = kk["s"]
        P, brk = fam_rmax(TOYPLUS, kk, eps=0.0)
        rec = dict(N=N, s=s, frac=kk["frac"], break_stage=None if brk is None else int(brk - s),
                   eta_hat_1_Phat_s1=float(P[s + 1] + k), b_beta_Phat_s2=float(P[s + 2] + k),
                   m_s_if_interior=float(P[s + 1]))
        print(json.dumps(rec), flush=True)
        out.append(rec)
    dump("rmaxidx", out)


# ------------------------------------------------------------------------------------------ sh
def toy_margin(toy, Pf, dPf, npts=20001):
    tau = tau_of(toy)
    tt = np.concatenate([np.linspace(0, tau, npts)[:-1], tau + np.geomspace(1e-7, toy.T - tau, npts)])
    tt = tt[np.abs(tt - tau) > 0]
    M = np.array([dPf(t) + 1.0 for t in tt])             # H_xx = 1, g_x = 0
    beta = np.array([Pf(t) + toy.k for t in tt])          # beta = P b - w, w = -k, b = 1
    sig = np.abs([toy_sigma(toy, t, tau) for t in tt])
    ratio = 2.0 * beta ** 2 / (2.0 * sig)                 # Delta = 2
    return dict(inf_lambda_min_M=float(M.min()), sup_ratio=float(ratio.max()),
                t_sup_ratio=float(tt[int(ratio.argmax())]), isotropic_ok=bool(ratio.max() < M.min()))


def n2_margin(p, eps, delta1=0.1, npts=6000, hstep=1e-6):
    Pf, dg = continuous_family(p, eps, delta1=delta1)
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    Delta = abs(p.ub - p.ua)
    Hxx, w = p.Hxx, p.w
    gap = 5e-5
    tt = np.concatenate([np.linspace(0 + gap, th - gap, npts), np.linspace(th + gap, th + delta1 - gap, npts),
                         np.linspace(th + delta1 + gap, p.T - gap, npts)])
    lmin, lmax, ratio, aniso, aniso_last = [], [], [], [], []
    for t in tt:
        P = Pf(t)
        dP = (Pf(t + hstep) - Pf(t - hstep)) / (2 * hstep)
        M = dP + A.T @ P + P @ A + Hxx
        M = (M + M.T) / 2
        beta = P @ B - w
        sg = abs((sol["a"]["sig"] if t < th else sol["b"]["sig"])(t))
        ev = np.linalg.eigvalsh(M)
        lmin.append(ev[0])
        lmax.append(ev[-1])
        ratio.append(Delta * beta @ beta / (2 * sg))
        a = float(np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - (Delta / (2 * sg)) * np.outer(beta, beta))[0])
        aniso.append(a)
        if t > th + delta1:
            aniso_last.append(a)
    lmin, ratio = np.array(lmin), np.array(ratio)
    return dict(eps=eps, delta1=delta1, pre_blowup=bool(dg["pre_blowup"]), inf_lambda_min_M=float(lmin.min()),
                sup_lambda_max_M=float(np.max(lmax)), sup_ratio=float(ratio.max()),
                t_sup_ratio=float(tt[int(ratio.argmax())]), isotropic_ok=bool(ratio.max() < lmin.min()),
                aniso_margin_min=float(np.min(aniso)), aniso_margin_last_arc_absmax=float(np.max(np.abs(aniso_last))))


def part_sh():
    out = {}
    tV, tP = tau_of(VERIFIER), tau_of(TOYPLUS)
    c = 0.3
    fams = {
        "verifier_linear_rate": (VERIFIER, lambda t: 0.5 if t <= tV else 0.5 - c * (t - tV),
                                 lambda t: 0.0 if t <= tV else -c),
        "plus_const": (TOYPLUS, lambda t: -0.5, lambda t: 0.0),
        "zero_kink": (TOYZERO, lambda t: 0.0 if t <= tP else -c * (t - tP), lambda t: 0.0 if t <= tP else -c),
        "zero_affine": (TOYZERO, lambda t: 0.0, lambda t: 0.0),
    }
    for name, (toy, Pf, dPf) in fams.items():
        out[name] = toy_margin(toy, Pf, dPf)
        print(name, out[name], flush=True)
    for name, eps in (("A", 0.02), ("Aminus", 0.02), ("Azero", 0.02), ("Azero", 0.1)):
        key = f"{name}_eps{eps}"
        out[key] = n2_margin(EXAMPLES[name], eps)
        print(key, out[key], flush=True)
    dump("sh", out)


# ------------------------------------------------------------------------------------------ om
def part_om():
    out = {}
    for name in ("A", "Aminus", "Azero"):
        p = EXAMPLES[name]
        th = find_switch(p)[0]
        sq = switch_quantities(p, solve_arcs(p, th))
        Delta = sq["Delta"]
        kap = float(B @ p.w)
        bQb = float(B @ sq["Qplus"] @ B)
        switch_term = sq["D"] - Delta ** 2 * kap
        arc_term = Delta ** 2 * bQb
        _, fd = Fpp_fd(p, th)
        rec = dict(tau=th, kappa_tau=kap, D=sq["D"], switch_term=switch_term, arc_term=arc_term,
                   OM_total=switch_term + arc_term, Fpp_formula=sq["Fpp_formula"], Fpp_fd=fd)
        print(name, rec, flush=True)
        out[name] = rec
    dump("om", out)


# ------------------------------------------------------------------------------------------ lb
def part_lb():
    with open(os.path.join(LOG, "toy_scip.json")) as f:
        scip = {r["N"]: r["window_K2_bound"] for r in json.load(f)}
    with open(os.path.join(LOG, "toy_plus.json")) as f:
        plus = {r["N"]: [w for w in r["windows"] if w["K"] == 2][0]["deficit_over_h2"] for r in json.load(f)}
    k = TOYPLUS.k
    out = []
    for N in (50, 100, 150, 200, 1000, 4000, 8000):
        kp, kz = kkt(TOYPLUS, N), kkt(TOYZERO, N)
        h = kp["h"]
        _, Jz_at_ubar = simulate(TOYZERO, N, kp["u"])
        ident = kp["J"] - (Jz_at_ubar - k / 2 * h * h * float(np.sum(kp["u"] ** 2)))
        lb = kz["J"] - k / 2 * h * h * N
        rec = dict(N=N, frac=kp["frac"], identity_residual=float(ident), zero_kkt_viol=kz["kkt_viol"],
                   convex_gap_over_h2=float((kp["J"] - lb) / h ** 2))
        if N in scip:
            rec["window_K2_deficit_over_h2"] = float((kp["J"] - scip[N]) / h ** 2)
        elif N in plus:
            rec["window_K2_deficit_over_h2"] = float(plus[N])
        print(json.dumps(rec), flush=True)
        out.append(rec)
    dump("lb", out)


if __name__ == "__main__":
    parts = dict(rmaxidx=part_rmaxidx, sh=part_sh, om=part_om, lb=part_lb)
    for q in sys.argv[1:]:
        print("====", q, flush=True)
        parts[q]()
