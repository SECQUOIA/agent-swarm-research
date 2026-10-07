"""Fetch instance pages, OSIL files and listed points from minlplib.org (own code).

Sequential, 2 s delay between requests, cached in data/.
Usage: python3 fetch.py name:p1,p2 ...
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "cached"
    r = subprocess.run(["curl", "-s", "-f", "-m", "300", "-A",
                        "minlp-notes bound-audit recheck (sequential, 2 s delay)", "-o", path, url])
    time.sleep(2)
    return "ok" if r.returncode == 0 else f"FAILED ({r.returncode})"


if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    for arg in sys.argv[1:]:
        name, _, pts = arg.partition(":")
        items = [f"{name}.html", f"osil/{name}.osil"] + [f"sol/{name}.{p}.sol" for p in pts.split(",") if p]
        for it in items:
            print(it, get("https://www.minlplib.org/" + it, os.path.join(DATA, os.path.basename(it))), flush=True)
