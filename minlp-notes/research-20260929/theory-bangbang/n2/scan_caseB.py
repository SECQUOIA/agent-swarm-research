"""Search for eta_L < 0 < F'' = D + Delta^2 eta_L with ratio r = Delta^2 |eta_L| / D close to 1
(continuous quantities only)."""
import itertools
import numpy as np
from model import Par, find_switch, solve_arcs, switch_quantities, pmp_check

for k1, k2, c, q, rho, x20, e in itertools.product([-0.6, -0.3, 0.0, 0.3, 0.6], [-1.2, -0.9, -0.6, -0.3],
                                                   [0.0, 0.2, 0.5], [0.0, 0.3, 1.0], [0.25, 0.5, 1.0],
                                                   [0.0, 0.5], [0.0, 0.3]):
    p = Par(T=2.0, a=1.0, rho=rho, k1=k1, k2=k2, q=q, c=c, x20=x20, e=e)
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
    if sq["eta_L"] < 0 < sq["Fpp_formula"]:
        r = 4 * abs(sq["eta_L"]) / sq["D"]
        print("r=%.3f k1=%+.1f k2=%+.1f c=%.1f q=%.1f rho=%.2f x20=%.1f e=%.1f | th=%.3f eta_L=%+.3f D=%.3f F''=%.3f beta_L=%s"
              % (r, k1, k2, c, q, rho, x20, e, sq["th"], sq["eta_L"], sq["D"], sq["Fpp_formula"], np.round(sq["beta_L"], 3)), flush=True)
