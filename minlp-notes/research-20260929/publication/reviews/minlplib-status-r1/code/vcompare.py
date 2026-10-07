"""Verifier: compare the verifier's own downloads (../dl) with
  * the cached OSIL files (~/.cache/minlplib/minlplib/osil), by sha256;
  * the stored instance pages of the audit (bound-audit/pages, 2026-09-30)
    and the scout (open-instances-scout/pages, 2026-09-29), byte for byte;
  * the audit's stored instances.html and minlplib.solu;
and parses the per-solver dual bounds and points from the fresh pages with
an own regex parser, comparing them with bound-audit/pages.json.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import hashlib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "..", "dl")
R = (_PUBLIC_REPO + '/research-20260929')
CACHE = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
sys.path.insert(0, HERE)
from vfetch import ALL  # noqa: E402


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def parse_duals(page):
    """(value, solver, date) triples from the 'dual bounds' block."""
    t = html.unescape(re.sub(r"<[^>]+>", " ", page))
    t = re.sub(r"\s+", " ", t)
    return t


def main():
    out = {}
    osil_same = page_audit = page_scout = 0
    n_scout = 0
    for n in ALL:
        rec = {}
        a = os.path.join(DL, "osil", n + ".osil")
        rec["osil_identical_to_cache"] = sha(a) == sha(os.path.join(CACHE, n + ".osil"))
        osil_same += rec["osil_identical_to_cache"]
        p = open(os.path.join(DL, "inst", n + ".html"), "rb").read()
        pa = os.path.join(R, "bound-audit", "pages", n + ".html")
        rec["page_identical_to_audit"] = os.path.exists(pa) and open(pa, "rb").read() == p
        page_audit += rec["page_identical_to_audit"]
        ps = os.path.join(R, "open-instances-scout", "pages", n + ".html")
        if os.path.exists(ps):
            n_scout += 1
            s = open(ps, "rb").read()
            rec["page_identical_to_scout"] = s == p
            page_scout += s == p
            if s != p:
                # where do they differ?
                k = next((i for i in range(min(len(s), len(p))) if s[i] != p[i]), min(len(s), len(p)))
                rec["scout_first_diff"] = [k, len(s), len(p), s[max(0, k - 60):k + 60].decode(errors="replace"),
                                           p[max(0, k - 60):k + 60].decode(errors="replace")]
        out[n] = rec
    for f in ("instances.html", "minlplib.solu"):
        mine = open(os.path.join(DL, "site", f), "rb").read()
        theirs = open(os.path.join(R, "bound-audit", "pages", f), "rb").read()
        print(f, "identical to audit copy:", mine == theirs, len(mine), len(theirs))
    print("OSIL sha256 identical to cache:", osil_same, "/", len(ALL))
    print("instance page identical to audit copy:", page_audit, "/", len(ALL))
    print("instance page identical to scout copy:", page_scout, "/", n_scout)
    for n, r in out.items():
        if not all(v for k, v in r.items() if k.endswith("cache") or k.endswith("audit") or k.endswith("scout")):
            print("DIFF", n, json.dumps(r)[:600])
    json.dump(out, open(os.path.join(DL, "vcompare.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
