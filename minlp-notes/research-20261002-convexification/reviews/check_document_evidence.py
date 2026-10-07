"""Recount report evidence from raw files without importing campaign code."""

from collections import Counter
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def check():
    root = Path(__file__).resolve().parents[1]
    campaign = root / "experiments/campaign-v1"
    records = [json.loads(line) for line in (campaign / "records.jsonl").read_text().splitlines()]
    summary = read(campaign / "summary.json")
    replay = read(campaign / "replay.json")
    assert len(records) == len({r["run_id"] for r in records}) == 316
    assert dict(Counter(r["status"] for r in records)) == summary["status_counts"]
    counts = {}
    for suite in ("synthetic", "holdout", "historical"):
        for mode in ("baseline", "control", "all", "auto"):
            rows = [r for r in records if (r["suite"], r["mode"], r["phase"]) == (suite, mode, "full")]
            solved = [r for r in rows if r["status"] in ("optimal", "gaplimit")]
            assert all(r.get("primal_check", {}).get("passed") is True
                       and r.get("primal_check", {}).get("checked") is True
                       and r.get("returncode") == 0 for r in solved)
            entry = {
                "selected": len(rows),
                "admitted": sum("original_model" in r and r["status"] != "source_model_mismatch" for r in rows),
                "refused": sum(r["status"] == "source_model_mismatch" for r in rows),
                "worker_errors": sum(r["status"] == "worker_error" for r in rows),
                "solved": len(solved),
                "recorded_cuts": sum(len(r.get("cuts", [])) for r in rows),
                "recorded_integration_seconds": sum(r["total_seconds"] + r.get("source_read_seconds", 0)
                                                    for r in rows if "total_seconds" in r),
            }
            assert entry["solved"] == summary["suites"][suite]["modes"][mode]["solved"]
            assert entry["recorded_cuts"] == summary["suites"][suite]["modes"][mode]["cuts"]
            assert abs(entry["recorded_integration_seconds"]
                       - summary["suites"][suite]["modes"][mode]["summed_integration_seconds"]) < 1e-9
            counts[f"{suite}/{mode}"] = entry
    cut_sum = sum(len(r.get("cuts", [])) for r in records)
    assert cut_sum == summary["cuts_all_phases"] == replay["cuts"] == replay["replayed_cuts"] == 1082
    assert len(replay["runs"]) == replay["bound_runs"] == 308
    assert len(replay["omitted_runs"]) == 8
    assert all(r["passed"] for r in replay["runs"])
    assert all(replay["tamper_rejections"].values()) and len(replay["tamper_rejections"]) == 12
    assert {r["run_id"] for r in records if "original_model" in r} == {r["run_id"] for r in replay["runs"]}
    checked = [r for r in records if r.get("primal_check", {}).get("checked")]
    assert len(checked) == 270 and all(r["primal_check"]["passed"] for r in checked)
    assert not any(r.get("reference_check", {}).get(key) is False
                   for r in records for key in ("dual_consistent", "root_dual_consistent"))
    queries = sum((r.get("separation") or {}).get("screen_queries", 0) for r in records)
    skips = sum((r.get("separation") or {}).get("screen_skips", 0) for r in records)
    assert (queries, skips) == (506, 2)
    baseline_roots = {r["name"]: r for r in records
                      if (r["suite"], r["phase"], r["mode"]) == ("holdout", "root", "baseline")}
    root_counts = {}
    for mode in ("all", "auto"):
        outcomes = Counter()
        for r in records:
            if (r["suite"], r["phase"], r["mode"]) != ("holdout", "root", mode):
                continue
            b = baseline_roots[r["name"]]
            if r.get("dual") is None or b.get("dual") is None:
                outcomes["unavailable"] += 1
                continue
            improvement = (r["dual"] - b["dual"]) * (1 if r["sense"] == "min" else -1)
            tolerance = 1e-6 * max(1, abs(r["dual"]), abs(b["dual"]))
            outcomes["better" if improvement > tolerance else "worse" if improvement < -tolerance else "tie"] += 1
        expected = {"better": 3, "tie": 15 if mode == "all" else 14,
                    "worse": 2 if mode == "all" else 3, "unavailable": 4}
        assert dict(outcomes) == expected
        root_counts[mode] = dict(outcomes)
    manifest = read(campaign / "source-manifest.json")
    assert len(manifest) == 101
    for name, digest in manifest.items():
        assert hashlib.sha256((campaign / "snapshot" / name).read_bytes()).hexdigest() == digest, name
    native = read(root / "implementation/native-kernel-benchmark.json")
    assert len(native["rows"]) == 35
    for name, key in (("solver/native_sampling.py", "python_source_sha256"),
                      ("solver/native_sampling.c", "source_sha256")):
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == native[key]
    native_expected = {
        "univariate_square": (5.20, 30.20, 0.17),
        "bivariate_quadratic_5": (30.81, 48.46, 0.64),
        "univariate_quartic": (236.94, 27.76, 8.54),
        "univariate_6": (972.95, 43.51, 22.36),
        "bivariate_24": (6176.34, 390.89, 15.80),
    }
    for r in native["rows"]:
        if r["points"] == 4096 and r["case"] in native_expected:
            assert (round(r["numpy_seconds"]*1e6, 2), round(r["native_seconds"]*1e6, 2),
                    round(r["native_speedup"], 2)) == native_expected[r["case"]]
    return {
        "records": len(records), "mode_counts": counts,
        "recorded_and_replayed_cuts": cut_sum, "model_bound_records": 308,
        "missing_model_and_cut_logs": 8, "rejected_tamper_controls": 12,
        "verified_manifest_entries": len(manifest), "native_benchmark_rows": 35,
        "checked_incumbents": len(checked), "reference_conflicts": 0,
        "screen_queries": queries, "screen_skips": skips,
        "heldout_root_comparisons": root_counts,
        "checks_passed": True,
    }


if __name__ == "__main__":
    result = check()
    output = Path(__file__).with_name("document-evidence-checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("Document evidence recount passed: 316 records, 1082 recorded/replayed cuts, 101 source hashes.")
