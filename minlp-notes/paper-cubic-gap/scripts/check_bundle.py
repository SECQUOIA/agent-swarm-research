#!/usr/bin/env python3
"""Check local links and the exported proof source fingerprints.

Requires qpdf for inspection of the PDF's actual link annotations.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
failures = []
link_count = 0


def check_link(base, link):
    global link_count
    parts = urlsplit(link)
    if parts.scheme or not parts.path:
        return
    path = (base / unquote(parts.path)).resolve()
    if not path.is_relative_to(root) or not path.exists():
        failures.append(f"Missing or external local link: {link}")
    link_count += 1


for doc in root.rglob("*.md"):
    if ".lake" in doc.parts:
        continue
    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
        check_link(doc.parent, link)

pdf = json.loads(subprocess.run(["qpdf", "--json", "main.pdf"], cwd=root,
                               check=True, capture_output=True, text=True).stdout)


def visit(value):
    if isinstance(value, dict):
        uri = value.get("/URI")
        if isinstance(uri, str) and uri.startswith("u:"):
            check_link(root, uri[2:])
        for child in value.values():
            visit(child)
    elif isinstance(value, list):
        for child in value:
            visit(child)


visit(pdf)
manifest = json.loads((root / "formal/verification/export.json").read_text())
for rel, expected in manifest["canonical_files_sha256"].items():
    if hashlib.sha256((root / "formal" / rel).read_bytes()).hexdigest() != expected:
        failures.append(f"Exported source differs from recorded canonical fingerprint: {rel}")

report = {"local_links_checked": link_count,
          "exported_files_checked": len(manifest["canonical_files_sha256"]),
          "failures": failures}
(root / "verification/bundle-check.json").write_text(json.dumps(report, indent=2) + "\n")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: {link_count} local links and exported source fingerprints.")
