"""Run only topic-21 builds, owned-declaration audits and kernel replay."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
MODULES = json.loads((OUT / "modules.json").read_text())
CLIENTS = [
    "BitFoundationReview.lean", "CoverBoundaryReview.lean",
    "CriteriaReview.lean", "DPBitCostReview.lean", "ExactCriteriaReview.lean",
    "NormalizationReview.lean", "PathTransferReview.lean", "ProfileDPReview.lean",
    "RationalPseudoinverseReview.lean", "RoundingReview.lean",
    "CacheStorageReview.lean", "CoverPreprocessingReview.lean",
    "CriterionSelectorReview.lean", "FactorDataReview.lean",
    "FactorInputExecutionReview.lean", "FactorizationReview.lean",
    "TopologicalMaterializationReview.lean", "WeightedExecutionReview.lean",
    "WholeCoverReview.lean", "CostObserverReview.lean",
]
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
    discovered = {"Formal.DAGSpectral." + path.stem
                  for path in (ROOT / "Formal/DAGSpectral").glob("*.lean")}
    if set(MODULES) != discovered or len(MODULES) != len(set(MODULES)):
        raise SystemExit("modules.json must list every topic module exactly once")
    sources = [ROOT / (module.replace(".", "/") + ".lean") for module in MODULES]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing topic sources: {missing}")
    imports = {line.removeprefix("import ").strip()
               for line in (ROOT / "Formal.lean").read_text().splitlines()
               if line.startswith("import ")}
    if set(MODULES) - imports:
        raise SystemExit(f"Topic imports missing: {sorted(set(MODULES) - imports)}")
    before = {str(path.relative_to(ROOT)): fingerprint(path) for path in sources}
    helpers = [OUT / name for name in
               ["AuditDAGSpectral.lean", "modules.json", "run_checks.py", *CLIENTS]]
    helper_before = {path.name: fingerprint(path) for path in helpers}
    run(["lake", "build", "--wfail", *MODULES], "build.log")
    run(["lake", "env", "lean", str(OUT / "AuditDAGSpectral.lean")], "axioms.log")
    for client in CLIENTS:
        run(["lake", "env", "lean", "-DwarningAsError=true", str(OUT / client)],
            "review-" + Path(client).stem + ".log")
    for module in MODULES:
        run(["lake", "env", "leanchecker", module], "kernel-" + module.split(".")[-1] + ".log")
    after = {str(path.relative_to(ROOT)): fingerprint(path) for path in sources}
    if before != after:
        raise SystemExit("Topic sources changed during verification; rerun affected checks.")
    helper_after = {path.name: fingerprint(path) for path in helpers}
    if helper_before != helper_after:
        raise SystemExit("Verification clients changed during checks; rerun affected checks.")
    record = {"completed_utc": datetime.now(timezone.utc).isoformat(),
              "modules": MODULES, "sources_sha256": after,
              "verification_sha256": helper_after,
              "lean_toolchain": (ROOT / "lean-toolchain").read_text().strip(),
              "lake_manifest_sha256": fingerprint(ROOT / "lake-manifest.json"),
              "checks": ["explicit topic module build with --wfail",
                         "topic-owned declaration axiom sweep",
                         "preserved independent review clients",
                         "individual topic module kernel replay",
                         "topic modules present in canonical root imports"],
              "project_wide_checks": "not run", "ci": "not inspected"}
    record["review_clients"] = CLIENTS
    (OUT / "manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: {len(MODULES)} topic modules; manifest.json written", flush=True)


if __name__ == "__main__":
    main()
