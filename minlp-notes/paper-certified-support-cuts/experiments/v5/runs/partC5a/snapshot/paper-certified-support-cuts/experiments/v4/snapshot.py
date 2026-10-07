"""Freeze the campaign-4 code: the campaign-3 snapshot plus two additions.

Copies every file of the verified campaign-3 snapshot (``../v3/snapshot``,
manifest-checked) into ``v4/snapshot/`` under the same relative paths, applies
the two additions of ``campaign-v4-protocol.md`` (Code) to
``research-20261003-convexification/solver/integration.py`` by exact text
replacement, adds the campaign-4 runner scripts, protocol and the frozen
Part B selection of campaign 3, records the SCIP parameters of every mode
(checked against ``Model.getParams()``), and writes
``source-manifest.json`` with the SHA-256 of every file. Refuses to
overwrite an existing snapshot.

The additions, both off by default:

1. ``Config.row_directions: bool = False``. When True,
   ``RowSeparator._directions`` first yields, for each source side, the
   direction whose block-variable coefficients are that side's affine
   coefficients (exact support of the whole row), then the frozen
   remainder-only direction. This is the code of the post hoc ``v3d``
   variant, guarded by the flag.
2. ``run_instance(..., scip_params=None)``: each item is passed to
   ``model.setParam`` before ``optimize`` in every mode, and the dict is
   recorded in the result as ``scip_params``.
"""
from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import re
import shutil
import sys
import tempfile
import time

from common import (DEPENDENCY_NAME, HERE, PAPER, REPO, RUNNER_FILES, SNAPSHOT, SNAPSHOT_MANIFEST,
                    TOPIC_NAME, V3, V3D, digest, verify_manifest, write_new)

V3_INTEGRATION_SHA256 = "128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210"
INTEGRATION = f"{TOPIC_NAME}/solver/integration.py"

# (old text, new text, expected number of occurrences in the campaign-3 file)
PATCHES = (
    ("    gap_limit: float = 1e-4\n",
     "    gap_limit: float = 1e-4\n"
     "    # Campaign 4: exact whole-row support directions first (post hoc v3d variant).\n"
     "    row_directions: bool = False\n", 1),
    ("            raise ValueError('work limits must be positive integers')\n",
     "            raise ValueError('work limits must be positive integers')\n"
     "        if type(self.row_directions) is not bool:\n"
     "            raise ValueError('row_directions must be a bool')\n", 1),
    ("        for j in range(len(block.sides)):\n"
     "            if self._expired(started): return\n"
     "            direction = [0.]*(d+len(block.sides))\n",
     "        for j in range(len(block.sides)):\n"
     "            if self._expired(started): return\n"
     "            if self.config.row_directions:\n"
     "                # Campaign 4 (post hoc variant of v3d): first the exact support of\n"
     "                # the whole source row, including its affine terms in the block\n"
     "                # variables; then the support of the nonlinear remainder alone.\n"
     "                names = [self.names[i] for i in block.variables]\n"
     "                affine = dict(block.sides[j].affine)\n"
     "                direction = [float(affine.get(name, 0)) for name in names]+[0.]*len(block.sides)\n"
     "                direction[d+j] = 1.\n"
     "                if any(direction[:d]):\n"
     "                    yield tuple(direction)\n"
     "            direction = [0.]*(d+len(block.sides))\n", 1),
    ("                 node_limit=None, config=None, quiet=True):\n"
     "    \"\"\"Run one model; setup and lazy discovery count against total time budget.\"\"\"\n",
     "                 node_limit=None, config=None, quiet=True, scip_params=None):\n"
     "    \"\"\"Run one model; setup and lazy discovery count against total time budget.\n"
     "\n"
     "    scip_params (campaign 4): SCIP parameters set on the model before solving,\n"
     "    in every mode alike; recorded in the result.\n"
     "    \"\"\"\n", 1),
    ("    config = config or Config()\n",
     "    config = config or Config()\n"
     "    scip_params = dict(scip_params or {})\n"
     "    if any(not isinstance(key, str) or key in RUN_INSTANCE_PARAMS for key in scip_params):\n"
     "        raise ValueError('scip_params must have string names not set by run_instance itself')\n", 1),
    ("'config':asdict(config),'scip_version':None,",
     "'config':asdict(config),'scip_params':scip_params,'scip_version':None,", 2),
    ("        if node_limit is not None: model.setParam('limits/nodes',int(node_limit))\n",
     "        if node_limit is not None: model.setParam('limits/nodes',int(node_limit))\n"
     "        for key, value in scip_params.items():\n"
     "            model.setParam(key, value)\n", 1),
    ("                'model_metadata':built.metadata,'config':asdict(config),\n",
     "                'model_metadata':built.metadata,'config':asdict(config),'scip_params':scip_params,\n", 1),
    ("def run_instance(instance_or_path,",
     "RUN_INSTANCE_PARAMS = ('parallel/maxnthreads', 'randomization/randomseedshift', 'limits/gap',\n"
     "                       'limits/nodes', 'limits/time')\n"
     "\n"
     "\n"
     "def run_instance(instance_or_path,", 1),
)


def patched_integration(source_text):
    for old, new, count in PATCHES:
        if source_text.count(old) != count:
            raise SystemExit(f"patch anchor found {source_text.count(old)} times, expected {count}: {old[:60]!r}")
        source_text = source_text.replace(old, new)
    return source_text


def scip_parameter_record():
    """Mode parameters with SCIP's defaults and descriptions, checked against getParams()."""
    sys.path.insert(0, str(HERE))
    import pyscipopt as ps
    from v4_worker import SCIP_PARAMETER_SETS
    model = ps.Model()
    model.hideOutput()
    defaults = model.getParams()
    with tempfile.TemporaryDirectory() as scratch:
        path = os.path.join(scratch, "all.set")
        model.writeParams(path, comments=True, onlychanged=False)
        lines = open(path).read().splitlines()
    descriptions = {}
    for k, line in enumerate(lines):
        match = re.match(r"^([\w/]+) = ", line)
        if match and k >= 2 and lines[k - 1].startswith("# [type:"):
            descriptions[match.group(1)] = {"description": lines[k - 2].lstrip("# "),
                                            "type": lines[k - 1].lstrip("# ")}
    record = {"scip_version": f"{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}",
              "pyscipopt": importlib.metadata.version("pyscipopt"), "sets": {}}
    for name, params in SCIP_PARAMETER_SETS.items():
        entries = {}
        for key, value in params.items():
            if key not in defaults:
                raise SystemExit(f"SCIP has no parameter {key}")
            if defaults[key] == value:
                raise SystemExit(f"{key} = {value!r} is SCIP's default; the mode would not change it")
            model.setParam(key, value)
            if model.getParam(key) != value:
                raise SystemExit(f"SCIP did not accept {key} = {value!r}")
            entries[key] = {"value": value, "default": defaults[key], **descriptions.get(key, {})}
        record["sets"][name] = entries
    model.freeProb()
    return record


def sources():
    """(relative target path, source path) for every snapshot file except the manifest."""
    v3_manifest = json.loads((V3 / "snapshot/source-manifest.json").read_text())
    mismatches = verify_manifest(V3 / "snapshot", v3_manifest)
    if mismatches:
        raise SystemExit("campaign-3 snapshot differs from its manifest: " + ", ".join(mismatches))
    if v3_manifest[INTEGRATION] != V3_INTEGRATION_SHA256:
        raise SystemExit("campaign-3 snapshot integration.py is not the frozen 128fe10b... file")
    pairs = [(relative, V3 / "snapshot" / relative) for relative in sorted(v3_manifest)]
    pairs += [(f"paper-certified-support-cuts/experiments/v4/{name}", HERE / name) for name in RUNNER_FILES]
    pairs += [("paper-certified-support-cuts/experiments/campaign-v4-protocol.md",
               PAPER / "experiments/campaign-v4-protocol.md"),
              ("paper-certified-support-cuts/experiments/v3d/README-diagnostic.md", V3D / "README-diagnostic.md"),
              ("paper-certified-support-cuts/experiments/v3/scan/partB-selection.json",
               V3 / "scan/partB-selection.json")]
    return pairs, v3_manifest


def main():
    pairs, v3_manifest = sources()
    parameters = scip_parameter_record()
    SNAPSHOT.mkdir(exist_ok=False)
    hashes = {}
    for relative, source in pairs:
        target = SNAPSHOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative == INTEGRATION:
            target.write_text(patched_integration(source.read_text()))
        else:
            before = digest(source)
            shutil.copyfile(source, target)
            if digest(target) != before:
                raise SystemExit(f"{source} changed while it was copied")
        hashes[relative] = digest(target)
    for relative, expected in v3_manifest.items():
        if relative != INTEGRATION and hashes[relative] != expected:
            raise SystemExit(f"copied campaign-3 file differs: {relative}")
    write_new(SNAPSHOT / "scip-parameters.json", parameters)
    hashes["scip-parameters.json"] = digest(SNAPSHOT / "scip-parameters.json")
    import gurobipy
    write_new(SNAPSHOT / "snapshot-info.json", {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base": "campaign-3 snapshot ../v3/snapshot (manifest verified)",
        "base_manifest_sha256": digest(V3 / "snapshot/source-manifest.json"),
        "base_integration_sha256": V3_INTEGRATION_SHA256,
        "v3d_integration_sha256": digest(V3D / "snapshot" / INTEGRATION),
        "integration_sha256": hashes[INTEGRATION],
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "packages": {p: importlib.metadata.version(p) for p in
                     ("numpy", "scipy", "sympy", "python-flint", "pyscipopt", "gurobipy")},
        "gurobi_version": ".".join(map(str, gurobipy.gurobi.version())),
        "files": len(hashes)})
    write_new(SNAPSHOT_MANIFEST, hashes)
    print(json.dumps({"snapshot": str(SNAPSHOT), "files": len(hashes),
                      "integration_sha256": hashes[INTEGRATION]}))


if __name__ == "__main__":
    main()
