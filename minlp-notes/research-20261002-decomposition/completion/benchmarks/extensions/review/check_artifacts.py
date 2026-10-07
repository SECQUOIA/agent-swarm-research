"""Audit the eleven frozen extension runs; never launch optimization backends.

Artifact/reference checks and each existing certificate replay run sequentially
in separate processes, with a five-second wall limit and a 512 MiB address limit.
Only Python's standard library is used by this independent artifact audit.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import ceil, floor
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FROZEN = BASE / "frozen"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coefficients(model):
    n = len(model["bounds"])
    out = Counter()
    for factor in model["factors"]:
        for value, local in factor["terms"]:
            powers = [0] * n
            for i, exponent in zip(factor["scope"], local):
                powers[i] = exponent
            out[tuple(powers)] += F(value)
    return {p: c for p, c in out.items() if c}


def expected_polynomial(name):
    # Independent expansion of the nonnegative identities recorded in REVIEW.md.
    if name == "integer_polynomial_lattice":
        return {(0, 0, 2): F(-3, 2), (0, 1, 2): F(-3, 2), (0, 2, 2): F(3, 2),
                (1, 0, 2): F(7, 2), (1, 1, 2): F(-1), (2, 0, 2): F(-5, 2)}
    if name == "quartic_zero_growth":
        return {(4,): F(1), (3,): F(-4, 3), (2,): F(2, 3),
                (1,): F(-4, 27), (0,): F(1, 81)}
    if name in ("mixed_sparse_quartic", "polynomial_table_cap"):
        return {(4, 0, 0): F(1), (2, 0, 0): F(-3), (0, 0, 0): F(5),
                (1, 1, 0): F(-2), (0, 2, 0): F(1),
                (0, 0, 2): F(1), (0, 0, 1): F(-2)}
    if name == "irrational_boundary":
        return {(4, 0): F(1), (2, 0): F(-1), (0, 0): F(1, 4),
                (0, 1): F(1), (1, 2): F(1)}
    if name == "weak_boundary":
        return {(2, 0): F(1), (1, 0): F(-1, 2), (0, 0): F(1, 16),
                (0, 1): F(1), (0, 2): F(-1)}
    assert name == "unresolved_symmetric_boundary"
    return {(4,): F(1), (2,): F(-1), (0,): F(1, 4)}


def expected_domain(name):
    if name == "integer_polynomial_lattice":
        return [(F(-3), F(6)), (F(-2), F(7)), (F(1, 3), F(1, 3))], [0, 1]
    if name == "quartic_zero_growth":
        return [(F(0), F(1))], []
    if name in ("mixed_sparse_quartic", "polynomial_table_cap"):
        return [(F(1), F(2)), (F(1), F(2)), (F(0), F(2))], [2]
    if name == "irrational_boundary":
        return [(F(0), F(1))] * 2, []
    if name == "weak_boundary":
        return [(F(0), F(1)), (F(0), F(1, 2))], []
    assert name == "unresolved_symmetric_boundary"
    return [(F(-1), F(1))], []


def value(model, point):
    if model["kind"] == "polynomial":
        return sum(c * prod_power(point, powers) for powers, c in coefficients(model).items())
    n = len(point)
    return F(model["constant"]) + sum(F(model["b"][i]) * point[i] for i in range(n)) + sum(
        F(model["A"][i][j]) * point[i] * point[j] / 2 for i in range(n) for j in range(n))


def prod_power(point, powers):
    out = F(1)
    for x, exponent in zip(point, powers):
        out *= x ** exponent
    return out


def feasible(model, point):
    return len(point) == len(model["bounds"]) and all(F(lo) <= x <= F(hi)
        for x, (lo, hi) in zip(point, model["bounds"])) and all(
        point[i].denominator == 1 for i in model["integers"])


def independent_qp_reference(model):
    """Use concave endpoint reduction, then explicit one/two-variable faces.

    This is separate from corpus.py's general integer-label/stationary-face
    enumeration. Every benchmark integer coordinate is concave, so endpoint
    reduction applies to it as well. The remaining Hessian is positive definite.
    """
    A = [[F(x) for x in row] for row in model["A"]]
    b = list(map(F, model["b"]))
    bounds = [tuple(map(F, pair)) for pair in model["bounds"]]
    n = len(b)
    D = [i for i in range(n) if A[i][i] <= 0]
    C = [i for i in range(n) if i not in D]
    assert set(model["integers"]) <= set(D) and len(C) <= 2
    if len(C) == 2:
        i, j = C
        assert A[i][i] * A[j][j] - A[i][j] ** 2 > 0
    assert all(endpoint.denominator == 1 for i in model["integers"] for endpoint in bounds[i])
    best = None
    witness = None
    candidates = 0
    for labels in product((0, 1), repeat=len(D)):
        for face in product((0, 1, None), repeat=len(C)):
            point = [None] * n
            for i, label in zip(D, labels):
                point[i] = bounds[i][label]
            for i, position in zip(C, face):
                if position is not None:
                    point[i] = bounds[i][position]
            free = [i for i in C if point[i] is None]
            rhs = [-b[i] - sum(A[i][j] * x for j, x in enumerate(point) if x is not None)
                   for i in free]
            if len(free) == 1:
                i = free[0]
                point[i] = rhs[0] / A[i][i]
            elif len(free) == 2:
                i, j = free
                determinant = A[i][i] * A[j][j] - A[i][j] ** 2
                point[i] = (rhs[0] * A[j][j] - A[i][j] * rhs[1]) / determinant
                point[j] = (A[i][i] * rhs[1] - A[i][j] * rhs[0]) / determinant
            if feasible(model, point):
                candidates += 1
                objective = value(model, point)
                if best is None or objective < best:
                    best, witness = objective, point
    assert best is not None
    return {"value": str(best), "point": list(map(str, witness)), "feasible_candidates": candidates}


def normalized_model(model):
    out = {"bounds": [list(map(F, pair)) for pair in model["bounds"]],
           "integers": sorted(model["integers"])}
    if "A" in model:
        out.update(A=[list(map(F, row)) for row in model["A"]], b=list(map(F, model["b"])),
                   constant=F(model["constant"]))
    else:
        out["coefficients"] = coefficients(model)
    return out


def audit():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    manifest = read(FROZEN / "manifest.json")
    assert {key: manifest[key] for key in ("threads", "solver_time_limit_seconds",
        "worker_wall_limit_seconds", "address_space_limit_mib")} == {
        "threads": 1, "solver_time_limit_seconds": 2, "worker_wall_limit_seconds": 5,
        "address_space_limit_mib": 512}
    for relative, expected in manifest["source_sha256"].items():
        assert sha(FROZEN / relative) == expected, relative
    assert set(manifest["source_sha256"]) == {str(p.relative_to(FROZEN)) for p in FROZEN.rglob("*")
        if p.is_file() and p.suffix in (".py", ".json") and p.name != "manifest.json"}
    specs, references = read(FROZEN / "cases.json"), read(FROZEN / "references.json")
    summary = read(BASE / "summary.json")
    rows = summary["results"]
    assert len(rows) == len(specs) == summary["configurations"] == 11
    assert set(specs) == set(references) == {row["case"] for row in rows}
    reference_checks, statuses = {}, Counter()
    for row in rows:
        name = row["case"]
        spec, reference = specs[name], references[name]
        model = spec["model"]
        assert read(BASE / "results" / (name + ".json")) == row
        if model["kind"] == "qp":
            reference_checks[name] = independent_qp_reference(model)
            assert F(reference_checks[name]["value"]) == F(reference["value"])
            x = list(map(F, reference["point"]))
            assert feasible(model, x) and value(model, x) == F(reference["value"])
        else:
            assert coefficients(model) == expected_polynomial(name)
            expected_bounds, expected_integers = expected_domain(name)
            assert [tuple(map(F, pair)) for pair in model["bounds"]] == expected_bounds
            assert model["integers"] == expected_integers
            if name == "integer_polynomial_lattice":
                # The x polynomial is concave; choose x=-3 or 6. For fixed x,
                # the convex y polynomial minimizes at the nearest integers to
                # (3+2x)/6. These four candidates replace corpus's 100 labels.
                candidates = [(F(x), F(y), F(1, 3)) for x in (-3, 6)
                              for y in (floor(F(3 + 2 * x, 6)), ceil(F(3 + 2 * x, 6)))]
                assert all(feasible(model, point) for point in candidates)
                best = min(value(model, point) for point in candidates)
                assert best == F(-53, 6) == F(reference["value"])
                x = list(map(F, reference["point"]))
                assert feasible(model, x) and value(model, x) == best
                reference_checks[name] = {"value": str(best), "feasible_candidates": 4,
                                          "identity_coefficients_checked": True}
            else:
                assert F(reference["value"]) == 0
                reference_checks[name] = {"value": "0", "identity_coefficients_checked": True}
        statuses[row["status"]] += 1
        for key in ("loaded_source_sha256", "checker_loaded_source_sha256"):
            for relative, expected in row.get(key, {}).items():
                assert manifest["source_sha256"][relative] == expected == sha(FROZEN / relative)
        assert row["solver_subprocess"]["returncode"] == 0
        assert 0 <= row["load_and_preprocessing_seconds"] + row["solve_seconds"] <= row["worker_seconds"]
        assert row["worker_seconds"] <= row["solver_subprocess"]["seconds"] < 5
        assert 0 < row["peak_rss_kib"] < 512 * 1024
        certificate_file = row.get("certificate_file")
        if not certificate_file:
            assert name == "unresolved_symmetric_boundary" and row["status"] == "inconclusive"
            assert len(row["attempts"]) == spec["options"]["max_rounds"] == 2
            continue
        path = BASE / "results" / certificate_file
        assert sha(path) == row["certificate_sha256"]
        assert path.stat().st_size == row["certificate_bytes_gzip"]
        with gzip.open(path, "rt") as stream:
            certificate = json.load(stream)
        assert normalized_model(certificate["problem"]) == normalized_model(model)
        assert certificate["problem"]["name"] == name and row["certificate_input_bound"]
        assert certificate["schema"] == row["certificate_schema"]
        check = read(BASE / "results" / (name + ".check.json"))
        assert all(row[key] == val for key, val in check.items())
        assert row["certificate_check"]["valid"] is True
        assert row["checker_subprocess"]["returncode"] == 0
        assert 0 <= row["check_seconds"] <= row["checker_worker_seconds"] <= row["checker_subprocess"]["seconds"] < 5
        assert 0 < row["checker_peak_rss_kib"] < 512 * 1024
        assert row["total_subprocess_seconds"] == row["solver_subprocess"]["seconds"] + row["checker_subprocess"]["seconds"]
        if "lower" in certificate:
            assert row["status"] == certificate["status"]
            lo, hi, gap = (F(certificate[key]) for key in ("lower", "upper", "gap"))
            assert lo <= F(reference["value"]) <= hi and hi - lo == gap >= 0
            assert all(row[key] == certificate[key] for key in ("lower", "upper", "gap", "point"))
            x = list(map(F, certificate["point"]))
            assert feasible(model, x) and value(model, x) == hi
            if row["status"] == "exact":
                assert lo == hi == F(reference["value"])
                if name == "integer_polynomial_lattice":
                    lattice = certificate["integer_lattice"]
                    assert lattice == row["integer_lattice"]
                    assert lattice["denominator"] == 18
                    assert F(lattice["lower_before"]) == F(-71, 8)
                    assert hi - F(lattice["lower_before"]) == F(1, 24) < F(1, 18)
                    assert row["certificate_check"]["nonzero_gap_lattice_stop_checked"]
            elif row["status"] == "certified":
                assert gap <= F(spec["options"]["epsilon"])
        else:
            bounds = [tuple(map(F, pair)) for pair in certificate["face_bounds"]]
            assert bounds[1] == (0, 0)
            lo, hi = bounds[0]
            if name == "irrational_boundary":
                assert 0 <= lo < hi and lo * lo <= F(1, 2) <= hi * hi
            else:
                assert name == "weak_boundary" and lo <= F(1, 4) <= hi
    assert specs["polynomial_table_cap"]["model"] == specs["mixed_sparse_quartic"]["model"]
    assert specs["submodular_cut_cap"]["model"] == specs["mixed_two_cut"]["model"]
    assert specs["polynomial_table_cap"]["options"]["max_table_states"] == 1
    assert specs["submodular_cut_cap"]["options"]["max_cuts"] == 1
    assert statuses == Counter(exact=3, certified=4, table_limit=1, resource_limit=1, unsupported=1, inconclusive=1)
    assert summary["valid_certificate_replays"] == 10 and summary["proof_replay_failures"] == 0
    return {"valid": True, "configurations": 11, "requested_outputs": 7,
            "valid_certificate_replays": 10, "status_counts": dict(statuses),
            "source_hashes_checked": len(manifest["source_sha256"]),
            "independent_references": reference_checks}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--audit-worker":
        print(json.dumps(audit(), sort_keys=True))
        return
    env = dict(os.environ)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--audit-worker"],
                            capture_output=True, text=True, check=True, timeout=5, env=env)
    report = json.loads(result.stdout)
    repeated = []
    # Checkers consume only frozen inputs and existing proofs. No solver runs.
    with tempfile.TemporaryDirectory(prefix="extension-proof-audit-") as directory:
        for row in read(BASE / "summary.json")["results"]:
            if not row.get("certificate_file"):
                continue
            output = Path(directory) / (row["case"] + ".json")
            subprocess.run([sys.executable, str(FROZEN / "run_extensions.py"), "--check-worker",
                "--case", row["case"], "--certificate", str(BASE / "results" / row["certificate_file"]),
                "--output", str(output)], capture_output=True, text=True, check=True, timeout=5, env=env)
            checked = read(output)
            assert checked["certificate_check"] == row["certificate_check"]
            assert checked["checker_loaded_source_sha256"] == row["checker_loaded_source_sha256"]
            repeated.append(row["case"])
    report["independent_repeat_replays"] = repeated
    (HERE / "audit.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: val for key, val in report.items() if key != "independent_references"}, sort_keys=True))


if __name__ == "__main__":
    main()
