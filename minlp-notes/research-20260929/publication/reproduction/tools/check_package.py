"""Targeted packaging checks: paths, hashes, syntax, patch replay and result maps.

No solver, experiment, project-wide test or CI query is run.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import ast
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import sys

from finish_paths import ROOT, RESEARCH, OUT
from rebuild_manifest import EXTRA_FILES


def check_manifest(manifest):
    problems = []
    paths = {item["path"] for item in manifest["files"]}
    for path in EXTRA_FILES:
        if path not in paths:
            problems.append(dict(path=path, problem="not inventoried"))
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file():
            problems.append(dict(path=item["path"], problem="missing"))
        else:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != item["sha256"]:
                problems.append(dict(path=item["path"], problem="stale hash",
                                     expected=item["sha256"], actual=actual))
    for item in manifest["archives"]:
        path = OUT / item["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            problems.append(dict(path=item["path"], problem="missing or changed archive"))
    return problems


def check_maps(result_map, audit_map):
    numbers = 0
    for row in result_map + audit_map:
        mapped_paths = set()
        for key in ("scripts", "saved_inputs", "outputs", "inputs", "point_outputs", "special_certificates"):
            for item in row.get(key, []):
                p = Path(item["path"]).expanduser() if item["path"].startswith("~/") else RESEARCH / item["path"]
                assert p.is_file(), f"{row['instance']}: missing mapped file {item['path']}"
                assert hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"], f"Stale map hash: {item['path']}"
                mapped_paths.add(item["path"])
        assert row.get("numeric_evidence"), f"{row['instance']}: missing numeric evidence"
        for item in row["numeric_evidence"]:
            assert item["path"] in mapped_paths, f"Unmapped numeric source: {item['path']}"
            value = item["value"]
            assert isinstance(value, str) and value, f"Empty mapped number: {row['instance']}"
            text = (RESEARCH / item["path"]).read_text()
            # Match the whole numeric token, not a prefix of a different number.
            assert re.search(r"(?<![\w.+-])" + re.escape(value) + r"(?![\w.])", text), (
                f"{row['instance']}: mapped number {value} absent from {item['path']}")
            numbers += 1
    return numbers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checks", nargs="+", choices=["manifest", "maps", "syntax", "patches", "smoke"],
                        default=["manifest", "maps", "syntax", "patches", "smoke"],
                        help="Select targeted groups; the default checks all package groups")
    selected = parser.parse_args().checks
    manifest = json.loads((OUT / "manifest.json").read_text())
    stale = check_manifest(manifest) if "manifest" in selected else []
    if stale:
        print("Stale manifest entries:", file=sys.stderr)
        for item in stale:
            detail = f" (expected {item['expected']}, actual {item['actual']})" if "expected" in item else ""
            print(f"  {item['problem']}: {item['path']}{detail}", file=sys.stderr)
    result_map = json.loads((OUT / "result-map.json").read_text())
    audit_map = json.loads((OUT / "audit-map.json").read_text())
    numbers = check_maps(result_map, audit_map) if "maps" in selected else None
    if "maps" in selected:
        from eg_evidence import check_command_index
        eg_commands = check_command_index(result_map)
    patches = [p for p in sorted(OUT.glob("*/patches/*.patch"))
               if "applied-by-another-track" not in p.name]
    patches.extend(sorted((OUT / "patches").glob("*.patch")))
    paths = sorted({m[1] for p in patches for m in re.finditer(r"^\+\+\+ b/(.+)$", p.read_text(), re.M)})
    syntax_py, syntax_sh = 0, 0
    for path in paths if "syntax" in selected else []:
        p = ROOT / path
        if p.suffix == ".py":
            ast.parse(p.read_text(), filename=path)
            assert (_PUBLIC_HOME) not in p.read_text(), path
            syntax_py += 1
        elif p.suffix == ".sh":
            subprocess.run(["bash", "-n", str(p)], check=True)
            assert (_PUBLIC_HOME) not in p.read_text() and "~/.local/opt/gams" not in p.read_text(), path
            syntax_sh += 1
    extra_syntax = [ROOT / p for p in EXTRA_FILES if p.endswith(".py")]
    extra_syntax += list((RESEARCH / "open-instances-scout").glob("*.py"))
    for p in list((OUT / "tools").glob("*.py")) + extra_syntax if "syntax" in selected else []:
        ast.parse(p.read_text(), filename=str(p.relative_to(ROOT)))
    eg_syntax = 0
    if "syntax" in selected:
        for scope in ("publication/eg-recheck", "publication/reviews/eg-recheck-r1"):
            for p in (RESEARCH / scope).glob("*.py"):
                ast.parse(p.read_text(), filename=str(p.relative_to(ROOT)))
                eg_syntax += 1
    differences = {}
    with tempfile.TemporaryDirectory(prefix="repro-patches-") as temp:
        tree = Path(temp)
        for path in paths if "patches" in selected else []:
            old = subprocess.run(["git", "show", "HEAD:" + path], cwd=ROOT, capture_output=True)
            if old.returncode == 0:
                dst = tree / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(old.stdout)
                dst.chmod((ROOT / path).stat().st_mode & 0o777)
        for patch in patches if "patches" in selected else []:
            for args in (["git", "apply", "--check", "--unsafe-paths", str(patch)],
                         ["git", "apply", "--unsafe-paths", str(patch)]):
                result = subprocess.run(args, cwd=tree, capture_output=True, text=True)
                assert result.returncode == 0, str(patch) + "\n" + result.stderr
        differences = {path: "".join(difflib.unified_diff(
            (tree / path).read_text().splitlines(True), (ROOT / path).read_text().splitlines(True)))
            for path in paths if "patches" in selected and (tree / path).read_bytes() != (ROOT / path).read_bytes()}
        preserved = json.loads((OUT / "logs/non-packaging-working-tree-differences.json").read_text())
        if "patches" in selected:
            assert differences == preserved, "Unexpected difference from the inspected non-packaging changes"
    smoke = json.loads((OUT / "logs/smoke-results.json").read_text())
    if "smoke" in selected:
        from check_eg_relocated import validate_saved_results
        eg_smoke = validate_saved_results()
        from smoke import CHECKS, compare_output
        assert {p["id"] for p in smoke["checks"]} == {p[0] for p in CHECKS}
        assert all(p["exit"] == 0 and p["normalized_match"] and p["successful_main_tree_opens"] == 0
                   and compare_output(p["id"], (OUT / p["output"]).read_text(),
                                      (OUT / p["reference"]).read_text(), Path(smoke["tree"]))[0]
                   for p in smoke["checks"])
    print(json.dumps(dict(manifest_files=len(manifest["files"]), summary_instances=len(result_map),
                          audit_instances=len(audit_map), python_syntax=syntax_py, shell_syntax=syntax_sh,
                          replayed_patches=len(patches) if "patches" in selected else None,
                          patch_outputs_identical=len(paths) - len(differences) if "patches" in selected else None,
                          preserved_non_packaging_differences=list(differences),
                          smoke_checks=len(smoke["checks"]) if "smoke" in selected else None, checked_groups=selected,
                          eg_python_syntax=eg_syntax, eg_smoke_checks=eg_smoke if "smoke" in selected else None,
                          eg_commands=eg_commands if "maps" in selected else None,
                          mapped_numbers=numbers, stale_manifest=stale, all_passed=not stale), indent=2))
    if stale:
        print("Manifest is stale. After all minor-fixes and integration edits, run:\n"
              "python3 research-20260929/publication/reproduction/tools/rebuild_manifest.py\n"
              "python3 research-20260929/publication/reproduction/tools/check_package.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
