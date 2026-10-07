"""Replace the user-specific OSIL cache path "$HOME/.cache/..." by
os.path.expanduser("~/.cache/..."), in the clean worktree only (portability; on this
machine both resolve to the same files). Usage: python3 fix_osil_cache_home.py WORKTREE_ROOT
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import os
import re
import sys

ROOT = sys.argv[1]
FILES = [
    "research-20260929/open-instances/osil_eval.py",
    "research-20260929/reviews/open-instances-verification/v_lnts.py",
    "research-20260929/reviews/open-instances-verification/v_dtoc5.py",
    "research-20260929/reviews/open-instances-verification/v_camshape.py",
    "research-20260929/reviews/open-instances-verification/v_optcdeg2.py",
    "research-20260929/reviews/open-instances-verification/v_lukvle10_prep.py",
    "research-20260929/reviews/bangbang-verification/v_model.py",
    "research-20260929/publication/primal/lnts/lnts_primal.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/dtoc5_construct.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/dtoc5_crosscheck.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/check_exact_point.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/lukvle10_enclose.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/lukvle10_crosscheck.py",
    "research-20260929/publication/reviews/primal-lnts-r1/verify_lnts_points.py",
]
PAT = re.compile(r"""(f?)(["'])/home/[^/]+/\.cache/([^"']*)\2""")
IMPORT = re.compile(r"^(import |from \S+ import )")
OS_IMPORT = re.compile(r"^import (?:[\w.]+\s*,\s*)*os\s*(?:,|#|$)")  # a plain "import os" (not "import osil", not "as _os")

for rel in FILES:
    path = os.path.join(ROOT, rel)
    lines = open(path).read().split("\n")
    uses = [i for i, l in enumerate(lines) if (_PUBLIC_HOME + '/.cache') in l]
    assert uses, rel
    for i in uses:
        new = PAT.sub(r"os.path.expanduser(\1\2~/.cache/\3\2)", lines[i])
        assert (_PUBLIC_HOME) not in new, (rel, lines[i])
        lines[i] = new
    has_os = any(OS_IMPORT.match(l) for l in lines[:uses[0]])
    if not has_os:
        first = next(i for i, l in enumerate(lines) if IMPORT.match(l))
        assert first < uses[0], rel
        lines[first:first] = ["import os"]
    open(path, "w").write("\n".join(lines))
    print(f"{rel}: {len(uses)} use(s); import os {'present' if has_os else 'added'}")
