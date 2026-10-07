"""Verifier: fetch the current .gms of the 69 instances (sequential, 1 s delay),
record sha256 and sha1 (base32, as in Wayback CDX digests)."""
import base64, hashlib, json, os, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfetch import ALL
DL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dl", "gms")
os.makedirs(DL, exist_ok=True)
out = {}
for n in ALL:
    p = os.path.join(DL, n + ".gms")
    if not os.path.exists(p):
        req = urllib.request.Request(f"https://www.minlplib.org/gms/{n}.gms", headers={"User-Agent": "minlp-notes verifier (sequential, 1 req/s)"})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read(); lm = r.headers.get("Last-Modified")
        open(p, "wb").write(data)
        time.sleep(1)
    else:
        data = open(p, "rb").read(); lm = None
    out[n] = dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                  sha1b32=base64.b32encode(hashlib.sha1(data).digest()).decode(), last_modified=lm)
    print(n, len(data), lm, flush=True)
json.dump(out, open(os.path.join(DL, "..", "gms_manifest.json"), "w"), indent=1)
print("DONE")
