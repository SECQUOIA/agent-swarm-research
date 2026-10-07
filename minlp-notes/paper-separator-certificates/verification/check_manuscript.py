#!/usr/bin/env python3
"""Check this manuscript's input graph, references, and final build log."""

from collections import Counter
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
seen = set()
errors = []


def read_tex(path):
    if path in seen:
        return
    seen.add(path)
    if not path.is_file():
        errors.append(f"Missing TeX input: {path.relative_to(root)}")
        return
    text = path.read_text()
    if any(ord(char) < 32 and char not in "\n\r\t" for char in text):
        errors.append(f"Control character: {path.relative_to(root)}")
    if any(line != line.rstrip(" \t") for line in text.splitlines()):
        errors.append(f"Trailing whitespace: {path.relative_to(root)}")
    for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
        target = root / name
        if not target.suffix:
            target = target.with_suffix(".tex")
        read_tex(target)


read_tex(root / "main.tex")
texts = [path.read_text() for path in sorted(seen) if path.is_file()]
combined = "\n".join(texts)
labels = re.findall(r"\\label\s*\{([^}]+)\}", combined)
duplicates = [key for key, count in Counter(labels).items() if count > 1]
errors.extend(f"Duplicate label: {key}" for key in duplicates)
refs = set()
for group in re.findall(r"\\(?:[Cc]ref|eqref|ref|pageref|autoref)\*?\s*\{([^}]+)\}", combined):
    refs.update(key.strip() for key in group.split(","))
errors.extend(f"Missing reference label: {key}" for key in sorted(refs - set(labels)))

bib = (root / "references.bib").read_text()
bib_keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib)
errors.extend(f"Duplicate bibliography key: {key}" for key, count in Counter(bib_keys).items() if count > 1)
cites = set()
for group in re.findall(r"\\cite\w*\*?(?:\[[^\]]*\])*\s*\{([^}]+)\}", combined):
    cites.update(key.strip() for key in group.split(","))
errors.extend(f"Missing bibliography key: {key}" for key in sorted(cites - set(bib_keys)))

for match in re.finditer(r"\b(?:TODO|TBD|FIXME|placeholder|ChatGPT|GPT|LLM|Codex)\b|research-20|/home/", combined):
    errors.append(f"Unresolved or internal text: {match.group()}")

log = (root / "build/main.log").read_text(errors="replace")
diagnostics = re.findall(
    r"^(?:.*(?:warning:|warning\s+\(|\boverfull\b|\bunderfull\b).*|! .*)$",
    log,
    re.MULTILINE | re.IGNORECASE,
)
errors.extend(f"Final build diagnostic: {line.strip()}" for line in diagnostics)

if errors:
    print("MANUSCRIPT_CHECK=failed")
    print("\n".join(errors))
    sys.exit(1)
print("MANUSCRIPT_CHECK=ok")
print(f"TeX inputs={len(seen)}; labels={len(labels)}; cited sources={len(cites)}")
print("No missing labels/citations, duplicate identifiers, control characters,")
print("internal placeholders, or final LaTeX diagnostics.")
