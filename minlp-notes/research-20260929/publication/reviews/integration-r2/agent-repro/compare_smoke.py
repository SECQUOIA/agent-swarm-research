"""Compare this review's relocated EG smoke outputs (smoke-out/) with the package's recorded
outputs (reproduction/logs/integration-r1-eg/) and with the stored all-leaf chunk p7_c0.

numpy and the standard library only; no repository module is imported.
Run with:  python3 -I -B compare_smoke.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import re

import numpy as np

R = (_PUBLIC_REPO + '/research-20260929')
MINE = R + "/publication/reviews/integration-r2/agent-repro/smoke-out"
REC = R + "/publication/reproduction/logs/integration-r1-eg"


def norm(text):
    # drop timings, absolute temp paths and progress-time fields
    text = re.sub(r"/tmp/\S+", "<tmp>", text)
    text = re.sub(r"\b\d+(\.\d+)?s\b", "<t>", text)
    text = re.sub(r"time \d+s", "time <t>", text)
    return text.splitlines()


ok = True
for name in ("summary", "chunk-subset", "unchanged-certifier"):
    a, b = norm(open(f"{MINE}/{name}.log").read()), norm(open(f"{REC}/{name}.log").read())
    same = a == b
    ok &= same
    print(f"{name}: {len(a)} lines; identical to recorded apart from timings/paths: {same}")
    if not same:
        for x, y in zip(a, b):
            if x != y:
                print("   mine:", x, "\n   rec: ", y)
    st = open(f"{MINE}/{name}.strace").read().splitlines()
    print(f"   strace lines {len(st)}; opens of the copied tree "
          f"{sum('/tmp/agent-repro-eg-r2-' in l for l in st)}; lines naming {_PUBLIC_REPO}: "
          f"{sum((_PUBLIC_REPO) in l for l in st)}")

m = np.load(f"{MINE}/smoke-subset.npz", allow_pickle=False)
r = np.load(f"{REC}/smoke-subset.npz", allow_pickle=False)
s = np.load(R + "/publication/eg-recheck/res/p7_c0.npz", allow_pickle=False)
print("subset keys equal:", sorted(m.files) == sorted(r.files))
diff = [k for k in m.files if k != "time" and not np.array_equal(m[k], r[k], equal_nan=m[k].dtype.kind == "f")]
print("subset arrays differing from recorded (excluding time):", diff)
ok &= not diff
sel = m["sel"]
print("subset sel:", sel.tolist()[:5], "...", len(sel), "== range(0, 29093, 1024):",
      np.array_equal(sel, np.arange(0, 29093, 1024)))
same_mg = np.array_equal(m["mg"], s["mg"][sel])
same_how = np.array_equal(m["how"], s["how"][sel])
print("subset margins/certificate kinds identical to the stored all-leaf chunk p7_c0 at these 29 leaves:",
      same_mg, same_how)
print("subset all ok, all margins > 0:", bool(np.all(m["ok"])), bool(np.all(m["mg"] > 0)),
      "cov_ok", bool(m["cov_ok"]), "n_proc", int(m["n_proc"]), "n_leaves", int(m["n_leaves"]))
ok &= same_mg and same_how
print("ALL MATCH" if ok else "DIFFERENCES FOUND")
