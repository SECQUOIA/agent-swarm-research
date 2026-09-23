#!/usr/bin/env python3
"""Check source inventory links and the Paper A source inventory and included section coverage."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PATTERNS = (
    "results/potential-flow-*.md",
    "notes/potential-flow-*.md",
    "notes/review-potential-flow-*.md",
    "code/potential_flow_mpd/*.py",
    "code/potential_flow_mpd/*.json",
)
EXTRA_FILES = (
    "results/ac-power-flow-existential-reals.md",
    "notes/fixed-core-convex-leaf-arithmetic-barrier.md",
    "notes/review-fixed-core-block-optimization.md",
    "notes/review-fixed-core-block-optimization-second.md",
)
SECTIONS = {
    "complexity": (
        "00-introduction", "01-preliminaries", "02-cactus", "03-block-rank",
        "04-laws", "05-boundaries", "06-weighted", "07-weighted-cactus",
        "08-design", "09-correlations-energy", "10-weighted-blocks",
        "11-certified-computation", "08-conclusion",
    ),
}


def local_links(path):
    """Read inline and reference-style Markdown links, excluding fenced code."""
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", path.read_text(),
                  flags=re.MULTILINE | re.DOTALL)
    targets = re.findall(r"\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", text)
    targets += re.findall(r"^\s*\[[^\]]+\]:\s*<?([^\s>]+)", text, re.MULTILINE)
    links = set()
    for target in targets:
        url = urlsplit(target)
        if not url.scheme and not url.netloc and url.path:
            links.add((path.parent / unquote(url.path)).resolve())
    return links


def inventory():
    files = {p.resolve() for pattern in PATTERNS for p in REPO.glob(pattern)}
    # Follow direct research-note/result links from the potential-flow corpus.
    # Do not recursively import unrelated programs linked by those dependencies.
    for source in sorted(files):
        if source.suffix == ".md":
            for target in local_links(source):
                if (target.suffix == ".md" and target.is_relative_to(REPO)
                        and target.relative_to(REPO).parts[0] in {"notes", "results"}):
                    files.add(target)
    files.update(REPO / path for path in EXTRA_FILES)
    return files


def main():
    coverage = ROOT / "coverage.md"
    if not coverage.is_file():
        print("Missing coverage.md", file=sys.stderr)
        return 1
    links = local_links(coverage)
    errors = []
    rows = {}
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", coverage.read_text(),
                  flags=re.MULTILINE | re.DOTALL)
    for match in re.finditer(r"^\| \[[^\]]+\]\(([^)]+)\) \| (.*) \|$", text,
                             re.MULTILINE):
        url = urlsplit(match[1])
        if url.scheme or url.netloc or not url.path:
            continue
        source = (ROOT / unquote(url.path)).resolve()
        cells = [cell.strip() for cell in match[2].split(" | ")]
        rows[source] = cells
    section_ids = {f"{letter}{i:02}" for letter, paper in
                   (("A", "complexity"),)
                   for i in range(len(SECTIONS[paper]))}
    for source, cells in rows.items():
        if source.is_relative_to(REPO / "results"):
            if len(cells) != 5:
                errors.append(f"Malformed result row: {source.relative_to(REPO)}")
                continue
            assigned = set(re.findall(r"\b[AB]\d{2}\b", cells[2])) & section_ids
            if not assigned and not cells[3].startswith(("excluded", "superseded by")):
                errors.append(f"Result has no planned section or exclusion: {source.relative_to(REPO)}")
    required = inventory()
    for source in sorted(required):
        if not source.is_file():
            errors.append(f"Missing source: {source.relative_to(REPO)}")
        if source not in rows:
            errors.append(f"Missing inventory row: {source.relative_to(REPO)}")
    planned = {ROOT / paper / "sections" / (stem + ".tex")
               for paper, stems in SECTIONS.items() for stem in stems}
    referenced = {p for p in links if p.suffix == ".tex" and "sections" in p.parts}
    for section in sorted(planned | referenced):
        if not section.is_file():
            errors.append(f"Missing section: {section}")
        if section in planned and section not in links:
            errors.append(f"Missing planned section link: {section.relative_to(ROOT)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(required)} inventory files and {len(planned)} included sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
