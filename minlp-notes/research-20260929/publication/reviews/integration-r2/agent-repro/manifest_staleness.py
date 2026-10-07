# Integration review r2 (agent-repro): read-only staleness check of reproduction/manifest.json.
# This is the exact stdin that was run as: taskset -c 0,1 python3 -I -B - < manifest_staleness.py
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import hashlib, json, os
ROOT = (_PUBLIC_REPO)
m = json.load(open(ROOT + "/research-20260929/publication/reproduction/manifest.json"))
print("manifest base_commit", m["base_commit"], "files", len(m["files"]), "has extra_files key", "extra_files" in m)
print("scopes include publication/eg-recheck:", "publication/eg-recheck" in m["scopes"],
      "; publication/reviews/eg-recheck-r1:", "publication/reviews/eg-recheck-r1" in m["scopes"])
paths = {r["path"] for r in m["files"]}
print("entries under publication/eg-recheck or reviews/eg-recheck-r1:",
      sum("publication/eg-recheck" in p or "reviews/eg-recheck-r1" in p for p in paths))
for p in ["research-20260929/publication/reviews/eg-recheck-review-r1.md",
          "research-20260929/publication/literature/network/report.md",
          "research-20260929/publication/literature/small/report.md"]:
    print("listed:", p, p in paths)
missing = changed = 0
ex = []
for r in m["files"]:
    f = os.path.join(ROOT, r["path"])
    if not os.path.isfile(f):
        missing += 1; ex.append(("missing", r["path"])); continue
    if hashlib.sha256(open(f, "rb").read()).hexdigest() != r["sha256"]:
        changed += 1; ex.append(("changed", r["path"]))
print(f"listed files missing {missing}, hash changed {changed}")
for e in ex[:20]:
    print("  ", *e)
