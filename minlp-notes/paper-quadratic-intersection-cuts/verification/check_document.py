#!/usr/bin/env python3
"""Check the submission source graph and manuscript references; no experiments."""

from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
errors = []
visited = set()
texts = {}


def read_tex(path):
    path = path.resolve()
    if path in visited:
        return
    visited.add(path)
    if not path.is_file():
        errors.append(f"Missing input: {path.relative_to(ROOT)}")
        return
    raw = path.read_text(encoding="utf-8")
    # Unescaped percent comments do not contribute references.
    text = re.sub(r"(?<!\\)%[^\n]*", "", raw)
    texts[path] = text
    for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
        target = ROOT / name
        if not target.suffix:
            target = target.with_suffix(".tex")
        read_tex(target)


read_tex(ROOT / "main.tex")
labels = {}
references = []
citations = set()
for path, text in texts.items():
    relative = path.relative_to(ROOT)
    for label in re.findall(r"\\label\s*\{([^}]+)\}", text):
        if label in labels:
            errors.append(f"Duplicate label {label}: {labels[label]}, {relative}")
        labels[label] = relative
    for group in re.findall(
        r"\\(?:[cC]ref|[cC]refrange|ref|eqref|pageref)\*?\s*\{([^}]+)\}", text
    ):
        references.extend((key.strip(), relative) for key in group.split(","))
    for group in re.findall(
        r"\\cite\w*\*?(?:\[[^\]]*\]){0,2}\s*\{([^}]+)\}", text
    ):
        citations.update(key.strip() for key in group.split(","))
    for marker in ("TODO", "FIXME", "PLACEHOLDER", (_PUBLIC_HOME), "not yet written"):
        if marker in text:
            errors.append(f"Unfinished or internal marker {marker!r}: {relative}")
    if any(ord(char) < 32 and char not in "\n\r\t" for char in text):
        errors.append(f"Control character: {relative}")

for key, path in references:
    if key not in labels:
        errors.append(f"Undefined reference {key}: {path}")

bib = ROOT / "references.bib"
if not bib.is_file():
    errors.append("Missing references.bib")
else:
    bib_text = bib.read_text(encoding="utf-8")
    keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text)
    if len(keys) != len(set(keys)):
        errors.append("Duplicate bibliography keys")
    for key in sorted(citations - set(keys)):
        errors.append(f"Undefined citation {key}")

if errors:
    for error in errors:
        print(error)
    print(f"FAIL: {len(errors)} source issues")
    sys.exit(1)

print(f"PASS: {len(texts)} TeX files, {len(labels)} labels, "
      f"{len(references)} references, {len(citations)} cited sources")
