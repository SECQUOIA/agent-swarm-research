"""Render check for the literature table of open-instances-summary.md (read-only)."""
import re, sys
from markdown_it import MarkdownIt

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("| instance | prior result and consequence | report |"))
end = start
while end < len(lines) and lines[end].startswith("|"):
    end += 1
print(f"table lines {start+1}-{end} ({end-start} lines incl. header+delimiter); next line {end+1}: {lines[end]!r}")

def cells(l):
    s = re.sub(r"\\\|", "", l).strip()
    return s.strip("|").count("|") + 1

counts = {cells(l) for l in lines[start:end]}
print("distinct unescaped cell counts:", counts)
for i in range(start, end):
    if not lines[i].strip():
        print("blank line inside table at", i + 1)

md = MarkdownIt("commonmark").enable("table")
tokens = md.parse("\n".join(lines))
tables = []
cur = None
for t in tokens:
    if t.type == "table_open":
        cur = {"line": t.map[0] + 1, "rows": 0, "cells": [], "texts": []}
    elif t.type == "tr_open" and cur is not None:
        cur["rows"] += 1; cur["cells"].append(0)
    elif t.type in ("td_open", "th_open") and cur is not None:
        cur["cells"][-1] += 1
    elif t.type == "inline" and cur is not None:
        cur["texts"].append(t.content)
    elif t.type == "table_close":
        tables.append(cur); cur = None
lit = [t for t in tables if t["line"] == start + 1]
print("rendered tables:", [(t["line"], t["rows"]) for t in tables])
assert lit, "literature table did not render as a table"
t = lit[0]
print(f"literature table: {t['rows']} rows (1 header + {t['rows']-1} body), cells per row {set(t['cells'])}")
html = md.render("\n".join(lines[start:end]))
print("links rendered in table:", html.count("<a href="))
inst = [l.split("|")[1].strip() for l in lines[start + 2:end]]
print("instances:", len(inst), "unique:", len(set(inst)))
