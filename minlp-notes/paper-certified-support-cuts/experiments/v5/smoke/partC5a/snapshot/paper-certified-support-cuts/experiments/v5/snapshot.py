"""Freeze the campaign-5 code: the campaign-4 snapshot plus two additions.

Copies every file of the verified campaign-4 snapshot (``../v4/snapshot``,
manifest ``098bda40...``, integration.py ``35b5a4fd...``) into ``v5/snapshot/``
under the same relative paths, applies the two additions of
``campaign-v5-protocol.md`` (Code) to
``research-20261003-convexification/solver/integration.py`` by exact text
replacement (``PATCHES``), adds the campaign-5 runner scripts and the protocol,
and writes ``source-manifest.json`` with the SHA-256 of every file. The SCIP
parameter record ``scip-parameters.json`` of campaign 4 is copied unchanged
(campaign 5 adds no SCIP parameter; ``v5_worker.SCIP_PARAMETER_SETS`` must equal
it). Refuses to overwrite an existing snapshot.

The additions, both off by default:

1. ``Config.aggregate_directions: bool = False``. When True,
   ``RowSeparator._directions`` first yields, for each block, the *block
   direction*: lambda = 1 for every chosen source side and ``a`` equal to the
   exact sum of these sides' affine coefficients of the block variables
   (rounded once to binary64), i.e. the support of the sum of the block's rows.
   The directions of the mode follow as before.
2. ``Config.star_leaves: int = 0``. When positive, ``discover`` also forms star
   blocks (``star_variable_sets``): for each variable c that occurs in
   admissible two-variable sides together with at least two other variables,
   the block with c and the first ``star_leaves`` of these variables in variable
   order (equal sets kept once), with the first ``star_leaves`` admissible sides
   inside it and its first 2 * ``star_leaves`` + 4 affine domain rows. Star
   blocks precede the other blocks (all count against ``max_blocks``);
   ``discovery['star_blocks']`` records how many were kept. For blocks with
   more than four variables ``_directions`` yields only the block direction
   (if ``aggregate_directions``) and, if ``row_directions``, the whole-row
   direction of every side (also when its affine part in the block variables
   is zero); no remainder, sampling or LP directions. The dimension cap of
   four (``max_dimensions``) is unchanged for all other blocks.

Certification is unchanged: ``support.certify_support`` uses the polytope
enumeration up to dimension four and otherwise falls back to the inherited
kernels, whose constrained-star oracle certifies star blocks (method
``quadratic_star``, replayed by the inherited ``replay_support``).
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import sys
import time

from common import (HERE, PAPER, RUNNER_FILES, SNAPSHOT, SNAPSHOT_MANIFEST, TOPIC_NAME, V4, digest,
                    verify_manifest, write_new)

V4_MANIFEST_SHA256 = "098bda4033b5c159147596844e3c792c90b20ca3bf450823e643bdb2275fa2d6"
V4_INTEGRATION_SHA256 = "35b5a4fd928e123bab987c96b48e3f2c18a07f3599642ebb1ae19e96f91c39b2"
INTEGRATION = f"{TOPIC_NAME}/solver/integration.py"

# (old text, new text, expected number of occurrences in the campaign-4 file)
PATCHES = (
    # 1. Config fields.
    ("    # Campaign 4: exact whole-row support directions first (post hoc v3d variant).\n"
     "    row_directions: bool = False\n",
     "    # Campaign 4: exact whole-row support directions first (post hoc v3d variant).\n"
     "    row_directions: bool = False\n"
     "    # Campaign 5: the block direction first, and star blocks (0 = off).\n"
     "    aggregate_directions: bool = False\n"
     "    star_leaves: int = 0\n", 1),
    # 2. Validation (the dimension cap of four stays for the other blocks).
    ("        if type(self.row_directions) is not bool:\n"
     "            raise ValueError('row_directions must be a bool')\n",
     "        if type(self.row_directions) is not bool:\n"
     "            raise ValueError('row_directions must be a bool')\n"
     "        if type(self.aggregate_directions) is not bool:\n"
     "            raise ValueError('aggregate_directions must be a bool')\n"
     "        if type(self.star_leaves) is not int or self.star_leaves < 0:\n"
     "            raise ValueError('star_leaves must be a nonnegative integer')\n", 1),
    # 3. Star variable sets.
    ("def discover(inst, built, config=Config(), *, deadline=None):\n",
     "def star_variable_sets(admissible, config, *, deadline=None):\n"
     "    \"\"\"Campaign 5: variable sets of the star blocks, by center in variable order.\n"
     "\n"
     "    A center c occurs in admissible two-variable sides together with at least\n"
     "    two other variables; its star has c and the first star_leaves of these\n"
     "    variables in variable order. Equal sets are kept once.\n"
     "    \"\"\"\n"
     "    neighbours = {}\n"
     "    for side in admissible:\n"
     "        _check_discovery_deadline(deadline)\n"
     "        if len(side.variables) == 2:\n"
     "            u, v = side.variables\n"
     "            neighbours.setdefault(u, set()).add(v)\n"
     "            neighbours.setdefault(v, set()).add(u)\n"
     "    stars, kept = [], set()\n"
     "    for center, others in sorted(neighbours.items()):\n"
     "        if len(others) >= 2:\n"
     "            variables = tuple(sorted((center,)+tuple(sorted(others)[:config.star_leaves])))\n"
     "            if variables not in kept:\n"
     "                kept.add(variables)\n"
     "                stars.append(variables)\n"
     "    return stars\n"
     "\n"
     "\n"
     "def discover(inst, built, config=Config(), *, deadline=None):\n", 1),
    # 4. Star blocks first, each with its own caps on sides and domain rows.
    ("    blocks = []\n"
     "    affine_sides = [s for s in sides if s.nonlinear == 0]\n"
     "    for variables in sorted(groups, key=lambda v: (-len(v), v)):\n"
     "        _check_discovery_deadline(deadline)\n"
     "        chosen_list = []\n"
     "        for side in admissible:\n"
     "            _check_discovery_deadline(deadline)\n"
     "            if set(side.variables).issubset(variables):\n"
     "                chosen_list.append(side)\n"
     "                if len(chosen_list) >= config.max_rows_per_block:\n"
     "                    break\n",
     "    blocks = []\n"
     "    affine_sides = [s for s in sides if s.nonlinear == 0]\n"
     "    # Campaign 5: star blocks (star_leaves > 0) precede the other blocks, with\n"
     "    # up to star_leaves sides and 2*star_leaves+4 domain rows each.\n"
     "    stars = star_variable_sets(admissible, config, deadline=deadline) if config.star_leaves else []\n"
     "    entries = [(variables, config.star_leaves, 2*config.star_leaves+4) for variables in stars]\n"
     "    entries += [(variables, config.max_rows_per_block, config.max_domain_rows)\n"
     "                for variables in sorted(groups, key=lambda v: (-len(v), v))]\n"
     "    for variables, max_sides, max_rows in entries:\n"
     "        _check_discovery_deadline(deadline)\n"
     "        chosen_list = []\n"
     "        for side in admissible:\n"
     "            _check_discovery_deadline(deadline)\n"
     "            if set(side.variables).issubset(variables):\n"
     "                chosen_list.append(side)\n"
     "                if len(chosen_list) >= max_sides:\n"
     "                    break\n", 1),
    ("            if len(rows) >= config.max_domain_rows:\n",
     "            if len(rows) >= max_rows:\n", 1),
    ("            stats['block_cap_reached'] = len(groups) > len(blocks)\n",
     "            stats['block_cap_reached'] = len(entries) > len(blocks)\n", 1),
    ("    stats.update(blocks=len(blocks), auto_eligible=sum(b.auto_eligible for b in blocks))\n",
     "    stats.update(blocks=len(blocks), auto_eligible=sum(b.auto_eligible for b in blocks))\n"
     "    if config.star_leaves:\n"
     "        stats['star_blocks'] = min(len(stars), len(blocks))\n", 1),
    # 5. Block direction first; blocks of more than four variables.
    ("    def _directions(self, block, query, started):\n"
     "        d = len(block.variables)\n",
     "    def _directions(self, block, query, started):\n"
     "        d = len(block.variables)\n"
     "        if self.config.aggregate_directions:\n"
     "            # Campaign 5: the block direction, lambda = 1 on every source side and\n"
     "            # a = the sum of these sides' affine coefficients of the block\n"
     "            # variables (the exact support of the sum of the block's rows).\n"
     "            if self._expired(started): return\n"
     "            names = [self.names[i] for i in block.variables]\n"
     "            total = [sum((dict(side.affine).get(name, Q(0)) for side in block.sides), Q(0)) for name in names]\n"
     "            yield tuple(float(c) for c in total)+(1.,)*len(block.sides)\n"
     "        if d > 4:\n"
     "            # Campaign 5: blocks of more than four variables (star blocks) get only\n"
     "            # the block direction and the whole-row directions (no sampling, no LP).\n"
     "            if self.config.row_directions:\n"
     "                names = [self.names[i] for i in block.variables]\n"
     "                for j in range(len(block.sides)):\n"
     "                    if self._expired(started): return\n"
     "                    affine = dict(block.sides[j].affine)\n"
     "                    direction = [float(affine.get(name, 0)) for name in names]+[0.]*len(block.sides)\n"
     "                    direction[d+j] = 1.\n"
     "                    yield tuple(direction)\n"
     "            return\n", 1),
)


def patch_digests():
    """SHA-256 of each patch (old, new, count as JSON) and of the whole patch list."""
    each = [hashlib.sha256(json.dumps(list(p)).encode()).hexdigest() for p in PATCHES]
    return {"patches": each, "all": hashlib.sha256(json.dumps([list(p) for p in PATCHES]).encode()).hexdigest()}


def patched_integration(source_text):
    for old, new, count in PATCHES:
        if source_text.count(old) != count:
            raise SystemExit(f"patch anchor found {source_text.count(old)} times, expected {count}: {old[:60]!r}")
        source_text = source_text.replace(old, new)
    return source_text


def sources():
    """(relative target path, source path) for every snapshot file except the manifest."""
    if digest(V4 / "snapshot/source-manifest.json") != V4_MANIFEST_SHA256:
        raise SystemExit("campaign-4 snapshot manifest is not the frozen 098bda40... file")
    v4_manifest = json.loads((V4 / "snapshot/source-manifest.json").read_text())
    mismatches = verify_manifest(V4 / "snapshot", v4_manifest)
    if mismatches:
        raise SystemExit("campaign-4 snapshot differs from its manifest: " + ", ".join(mismatches))
    if v4_manifest[INTEGRATION] != V4_INTEGRATION_SHA256:
        raise SystemExit("campaign-4 snapshot integration.py is not the frozen 35b5a4fd... file")
    pairs = [(relative, V4 / "snapshot" / relative) for relative in sorted(v4_manifest)]
    pairs += [(f"paper-certified-support-cuts/experiments/v5/{name}", HERE / name) for name in RUNNER_FILES]
    pairs += [("paper-certified-support-cuts/experiments/campaign-v5-protocol.md",
               PAPER / "experiments/campaign-v5-protocol.md")]
    return pairs, v4_manifest


def check_scip_parameters():
    sys.path.insert(0, str(HERE))
    from v5_worker import SCIP_PARAMETER_SETS
    record = json.loads((V4 / "snapshot/scip-parameters.json").read_text())
    recorded = {name: {key: entry["value"] for key, entry in params.items()} for name, params in record["sets"].items()}
    if recorded != SCIP_PARAMETER_SETS:
        raise SystemExit("v5_worker.SCIP_PARAMETER_SETS differs from the campaign-4 record")


def main():
    pairs, v4_manifest = sources()
    check_scip_parameters()
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
    for relative, expected in v4_manifest.items():
        if relative != INTEGRATION and hashes[relative] != expected:
            raise SystemExit(f"copied campaign-4 file differs: {relative}")
    import gurobipy
    write_new(SNAPSHOT / "snapshot-info.json", {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base": "campaign-4 snapshot ../v4/snapshot (manifest verified)",
        "base_manifest_sha256": V4_MANIFEST_SHA256,
        "base_integration_sha256": V4_INTEGRATION_SHA256,
        "integration_sha256": hashes[INTEGRATION],
        "patch_sha256": patch_digests(),
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "packages": {p: importlib.metadata.version(p) for p in
                     ("numpy", "scipy", "sympy", "python-flint", "pyscipopt", "gurobipy")},
        "gurobi_version": ".".join(map(str, gurobipy.gurobi.version())),
        "files": len(hashes)})
    write_new(SNAPSHOT_MANIFEST, hashes)
    print(json.dumps({"snapshot": str(SNAPSHOT), "files": len(hashes),
                      "integration_sha256": hashes[INTEGRATION], "patch_sha256": patch_digests()["all"]}))


if __name__ == "__main__":
    main()
