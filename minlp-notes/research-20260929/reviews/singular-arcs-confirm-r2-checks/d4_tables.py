"""Confirmation check d4: GFM table cell counts in singular-arcs.md.  GFM
splits table cells at every pipe not escaped by a backslash, including pipes
inside code spans.  Reports every table row whose cell count differs from its
header row."""
import re
import sys

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")


def cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return re.split(r"(?<!\\)\|", s)


i, bad, ntab = 0, 0, 0
while i < len(lines) - 1:
    if lines[i].lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
        ntab += 1
        nh = len(cells(lines[i]))
        j = i + 2
        while j < len(lines) and lines[j].lstrip().startswith("|"):
            if len(cells(lines[j])) != nh:
                bad += 1
                print("line %d: %d cells, header has %d: %s" % (j + 1, len(cells(lines[j])), nh, lines[j][:100]))
            j += 1
        i = j
    else:
        i += 1
print("%d tables, %d rows with a cell-count mismatch" % (ntab, bad))
