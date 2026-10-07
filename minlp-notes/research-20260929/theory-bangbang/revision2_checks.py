"""Targeted checks for the second revision of report.md (round-1 confirmation issues).

Reads stored results only; nothing is re-optimized. Run from theory-bangbang/:
    OMP_NUM_THREADS=1 python3 revision2_checks.py > logs/revision2_checks.log

R1/M7: gaps between the author's certified bound, the verifier's exact value of the same
certificate, the verifier's rigorous upper bound and the float primal points (exact rationals).
R2:    p_v(3092) in the certificate data versus the refinement log.
M2:    durations and sides of the failing windows in the verifier's w = 0.5 toy.
"""
import json
from fractions import Fraction as F

import numpy as np

VER = "../reviews/bangbang-verification/logs/"


def show(label, x):
    print(f"{label}: {float(x):.4e}")


# R1 / M7 -------------------------------------------------------------------
cert = json.load(open("logs/optcdeg2_qcal_certify.json"))
exact = json.load(open(VER + "qcal_exact.json"))
primal = json.load(open(VER + "primal_check.json"))

lb_author = F(cert["certified_bound"])  # the stored double, exactly
s = exact["bound_str"]  # digits of the exact value, 3 integer digits
lb_exact = F(s[:3] + "." + s[3:])
ub_full = F(primal["rigorous_primal"]["J_point"])  # upper end of the enclosure (width 4.7e-44)
ub_quoted = F("293.87607509587509328")  # rounded up, as quoted
fp_author = F(cert["J_float"])
fp_first_wave = F("293.876075095886")
lb_trunc = F("293.876075095875092379")

print("exact LB of the same certificate:", s[:3] + "." + s[3:])
print("truncated quote <= exact LB:", lb_trunc <= lb_exact)
print("quoted UB >= enclosure upper end:", ub_quoted >= ub_full)
show("gap, author LB vs rigorous UB", ub_quoted - lb_author)
show("  relative", (ub_quoted - lb_author) / ub_quoted)
show("gap, exact LB vs rigorous UB (quoted)", ub_quoted - lb_exact)
show("gap, exact LB vs rigorous UB (enclosure end)", ub_full - lb_exact)
show("author LB below exact LB", lb_exact - lb_author)
show("author float point above rigorous UB", fp_author - ub_full)
show("gap, author LB vs author float point", fp_author - lb_author)
show("gap, author LB vs first-wave float point", fp_first_wave - lb_author)

# R2 ------------------------------------------------------------------------
pv = np.load("logs/optcdeg2_qcal_data.npz")["pv"]
print(f"certificate data p_v(3092) = {pv[3092]:.4e}")
last = [json.loads(line) for line in open("logs/refine_primal.log") if line.strip()][-1]
print(f"refinement log final pv_k1p1 = {last['pv_k1p1']:.4e}")
first = json.loads(open("logs/explore1.log").readline())
print(f"before refinement p_v(3092) = {first['pv_s1p1']:.4e}")

# M2 ------------------------------------------------------------------------
for dom in ("box", "reach"):
    for r in json.load(open(VER + f"window_toy_k-0.5_{dom}.json")):
        a = r["A"]
        print(f"toy {dom:5s} N={r['N']:5d} affine fails {a['fail']:4d} stages, "
              f"duration {a['duration']:.5f}, stages rel. to switch {a['range']}; "
              f"tangential fails {r['B']['fail']}; predicted {r['predicted_duration_A']:.3f}")
