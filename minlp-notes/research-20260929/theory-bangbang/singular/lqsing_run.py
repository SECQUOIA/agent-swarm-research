"""Driver for example E2 (lqsing.py): discrete optimum (float QP, then exact
rational KKT point for the float active set), and three calibration families:

  A   affine (costate) family, P_t = 0;
  B1  constant tangential Hessian P = [[-k1, -k2], [-k2, 1/4 - delta]]
      (continuous tangential calibration transferred; delta = 1/10);
  B2  discrete maximal recursion (Lemma 10 of extension-n2.md) with margin
      eps, from P_N = F - 2 eps I, computed in floats and rounded to dyadic
      rationals; exactness then checked exactly.

For each family: number of failing stages (exact test, Lemma 10), where they
are (bang / singular-type stages, time range), and the float loss sum.
Usage: python3 lqsing_run.py k1 N [N ...]      (k1 as a fraction, e.g. -1/2)
"""
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import lqsing as L


def fam_B1(d, delta=Fr(1, 10)):
    P = ((-d["k1"], -L.K2), (-L.K2, Fr(1, 4) - delta))
    return [P] * (d["N"] + 1)


def fam_A(d):
    Z = ((Fr(0), Fr(0)), (Fr(0), Fr(0)))
    return [Z] * (d["N"] + 1)


def fam_B2(d, sol, status, eps=0.01):
    N, h = d["N"], float(d["h"])
    Fx = np.array([[float(v) for v in r] for r in d["Fx"]])
    k = np.array([float(v) for v in d["k"]])
    Fm = np.array([[float(v) for v in r] for r in d["F"]])
    b = np.array([1.0, 0.0])
    P = [None] * (N + 1)
    P[N] = Fm - 2 * eps * np.eye(2)
    broke = None
    for t in range(N - 1, -1, -1):
        Pn = P[t + 1]
        beta = Fx.T @ Pn @ b + k
        kap = b @ Pn @ b
        if status[t] == 0:
            m = kap
        else:
            m = 2 * abs(float(sol["sigma"][t])) / (h * 2.0) + kap
        Pt = h * np.eye(2) + Fx.T @ Pn @ Fx - 2 * h * eps * np.eye(2)
        if m > 0:
            Pt = Pt - np.outer(beta, beta) / m
        else:
            broke = t
            break
        P[t] = Pt
    if broke is not None:
        return None, broke
    # round to dyadic rationals (exact floats)
    return [tuple(tuple(Fr(float(v)) for v in r) for r in Pt) for Pt in P], None


def evaluate(d, sol, status, Ps):
    N, h = d["N"], d["h"]
    fails = []
    loss = 0.0
    minfo = []
    for t in range(N):
        Kt, beta, kap = L.stage_terms(d, Ps[t + 1], Ps[t])
        ok, m = L.stage_exact(d, Kt, beta, kap, sol["sigma"][t], status[t])
        if not ok:
            ls = L.stage_loss_float(float(h), Kt, beta, kap, sol["sigma"][t], sol["u"][t], status[t])
            fails.append((t, status[t], ls))
            loss += -ls if np.isfinite(ls) else np.inf
    # terminal: Phi - S_N = 1/2 d'(F - P_N)d (linear terms vanish since p_N = F x_N)
    term_ok = L.psd2(L.add(d["F"], Ps[N], -1))
    return fails, loss, term_ok


def multistart(d, Hq, gq, c0, nrand=20, seed=0):
    """nonconvex case: best of L-BFGS-B runs from several starts, then an
    active-set polish (free stages solved from the float KKT system)."""
    from scipy.optimize import minimize
    N = d["N"]
    f = lambda u: (0.5 * u @ Hq @ u + gq @ u + c0, Hq @ u + gq)
    dm = L.data(Fr(-1, 2), N)
    Hm, gm, cm = L.float_qp(dm)
    starts = [L.solve_box_qp(Hm, gm), np.zeros(N), np.where(np.arange(N) % 2 == 0, 1.0, -1.0)]
    rng = np.random.default_rng(seed)
    starts += [rng.uniform(-1, 1, N) for _ in range(nrand)]
    best = None
    for s0 in starts:
        r = minimize(f, s0, jac=True, method="L-BFGS-B", bounds=[(-1, 1)] * N,
                     options=dict(maxiter=20000, ftol=1e-15, gtol=1e-13))
        if best is None or r.fun < best.fun:
            best = r
    u = np.clip(best.x, -1, 1)
    u[u <= -1 + 1e-9] = -1.0
    u[u >= 1 - 1e-9] = 1.0
    return u


def main():
    k1 = Fr(sys.argv[1])
    out = []
    for N in [int(v) for v in sys.argv[2:]]:
        t0 = time.time()
        d = L.data(k1, N)
        Hq, gq, c0 = L.float_qp(d)
        ev_min = float(np.linalg.eigvalsh(Hq)[0])
        if ev_min >= 0:
            u = L.solve_box_qp(Hq, gq)
        else:
            u = multistart(d, Hq, gq, c0)
        viol = L.kkt_check_float(Hq, gq, u)
        Jf = 0.5 * u @ Hq @ u + gq @ u + c0
        status = [(-1 if ui <= -1 + 1e-12 else (1 if ui >= 1 - 1e-12 else 0)) for ui in u]
        sol = L.exact_kkt(d, status)
        tk = time.time() - t0
        nfree = sum(1 for s in status if s == 0)
        first_free = next((t for t in range(N) if status[t] == 0), None)
        rec = dict(k1=str(k1), N=N, h=str(d["h"]), Hq_min_eig=ev_min, float_kkt_viol=viol,
                   J_float=Jf, exact_kkt_ok=bool(sol["kkt_ok"]), J_exact=float(sol["J"]),
                   n_free=nfree, first_free_stage=first_free,
                   first_free_time=(float(first_free * d["h"]) if first_free is not None else None),
                   n_upper=sum(1 for s in status if s == 1), time_kkt=tk)
        # free-stage alternation diagnostics
        uf = np.array([float(x) for x in sol["u"]])
        rec["u_free_range"] = [float(uf[np.array(status) == 0].min()), float(uf[np.array(status) == 0].max())] if nfree else None
        fams = {"A": fam_A(d), "B1": fam_B1(d)}
        PB2, broke = fam_B2(d, sol, status)
        if PB2 is not None:
            fams["B2"] = PB2
        else:
            rec["B2_broke_at"] = broke
            rec["B2_broke_time"] = float(broke * d["h"])
        for name, Ps in fams.items():
            fails, loss, term_ok = evaluate(d, sol, status, Ps)
            nb = sum(1 for f in fails if f[1] != 0)
            ns = sum(1 for f in fails if f[1] == 0)
            tb = [float(f[0] * d["h"]) for f in fails if f[1] != 0]
            ts = [float(f[0] * d["h"]) for f in fails if f[1] == 0]
            rec[name] = dict(n_fail=len(fails), n_fail_bang=nb, n_fail_free=ns,
                             bang_fail_times=[min(tb), max(tb)] if tb else None,
                             free_fail_times=[min(ts), max(ts)] if ts else None,
                             loss=loss, terminal_ok=bool(term_ok),
                             exact_certificate=bool(len(fails) == 0 and term_ok and sol["kkt_ok"]))
        rec["time_total"] = time.time() - t0
        print(json.dumps(rec), flush=True)
        out.append(rec)
    return out


if __name__ == "__main__":
    main()
