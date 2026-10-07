"""Check the manuscript's explicit labels, citations, and unfinished markers."""

from collections import Counter
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
paths = [root / name for name in ("main.tex", "abstract.tex", "macros.tex")]
paths += sorted((root / "sections").glob("*.tex"))
source = "\n".join(path.read_text() for path in paths)
labels = re.findall(r"\\label\{([^}]+)\}", source)
refs = [key for group in re.findall(r"\\(?:[Cc]ref|eqref|ref)\{([^}]+)\}", source)
        for key in group.split(",")]
cites = [key for group in re.findall(r"\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}", source)
         for key in group.split(",")]
bibkeys = re.findall(r"@\w+\s*\{([^,]+),", (root / "references.bib").read_text())
issues = {
    "duplicate_labels": [key for key, count in Counter(labels).items() if count > 1],
    "undefined_references": sorted(set(refs) - set(labels)),
    "missing_citations": sorted(set(cites) - set(bibkeys)),
    "duplicate_bibkeys": [key for key, count in Counter(bibkeys).items() if count > 1],
    "unfinished_markers": re.findall(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", source),
}
print(f"Manuscript files: {len(paths)}; labels: {len(labels)}; cited sources: {len(set(cites))}")
for name, values in issues.items():
    print(f"{name}: {values}")
raise SystemExit(1 if any(issues.values()) else 0)
