"""Outcome-independent, stratified second-campaign selection."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "code/univariate_envelopes"))
from uenv.osil import read_osil


def select():
    previous = REPO / "research-20261002-convexification/experiments"
    old = json.loads((previous / "holdout-selection.json").read_text())
    exclusions = set(old["excluded_names"])
    exclusions.update(p.stem for p in (previous / "campaign-v1/cases").glob("*.json"))
    exclusions.update(e["name"] for e in old["selected"])
    with (REPO / "code/minlp_solver_lab/instances/instancedata.csv").open() as stream:
        metadata = {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}
    eligible, errors = [], []
    for path in sorted((Path.home() / ".cache/minlplib/minlplib/osil").glob("*.osil")):
        name = path.stem
        row = metadata.get(name)
        if name in exclusions or row is None or path.stat().st_size > 250000:
            continue
        if int(row["nvars"]) > 120 or int(row["ncons"]) > 180:
            continue
        if sum(int(row[k]) for k in ("ngennlfunc", "nquadfunc", "npolynomfunc")) == 0:
            continue
        try:
            model = read_osil(str(path))
        except Exception as error:
            errors.append({"name": name, "type": type(error).__name__, "reason": str(error)})
            continue
        finite = sum(math.isfinite(a) and math.isfinite(b) and a < b
                     for a, b in zip(model.var_lb, model.var_ub))
        if finite < 2:
            continue
        integer = int(row["nbinvars"]) + int(row["nintvars"]) > 0
        stratum = ("convex" if row["convex"] == "True" else
                   "nonconvex_integer" if integer else "nonconvex_continuous")
        rank = hashlib.sha256(("convexification-holdout-v2:" + name).encode()).hexdigest()
        eligible.append({"name": name, "stratum": stratum, "rank": rank,
                         "variables": len(model.var_lb), "constraints": len(model.rows) - 1,
                         "finite_nonfixed_variables": finite, "integer": integer,
                         "convex": row["convex"] == "True", "bytes": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "reference_primal": row["primalbound"], "reference_dual": row["dualbound"]})
    eligible.sort(key=lambda r: r["rank"])
    strata = ("convex", "nonconvex_continuous", "nonconvex_integer")
    selected = []
    for stratum in strata:
        candidates = [r for r in eligible if r["stratum"] == stratum]
        if len(candidates) < 10:
            raise ValueError(f"insufficient frozen stratum {stratum}: {len(candidates)}")
        selected.extend(candidates[:10])
    selected.sort(key=lambda r: r["rank"])
    result = {"frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "selection": "First ten per metadata stratum in SHA256(convexification-holdout-v2: + name) order; no new solver outcomes or handler-applicability filter.",
              "limits": {"variables": 120, "constraints": 180, "osil_bytes": 250000,
                         "minimum_finite_nonfixed_variables": 2},
              "excluded_names": sorted(exclusions), "eligible_count": len(eligible),
              "stratum_eligible_counts": {s: sum(r["stratum"] == s for r in eligible) for s in strata},
              "eligible_names_in_rank_order": [r["name"] for r in eligible],
              "parser_errors": errors, "selected": selected}
    (HERE / "holdout-selection.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    output = select()
    print(json.dumps({"eligible": output["eligible_count"],
                      "strata": output["stratum_eligible_counts"],
                      "selected": [r["name"] for r in output["selected"]]}, indent=2))
