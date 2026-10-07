"""Revision checks for singular-arcs.md, Sections 3-4 (example E2, lqsing.py),
written after review round 1 (findings F4, F5).

1. F5(a,b,e,f): values read back from the logged runs (junction-layer
   distances, fractional-stage counts, window starts, B1 failures, B2 break
   times).
2. F5(c): k1 = +1/2, the KKT point with the active set of the k1 = 0 optimum
   (bang then free), solved exactly (lqsing.exact_kkt, KKT signs checked in
   rationals): (J_smooth - J*)/h, and the chattering values relative to it.
3. F5(d): k1 = +1/2 multistart with a new seed and more starts (L-BFGS-B),
   best value, exact KKT check of its active set.
4. F5(g): family B2 at k1 = 0: norm and components of beta_t on fractional
   stages, in units of h and sqrt(h), and where the largest |beta_t| sits.
5. F4: k1 = +1/2 (b^T w = -1/2), an isolated fractional stage made exact by
   an O(1) drop of a bounded Hessian: P_{t+1} = e1 e1^T, P_t from the
   maximal recursion; exact rational test of Lemma 10 of extension-n2.md;
   the next stage back then fails.
Usage: python3 revision_e2.py
"""
import json
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import minimize

import lqsing as L
import lqsing_run as RUN

T1 = 1.1982904373
JSTAR = {Fr(-1, 2): 0.3989691259, Fr(0): 0.1489691259, Fr(1, 2): -0.1010308741}


def read_logs():
    print("== 1. values read back from the logs")
    for k1, f in (("-1/2", "logs/lqsing_k1_m1_2.jsonl"), ("0", "logs/lqsing_k1_0.jsonl"),
                  ("1/2", "logs/lqsing_k1_p1_2.jsonl")):
        for line in open(f):
            r = json.loads(line)
            ft = r["first_free_time"]
            print("k1=%s N=%d J=%.12f n_free=%d first_free_time=%s t1-first=%s A_window_start=%s "
                  "B1 fails (bang/free)=%d/%d B2_broke_time=%s"
                  % (k1, r["N"], r["J_exact"], r["n_free"], ft,
                     ("%.4f" % (T1 - ft)) if ft is not None else None,
                     r["A"]["bang_fail_times"][0] if r["A"]["bang_fail_times"] else None,
                     r["B1"]["n_fail_bang"], r["B1"]["n_fail_free"], r.get("B2_broke_time")))


def status_of(u):
    return [(-1 if v <= -1 + 1e-12 else (1 if v >= 1 - 1e-12 else 0)) for v in u]


def smooth_vs_chatter():
    print("== 2./3. k1 = +1/2: KKT point with the continuous structure, and multistart")
    k1 = Fr(1, 2)
    for N in (50, 100, 200, 400):
        h = 3.0 / N
        d0 = L.data(Fr(0), N)
        H0, g0, _ = L.float_qp(d0)
        st0 = status_of(L.solve_box_qp(H0, g0))
        d = L.data(k1, N)
        sol = L.exact_kkt(d, st0)
        Js = float(sol["J"])
        uf = np.array([float(x) for x, s in zip(sol["u"], st0) if s == 0])
        dev = np.max(np.abs(uf[1:-1] - 0.5 * (uf[:-2] + uf[2:])))
        print("N=%d KKT point with the continuous structure: arc controls in [%.4f, %.4f], "
              "max deviation from the neighbour average %.2e" % (N, uf.min(), uf.max(), dev))
        # multistart: new seed, 60 random starts plus structured ones
        Hq, gq, c0 = L.float_qp(d)
        f = lambda u: (0.5 * u @ Hq @ u + gq @ u + c0, Hq @ u + gq)
        rng = np.random.default_rng(12345)
        starts = [np.array([float(v) for v in sol["u"]]), np.where(np.arange(N) % 2 == 0, 1.0, -1.0),
                  np.where(np.arange(N) % 2 == 0, -1.0, 1.0), np.zeros(N)]
        starts += [rng.uniform(-1, 1, N) for _ in range(60)]
        best = None
        vals = []
        for s0 in starts:
            r = minimize(f, s0, jac=True, method="L-BFGS-B", bounds=[(-1, 1)] * N,
                         options=dict(maxiter=20000, ftol=1e-15, gtol=1e-13))
            vals.append(r.fun)
            if best is None or r.fun < best.fun:
                best = r
        u = np.clip(best.x, -1, 1)
        st = status_of(u)
        solc = L.exact_kkt(d, st)
        Jc = float(solc["J"])
        pred = 0.25 * h  # times int_arc (1 - u_s^2), evaluated below
        print("N=%d smooth KKT: kkt_ok=%s n_free=%d J=%.10f (J-J*)/h=%+.4f | multistart best: kkt_ok=%s "
              "n_free=%d J=%.10f (J-J*)/h=%+.4f (J-J_smooth)/h=%+.4f | distinct local values (rounded 1e-9)=%d"
              % (N, sol["kkt_ok"], st0.count(0), Js, (Js - JSTAR[k1]) / h, solc["kkt_ok"], st.count(0), Jc,
                 (Jc - JSTAR[k1]) / h, (Jc - Js) / h, len(set(np.round(vals, 9)))), flush=True)


def b2_beta():
    print("== 4. B2 at k1 = 0: beta_t on fractional stages")
    for N in (200, 800):
        d = L.data(Fr(0), N)
        Hq, gq, _ = L.float_qp(d)
        st = status_of(L.solve_box_qp(Hq, gq))
        sol = L.exact_kkt(d, st)
        P, broke = RUN.fam_B2(d, sol, st)
        h = float(d["h"])
        rows = []
        for t in range(N):
            if st[t] == 0:
                Kt, beta, kap = L.stage_terms(d, P[t + 1], P[t])
                b = np.array([float(beta[0]), float(beta[1])])
                rows.append((t, np.linalg.norm(b), abs(b[0]), abs(b[1]), float(kap)))
        a = np.array(rows)
        tmax = int(a[np.argmax(a[:, 1]), 0])
        print("N=%d broke=%s n_frac=%d median |beta|/h=%.3f  median |beta|/sqrt(h)=%.3f  median |beta_1|/sqrt(h)=%.3f "
              "median |beta_2|/sqrt(h)=%.3f  median kappa/h=%.3f  max |beta|=%.3f at t=%.4f (last stage t=%.4f); "
              "90%% quantile |beta|/h=%.3f"
              % (N, broke, len(a), np.median(a[:, 1]) / h, np.median(a[:, 1]) / np.sqrt(h),
                 np.median(a[:, 2]) / np.sqrt(h), np.median(a[:, 3]) / np.sqrt(h), np.median(a[:, 4]) / h,
                 a[:, 1].max(), tmax * h, (N - 1) * h, np.quantile(a[:, 1], 0.9) / h), flush=True)


def isolated_exact_stage():
    print("== 5. F4: isolated exact fractional stage with b^T w < 0 (k1 = +1/2) by an O(1) Hessian drop")
    k1 = Fr(1, 2)
    N = 100
    d0 = L.data(Fr(0), N)
    H0, g0, _ = L.float_qp(d0)
    st = status_of(L.solve_box_qp(H0, g0))
    d = L.data(k1, N)
    sol = L.exact_kkt(d, st)
    frac = [t for t in range(N) if st[t] == 0]
    t = frac[len(frac) // 2]
    h, Fx = d["h"], d["Fx"]
    Pn = ((Fr(1), Fr(0)), (Fr(0), Fr(0)))            # P_{t+1} = e1 e1^T, |P| = 1
    Kt0, beta, kap = L.stage_terms(d, Pn, ((Fr(0), Fr(0)), (Fr(0), Fr(0))))
    # maximal recursion: P_t = h I + Fx^T Pn Fx - beta beta^T / kappa
    Pt = L.add(L.add(L.scal(h, L.Q), L.mm(L.tr(Fx), L.mm(Pn, Fx))), L.scal(1 / kap, L.outer(beta, beta)), -1)
    Kt, beta, kap = L.stage_terms(d, Pn, Pt)
    ok, m = L.stage_exact(d, Kt, beta, kap, sol["sigma"][t], st[t])
    ev = np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in Kt]))
    evP = np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in Pt]))
    print("KKT point kkt_ok=%s; stage t=%d (time %.3f) fractional; P_{t+1}=e1e1^T; P_t eigenvalues %s; "
          "stage exact (exact rational Lemma 10 test): %s; kappa_t=%s; |beta_t|=%.3f; K_t eigenvalues %s (h=%.3f)"
          % (sol["kkt_ok"], t, float(t * h), np.round(evP, 4).tolist(), ok, kap,
             float(np.hypot(float(beta[0]), float(beta[1]))), np.round(ev, 4).tolist(), float(h)))
    # the stage before, with the same P_t as its P_{t+1}: kappa = e1^T P_t e1
    Kt2, beta2, kap2 = L.stage_terms(d, Pt, Pt)
    print("stage t-1 (fractional: %s) has kappa_{t-1} = b^T P_t b = %.4f < 0, so it fails for every P_{t-1} (Lemma 3.1(a))"
          % (st[t - 1] == 0, float(kap2)))


if __name__ == "__main__":
    read_logs()
    smooth_vs_chatter()
    b2_beta()
    isolated_exact_stage()
