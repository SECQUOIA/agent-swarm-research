"""Replace hard-coded absolute paths into the main tree by paths relative to the file.

    python3 fix_paths.py <worktree root> <file relative to the worktree> ...

For each file: every string literal that starts with
/workspace/minlp-notes/research-20260929 is rewritten to start from
_RESEARCH, the research-20260929 folder computed from __file__; the definition
of _RESEARCH is inserted before the first top-level import.  Only path prefixes
change; no other code is touched.  The tool refuses files that it cannot
rewrite unambiguously.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import os
import re
import sys

PREFIX = (_PUBLIC_REPO + '/research-20260929')


def fix(root, rel):
    path = os.path.join(root, rel)
    src = open(path).read()
    if PREFIX not in src:
        print(f"{rel}: nothing to do")
        return
    if "_RESEARCH" in src:
        raise SystemExit(f"{rel}: already contains _RESEARCH; refusing")
    up = os.path.relpath(os.path.join(root, "research-20260929"), os.path.dirname(path))
    new = src
    for q in ('"', "'"):
        new = new.replace(f"f{q}{PREFIX}", f"f{q}{{_RESEARCH}}")
        new = new.replace(f"{q}{PREFIX}", f"_RESEARCH + {q}")
    if PREFIX in new:
        raise SystemExit(f"{rel}: prefix left in an unhandled form")
    lines = new.split("\n")
    k = next(i for i, l in enumerate(lines) if re.match(r"(import|from) \S", l) and "__future__" not in l)
    block = ["import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)",
             f"_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), {up!r}))"]
    lines[k:k] = block
    open(path, "w").write("\n".join(lines))
    print(f"{rel}: fixed ({src.count(PREFIX)} occurrences, _RESEARCH = {up})")


if __name__ == "__main__":
    for r in sys.argv[2:]:
        fix(sys.argv[1], r)
