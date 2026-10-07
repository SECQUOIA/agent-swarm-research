"""Group C: digit histogram of 17 Sep 2013 dual bounds (audit-ir report Section 5) under definitions A/B/C."""
import collections, re
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('dc', Path(__file__).with_name('digits_check.py'))
from html.parser import HTMLParser
PAGES = Path(__file__).resolve().parents[4] / 'bound-audit' / 'pages'
NUM = re.compile(r'^[-+]?(\d+\.?\d*|\.\d+)$')
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.cur = None; self.buf = []; self.out = []
    def handle_starttag(self, tag, attrs):
        t = dict(attrs).get('title') or ''
        if tag == 'div' and t.startswith('Last updated: ') and self.cur is None:
            self.cur = t[len('Last updated: '):]; self.buf = []
    def handle_endtag(self, tag):
        if tag == 'div' and self.cur is not None:
            toks = ''.join(self.buf).split(); self.out.append((self.cur, toks[0] if toks else '')); self.cur = None
    def handle_data(self, d):
        if self.cur is not None: self.buf.append(d)
nz = lambda v: len(v.lstrip('+-').replace('.', '').strip('0'))
tr = lambda v: len(v.lstrip('+-').replace('.', '').lstrip('0'))
vals = []
for f in sorted(PAGES.glob('*.html')):
    if f.name == 'instances.html': continue
    p = P(); p.feed(f.read_text(errors='replace'))
    vals += [v for d, v in p.out if d == '17 Sep 2013' and NUM.match(v)]
print('17 Sep 2013 numeric duals', len(vals))
for lab, fn in (('nonzero span', nz), ('to last shown digit', tr)):
    c = collections.Counter(min(fn(v), 11) if fn(v) else 1 for v in vals)
    print(lab, [c[k] for k in range(1, 12)])
print('fractional-filter >10:', sum(1 for v in vals if v.split('.')[1:] and v.split('.')[1] and nz(v) > 10))
