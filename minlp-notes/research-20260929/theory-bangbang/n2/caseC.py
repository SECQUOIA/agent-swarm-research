"""Case C (eta_L = +0.20 > 0): local-version tangential calibrations exist (Theorem 2), but the
global-model maximal solution is tangential only at a very slow logarithmic rate after the switch,
and its tangential continuation blows up before the switch (relaxed-LQ conjugate point).
Also records where the discrete R^2-maximal recursion breaks."""
import json
import numpy as np
from model import Par, find_switch, solve_arcs, switch_quantities, continuous_family, B
from discrete import solve_kkt, fam_rmax

pC = Par(T=2.0, a=1.0, rho=0.5, k1=0.5, q=0.3, c=0.2, k2=-0.2)
out = dict(cont=[], disc=[])
th = find_switch(pC)[0]
sq = switch_quantities(pC, solve_arcs(pC, th))
out["eta_L"], out["D"], out["th"] = sq["eta_L"], sq["D"], th
for eps in (0.0, 0.02):
    for d1 in (None, 0.05, 0.02, 0.01):
        try:
            Pf, dg = continuous_family(pC, eps, d1)
            rec = dict(eps=eps, delta1=d1, ok=True, pre_blowup=dg["pre_blowup"], pre_blowup_t=dg["pre_blowup_t"],
                       beta_start=(dg.get("beta_layer_start") if d1 else dg.get("beta_tiny")).tolist(),
                       Ptau=dg["Ptau"].tolist())
        except AssertionError as ex:
            rec = dict(eps=eps, delta1=d1, ok=False, err=str(ex)[:120])
        out["cont"].append(rec)
        print(rec, flush=True)
for N in (500, 1000, 2000, 4000, 8000, 16000):
    kk = solve_kkt(pC, N)
    for eps in (0.0, 0.02):
        Ps, brk, ms = fam_rmax(pC, kk, eps)
        rec = dict(N=N, eps=eps, s=kk["m"], brk=brk, brk_time=None if brk is None else brk * kk["h"])
        out["disc"].append(rec)
        print(rec, flush=True)
json.dump(out, open("logs/caseC.json", "w"), indent=1, default=float)
