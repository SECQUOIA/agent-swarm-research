"""Referee check: opposite orientation + ball 2M^2 - x^2 - y^2, larger n (floating point, Clarabel; d2_sdp.build).
Usage: python3 d5_radius_n.py
"""
import json, warnings
warnings.filterwarnings("ignore")
import d2_sdp as D
for M in (1.1, 1.3, 1.5, 2.0):
    for n in (12, 16, 24, 32):
        prob, _ = D.build(n, "opp", M)
        prob.solve(solver="CLARABEL")
        print(json.dumps(dict(M=M, n=n, CLARABEL=[prob.status, float(f"{prob.value:.7g}")])), flush=True)
