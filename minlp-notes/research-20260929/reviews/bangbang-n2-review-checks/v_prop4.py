"""Proposition 4: P(tau) of the Theorem-2 construction vs the bound Q_eps(tau+) - beta beta^T / eta, as d1 -> 0."""
import json
import numpy as np
import v_localtsqc as L
import v_riccati as R

out = []
for name in ("A", "C"):
    for eps in (0.02,):
        tau, Q, beta, eta, siga, par, w = R.Qeps_at_tau(name, eps)
        Pmax = Q - np.outer(beta, beta) / eta
        for d1 in (0.04, 0.02, 0.01, 0.005, 0.0025):
            P_and_M, siga, sigb, tau, w, info, by_min = L.build(name, eps, d1)
            Pt = np.array(info["Ptau"])
            diff = Pt - Pmax
            rec = dict(example=name, eps=eps, d1=d1, Ptau=Pt.tolist(), Pmax=Pmax.tolist(),
                       max_eig_diff=float(np.linalg.eigvalsh(diff)[-1]), norm_diff=float(np.abs(diff).max()))
            print(json.dumps(rec), flush=True)
            out.append(rec)
json.dump(out, open("logs/v_prop4.json", "w"), indent=1)
