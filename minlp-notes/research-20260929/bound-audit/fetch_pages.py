"""Fetch the MINLPLib instance listing and every instance page (header part).

Sequential, 1 s delay between requests. Pages are cached in pages/<name>.html,
truncated before the embedded GAMS listing (<PRE>). Already cached pages are
skipped, so the script can be re-run after an interruption.

Usage: python3 fetch_pages.py
"""
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
UA = "minlp-notes bound audit (sequential, 1 req/s)"


def get(url, path, cut_pre=False, limit=None):
    cmd = f"curl -s -m 120 -A '{UA}' '{url}'"
    if limit:
        cmd += f" | head -c {limit}"
    p = subprocess.run(cmd, shell=True, capture_output=True)
    txt = p.stdout.decode("utf-8", "replace")
    if cut_pre:
        k = txt.find("<PRE>")
        if k > 0:
            txt = txt[:k]
    with open(path, "w") as f:
        f.write(txt)
    return len(txt)


def names_from_listing(path):
    s = open(path).read()
    return re.findall(r'<TR bgcolor="#[0-9a-f]+">\s*<TD align="left"><A href=([^>]+)\.html>', s)


if __name__ == "__main__":
    os.makedirs(PAGES, exist_ok=True)
    lst = os.path.join(PAGES, "instances.html")
    if not os.path.exists(lst):
        get("https://www.minlplib.org/instances.html", lst)
        time.sleep(1)
        get("https://www.minlplib.org/minlplib.solu", os.path.join(PAGES, "minlplib.solu"))
        time.sleep(1)
    names = names_from_listing(lst)
    print(len(names), "instances in listing", flush=True)
    t0 = time.time()
    for i, n in enumerate(names):
        path = os.path.join(PAGES, n + ".html")
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            continue
        get(f"https://www.minlplib.org/{n}.html", path, cut_pre=True, limit=400000)
        time.sleep(1.0)
        if i % 50 == 0:
            print(i, n, round(time.time() - t0), "s", flush=True)
    print("done", round(time.time() - t0), "s")
