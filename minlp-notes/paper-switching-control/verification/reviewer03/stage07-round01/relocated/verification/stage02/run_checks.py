"""Run all stage 2 checks from bundled artifacts, saving individual logs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / "reference"


def run(script):
    result = subprocess.run([sys.executable, str(script)], cwd=HERE,
                            text=True, capture_output=True)
    (HERE / (script.stem + ".log")).write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"{script.name} failed: see its log")
    return f"PASS {script.name}"


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run without -O: integrity checks require assertions")
    manifest = json.loads((REFERENCE / "origin-manifest.json").read_text())
    for name, record in manifest.items():
        assert hashlib.sha256((REFERENCE / name).read_bytes()).hexdigest() == record["sha256"]
    (HERE / "integrity.log").write_text(f"All {len(manifest)} bundled artifact hashes match their recorded originals.\n")
    scripts = [REFERENCE / name for name in (
        "verify_general_four_block.py", "verify_n4.py", "verify_n5_weighted_pairs.py",
        "verify_n3_counterexample.py", "universal_heavy_certificate.py",
        "audit_universal_heavy.py")]
    scripts.append(HERE / "check_new_results.py")
    scripts.append(HERE / "check_symbolic_quotient.py")
    with ThreadPoolExecutor(max_workers=4) as executor:
        for message in executor.map(run, scripts):
            print(message)
    print("All stage 2 checks passed with frozen local dependencies.")
