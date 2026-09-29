"""Closing audit (b), item 2: binary least squares, Proposition 6.3 and the Section 6 numbers
(shifted-relaxation gaps at beta = 2, N = 200), plus per-instance shift thresholds.

Own code.  The generator mirrors the note's documented generator (core.instance / the scout's
bls.py): rng = default_rng(seed); H = N(0,1)^{M x N}; A = sqrt(rho/N) H; x* = random signs;
y = A x* + N(0, I_M); w = y - A x*.
The box QP  min_{x in [-1,1]^N} ||y - A x||^2 + d sum(1 - x_i^2)  is solved by an exact
active-set method (primal feasible, Newton steps on the free set, multiplier release), not by BVLS;
the reported bound is the Frank-Wolfe (linearization) lower bound at the final point, which is
valid for any feasible point because the objective is convex for d <= lambda_min(A'A).
"""
import os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np


def instance(N, M, rho, seed):
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N))
    A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    y = A @ xs + rng.standard_normal(M)
    return H, A, xs, y, y - A @ xs


def box_qp(Q, c, x0=None, iters=500):
    """min 0.5 x'Qx - c'x over [-1,1]^N, Q PSD. Primal active-set with exact solves on the free set."""
    N = len(c)
    x = np.zeros(N) if x0 is None else np.clip(x0, -1, 1)
    # start from projected gradient iterations to get a sensible active set
    Lc = np.linalg.eigvalsh(Q)[-1]
    for _ in range(3000):
        x = np.clip(x - (Q @ x - c) / Lc, -1, 1)
    for it in range(iters):
        g = Q @ x - c
        # KKT: free coords g = 0; x = 1 -> g <= 0; x = -1 -> g >= 0
        atU = x >= 1 - 1e-12; atL = x <= -1 + 1e-12
        release = (atU & (g > 1e-12)) | (atL & (g < -1e-12))
        free = ~(atU | atL) | release
        # Newton step on the free set with the others fixed
        Fi = np.where(free)[0]; Bi = np.where(~free)[0]
        if len(Fi) == 0:
            break
        rhs = c[Fi] - Q[np.ix_(Fi, Bi)] @ x[Bi]
        xf = np.linalg.lstsq(Q[np.ix_(Fi, Fi)], rhs, rcond=None)[0]
        dstep = np.zeros(N); dstep[Fi] = xf - x[Fi]
        # longest feasible step along dstep
        with np.errstate(divide="ignore", invalid="ignore"):
            tU = np.where(dstep > 0, (1 - x) / dstep, np.inf)
            tL = np.where(dstep < 0, (-1 - x) / dstep, np.inf)
        t = min(1.0, tU.min(), tL.min())
        x = np.clip(x + t * dstep, -1, 1)
        if t >= 1.0:
            g = Q @ x - c
            atU = x >= 1 - 1e-12; atL = x <= -1 + 1e-12
            bad = (atU & (g > 1e-10)) | (atL & (g < -1e-10)) | (~(atU | atL) & (np.abs(g) > 1e-8))
            if not bad.any():
                break
    return x


def shifted_value(A, y, d):
    """Returns (upper value at the computed point, certified FW lower bound)."""
    N = A.shape[1]
    G = A.T @ A
    Q = 2 * (G - d * np.eye(N)); c = 2 * A.T @ y
    x = box_qp(Q, c)
    val = float(np.sum((y - A @ x) ** 2) + d * np.sum(1 - x ** 2))
    g = Q @ x - c
    lb = val - float(np.sum(g * x + np.abs(g)))   # min over the box of the linearization
    return val, lb, x


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "F"
    if part == "F":
        N, M = 200, 400
        print("beta = 2, N = 200, seeds 0-3: relative gaps (W - bound)/W; W = f(x*); OPT = W certified by "
              "lambda_min(A'A + diag zeta) > 0 (Prop. 6.1)")
        for rho in (30.0, 60.0, 130.0, 300.0, 600.0):
            rows = []
            for s in range(4):
                H, A, xs, y, w = instance(N, M, rho, s)
                W = float(w @ w)
                G = A.T @ A
                lmin = np.linalg.eigvalsh(G)[0]
                zeta = xs * (A.T @ w)
                sdp = np.linalg.eigvalsh(G + np.diag(zeta))[0]
                v0, lb0, _ = shifted_value(A, y, 0.0)
                v99, lb99, x99 = shifted_value(A, y, 0.99 * lmin)
                v1, lb1, x1 = shifted_value(A, y, lmin)
                rows.append(dict(s=s, sdp=sdp, box=(W - lb0) / W, box_up=(W - v0) / W, g99=(W - lb99) / W,
                                 g99u=(W - v99) / W, g1=(W - lb1) / W, g1u=(W - v1) / W,
                                 kkt=bool(zeta.min() >= -lmin), kkt99=bool(zeta.min() >= -0.99 * lmin),
                                 xstar99=float(np.max(np.abs(x99 - xs)))))
            print("rho=%5.0f  SDP-min-eig>0: %d/4  box gap (median) %.4f" %
                  (rho, sum(r["sdp"] > 0 for r in rows), np.median([r["box"] for r in rows])))
            for r in rows:
                print("   seed %d: shifted gap d=0.99lmin: [%.3e, %.3e] (lower..upper bracket), d=lmin: [%.3e, %.3e];"
                      " min zeta >= -lmin: %s, >= -0.99 lmin: %s; max|x-x*| (d=.99) %.2e"
                      % (r["s"], r["g99u"], r["g99"], r["g1u"], r["g1"], r["kkt"], r["kkt99"], r["xstar99"]))
            print("   median gap d=0.99 lmin: %.3e (max %.3e); median gap d=lmin: %.3e (max %.3e); exact (d=lmin) %d/4"
                  % (np.median([r["g99"] for r in rows]), max(r["g99"] for r in rows),
                     np.median([r["g1"] for r in rows]), max(r["g1"] for r in rows), sum(r["kkt"] for r in rows)))
    if part == "T":
        # per-instance shift thresholds: x* minimizes f_d (d = lambda_min) iff zeta_i >= -lambda_min for all i;
        # zeta = sqrt(rho/N) x* o H'w, lambda_min(A'A) = (rho/N) lambda_min(H'H), w independent of rho:
        # rho_shift = N * (max_i(-x*_i h_i'w))_+^2 / lambda_min(H'H)^2
        for beta in (2, 4):
            for N in (100, 400):
                M = beta * N
                th = []
                for s in range(20):
                    H, A, xs, y, w = instance(N, M, 1.0, s)
                    lm = np.linalg.eigvalsh(H.T @ H)[0]
                    th.append(N * max(0.0, np.max(-xs * (H.T @ w))) ** 2 / lm ** 2 / np.log(N))
                print("beta=%d N=%4d: median rho_shift/log N = %.1f over 20 seeds (range %.1f-%.1f); asymptotic "
                      "2 beta/(sqrt beta - 1)^4 = %.1f" % (beta, N, np.median(th), min(th), max(th),
                                                            2 * beta / (np.sqrt(beta) - 1) ** 4))
    if part == "K":
        # Theorem 4.1: counting at rho = Theta(N).  Display (N+1) sum_{j<=K} C(N,j) versus the Summary's
        # (N+1) exp(c log rho), c = N/(4(2 beta - 1) rho), versus the refined count
        # 1 + 2 sum_{d<N} sum_{j<=K-1} C(d,j) (branched nodes have |Wr| <= K-1).
        from math import lgamma, log, exp, ceil
        lC = lambda n, k: lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
        N = 10 ** 6
        for beta, rho in ((1, N / 6), (1, N / 10), (1, N / 100), (1, N / 1000)):
            c = N / (4 * (2 * beta - 1) * rho)
            kap = 1 - np.sqrt(2 * log(4 * (2 * beta - 1) * rho) / (rho * beta)) - 1 / np.sqrt(rho * beta)
            K = ceil(c / kap)
            disp = log(N + 1) + np.logaddexp.reduce([lC(N, j) for j in range(K + 1)])
            summ = log(N + 1) + c * log(rho)
            # refined: sum_{d<N} C(d, j) = C(N, j+1)
            ref = log(1 + 2 * sum(exp(lC(N, j + 1) - lC(N, K)) for j in range(K))) + lC(N, K) if K >= 1 else log(2 * N + 1)
            print("beta=%d rho=N/%d: c=%.3f kappa_rho=%.4f K=%d  log(display)=%.2f  log(Summary form, o(1)=0)=%.2f"
                  "  log(refined count)=%.2f" % (beta, round(N / rho), c, kap, K, disp, summ, ref))
    if part == "G":
        # F9: proved exponent K log(eN/K), K = N/(4(2b-1) kappa_rho rho), against the asymptotic
        # expression (N/(4(2b-1) rho)) log rho, at N = 1e6; also the prefactor ratio 1/kappa_rho alone.
        N = 1e6
        for beta in (1.0, 2.0):
            for c in (2.0, 4.0, 8.0, 16.0):
                rho = c * np.log(N) / beta
                kap = 1 - np.sqrt(2 * np.log(4 * (2 * beta - 1) * rho) / (rho * beta)) - 1 / np.sqrt(rho * beta)
                K = N / (4 * (2 * beta - 1) * kap * rho)
                ratio = K * np.log(np.e * N / K) / (N / (4 * (2 * beta - 1) * rho) * np.log(rho))
                print("beta=%.0f rho beta=%2.0f log N: kappa_rho=%.3f, 1/kappa=%.2f, K log(eN/K) / [(N/(4(2b-1)rho)) log rho] = %.2f"
                      % (beta, c, kap, 1 / kap, ratio))
