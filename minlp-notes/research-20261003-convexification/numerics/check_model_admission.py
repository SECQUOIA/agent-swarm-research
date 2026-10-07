"""Reproduce admission checks for all seven previously refused applications.

Run with the repository solver environment; this script never optimizes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

PROGRAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROGRAM))
from solver.model import ModelAdmissionError, build_model, read_osil

NAMES = ("syn15m", "cvxnonsep_psig30r", "cvxnonsep_pcon40r", "syn10hfsg",
         "btest14", "ghg_2veh", "chp_partload")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path,
                        default=Path.home()/".cache/minlplib/minlplib/osil")
    parser.add_argument("--output", type=Path,
                        default=PROGRAM/"numerics/model-admission.json")
    args = parser.parse_args()
    records = []
    for name in NAMES:
        path = args.cache/(name+".osil")
        record = {"name": name, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        start = time.perf_counter()
        try:
            built = build_model(read_osil(str(path)))
            data = built.metadata
            record.update(status="admitted", original_variables=len(built.xs),
                          domain_witnesses=sum(g["witness"] is not None for g in data["domain_guards"]),
                          domain_guards=data["domain_guards"],
                          domain_requirements=data["domain_requirements"],
                          proved_domain_requirements=data["proved_domain_requirements"],
                          generic_fallback_rows=data["generic_fallback_rows"],
                          affine_bound_steps=len(data["bound_certificate"]["steps"]))
            built.model.freeProb()
        except ModelAdmissionError as error:
            record.update(status=error.status, diagnostic=error.diagnostic)
        record["build_and_read_seconds"] = time.perf_counter()-start
        records.append(record)
        print(name, record["status"], round(record["build_and_read_seconds"], 3), flush=True)
    files = ["solver/model.py", "solver/bounds.py", "numerics/check_model_admission.py"]
    report = {"schema": "model-admission-v2",
              "purpose": "construction and exact-source admission only; no optimization, feasibility, or performance conclusion",
              "python": sys.version, "models": records,
              "code_sha256": {f: hashlib.sha256((PROGRAM/f).read_bytes()).hexdigest() for f in files}}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    return 0 if all(r["status"] == "admitted" for r in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
