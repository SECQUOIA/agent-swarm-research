"""Part A: dated history of points and dual bounds for the 69 instances, from
MINLPLib's own change log https://www.minlplib.org/bounddates.html (fetched
2026-10-02 UTC; "Removals are not documented" on that page).

Output: data/bounddates.json (per instance: list of [date, kind, entry]) and
a printed summary (latest entry per instance).
"""
import html
import json
import os
import re

from instances import ALL

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    s = open(os.path.join(HERE, "pages", "site", "bounddates.html")).read()
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    blocks = re.split(r" (?=\d{4}-\d{2}-\d{2} (?:points|dual bounds) added:)", t)
    names = set(ALL)
    out = {n: [] for n in ALL}
    for b in blocks:
        m = re.match(r"(\d{4}-\d{2}-\d{2}) (points|dual bounds) added: (.*)", b)
        if not m:
            continue
        date, kind, body = m.groups()
        body = body.split(" Last updated:")[0]
        if kind == "points":
            for nm, pk, val in re.findall(r"(\S+)\.(p\d+) : (\S+)", body):
                if nm in names:
                    out[nm].append([date, "point", f"{pk} {val}"])
        else:
            for nm, solver, val in re.findall(r"(\S+) : (\S+(?: \S+)*?) (-?[\d.]+(?:[eE][-+]?\d+)?|-?inf)(?= \S+ : |$)", body):
                if nm in names:
                    out[nm].append([date, "dual", f"{solver} {val}"])
    json.dump(out, open(os.path.join(HERE, "data", "bounddates.json"), "w"), indent=1)
    for n in ALL:
        e = sorted(out[n])
        last = e[-1] if e else None
        print(f"{n:28s} entries={len(e):3d} latest={last}")


if __name__ == "__main__":
    main()
