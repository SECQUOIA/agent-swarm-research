"""Independent continuous checks for the revision of extension-n2.md.
Parts: blowup (B, B2), cpre (C, A), localF (A, C), lyapW5 (A).  Plain-time integration (Radau and LSODA),
own model derivation (c_common.py).  Usage: python3 c_cont.py [part ...]"""
import json
import sys

import numpy as np
from scipy.integrate import solve_ivp

from c_common import setup, T

A = np.array([[0.0, 1.0], [0.0, 0.0]])
b = np.array([0.0, 1.0])
I2 = np.eye(2)
DELTA = 2.0


def data(name):
    d = setup(name)
    P = d["P"]
    d["w"] = -np.array([P["k1"], P["k2"]])
    d["Hxx"] = np.diag([P["q"], -P["c"]])
    d["PhiXX"] = np.diag([0.0, P["rho"]])
    return d


def sig(d, tt):
    return d["f"]["siga"](tt) if tt < d["tau"] else d["f"]["sigb"](tt)


def rhs_factory(d, eps, singular_until=None, side="b"):
    w, H = d["w"], d["Hxx"]
    sfun = d["f"]["sigb"] if side == "b" else d["f"]["siga"]

    def f(tt, y):
        P = y.reshape(2, 2)
        lin = -(A.T @ P + P @ A + H) + 2 * eps * I2
        if singular_until is not None and tt - d["tau"] > singular_until:
            return lin.ravel()
        be = P @ b - w
        return (lin + DELTA / (2 * abs(sfun(tt))) * np.outer(be, be)).ravel()
    return f


def blowup_after(d, eps, delta0=None, method="Radau", big=1e8):
    f = rhs_factory(d, eps, delta0)
    ev = lambda tt, y: big - np.abs(y).max()
    ev.terminal = True
    P0 = d["PhiXX"] - 2 * eps * I2
    r = solve_ivp(f, (T, d["tau"] + 1e-15), P0.ravel(), method=method, rtol=1e-12, atol=1e-12, events=ev)
    if r.status == 1:
        return float(r.t_events[0][0] - d["tau"])
    return None


def blowup_after_log(d, eps, delta0=None, big=1e8):
    """Cross-check in log time lam = log(t - tau) below s = 0.05."""
    f = rhs_factory(d, eps, delta0)
    P0 = d["PhiXX"] - 2 * eps * I2
    r1 = solve_ivp(f, (T, d["tau"] + 0.05), P0.ravel(), method="DOP853", rtol=1e-12, atol=1e-13)
    g = lambda lam, y: np.exp(lam) * f(d["tau"] + np.exp(lam), y)
    ev = lambda lam, y: big - np.abs(y).max()
    ev.terminal = True
    r2 = solve_ivp(g, (np.log(0.05), np.log(1e-14)), r1.y[:, -1], method="DOP853", rtol=1e-12, atol=1e-13, events=ev)
    return float(np.exp(r2.t_events[0][0])) if r2.status == 1 else None


def lyap(d, eps, t0):
    f = lambda tt, y: (-(A.T @ y.reshape(2, 2) + y.reshape(2, 2) @ A + d["Hxx"]) + 2 * eps * I2).ravel()
    return solve_ivp(f, (T, t0), (d["PhiXX"] - 2 * eps * I2).ravel(), method="DOP853", rtol=1e-13, atol=1e-14,
                     dense_output=True).sol


def part_blowup():
    out = []
    for name in ("B", "B2"):
        d = data(name)
        Q = lyap(d, 0.0, d["tau"])
        etaL = float(b @ (Q(d["tau"]).reshape(2, 2) @ b - d["w"]))
        kap = DELTA / (2 * abs(d["sdot"]))
        for eps in (0.0, 0.02):
            for d0 in ((None, 0.2, 0.1) if name == "B" else (None,)):
                vals = {m: blowup_after(d, eps, d0, method=m) for m in ("Radau", "LSODA")}
                vals["Radau_big1e10"] = blowup_after(d, eps, d0, big=1e10)
                vals["log_DOP853"] = blowup_after_log(d, eps, d0)
                rec = dict(ex=name, eps=eps, delta0=d0, etaL=etaL, kappa=kap, **vals)
                if d0 is not None:
                    rec["pred"] = d0 * np.exp(-1 / (kap * abs(etaL)))
                    rec["pred_over_sb"] = rec["pred"] / vals["Radau"]
                print(rec, flush=True)
                out.append(rec)
    return out


def part_cpre():
    out = []
    for name in ("C", "A"):
        d = data(name)
        for eps in (0.0, 0.02):
            Q = lyap(d, eps, d["tau"])
            Qp = Q(d["tau"]).reshape(2, 2)
            be = Qp @ b - d["w"]
            eta = float(b @ be)
            Pmax = Qp - np.outer(be, be) / eta
            f = rhs_factory(d, eps, side="a")
            ev = lambda tt, y: 1e8 - np.abs(y).max()
            ev.terminal = True
            for s0 in (1e-10, 1e-7):
                for method in ("Radau", "DOP853"):
                    r = solve_ivp(f, (d["tau"] - s0, 0.0), Pmax.ravel(), method=method, rtol=1e-12, atol=1e-12,
                                  events=ev)
                    rec = dict(ex=name, eps=eps, eta=eta, s0=s0, method=method, blow=r.status == 1)
                    if r.status == 1:
                        Pe = r.y_events[0][0].reshape(2, 2)
                        rec["t_blow"] = float(r.t_events[0][0])
                        rec["eig"] = np.linalg.eigvalsh(0.5 * (Pe + Pe.T)).tolist()
                    else:
                        rec["P0"] = r.y[:, -1].tolist()
                    print(rec, flush=True)
                    out.append(rec)
    return out


def xstar(d, tt):
    f = d["f"]
    return np.array([f["x1a"](tt), f["x2a"](tt)]) if tt < d["tau"] else np.array([f["x1b"](tt), f["x2b"](tt)])


def box(d, tt):
    x20 = d["P"]["x20"]
    return np.array([x20 * tt - tt * tt / 2, x20 - tt]), np.array([x20 * tt + tt * tt / 2, x20 + tt])


def reach_x1_range(d, tt, v):
    """True reachable set at time tt: for final x2 = v, the range of x1 (tent paths)."""
    x20 = d["P"]["x20"]
    th1 = (v - x20 + tt) / 2  # up then down
    x1max = x20 * tt + th1 ** 2 / 2 + th1 * (tt - th1) - (tt - th1) ** 2 / 2
    th2 = (x20 - v + tt) / 2  # down then up
    x1min = x20 * tt - th2 ** 2 / 2 - th2 * (tt - th2) + (tt - th2) ** 2 / 2
    return x1min, x1max


def rmin(d, tt, be, eps, where="box"):
    """min over x in the domain and u in U of r = sig om + om be.dx + eps|dx|^2 (quadratic S with M = 2 eps I)."""
    s = sig(d, tt)
    om = (-1.0 - 1.0) if tt < d["tau"] else (1.0 - (-1.0))  # other vertex minus u*
    xs = xstar(d, tt)
    if where == "box":
        lo, hi = box(d, tt)
        dd = np.clip(-om * be / (2 * eps), lo - xs, hi - xs)
        return min(0.0, s * om + om * be @ dd + eps * dd @ dd)
    x20 = d["P"]["x20"]
    v = np.linspace(x20 - tt, x20 + tt, 20001)
    lo1, hi1 = reach_x1_range(d, tt, v)
    d2 = v - xs[1]
    d1 = np.clip(-om * be[0] / (2 * eps), lo1 - xs[0], hi1 - xs[0])
    val = s * om + om * (be[0] * d1 + be[1] * d2) + eps * (d1 ** 2 + d2 ** 2)
    return min(0.0, float(val.min()))


def part_localF():
    out = []
    for name in ("A", "C"):
        d = data(name)
        for eps in (0.02, 0.01):
            Q = lyap(d, eps, d["tau"])
            tt = np.linspace(d["tau"] + 0.02, T, 2001)
            h3, fb, nb = [], [], []
            for x in tt:
                be = Q(x).reshape(2, 2) @ b - d["w"]
                nb.append(np.linalg.norm(be))
                h3.append(abs(sig(d, x)) - DELTA * (be @ be) / (2 * 2 * eps))
                fb.append(rmin(d, x, be, eps, "box"))
            fr = []
            ts = tt[::40]
            for x in ts:
                be = Q(x).reshape(2, 2) @ b - d["w"]
                fr.append(rmin(d, x, be, eps, "reach"))
            h3, fb, fr = map(np.array, (h3, fb, fr))
            rec = dict(ex=name, eps=eps, H3min=float(h3.min()), H3fail_frac=float(np.mean(h3 <= 0)),
                       boxmin=float(fb.min()), box_fail_frac=float(np.mean(fb < 0)),
                       reachmin=float(fr.min()), reach_fail_frac=float(np.mean(fr < 0)), reach_n=len(ts),
                       beta_range=[float(min(nb)), float(max(nb))])
            print(rec, flush=True)
            out.append(rec)
    return out


def part_lyapW5():
    d = data("A")
    eps = 0.02
    Q = lyap(d, eps, 0.0)
    tt = np.linspace(0, T, 4001)[1:]
    tt = tt[np.abs(tt - d["tau"]) > 1e-9]
    w5, fb, nb = [], [], []
    for x in tt:
        be = Q(x).reshape(2, 2) @ b - d["w"]
        nb.append(np.linalg.norm(be))
        w5.append(abs(sig(d, x)) - DELTA * (be @ be) / (2 * 2 * eps))
        fb.append(rmin(d, x, be, eps, "box"))
    w5, fb, nb = map(np.array, (w5, fb, nb))
    last = tt > d["tau"]
    # true reachable set on a coarser grid
    ts = tt[::20]
    fr = np.array([rmin(d, x, Q(x).reshape(2, 2) @ b - d["w"], eps, "reach") for x in ts])
    rec = dict(tau=d["tau"], W5_fail=[float(tt[w5 <= 0].min()), float(tt[w5 <= 0].max())],
               W5_contig=bool(np.all(w5[(tt >= tt[w5 <= 0].min())] <= 0)),
               beta_last=[float(nb[last].min()), float(nb[last].max())],
               box_fail=[float(tt[fb < 0].min()), float(tt[fb < 0].max())],
               box_contig=bool(np.all(fb[tt >= tt[fb < 0].min()] < 0)),
               box_fail_before_tau=float(d["tau"] - tt[fb < 0].min()),
               reach_fail=[float(ts[fr < 0].min()), float(ts[fr < 0].max())] if np.any(fr < 0) else None,
               reach_fail_before_tau=float(d["tau"] - ts[fr < 0].min()) if np.any(fr < 0) else None,
               reach_contig=bool(np.all(fr[ts >= ts[fr < 0].min()] < 0)) if np.any(fr < 0) else None)
    print(rec, flush=True)
    return rec


PARTS = dict(blowup=part_blowup, cpre=part_cpre, localF=part_localF, lyapW5=part_lyapW5)
if __name__ == "__main__":
    for nm in sys.argv[1:] or list(PARTS):
        print("==", nm, flush=True)
        res = PARTS[nm]()
        json.dump(res, open("logs/c_cont_%s.json" % nm, "w"), indent=1, default=float)
