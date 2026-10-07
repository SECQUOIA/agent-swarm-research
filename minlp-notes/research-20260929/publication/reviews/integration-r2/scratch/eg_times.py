# Read-only: sums eg-recheck chunk timing fields from NPZ files and logs. No repo imports.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import glob, re, numpy as np
from fractions import Fraction
base = (_PUBLIC_REPO + '/research-20260929/publication/eg-recheck/')
npz = sorted(glob.glob(base + 'res/p*_c*.npz'))
tot = Fraction(0); cert = fail = 0
for f in npz:
    d = np.load(f, allow_pickle=False)
    tot += Fraction(float(d['time']))
print('npz files', len(npz), 'keys', list(np.load(npz[0]).keys()))
print('sum time fields', float(tot), 'rounded', round(float(tot)))
logs = sorted(glob.glob(base + 'logs/cert_p*_c*.log'))
s = 0; c = 0; fl = 0; tot_n = 0
for f in logs:
    t = open(f).read()
    m = re.search(r'certified (\d+)/(\d+); failures (\d+).*time (\d+)s', t)
    s += int(m.group(4)); c += int(m.group(1)); fl += int(m.group(3)); tot_n += int(m.group(2))
print('logs', len(logs), 'sum whole seconds', s, 'certified', c, 'of', tot_n, 'failures', fl)
