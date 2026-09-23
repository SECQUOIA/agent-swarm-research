#!/usr/bin/env python3
"""Build and audit only the paper's 64 modules, then replay their kernels."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "verification"
ENV = dict(os.environ)
ENV["PATH"] = str(Path.home() / ".elan/bin") + os.pathsep + ENV.get("PATH", "")
ENV["LEAN_NUM_THREADS"] = "1"
EXPECTED_COUNTS = {"27": 178, "28": 158, "29": 248, "30": 93, "31": 232}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, log):
    print("RUN", " ".join(args), flush=True)
    with (OUT / log).open("w") as stream:
        result = subprocess.run(args, cwd=ROOT, env=ENV, stdout=stream,
                                stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        print((OUT / log).read_text(), flush=True)
        raise SystemExit(result.returncode)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "manifest.json").unlink(missing_ok=True)
    modules = json.loads((ROOT / "modules.json").read_text())
    source_record = json.loads((ROOT / "source-manifest.json").read_text())
    if modules != source_record["owned_modules"] or len(set(modules)) != 64:
        raise SystemExit("Owned module list differs from the source manifest.")
    tracked = list(source_record["sources_sha256"])
    tracked += ["Formal.lean", "lean-toolchain", "lakefile.toml", "lake-manifest.json",
                "modules.json", "source-manifest.json", "verify.py"]
    audits = sorted((ROOT / "audits").iterdir())
    audited_modules = []
    for audit in audits:
        audited_modules += json.loads((audit / "modules.json").read_text())
        tracked += [str((audit / n).relative_to(ROOT)) for n in
                    ["modules.json", "AuditAggregation.lean"]]
    if audited_modules != modules:
        raise SystemExit("Audit partitions do not cover precisely the owned modules.")
    before = {name: digest(ROOT / name) for name in tracked}
    for name, expected in source_record["sources_sha256"].items():
        if before[name] != expected:
            raise SystemExit(f"Source fingerprint mismatch: {name}")
    run(["lake", "build", "--wfail", *modules], "build.log")
    for audit in audits:
        number = audit.name[:2]
        log = f"axioms-{number}.log"
        run(["lake", "env", "lean", str(audit / "AuditAggregation.lean")], log)
        expected = f"audited {EXPECTED_COUNTS[number]} topic-{number} declarations"
        if expected not in (OUT / log).read_text():
            raise SystemExit(f"Unexpected owned declaration count in {log}")
    for module in modules:
        run(["lake", "env", "leanchecker", module], f"kernel-{module}.log")
    after = {name: digest(ROOT / name) for name in tracked}
    if before != after:
        raise SystemExit("Inputs changed during verification; rerun.")
    record = {"owned_modules": modules, "owned_declarations": sum(EXPECTED_COUNTS.values()),
              "support_modules": source_record["support_modules"],
              "inputs_sha256": after,
              "allowed_transitive_axioms": ["propext", "Classical.choice", "Quot.sound"],
              "checks": ["explicit 64-module warning-free build", "five owned-declaration transitive axiom audits",
                         "individual owned-module kernel replay", "unchanged input fingerprints"],
              "dependency_scope": "Imported support and Mathlib dependencies are used, not individually replayed.",
              "project_wide_checks": "not run", "ci": "not inspected"}
    (OUT / "manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: 64 modules, 909 owned declarations, 64 kernel replays", flush=True)


if __name__ == "__main__":
    main()
