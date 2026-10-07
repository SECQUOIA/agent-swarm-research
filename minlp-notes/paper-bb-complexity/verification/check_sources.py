#!/usr/bin/env python3
"""Check static submission dependencies. Run from any directory; no TeX required."""

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIRS = {"evidence", "review", "reviews", "verification", "delivery", "literature"}
GRAPHICS_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps", ".ps")
REF_COMMANDS = {
    "ref", "eqref", "pageref", "autoref", "autopageref", "nameref", "vref", "Vref",
    "cref", "Cref", "cpageref", "Cpageref", "labelcref", "labelcpageref",
    "namecref", "nameCref", "Namecref", "namecrefs", "nameCrefs", "Namecrefs",
}
RANGE_COMMANDS = {"crefrange", "Crefrange", "cpagerefrange", "Cpagerefrange"}
CITE_COMMANDS = {
    "cite", "citet", "citep", "citealt", "citealp", "citeauthor", "citeyear",
    "citeyearpar", "Citet", "Citep", "Citealt", "Citealp", "Citeauthor",
    "citetalias", "citepalias", "nocite", "bibentry", "defcitealias",
    "parencite", "textcite", "autocite", "footcite", "fullcite",
}
# Scan prose for private home-directory paths. Arbitrary drive-letter text
# is ambiguous with mathematical sets such as ``{x:\nabla\phi(x)>0}``.
# Dependency arguments are checked separately and reject all drive paths.
PRIVATE_PATH = (
    r"(?<![\w:/])/(?:home|Users)/|file://|"
    r"(?<!\w)[A-Za-z]:[\\/](?:Users|Documents and Settings|home)[\\/]"
)


def strip_comments(text):
    """Preserve newlines; % starts a comment after an even run of backslashes."""
    lines = []
    for line in text.splitlines(keepends=True):
        for index, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                line = line[:index] + ("\n" if line.endswith("\n") else "")
                break
        lines.append(line)
    return "".join(lines)


def group(text, position, opener="{", closer="}"):
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != opener:
        return None, position
    start = position + 1
    depth = 1
    braces = 0
    quoted = False
    position = start
    while position < len(text):
        char = text[position]
        if char == "\\":
            position += 2
            continue
        if opener != "{":
            if char == '"' and opener == "(" and not braces:
                quoted = not quoted
            if char == "{":
                braces += 1
            elif char == "}":
                braces -= 1
            if braces or quoted or char in "{}":
                position += 1
                continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if not depth:
                return text[start:position], position + 1
        position += 1
    raise ValueError("unclosed argument")


def argument(text, position):
    if position < len(text) and text[position] == "*":
        position += 1
    while True:
        option, end = group(text, position, "[", "]")
        if option is None:
            break
        position = end
    return group(text, position)


@dataclass
class Report:
    root: Path
    files: set = field(default_factory=set)
    dependencies: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    labels: dict = field(default_factory=dict)
    references: list = field(default_factory=list)
    citations: list = field(default_factory=list)
    bib_keys: dict = field(default_factory=dict)

    def manifest(self):
        return {
            "schema_version": 1,
            "entrypoint": "main.tex",
            "files": sorted(self.files),
            "dependencies": sorted(self.dependencies, key=lambda item: (item["from"], item["to"], item["kind"])),
            "errors": self.errors,
        }


def check(root=ROOT):
    root = Path(root).resolve()
    report = Report(root)
    texts = {}
    active = set()
    bibs = set()
    graphics_paths = [Path(".")]

    def local_file(name, source, kind, extensions=(), prefixes=(Path("."),)):
        name = name.strip()
        if (not name or re.search(r"[\\#$\x00\r\n{}]", name)
                or Path(name).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", name)):
            report.errors.append(f"{source}: {kind} needs a literal relative path: {name!r}")
            return None
        allowed = {"TeX input": (".tex",), "bibliography": (".bib",), "graphic": GRAPHICS_EXTENSIONS}.get(kind)
        if allowed and Path(name).suffix and Path(name).suffix.lower() not in allowed:
            report.errors.append(f"{source}: unsupported {kind} extension: {name}")
            return None
        candidates = []
        for prefix in prefixes:
            target = root / prefix / name
            candidates.extend([target] if target.suffix else [target.with_suffix(ext) for ext in extensions] or [target])
        for target in candidates:
            resolved = target.resolve()
            if not resolved.is_relative_to(root):
                report.errors.append(f"{source}: {kind} escapes manuscript directory: {name}")
                return None
            relative = resolved.relative_to(root)
            if PRIVATE_DIRS.intersection(relative.parts) or PRIVATE_DIRS.intersection(resolved.relative_to(root).parts):
                report.errors.append(f"{source}: {kind} points into internal material: {name}")
                return None
            if any(part.is_symlink() for part in (target, *target.parents) if part != root and part.is_relative_to(root)):
                report.errors.append(f"{source}: symlink dependency is not allowed: {name}")
                return None
            if target.is_file():
                relative_name = relative.as_posix()
                report.files.add(relative_name)
                report.dependencies.append({"from": source, "to": relative_name, "kind": kind})
                return resolved
        report.errors.append(f"{source}: missing {kind}: {name}")
        return None

    def read_tex(path, once=False):
        relative = path.relative_to(root).as_posix()
        if relative in active:
            report.errors.append(f"{relative}: cyclic TeX input")
            return
        if once and relative in texts:
            return
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"{relative}: cannot read UTF-8 source: {exc}")
            return
        content = strip_comments(raw)
        texts[relative] = content
        active.add(relative)
        for match in re.finditer(PRIVATE_PATH + "|" + re.escape(str(root)), raw):
            report.errors.append(f"{relative}:{raw.count(chr(10), 0, match.start()) + 1}: private absolute path: {match.group()}")
        for match in re.finditer(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER|XXX)\b|\\(?:todo|fixme|pathref)\b|\brun:", content):
            report.errors.append(f"{relative}:{content.count(chr(10), 0, match.start()) + 1}: unfinished marker: {match.group()}")
        for match in re.finditer(r"\\([A-Za-z]+)", content):
            command = match.group(1)
            relevant = command in REF_COMMANDS | RANGE_COMMANDS | CITE_COMMANDS | {
                "input", "include", "includegraphics", "graphicspath", "label",
                "bibliography", "addbibresource", "bibliographystyle", "documentclass",
                "usepackage", "RequirePackage", "LoadClass", "hyperref",
            }
            if not relevant:
                continue
            location = f"{relative}:{content.count(chr(10), 0, match.start()) + 1}"
            try:
                value, end = argument(content, match.end())
                if value is None and command == "input":
                    token = re.match(r"\s*([^\s{}]+)", content[match.end():])
                    value = token.group(1) if token else None
                if value is None:
                    report.errors.append(f"{location}: cannot parse \\{command} argument")
                    continue
                keys = [key.strip() for key in value.split(",") if key.strip()]
                if command == "hyperref":
                    label, _ = group(content, match.end(), "[", "]")
                    if label is not None:
                        report.references.append((label.strip(), location))
                elif command in {"input", "include"}:
                    child = local_file(value, relative, "TeX input", (".tex",))
                    if child:
                        read_tex(child)
                elif command == "graphicspath":
                    graphics_paths[:] = [Path(".")]
                    position = 0
                    while position < len(value):
                        directory, position = group(value, position)
                        if directory is None:
                            if value[position:].strip():
                                report.errors.append(f"{location}: cannot parse graphicspath")
                            break
                        graphics_paths.append(Path(directory.strip()))
                elif command == "includegraphics":
                    local_file(value, relative, "graphic", GRAPHICS_EXTENSIONS, graphics_paths)
                elif command in {"bibliography", "addbibresource"}:
                    for key in keys:
                        bib = local_file(key, relative, "bibliography", (".bib",))
                        if bib:
                            bibs.add(bib)
                elif command in {"documentclass", "LoadClass", "usepackage", "RequirePackage", "bibliographystyle"}:
                    extension = ".cls" if command in {"documentclass", "LoadClass"} else ".bst" if command == "bibliographystyle" else ".sty"
                    for key in keys:
                        # Installed TeX classes/packages/styles are build requirements, not local files.
                        if (root / (key + extension)).exists():
                            child = local_file(key + extension, relative, "local TeX support")
                            if child and extension != ".bst":
                                read_tex(child, once=True)
                elif command == "label":
                    if value in report.labels:
                        report.errors.append(f"{location}: duplicate label {value!r}; first at {report.labels[value]}")
                    report.labels[value] = location
                elif command in REF_COMMANDS | RANGE_COMMANDS:
                    report.references.extend((key, location) for key in keys)
                    if command in RANGE_COMMANDS:
                        second, _ = group(content, end)
                        if second is None:
                            report.errors.append(f"{location}: missing second range reference")
                        else:
                            report.references.append((second.strip(), location))
                elif command in CITE_COMMANDS:
                    report.citations.extend((key, location) for key in keys if key != "*")
            except ValueError as exc:
                report.errors.append(f"{location}: {exc}")
        active.remove(relative)

    main = local_file("main.tex", "entrypoint", "TeX input")
    if main:
        read_tex(main)
    for bib in sorted(bibs):
        relative = bib.relative_to(root).as_posix()
        try:
            text = bib.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"{relative}: cannot read bibliography: {exc}")
            continue
        # Consume whole entries so keys inside @comment or a field do not count.
        bib_content = strip_comments(text)
        position = 0
        while match := re.search(r"@([A-Za-z]+)\s*([{(])", bib_content[position:]):
            start = position + match.end() - 1
            opener = match.group(2)
            try:
                body, position = group(bib_content, start, opener, "}" if opener == "{" else ")")
            except ValueError as exc:
                report.errors.append(f"{relative}: malformed bibliography entry: {exc}")
                break
            if match.group(1).lower() in {"comment", "preamble", "string"}:
                continue
            key_match = re.match(r"\s*([^,\s]+)\s*,", body)
            if not key_match:
                report.errors.append(f"{relative}: bibliography entry has no key")
                continue
            key = key_match.group(1)
            if key in report.bib_keys:
                report.errors.append(f"{relative}: duplicate bibliography key {key!r}; first in {report.bib_keys[key]}")
            report.bib_keys[key] = relative
        for match in re.finditer(PRIVATE_PATH + r"|\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text):
            report.errors.append(f"{relative}: private path or unfinished marker: {match.group()}")
    for key, location in report.references:
        if key not in report.labels:
            report.errors.append(f"{location}: unresolved internal reference: {key}")
    for key, location in report.citations:
        if key not in report.bib_keys:
            report.errors.append(f"{location}: missing bibliography entry: {key}")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="manuscript directory")
    parser.add_argument("--json", type=Path, help="write dependency report, including errors")
    args = parser.parse_args()
    report = check(args.root)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report.manifest(), indent=2) + "\n", encoding="utf-8")
    for error in report.errors:
        print(error, file=sys.stderr)
    if report.errors:
        return 1
    print(f"SOURCE_CHECK=ok: {len(report.files)} files, {len(report.labels)} labels, {len(report.citations)} citation uses")
    print("Static consistency only; compile the paper and review mathematical claims separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
