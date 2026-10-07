"""Refresh only manifest.json from final saved files; never run experiments.

Run after minor-fixes and integration edits, immediately before check_package.py.
The input archive, model pins, maps and historical command catalogue stay intact.
"""
import hashlib
import json
import subprocess

from finish_paths import ROOT, RESEARCH, OUT, SCOPES

EXTRA_FILES = [
    "research-20260922/scouting/minlplib-open-data/osil.py",
    "research-20260929/treewidth-census/census.py",
    "research-20260929/treewidth-census/census_merged.json",
    "research-20260929/open-instances-summary.md",
    "research-20260929/publication/reviews/eg-recheck-review-r1.md",
    "research-20260929/publication/literature/network/report.md",
    "research-20260929/publication/literature/small/report.md",
    "research-20260929/publication/literature/control/report.md",
    "research-20260929/publication/literature/control/sources/MANIFEST.md",
    "research-20260929/publication/literature/network/sources/MANIFEST.md",
    "research-20260929/publication/literature/small/sources/manifest.tsv",
]


def rebuild_manifest():
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    scopes = SCOPES + ["open-instances-scout"]
    files = {p for scope in scopes for p in (RESEARCH / scope).rglob("*")
             if p.is_file() and "__pycache__" not in p.parts and "singular" not in p.parts
             and (str(p.relative_to(ROOT)) in tracked or p.suffix == ".py")}
    files.update(ROOT / path for path in EXTRA_FILES)
    records = [dict(path=str(p.relative_to(ROOT)),
                    sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                    bytes=p.stat().st_size, tracked=str(p.relative_to(ROOT)) in tracked)
               for p in sorted(files)]
    archive = OUT / "inputs/saved-inputs.tar.gz"
    manifest = dict(
        base_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        note="Hashes describe the final working tree, including minor-fixes and integration edits. Rebuild and check immediately before committing.",
        scopes=scopes, extra_files=EXTRA_FILES, files=records,
        archives=[dict(path="inputs/saved-inputs.tar.gz",
                       sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                       members_manifest="inputs/saved-inputs.json")],
        osil_manifest="inputs/osil-models.json")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return len(records)


if __name__ == "__main__":
    print(json.dumps(dict(manifest_files=rebuild_manifest(), experiments_run=0)))
