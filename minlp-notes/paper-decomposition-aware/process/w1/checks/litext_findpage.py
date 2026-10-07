#!/usr/bin/env python3
"""Print (page, line excerpt) for regex matches in a text with '<!-- page N -->' markers.
Usage: litext_findpage.py FILE REGEX [maxhits] [context_chars]
Used by the lit-ext audit to attach page locators to primary-source statements."""
import re, sys
path, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
maxhits = int(sys.argv[3]) if len(sys.argv) > 3 else 20
ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 220
page, hits = 0, 0
for line in open(path, encoding='utf-8', errors='replace'):
    m = re.search(r'<!-- page (\d+) -->', line) or re.search(r'^\f', line)
    if m and m.groups():
        page = int(m.group(1))
    for mm in pat.finditer(line):
        s = max(0, mm.start() - ctx // 3)
        print(f"p.{page}: ...{line[s:s+ctx].strip()}...")
        hits += 1
        break
    if hits >= maxhits:
        break
