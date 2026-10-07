"""Part B, revision after review round 1: model copies inside archived
instance pages.

Every minlplib.org instance page embeds the full GAMS model (.gms) between
<PRE> and </PRE>. Internet Archive captures of these pages are therefore
dated model copies. For each audited instance of Part B (class (i), (i-r)
and the rocket instances) this script

  1. reads the CDX index of minlplib.org/<name>.html (stored by
     wayback_pages.py; queried again if the stored answer is not a CDX list),
  2. selects the status-200 captures that matter for the flagged bounds:
     the earliest capture, the last capture on or before the latest flagged
     bound date, and the first capture after it,
  3. downloads each selected capture raw (id_), sequentially with >= 1 s
     delay, unless a copy is already on disk,
  4. extracts the listing (between <PRE> and </PRE>, tags removed,
     HTML-unescaped) and compares it with the current .gms file
     (pages/models/gms/<name>.gms): "identical" if equal up to leading and
     trailing newlines; for a capture cut off before </PRE> (the archive
     stores at most a fixed number of bytes), "prefix" if all complete
     lines of the listing equal the start of the current file,
  5. parses the page head (bound-audit/parse_pages.py) to record which
     dual bounds the page listed at that time.

Usage: python3 archived_listings.py
Output: data/archived_listings.json, printed summary (logs/archived_listings.log)
"""
import csv
import html
import json
import os
import re
import subprocess
import time

import instances as I
import wayback_pages as W

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
CDX = os.path.join(HERE, "pages", "wayback", "cdx")
OUT = os.path.join(HERE, "pages", "wayback", "instpages")
NAMES = I.AUDIT_I + I.AUDIT_IR + I.ROCKET
UA = "minlp-notes MINLPLib history check (sequential, 1 req/s)"
# rocket bounds are not in the audit's results.csv (earlier LINDO findings);
# dates from the current instance pages
ROCKET_DATES = {"rocket100": ["2018-05-23"], "rocket200": ["2015-03-08"], "rocket400": ["2017-09-13"]}
MONTHS = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def iso(d):
    """'15 Feb 2022' -> '2022-02-15'"""
    day, mon, year = d.split()
    return f"{int(year):04d}-{MONTHS[mon]:02d}-{int(day):02d}"


def flagged_dates():
    res = {}
    with open(os.path.join(R, "bound-audit", "results.csv")) as f:
        for row in csv.DictReader(f):
            if row["cls"].startswith("(i)") or row["cls"].startswith("(i-r)"):
                res.setdefault(row["name"], set()).add(iso(row["d_date"]))
    for n, ds in ROCKET_DATES.items():
        res[n] = set(ds)
    return {n: sorted(ds) for n, ds in res.items()}


def curl(url, path):
    for attempt in range(3):
        p = subprocess.run(["curl", "-s", "-L", "-m", "600", "-A", UA, "-o", path, url])
        time.sleep(1.2)
        if p.returncode == 0 and os.path.getsize(path) > 0:
            return True
        time.sleep(10 * (attempt + 1))
    return False


def cdx_rows(n):
    path = os.path.join(CDX, f"page_{n}.txt")
    rows = [l.split() for l in open(path) if l.strip()] if os.path.exists(path) else []
    if not rows or not all(len(r) >= 3 and r[0].isdigit() for r in rows):
        curl(f"http://web.archive.org/cdx/search/cdx?url=minlplib.org/{n}.html"
             "&fl=timestamp,original,statuscode,digest,length", path)
        rows = [l.split() for l in open(path) if l.strip()]
    if not all(len(r) >= 3 and r[0].isdigit() for r in rows):
        return None
    return rows


def listing(text):
    i = text.find("<PRE>")
    if i < 0:
        return None, None
    j = text.find("</PRE>", i)
    complete = j >= 0
    body = text[i + 5:j if complete else len(text)]
    body = html.unescape(re.sub(r"<[^>]+>", "", body))
    return body, complete


def compare(body, complete, gms):
    a, b = body.strip("\n"), gms.strip("\n")
    if complete:
        return dict(verdict="identical" if a == b else "differs",
                    listing_lines=a.count("\n") + 1, gms_lines=b.count("\n") + 1)
    # cut capture: drop the last (possibly partial) line, compare the rest
    k = a.rfind("\n")
    head = a[:k + 1] if k >= 0 else ""
    return dict(verdict="prefix" if b.startswith(head) else "differs",
                listing_chars=len(head), listing_lines=head.count("\n"), gms_lines=b.count("\n") + 1)


def head_duals(text, n):
    tmp = os.path.join(OUT, f"_{n}.head.html")
    k = text.find("<PRE>")
    open(tmp, "w").write(text[:k] if k > 0 else text)
    d = W.parse_head(tmp)
    os.remove(tmp)
    return [(x["solver"], x["value"], x["date"]) for x in d["duals"]]


def main():
    os.makedirs(OUT, exist_ok=True)
    dates = flagged_dates()
    res = {}
    for n in NAMES:
        gms = open(os.path.join(HERE, "pages", "models", "gms", n + ".gms"), encoding="utf-8").read()
        rows = cdx_rows(n)
        rec = dict(flagged_bound_dates=dates[n])
        if rows is None:
            rec["error"] = "CDX query failed"
            res[n] = rec
            print(n, "CDX query failed", flush=True)
            continue
        caps = sorted({(r[0], r[1]) for r in rows if r[2] == "200"})
        last_bound = max(dates[n]).replace("-", "")
        before = [c for c in caps if c[0][:8] <= last_bound]
        after = [c for c in caps if c[0][:8] > last_bound]
        sel = {}
        if caps:
            sel[caps[0]] = ["earliest"]
        if before:
            sel.setdefault(before[-1], []).append("last on or before latest flagged bound")
        if after:
            sel.setdefault(after[0], []).append("first after latest flagged bound")
        rec.update(captures_200=len(caps), first=caps[0][0] if caps else None, checked=[])
        for (ts, url), roles in sorted(sel.items()):
            raw = os.path.join(OUT, f"{n}.{ts}.full.html")
            if not os.path.exists(raw):
                if not curl(f"http://web.archive.org/web/{ts}id_/{url}", raw):
                    rec["checked"].append(dict(timestamp=ts, roles=roles, error="download failed"))
                    continue
            text = open(raw, "rb").read().decode("utf-8", "replace")
            body, complete = listing(text)
            c = dict(timestamp=ts, roles=roles, bytes=os.path.getsize(raw), listing_complete=complete)
            if body is None:
                c["verdict"] = "no listing"
            else:
                c.update(compare(body, complete, gms))
            c["listed_duals"] = head_duals(text, n)
            rec["checked"].append(c)
            print(n, ts, "+".join(roles), c.get("verdict"), "complete" if complete else "cut",
                  c.get("listing_lines"), "/", c.get("gms_lines"), "duals:", c["listed_duals"], flush=True)
        res[n] = rec
    json.dump(res, open(os.path.join(HERE, "data", "archived_listings.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
