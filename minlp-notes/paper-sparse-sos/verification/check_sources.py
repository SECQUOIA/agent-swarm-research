#!/usr/bin/env python3
"""Check the inputs, labels, and citations of this manuscript only."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
errors = []
sources = {}


def visit(path):
    path = path.resolve()
    if path in sources:
        return
    if not path.is_relative_to(ROOT):
        errors.append(f"External manuscript input: {path}")
        return
    if not path.is_file():
        errors.append(f"Missing manuscript input: {path.relative_to(ROOT)}")
        return
    text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
    sources[path] = text
    for name in re.findall(r"\\(?:input|include|inputpart)\s*\{([^}]+)\}", text):
        target = ROOT / name
        if not target.suffix:
            target = target.with_suffix(".tex")
        visit(target)


visit(ROOT / "main.tex")
labels = {}
references = set()
citations = set()
bibliographies = set()
for path, text in sources.items():
    relative = path.relative_to(ROOT)
    for label in re.findall(r"\\label\s*\{([^}]+)\}", text):
        if label in labels:
            errors.append(f"Duplicate label {label}: {labels[label]} and {relative}")
        labels[label] = relative
    for group in re.findall(r"\\(?:[Cc]ref|eqref|ref|pageref|autoref)\*?\s*\{([^}]+)\}", text):
        references.update(item.strip() for item in group.split(","))
    for group in re.findall(r"\\(?:cite[a-zA-Z]*|nocite)\*?(?:\s*\[[^\]]*\])*\s*\{([^}]+)\}", text):
        citations.update(item.strip() for item in group.split(",") if item.strip() != "*")
    for group in re.findall(r"\\bibliography\s*\{([^}]+)\}", text):
        bibliographies.update(item.strip() for item in group.split(","))
    for marker in re.finditer(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text):
        line = text.count("\n", 0, marker.start()) + 1
        errors.append(f"Draft marker in {relative}:{line}: {marker.group()}")
    if "/home/" in text or "../research-" in text:
        errors.append(f"Repository-dependent path in {relative}")

keys = set()
for name in sorted(bibliographies):
    path = ROOT / (name if name.endswith(".bib") else name + ".bib")
    if not path.is_file():
        errors.append(f"Missing bibliography: {path.relative_to(ROOT)}")
        continue
    for key in re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", path.read_text()):
        if key in keys:
            errors.append(f"Duplicate bibliography key: {key}")
        keys.add(key)
errors.extend(f"Undefined reference: {label}" for label in sorted(references - labels.keys()))
errors.extend(f"Undefined citation: {key}" for key in sorted(citations - keys))
for error in errors:
    print(error)
print(f"Checked {len(sources)} manuscript inputs, {len(labels)} labels, {len(citations)} cited keys.")
print("SOURCE_CHECK=" + ("failed" if errors else "ok"))
sys.exit(bool(errors))
