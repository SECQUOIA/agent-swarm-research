"""Independent check (review r2) of archived minlplib.org instance pages.

For each archived page file given on the command line (name.TIMESTAMP...html),
extract the text after the first <PRE> tag up to </PRE> (or to EOF if the
capture is cut), HTML-unescape it and compare it with the current .gms file.
Reports: raw equality; for cut captures, the number of complete lines and
characters and whether the whole cut text (including the partial last line)
is a prefix of the current .gms.
Also prints the dual-bound rows of the page head (solver, value, date) with a
simple regex of my own.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys, os, re, html, hashlib, json

GMS = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/gms')

def duals(head):
    # the <TD> after the 'Dual Bounds' label: divs titled 'Last updated: DATE' with 'VALUE (SOLVER)'
    k = head.find("Dual Bounds")
    if k < 0:
        return []
    seg = head[k:]
    seg = seg[:seg.find("</TR>")]
    out = []
    for date, inner in re.findall(r'<div title="Last updated: ([^"]+)">(.*?)</div>', seg, flags=re.S):
        t = re.sub(r"<[^>]+>", "", inner).strip()
        m = re.match(r"(\S+)\s*\((\S+)\)", t)
        out.append((m.group(2), m.group(1), date) if m else (t, date))
    return out

res = {}
for path in sys.argv[1:]:
    base = os.path.basename(path)
    m = re.match(r"(?:page\.)?(.+?)\.(\d{14})(?:\.full)?\.html$", base)
    name, ts = m.group(1), m.group(2)
    if name == "topopt":
        name = "topopt-cantilever_60x40_50"
    raw = open(path, "rb").read()
    txt = raw.decode("utf-8")  # strict
    assert txt.count("<PRE>") == 1, "expected exactly one uppercase <PRE>"
    mo = re.search(r"<PRE>", txt)
    if not mo:
        print(base, "NO <PRE>"); continue
    start = mo.end()
    mc = re.search(r"</PRE>", txt[start:])
    complete = mc is not None
    body = txt[start:start + mc.start()] if complete else txt[start:]
    ntags = len(re.findall(r"<[a-zA-Z/][^>]*>", body))
    lst = html.unescape(body)
    gms = open(os.path.join(GMS, name + ".gms"), "rb").read().decode("utf-8")
    # page puts a newline after <PRE>
    lead = lst.startswith("\n")
    L = lst[1:] if lead else lst
    rec = dict(name=name, ts=ts, bytes=len(raw), complete=complete, tags_inside=ntags, lead_newline=lead,
               gms_lines=gms.count("\n"), gms_chars=len(gms))
    if complete:
        rec["identical_exact"] = (L == gms)
        rec["identical_mod_trailing_ws"] = (L.rstrip("\n") == gms.rstrip("\n"))
        rec["listing_lines"] = L.count("\n")
        if not rec["identical_exact"]:
            # locate first difference
            i = next((k for k in range(min(len(L), len(gms))) if L[k] != gms[k]), min(len(L), len(gms)))
            rec["first_diff_at"] = i
            rec["L_tail"] = repr(L[-40:]); rec["gms_tail"] = repr(gms[-40:])
    else:
        rec["cut_text_is_prefix"] = gms.startswith(L)
        k = L.rfind("\n")
        rec["complete_lines"] = L[:k + 1].count("\n")
        rec["complete_chars_incl_newlines"] = k + 1
        rec["partial_last_line_chars"] = len(L) - (k + 1)
        rec["cut_chars_total"] = len(L)
    head = txt[:mo.start()]
    rec["duals"] = duals(head)
    m2 = re.search(r"Last updated: (\d{4}-\d\d-\d\d)", txt)
    rec["footer_last_updated"] = m2.group(1) if m2 else None
    res[base] = rec
    print(json.dumps(rec))
