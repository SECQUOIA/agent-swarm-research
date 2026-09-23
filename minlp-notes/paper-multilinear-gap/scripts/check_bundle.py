#!/usr/bin/env python3
"""Check local links, exported source identity, and the paper's finite examples.

Requires qpdf for inspection of the PDF's actual link annotations.
"""
from fractions import Fraction
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

# These small arithmetic checks protect the printed table and the attaining
# mixture's boundary cases. They do not prove a general theorem.
examples = [(2, 1, Fraction(3, 2), Fraction(4, 3)),
            (8, 2, Fraction(7, 2), Fraction(16, 7)),
            (16, 3, Fraction(37, 8), Fraction(128, 37)),
            (64, 5, Fraction(219, 32), Fraction(2048, 219))]
for level, cutoff, hull, ratio in examples:
    assert Fraction(level - cutoff + 1, 2 ** (cutoff + 1)) <= 1
    assert 1 <= Fraction(level - cutoff + 2, 2 ** cutoff)
    assert cutoff + Fraction(level - cutoff, 2 ** cutoff) == hull
    assert level / hull == ratio

states_checked = 0
for level in range(2, 17):
    budget = lambda q: Fraction(level - q + 2, 2 ** q)
    cutoffs = [s for s in range(1, level) if budget(s + 1) <= 1 <= budget(s)]
    assert cutoffs
    exact = set()
    for cutoff in cutoffs:
        weight = (1 - budget(cutoff + 1)) / (budget(cutoff) - budget(cutoff + 1))
        assert 0 <= weight <= 1
        total_failures = total_selected = Fraction(0)
        for q, mixture_mass in [(cutoff, weight), (cutoff + 1, 1 - weight)]:
            for threshold in range(level + 1):
                mass = Fraction(1, 2 ** (threshold + 1 if threshold < level else level))
                failures_in_state = 0 if threshold < q else 2 ** (threshold - q + 1)
                selected = sum(min(2 ** j, failures_in_state) for j in range(1, threshold + 1))
                certificate = cutoff * failures_in_state + sum(
                    2 ** (j - cutoff) for j in range(cutoff + 1, threshold + 1))
                assert selected == certificate
                total_failures += mixture_mass * mass * failures_in_state
                total_selected += mixture_mass * mass * selected
                states_checked += 1
        assert total_failures == 1
        hull = cutoff + Fraction(level - cutoff, 2 ** cutoff)
        assert total_selected == hull
        exact.add(hull)
    assert len(exact) == 1

report = {"local_links_checked": link_count,
          "exported_files_checked": len(manifest["canonical_files_sha256"]),
          "table_rows_checked": len(examples), "cutoff_states_checked": states_checked,
          "failures": failures}
(root / "verification/bundle-check.json").write_text(json.dumps(report, indent=2) + "\n")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: {link_count} local links, exported source fingerprints, "
      f"{len(examples)} table rows, and {states_checked} cutoff states.")
