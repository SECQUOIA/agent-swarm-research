"""Small dimension sweep and certified affine-recourse preprocessing demo."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter

from corpus import Instance, minimum_degree_decomposition, random_band, value
from run_benchmarks import HERE, SOLVER, digest, worker, write_json

RECOURSE = HERE.parents[1] / "negative-curvature"
sys.path.insert(0, str(RECOURSE))
from check_affine_convex_recourse import family_hessian, family_value, mm, transpose


def family(stiffness, reduced=False, m=2):
    full = family_hessian(m, F(stiffness))
    lift = [[F(i == j) for j in range(2 * m)] for i in range(2 * m)]
    lift += [[F(i == j) for j in range(2 * m)] for i in range(m)]
    core = mm(mm(transpose(lift), full), lift)
    expected = [row[:2 * m] for row in family_hessian(m, F(0))[:2 * m]]
    assert core == expected
    # Verify the full coefficient identity F(z,y)-q(z)=M*||y-u||^2.
    remainder = [[F(0) for _ in range(3 * m)] for _ in range(3 * m)]
    for i in range(m):
        remainder[i][i] = remainder[2 * m + i][2 * m + i] = 2 * stiffness
        remainder[i][2 * m + i] = remainder[2 * m + i][i] = -2 * stiffness
    assert all(full[i][j] == remainder[i][j] + (core[i][j] if i < 2*m and j < 2*m else 0)
               for i in range(3 * m) for j in range(3 * m))
    b = [F(-2, 3)] * m + [F(10, 3)] * m
    name = "affine_reduced" if reduced else f"affine_original_M{stiffness}"
    if not reduced:
        b += [F(0)] * m
    p = Instance(name, core if reduced else full, b, [(F(0), F(1))] * len(b), set(),
                 F(m, 9), "Equation (17), m=2; known elementary optimum zero",
                 "../../negative-curvature/affine-convex-recourse.md")
    # A source formula check independent of BoxQP objective assembly.
    point = [F(i + 1, 3 * m + 1) for i in range(3 * m)]
    if reduced:
        point[2 * m:] = point[:m]
    assert value(p, point[:len(b)]) == family_value(point[:m], point[m:2*m], point[2*m:], stiffness)
    return p


def extra_instances():
    result = {}
    for n in (16, 64, 256):
        p = random_band(f"dimension_path_n{n}", n, 1, 20261002)
        result[p.name] = p
    p = random_band("dimension_width2_n16", 16, 2, 20261002)
    result[p.name] = p
    for stiffness in (1, 100, 1000):
        p = family(stiffness)
        result[p.name] = p
    reduced = family(1, reduced=True)
    result[reduced.name] = reduced
    return result


def run(args):
    args.output.mkdir(parents=True, exist_ok=True)
    paths = [Path(__file__), HERE / "run_benchmarks.py", HERE / "corpus.py",
             SOLVER / "certified_grid.py", SOLVER / "verify_certificate.py",
             RECOURSE / "check_affine_convex_recourse.py"]
    hashes = {str(p.relative_to(HERE.parents[2])): digest(p) for p in paths}
    write_json(args.output / "source_hashes.json", hashes)
    for path in paths:
        (args.output / (path.stem + "_snapshot.py")).write_bytes(path.read_bytes())
    cases = extra_instances()
    configurations = []
    for n in (16, 64, 256):
        for method in ("geometric_pruned", "geometric_unpruned", "scip"):
            configurations.append((f"dimension_path_n{n}", "1/50", method))
    configurations.append(("dimension_width2_n16", "1/50", "geometric_pruned"))
    configurations.extend((name, "1/1000", "geometric_pruned")
                          for name in cases if name.startswith("affine"))
    env = dict(os.environ)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    rows = []
    for name, epsilon, method in configurations:
        output = args.output / (name + "__" + method + ".json")
        command = [sys.executable, str(Path(__file__).resolve()), "--worker",
                   "--case", name, "--epsilon", epsilon, "--method", method,
                   "--time-limit", str(args.time_limit), "--max-table-states",
                   str(args.max_table_states), "--output", str(output)]
        started = perf_counter()
        try:
            completed = subprocess.run(command, env=env, capture_output=True, text=True,
                                       timeout=args.time_limit + 12)
            if completed.returncode:
                row = {"case": name, "epsilon": epsilon, "method": method,
                       "status": "worker_failed", "stderr": completed.stderr[-3000:]}
            else:
                row = json.loads(output.read_text())
        except subprocess.TimeoutExpired:
            row = {"case": name, "epsilon": epsilon, "method": method,
                   "status": "outer_wall_limit"}
        row["subprocess_wall_seconds"] = perf_counter() - started
        if name.startswith("affine") and "lower" in row:
            assert F(row["lower"]) <= 0 <= F(row["upper"])
            row["known_zero_optimum_enclosed"] = True
        write_json(output, row)
        rows.append(row)
        write_json(args.output / "results.json", rows)
        print(name, method, row["status"], f"{row['subprocess_wall_seconds']:.3f}s", flush=True)

    reduced_row = next(row for row in rows if row["case"] == "affine_reduced")
    if "certificate_file" in reduced_row:
        with gzip.open(args.output / reduced_row["certificate_file"], "rt") as stream:
            reduced_certificate = json.load(stream)
        point = tuple(map(F, reduced_certificate["point"]))
        lifted_point = point + point[:2]
        comparisons = []
        for stiffness in (1, 100, 1000):
            original = cases[f"affine_original_M{stiffness}"]
            reconstructed = value(original, lifted_point)
            assert all(F(0) <= x <= F(1) for x in lifted_point)
            assert reconstructed == F(reduced_row["upper"])
            comparisons.append({
                "stiffness": stiffness,
                "identity": "F(u,v,y) = q(u,v) + M*sum_i (y_i-u_i)^2",
                "coefficient_identity_checked_exactly": True,
                "response_feasible_on_entire_core_box": "y=u, both in [0,1]^2",
                "reduced_certificate_file": reduced_row["certificate_file"],
                "transferred_original_lower": reduced_row["lower"],
                "reconstructed_original_point": list(map(str, lifted_point)),
                "reconstructed_original_upper": str(reconstructed),
                "original_certified_gap_after_reduction": reduced_row["gap"]})
        write_json(args.output / "affine_lift_certificates.json", comparisons)
    assert {str(p.relative_to(HERE.parents[2])): digest(p) for p in paths} == hashes, (
        "Source changed during extension benchmark")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--method", default="geometric_pruned")
    parser.add_argument("--epsilon", default="1/50")
    parser.add_argument("--time-limit", type=float, default=2)
    parser.add_argument("--max-table-states", type=int, default=20000)
    parser.add_argument("--output", type=Path, default=HERE / "extension-results")
    args = parser.parse_args()
    if args.worker:
        worker(args, problem=extra_instances()[args.case])
    elif args.run:
        run(args)
    else:
        parser.error("choose --run or --worker")


if __name__ == "__main__":
    main()
