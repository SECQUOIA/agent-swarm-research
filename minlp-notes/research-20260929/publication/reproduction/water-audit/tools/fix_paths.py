"""Replace hard-coded absolute paths into the main tree by paths relative to the file.

Clean-checkout fix for the water/audit reproduction track. For each listed file
(relative to research-20260929/ of the given checkout):
  - insert, before the first top-level import, the line pair used by the other
    reproduction tracks:
        import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
        _RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '<rel>'))
  - "/workspace/minlp-notes/research-20260929/X"  -> _RESEARCH + "/X"
    f"/workspace/minlp-notes/research-20260929/X" -> f"{_RESEARCH}/X"
  - "$HOME/.cache/minlplib/..." -> _os.path.expanduser("~/.cache/minlplib/...")
Shell scripts: `cd /home/.../research-20260929/<dir>` -> `cd "$(dirname "$0")"`.

usage: python3 fix_paths.py <checkout>/research-20260929 file1 file2 ...
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])
_PUBLIC_HOME = str(_PublicPath.home())

import os
import re
import sys

MAIN = (_PUBLIC_REPO + '/research-20260929/')
CACHE = (_PUBLIC_HOME + '/.cache/minlplib/')


def fix_py(path, rel_from_root):
    src = open(path).read()
    if MAIN not in src and CACHE not in src:
        return False
    depth = len(os.path.dirname(rel_from_root).split("/")) if os.path.dirname(rel_from_root) else 0
    rel = "/".join([".."] * depth) if depth else "."
    s = src
    s = s.replace('f"' + MAIN, 'f"{_RESEARCH}/')
    s = s.replace("f'" + MAIN, "f'{_RESEARCH}/")
    s = s.replace('"' + MAIN, '_RESEARCH + "/')
    s = s.replace("'" + MAIN, "_RESEARCH + '/")
    # f-string cache path: f"$HOME/.cache/minlplib/...{T}..." -> _os.path.expanduser("~") + f"/.cache/..."
    s = s.replace('f"' + CACHE, '_os.path.expanduser("~") + f"/.cache/minlplib/')
    s = re.sub(r'"' + re.escape(CACHE) + r'([^"]*)"',
               lambda m: '_os.path.expanduser("~/.cache/minlplib/' + m.group(1) + '")', s)
    assert MAIN not in s and CACHE not in s, path
    lines = s.split("\n")
    # first top-level import statement (after the module docstring), located with ast
    import ast
    k = min(n.lineno for n in ast.parse(src).body if isinstance(n, (ast.Import, ast.ImportFrom))) - 1
    hdr = ["import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)",
           f"_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '{rel}'))"]
    lines[k:k] = hdr
    open(path, "w").write("\n".join(lines))
    return True


def fix_sh(path):
    src = open(path).read()
    s = re.sub(r"cd " + re.escape(MAIN) + r"\S+", 'cd "$(dirname "$0")"', src)
    assert MAIN not in s, path
    if s != src:
        open(path, "w").write(s)
        return True
    return False


def main():
    root = sys.argv[1].rstrip("/")
    for rel in sys.argv[2:]:
        p = os.path.join(root, rel)
        ch = fix_sh(p) if p.endswith(".sh") else fix_py(p, rel)
        print(("fixed " if ch else "unchanged ") + rel)


if __name__ == "__main__":
    main()
