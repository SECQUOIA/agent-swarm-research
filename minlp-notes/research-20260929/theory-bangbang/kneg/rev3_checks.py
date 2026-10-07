"""Targeted checks for the revision of kappa-negative.md after review round 3
(reviews/kappa-negative-confirm-r2.md, item P1: phase position theta_1 of a fractional first switch).

usage: python3 rev3_checks.py PART [PART ...]    PART in: compare tallies   (read-only, seconds)
  compare  logs/sweep.json (rerun of run_multi.py sweep with the corrected theta_1) against the round-2 log
           logs/pre_revision/sweep_r2.json: every field other than break_time_minus_theta1, u_s1 (new) and
           time must be identical; break_time_minus_theta1 must change by -h u[s1] exactly on grids with a
           fractional first switch and a break, and not at all elsewhere.
  tallies  strong-drop configurations (kappa 1 -> 0): break time - theta_1 on grids with a fractional second
           switch; layer-law ratios exp(-2 gamma / (Delta |eta|)), Delta = 2, and the matching times that
           would reproduce the observed larger-N break times (computed from the log, not typed in); and, as a
           data check of the convention, theta_1 by the corrected and by the round-2 formula on grids with a
           fractional first switch, against theta_1 at N = 16000. Added after review round 4
           (reviews/kappa-negative-confirm-r3.md, nit N2): the round-2 formula also against its own
           theta_1(16000), and the overall ranges over all three configurations (record P1_theta1_overall).
Each part prints JSON lines and writes logs/rev3_<part>.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "logs")
T = 2.0
STRONG = ((0.5, 1.5, 3.70, 0.59), (0.55, 1.45, 3.58, 0.69), (0.45, 1.55, 3.81, 0.49))  # (t1, t2, gamma, |eta|)


def load(path):
    return json.load(open(os.path.join(LOG, path)))


def out(name, recs):
    with open(os.path.join(LOG, f"rev3_{name}.json"), "w") as f:
        json.dump(recs, f, indent=1, default=float)


def emit(recs, rec):
    print(json.dumps(rec, default=float), flush=True)
    recs.append(rec)


def theta1(r, sign):
    """Phase position of the first switch (+1 -> -1); sign = +1: corrected, sign = -1: round-2 formula."""
    h = T / r["N"]
    s1 = r["s1"]
    return s1 * h + h * (1 + sign * r["u_s1"]) / 2 if s1 in r["frac"] else s1 * h


def part_compare():
    recs = []
    old, new = load("pre_revision/sweep_r2.json"), load("sweep.json")
    assert len(old) == len(new), (len(old), len(new))
    skip = {"time", "break_time_minus_theta1", "u_s1"}
    other_diffs, changed, max_dev = [], [], 0.0
    for a, b in zip(old, new):
        keys = (set(a) | set(b)) - skip
        d = [k for k in sorted(keys) if a.get(k) != b.get(k)]
        if d:
            other_diffs.append((a.get("kappa1"), a.get("t1"), a.get("N"), d))
        if "s1" not in b or b["break_time_minus_theta1"] is None:
            continue
        h = T / b["N"]
        expect = a["break_time_minus_theta1"] - (h * b["u_s1"] if b["s1"] in b["frac"] else 0.0)
        max_dev = max(max_dev, abs(b["break_time_minus_theta1"] - expect))
        if b["break_time_minus_theta1"] != a["break_time_minus_theta1"]:
            changed.append((b["kappa1"], b["kappa2"], b["t1"], b["N"], round(b["u_s1"], 4),
                            a["break_time_minus_theta1"], b["break_time_minus_theta1"]))
    emit(recs, dict(check="P1_compare", records=len(new), other_field_differences=other_diffs,
                    n_changed_break_times=len(changed), changed=changed,
                    max_abs_dev_from_old_minus_h_u_s1=max_dev))
    out("compare", recs)


def part_tallies():
    recs = []
    sweep = load("sweep.json")
    allrows = []
    for (t1, t2, gam, eta) in STRONG:
        rows = [r for r in sweep if r.get("kappa1") == 1.0 and r.get("t1") == t1 and r.get("t2") == t2]
        fr = [(r["N"], r["break_minus_s1"], "f" if r["s1"] in r["frac"] else "v", round(r["u_s1"], 4),
               r["break_time_minus_theta1"]) for r in rows if r["s2"] in r["frac"]]
        larger = [x[4] for x in fr if x[0] > 1000]
        ratio = math.exp(-2 * gam / (2 * eta))
        emit(recs, dict(check="P1_break_times", t1=t1, t2=t2, frac_second_switch=fr,
                        larger_N_range=[min(larger), max(larger)], gamma=gam, abs_eta=eta, sb_over_s1=ratio,
                        implied_matching_time=[min(larger) / ratio, max(larger) / ratio]))
        # convention check: theta_1(N) should approach tau_1 smoothly; compare both formulas with N = 16000
        ref = [r for r in rows if r["N"] == 16000][0]
        th_ref = theta1(ref, +1)
        dev = [(r["N"], round(r["u_s1"], 4), (theta1(r, +1) - th_ref) / (T / r["N"]),
                (theta1(r, -1) - th_ref) / (T / r["N"])) for r in rows if r["s1"] in r["frac"] and r["N"] < 16000]
        # round 4 (nit N2): the round-2 formula against its own theta_1(16000) (differs from th_ref when the
        # N = 16000 first switch is fractional)
        th_ref2 = theta1(ref, -1)
        own = [(r["N"], (theta1(r, -1) - th_ref2) / (T / r["N"]))
               for r in rows if r["s1"] in r["frac"] and r["N"] < 16000]
        allrows += [(x[2], x[3], y[1]) for x, y in zip(dev, own)]
        emit(recs, dict(check="P1_theta1_vs_N16000_in_stages", t1=t1, t2=t2, theta1_N16000=th_ref,
                        ref_first_switch="f" if ref["s1"] in ref["frac"] else "v",
                        rows_N_u_corrected_roundtwo=dev,
                        max_abs_corrected=max(abs(x[2]) for x in dev), max_abs_roundtwo=max(abs(x[3]) for x in dev),
                        theta1_N16000_roundtwo=th_ref2, rows_N_roundtwo_own_ref=own))
    emit(recs, dict(check="P1_theta1_overall", n_rows=len(allrows),
                    corrected=[min(x[0] for x in allrows), max(x[0] for x in allrows)],
                    roundtwo_vs_corrected_ref=[min(x[1] for x in allrows), max(x[1] for x in allrows)],
                    roundtwo_vs_own_ref=[min(x[2] for x in allrows), max(x[2] for x in allrows)]))
    out("tallies", recs)


if __name__ == "__main__":
    for part in sys.argv[1:]:
        dict(compare=part_compare, tallies=part_tallies)[part]()
