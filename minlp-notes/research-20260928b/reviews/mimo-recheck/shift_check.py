"""Item (3): Proposition 6.3, the eigenvalue-shift relaxation
f_d(x) = ||y - A x||^2 + d sum_i (1 - x_i^2),  0 <= d <= lambda_min(A'A).

 (a) f_d = f on {-1,1}^N; Hessian 2(A'A - dI) is PSD; the gradient identity
     x*_i d_i f_d(x*) = -2 zeta_i - 2d (finite differences);
 (b) KKT characterisation: over many instances, the box minimiser of f_d
     (solved by CVXPY/Clarabel as a convex QP, d = lambda_min exactly, no
     factorisation) equals x* iff min_i zeta_i >= -d;
 (c) per-instance exactness thresholds in rho.  The generator draws H, x*, w
     independently of rho, so with g_i = x*_i h_i'w/||w|| and s = s_min(H):
       shift relaxation exact at x*  iff  rho >= N W max(-g)^2 / s^4   (when -g has a positive max)
       Shor SDP exact at x*          iff  rho >= lambda_max(-D; K)^2,  K = H'H/N, D = diag(x* o H'w)/sqrt N
     (Proposition 6.1 and the note's closed form).  Compared with
     2 beta log N/(sqrt beta - 1)^4 (Prop. 6.3) and 2 beta log N/(beta - 1)^2;
 (d) the note's part-F numbers (beta = 2, N = 200, 4 seeds), with exactness
     counts, at d = lambda_min.
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import cvxpy as cp
from scipy.linalg import eigh
from rc_common import make_instance, box_value


def shifted_box_min(A, y, d):
    N = A.shape[1]
    x = cp.Variable(N)
    P = A.T @ A - d * np.eye(N)
    P = (P + P.T) / 2
    ev = np.linalg.eigvalsh(P)
    P = P - min(ev[0], 0.0) * np.eye(N)          # remove -1e-13 rounding so that CVXPY accepts it
    obj = cp.quad_form(x, cp.psd_wrap(P)) - 2 * (A.T @ y) @ x + y @ y + d * N
    prob = cp.Problem(cp.Minimize(obj), [x >= -1, x <= 1])
    prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    return float(prob.value), np.asarray(x.value)


def part_a():
    rng = np.random.default_rng(7)
    worst_v = 0.0; worst_g = 0.0; minev = np.inf
    for s in range(20):
        N, M, rho = 30, 60, 20.0
        A, y, xs = make_instance(N, M, rho, s)
        w = y - A @ xs
        G = A.T @ A
        d = np.linalg.eigvalsh(G)[0]
        f = lambda x: float(np.sum((y - A @ x) ** 2))
        fd = lambda x: f(x) + d * float(np.sum(1 - x ** 2))
        for _ in range(20):
            x = rng.choice([-1.0, 1.0], N)
            worst_v = max(worst_v, abs(fd(x) - f(x)) / f(x))
        minev = min(minev, np.linalg.eigvalsh(2 * (G - d * np.eye(N)))[0] / (2 * np.linalg.eigvalsh(G)[-1]))
        zeta = xs * (A.T @ w)
        h = 1e-6
        for i in range(N):
            e = np.zeros(N); e[i] = h
            gi = (fd(xs + e) - fd(xs - e)) / (2 * h)
            worst_g = max(worst_g, abs(xs[i] * gi - (-2 * zeta[i] - 2 * d)) / (1 + abs(zeta[i])))
    print("(a) max |f_d - f|/f on 400 random vertices: %.1e; min eigenvalue of Hessian / (2 lambda_max(A'A)): %.1e; max gradient-identity error: %.1e"
          % (worst_v, minev, worst_g))


def part_b():
    agree = 0; tot = 0; n_exact = 0
    for s in range(160):
        N, M = 40, 80
        rho = [30.0, 60.0, 100.0, 200.0][s % 4]
        A, y, xs = make_instance(N, M, rho, 1000 + s)
        w = y - A @ xs
        d = np.linalg.eigvalsh(A.T @ A)[0]
        zeta = xs * (A.T @ w)
        cond = bool(zeta.min() >= -d)
        val, x = shifted_box_min(A, y, d)
        is_xs = bool(np.max(np.abs(x - xs)) < 1e-4)
        tot += 1; agree += (cond == is_xs); n_exact += is_xs
    print("(b) beta = 2, N = 40, rho in {30, 60, 100, 200}: box minimiser of f_d equals x* iff min zeta >= -lambda_min: agreement %d / %d (x* is the minimiser in %d)"
          % (agree, tot, n_exact))


def part_c():
    print("(c) per-instance exactness thresholds rho*/log N (medians [min, max]); prediction 2b/(sqrt b-1)^4 (shift, Prop. 6.3) and 2b/(b-1)^2 (SDP heuristic)")
    for beta in (2.0, 4.0):
        for N, S in ((100, 40), (400, 40), (1600, 10)):
            M = int(beta * N)
            sh = []; sd = []
            for s in range(S):
                A, y, xs = make_instance(N, M, 1.0, s)     # rho = 1: A = H/sqrt(N)
                w = y - A @ xs
                H = A * np.sqrt(N)
                g = xs * (H.T @ w) / np.linalg.norm(w)
                smin = np.linalg.svd(H, compute_uv=False)[-1]
                W = float(w @ w)
                sh.append(N * W * max(-g.min(), 0.0) ** 2 / smin ** 4)
                K = H.T @ H / N
                D = np.diag(xs * (H.T @ w)) / np.sqrt(N)
                lam = eigh(-D, K, eigvals_only=True)[-1]
                sd.append(max(lam, 0.0) ** 2)
            L = np.log(N)
            sh = np.array(sh) / L; sd = np.array(sd) / L
            print("   beta=%g N=%d (%d inst.): shift %.1f [%.1f, %.1f] (pred %.1f) | SDP %.2f [%.2f, %.2f] (heuristic %.2f)"
                  % (beta, N, S, np.median(sh), sh.min(), sh.max(), 2 * beta / (np.sqrt(beta) - 1) ** 4,
                     np.median(sd), sd.min(), sd.max(), 2 * beta / (beta - 1) ** 2), flush=True)


def part_d():
    print("(d) note's part F setting (beta = 2, N = 200, seeds 0-3), d = lambda_min(A'A): relative gaps (W - bound)/W")
    N, M = 200, 400
    for rho in (30.0, 60.0, 130.0, 300.0, 600.0):
        gb = []; gs = []; ex = 0; cond = 0
        for s in range(4):
            A, y, xs = make_instance(N, M, rho, s)
            w = y - A @ xs
            W = float(w @ w)
            B = A * xs
            R, _, _ = box_value(B, w)
            d = np.linalg.eigvalsh(A.T @ A)[0]
            val, x = shifted_box_min(A, y, d)
            zeta = xs * (A.T @ w)
            gb.append((W - R) / W); gs.append((W - val) / W)
            ex += bool(np.max(np.abs(x - xs)) < 1e-4); cond += bool(zeta.min() >= -d)
        print("   rho=%5.0f: box gap median %.3f | shifted gap median %.2e max %.2e | x* is the shifted box minimiser in %d/4 (condition holds in %d/4)"
              % (rho, np.median(gb), np.median(gs), np.max(gs), ex, cond), flush=True)


if __name__ == "__main__":
    part_a(); part_b(); part_c(); part_d()
