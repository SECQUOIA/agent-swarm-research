"""Runtime independence check of the certification path used here.

Certifies the first 128 leaves of part 7 with MarginCertifier (the path used by
recheck_leaves.py), then lists every loaded module whose file lies inside the repository and
asserts that none of the author's modules (egbb, egfast, egtm, egdata, eg_model, kan_iv, ia,
osilx, ev, eg_bb, eg_bb2) is loaded.  Also greps the certification sources for those names."""
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from margin_cert import MarginCertifier  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
AUTHOR = {"egbb", "egfast", "egtm", "egdata", "eg_model", "kan_iv", "ia", "osilx", "ev", "eg_bb", "eg_bb2", "eg_run"}

z = np.load(os.path.join(HERE, "res", "p7_c0.npz")) if os.path.exists(os.path.join(HERE, "res", "p7_c0.npz")) else None
C = MarginCertifier("eg_disc2_s", "5.642100574331458")
if z is not None:
    ok = C.certify_batch(z["lo"][:128], z["hi"][:128])
    print(f"certified {int(ok.sum())}/128 leaves of part 7; stats {C.stats}")
else:
    rec = np.load(os.path.join(HERE, "rec", "rec_disc2_p7.npz"))
    keep = rec["P_keep"].astype(bool)
    ok = C.certify_batch(rec["P_lo"][~keep][:128], rec["P_hi"][~keep][:128])
    print(f"certified {int(ok.sum())}/128 closed boxes of part 7; stats {C.stats}")
local = sorted((n, os.path.relpath(m.__file__, REPO)) for n, m in list(sys.modules.items())
               if getattr(m, "__file__", None) and os.path.abspath(m.__file__).startswith(REPO))
print("modules loaded from the repository:")
for n, f in local:
    print(f"   {n}: {f}")
bad = [n for n, _ in local if n in AUTHOR]
print("author modules loaded:", bad)
assert not bad
srcs = ["margin_cert.py", "recheck_leaves.py", "../../reviews/eg-retry-review-checks/indep_cert.py",
        "../../reviews/eg-retry-review-checks/gms_model.py", "../../reviews/eg-retry-review-checks/verify_tree.py"]
pat = re.compile(r"^\s*(import|from)\s+(\w+)", re.M)
for s in srcs:
    mods = sorted(set(m.group(2) for m in pat.finditer(open(os.path.join(HERE, s)).read())))
    print(f"imports in {s}: {mods}; author modules among them: {sorted(set(mods) & AUTHOR)}")
    assert not set(mods) & AUTHOR
print("OK: the certification path loads none of the author's modules")
