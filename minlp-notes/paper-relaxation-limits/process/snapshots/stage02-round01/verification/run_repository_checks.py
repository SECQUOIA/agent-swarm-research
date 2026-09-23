"""Replay selected mathematical checks and retain reproducible execution records.

Exact finite checks and numerical checks supplement the manuscript's proofs.
They do not prove statements quantified over arbitrary dimensions or real data.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent / "repository-checks"
CHECKS = {
    "bilinear": ["code/mccormick_degeneracy/audit_cut_identity.py"],
    "global": [
        "code/multilinear_ratio/verify_cubic_bounds.py",
        "code/verify_multilinear_second_order.py",
        "code/multilinear_ratio/verify_cubic_analytic_family.py",
        "code/multilinear_ratio/verify_cubic_two_level.py",
        "code/multilinear_ratio/verify_cubic_rounding_upper.py",
    ],
    "structural": [
        "code/verify_multilinear_variable_radix.py",
        "code/audit-multilinear-feedback-law.py",
        "code/multilinear_frequency_two_verify.py",
        "code/multilinear_convex_cardinality_verify.py",
        "code/audit-positive-box-coefficients.py",
        "code/audit_single_monomial_hardness.py",
    ],
    "spatial": [
        "code/spatial_bb_lower_bound/check_lower_bound.py",
        "code/spatial_bb_lower_bound/check_sdp_rlt_strengthening.py",
        "code/spatial_bb_lower_bound/check_higher_sos.py",
        "code/spatial_bb_lower_bound/check_relative_gap.py",
    ],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("groups", nargs="*", choices=list(CHECKS))
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    OUTPUT.mkdir(exist_ok=True)
    records = []
    for group in args.groups or CHECKS:
        for relative in CHECKS[group]:
            source = ROOT / relative
            start = time.monotonic()
            try:
                result = subprocess.run(
                    [sys.executable, str(source)],
                    cwd=ROOT,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=args.timeout,
                    check=False,
                )
                status, output = result.returncode, result.stdout
            except subprocess.TimeoutExpired as error:
                status = "timeout"
                output = error.stdout or ""
                if isinstance(output, bytes):
                    output = output.decode(errors="replace")
            log = OUTPUT / (source.stem + ".txt")
            log.write_text(output)
            record = {
                "group": group,
                "script": relative,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "status": status,
                "seconds": round(time.monotonic() - start, 3),
                "log": log.name,
            }
            records.append(record)
            print(json.dumps(record), flush=True)
    report = {
        "python": sys.executable,
        "python_version": platform.python_version(),
        "checks": records,
        "interpretation": "Exit status records execution, not universal proof validity.",
    }
    name = "-".join(args.groups) if args.groups else "all"
    (OUTPUT / (name + ".json")).write_text(json.dumps(report, indent=2) + "\n")
    return int(any(record["status"] != 0 for record in records))


if __name__ == "__main__":
    raise SystemExit(main())
