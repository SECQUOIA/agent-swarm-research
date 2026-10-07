"""Confirmation recheck of scouting.md, second revision.
(a) R4: Check 5.3 differences between the three implementations, read directly from
    their JSON logs (author: revision_checks.json; review: c2_transfer_theorem.json;
    recheck: r3_check53.json), and the review's a-increment ratios.
(b) R2: location of the binding stage at the h_0 threshold of the tilted scalar-LQ
    family (the leading-order prediction assumes it is near t = T), and the actual
    (T2) strictness constant c of the tilted S compared with e(T).
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
out = {}

own = {r["N"]: r for r in json.load(open(os.path.join(ROOT, "theory-calibration", "logs", "revision_checks.json")))["B"]}
rev = {r["N"]: r for r in json.load(open(os.path.join(ROOT, "reviews", "calibration-review-checks", "logs", "c2_transfer_theorem.json")))["B"]}
rch = {r["N"]: r for r in json.load(open(os.path.join(ROOT, "reviews", "calibration-recheck-checks", "logs", "r3_check53.json")))}
rows = []
for N in (10, 20, 40, 80):
    rec = {"N": N}
    for fam, ko, kr, kc in (("transferred", "transferred_gap", "transferred", "gap_transferred"),
                            ("uncorrected", "uncorrected_gap", "sampled_no_correction", "gap_uncorrected"),
                            ("costate", "costate_gap", "costate_affine", "gap_costate")):
        a, b, c = own[N][ko], rev[N]["families"][kr]["gap"], rch[N][kc]
        rec[fam] = {"author": a, "author-review": a - b, "author-recheck": a - c}
    rec["author_max_state_err_over_h"] = own[N]["max_state_err"] * N
    rows.append(rec)
    print("a", json.dumps(rec))
out["a_check53"] = rows
out["a_review_a_increment_over_h2"] = {N: rev[N]["a_increment_max_over_h2"] for N in sorted(rev)}
print("a_increment", out["a_review_a_increment_over_h2"])

T = 1.0
CASES = {1: (-2.0, 0.0), 2: (1.0, 1.0)}


def closed(cs, tt):
    if cs == 1:
        return 1.0 / (-0.25 + 1.25 * np.exp(4.0 * (T - tt)))
    c = T - np.arctanh(1 / np.sqrt(2)) / np.sqrt(2)
    return 1.0 - np.sqrt(2) * np.tanh(np.sqrt(2) * (tt - c))


def schur(cs, N, eps, lam):
    al, q = CASES[cs]
    h = T / N
    tt = h * np.arange(N + 1)
    s = closed(cs, tt) - 2 * eps * np.exp(-lam * tt)
    A = 1 + al * h
    return h * q + A * A * s[2:] / (1 + h * s[2:]) - s[1:-1]


k2 = json.load(open(os.path.join(HERE, "logs", "k2_tilted_h0.json")))
bind = []
for r in k2["scan"]:
    if r["N_bad"] is None:
        continue
    N = r["N_bad"]
    m = schur(r["case"], N, r["eps"], r["lam"])
    bad = np.nonzero(m < 0)[0] + 1  # stage indices t
    rec = {"case": r["case"], "lam": r["lam"], "eps": r["eps"], "N_bad": N,
           "failing_stages_t_over_N": [float(bad.min() / N), float(bad.max() / N)], "n_failing": int(bad.size)}
    bind.append(rec)
    print("b", json.dumps(rec))
out["b_binding"] = bind

# (T2) strictness constant of the tilted S for scalar LQ: r_S as a quadratic form in
# (d, w) = (x - x*, u - u*) is (w + P d)^2/2 + e[(lam - 2 alpha) d^2 - 2 d w]; the
# terminal constant is e(T).  c = min(min_t lambda_min(M(t)), e(T)).
cc = []
for cs, lams in ((1, (1.0, 4.0, 8.0)), (2, (4.0, 8.0))):
    al, q = CASES[cs]
    for lam in lams:
        for eps in (0.5, 0.02):
            tt = np.linspace(0, T, 20001)
            P = closed(cs, tt)
            e = eps * np.exp(-lam * tt)
            M11 = P * P / 2 + e * (lam - 2 * al)
            M12 = P / 2 - e
            M22 = 0.5 * np.ones_like(tt)
            tr, det = M11 + M22, M11 * M22 - M12 * M12
            lmin = tr / 2 - np.sqrt(np.maximum(tr * tr / 4 - det, 0))
            eT = eps * np.exp(-lam * T)
            c_stage = float(lmin.min())
            rec = {"case": cs, "lam": lam, "eps": eps, "eT": eT, "c_stage_min": c_stage,
                   "c_stage_over_eT": c_stage / eT, "argmin_t": float(tt[lmin.argmin()]),
                   "c_T2_over_eT": min(c_stage, eT) / eT}
            cc.append(rec)
            print("c", json.dumps(rec))
out["c_strictness"] = cc
with open(os.path.join(HERE, "logs", "k4_logs_and_binding.json"), "w") as fh:
    json.dump(out, fh, indent=1)
