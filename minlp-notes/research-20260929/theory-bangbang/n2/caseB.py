"""Example B (eta_L < 0 < F''): continuous obstruction and its discrete trace.
- continuous: eta_L, D, F'' (formula and finite differences), singular-Riccati blow-up distance s_b
  (global model; and local model with the singular term only on (tau, tau + delta0]);
  leading-order prediction s_b ~ delta0 * exp(-1 / (kappa |eta|)), kappa = Delta / (2 |sigma'(tau)|);
- bang-bang grid search (<= 3 switches) for global optimality among bang-bang controls;
- discrete: the R^2-maximal recursion (discrete P-hat) breaks at stage t_b; (t_b - s) h vs N."""
import json
import numpy as np
from model import Par, find_switch, solve_arcs, switch_quantities, Fpp_fd, pmp_check, singular_riccati_after, B
from discrete import solve_kkt, fam_rmax, fx, bvec
from explore_family import global_bb

pB = Par(T=2.0, a=1.0, rho=1.0, k1=0.6, k2=-1.2, c=0.5, q=1.0, x20=0.5, e=0.3)

if __name__ == "__main__":
    res = {}
    roots = find_switch(pB)
    th = roots[0]
    sol = solve_arcs(pB, th)
    sq = switch_quantities(pB, sol)
    fd, fdr = Fpp_fd(pB, th)
    kap = sq["Delta"] / (2 * abs(sq["sigdot_b"]))
    res["continuous"] = dict(roots=roots, th=th, J=sol["J"], pmp=pmp_check(pB, sol), eta_L=sq["eta_L"], D=sq["D"],
                             Fpp=sq["Fpp_formula"], Fpp_fd=fdr, kappa=kap, beta_L=sq["beta_L"].tolist(),
                             ratio=sq["Delta"] ** 2 * abs(sq["eta_L"]) / sq["D"])
    print(json.dumps(res["continuous"]), flush=True)
    gb = global_bb(pB, n=61)
    res["bb_grid"] = dict(J=gb[0], u0=gb[1][0], switches=list(gb[1][1]))
    print("bang-bang grid best", res["bb_grid"], flush=True)
    res["blowup"] = []
    for eps in (0.0, 0.02):
        for d0 in (None, 0.2, 0.1):
            r = singular_riccati_after(pB, sol, eps, delta0=d0, s_top=0.19 if d0 is None else 0.999 * d0)
            pred = None if d0 is None else d0 * np.exp(-1.0 / (kap * abs(sq["eta_L"])))
            rec = dict(eps=eps, delta0=d0, blowup=r["blowup"], s_b=r.get("s_blow"), leading_order_pred=pred)
            res["blowup"].append(rec)
            print(rec, flush=True)
    res["discrete"] = []
    for N in (500, 1000, 2000, 4000, 8000, 16000):
        kk = solve_kkt(pB, N)
        for eps in (0.0, 0.02):
            Ps, brk, ms = fam_rmax(pB, kk, eps)
            s = kk["m"]
            rec = dict(N=N, eps=eps, s=s, fracset=sorted(kk["fracset"]), kkt=kk["kkt_viol"], J=kk["J"], brk=brk,
                       brk_minus_s=None if brk is None else brk - s,
                       brk_time_after_switch=None if brk is None else (brk - s) * kk["h"])
            res["discrete"].append(rec)
            print(rec, flush=True)
    json.dump(res, open("logs/caseB.json", "w"), indent=1, default=float)
