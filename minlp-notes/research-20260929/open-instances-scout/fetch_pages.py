"""Select candidate instances from the treewidth census and fetch their
MINLPLib instance pages (sequential, 1.5 s delay, header part only).

Selection: nonconvex, (tw_fac_ub <= 16 or (tw_nlprimal_ub <= 6 and
n_nl >= 50)), metadata gap > 1e-4 (or inf), not among the 11 closed
instances. Pages are cached in pages/<name>.html, truncated before the
embedded GAMS listing (<PRE>), which is not needed.

Usage: python3 fetch_pages.py
"""
import json, os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "..", "treewidth-census", "census_merged.json")
CLOSED = {"lnts50", "lnts100", "lnts200", "lnts400", "dtoc5", "camshape100",
          "camshape200", "camshape400", "camshape800", "optcdeg2", "lukvle10"}


def candidates():
    out = []
    for r in json.load(open(CENSUS)):
        if r["convex"] or r["name"] in CLOSED:
            continue
        tf, tn = r.get("tw_fac_ub"), r.get("tw_nlprimal_ub")
        if not ((tf is not None and tf <= 16) or
                (tn is not None and tn <= 6 and r["n_nl"] >= 50)):
            continue
        g = float(r["gap"])  # 'inf' parses to inf
        if g <= 1e-4:
            continue
        out.append(r)
    return out


def fetch(name):
    path = os.path.join(HERE, "pages", name + ".html")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return False
    url = f"https://www.minlplib.org/{name}.html"
    # Read only the first 120 kB; the metadata table precedes the GAMS listing.
    p = subprocess.run(f"curl -s -A 'minlp-notes research scout (sequential)' '{url}' | head -c 120000",
                       shell=True, capture_output=True)
    html = p.stdout.decode("utf-8", "replace")
    cut = html.find("<PRE>")
    if cut > 0:
        html = html[:cut]
    with open(path, "w") as f:
        f.write(html)
    return True


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "pages"), exist_ok=True)
    cands = candidates()
    with open(os.path.join(HERE, "candidates.json"), "w") as f:
        json.dump(cands, f, indent=0)
    print(len(cands), "candidates")
    for i, r in enumerate(cands):
        if fetch(r["name"]):
            time.sleep(1.5)
        if i % 20 == 0:
            print(i, r["name"], flush=True)
