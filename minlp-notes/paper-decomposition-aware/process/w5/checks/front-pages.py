"""Fractional page spans of the front-group sections in a built main.pdf.

Usage: python3 front-pages.py /path/to/main.pdf
A position is page + (line index on page)/(lines on page) in pdftotext -layout.
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
    return None

marks = [('Abstract', r'^\s*Abstract\s*$'), ('1 Introduction', r'^1\s+Introduction'),
         ('Results', r'^(1\.1\s+Results|Results\.)'),
         ('Table 1', r'^\s*Table 1:'),
         ('Organization', r'^Organization\.'),
         ('2 Related', r'^2\s+Related work'), ('3 Problem', r'^3\s+Problem class'),
         ('11 Impl', r'^11\s+Implementation'),
         ('12 Concl', r'^12\s+Conclusions'), ('References', r'^References\s*$')]
pos = {}
for name, pat in marks:
    pos[name] = find(pat, pos.get('1 Introduction', 0.0) if name not in ('Abstract', '1 Introduction') else 0.0)
    print(f'{name:16s} {pos[name]}')
def sp(a, b):
    if pos[a] is None or pos[b] is None:
        return None
    return round(pos[b] - pos[a], 2)
print('Section 1 (intro):', sp('1 Introduction', '2 Related'))
print('Results..Organization:', sp('Results', 'Organization'))
print('Section 2 (related):', sp('2 Related', '3 Problem'))
print('Section 12 (concl):', sp('12 Concl', 'References'))
print('Main text end (References at):', pos['References'])
