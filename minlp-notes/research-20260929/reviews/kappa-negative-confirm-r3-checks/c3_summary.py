"""Summaries of logs/phase3.json (own KKT rebuild) and an own read-only diff of the author's sweep logs."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KLOG = os.path.join(HERE, "..", "..", "theory-bangbang", "kneg", "logs")
P = json.load(open(os.path.join(HERE, "logs", "phase3.json")))
out = {}
out["grids"] = len(P)
out["max_kkt_in_window"] = max(r["n_kkt_in_window"] for r in P)
out["max_abs_dev_new_vs_logged"] = max(abs(r["dev_new"]) for r in P)
out["max_abs_dev_r2formula_vs_old_log"] = max(abs(r["dev_old"]) for r in P)
out["max_abs_u_s1_vs_logged"] = max(abs(r["u_s1"] - r["u_s1_logged"]) for r in P)
out["max_abs_u_s1_vs_r1referee"] = max(abs(r["u_s1"] - r["u_s1_r1referee"]) for r in P if r["u_s1_r1referee"] is not None)
# quoted set: grids with a fractional second switch
GAM = {(0.5, 1.5): (3.70, 0.59), (0.55, 1.45): (3.58, 0.69), (0.45, 1.55): (3.81, 0.49)}
q = {}
for cfg, (g, e) in GAM.items():
    rows = [r for r in P if tuple(r["cfg"]) == cfg and r["s2_frac"]]
    ratio = math.exp(-g / e)
    larger = [r["corrected"] for r in rows if r["N"] > 1000]
    q[str(cfg)] = dict(grids=[(r["N"], "f" if r["s1_frac"] else "v", round(r["u_s1"], 4), r["break_minus_s1"],
                              "%.3e" % r["corrected"], "%.3e" % r["round2_formula"]) for r in rows],
                       larger_range=["%.3e" % min(larger), "%.3e" % max(larger)], factor=max(larger) / min(larger),
                       ratio="%.4e" % ratio, matching=[min(larger) / ratio, max(larger) / ratio])
out["quoted"] = q
out["n_quoted"] = sum(len(v["grids"]) for v in q.values())
# Check 4: theta_1(N) - theta_1(16000), stages of grid N; reference as in the note (corrected formula) and
# self-consistent reference for the round-2 formula
c4 = []
for cfg in GAM:
    rows = [r for r in P if tuple(r["cfg"]) == cfg]
    ref = [r for r in rows if r["N"] == 16000][0]
    for r in rows:
        if r["s1_frac"] and r["N"] < 16000:
            h = 2 / r["N"]
            c4.append((cfg, r["N"], (r["theta1_corr"] - ref["theta1_corr"]) / h,
                       (r["theta1_r2"] - ref["theta1_corr"]) / h, (r["theta1_r2"] - ref["theta1_r2"]) / h))
out["check4_n"] = len(c4)
out["check4_corrected"] = [min(x[2] for x in c4), max(x[2] for x in c4)]
out["check4_r2_vs_corrected_ref"] = [min(x[3] for x in c4), max(x[3] for x in c4)]
out["check4_r2_vs_own_ref"] = [min(x[4] for x in c4), max(x[4] for x in c4)]
# own diff of the two author logs
new = json.load(open(os.path.join(KLOG, "sweep.json")))
old = json.load(open(os.path.join(KLOG, "pre_revision", "sweep_r2.json")))
diffs, changed, fb = [], [], 0
for a, b in zip(old, new):
    for key in set(a) | set(b):
        if key in ("time", "break_time_minus_theta1", "u_s1"):
            continue
        if a.get(key) != b.get(key):
            diffs.append((b.get("t1"), b.get("N"), key))
    if "s1" in b and b["s1"] in b["frac"] and b["break_time_minus_theta1"] is not None:
        fb += 1
    if a.get("break_time_minus_theta1") != b.get("break_time_minus_theta1"):
        changed.append((b.get("kappa1"), b.get("t1"), b.get("N"), b["s1"] in b["frac"]))
out["log_records"] = (len(old), len(new))
out["log_other_diffs"] = diffs
out["log_frac_s1_with_break"] = fb
out["log_changed"] = len(changed)
out["log_changed_all_frac_s1"] = all(c[3] for c in changed)
out["log_total_time_s"] = sum(r.get("time", 0) for r in new)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "logs", "summary3.json"), "w"), indent=1)
