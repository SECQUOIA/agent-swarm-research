"""Fraction of grids N whose discrete KKT point has an interior (fractional) stage, compared with the
leading-order phase model of window-exactness.md, Remark 1.4: Delta^2 (kappa_tau + eta_L) / (D + Delta^2 eta_L).
Float screening.  usage: python3 phase_check.py  ->  logs/phase_check.json"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from toy import VERIFIER, TOYPLUS, TOYZERO, kkt, float_data, fam_const, stage_losses  # noqa: E402
from toy_cont import switch  # noqa: E402

out = {}
for name, toy in (("verifier", VERIFIER), ("plus", TOYPLUS), ("zero", TOYZERO)):
    sw = [r for r in switch(toy) if r["pmp_viol"] < 1e-9][0]
    pred = 4 * sw["frac_curv"] / sw["Fpp"]
    Ns = list(range(101, 1101, 4))
    fr, two, cert = 0, 0, 0
    for N in Ns:
        kk = kkt(toy, N)
        fr += len(kk["frac"]) >= 1
        two += len(kk["frac"]) >= 2
        if name == "plus":   # transferred family P = -k; stage-wise exact near the switch?
            L = stage_losses(toy, float_data(toy, kk), fam_const(N, -toy.k), stages=range(kk["s"] - 6, kk["s"] + 7))
            cert += max(L.values()) <= 1e-14
    out[name] = dict(N_range=[Ns[0], Ns[-1], 4], n=len(Ns), fraction_with_interior=fr / len(Ns), with_two=two,
                     predicted=pred, kinks_convex=bool(sw["D"] - 4 * sw["kappa_tau"] > 0))
    if name == "plus":
        out[name]["fraction_stagewise_exact"] = cert / len(Ns)
        out[name]["predicted_stagewise_exact_D_over_Fpp"] = sw["D"] / sw["Fpp"]
    print(name, out[name], flush=True)
json.dump(out, open(os.path.join(HERE, "logs", "phase_check.json"), "w"), indent=1)
