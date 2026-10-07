"""Audit existing stream logs; no optimization or separation is run.

Usage (from the stream directory): python3 code/audit_closeout.py
Writes logs/audit_closeout.json and prints the same report. Quantiles use
linear interpolation (numpy). 'complete' is the implementation's flag,
not an exact-arithmetic certificate. Earlier runs are compared only on
common points, with timing and time-limited MIQP outcomes kept separate.
"""
import collections
import json
from pathlib import Path
import statistics as st

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs"


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def dist(values):
    v = list(values)
    return None if not v else dict(zip(("min", "median", "p90", "max"),
                                       map(float, np.quantile(v, (0, .5, .9, 1)))))


def counts(values):
    return dict(sorted(collections.Counter(map(str, values)).items()))


def ident(d):
    name, base, stage = d["file"].removesuffix(".npz").split("__")
    return name, base, stage


def main():
    report = {}
    selections = [p for f in ("sep_selection_A.txt", "sep_selection_B.txt")
                  for p in (LOG / f).read_text().split()]
    selected_names = [Path(p).name for p in selections]
    rows = []
    shards = []
    for i in range(3):
        selection = (LOG / f"sep_shard_{i:02d}").read_text().split()
        rr = read(LOG / f"sep_run2_s{i}.jsonl")
        names = [r["file"] for r in rr]
        assert collections.Counter(names) == collections.Counter(Path(p).name for p in selection)
        output = (LOG / f"run_sep_run2_s{i}.out").read_text()
        assert "Traceback" not in output
        shards.append(dict(shard=i, records=len(rr), warning_lines=output.count("RuntimeWarning"),
                           thm3_errors=[r["file"] for r in rr if "error" in r.get("thm3", {})]))
        rows.extend(rr)
    assert collections.Counter(r["file"] for r in rows) == collections.Counter(selected_names)
    assert len(set(selected_names)) == len(selected_names) == 123
    report["completeness"] = dict(selections=[92, 31], shards=shards, unique_points=123,
                                  disjoint_shards=True)
    opened = set((LOG / "open_gap.txt").read_text().split())
    group = lambda d: "root" if ident(d)[2] == "root" else (
        "open-final" if ident(d)[0] in opened else "near-closed-final")
    report["separation"] = {}
    for key in ("root", "open-final", "near-closed-final"):
        rr = [r for r in rows if group(r) == key]
        ratio = [r["ratio"] for r in rr]
        meaningful = [r for r in ratio if r["q"] is not None and -r["q"] > 1e-3]
        d = dict(points=len(rr), ranks=dist(r["rank"]["1e-05"] for r in rr),
                 stages=counts(ident(r)[2] for r in rr),
                 complete=sum(r["complete"] for r in ratio),
                 times=dist(r["time"] for r in ratio),
                 complete_times=dist(r["time"] for r in ratio if r["complete"]),
                 incomplete_times=dist(r["time"] for r in ratio if not r["complete"]),
                 ratios=dist(r["ratio"] for r in ratio),
                 violations=dist(-r["q"] for r in ratio if r["q"] is not None),
                 meaningful_splits=len(meaningful),
                 meaningful_support=counts(r["supp"] for r in meaningful),
                 meaningful_vmax=counts(r["vmax"] for r in meaningful),
                 incomplete_points=[r["file"] for r in rr if not r["ratio"]["complete"]],
                 iteration_limit=sum(r["iters"] == 60 for r in ratio))
        d["families"] = {str(k): dict(above_1e3=sum(r[f"fam{k}"]["max_viol"] > 1e-3 for r in rr),
                                            violations=dist(r[f"fam{k}"]["max_viol"] for r in rr),
                                            times=dist(r[f"fam{k}"]["time"] for r in rr)) for k in (1, 2, 3)}
        family_ratio = lambda r: max(0, *(r[f"fam{k}"]["max_ratio"] for k in (1, 2, 3)))
        d["ratio_agrees_family_1e8"] = sum(abs(r["ratio"]["ratio"] - family_ratio(r)) < 1e-8 for r in rr)
        d["max_ratio_minus_family"] = max(r["ratio"]["ratio"] - family_ratio(r) for r in rr)
        d["general_ratio_improvements"] = [dict(file=r["file"], improvement=r["ratio"]["ratio"] - family_ratio(r))
                                             for r in rr if r["ratio"]["ratio"] - family_ratio(r) > 1e-8]
        d["gurobi"] = {}
        for k in (1, 3, 10):
            gg = [r[f"grb{k}"] for r in rr]
            d["gurobi"][str(k)] = dict(status=counts(g["status"] for g in gg),
                                       times=dist(g["time"] for g in gg),
                                       violations=dist(-g["q"] for g in gg if g["q"] is not None),
                                       above_1e3=sum(g["q"] is not None and g["q"] < -1e-3 for g in gg),
                                       below_psd_floor=sum(g["q"] is not None and g["q"] < -.250001 for g in gg))
        tt = [r["thm3"] for r in rr if "thm3" in r and "error" not in r["thm3"]]
        d["thm3"] = dict(attempted=sum("thm3" in r for r in rr), returned=len(tt),
                          errors=[r["thm3"]["error"] for r in rr if "error" in r.get("thm3", {})],
                          q_near_quarter=sum(abs(t["q"] + .25) < 1e-9 for t in tt),
                          q_float_equals_quarter=sum(t["q"] == -.25 for t in tt),
                          complete=sum(t["complete"] for t in tt),
                          digits=dist(t["vmax_digits"] for t in tt if t["q"] < 0),
                          times=dist(t["time"] for t in tt), errors_in_matrix=dist(t["err"] for t in tt),
                          no_split=sum(t["q_at_Y"] is None for t in tt),
                          survives_at_raw_point=sum(isinstance(t["q_at_Y"], (int, float)) and
                              -.250001 <= t["q_at_Y"] < 0 for t in tt),
                          bad_at_raw_point=sum(t["q_at_Y"] is not None and (
                              isinstance(t["q_at_Y"], str) or not -.250001 <= t["q_at_Y"] < 0) for t in tt))
        report["separation"][key] = d
    report["root_by_n"] = {str(n): dict(points=len(rr), complete=sum(r["ratio"]["complete"] for r in rr),
                                        times=dist(r["ratio"]["time"] for r in rr))
                            for n in sorted({r["N"] - 1 for r in rows if group(r) == "root"})
                            for rr in [[r for r in rows if group(r) == "root" and r["N"] - 1 == n]]}
    paths = {p.name: p for p in (ROOT / "data").glob("points_*/*.npz")}
    raw_checks = []
    for r in rows:
        Y = np.load(paths[r["file"]])["Y"]
        a = r["ratio"]
        if a["v"] is not None:
            v = np.array(a["v"], dtype=float)
            raw_q = float(v @ Y @ v + v @ Y[:, 0])
            raw_checks.append(dict(file=r["file"], logged_q=a["q"], raw_q=raw_q,
                                   difference=abs(raw_q - a["q"])))
            assert abs(a["ratio"] + a["q"] / (v[1:] @ v[1:])) < 1e-9
    report["raw_ratio_check"] = dict(points=len(raw_checks), max_q_difference=max(d["difference"] for d in raw_checks),
                                     meaningful_lost=[d for d in raw_checks if d["logged_q"] < -1e-3 and d["raw_q"] >= -1e-3])
    old = {r["file"]: r for f in (LOG / "run1_highload").glob("sep_*.jsonl") for r in read(f)}
    common = [r for r in rows if r["file"] in old]
    report["run_agreement"] = dict(common=len(common), missing_in_first=sorted(set(selected_names) - set(old)),
        max_family_difference=max(abs(r[f"fam{k}"]["max_viol"] - old[r["file"]][f"fam{k}"]["max_viol"])
                                  for r in common for k in (1, 2, 3)),
        max_ratio_difference=max(abs(r["ratio"]["ratio"] - old[r["file"]]["ratio"]["ratio"]) for r in common),
        changed_ratios=[dict(file=r["file"], old=old[r["file"]]["ratio"]["ratio"], new=r["ratio"]["ratio"])
                       for r in common if abs(r["ratio"]["ratio"] - old[r["file"]]["ratio"]["ratio"]) > 1e-8],
        same_ratio_complete=sum(r["ratio"]["complete"] == old[r["file"]]["ratio"]["complete"] for r in common),
        thm3_same_q=sum(abs(r["thm3"]["q"] - old[r["file"]]["thm3"]["q"]) < 1e-12
                       for r in common if "q" in r.get("thm3", {}) and "q" in old[r["file"]].get("thm3", {})),
        thm3_common_values=sum("q" in r.get("thm3", {}) and "q" in old[r["file"]].get("thm3", {}) for r in common))
    report["run_agreement"]["gurobi"] = {str(k): dict(
        same_status=sum(r[f"grb{k}"]["status"] == old[r["file"]][f"grb{k}"]["status"] for r in common),
        max_incumbent_q_difference=max(abs(r[f"grb{k}"]["q"] - old[r["file"]][f"grb{k}"]["q"])
                                      for r in common if r[f"grb{k}"]["q"] is not None and old[r["file"]][f"grb{k}"]["q"] is not None))
        for k in (1, 3, 10)}
    loads = [float(l.split()[1]) for l in (LOG / "machine_load_run2.txt").read_text().splitlines()]
    report["load"] = dict(samples=len(loads), one_minute=dist(loads), first=(LOG / "machine_load_run2.txt").read_text().splitlines()[0],
                         last=(LOG / "machine_load_run2.txt").read_text().splitlines()[-1])
    points = [r for f in LOG.glob("points_*.jsonl") for r in read(f)]
    by = collections.defaultdict(dict)
    for r in points:
        if "stage" in r:
            by[r["name"]][r["stage"]] = r
    report["points"] = dict(records=len(points), instances=len(by), stage_counts=counts(r.get("stage", "error") for r in points),
        errors=[r for r in points if "error" in r], face_failures=[dict(name=r["name"], stage=r["stage"], status=r["status"])
                                                               for r in points if "rank" not in r and "stage" in r],
        root_inaccurate=sum(d["root"]["status"] != "optimal" for d in by.values()),
        cut_inaccurate=sum(d["cut"]["status"] != "optimal" for d in by.values()),
        cut_last_violations=sum(d["cut"]["hist"][-1]["nviol"] > 0 for d in by.values()),
        rank1_final=sum(d["cut"]["rank"]["1e-05"] == 1 for d in by.values()),
        root_boundary=dist(d["root"]["eig"][d["root"]["rank"]["1e-05"]] /
                           d["root"]["eig"][d["root"]["rank"]["1e-05"] - 1] for d in by.values()),
        open_face_same_ranks=all(d[s]["rank"][t] == d["cut"]["rank"][t] for name, d in by.items() if name in opened
                                 for s in ("cut_trace", "cut_rand") for t in ("0.001", "1e-05")),
        open_second_eigenvalue=dist(d["cut"]["eig"][1] for name, d in by.items() if name in opened))
    assert report["points"]["cut_last_violations"] == 0
    report["bt_loops"] = {}
    opt = {r["name"]: r for r in read(LOG / "opt_gurobi.jsonl")}
    for setname in ("BT10", "BT20"):
        rr = read(LOG / f"loop_bt_{setname}.jsonl")
        fam = {r["name"]: r for r in read(LOG / f"loop_btfam_{setname}.jsonl")}
        hh = [h for r in rr for h in r["hist"]]
        gen = [h for h in hh if max(h["fam_viol"].values()) <= 1e-6 and h["ratio"] > 1e-6]
        value = lambda r: r["opt"] if r["opt"] is not None else opt[r["name"]]["best"]
        closures = lambda rs: [100 * (r["final"] - r["root"]) / (value(r) - r["root"])
                               for r in rs if value(r) - r["root"] > 1e-7]
        report["bt_loops"][setname] = dict(records=len(rr), calls=len(hh), complete=sum(h["ratio_complete"] for h in hh),
            negative_ratio_times=sum(h["ratio_time"] < 0 for h in hh),
            cap_rounds=sum(r["rounds"] == 150 for r in rr), closure_mean=st.mean(closures(rr)),
            family_closure_mean=st.mean(closures(fam.values())), general_only_rounds=len(gen),
            ratio_times=dist(h["ratio_time"] for h in hh), general_violations=dist(-h["ratio_q"] for h in gen if h["ratio_q"] is not None),
            general_support=dist(h["ratio_supp"] for h in gen), general_vmax=dist(h["ratio_vmax"] for h in gen),
            general_support_le3=sum(h["ratio_supp"] <= 3 for h in gen),
            visited_rank=dist(h["rank"]["1e-05"] for h in hh), final_rank=dist(r["final_rank"]["1e-05"] for r in rr))
        if setname == "BT10":
            earlier = {r["name"]: r for r in read(LOG / "loop_bt_BT10_firstrun.jsonl")}
            report["bt_loops"][setname]["repeat_final_difference"] = max(abs(r["final"] - earlier[r["name"]]["final"]) for r in rr)
    report["dm_loops"] = {}
    opt = {r["name"]: r for r in read(LOG / "opt_gurobi.jsonl")}
    for mode in ("dmfam", "dmplus"):
        rr = read(LOG / f"loop_{mode}_open.jsonl")
        assert {r["name"] for r in rr} == opened and len(rr) == 12
        report["dm_loops"][mode] = []
        for r in rr:
            hh = r["hist"]
            gen = [h for h in hh if max(h["fam_viol"].values()) <= 1e-6 and h["ratio"] > 1e-6]
            gap = lambda b: 100 * (opt[r["name"]]["best"] - b) / abs(opt[r["name"]]["best"])
            report["dm_loops"][mode].append(dict(name=r["name"], rounds=r["rounds"], stopped=r["stopped"], time=r["time"],
                final=r["final"], gap=gap(r["final"]), original_gap=gap(by[r["name"]]["cut"]["obj"]), final_rank=r["final_rank"]["1e-05"],
                ratio_times=dist(h["ratio_time"] for h in hh), incomplete=sum(not h["ratio_complete"] for h in hh),
                general_only_rounds=len(gen), general_support=dist(h["ratio_supp"] for h in gen),
                general_vmax=dist(h["ratio_vmax"] for h in gen), general_violations=dist(-h["ratio_q"] for h in gen)))
    hard = read(LOG / "hard_run2.jsonl")
    oldhard = {(r["kind"], r["q"], r["n"], r["planted"]): r for r in read(LOG / "run1_highload/hard.jsonl")}
    assert len(hard) == len(oldhard) == 88
    complete = [r for r in hard if r["enum"]["complete"]]
    cor = [r for r in hard if r["kind"] == "cor5"]
    large = [r for r in cor if r["N"] >= 47]
    report["hard"] = dict(records=len(hard), completed_enum=len(complete),
        max_completed_error=max(abs(r["enum"]["q"] - r["predicted_min_q"]) for r in complete),
        first_run_enum_max_difference=max(abs(r["enum"]["q"] - oldhard[(r["kind"], r["q"], r["n"], r["planted"])]["enum"]["q"]) for r in hard),
        small_support_detected_q_ge3=sum(max(r[f"fam{k}"]["max_viol"] for k in (1, 2, 3)) > 1e-10 for r in hard if r["q"] >= 3),
        large_cor5_records=len(large), large_cor5_grb_nonoptimal=sum(not r["grb1"]["status"].startswith("Optimal") for r in large),
        cor5_N_ge18_max_violation=max(-r["predicted_min_q"] for r in cor if r["N"] >= 18),
        cor5_N_ge62_max_violation=max(-r["predicted_min_q"] for r in cor if r["N"] >= 62),
        both_finish_scip_over_grb=dist(r["scip1"]["time"] / r["grb1"]["time"] for r in hard
            if "scip1" in r and r["scip1"]["status"] == "optimal" and r["grb1"]["status"].startswith("Optimal")),
        cond=dist(r["cond"] for r in hard), long=read(LOG / "hard_long.jsonl"))
    report["long_opt"] = []
    for fname in ("opt_gurobi_long_1.jsonl", "opt_gurobi_long_2.jsonl"):
        for r in read(LOG / fname):
            name = r["name"]
            stages = {r["mode"]: r["final"] for mode in ("dmfam", "dmplus") for r in read(LOG / f"loop_{mode}_open.jsonl") if r["name"] == name}
            stages["cut"] = by[name]["cut"]["obj"]
            report["long_opt"].append(dict(**r, original_incumbent=opt[name]["best"],
                opt_relative_gap=100 * (r["best"] - r["bound"]) / abs(r["best"]),
                remaining_gap_upper={s: 100 * (r["best"] - b) / abs(r["best"]) for s, b in stages.items()}))
    print(json.dumps(report, indent=2))
    (LOG / "audit_closeout.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
