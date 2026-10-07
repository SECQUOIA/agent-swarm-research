"""(Run as an inline heredoc on 2026-10-01; saved here for the record.)
Recount the author's required subset (seed 20261001 sample + 23 finding pages)
and compare it with the reviewer's parser."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json
import step4_pages as S
log = open((_PUBLIC_REPO + '/research-20260929/publication/audit-ir/logs/parse_check.log')).read()
names = log.split('random sample:')[1].split()
pj = {r['name']: r for r in json.load(open(S.BA + 'pages.json'))}
fl = json.loads(log.split('random sample:')[0])['finding_pages']
sub = names + fl
print(len(names), len(fl), len(set(sub)))
print('points', sum(len(pj[n]['points']) for n in sub), 'duals', sum(len(pj[n]['duals']) for n in sub))
bad = [n for n in sub if S.compare(n, pj[n])[0]]
print('my parser differences on the author subset:', bad)
