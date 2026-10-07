"""Check that each probe3 instance has a unique, interior, nondegenerate global
minimizer and that F is nonconvex somewhere in the box.

Heuristic evidence: multistart L-BFGS-B (random interior starts + random corners).
Certificate: chain_bb in localization mode. Cells are removed only if their
DP min-marginal exceeds UB + delta, so every x with F(x) <= UB + delta lies in
the box H = hull of the surviving cells. If H is inside (-1,1)^n and the
Hessian lower bound on H is positive definite, F is strictly convex on H, so
the global minimizer is unique, interior, and nondegenerate.

Nonconvexity: the Hessian diag(2 - 12 kappa x_i^2) + b offdiag dominates the
Hessian at any corner (diag 2 - 12 kappa), so lambda_min over the box equals
lambda_min of that constant tridiagonal matrix.
"""
import json, sys
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
import instances as I
import chain_bb as CB


def check(n, seed, amp=0.3, nstarts=200, ncorners=50, delta=1e-4, eps=1e-6):
    c = I.coeffs(n, seed, amp)
    rng = np.random.default_rng(1000 + seed)
    starts = list(rng.uniform(-1, 1, (nstarts, n))) + list(rng.choice([-1.0, 1.0], (ncorners, n)))
    sols = [I.local_min(x0, c) for x0 in starts]
    fs = np.array([f for _, f in sols])
    best = int(np.argmin(fs)); xb = sols[best][0]; fb = fs[best]
    # distinct local minima (by position), and how many starts reached the best one
    reps = []
    for x, f in sols:
        if not any(np.max(abs(x - r)) < 1e-4 for r, _ in reps):
            reps.append((x, f))
    nbest = int(sum(np.max(abs(x - xb)) < 1e-4 for x, _ in sols))
    d, off = I.hess_tridiag(xb)
    lmin_at_min = float(eigvalsh_tridiagonal(d, off, select="i", select_range=(0, 0))[0])
    dc = np.full(n, 2 - 12 * I.KAPPA)
    lmin_box = float(eigvalsh_tridiagonal(dc, off, select="i", select_range=(0, 0))[0]) if n > 1 else float(dc[0])
    rec = dict(amp=amp, n=n, seed=seed, f_best=float(fb), n_starts=len(starts), n_distinct_local_min=len(reps),
               n_starts_to_best=nbest, second_best_f=float(sorted(f for _, f in reps)[1]) if len(reps) > 1 else None,
               max_abs_xstar=float(abs(xb).max()), grad_norm=float(np.linalg.norm(I.grad(xb, c))),
               lmin_hess_at_min=lmin_at_min, lmin_hess_over_box=lmin_box)
    pr = I.Probe3Chain(c)
    r = CB.chain_bb(pr, eps, mode="quad", localize_delta=delta, max_iter=40, time_limit=1200,
                    max_pairs_iter=5_000_000)
    rec.update(cert_status=r["status"], cert_certified=r["certified"] is not None, cert_delta=delta,
               cert_eps=eps, cert_LB=r["LB"], cert_UB=r["UB"], cert_iters=r["iters"], cert_time=r["time"],
               cert_UB_minus_multistart=float(r["UB"] - fb))
    if pr.cert is not None:
        rec.update({"cert_" + k: v for k, v in pr.cert.items()})
    return rec


if __name__ == "__main__":
    out, amp = sys.argv[1], float(sys.argv[2])
    ns = [int(a) for a in sys.argv[3:]]
    import os
    done = set()
    if os.path.exists(out):
        done = {(r["n"], r["seed"], r["amp"]) for r in map(json.loads, open(out))}
    jobs = [(n, s, amp) for n in ns for s in range(5) if (n, s, amp) not in done]
    with ProcessPoolExecutor(int(__import__("os").environ.get("WORKERS", "8"))) as ex, open(out, "a") as f:
        for rec in ex.map(check, *zip(*jobs)):
            f.write(json.dumps(rec) + "\n"); f.flush()
            print(rec["amp"], rec["n"], rec["seed"], rec["f_best"], rec["n_distinct_local_min"], rec["max_abs_xstar"],
                  round(rec["lmin_hess_at_min"], 4), round(rec["lmin_hess_over_box"], 4),
                  rec["cert_certified"], rec.get("cert_lmin"), flush=True)
