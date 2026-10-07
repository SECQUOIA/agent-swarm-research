"""Compare flagged dual bounds listed on archived pages with today's pages (own parser)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import csv, json, re, sys
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r2/code'))
INST = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/inst')
def duals(head):
    k = head.find("Dual Bounds"); seg = head[k:]; seg = seg[:seg.find("</TR>")]
    out = {}
    for date, inner in re.findall(r'<div title="Last updated: ([^"]+)">(.*?)</div>', seg, flags=re.S):
        t = re.sub(r"<[^>]+>", "", inner).strip()
        m = re.match(r"(\S+)\s*\((\S+)\)", t)
        out[m.group(2)] = (m.group(1), date)
    return out
flag = {}
for r in csv.DictReader(open((_PUBLIC_REPO + '/research-20260929/bound-audit/results.csv'))):
    if r['cls'].startswith('(i)') or r['cls'].startswith('(i-r)'):
        flag.setdefault(r['name'], set()).add(r['solver'])
for n in ['rocket100', 'rocket200', 'rocket400']:
    flag[n] = {'LINDO'}
arch = [json.loads(l) for l in open('logs/listing_check_author_files.log')]
for n in sorted(flag):
    now = duals(open(f'{INST}/{n}.html').read())
    for s in sorted(flag[n]):
        then = [(a['ts'][:8], tuple(x[1:]) ) for a in arch if a['name'] == n for x in a['duals'] if x[0] == s]
        print(n, s, 'now', now.get(s), '| archived:', then)
