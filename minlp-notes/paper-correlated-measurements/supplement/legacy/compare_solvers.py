"""Bounded matched-instance comparison; save every limit and failure."""

from dataclasses import asdict
import argparse
import hashlib
import json
from pathlib import Path
import platform

import gurobipy as gp
import numpy as np
import scipy

from markov_design import (generic_design, reaction_design, exact_objective,
                           enumerate_optimum, solve_oa, solve_relaxation)
from path_oracle import scalar_markov, solve_branch_bound, hull_bound


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--sizes", type=int, nargs="+", default=[12, 24])
    parser.add_argument("--seed", type=int, default=31)
    parser.add_argument("--root-rounds", type=int, default=0)
    parser.add_argument("--split-fraction", type=float, default=0.5)
    args = parser.parse_args()
    report = {"environment": {"python": platform.python_version(),
                "numpy": np.__version__, "scipy": scipy.__version__,
                "gurobi": gp.gurobi.version(), "solver_threads": 1},
              "settings": {"seconds_per_solve": args.seconds,
                "absolute_logdet_gap": 1e-6,
                "dense_noise_split_fraction": args.split_fraction,
                "root_cut_round_limit": args.root_rounds,
                "note": "Synthetic local designs; numerical bounds, not interval certificates"},
              "cases": []}
    report["source_sha256"] = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ("markov_design.py", "path_oracle.py", "compare_solvers.py")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for n in args.sizes:
        for family in ("generic", "reaction"):
            for rho in (0.4, 0.9):
                k = min(5, n // 2)
                design = (generic_design(n=n, p=3, k=k, rho=rho, seed=args.seed)
                          if family == "generic" else reaction_design(n=n, k=k, rho=rho))
                chain = design.chains[0]
                paths = scalar_markov(chain.F, chain.rho, design.prior, chain.sigma**2)
                record = {"family": family, "n": n, "p": 3, "k": k,
                          "rho": rho, "seed": args.seed,
                          "data": {"sensitivity": chain.F.tolist(),
                                   "prior": design.prior.tolist(), "sigma": chain.sigma},
                          "solves": []}
                if n <= 16:
                    record["enumeration"] = enumerate_optimum(design)
                report["cases"].append(record)
                args.output.write_text(json.dumps(report, indent=2) + "\n")
                for formulation in ("dense", "path"):
                    for integer in (False, True):
                        solver = solve_oa if integer else solve_relaxation
                        options = {"time_limit": args.seconds,
                                   "split_fraction": args.split_fraction}
                        if integer:
                            options["root_rounds"] = args.root_rounds
                        try:
                            result = asdict(solver(design, formulation, **options))
                        except Exception as error:
                            result = {"formulation": formulation, "integer": integer,
                                      "status": "exception",
                                      "exception_type": type(error).__name__,
                                      "exception_message": str(error)}
                        record["solves"].append(result)
                        args.output.write_text(json.dumps(report, indent=2) + "\n")
                        print(json.dumps({"case": [family, n, rho],
                                          **{key: result[key] for key in
                                             ("formulation", "integer", "status",
                                              "wall_seconds", "absolute_gap")
                                             if key in result}}), flush=True)
                try:
                    result = solve_branch_bound(paths, k, time_limit=args.seconds)
                    result["original_objective"] = exact_objective(design, result["path"])
                except Exception as error:
                    result = {"status": "exception",
                              "exception_type": type(error).__name__,
                              "exception_message": str(error)}
                result["formulation"] = "count_path_oracle"
                record["solves"].append(result)
                print(json.dumps({"case": [family, n, rho], **result}), flush=True)
                args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
