"""Continuous quantities of the examples used in extension-n2.md: switch time, eta_L, D, F''(tau)
(formula D + Delta^2 eta_L and finite differences), kappa, beta_L, w, the bang-bang grid optimum
(<= 3 switches, 61-point grid), and the continuous calibration families for A."""
import json
import numpy as np
from model import Par, find_switch, solve_arcs, switch_quantities, Fpp_fd, pmp_check, continuous_family
from explore_family import global_bb

EX = {
    "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
    "A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5),
    "B": Par(T=2.0, a=1.0, rho=1.0, k1=0.6, k2=-1.2, c=0.5, q=1.0, x20=0.5, e=0.3),
    "B2": Par(T=2.0, a=1.0, rho=0.5, k1=0.5, k2=-0.6, q=0.3, c=0.2),
    "C": Par(T=2.0, a=1.0, rho=0.5, k1=0.5, k2=-0.2, q=0.3, c=0.2),
}
out = {}
for name, p in EX.items():
    roots = find_switch(p)
    sol = solve_arcs(p, roots[0])
    sq = switch_quantities(p, sol)
    _, fdr = Fpp_fd(p, roots[0])
    gb = global_bb(p, n=61)
    rec = dict(roots=roots, tau=roots[0], J=sol["J"], pmp_violation=pmp_check(p, sol), w=p.w.tolist(),
               eta_L=sq["eta_L"], beta_L=sq["beta_L"].tolist(), D=sq["D"], Fpp=sq["Fpp_formula"], Fpp_fd=fdr,
               kappa=sq["Delta"] / (2 * abs(sq["sigdot_b"])), ratio=sq["Delta"] ** 2 * abs(sq["eta_L"]) / sq["D"],
               bb_grid_J=gb[0], bb_grid_u0=gb[1][0], bb_grid_switches=[float(v) for v in gb[1][1]])
    if name in ("A", "A0"):
        for d1 in (None, 0.1, 0.02):
            Pf, dg = continuous_family(p, 0.02, d1)
            rec["cont_family_delta1_%s" % d1] = dict(pre_blowup=dg["pre_blowup"], Ptau=dg["Ptau"].tolist(),
                                                     beta_tau=dg["beta_tau"].tolist())
    out[name] = rec
    print(name, json.dumps(rec, default=float), flush=True)
json.dump(out, open("logs/examples_summary.json", "w"), indent=1, default=float)
