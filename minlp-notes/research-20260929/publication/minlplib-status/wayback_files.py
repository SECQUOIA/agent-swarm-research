"""Part B: Internet Archive captures of the MINLPLib model files.

Reads the CDX listings in pages/wayback/cdx/minlplib.org_{gms,osil}_.txt
(queried with http://web.archive.org/cdx/search/cdx?url=minlplib.org/gms/
&matchType=prefix&fl=timestamp,original,statuscode,digest,length).
For every capture of an instance in instances.ALL it compares the CDX digest
(base32 SHA-1 of the archived payload) with the SHA-1 of the current file.
Captures whose digest differs, and a few whose digest matches (as a check of
the digest comparison), are downloaded in raw form
(http://web.archive.org/web/<timestamp>id_/<url>), sequentially with a 1 s
delay, to pages/wayback/files/, and compared byte by byte with the current
file (identical / proper prefix = truncated capture / different).

Output: data/wayback_files.json
"""
import base64
import collections
import hashlib
import json
import os
import subprocess
import sys
import time

from instances import ALL

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "minlp-notes MINLPLib history check (sequential, 1 req/s)"
CHECK_MATCHED = {("glider100", "gms"), ("ghg_3veh", "osil"), ("sssd22-08persp", "gms")}


def d32(b):
    return base64.b32encode(hashlib.sha1(b).digest()).decode()


def fetch(ts, url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return 0
    raw = f"http://web.archive.org/web/{ts}id_/{url}"
    p = subprocess.run(["curl", "-s", "-L", "-m", "900", "-A", UA, "-o", path, raw], capture_output=True)
    time.sleep(1.0)
    return p.returncode


def main():
    out = {}
    os.makedirs(os.path.join(HERE, "pages", "wayback", "files"), exist_ok=True)
    for kind in ("gms", "osil"):
        rows = [l.split() for l in open(os.path.join(HERE, "pages", "wayback", "cdx", f"minlplib.org_{kind}_.txt"))]
        by = collections.defaultdict(list)
        for r in rows:
            if len(r) >= 5:
                by[r[1].split("/")[-1].split("?")[0].rsplit(".", 1)[0]].append(r)
        for n in ALL:
            cur = open(os.path.join(HERE, "pages", "models", kind, f"{n}.{kind}"), "rb").read()
            cd = d32(cur)
            seen = set()
            recs = []
            for ts, url, st, dig, ln in sorted(by.get(n, [])):
                if (ts, dig) in seen:
                    continue
                seen.add((ts, dig))
                rec = dict(timestamp=ts, url=url, status=st, cdx_digest=dig, digest_matches_current=dig == cd)
                if st == "200" and (dig != cd or ((n, kind) in CHECK_MATCHED and not any(
                        x.get("downloaded") for x in recs))):
                    path = os.path.join(HERE, "pages", "wayback", "files", f"{n}.{ts}.{kind}")
                    rc = fetch(ts, url, path)
                    b = open(path, "rb").read() if os.path.exists(path) else b""
                    rec.update(downloaded=True, curl_rc=rc, bytes=len(b), sha1_b32=d32(b),
                               payload_matches_cdx_digest=d32(b) == dig,
                               identical_to_current=b == cur,
                               proper_prefix_of_current=(len(b) < len(cur) and cur.startswith(b)),
                               path=os.path.relpath(path, HERE))
                    print(n, kind, ts, rec["bytes"], len(cur), "identical" if rec["identical_to_current"]
                          else "prefix" if rec["proper_prefix_of_current"] else "DIFFERENT", flush=True)
                recs.append(rec)
            out[f"{n}:{kind}"] = dict(current_sha1_b32=cd, captures=recs)
    json.dump(out, open(os.path.join(HERE, "data", "wayback_files.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
