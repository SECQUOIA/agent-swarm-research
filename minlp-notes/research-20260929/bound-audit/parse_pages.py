"""Parse the MINLPLib listing and the cached instance pages into pages.json.

Per instance: listing data (type, convex mark, solved mark "S", listing dual
and primal bound), objective sense, every listed point (value as displayed,
infeas as displayed, section "primal" (infeas <= 1e-8) or "other"), and every
per-solver dual bound (value as displayed, solver, date, bold flag).

Displayed numbers are kept as strings, because the display precision matters
for the audit (see display_unit).

Usage: python3 parse_pages.py
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def listing():
    s = open(os.path.join(PAGES, "instances.html")).read()
    out = {}
    for r in re.findall(r'<TR bgcolor="#[0-9a-f]+">(.*?)</TR>', s, re.S):
        td = re.findall(r"<TD[^>]*>(.*?)</TD>", r, re.S)
        name = re.search(r"<A href=([^>]+)\.html>", td[0]).group(1)
        out[name] = dict(type=text(td[2]), convex=text(td[3]) == "✔",
                         nvars=text(td[4]), ncons=text(td[7]), solved=text(td[10]) == "✔",
                         listing_dual=text(td[11]), listing_primal=text(td[12]))
    return out


def cells(page):
    out = {}
    for m in re.finditer(r"<TR>\s*<TD><span>(.*?)<sup>.*?</TD>\s*<TD>(.*?)</TD>\s*</TR>", page, re.S):
        out[text(m.group(1))] = m.group(2)
    return out


def points(raw, section):
    pts = []
    for m in re.finditer(r'<div title="Added on ([^"]*)">(.*?)</div>', raw, re.S):
        chunk = m.group(2)
        v = re.search(r"(" + NUM + r")\s*(?:</B>)?\s*<A href=[^>]*>(p\d+)</A>", chunk)
        if not v:
            continue
        inf = re.search(r"infeas:\s*(" + NUM + ")", chunk)
        pts.append(dict(point=v.group(2), value=v.group(1), infeas=inf.group(1) if inf else None,
                        section=section, added=m.group(1), bold="<B>" in chunk.split("<A")[0]))
    return pts


def duals(raw):
    out = []
    for m in re.finditer(r'<div title="Last updated: ([^"]*)">(.*?)</div>', raw, re.S):
        t = text(m.group(2))
        mm = re.match(r"(\S+)\s*\((.*?)\)$", t)
        if not mm:
            out.append(dict(raw=t, date=m.group(1), value=None, solver=None, bold=False))
            continue
        out.append(dict(value=mm.group(1), solver=mm.group(2).strip(), date=m.group(1),
                        bold="<B>" in m.group(2), raw=t))
    return out


def parse(name):
    page = open(os.path.join(PAGES, name + ".html")).read()
    c = cells(page)
    prim = points(c.get("Primal Bounds (infeas ≤ 1e-08)", ""), "primal")
    other = points(c.get("Other points (infeas > 1e-08)", ""), "other")
    return dict(sense=text(c.get("Objective Sense", "")).lower(),
                problem_type=text(c.get("Problem type", "")),
                points=prim + other, duals=duals(c.get("Dual Bounds", "")),
                page_bytes=len(page))


if __name__ == "__main__":
    L = listing()
    out = []
    missing = []
    for name, rec in L.items():
        p = os.path.join(PAGES, name + ".html")
        if not os.path.exists(p):
            missing.append(name)
            continue
        rec = dict(name=name, **rec, **parse(name))
        out.append(rec)
    json.dump(out, open(os.path.join(HERE, "pages.json"), "w"), indent=0)
    print(len(out), "parsed;", len(missing), "missing pages")
    print("no sense:", [r["name"] for r in out if r["sense"] not in ("min", "max")][:20])
    print("points:", sum(len(r["points"]) for r in out), "duals:", sum(len(r["duals"]) for r in out))
