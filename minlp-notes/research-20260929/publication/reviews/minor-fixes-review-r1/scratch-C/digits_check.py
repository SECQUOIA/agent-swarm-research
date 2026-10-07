"""Group C: independent recount of displayed digits on the saved MINLPLib instance pages
(bound-audit/pages/*.html), using html.parser; does not use pages.json or parse_pages.py."""
import re, sys, collections
from html.parser import HTMLParser
from pathlib import Path
PAGES = Path(__file__).resolve().parents[4] / 'bound-audit' / 'pages'
NUM = re.compile(r'^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$')

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth = 0; self.kind = None; self.buf = []; self.vals = []
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            a = dict(attrs); t = a.get('title') or ''
            if self.kind is None and (t.startswith('Added on ') or t.startswith('Last updated: ')):
                self.kind = 'point' if t.startswith('Added') else 'dual'; self.depth = 1; self.buf = []
            elif self.kind is not None:
                self.depth += 1
    def handle_endtag(self, tag):
        if tag == 'div' and self.kind is not None:
            self.depth -= 1
            if self.depth == 0:
                toks = ''.join(self.buf).split()
                self.vals.append((self.kind, toks[0] if toks else ''))
                self.kind = None
    def handle_data(self, d):
        if self.kind is not None: self.buf.append(d)

def sig_nonzero(v):          # first through last nonzero digit
    return len(v.lstrip('+-').replace('.', '').strip('0'))
def sig_trailing(v):         # first nonzero digit through the last shown digit
    return len(v.lstrip('+-').replace('.', '').lstrip('0'))

allv = []; nonnum = collections.Counter(); expo = []
files = sorted(p for p in PAGES.glob('*.html') if p.name not in ('instances.html',))
for f in files:
    p = P(); p.feed(f.read_text(errors='replace'))
    for kind, tok in p.vals:
        if NUM.match(tok):
            if 'e' in tok.lower(): expo.append((f.stem, tok))
            allv.append((f.stem, kind, tok))
        else:
            nonnum[tok] += 1
print('pages parsed', len(files), 'numeric values', len(allv), 'non-numeric tokens', dict(nonnum.most_common(5)), 'exponent-form', expo[:5])
maxdec = max(len(v.split('.')[1]) if '.' in v else 0 for _, _, v in allv)
print('max decimals shown', maxdec)
A = [x for x in allv if '.' in x[2] and x[2].split('.')[1] != '' and sig_nonzero(x[2]) > 10]
B = [x for x in allv if sig_nonzero(x[2]) > 10]
C = [x for x in allv if sig_trailing(x[2]) > 10]
for lab, S, fn in (('A nonempty fractional part, first..last nonzero', A, sig_nonzero),
                   ('B no filter, first..last nonzero', B, sig_nonzero),
                   ('C first nonzero..last shown digit (trailing zeros count)', C, sig_trailing)):
    print(f'{lab}: {len(S)} entries, range {min(fn(v) for *_, v in S)}-{max(fn(v) for *_, v in S)}, '
          f'distinct strings {len(set(v for *_, v in S))}, pages {len(set(n for n, *_ in S))}, '
          f'points {sum(k=="point" for _, k, _ in S)}, duals {sum(k=="dual" for _, k, _ in S)}')
print('B minus A:', sorted(set(B) - set(A)))
print('C minus B:', sorted(set(C) - set(B)))
print('A pages:', sorted(collections.Counter(n for n, *_ in A).items()))
# does any value with a nonempty fractional part have trailing zeros after the point?
print('fractional values ending in 0:', [x for x in allv if '.' in x[2] and x[2].endswith('0') and x[2].split('.')[1]][:5])
# integer-looking displays ending with '.'
print('values with empty fractional part ("N."):', sum(1 for x in allv if x[2].endswith('.')), 'without a point:', sum(1 for x in allv if '.' not in x[2]))
