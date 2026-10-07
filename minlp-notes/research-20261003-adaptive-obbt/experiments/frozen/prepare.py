"""Freeze inputs by a rule defined before the current comparative campaign."""
from __future__ import annotations

import argparse
import collections
import csv
import gzip
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from models import synthetic, write_problem

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "research-20260922/iterated-obbt"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", action="store_true", required=True)
    args = ap.parse_args()
    target = HERE / "frozen"
    if target.exists():
        raise SystemExit("Frozen cohort already exists; refusing to overwrite.")
    target.mkdir()
    (target / "models").mkdir()
    (target / "osil").mkdir()
    metadata_path = OLD / "results/instances.csv"
    history_path = OLD / "results/final_outcomes.csv"
    metadata = {r["name"]: r for r in csv.DictReader(metadata_path.open())}
    baseline = collections.defaultdict(list)
    for r in csv.DictReader(history_path.open()):
        if r["solver"] == "scip" and r["arm"] == "base":
            baseline[r["name"]].append(float(r["total"]))
    candidates = []
    for name, r in metadata.items():
        if (r["in_scope"] == "True" and baseline[name] and min(baseline[name]) >= 5
                and 5 <= float(r["n"]) <= 300 and 1 <= float(r["nnl"]) <= 200
                and float(r["nterms"]) <= 500):
            candidates.append((hashlib.sha256(("adaptive-obbt-v1/"+name).encode()).hexdigest(), name))
    sys.path.insert(0, str(OLD / "code"))
    from qcqp import QCQP
    selected, families = [], set()
    admissions = []
    for h, name in sorted(candidates):
        family = metadata[name]["family"]
        choose = len(selected) < 12 and family not in families
        admissions.append({"name": name, "family": family, "order_hash": h,
                           "historical_min_scip_seconds": min(baseline[name]),
                           "selected": choose})
        if not choose:
            continue
        families.add(family)
        input_path = target / "models" / (name + ".json")
        source = Path.home() / ".cache/minlplib/minlplib/osil" / (name + ".osil")
        with (target / "osil" / (name + ".osil.gz")).open("wb") as out:
            with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0) as gz:
                gz.write(source.read_bytes())
        p = QCQP(name)
        write_problem(p, input_path)
        selected.append({"name": name, "family": family, "kind": "public",
                         "model": str(input_path.relative_to(target)),
                         "model_sha256": sha(input_path), "source_sha256": sha(source),
                         "n": p.n, "m": p.m, "nonlinear_variables": len(p.nlvars)})
    for family, sizes in (("packing", (5, 7)), ("coupled_squares", (12, 24)),
                          ("bilinear_cycle", (12, 20)), ("indefinite_qp", (20, 36))):
        for size in sizes:
            p = synthetic(family, size, 20261003)
            path = target / "models" / (p.name + ".json")
            write_problem(p, path)
            selected.append({"name": p.name, "family": family, "kind": "synthetic",
                             "model": str(path.relative_to(target)), "model_sha256": sha(path),
                             "n": p.n, "m": p.m, "nonlinear_variables": len(p.nlvars)})
    manifest = {"frozen_utc": datetime.now(timezone.utc).isoformat(),
                "arms": ["native", "fixed", "adaptive"], "seeds": [0, 1],
                "time_limit_seconds": 10, "workers": 2, "task_order_seed": 20261003,
                "historical_metadata_sha256": sha(metadata_path),
                "historical_outcomes_sha256": sha(history_path),
                "parser_sha256": sha(OLD / "code/qcqp.py"),
                "generation_sha256": sha(HERE / "models.py"),
                "preparation_sha256": sha(__file__),
                "models": selected, "candidate_admissions": admissions}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
    shutil.copy2(HERE / "PROTOCOL.md", target / "PROTOCOL.md")
    print(json.dumps({"frozen": str(target), "models": len(selected),
                      "manifest_sha256": sha(target / "manifest.json")}))


if __name__ == "__main__":
    main()
