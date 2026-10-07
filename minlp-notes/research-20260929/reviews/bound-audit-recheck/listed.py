"""Print the listed primal points, other points, dual bounds and objective sense of fetched pages (own code)."""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def text(name):
    s = open(os.path.join(HERE, "data", name + ".html"), encoding="utf-8", errors="replace").read()
    s = re.sub(r"<[^>]*>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))


def section(t, start, end):
    i = t.find(start)
    if i < 0:
        return "?"
    j = t.find(end, i + len(start))
    return t[i + len(start):j if j >= 0 else i + len(start) + 400].strip()[:600]


if __name__ == "__main__":
    for name in sys.argv[1:]:
        t = text(name)
        print("==", name)
        print("  primal:", section(t, "Primal Bounds (infeas ≤ 1e-08) ⓘ", "Other points"))
        print("  other: ", section(t, "Other points (infeas > 1e-08) ⓘ", "Dual Bounds"))
        print("  duals: ", section(t, "Dual Bounds ⓘ", " ⓘ"))
        m = re.search(r"Objective Sense ⓘ (\w+)", t, re.I)
        print("  sense: ", m.group(1) if m else "?")
