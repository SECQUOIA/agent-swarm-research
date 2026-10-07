"""Replay retained proofs, or rerun frozen configurations in a temporary directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solve", action="store_true", help="rerun all ten solvers before separate replay")
    args = parser.parse_args()
    frozen = HERE / "frozen"
    manifest = json.loads((frozen / "manifest.json").read_text())
    for name, expected in manifest["source_sha256"].items():
        assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == expected, name
    env = dict(os.environ)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    rows = json.loads((HERE / "summary.json").read_text())["results"]
    replays = 0
    with TemporaryDirectory(prefix="minlp-extension-replay-") as temporary:
        work = Path(temporary)
        for row in rows:
            name = row["case"]
            if args.solve:
                output = work / (name + ".json")
                subprocess.run([sys.executable, str(frozen / "run_extensions.py"), "--solve-worker",
                                "--case", name, "--output", str(output)], check=True, timeout=5, env=env)
                fresh = json.loads(output.read_text())
                assert fresh["status"] == row["status"], (name, fresh["status"], row["status"])
                certificate = work / fresh["certificate_file"] if fresh["certificate_file"] else None
            else:
                certificate = HERE / "results" / row["certificate_file"] if row["certificate_file"] else None
                if certificate is not None:
                    assert hashlib.sha256(certificate.read_bytes()).hexdigest() == row["certificate_sha256"]
            if certificate is not None:
                output = work / (name + ".check.json")
                subprocess.run([sys.executable, str(frozen / "run_extensions.py"), "--check-worker",
                                "--case", name, "--certificate", str(certificate), "--output", str(output)],
                               check=True, timeout=5, env=env)
                assert json.loads(output.read_text())["certificate_check"]["valid"] is True
                replays += 1
    print(json.dumps({"configurations": len(rows), "solvers_rerun": len(rows) if args.solve else 0,
                      "valid_certificate_replays": replays, "source_hashes_checked": len(manifest["source_sha256"])}))


if __name__ == "__main__":
    main()
