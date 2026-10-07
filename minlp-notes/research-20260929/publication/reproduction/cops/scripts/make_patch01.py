"""Patch 01 (applied in the clean worktree): replace absolute paths into the main tree
(/workspace/minlp-notes/research-20260929/...) in the COPS reviewer scripts by
paths relative to the script's own location. No other change."""
import re
import sys

ROOT = sys.argv[1]  # research-20260929 directory of the tree to patch
FILES = {
    "reviews/cops-verification/v_chain_checks.py": "import random\n",
    "reviews/cops-verification/v_chain_bnb.py": "import sys\n",
    "reviews/cops-verification/v_catmix_model.py": "import sys\n",
    "reviews/cops-verification/v_catmix_primal.py": "import sys\n",
    "reviews/cops-verification/v_catmix_newton.py": "import sys\n",
    "reviews/cops-verification/v_catmix_selftest.py": "import sys\n",
    "reviews/catmix-recheck-checks/v_catmix_model.py": "import sys\n",
    "reviews/catmix-recheck-checks/v_catmix_selftest.py": "import sys\n",
}
LIT = re.compile(r'"/home/[^/]+/repo/minlp-notes/research-20260929/([^"]*)"')
DEF = ("\n# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)\n"
       "R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), \"..\", \"..\"))\n")
for rel, anchor in FILES.items():
    p = "%s/%s" % (ROOT, rel)
    s = open(p).read()
    assert s.count(anchor) >= 1 and "import os\n" not in s, rel
    s = s.replace(anchor, "import os\n" + anchor, 1)
    lines = s.split("\n")
    last = max(i for i, l in enumerate(lines[:60]) if re.match(r"(import|from) \S", l))
    lines.insert(last + 1, DEF.rstrip("\n"))
    s = "\n".join(lines)
    s, n = LIT.subn(lambda m: 'os.path.join(R29, "%s")' % m.group(1), s)
    assert n >= 1, rel
    open(p, "w").write(s)
    print(rel, "replaced", n)
