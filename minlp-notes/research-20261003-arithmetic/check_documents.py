"""Check only this topic's authored documents, links, and LaTeX references."""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
DOCUMENT = ROOT / "document"


def main():
    errors = []
    links = 0
    documents = sorted(ROOT.rglob("*.md")) + sorted(DOCUMENT.rglob("*.tex"))
    for path in documents:
        body = path.read_text()
        name = path.relative_to(ROOT)
        if not body.endswith("\n"):
            errors.append(f"{name}: missing final newline")
        for number, line in enumerate(body.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{name}:{number}: trailing whitespace")
        if path.suffix == ".md":
            if sum(line.startswith("```") for line in body.splitlines()) % 2:
                errors.append(f"{name}: unmatched code fence")
            targets = re.findall(r"\[[^\]\n]*\]\(([^\n]*?)\)", body)
            base = path.parent
        else:
            targets = re.findall(r"\\href\{([^{}]+)\}", body)
            base = DOCUMENT
        for target in targets:
            target = target.strip().strip("<>")
            if urlsplit(target).scheme or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            if target:
                links += 1
                if not (base / target).exists():
                    errors.append(f"{name}: missing local target {target}")

    tex = "\n".join(p.read_text() for p in DOCUMENT.rglob("*.tex"))
    labels = re.findall(r"\\label\{([^{}]+)\}", tex)
    for label in sorted(set(labels)):
        if labels.count(label) > 1:
            errors.append(f"duplicate LaTeX label: {label}")
    for reference in re.findall(r"\\(?:eqref|ref)\{([^{}]+)\}", tex):
        if reference not in labels:
            errors.append(f"undefined LaTeX reference: {reference}")
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)",
                          (DOCUMENT / "references.bib").read_text()))
    citations = re.findall(r"\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^{}]+)\}", tex)
    used = {key.strip() for group in citations for key in group.split(",")}
    for key in sorted(used - keys):
        errors.append(f"undefined bibliography key: {key}")
    for target in re.findall(r"\\input\{([^{}]+)\}", tex):
        if not (DOCUMENT / (target + ".tex")).is_file():
            errors.append(f"missing LaTeX input: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(documents)} documents, {links} local links, "
          f"{len(labels)} LaTeX labels, {len(used)} citation keys")


if __name__ == "__main__":
    main()
