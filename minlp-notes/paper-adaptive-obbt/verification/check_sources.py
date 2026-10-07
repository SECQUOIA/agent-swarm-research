#!/usr/bin/env python3
"""Check the manuscript's included files, labels, citations, and unfinished text."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
errors = []
seen = set()
sources = {}


def read_source(path):
    path = path.resolve()
    if path in seen:
        return
    seen.add(path)
    if not path.is_relative_to(ROOT):
        errors.append(f"External TeX input: {path}")
        return
    if not path.is_file():
        errors.append(f"Missing TeX input: {path.relative_to(ROOT)}")
        return
    raw = path.read_text()
    # A percent escaped with a backslash remains ordinary TeX text.
    content = re.sub(r"(?<!\\)%[^\n]*", "", raw)
    sources[path] = content
    for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", content):
        target = ROOT / name
        if not target.suffix:
            target = target.with_suffix(".tex")
        read_source(target)
    for name in re.findall(r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}", content):
        target = ROOT / name
        candidates = [target] if target.suffix else [target.with_suffix(s) for s in (".pdf", ".png", ".jpg", ".eps")]
        if not any(candidate.is_file() for candidate in candidates):
            errors.append(f"Missing figure input: {name}")


read_source(ROOT / "main.tex")
labels = {}
references = []
citations = set()
for path, content in sources.items():
    relative = path.relative_to(ROOT)
    for label in re.findall(r"\\label\s*\{([^}]+)\}", content):
        if label in labels:
            errors.append(f"Duplicate label {label}: {labels[label]}, {relative}")
        labels[label] = relative
    for group in re.findall(r"\\(?:eqref|ref|pageref|[cC]ref|autoref)\*?\s*\{([^}]+)\}", content):
        references.extend((key.strip(), relative) for key in group.split(","))
    for group in re.findall(r"\\cite\w*\*?(?:\s*\[[^\]]*\])*\s*\{([^}]+)\}", content):
        citations.update(key.strip() for key in group.split(","))
    for match in re.finditer(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b|\\pathref\b|run:|file://|/home/", content):
        line = content.count("\n", 0, match.start()) + 1
        errors.append(f"Unfinished text or private reference: {relative}:{line}: {match.group()}")

for label, path in references:
    if label not in labels:
        errors.append(f"Undefined label {label} in {path}")

bib = ROOT / "references.bib"
keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib.read_text()) if bib.is_file() else []
if len(set(keys)) != len(keys):
    errors.append("Duplicate bibliography keys")
for key in sorted(citations - set(keys)):
    errors.append(f"Missing bibliography entry {key}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"SOURCE_CHECK=ok: {len(sources)} TeX files, {len(labels)} labels, {len(citations)} citations")
print("This checks document consistency, not mathematical correctness.")
