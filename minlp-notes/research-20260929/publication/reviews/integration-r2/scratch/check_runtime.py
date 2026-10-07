# Read-only check of READINESS runtime table against commands.json and saved outputs.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, hashlib, os, re
P = (_PUBLIC_REPO + '/research-20260929/publication/')
R = (_PUBLIC_REPO + '/research-20260929')
ev = json.load(open(P + 'integration/runtime-evidence-r1.json'))
cmds = json.load(open(P + 'reproduction/commands.json'))
byid = {c['id']: c for c in cmds}
print('commands now', len(cmds), 'eg-recheck ids', sum(c['id'].startswith('eg-recheck/') for c in cmds),
      'non-eg-recheck', sum(not c['id'].startswith('eg-recheck/') for c in cmds))
bad = 0
for e in ev['entries']:
    c = byid.get(e['id'])
    msg = []
    if c is None: msg.append('MISSING id')
    else:
        if str(c.get('wall_s')) != str(e['wall_s']): msg.append(f"wall {c.get('wall_s')} != {e['wall_s']}")
        if c.get('exit') != 0: msg.append(f"exit {c.get('exit')}")
        if c.get('command') != e['command']: msg.append('command differs')
    out = e['output']
    path = out.replace('$R', R) if out.startswith('$R') else P + 'reproduction/' + out
    if os.path.exists(path):
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        if h != e['sha256']: msg.append('sha mismatch')
    else: msg.append('output missing ' + path)
    if msg: bad += 1
    print(e['id'], e['wall_s'], 'OK' if not msg else msg)
print('entries', len(ev['entries']), 'bad', bad)
# compare with READINESS table
txt = open(P + 'READINESS.md').read()
tab = txt[txt.index('| family / recorded operation'):txt.index('For the eg_disc2_s all-leaf recheck')]
vals = []
for line in tab.splitlines()[2:]:
    if line.startswith('|'):
        cell = line.split('|')[2]
        vals += [v.strip() for v in cell.split('/')]
ev_vals = [str(e['wall_s']) for e in ev['entries']]
print('table values', len(vals), 'evidence values', len(ev_vals))
print('match in order:', vals == ev_vals)
if vals != ev_vals:
    for i,(a,b) in enumerate(zip(vals, ev_vals)):
        if a != b: print(i, a, b)
