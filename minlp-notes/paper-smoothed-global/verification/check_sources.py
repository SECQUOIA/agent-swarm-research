#!/usr/bin/env python3
"""Check the manuscript's source closure, references and unfinished text."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def uncomment(text):
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0]
                     for line in text.splitlines())


def check(root):
    errors = []
    files = {}

    def visit(path):
        resolved = path.resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"External source dependency: {path}")
            return
        if resolved in files:
            return
        if not resolved.is_file():
            errors.append(f"Missing source: {path.relative_to(root)}")
            return
        text = uncomment(resolved.read_text())
        files[resolved] = text
        for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            source = root / name
            if not source.suffix:
                source = source.with_suffix(".tex")
            visit(source)

    visit(root / "main.tex")
    labels = {}
    refs = []
    cites = set()
    bibs = set()
    for path, text in files.items():
        rel = path.relative_to(root)
        for label in re.findall(r"\\label\s*\{([^}]+)\}", text):
            if label in labels:
                errors.append(f"Duplicate label {label}: {labels[label]}, {rel}")
            labels[label] = rel
        for names in re.findall(r"\\(?:ref|eqref|pageref|[Cc]ref|[Cc]refrange)\*?\s*\{([^}]+)\}", text):
            refs.extend((rel, name.strip()) for name in names.split(","))
        for name in re.findall(r"\\[Cc]refrange\*?\s*\{[^}]+\}\s*\{([^}]+)\}", text):
            refs.append((rel, name.strip()))
        for names in re.findall(r"\\cite[a-zA-Z]*\*?(?:\s*\[[^\]]*\])*\s*\{([^}]+)\}", text):
            cites.update(name.strip() for name in names.split(","))
        for names in re.findall(r"\\bibliography\s*\{([^}]+)\}", text):
            bibs.update(name.strip() for name in names.split(","))
        for pattern in [r"\bTODO\b", r"\bFIXME\b", r"\bPLACEHOLDER\b",
                        r"\\(?:todo|missing|draftnote)\b"]:
            if re.search(pattern, text):
                errors.append(f"Unfinished text matching {pattern}: {rel}")
        if re.search(r"(?:/home/|research-20\d{6}/|evidence/(?:reviews|author-reports)/)", text):
            errors.append(f"Internal development path in manuscript: {rel}")
        for name in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]+)\}", text):
            source = root / name
            if source.suffix:
                exists = source.is_file()
            else:
                exists = any(source.with_suffix(ext).is_file()
                             for ext in [".pdf", ".png", ".jpg", ".eps"])
            if not exists:
                errors.append(f"Missing figure {name}: {rel}")
        stack = []
        for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", text):
            kind, env = match.groups()
            if kind == "begin":
                stack.append(env)
            elif not stack or stack.pop() != env:
                errors.append(f"Unmatched environment {env}: {rel}")
        if stack:
            errors.append(f"Unclosed environments {stack}: {rel}")
    for rel, name in refs:
        if name not in labels:
            errors.append(f"Undefined label {name}: {rel}")
    keys = {}
    for name in sorted(bibs):
        path = root / (name + ".bib")
        if not path.is_file():
            errors.append(f"Missing bibliography {path.name}")
            continue
        for key in re.findall(r"@(?!(?:comment|string|preamble)\b)\w+\s*\{\s*([^,\s]+)\s*,",
                              path.read_text(), re.I):
            if key in keys:
                errors.append(f"Duplicate bibliography key {key}")
            keys[key] = path.name
    errors.extend(f"Undefined citation {key}" for key in sorted(cites - keys.keys()))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"SOURCE_CHECK=ok; {len(files)} TeX files; {len(labels)} labels; "
          f"{len(cites)} cited bibliography entries")
    return 0


if __name__ == "__main__":
    sys.exit(check(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT))
