"""Run only topic-22 builds, owned-declaration audits and kernel replay."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
MODULES = json.loads((OUT / "modules.json").read_text())
ENV = dict(os.environ)
ENV["PATH"] = str(Path.home() / ".elan/bin") + os.pathsep + ENV.get("PATH", "")
ENV["LEAN_NUM_THREADS"] = "1"


def run(args, log):
    print("RUN", " ".join(args), flush=True)
    with (OUT / log).open("w") as stream:
        result = subprocess.run(args, cwd=ROOT, env=ENV, stdout=stream,
                                stderr=subprocess.STDOUT, check=False)
    print("EXIT", result.returncode, log, flush=True)
    if result.returncode:
        print((OUT / log).read_text(), flush=True)
        raise SystemExit(result.returncode)


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    discovered = sorted("Formal.MatroidSpectral." + path.stem
                        for path in (ROOT / "Formal/MatroidSpectral").glob("*.lean"))
    if sorted(MODULES) != discovered:
        raise SystemExit("Topic module inventory differs from the source directory.")
    sources = [ROOT / (module.replace(".", "/") + ".lean") for module in MODULES]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing topic sources: {missing}")
    imports = {line.removeprefix("import ").strip()
               for line in (ROOT / "Formal.lean").read_text().splitlines()
               if line.startswith("import ")}
    if set(MODULES) - imports:
        raise SystemExit(f"Topic imports missing: {sorted(set(MODULES) - imports)}")
    helpers = [OUT / "run_checks.py", OUT / "AuditMatroid.lean", OUT / "modules.json",
               OUT / "ExecutionExamples.lean"]
    tracked = sources + helpers
    before = {str(path.relative_to(ROOT)): fingerprint(path) for path in tracked}
    run(["lake", "build", "--wfail", *MODULES], "build.log")
    run(["lake", "env", "lean", str(OUT / "AuditMatroid.lean")], "axioms.log")
    run(["lake", "env", "lean", "-DwarningAsError=true",
         str(OUT / "ExecutionExamples.lean")], "execution-examples.log")
    for module in MODULES:
        run(["lake", "env", "leanchecker", module], "kernel-" + module.split(".")[-1] + ".log")
    after = {str(path.relative_to(ROOT)): fingerprint(path) for path in tracked}
    if before != after:
        raise SystemExit("Topic sources changed during verification; rerun affected checks.")
    record = {"completed_utc": datetime.now(timezone.utc).isoformat(),
              "modules": MODULES, "sources_sha256": after,
              "lean_toolchain": (ROOT / "lean-toolchain").read_text().strip(),
              "lake_manifest_sha256": fingerprint(ROOT / "lake-manifest.json"),
              "checks": ["explicit topic module build with --wfail",
                         "topic-owned declaration axiom sweep",
                         "three original-input execution examples",
                         "individual topic module kernel replay",
                         "topic modules present in canonical root imports"],
              "project_wide_checks": "not run", "ci": "not inspected"}
    (OUT / "manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: {len(MODULES)} topic modules; manifest.json written", flush=True)


if __name__ == "__main__":
    main()
