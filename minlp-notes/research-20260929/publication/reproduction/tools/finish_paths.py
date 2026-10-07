"""Apply the remaining literal path fixes. No numerical code is changed.

Run from any directory: python3 finish_paths.py
The generated patch records only these additional edits, after the older patches.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import ast
import difflib
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = ROOT / "research-20260929"
OUT = Path(__file__).resolve().parents[1]
SCOPES = [
    "open-instances", "open-instances-wave2", "open-instances-wave3",
    "bound-audit", "theory-bangbang", "reviews/open-instances-verification",
    "reviews/bangbang-verification", "reviews/cops-verification",
    "reviews/catmix-recheck-checks", "reviews/wave2-small-verification",
    "reviews/pindyck-review-checks", "reviews/wave3-verification",
    "reviews/powerflow0039-review-checks", "reviews/ann-extension-review-checks",
    "reviews/eg-retry-review-checks", "reviews/waterno2-verification",
    "reviews/waterno2-recheck", "reviews/waterno2-sepbranch-review-checks",
    "reviews/waterno2-cellslopes-review-checks", "reviews/bound-audit-verification",
    "reviews/bound-audit-recheck", "publication/primal",
    "publication/reviews/primal-chain-r1", "publication/reviews/primal-lnts-r1",
    "publication/reviews/primal-dtoc5-lukvle10-r1",
    "publication/reviews/primal-powerflow-r1",
    "publication/reviews/primal-water-ann-kan-r1",
    "publication/eg-recheck", "publication/reviews/eg-recheck-r1",
]


def main():
    patch = []
    old_root = (_PUBLIC_REPO)
    files = sorted({p for scope in SCOPES for p in (RESEARCH / scope).rglob("*.py")
                    if "singular" not in p.parts})
    files.append(OUT / "cops/scripts/exact_display_checks.py")
    for path in files:
        src = path.read_text()
        new = src
        if path.name == "exact_display_checks.py":
            new = new.replace(('WT = "' + _PUBLIC_REPO + '-clean/research-20260929"'),
                              'WT = os.path.abspath(os.path.join(HERE, "../../../.."))')
        for quote in ('"', "'"):
            new = new.replace(f"f{quote}{old_root}/", f"f{quote}{{_REPRO_ROOT}}/")
            new = new.replace(f"{quote}{old_root}/", f"_REPRO_ROOT + {quote}/")
        if old_root in new:
            raise ValueError(f"Unhandled path in {path}")
        new = re.sub(r'''(f?)(["'])/home/[^/]+/\.cache/([^"']*)\2''',
                     r"_repro_os.path.expanduser(\1\2~/.cache/\3\2)", new)
        uses_path = "_REPRO_ROOT" in new and "_REPRO_ROOT" not in src or "_repro_os.path.expanduser" in new and "_repro_os.path.expanduser" not in src
        if uses_path:
            tree = ast.parse(new)
            first = next(n for n in tree.body
                         if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))
                         and not (isinstance(n, ast.ImportFrom) and n.module == "__future__"))
            lines = new.splitlines(keepends=True)
            relative = os.path.relpath(ROOT, path.parent)
            lines[first.lineno - 1:first.lineno - 1] = [
                "import os as _repro_os\n",
                "_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(\n",
                f"    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), {relative!r}))\n",
            ]
            new = "".join(lines)
        # Optional GAMS tools follow the user's PATH, like other command-line tools.
        for executable in ("gams", "gdxdump"):
            new = re.sub(r'"/home/[^/]+/\.local/opt/gams/[^"\n]+/' + executable + r'"',
                         repr(executable), new)
        if new != src:
            ast.parse(new)
            path.write_text(new)
            rel = str(path.relative_to(ROOT))
            patch.extend(difflib.unified_diff(src.splitlines(True), new.splitlines(True),
                                             fromfile="a/" + rel, tofile="b/" + rel))
            print(rel)
    if patch:
        (OUT / "patches").mkdir(exist_ok=True)
        (OUT / "patches/01-remaining-portability.patch").write_text("".join(patch))


if __name__ == "__main__":
    main()
