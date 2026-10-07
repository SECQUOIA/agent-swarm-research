"""Read-only: compare manifest.json hashes with current files; list result-map eg rows."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import json, hashlib, os
ROOT = (_PUBLIC_REPO)
R = ROOT + "/research-20260929"
m = json.load(open(R + "/publication/reproduction/manifest.json"))
print("base_commit", m.get("base_commit")); print("note", str(m.get("note"))[:300])
files = m["files"]
def walk(x, pre=""):
    if isinstance(x, dict):
        if "sha256" in x: yield pre, x
        else:
            for k, v in x.items(): yield from walk(v, pre + "/" + k if pre else k)
    elif isinstance(x, list):
        for e in x:
            if isinstance(e, dict) and "path" in e: yield e["path"], e
entries = list(walk(files))
print("entries", len(entries)); print("example", entries[0])
stale, missing = [], []
for p, e in entries:
    fp = os.path.join(ROOT, p)
    if not os.path.exists(fp): missing.append(p); continue
    h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    if h != e["sha256"]: stale.append(p)
print("missing", len(missing), missing[:20]); print("stale", len(stale))
for p in stale: print("  stale", p)
rm = json.load(open(R + "/publication/reproduction/result-map.json"))
s = json.dumps(rm)
import re
for key in ("110,676", "110676", "1,114,361", "1114361", "under A1/A2", "6.4531031593842274", "6.4531031593842275", "5.7605396164535106", "5.7605396164535107"):
    print(key, s.count(key))
