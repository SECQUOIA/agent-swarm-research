"""Parameter scan: continuous eta_L, D, F'' and the discrete R^2-maximal recursion (N=400, eps=0.02):
does it break, and how tangential is it at the switch (|beta_s|)?"""
import itertools, sys
import numpy as np
from model import Par, find_switch, solve_arcs, switch_quantities, pmp_check
from discrete import solve_kkt, fam_rmax, fx, bvec

rows = []
for k1, k2, c, q, rho, x20 in itertools.product([-0.6, -0.3, 0.0, 0.3], [-0.6, -0.3, 0.0, 0.3],
                                                [0.0, 0.2], [0.3, 1.0], [0.5, 1.0, 2.0], [0.0, 0.5]):
    p = Par(T=2.0, a=1.0, rho=rho, k1=k1, k2=k2, q=q, c=c, x20=x20)
    try:
        roots = find_switch(p)
    except Exception:
        continue
    if len(roots) != 1:
        continue
    sol = solve_arcs(p, roots[0])
    if pmp_check(p, sol) > 1e-9:
        continue
    sq = switch_quantities(p, sol)
    try:
        kk = solve_kkt(p, 400)
    except AssertionError:
        continue
    Ps, brk, ms = fam_rmax(p, kk, 0.02)
    s = kk["m"]
    F = fx(kk["h"])
    bs = F.T @ Ps[s + 1] @ bvec - p.w
    r = (k1, k2, c, q, rho, x20, sq["th"], sq["eta_L"], sq["D"], sq["Fpp_formula"], brk,
         float(np.linalg.norm(bs)), float(np.nanmax(np.abs(Ps))), sq["beta_L"][0])
    rows.append(r)
    print("k1=%+.1f k2=%+.1f c=%.1f q=%.1f rho=%.1f x20=%.1f | th=%.3f eta_L=%+.3f D=%.2f F''=%.2f beta_L1=%+.2f | rmax brk=%s |beta_s|=%.3f max|P|=%.1f"
          % (k1, k2, c, q, rho, x20, sq["th"], sq["eta_L"], sq["D"], sq["Fpp_formula"], sq["beta_L"][0], brk, r[11], r[12]), flush=True)
