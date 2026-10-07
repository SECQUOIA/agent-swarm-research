"""Fractional page spans of Section 9 and Appendix F (W5 optsets).

Usage: python3 optsets-w5-pages.py <main.pdf>
Position = page + (line index on page)/(lines on page), from pdftotext -layout.
"""
import re, subprocess, sys
pdf = sys.argv[1]
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True,
                     capture_output=True, text=True).stdout
lines = []
for pi, p in enumerate(txt.split('\f')):
    pl = p.split('\n')
    for li, l in enumerate(pl):
        lines.append((pi + 1 + li / max(len(pl), 1), l))

def find(pat, after=0.0):
    for pos, l in lines:
        if pos >= after and re.search(pat, l):
            return pos
    raise ValueError(pat)

def span(name, s, e, after=0.0):
    try:
        a = find(s, after); b = find(e, a + 1e-9)
        print(f'{name:28s} p{a:7.2f} -> p{b:7.2f}  span {b - a:5.2f}')
    except ValueError as ex:
        print(name, 'not found:', ex)

span('Section 9', r'^\s*9\s+Several minimizers', r'^\s*10\s+Structural limits')
span('  9.1', r'^\s*9\.1\s', r'^\s*9\.2\s')
span('  9.2', r'^\s*9\.2\s', r'^\s*9\.3\s')
span('  9.3', r'^\s*9\.3\s', r'^\s*10\s+Structural limits')
span('Appendix F', r'^\s*F\s+(The diagonal|Proofs for Section 9)', r'^\s*G\s+Proofs')
span('Main text (1 .. References)', r'^\s*1\s+Introduction', r'^\s*References\s*$')
