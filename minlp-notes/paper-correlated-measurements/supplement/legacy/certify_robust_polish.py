"""Recompute a robust certificate using the completed hull-polishing schedule."""

import argparse
import hashlib
import json
from pathlib import Path

from certify_robust_design import certify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("comparison", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)
    comparison = json.loads(args.comparison.read_text(), parse_float=str)
    proposal = dict(record["robust"])
    proposal["selected"] = comparison["hull_polish"]["selected"]
    result = certify(record, proposal)
    result["incumbent_source"] = "completed hull polishing; selected schedule is revalidated and evaluated exactly"
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["dependency_sha256"] = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ("certify_robust_design.py", "certify_noisy_markov.py", "integer_interval_scores.py")}
    result["input_sha256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    result["comparison_sha256"] = hashlib.sha256(args.comparison.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ("n", "fixed_offset", "standardized", "wall_seconds")}))


if __name__ == "__main__":
    main()
