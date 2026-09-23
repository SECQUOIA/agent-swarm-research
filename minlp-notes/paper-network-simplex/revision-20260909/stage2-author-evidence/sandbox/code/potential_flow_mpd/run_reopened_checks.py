"""Replay the bounded potential-flow continuation checks and retain their output.

Run with the minlp-notes environment for the numerical checks. The exact
verifiers are also run with site packages and Python assertions disabled.
These checks supplement the independent proof reviews; they do not implement
or certify the general real-algebraic optimization algorithms.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[1]


def main():
    cases = [
        ("reopened_constraints_exact_checks.py", [], True),
        ("check_reopened_constraints_review.py", [], True),
        ("reopened_weighted_checks.py", [], False),
        ("check_reopened_weighted_review.py", [], False),
        ("reopened_weighted_contraction_checks.py", [], False),
        ("check_reopened_weighted_faces_review.py", [], False),
        ("reopened_joint_weighted_checks.py", [], True),
        ("check_reopened_joint_weighted_review.py", [], False),
        ("check_reopened_joint_weighted_second.py", [], True),
        ("exact_weighted_cactus_checks.py", [], False),
        ("check_exact_weighted_cactus_review.py", [], True),
        ("check_exact_weighted_cactus_arithmetic.py", [], True),
        ("exact_weighted_cactus.py", [str(DIRECTORY / "exact_weighted_cactus_example.json"), "--bits", "80"], True),
        ("check_goal_flow_certificate_review.py", [], True),
        ("check_certified_envelope_review.py", [], True),
        ("check_certified_envelope_review.py", ["--producer"], False),
        ("goal_flow_certificate.py", ["--certificate", str(DIRECTORY / "envelope_certificate_example.json")], True),
        ("certified_envelope_benchmarks.py", [], False),
        ("certified_envelope.py", ["verify", str(DIRECTORY / "certified_envelope_example.json")], True),
    ]
    report = {"python": sys.version, "executable": sys.executable, "checks": []}
    failed = False
    for name, arguments, exact in cases:
        path = DIRECTORY / name
        command = [sys.executable, *(["-S", "-O"] if exact else []), str(path), *arguments]
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=300)
        record = {
            "script": str(path.relative_to(ROOT)),
            "arguments": arguments,
            "isolated_optimized": exact,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "exit_code": result.returncode,
            "seconds": time.monotonic() - started,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        report["checks"].append(record)
        failed |= result.returncode != 0
        print(f"{'PASS' if result.returncode == 0 else 'FAIL'} {name} ({record['seconds']:.2f}s)", flush=True)
    report["passed"] = not failed
    output = DIRECTORY / "reopened_validation.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Saved {output.relative_to(ROOT)}", flush=True)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
