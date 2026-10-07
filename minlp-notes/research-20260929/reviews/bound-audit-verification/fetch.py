"""Fetch instance pages, current OSIL files and selected points from minlplib.org.

Sequential, 2 s delay, files cached in data/. Re-running skips cached files.
Usage: python3 fetch.py name[:p2,p3] ...   (also fetches <name>.html and <name>.osil)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
UA = "minlp-notes independent verification (sequential, 1 req per 2 s)"


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "cached"
    r = subprocess.run(["curl", "-s", "-f", "-m", "300", "-A", UA, "-o", path, url])
    time.sleep(2)
    return "ok" if r.returncode == 0 else f"fail {r.returncode}"


if __name__ == "__main__":
    os.makedirs(D, exist_ok=True)
    for arg in sys.argv[1:]:
        name, _, pts = arg.partition(":")
        items = [f"{name}.html", f"osil/{name}.osil"]
        items += [f"sol/{name}.{p}.sol" for p in pts.split(",") if p]
        for it in items:
            path = os.path.join(D, os.path.basename(it))
            print(it, get("https://www.minlplib.org/" + it, path), flush=True)
