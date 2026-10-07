#!/usr/bin/env python3
"""Check the manuscript's source closure, labels, citations, and unfinished text."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def uncomment(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def main():
    errors = []
    texts = {}
    visiting = set()

    def read(path):
        path = path.resolve()
        if path in visiting:
            errors.append(f"Recursive input: {path.relative_to(ROOT)}")
            return
        if path in texts:
            return
        if not path.is_file():
            errors.append(f"Missing input: {path.relative_to(ROOT)}")
            return
        visiting.add(path)
        source = uncomment(path.read_text(encoding="utf-8"))
        texts[path] = source
        for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", source):
            target = ROOT / name
            if not target.suffix:
                target = target.with_suffix(".tex")
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"Input outside submission source: {name}")
                continue
            read(target)
        visiting.remove(path)

    read(ROOT / "main.tex")
    labels = {}
    references = []
    citations = set()
    cite_re = re.compile(
        r"\\cite(?:t|p|alt|alp|author|year|yearpar)?\*?"
        r"(?:\[[^\]]*\])*\s*\{([^}]+)\}"
    )
    unfinished_re = re.compile(
        r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b|"
        r"proof omitted|companion proof|pending review|to be supplied",
        re.IGNORECASE,
    )
    for path, source in texts.items():
        name = str(path.relative_to(ROOT))
        for label in re.findall(r"\\label\s*\{([^}]+)\}", source):
            if label in labels:
                errors.append(f"Duplicate label {label}: {labels[label]}, {name}")
            labels[label] = name
        for group in re.findall(
            r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\*?\s*\{([^}]+)\}",
            source,
        ):
            references.extend((label.strip(), name) for label in group.split(","))
        references.extend(
            (label, name)
            for label in re.findall(r"\\hyperref\[([^\]]+)\]", source)
        )
        for group in cite_re.findall(source):
            citations.update(key.strip() for key in group.split(","))
        for match in unfinished_re.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            errors.append(f"Unfinished text: {name}:{line}: {match.group()}")
        for pattern in ("../research-", "../notes/", "../results/", "/home/"):
            if pattern in source:
                errors.append(f"Repository-dependent link or path in {name}: {pattern}")
    for label, name in references:
        if label not in labels:
            errors.append(f"Undefined reference {label} in {name}")

    bib_path = ROOT / "references.bib"
    if bib_path.is_file():
        bib = bib_path.read_text(encoding="utf-8")
        keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib)
        seen = set()
        for key in keys:
            if key in seen:
                errors.append(f"Duplicate bibliography key: {key}")
            seen.add(key)
        for key in sorted(citations - seen):
            errors.append(f"Missing bibliography key: {key}")
    else:
        errors.append("Missing references.bib")

    for error in errors:
        print(error, file=sys.stderr)
    print(
        f"Manuscript check: {len(texts)} source files, {len(labels)} labels, "
        f"{len(references)} references, {len(citations)} cited works; "
        f"{len(errors)} errors."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
