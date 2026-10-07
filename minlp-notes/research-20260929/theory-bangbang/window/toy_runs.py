"""Runs for window-exactness.md on the scalar toys of toy.py.

usage: python3 toy_runs.py PART [PART ...]   PART in cont verifier plus zero rmax scip
Each part writes logs/toy_<part>.json and prints a log.  Float screening unless a key says exact.
"""
import json
import os
import sys
import time
import warnings
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from toy import (VERIFIER, TOYPLUS, TOYZERO, Toy, kkt, float_data, exact_traj, exact_kkt_traj, fam_const, fam_fun,  # noqa: E402
                 fam_rmax, stage_losses, terminal_loss, window_value, window_quad, simulate)
from toy_cont import switch, family_margins  # noqa: E402

warnings.filterwarnings("ignore")
LOG = os.path.join(HERE, "logs")
NS = (500, 1000, 2000, 4000, 8000)


def dump(name, obj):
    with open(os.path.join(LOG, f"toy_{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def tau_of(toy):
    return [r for r in switch(toy) if r["pmp_viol"] < 1e-9][0]


def lin_rate(tau, c, top=0.5):
    """verifier toy: P = 1/2 before tau, 1/2 - c (t - tau) after (tangential: P(tau) b = w = 1/2)."""
    return (lambda t: top if t <= tau else top - c * (t - tau)), (lambda t: 0.0 if t <= tau else -c)


def kink_down(tau, c):
    """degenerate toy: P = 0 before tau, -c (t - tau) after (tangential: P(tau) b = w = 0)."""
    return (lambda t: 0.0 if t <= tau else -c * (t - tau)), (lambda t: 0.0 if t <= tau else -c)


# ------------------------------------------------------------------------------------------ cont
def part_cont():
    out = {}
    for name, toy in (("verifier", VERIFIER), ("plus", TOYPLUS), ("zero", TOYZERO)):
        sw = tau_of(toy)
        out[name] = dict(switch=sw)
        print(name, {k: round(v, 6) for k, v in sw.items()})
    tauV, tauP = out["verifier"]["switch"]["tau"], out["plus"]["switch"]["tau"]
    P, dP = lin_rate(tauV, 0.3)
    out["verifier"]["lin_rate_c0.3_eps0.01"] = family_margins(VERIFIER, tauV, P, dP, 0.01)
    out["verifier"]["famB_eps0"] = family_margins(VERIFIER, tauV, lambda t: 0.5, lambda t: 0.0, 0.0)
    out["plus"]["const_-k_eps0.1"] = family_margins(TOYPLUS, tauP, lambda t: -0.5, lambda t: 0.0, 0.1)
    P, dP = kink_down(tauP, 0.3)
    out["zero"]["kink_c0.3_eps0.01"] = family_margins(TOYZERO, tauP, P, dP, 0.01)
    out["zero"]["affine_eps0.1"] = family_margins(TOYZERO, tauP, lambda t: 0.0, lambda t: 0.0, 0.1)
    for n in out:
        for k, v in out[n].items():
            if k != "switch":
                print(n, k, v)
    dump("cont", out)


# ------------------------------------------------------------------------------------------ verifier
def exact_check(toy, kk, P, stages=None):
    """Exact rational stage minima and terminal term for the rational data (float controls taken as
    exact rationals, states and costates recomputed exactly).  Returns the exact gap J - B."""
    E = exact_kkt_traj(toy, kk["N"], kk["u"])
    L = stage_losses(toy, E, P, exact=True, stages=stages)
    LN = terminal_loss(toy, E, P, exact=True)
    gap = sum(L.values(), Fr(0)) + LN
    neg = min(L.values()) if L else Fr(0)
    return dict(J_exact=float(E["J"]), gap=float(gap), gap_is_zero=(gap == 0), terminal_loss=float(LN),
                max_stage_loss=float(max(L.values())) if L else None, min_stage_loss=float(neg),
                n_positive=sum(1 for v in L.values() if v > 0))


def part_verifier(exactN=(500, 1000, 2000, 4000, 8000)):
    toy = VERIFIER
    tau = tau_of(toy)["tau"]
    P_, _ = lin_rate(tau, 0.3)
    out = []
    for N in NS:
        t0 = time.time()
        kk = kkt(toy, N)
        D = float_data(toy, kk)
        s = kk["s"]
        rec = dict(N=N, s=s, frac=kk["frac"], u_frac=[float(kk["u"][i]) for i in kk["frac"]], kkt_viol=kk["kkt_viol"],
                   J=kk["J"], sig_over_h=[float(v) for v in kk["sig"][s - 2:s + 3] / kk["h"]])
        PB = fam_const(N, 0.5)
        LB = stage_losses(toy, D, PB)
        rec["famB"] = dict(max_stage_loss=max(LB.values()), terminal_loss=terminal_loss(toy, D, PB))
        P = fam_fun(toy, N, P_)
        L = stage_losses(toy, D, P)
        rec["lin"] = dict(failing=int(sum(v > 1e-14 for v in L.values())), max_stage_loss=max(L.values()),
                          terminal_loss=terminal_loss(toy, D, P), kappa_switch=float(P[s + 1]))
        if N in exactN:
            rec["lin"]["exact"] = exact_check(toy, kk, P)
            if N == 1000:
                rec["famB"]["exact"] = exact_check(toy, kk, PB, stages=[])
        rec["time"] = time.time() - t0
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    dump("verifier", out)


# ------------------------------------------------------------------------------------------ plus
def window_exact_flip(toy, kk, P, a, b, j):
    """Exact J_W change of the window trajectory x_a = xbar_a, u_j moved to its farther bound."""
    E = exact_kkt_traj(toy, kk["N"], kk["u"])
    g, H, lo, hi = window_quad(toy, E, P, a, b, exact=True)
    i = 1 + j - a
    v = [Fr(0)] * len(g)
    v[i] = lo[i] if abs(lo[i]) > abs(hi[i]) else hi[i]
    val = sum(g[r] * v[r] for r in range(len(g))) + sum(H[r][c] * v[r] * v[c] for r in range(len(g)) for c in range(len(g))) / 2
    return val, v[i], E


def fixed_entry_change(toy, kk, P, b, j, om):
    """J_W(z) - J_W(zbar) for the window [0, b) with x_0 fixed and u_j -> ubar_j + om (float)."""
    N, h = kk["N"], kk["h"]
    a = toy.a_of(N)
    u2 = kk["u"].copy()
    u2[j] += om
    x2 = toy.x0 + np.concatenate([[0.0], np.cumsum(h * u2)])
    x1, u1 = kk["x"], kk["u"]
    run = lambda x, u: h * np.sum((x[j:b] - a[j:b]) ** 2 / 2 + toy.k * x[j:b] * u[j:b])
    Sb = lambda xb: kk["p"][b] * xb + 0.5 * P[b] * (xb - x1[b]) ** 2
    return (run(x2, u2) + Sb(x2[b])) - (run(x1, u1) + Sb(x1[b]))



def part_plus(exactN=(1000, 4000)):
    toy = TOYPLUS
    k = toy.k
    out = []
    for N in NS:
        t0 = time.time()
        kk = kkt(toy, N)
        D = float_data(toy, kk)
        h, s = kk["h"], kk["s"]
        P = fam_const(N, -k)
        L = stage_losses(toy, D, P, stages=range(1, N))
        fail = {int(t - s): v / h ** 2 for t, v in L.items() if v > 1e-14}
        # leading-order prediction: fractional stage (k/2) om_hat^2; vertex stage 2 max(0, k - |sig|/h)
        pred = {}
        for t in range(s - 3, s + 4):
            if t in kk["frac"]:
                om = max(1 - kk["u"][t], 1 + kk["u"][t])
                pred[t - s] = 0.5 * k * om * om
            else:
                pred[t - s] = 2 * max(0.0, k - abs(kk["sig"][t]) / h)
        rec = dict(N=N, s=s, frac=kk["frac"], u_frac=[float(kk["u"][i]) for i in kk["frac"]], kkt_viol=kk["kkt_viol"],
                   sig_over_h=[float(v) for v in kk["sig"][s - 2:s + 3] / h],
                   failing_loss_over_h2=fail, predicted_over_h2={q: v for q, v in pred.items() if v > 0},
                   terminal_loss=terminal_loss(toy, D, P), windows=[])
        for K in range(0, 5):
            a, b = s - K, s + K + 1
            v, z = window_value(toy, D, P, a, b)
            rec["windows"].append(dict(K=K, deficit_over_h2=-v / h ** 2,
                                       stage_sum_over_h2=sum(L[t] for t in range(a, b)) / h ** 2,
                                       argmin_om=[float(q) for q in z[1:]], argmin_da_over_h=float(z[0] / h)))
        if N in exactN:
            ex = []
            j = kk["frac"][0] if kk["frac"] else min(range(s - 2, s + 3), key=lambda t: abs(kk["sig"][t]))
            for K in range(0, 5):
                val, om, E = window_exact_flip(toy, kk, P, s - K, s + K + 1, j)
                row = dict(K=K, flip_stage=int(j - s), flip_om=float(om), flip_change_over_h2=float(val / E["h"] ** 2),
                           flip_change_negative=bool(val < 0))
                if K <= 2:
                    vmin, _ = window_value(toy, E, P, s - K, s + K + 1, exact=True)
                    row["exact_window_min_over_h2"] = float(vmin / E["h"] ** 2)
                ex.append(row)
            rec["exact"] = ex
        # fixed-entry window [0, b) (x_0 is fixed, so no entry freedom): smallest number of stages after
        # the fractional stage j for which moving u_j to its farther bound no longer lowers J_W
        # (prediction for P = -k: b - 1 - j >= k / h, i.e. a fixed duration k)
        if kk["frac"]:
            j = kk["frac"][0]
            om = (1.0 if kk["u"][j] < 0 else -1.0) - kk["u"][j]
            Lmin = None
            for b in range(j + 1, N + 1):
                if fixed_entry_change(toy, kk, P, b, j, om) >= 0:
                    Lmin = b - 1 - j
                    break
            rec["fixed_entry_min_post_stages"] = Lmin
            rec["fixed_entry_min_post_duration"] = None if Lmin is None else Lmin * h
            rec["fixed_entry_prediction_stages"] = k / h
        rec["time"] = time.time() - t0
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    dump("plus", out)


# ------------------------------------------------------------------------------------------ zero
def part_zero(exactN=(1000, 4000, 8000)):
    toy = TOYZERO
    tau = tau_of(toy)["tau"]
    P_, _ = kink_down(tau, 0.3)
    out = []
    for N in (1000, 2000, 4000, 8000, 16000):
        t0 = time.time()
        kk = kkt(toy, N)
        D = float_data(toy, kk)
        h, s = kk["h"], kk["s"]
        P = fam_fun(toy, N, P_)
        L = stage_losses(toy, D, P, stages=range(1, N))
        fail = {int(t - s): v / h ** 3 for t, v in L.items() if v > 1e-20}
        P0 = fam_const(N, 0.0)
        L0 = stage_losses(toy, D, P0, stages=range(1, N))
        rec = dict(N=N, s=s, frac=kk["frac"], u_frac=[float(kk["u"][i]) for i in kk["frac"]],
                   sig_over_h=[float(v) for v in kk["sig"][s - 2:s + 3] / h],
                   P_next_over_h=float(P[s + 1] / h), failing_loss_over_h3=fail,
                   terminal_loss=terminal_loss(toy, D, P),
                   affine_family=dict(max_stage_loss=max(L0.values()), terminal_loss=terminal_loss(toy, D, P0)),
                   windows=[])
        for K in range(0, 4):
            a, b = s - K, s + K + 1
            v, z = window_value(toy, D, P, a, b)
            rec["windows"].append(dict(K=K, deficit_over_h3=-v / h ** 3))
        if N in exactN:
            E = exact_kkt_traj(toy, N, kk["u"])
            ex = []
            for K in range(0, 3):
                vmin, _ = window_value(toy, E, P, s - K, s + K + 1, exact=True)
                ex.append(dict(K=K, exact_window_min=float(vmin), exact_window_min_over_h3=float(vmin / E["h"] ** 3)))
            rec["exact"] = ex
        rec["time"] = time.time() - t0
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    dump("zero", out)


# ------------------------------------------------------------------------------------------ rmax
def part_rmax():
    out = []
    for k in (0.5, 0.2, 0.1, 0.05):
        toy = Toy(k=k, a2=-1.0, phi1=1.0)
        sw = tau_of(toy)
        for N in (500, 1000, 2000, 4000, 8000, 16000, 32000):
            t0 = time.time()
            kk = kkt(toy, N)
            h, s = kk["h"], kk["s"]
            P, brk = fam_rmax(toy, kk, eps=0.0)
            eta = {Kp: (float(P[s + Kp] + k) if not np.isnan(P[s + Kp]) else None) for Kp in (1, 4, 16, 64, 256) if s + Kp <= N}
            rec = dict(k=k, N=N, s=s, frac=kk["frac"], break_stage=None if brk is None else int(brk - s), eta_hat=eta)
            # leading-order log law for eta at s + K': 1 / (1 / eta_L + (Delta / (2 gamma)) log(1 / (K' h)))
            rec["eta_law"] = {Kp: 1.0 / (1.0 / sw["eta_L"] + (1.0 / sw["gamma"]) * np.log(1.0 / (Kp * h))) for Kp in (1, 4, 16, 64, 256)}
            if brk is None:
                D = float_data(toy, kk)
                L = stage_losses(toy, D, P)
                rec["exact_everywhere_float"] = dict(max_stage_loss=max(L.values()), terminal_loss=terminal_loss(toy, D, P))
            rec["time"] = time.time() - t0
            print(json.dumps(rec, default=float), flush=True)
            out.append(rec)
    dump("rmax", out)


# ------------------------------------------------------------------------------------------ scip
def part_scip(Ns=(50, 100, 150, 200), tlim=900):
    from pyscipopt import Model, quicksum
    toy = TOYPLUS
    out = []
    for N in Ns:
        kk = kkt(toy, N)
        h = toy.T / N
        a = toy.a_of(N)
        m = Model()
        m.hideOutput()
        m.setParam("limits/time", tlim)
        m.setParam("limits/gap", 0.0)
        m.setParam("limits/absgap", 1e-12)
        m.setParam("numerics/feastol", 1e-9)
        m.setParam("numerics/dualfeastol", 1e-9)
        m.setParam("parallel/maxnthreads", 1)
        u = [m.addVar(lb=-1, ub=1, name=f"u{t}") for t in range(N)]
        x = [m.addVar(lb=-toy.R, ub=toy.R, name=f"x{t}") for t in range(N + 1)]
        m.addCons(x[0] == toy.x0)
        for t in range(N):
            m.addCons(x[t + 1] == x[t] + h * u[t])
        z = m.addVar(lb=None, name="obj")
        m.addCons(z >= quicksum(h * ((x[t] - a[t]) * (x[t] - a[t]) / 2 + toy.k * x[t] * u[t]) for t in range(N))
                  + toy.phi1 * x[N] + toy.phi2 * x[N] * x[N] / 2)
        m.setObjective(z, "minimize")
        t0 = time.time()
        m.optimize()
        rec = dict(N=N, frac=kk["frac"], J_kkt=kk["J"], status=m.getStatus(), primal=m.getPrimalbound(),
                   dual=m.getDualbound(), time=time.time() - t0)
        # re-evaluate SCIP's controls exactly on the dynamics (its states satisfy the rows only to feastol)
        us = np.clip(np.array([m.getVal(v) for v in u]), -1.0, 1.0)
        _, Js = simulate(toy, N, us)
        rec["J_scip_controls_resimulated"] = Js
        rec["max_control_diff_to_kkt"] = float(np.max(np.abs(us - kk["u"])))
        if kk["frac"]:
            j = kk["frac"][0]
            om = max(1 - kk["u"][j], 1 + kk["u"][j])
            rec["stage_loss_pred"] = 0.5 * toy.k * om * om * h * h
            D = float_data(toy, kk)
            P = fam_const(N, -toy.k)
            s = kk["s"]
            v, _ = window_value(toy, D, P, s - 2, s + 3)
            rec["window_K2_bound"] = kk["J"] + v
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    dump("scip", out)


if __name__ == "__main__":
    parts = dict(cont=part_cont, verifier=part_verifier, plus=part_plus, zero=part_zero, rmax=part_rmax, scip=part_scip)
    for p in sys.argv[1:]:
        print(f"==== {p}", flush=True)
        parts[p]()
