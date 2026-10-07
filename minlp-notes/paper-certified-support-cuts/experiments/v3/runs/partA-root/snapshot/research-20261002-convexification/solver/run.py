"""One independent SCIP run, including setup/callback costs in the time budget."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.integration import Config, run_instance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("mode", choices=("baseline", "control", "all", "auto"))
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--node-limit", type=int)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--no-sample-cache", action="store_true")
    parser.add_argument("--no-star-merge", action="store_true")
    parser.add_argument("--build-native-sampler", action="store_true")
    args = parser.parse_args()
    if args.build_native_sampler:
        from solver.native_sampling import build_native
        build_native()
    config = Config(cache_samples=not args.no_sample_cache, merge_stars=not args.no_star_merge)
    result = run_instance(args.path, args.mode, args.time_limit, args.seed,
                          args.node_limit, config, quiet=not args.verbose)
    output = json.dumps(result, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n")
    print(output)


if __name__ == "__main__":
    main()
