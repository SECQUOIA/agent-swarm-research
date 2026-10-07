"""R6-writing: list long sentences in the manuscript sources (read only)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import re, glob, sys
files = sorted(glob.glob((_PUBLIC_REPO + '/paper-certified-support-cuts/sections/*.tex')))
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
for f in files:
    text = open(f).read()
    lines = text.split('\n')
    # map char offset to line
    offs = []; o = 0
    for l in lines:
        offs.append(o); o += len(l) + 1
    clean = re.sub(r'%.*', '', text)
    # split on sentence end followed by space and capital/backslash
    for m in re.finditer(r'[^.!?]*?(?:\$[^$]*\$[^.!?]*?)*[.!?](?=\s+[A-Z\\]|\s*$)', clean, re.S):
        s = m.group(0)
        words = re.sub(r'\$[^$]*\$', 'MATH', s)
        words = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?', ' ', words)
        n = len(words.split())
        if n >= limit:
            start = m.start()
            ln = max(i for i, x in enumerate(offs) if x <= start + len(s) - len(s.lstrip())) + 1
            print(f"{f.split('/')[-1]}:{ln}: {n} words: {' '.join(s.split())[:220]}")
