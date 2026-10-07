"""Reviewer's own parser of the stored MINLPLib pages (bound-audit/pages/),
compared field by field with bound-audit/pages.json.
Uses html.parser to split table rows/cells, then parses each <div> entry."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import html
import json
import os
import random
import re
import sys
from html.parser import HTMLParser

BA = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
PAGES = BA + 'pages/'


class Rows(HTMLParser):
    """Collect, for every <tr>, the raw HTML of its <td> cells (top-level table rows)."""

    def __init__(self, raw):
        super().__init__(convert_charrefs=False)
        self.raw = raw
        self.rows = []
        self.depth_td = 0
        self.cur = None
        self.cell_start = None
        # line offsets
        self.lo = [0]
        for line in raw.splitlines(keepends=True):
            self.lo.append(self.lo[-1] + len(line))

    def off(self):
        l, c = self.getpos()
        return self.lo[l - 1] + c

    def handle_starttag(self, t, a):
        if t == 'tr':
            self.cur = []
        elif t == 'td' and self.cur is not None:
            if self.depth_td == 0:
                self.cell_start = self.off() + len(self.get_starttag_text())
            self.depth_td += 1

    def handle_endtag(self, t):
        if t == 'td' and self.cur is not None and self.depth_td > 0:
            self.depth_td -= 1
            if self.depth_td == 0:
                self.cur.append(self.raw[self.cell_start:self.off()])
        elif t == 'tr' and self.cur is not None:
            self.rows.append(self.cur)
            self.cur = None


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


DIV = re.compile(r'<div title="([^"]*)">(.*?)</div>\s*(?=<div title=|$)', re.S)


def parse_entries(cell):
    out = []
    pos = 0
    starts = [m.start() for m in re.finditer(r'<div title="', cell)]
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(cell)
        chunk = cell[s:e]
        title = re.match(r'<div title="([^"]*)">', chunk).group(1)
        body = chunk[len(re.match(r'<div title="[^"]*">', chunk).group(0)):]
        out.append((title, body))
    return out


def parse_page(path):
    raw = open(path, encoding='utf-8').read()
    p = Rows(raw)
    p.feed(raw)
    info = {}
    for r in p.rows:
        if len(r) != 2:
            continue
        key = text(re.sub(r"<sup>.*?</sup>", "", r[0], flags=re.S))
        info[key] = r[1]
    res = {'points': [], 'duals': []}
    for key, section in (('Primal Bounds (infeas ≤ 1e-08)', 'primal'), ('Other points (infeas > 1e-08)', 'other')):
        cell = info.get(key)
        if cell is None:
            raise ValueError('missing ' + key)
        for title, body in parse_entries(cell):
            assert title.startswith('Added on '), title
            bold = body.lstrip().startswith('<B>')
            val = text(body.split('<A href=')[0])
            lab = re.search(r'<A href=[^>]*>(p\d+)</A>', body).group(1)
            inf = re.search(r'\(infeas: ([^)]*)\)', body).group(1).strip()
            res['points'].append({'point': lab, 'value': val, 'infeas': inf, 'section': section,
                                  'added': title[len('Added on '):], 'bold': bold})
    cell = info.get('Dual Bounds')
    if cell is not None:
        for title, body in parse_entries(cell):
            assert title.startswith('Last updated: '), title
            bold = body.lstrip().startswith('<B>')
            t = text(body)
            mm = re.fullmatch(r'(\S+)\s+\((.+)\)', t)
            res['duals'].append({'value': mm.group(1), 'solver': mm.group(2),
                                 'date': title[len('Last updated: '):], 'bold': bold})
    res['sense'] = text(info.get('Objective Sense', ''))
    res['problem_type'] = text(info.get('Problem type', ''))
    return res, info


def compare(name, rec):
    mine, _ = parse_page(PAGES + name + '.html')
    diffs = []
    for k in ('sense', 'problem_type'):
        if mine[k] != rec[k]:
            diffs.append((k, mine[k], rec[k]))
    pts_rec = [{kk: q[kk] for kk in ('point', 'value', 'infeas', 'section', 'added', 'bold')} for q in rec['points']]
    if mine['points'] != pts_rec:
        diffs.append(('points', mine['points'], pts_rec))
    du_rec = [{kk: q[kk] for kk in ('value', 'solver', 'date', 'bold')} for q in rec['duals']]
    if mine['duals'] != du_rec:
        diffs.append(('duals', mine['duals'], du_rec))
    return diffs, mine


if __name__ == '__main__':
    pj = json.load(open(BA + 'pages.json'))
    recs = {r['name']: r for r in pj}
    names = sorted(recs)
    files = sorted(f[:-5] for f in os.listdir(PAGES) if f.endswith('.html') and f != 'instances.html')
    print('pages.json records', len(recs), 'stored pages', len(files), 'same set', set(files) == set(names))
    findings = ['glider100', 'topopt-cantilever_60x40_50', 'methanol50', 'sssd20-04persp', 'sssd22-08persp',
                'ghg_3veh', 'sssd25-04persp', 'nuclear14', 'sssd25-08persp', 'nd_netgen-2000-3-4-b-a-ns_7',
                'smallinvDAXr1b150-165', 'smallinvDAXr2b150-165', 'smallinvDAXr1b200-220',
                'smallinvDAXr2b200-220', 'watercontamination0303', 'eniplac', 'lop97icx', 'spring',
                'stockcycle', 'emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']
    # findings list cross-check with results.json
    res = json.load(open(BA + 'results.json'))
    cl = sorted({r['name'] for r in res if r['cls'].startswith('(i)') or r['cls'].startswith('(i-r)')} |
                {r['name'] for r in res if r['name'].startswith('emfl')})
    print('finding pages from results.json:', len(cl), 'agree with my list:', sorted(findings) == cl)
    rng = random.Random(777)  # reviewer's own seed, different from the author's
    sample = rng.sample([n for n in names if n not in findings], 50)
    tot = {'pages': 0, 'points': 0, 'duals': 0, 'diff_pages': 0}
    alld = {}
    for n in names:   # all pages; the required subset is reported separately
        d, mine = compare(n, recs[n])
        alld[n] = d
    for label, sub in (('required subset (50 random + 23 finding pages)', sample + findings), ('all pages', names)):
        npts = sum(len(recs[n]['points']) for n in sub)
        ndu = sum(len(recs[n]['duals']) for n in sub)
        bad = [n for n in sub if alld[n]]
        print('%s: pages %d, points %d, duals %d, pages with differences %d %s' % (label, len(sub), npts, ndu, len(bad), bad[:5]))
    for n in [n for n in names if alld[n]][:3]:
        print(n, alld[n][:2])
