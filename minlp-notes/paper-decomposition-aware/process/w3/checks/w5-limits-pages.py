"""Measure fractional page spans of Section 10 and Appendix G in a built PDF.

Usage: python3 w5-limits-pages.py /path/to/main.pdf
A position is page + (line index on page)/(lines on page).
"""
import re, subprocess, sys
pdf = sys.argv[1]
txt = pdf[:-4] + '.pages.txt'
subprocess.run(['pdftotext', '-layout', pdf, txt], check=True)
pages = open(txt).read().split('\f')
lines = []
for pi, p in enumerate(pages):
    pl = p.split('\n')
    for li, l in enumerate(pl):
        lines.append((pi + 1 + li / max(len(pl), 1), l))

def find(pat, after=0.0):
    for pos, l in lines:
        if pos >= after and re.search(pat, l):
            return pos
    raise ValueError(pat)

ref = find(r'^\s*References\s*$')
spans = [('S10', r'^\s*10\s+Structural limits', r'^\s*11\s+Implementation', 0),
         ('App G', r'^\s*G\s+Proofs and supplements', None, ref)]
for name, s, e, after in spans:
    a = find(s, after)
    if e is None:  # next appendix heading, else end of the document
        try:
            b = find(r'^\s*H\s+\S', a + 1e-9)
        except ValueError:
            b = max(pos for pos, l in lines if l.strip()) + 1e-9
    else:
        b = find(e, a + 1e-9)
    print(f'{name:6s} p{a:7.2f} -> p{b:7.2f}  span {b - a:5.2f}')
for sub in [r'^\s*10\.1\s', r'^\s*10\.2\s', r'^\s*10\.3\s', r'^\s*10\.4\s', r'^\s*10\.5\s', r'^\s*10\.6\s', r'^\s*10\.7\s']:
    print(sub, f'{find(sub, find(spans[0][1])):7.2f}')
print('pages', len(pages) - 1)
