"""Separate natural-default pilot for API and callback coverage, not tuning."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    target = HERE / "pilots" / sys.argv[1]
    target.mkdir(parents=True)
    source = target / "source"
    source.mkdir()
    for path in (HERE / "models.py", HERE / "pilot.py", HERE.parent / "solver/adaptive_obbt.py"):
        shutil.copy2(path, source / path.name)
    sys.path.insert(0, str(source))
    from models import synthetic, write_problem
    from adaptive_obbt import Config, solve_problem
    manifest = {"intent": "API, original model validation, natural-default callback coverage",
                "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir() if p.is_file()},
                "config": asdict(Config()), "time_limit": 2, "seed": 0, "generator_seed": 17}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    for family, size in (("packing", 3), ("coupled_squares", 6),
                         ("bilinear_cycle", 5), ("indefinite_qp", 8)):
        p = synthetic(family, size, 17)
        write_problem(p, target / (p.name+".json"))
        started = time.perf_counter()
        outcome = solve_problem(p, policy="adaptive", time_limit=2, seed=0,
                                log_path=str(target / (p.name+".log")), show_output=True)
        point = outcome.get("solution")
        result = {"outcome": outcome, "validation": None if point is None else p.validation(point),
                  "elapsed_seconds": time.perf_counter()-started}
        (target / (p.name+".result.json")).write_text(json.dumps(result, indent=2)+"\n")
        print(json.dumps({"model": p.name, "status": outcome["status"], "seconds": outcome["wall_time"],
                          "lp_calls": outcome["obbt"]["lp_calls"], "tightened": outcome["obbt"]["tightened"]}), flush=True)


if __name__ == "__main__":
    main()
