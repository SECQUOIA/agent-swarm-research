"""Which audited instances have an archived listing dated on or before their latest flagged bound?"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import json
al = json.load(open((_PUBLIC_REPO + '/research-20260929/publication/minlplib-status/data/archived_listings.json')))
pre, post_only = [], []
for n, v in sorted(al.items()):
    last = max(v['flagged_bound_dates']).replace('-', '')
    first = v['first'][:8]
    before = [c['timestamp'][:8] for c in v['checked'] if c['timestamp'][:8] <= last]
    (pre if before else post_only).append((n, max(v['flagged_bound_dates']), first[:4] + '-' + first[4:6] + '-' + first[6:], before))
print('listing on/before latest flagged bound:', len(pre))
for x in pre: print('  ', x)
print('only post-bound listings:', len(post_only))
for x in post_only: print('  ', x)
