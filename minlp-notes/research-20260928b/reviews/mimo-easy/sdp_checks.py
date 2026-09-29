"""Reviewer checks of Section 6 (Shor SDP).

Exact per-instance threshold.  With K = H'H/N and D = diag(x* o H'w)/sqrt(N),
    A'A + diag(zeta) = sqrt(rho) * ( sqrt(rho) K + D ),
so the certificate of Proposition 6.1 holds iff sqrt(rho) >= s*, where
s* = lambda_max of the generalized pencil (-D, K).  Hence the SDP is exact at
x* iff rho >= rho* := max(s*, 0)^2 (monotone in rho; closed form, no bisection).

(a) Proposition 6.1 checked against an actual SDP solve (CVXPY + Clarabel) at
    rho = 0.5 rho* and 2 rho*, small N.
(b) rho* statistics for beta in {1, 1.5, 2, 3, 4}, N = 100, 400, 1600 (+ 200, 800,
    3200 for beta = 1), with the note's heuristic 2 beta/(beta-1)^2, the proved
    constant 2 beta/(sqrt beta - 1)^4, the one-bit (diagonal) threshold, the
    coordinate (rank-one) heuristic and the reviewer's smallest-eigenvector
    heuristic for square systems.
Written by the reviewer.  Usage: python3 sdp_checks.py a|b
"""
import os, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.linalg import eigh
from multiprocessing import Pool


def gen(N, M, seed):
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N)); xs = rng.choice([-1.0, 1.0], N); w = rng.standard_normal(M)
    return H, xs, w


def rho_star(H, xs, w):
    M, N = H.shape
    K = H.T @ H / N
    d = xs * (H.T @ w) / np.sqrt(N)
    s = eigh(-np.diag(d), K, eigvals_only=True, subset_by_index=[N - 1, N - 1])[0]
    rs = max(s, 0.0) ** 2
    # one-bit (diagonal) threshold
    neg = d < 0
    sd = np.max(-d[neg] / np.diag(K)[neg]) if neg.any() else 0.0
    # coordinate rank-one heuristic: s >= -d_i (K^{-1})_ii
    Kinv_d = np.diag(np.linalg.inv(K))
    sc = np.max(-d[neg] * Kinv_d[neg]) if neg.any() else 0.0
    # smallest-eigenvector heuristic
    lam, V = np.linalg.eigh(K)
    # bottom-mode lower bound: s* >= -(v_k o v_k)'d / lambda_k for every eigenpair (Rayleigh quotient)
    vals = [-(V[:, k] ** 2) @ d / lam[k] for k in range(5)]
    sv = max(max(vals), 0.0)
    return rs, sd ** 2, sc ** 2, sv ** 2, (lam[0], vals[0])


def check_direct(H, xs, w, rho):
    M, N = H.shape
    A = np.sqrt(rho / N) * H
    zeta = xs * (A.T @ w)
    return np.linalg.eigvalsh(A.T @ A + np.diag(zeta))[0]


def sdp_value(A, y):
    import cvxpy as cp
    N = A.shape[1]
    C = np.hstack([A, -y[:, None]])
    Q = C.T @ C
    sc = np.abs(Q).max()  # rescale for conditioning; value rescaled back
    X = cp.Variable((N + 1, N + 1), PSD=True)
    prob = cp.Problem(cp.Minimize(cp.trace((Q / sc) @ X)), [cp.diag(X) == 1])
    prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11)
    if X.value is None:
        prob.solve(solver=cp.CLARABEL)
    Xv = X.value
    ev = np.linalg.eigvalsh(Xv)
    return prob.value * sc, ev[-2] / ev[-1]


def part_a():
    print("N beta seed rho*/logN | rho/rho*  SDP value  f(x*)  (f-SDP)/f  2nd/1st eig of X  lambda_min(cert)")
    bad = 0
    for beta in (1, 2):
        acc = skipped = 0
        for seed in range(100):
            if acc == 8:
                break
            N = 10; M = beta * N
            H, xs, w = gen(N, M, 300 + seed + 10 * beta)
            rs = rho_star(H, xs, w)[0]
            if rs > 1e4:  # Clarabel inaccurate at this scaling (see sdp_checks_a_first_attempt.out)
                skipped += 1
                continue
            acc += 1
            for fac in (0.5, 2.0):
                rho = fac * rs
                A = np.sqrt(rho / N) * H
                y = A @ xs + w
                val, er = sdp_value(A, y)
                f = float(w @ w)
                lm = check_direct(H, xs, w, rho)
                ok = (fac > 1 and abs(f - val) <= 1e-6 * f and er < 1e-6) or (fac < 1 and f - val > 1e-6 * f)
                bad += not ok
                print(f"{N} {beta} {seed} {rs/np.log(N):9.3g} | {fac:.1f} {val:.8f} {f:.8f} {(f-val)/f:+.2e} {er:.1e} {lm:+.3e} {'OK' if ok else 'MISMATCH'}")
        print(f"beta={beta}: skipped {skipped} instances with rho* > 1e4")
    print("mismatches:", bad)


def job(args):
    beta, N, seed = args
    M = int(round(beta * N))
    H, xs, w = gen(N, M, seed)
    rs, rd, rc, rv, lam0 = rho_star(H, xs, w)
    # consistency with the direct certificate
    c1 = check_direct(H, xs, w, rs * 1.001) >= -1e-9 if rs > 0 else True
    c2 = check_direct(H, xs, w, rs * 0.999) < 0 if rs > 0 else True
    return beta, N, rs, rd, rc, rv, lam0, bool(c1 and c2)


def part_b():
    jobs = []
    for beta in (1.0, 1.5, 2.0, 3.0, 4.0):
        for N, T in ((100, 40), (400, 40), (1600, 10)):
            jobs += [(beta, N, 10 ** 6 + int(10 * beta) * 1000 + N + s) for s in range(T)]
    for N, T in ((200, 40), (800, 20), (3200, 5)):
        jobs += [(1.0, N, 2 * 10 ** 6 + N + s) for s in range(T)]
    jobs.sort(key=lambda a: -a[1] * a[0])
    with Pool(5) as p:
        out = p.map(job, jobs, chunksize=1)
    print("beta N inst | median c*=rho*/logN [min,max] | median log(rho*)/logN | median one-bit/logN | heuristic 2b/(b-1)^2 | "
          "proved 2b/(sqrt b-1)^4 | median rho*/rho_coord | median (bottom-5-mode lower bound)/rho* | frac bottom mode unfavourable | median log(rho*/N^3) | direct-check ok")
    for beta in (1.0, 1.5, 2.0, 3.0, 4.0):
        for N in (100, 200, 400, 800, 1600, 3200):
            R = [o for o in out if o[0] == beta and o[1] == N]
            if not R:
                continue
            rs = np.array([o[2] for o in R]); rd = np.array([o[3] for o in R]); rc = np.array([o[4] for o in R]); rv = np.array([o[5] for o in R])
            L = np.log(N)
            heur = f"{2*beta/(beta-1)**2:.2f}" if beta > 1 else "-"
            prov = f"{2*beta/(np.sqrt(beta)-1)**4:.1f}" if beta > 1 else "-"
            unf = np.array([o[6][1] > 0 for o in R])  # bottom K-mode has v'Dv < 0
            print(f"{beta} {N} {len(R)} | {np.median(rs)/L:.3g} [{rs.min()/L:.3g}, {rs.max()/L:.3g}] | {np.median(np.log(rs))/L:.3f} | "
                  f"{np.median(rd)/L:.3g} | {heur} | {prov} | {np.median(rs/rc):.3g} | "
                  f"{np.median(rv/rs):.3g} | {unf.mean():.2f} | {np.median(np.log(rs/N**3)):+.2f} | {all(o[7] for o in R)}")


def brute_opt(A, y):
    N = A.shape[1]
    best = np.inf
    # enumerate x in {-1,1}^N in chunks of 2^12
    lo = 12 if N > 12 else N
    V_lo = np.array(list(__import__("itertools").product([-1.0, 1.0], repeat=lo)))
    for hi in __import__("itertools").product([-1.0, 1.0], repeat=N - lo):
        r0 = y - A[:, lo:] @ np.array(hi) if N > lo else y
        F = ((r0[None, :] - V_lo @ A[:, :lo].T) ** 2).sum(1)
        best = min(best, F.min())
    return best


def part_c():
    """Square systems: relative root gaps (OPT - bound)/OPT of box and SDP, OPT by enumeration."""
    from scipy.optimize import lsq_linear
    print("N rho | median box gap | median SDP gap [max] | SDP exact at x* (rho >= rho*) | x* optimal")
    for N in (16, 20):
        for tag, rho in (("2logN", 2 * np.log(N)), ("4logN", 4 * np.log(N)), ("8logN", 8 * np.log(N)), ("N/4", N / 4)):
            bg, sg, ex, xo = [], [], 0, 0
            for s in range(6):
                H, xs, w = gen(N, N, 5000 + 31 * N + s)
                A = np.sqrt(rho / N) * H; y = A @ xs + w
                OPT = brute_opt(A, y)
                r = lsq_linear(A, y, bounds=(-1, 1), method="bvls", tol=1e-14)
                R = float(np.sum((y - A @ r.x) ** 2))
                val, _ = sdp_value(A, y)
                bg.append((OPT - R) / OPT); sg.append((OPT - val) / OPT)
                ex += rho >= rho_star(H, xs, w)[0]
                xo += abs(OPT - float(w @ w)) <= 1e-9 * OPT
            print(f"{N} {tag}({rho:.1f}) | {np.median(bg):.3f} | {np.median(sg):.3f} [{max(sg):.3f}] | {ex}/6 | {xo}/6")


if __name__ == "__main__":
    if sys.argv[1] == "a":
        part_a()
    elif sys.argv[1] == "c":
        part_c()
    else:
        part_b()
