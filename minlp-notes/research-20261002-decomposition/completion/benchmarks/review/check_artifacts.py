"""Audit retained phase-two rows, certificates, input binding, and hashes.

This reads saved replay outcomes; it does not count an enclosure replay as a
successful solve and does not repeat solver experiments.
"""
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BENCHMARKS = HERE.parent
sys.path.insert(0, str(BENCHMARKS))
from corpus import cases, value
from constrained_cases import cases as constrained_cases


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    box = cases()
    constrained = constrained_cases()
    result = {}
    for lane in ("baseline", "completed_grid", "completed_exact", "completed_recourse",
                 "completed_constraints", "completed_sets"):
        aggregate = BENCHMARKS / "results" / (lane + ".json")
        if not aggregate.exists():
            continue
        rows = json.loads(aggregate.read_text())
        statuses = Counter()
        checked = 0
        successful = 0
        proofs = 0
        references = 0
        exact_values = 0
        for row in rows:
            name, method = row["case"], row["method"]
            tag = f"{lane}__{name}__{method}"
            assert row == json.loads((aggregate.parent / (tag + ".json")).read_text()), tag
            statuses[row["status"]] += 1
            valid = isinstance(row.get("certificate_check"), dict) and row["certificate_check"].get("valid") is True
            checked += valid
            success = row["status"] in ("certified", "epsilon", "epsilon_optimal", "exact", "infeasible")
            successful += success and valid
            assert abs(row["total_subprocess_seconds"] - row["solve_subprocess_seconds"]
                       - row.get("check_subprocess_seconds", 0)) < 1e-8, tag
            if "certificate_file" not in row:
                assert not valid and not success, tag
                continue
            path = aggregate.parent / row["certificate_file"]
            assert path.stat().st_size == row["certificate_bytes_gzip"], tag
            with gzip.open(path, "rt") as stream:
                certificate = json.load(stream)
            proofs += 1
            if "status" in certificate:
                assert certificate["status"] == row["status"], tag
            if "point" in row:
                assert certificate["point"] == row["point"], tag
            for key in ("lower", "upper"):
                claimed = certificate.get(key, certificate.get("minimum"))
                if row.get(key) is not None:
                    assert claimed is not None and F(claimed) == F(row[key]), tag
                if valid and key in row["certificate_check"]:
                    replayed = row["certificate_check"][key]
                    assert (None if replayed is None else F(replayed)) == (None if row.get(key) is None else F(row[key])), tag
            model = certificate["problem"]
            p = constrained[name][0] if lane == "completed_constraints" else box[name]
            assert model["name"] == name, tag
            assert [list(map(F, vals)) for vals in model.get("A", model.get("H"))] == p.A, tag
            assert list(map(F, model["b"])) == p.b, tag
            assert [tuple(map(F, vals)) for vals in model["bounds"]] == p.bounds, tag
            assert F(model["constant"]) == p.c, tag
            if lane == "completed_constraints":
                original = constrained[name][1]
                assert {int(k): list(map(F, vals)) for k, vals in model["labels"].items()} == original["labels"], tag
                assert [list(map(F, vals)) for vals in model["rows"]] == original["rows"], tag
                assert list(map(F, model["rhs"])) == original["rhs"], tag
                assert model["senses"] == original["senses"], tag
            else:
                assert set(model["integers"]) == p.integers, tag
            if row.get("point") is not None:
                point = tuple(map(F, row["point"]))
                assert all(lo <= x <= hi for x, (lo, hi) in zip(point, p.bounds)), tag
                assert all(point[i].denominator == 1 for i in p.integers), tag
                assert value(p, point) == F(row["upper"]), tag
                if lane == "completed_constraints":
                    assert all(point[i] in labels for i, labels in original["labels"].items()), tag
                    for coefficients, rhs, sense in zip(original["rows"], original["rhs"], original["senses"]):
                        lhs = sum((a * x for a, x in zip(coefficients, point)), F(0))
                        assert lhs == rhs if sense == "==" else lhs <= rhs, tag
            if row.get("lower") is not None and row.get("upper") is not None:
                gap = F(row["upper"]) - F(row["lower"])
                assert gap >= 0, tag
                exact_values += valid and gap == 0
                if "gap" in row:
                    assert gap == F(row["gap"]), tag
                if row["status"] in ("certified", "epsilon", "epsilon_optimal"):
                    assert 0 <= gap <= F(1, 1024), tag
                if "exact_reference" in row:
                    assert F(row["lower"]) <= F(row["exact_reference"]) <= F(row["upper"]), tag
                    references += 1
                if row["status"] == "exact":
                    assert gap == 0 and valid, tag
        manifest = json.loads((aggregate.parent / (lane + "_run_manifest.json")).read_text())
        for name, expected in manifest["source_sha256"].items():
            path = BENCHMARKS / name
            if name in ("run_benchmarks.py", "corpus.py", "constrained_cases.py"):
                archived = ("run_benchmarks_snapshot.py" if lane == "baseline" else "runner_snapshot.py") if name == "run_benchmarks.py" else name.replace(".py", "_snapshot.py")
                path = BENCHMARKS / "frozen" / lane / archived
            elif name in ("cases.json", "constrained_references.json"):
                archived = BENCHMARKS / "frozen" / lane / name.replace(".json", "_snapshot.json")
                if archived.exists():
                    path = archived
            assert digest(path) == expected, (lane, name)
        result[lane] = {"configurations": len(rows), "statuses": dict(statuses),
                        "retained_certificates": proofs, "valid_saved_replays": checked,
                        "successful_solve_and_valid_replay": successful,
                        "exact_reference_enclosures_checked": references,
                        "exact_values_with_valid_replay": exact_values,
                        "input_binding_and_artifact_consistency": True,
                        "run_source_hashes_match": True}
    summary_path = BENCHMARKS / "summary.json"
    if summary_path.exists():
        summary = json.loads(summary_path.read_text())
        mapping = {"runs": "configurations", "valid_replays": "valid_saved_replays",
                   "completed_certifications": "successful_solve_and_valid_replay",
                   "exact_reference_enclosures": "exact_reference_enclosures_checked",
                   "exact_values_certified": "exact_values_with_valid_replay"}
        for lane, counts in result.items():
            for reported, audited in mapping.items():
                assert summary[lane][reported] == counts[audited], (lane, reported)
        for reported, audited in mapping.items():
            assert summary["totals"][reported] == sum(counts[audited] for counts in result.values()), reported
    return result


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
