"""Independent re-parse of the stored MINLPLib pages (audit-ir track).

Own parser; does not import or copy bound-audit/parse_pages.py. Re-parses
the stored HTML in bound-audit/pages/ and compares every listed point
(label, value, infeas, section, date, bold mark) and every listed dual bound
(value, solver, date, bold mark), the objective sense and problem type, and
the listing row of instances.html (type, convexity mark, #vars, #cons, S
mark, listed dual and primal bound) with bound-audit/pages.json.

All 1633 pages are compared; the report also gives the result on the
designated subset: a seeded random sample of 50 pages plus every page with a
class (i), (i-r) or emfl finding.
"""
import collections
import copy
import glob
import html
import json
import os
import random
import re
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
BA = os.path.join(HERE, '..', '..', 'bound-audit')
PAGES = os.path.join(BA, 'pages')


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def row_cell(page, label):
    """Second <TD> of the table row whose first cell starts with label."""
    k = page.find('<TD><span>' + label)
    if k < 0:
        return None
    a = page.find('</TD>', k) + len('</TD>')
    a = page.find('<TD>', a) + len('<TD>')
    b = page.find('</TD>', a)
    return page[a:b]


def entries(cell, title_prefix):
    """Split a cell into its <div title="title_prefix ..."> entries."""
    out = []
    key = '<div title="' + title_prefix
    parts = cell.split(key)
    assert parts[0].strip() in ('', '&nbsp;'), parts[0][:80]
    for p in parts[1:]:
        q = p.find('">')
        date = p[:q].strip()
        body = p[q + 2:]
        assert body.endswith('</div>'), body[-40:]
        out.append((date, body[:-len('</div>')]))
    return out


NUM = r'(?:-?inf|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)'


def value_and_rest(body):
    m = re.match(r'\s*(<B>)?\s*(' + NUM + r')\s*(</B>)?(.*)$', body, re.S)
    assert m, body[:80]
    bold = m.group(1) is not None
    assert bold == (m.group(3) is not None)
    return m.group(2), bold, m.group(4)


def parse_points(cell, section):
    pts = []
    if cell is None:
        return pts
    for date, body in entries(cell, 'Added on '):
        val, bold, rest = value_and_rest(body)
        lab = re.search(r'<A href=[^>]*\.(p\d+)\.html>(p\d+)</A>', rest)
        assert lab and lab.group(1) == lab.group(2), rest[:80]
        inf = re.search(r'\(infeas:\s*(' + NUM + r')\)', rest)
        assert inf, rest
        pts.append(dict(point=lab.group(1), value=val, infeas=inf.group(1),
                        section=section, added=date, bold=bold))
    return pts


def parse_duals(cell):
    ds = []
    for date, body in entries(cell, 'Last updated: '):
        val, bold, rest = value_and_rest(body)
        t = strip_tags(rest).strip()
        assert t.startswith('(') and t.endswith(')'), t
        ds.append(dict(value=val, solver=t[1:-1].strip(), date=date, bold=bold))
    return ds


def parse_page(path):
    s = open(path, encoding='utf-8').read()
    name = re.search(r'<H4> Instance <b> (.*?) </b> </H4>', s).group(1)
    sense = row_cell(s, 'Objective Sense')
    return dict(
        name=name,
        problem_type=strip_tags(row_cell(s, 'Problem type')).strip(),
        sense='' if sense is None else strip_tags(sense).strip(),
        points=parse_points(row_cell(s, 'Primal Bounds (infeas &le; 1e-08)'), 'primal') +
        parse_points(row_cell(s, 'Other points (infeas > 1e-08)'), 'other'),
        duals=parse_duals(row_cell(s, 'Dual Bounds')),
        page_bytes=os.path.getsize(path))


def parse_listing(path):
    s = open(path, encoding='utf-8').read()
    a = s.find('<TABLE id="instancelisting"')
    if a < 0:
        a = s.find('instancelisting')
    body = s[s.find('<TBODY', a):s.find('</TBODY>', a)]
    rows = {}
    for tr in re.findall(r'<TR[^>]*>(.*?)</TR>', body, re.S):
        tds = re.findall(r'<TD[^>]*>(.*?)</TD>', tr, re.S)
        if len(tds) != 14:
            continue
        name = strip_tags(tds[0]).strip()
        txt = [strip_tags(t).replace('\xa0', ' ').strip() for t in tds]
        rows[name] = dict(type=txt[2], convex=(txt[3] == '✔'), nvars=txt[4],
                          ncons=txt[7], solved=(txt[10] == '✔'),
                          listing_dual=txt[11], listing_primal=txt[12])
    return rows


def finding_pages():
    r = json.load(open(os.path.join(BA, 'results.json')))
    s = set()
    for x in r:
        if x['cls'].startswith('(i) ') or x['cls'].startswith('(i-r)') or \
                x['name'].startswith('emfl'):
            s.add(x['name'])
    return sorted(s)


def sig_digits(v):
    """Digits from the first to the last nonzero digit, and decimals shown."""
    t = v.lstrip('-+')
    a, _, b = t.partition('.')
    d = (a + b).strip('0')
    return len(d), len(b)


FIELDS_PT = ('point', 'value', 'infeas', 'section', 'added', 'bold')
FIELDS_D = ('value', 'solver', 'date', 'bold')
FIELDS_L = ('type', 'convex', 'nvars', 'ncons', 'solved', 'listing_dual', 'listing_primal')


def compare(mine, ref, listing):
    """Field-by-field comparison; returns (mismatches, #points, #duals,
    #listing fields compared)."""
    mism = collections.defaultdict(list)
    n_pt = n_d = n_lf = 0
    for name in sorted(set(mine) | set(ref)):
        if name not in mine or name not in ref:
            mism[name].append('page missing in one source')
            continue
        a, b = mine[name], ref[name]
        for k in ('problem_type', 'sense', 'page_bytes'):
            if a[k] != b[k]:
                mism[name].append('%s: %r vs %r' % (k, a[k], b[k]))
        pa = [tuple(p[k] for k in FIELDS_PT) for p in a['points']]
        pb = [tuple(p[k] for k in FIELDS_PT) for p in b['points']]
        n_pt += len(pa)
        if pa != pb:
            mism[name].append('points differ: %r vs %r' % (pa, pb))
        da = [tuple(d[k] for k in FIELDS_D) for d in a['duals']]
        db = [tuple(d[k] for k in FIELDS_D) for d in b['duals']]
        n_d += len(da)
        if da != db:
            mism[name].append('duals differ: %r vs %r' % (da, db))
        if name not in listing:
            mism[name].append('not in listing')
        else:
            for k in FIELDS_L:
                n_lf += 1
                if listing[name][k] != b[k]:
                    mism[name].append('listing %s: %r vs %r' % (k, listing[name][k], b[k]))
    return dict(mism), n_pt, n_d, n_lf


def main():
    ref = {e['name']: e for e in json.load(open(os.path.join(BA, 'pages.json')))}
    files = sorted(f for f in glob.glob(os.path.join(PAGES, '*.html'))
                   if os.path.basename(f) != 'instances.html')
    mine = {}
    for f in files:
        p = parse_page(f)
        assert os.path.basename(f) == p['name'] + '.html'
        mine[p['name']] = p
    listing = parse_listing(os.path.join(PAGES, 'instances.html'))

    mism, n_pt, n_d, n_lf = compare(mine, ref, listing)
    # negative control: two altered reference fields must both be reported
    bad = copy.deepcopy(ref)
    bad['spring']['duals'][0]['value'] = '0.84624568'
    bad['eniplac']['listing_dual'] = '-132117.1'
    neg = compare(mine, bad, listing)[0]
    negative_control_ok = sorted(neg) == ['eniplac', 'spring']

    finds = finding_pages()
    rest = sorted(n for n in mine if n not in finds)
    sample = sorted(random.Random(20261001).sample(rest, 50))
    subset = finds + sample

    # counts and the screen, recomputed from the re-parsed pages
    n_fin = sum(1 for p in mine.values() for d in p['duals'] if 'inf' not in d['value'])
    flagged, ties = [], []
    for p in mine.values():
        if p['sense'] not in ('min', 'max'):
            continue
        for d in p['duals']:
            if 'inf' in d['value']:
                continue
            dv = Q(d['value'])
            for pt in p['points']:
                if Q(pt['infeas']) > Q('1e-5'):
                    continue
                pv = Q(pt['value'])
                key = (p['name'], d['solver'], pt['point'], d['value'], pt['value'])
                if dv == pv:
                    ties.append(key)
                elif (dv > pv) if p['sense'] == 'min' else (dv < pv):
                    flagged.append(key)
    scr = json.load(open(os.path.join(BA, 'screen.json')))

    # display format of all listed values
    dec_max = max(sig_digits(v)[1] for p in mine.values()
                  for v in [x['value'] for x in p['points']] + [x['value'] for x in p['duals']]
                  if 'inf' not in v)
    over10 = [(p['name'], v) for p in mine.values()
              for v in [x['value'] for x in p['points']] + [x['value'] for x in p['duals']]
              if 'inf' not in v and '.' in v and v.split('.')[1] != '' and sig_digits(v)[0] > 10]

    def short(v):
        """Shown with fewer significant digits than the display allows
        (10 significant digits, 8 decimals)."""
        if 'inf' in v or Q(v) == 0:
            return None
        av = abs(Q(v))
        e = 0
        while Q(10) ** (e + 1) <= av:
            e += 1
        while Q(10) ** e > av:
            e -= 1
        allowed = min(10, 8 + e + 1)
        return sig_digits(v)[0] < allowed, sig_digits(v)[0]

    by_date = collections.defaultdict(collections.Counter)
    for p in mine.values():
        for d in p['duals']:
            s = short(d['value'])
            if s is None:
                continue
            c = by_date[d['date'][-4:]]
            c['all'] += 1
            if s[0]:
                c['short'] += 1
                if s[1] == 6:
                    c['short6'] += 1
    pts_short = collections.Counter()
    for p in mine.values():
        for x in p['points']:
            s = short(x['value'])
            if s is None:
                continue
            pts_short['all'] += 1
            if s[0]:
                pts_short['short'] += 1
                if s[1] == 6:
                    pts_short['short6'] += 1
    d17 = collections.Counter()
    for p in mine.values():
        for d in p['duals']:
            if d['date'] == '17 Sep 2013':
                s = short(d['value'])
                if s is not None:
                    d17['all'] += 1
                    d17['sig%d' % s[1]] += 1
                    d17['short'] += s[0]

    out = dict(
        pages_parsed=len(mine), pages_in_pages_json=len(ref), listing_rows=len(listing),
        points=n_pt, duals=n_d, finite_duals=n_fin, listing_fields=n_lf,
        pages_with_mismatch=len(mism), mismatches=mism,
        negative_control_detected=negative_control_ok,
        finding_pages=finds, random_sample_seed=20261001, random_sample=sample,
        subset_pages=len(subset),
        subset_points=sum(len(mine[n]['points']) for n in subset),
        subset_duals=sum(len(mine[n]['duals']) for n in subset),
        subset_mismatch=[n for n in subset if n in mism],
        screen=dict(flagged_pairs=len(flagged),
                    instances=len({f[0] for f in flagged}),
                    points=len({(f[0], f[2]) for f in flagged}),
                    instance_solver_pairs=len({(f[0], f[1]) for f in flagged}),
                    ties=len(ties),
                    same_pairs_as_screen_json=set(flagged) == {
                        (r['name'], r['solver'], r['point'], r['d_listed'], r['p_listed'])
                        for r in scr['pairs']} and len(flagged) == len(scr['pairs']),
                    same_ties_as_screen_json=set(ties) == {
                        (r['name'], r['solver'], r['point'], r['d_listed'], r['p_listed'])
                        for r in scr['ties']} and len(ties) == len(scr['ties'])),
        display=dict(max_decimals=dec_max, values_over_10_sig_digits=over10[:20],
                     n_over_10=len(over10),
                     duals_short_by_year={k: dict(v) for k, v in sorted(by_date.items())},
                     points_short=dict(pts_short),
                     duals_17_Sep_2013=dict(d17)),
        i_r_pages={n: dict(points=mine[n]['points'], duals=mine[n]['duals'],
                           listing=listing.get(n)) for n in
                   ('eniplac', 'lop97icx', 'spring', 'stockcycle')},
    )
    json.dump(out, open(os.path.join(HERE, 'logs', 'parse_check.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('i_r_pages', 'random_sample')},
                     indent=1)[:6000])
    print('random sample:', ' '.join(sample))


if __name__ == '__main__':
    main()
