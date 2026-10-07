"""Part A: fetch the current MINLPLib instance pages and model files.

For each instance in instances.ALL this fetches, sequentially with a 1 s
delay between requests:
  https://www.minlplib.org/<name>.html  -> pages/instances/<name>.html
      (the first 400 kB are read and the page is truncated before the
      embedded GAMS listing <PRE>, as in bound-audit/fetch_pages.py; the
      first 4000 bytes after <PRE> are kept in pages/instances/<name>.pre.txt)
  https://www.minlplib.org/osil/<name>.osil -> pages/models/osil/<name>.osil
  https://www.minlplib.org/gms/<name>.gms   -> pages/models/gms/<name>.gms
HTTP response headers are kept (Last-Modified, ETag). A manifest with
sha256, size, HTTP status and Last-Modified is written to
data/fetch_manifest.json. Existing files are skipped, so the script can be
re-run after an interruption (or with a time budget, --budget seconds).

Usage: python3 fetch_current.py [--budget 560]
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

from instances import ALL

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
DATA = os.path.join(HERE, "data")
MANIFEST = os.path.join(DATA, "fetch_manifest.json")
UA = "minlp-notes MINLPLib status check (sequential, 1 req/s)"


def curl(url, path, limit=None):
    """Download url to path (at most `limit` bytes if given); parse headers."""
    hdr = path + ".headers"
    if limit:
        cmd = f"curl -s -m 600 -A '{UA}' -D '{hdr}' '{url}' | head -c {limit} > '{path}'"
        p = subprocess.run(cmd, shell=True, capture_output=True)
    else:
        p = subprocess.run(["curl", "-s", "-m", "600", "-A", UA, "-D", hdr, "-o", path, url],
                           capture_output=True)
    headers = {}
    status = None
    for line in open(hdr, errors="replace"):
        line = line.strip()
        if line.startswith("HTTP/"):
            status = int(line.split()[1])
            headers = {}
        elif ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return p.returncode, status, headers


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 1e9
    os.makedirs(DATA, exist_ok=True)
    for d in ("instances", "models/osil", "models/gms"):
        os.makedirs(os.path.join(PAGES, d), exist_ok=True)
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    t0 = time.time()
    for name in ALL:
        jobs = [("page", f"https://www.minlplib.org/{name}.html",
                 os.path.join(PAGES, "instances", name + ".full.tmp")),
                ("osil", f"https://www.minlplib.org/osil/{name}.osil",
                 os.path.join(PAGES, "models/osil", name + ".osil")),
                ("gms", f"https://www.minlplib.org/gms/{name}.gms",
                 os.path.join(PAGES, "models/gms", name + ".gms"))]
        for kind, url, path in jobs:
            key = f"{name}:{kind}"
            if key in man and man[key].get("status") == 200:
                continue
            if time.time() - t0 > budget:
                json.dump(man, open(MANIFEST, "w"), indent=1, sort_keys=True)
                print("budget reached", flush=True)
                return
            when = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            rc, status, headers = curl(url, path, 400000 if kind == "page" else None)
            rec = dict(url=url, fetched_utc=when, curl_rc=rc, status=status,
                       last_modified=headers.get("last-modified"), etag=headers.get("etag"))
            if kind == "page" and status == 200:
                raw = open(path, "rb").read()
                txt = raw.decode("utf-8", "replace")
                k = txt.find("<PRE>")
                head = txt[:k] if k > 0 else txt
                out = os.path.join(PAGES, "instances", name + ".html")
                with open(out, "w") as f:
                    f.write(head)
                with open(os.path.join(PAGES, "instances", name + ".pre.txt"), "w") as f:
                    f.write(txt[k:k + 4000] if k > 0 else "")
                rec.update(fetched_bytes=len(raw), head_bytes=len(head.encode()),
                           head_sha256=hashlib.sha256(head.encode()).hexdigest(),
                           path=os.path.relpath(out, HERE))
                os.remove(path)
                os.replace(path + ".headers", out + ".headers")
            elif status == 200:
                rec.update(bytes=os.path.getsize(path), sha256=sha256(path),
                           path=os.path.relpath(path, HERE))
            man[key] = rec
            print(key, status, rec.get("last_modified"), rec.get("bytes", rec.get("head_bytes")),
                  flush=True)
            json.dump(man, open(MANIFEST, "w"), indent=1, sort_keys=True)
            time.sleep(1.0)
    json.dump(man, open(MANIFEST, "w"), indent=1, sort_keys=True)
    print("done", round(time.time() - t0), "s", flush=True)


if __name__ == "__main__":
    main()
