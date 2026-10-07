"""Part B: instance statistics over time (coarse model-identity evidence).

Compares structural statistics of each instance across archived MINLPLib
statistics tables:
  2014-12-09, 2015-06-08  gamsworld.org/minlp/minlplib2/html/allinstancedata.html
  2016-03-08, 2017-11-14  gamsworld.org/minlp/minlplib2/instancedata.csv
  2019-06-23, 2019-10-21, 2020-02-19, 2024-03-15, 2024-11-14
                          minlplib.org/instancedata.csv (Internet Archive)
  current                 minlplib.org/instancedata.csv (fetched 2026-10-02 UTC)
Equal statistics do not prove an unchanged model (a changed coefficient or
bound need not change any count); a changed statistic shows that something
changed (the model, or the way the statistic is computed).

Output: data/stats_history.json and a printed table of changes.
"""
import csv
import html
import io
import json
import os
import re

from instances import ALL

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, "pages", "wayback", "meta")
FIELDS = ["nvars", "ncons", "nbinvars", "nintvars", "ncontvars", "nz", "nlnz", "njacobiannz",
          "njacobiannlnz", "nlaghessiannz", "nlaghessiandiagnz", "nnlvars", "nlincons", "nquadcons",
          "npolynomcons", "nsignomcons", "ngennlcons", "nobjnz", "nobjnlnz", "objsense", "objtype",
          "conscurvature", "objcurvature", "initinfeasibility", "maxcoef", "mincoef", "maxjaccoef",
          "minjaccoef", "maxobjcoef", "minobjcoef", "adddate"]


def from_html(path):
    s = open(path, errors="replace").read()
    t = s[s.find('<table border="1" class="dataframe">'):]
    thead = t[:t.find("</thead>")]
    first_tr = re.search(r"<tr[^>]*>(.*?)</tr>", thead, re.S).group(1)
    head = re.findall(r"<th[^>]*>(.*?)</th>", first_tr, re.S)[1:]  # drop the index column
    rows = {}
    for tr in re.findall(r"<tr>(.*?)</tr>", t[t.find("<tbody>"):], re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
        if not cells:
            continue
        rows[cells[0]] = dict(zip(head, cells[1:]))
    return rows


def from_csv(path):
    s = open(path, errors="replace").read()
    k = s.find("name,")
    if k < 0 or (s.find("name;") >= 0 and s.find("name;") < k):
        k = s.find("name;")
    s = s[k:]
    delim = ";" if s.split("\n", 1)[0].count(";") > s.split("\n", 1)[0].count(",") else ","
    return {r["name"]: r for r in csv.DictReader(io.StringIO(s), delimiter=delim)}


SNAPS = [("2014-12-09", "gw_allinstancedata_20141209.html"), ("2015-06-08", "gw_allinstancedata_20150608.html"),
         ("2016-03-08", "gw_instancedata_20160308.csv"), ("2017-11-14", "gw_instancedata_20171114.csv"),
         ("2019-06-23", "ml_instancedata_20190623.csv"), ("2019-10-21", "ml_instancedata_20191021.csv"),
         ("2020-02-19", "ml_instancedata_20200219.csv"), ("2024-03-15", "ml_instancedata_20240315.csv"),
         ("2024-11-14", "ml_instancedata_20241114.csv")]


def norm(v):
    if v is None:
        return None
    v = v.strip()
    if v in ("", "None", "nan", "-"):
        return None
    try:
        f = float(v)
        return f
    except ValueError:
        return v.split(" ")[0] if re.match(r"\d{4}-\d{2}-\d{2}", v) else v


def main():
    tables = []
    for date, f in SNAPS:
        p = os.path.join(META, f)
        tables.append((date, from_html(p) if f.endswith(".html") else from_csv(p)))
    tables.append(("current", from_csv(os.path.join(HERE, "pages", "site", "instancedata.csv"))))
    out = {}
    for n in ALL:
        hist = {}
        for date, t in tables:
            r = t.get(n)
            hist[date] = None if r is None else {f: norm(r.get(f)) for f in FIELDS if f in r}
        changes = {}
        for f in FIELDS:
            seq = [(d, h[f]) for d, h in hist.items() if h is not None and f in h and h[f] is not None]
            vals = []
            for d, v in seq:
                if not vals or not same(vals[-1][1], v):
                    vals.append((d, v))
            if len(vals) > 1:
                changes[f] = vals
        present = [d for d, h in hist.items() if h is not None]
        out[n] = dict(present_in=present, changes=changes, history=hist)
    json.dump(out, open(os.path.join(HERE, "data", "stats_history.json"), "w"), indent=1, default=str)
    for n, r in out.items():
        print(n, "present:", ",".join(r["present_in"]))
        for f, v in r["changes"].items():
            print("   ", f, v)


def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= 1e-6 * max(1.0, abs(a), abs(b))
    return a == b


if __name__ == "__main__":
    main()
