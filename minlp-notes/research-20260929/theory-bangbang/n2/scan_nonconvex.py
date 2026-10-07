"""Look for a variant of example A whose Euler transcription is NOT convex in u (reduced Hessian
indefinite at the KKT point) while eta_L > 0 and the discrete maximal recursion stays unbroken
and exact over the reachable box."""
import itertools, json
import numpy as np
from model import Par, with_, find_switch, solve_arcs, switch_quantities, pmp_check
from discrete import solve_kkt, fam_rmax, stage_losses, _sig_of

base = Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5)
N = 200
for c, q, rho in itertools.product([0.4, 0.6, 1.0, 1.5], [0.3, 1.0], [1.0, 2.0]):
    p = with_(base, c=c, q=q, rho=rho)
    r = find_switch(p)
    if len(r) != 1:
        print("c=%.1f q=%.1f rho=%.1f: %d switches" % (c, q, rho, len(r))); continue
    sol = solve_arcs(p, r[0])
    if pmp_check(p, sol) > 1e-9:
        print("c=%.1f q=%.1f rho=%.1f: PMP fails" % (c, q, rho)); continue
    sq = switch_quantities(p, sol)
    try:
        kk = solve_kkt(p, N)
    except Exception as ex:
        print("c=%.1f q=%.1f rho=%.1f: kkt fail %s" % (c, q, rho, ex)); continue
    h, u = kk["h"], kk["u"]
    s0 = _sig_of(p, N, u)
    Hm = np.empty((N, N))
    for j in range(N):
        du = np.zeros(N); du[j] = 1.0
        Hm[:, j] = h * (_sig_of(p, N, u + du) - s0)
    ev = np.linalg.eigvalsh(0.5 * (Hm + Hm.T))
    Ps, brk, _ = fam_rmax(p, kk, 0.02)
    nf = None
    if brk is None:
        loss, lN = stage_losses(p, kk, Ps)
        nf = int((loss > 1e-12).sum())
    print("c=%.1f q=%.1f rho=%.1f: th=%.3f eta_L=%+.3f D=%.3f F''=%.3f | reduced Hessian min eig %.2e (#neg %d) | rmax brk=%s nfail=%s"
          % (c, q, rho, r[0], sq["eta_L"], sq["D"], sq["Fpp_formula"], ev[0], (ev < 0).sum(), brk, nf), flush=True)
