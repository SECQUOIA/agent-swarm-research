"""Replace hard-coded absolute paths into the main working tree
(/workspace/minlp-notes/...) by paths computed from the script's own
location, in the clean worktree only. Usage: python3 fix_main_tree_paths.py WORKTREE_ROOT

For each file: define _REPO (the repository root, from __file__) just before the
first top-level line that uses the old path (or after the last top-level import if
the first use is inside a function), then replace the quoted prefix
"/workspace/minlp-notes/  by  _REPO + "/ .
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import os
import re
import sys

ROOT = sys.argv[1]
OLD = (_PUBLIC_REPO + '/')
FILES = [
    "research-20260929/open-instances/osil_eval.py",
    "research-20260929/theory-bangbang/optcdeg2_kkt_primal_check.py",
    "research-20260929/theory-bangbang/optcdeg2_refine_primal.py",
    "research-20260929/theory-bangbang/optcdeg2_qcal_certify.py",
    "research-20260929/theory-bangbang/optcdeg2_qcal_recheck.py",
    "research-20260929/theory-bangbang/optcdeg2_explore.py",
    "research-20260929/reviews/open-instances-verification/v_lnts.py",
    "research-20260929/reviews/open-instances-verification/v_dtoc5.py",
    "research-20260929/reviews/open-instances-verification/v_camshape.py",
    "research-20260929/reviews/open-instances-verification/v_optcdeg2.py",
    "research-20260929/reviews/open-instances-verification/v_lukvle10_prep.py",
    "research-20260929/reviews/bangbang-verification/v_primal.py",
    "research-20260929/reviews/bangbang-verification/v_states.py",
    "research-20260929/reviews/bangbang-verification/v_qcal_exact.py",
    "research-20260929/publication/primal/lnts/crosscheck.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/dtoc5_construct.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/dtoc5_crosscheck.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/lukvle10_kkt.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/lukvle10_crosscheck.py",
    "research-20260929/publication/primal/dtoc5-lukvle10/lukvle10_seed_sensitivity.py",
    "research-20260929/publication/reviews/primal-lnts-r1/verify_lnts_points.py",
    "research-20260929/publication/reviews/primal-lnts-r1/sanity_checks.py",
    "research-20260929/publication/reviews/primal-dtoc5-lukvle10-r1/check_dtoc5.py",
    "research-20260929/publication/reviews/primal-dtoc5-lukvle10-r1/check_lukvle10.py",
    "research-20260929/publication/reviews/primal-dtoc5-lukvle10-r1/kkt_lukvle10.py",
    "research-20260929/publication/reviews/primal-dtoc5-lukvle10-r1/objective_noniv_lukvle10.py",
    "research-20260929/publication/reviews/primal-dtoc5-lukvle10-r1/seed_sens_lukvle10.py",
]
IMPORT = re.compile(r"^(import |from \S+ import )")

for rel in FILES:
    path = os.path.join(ROOT, rel)
    lines = open(path).read().split("\n")
    uses = [i for i, l in enumerate(lines) if OLD in l]
    assert uses, rel
    for i in uses:
        assert re.search(r"(?<![fbr])[\"']" + re.escape(OLD), lines[i]), (rel, lines[i])
    depth = rel.count("/")  # number of directories between the repo root and the file
    up = "/".join([".."] * depth)
    defn = [
        "import os as _os  # repository root, from this file's location (no absolute paths)",
        f'_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "{up}"))',
    ]
    first = uses[0]
    if lines[first] == lines[first].lstrip():
        at = first
    else:
        tops = [i for i, l in enumerate(lines[:first]) if IMPORT.match(l)]
        at = tops[-1] + 1
    for i in uses:
        lines[i] = re.sub(r"([\"'])" + re.escape(OLD), r'_REPO + \1/', lines[i])
    lines[at:at] = defn
    open(path, "w").write("\n".join(lines))
    print(f"{rel}: {len(uses)} use(s), _REPO = <file dir>/{up}, inserted at line {at + 1}")
