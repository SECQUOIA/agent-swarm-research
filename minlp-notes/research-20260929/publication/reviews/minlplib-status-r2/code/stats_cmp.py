"""Review r2: structural counts of Part B instances in archived instancedata.csv (2020-02-19, 2024-03-15) vs today's."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import csv, io
CUR = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/site/instancedata.csv')
F = ['nvars', 'ncons', 'nbinvars', 'nintvars', 'nz', 'nlnz', 'njacobiannz', 'njacobiannlnz', 'nlaghessiannz', 'nlaghessiandiagnz', 'nobjnz', 'nobjnlnz', 'objsense', 'nnlvars']
NAMES = ['glider100', 'ghg_3veh', 'topopt-cantilever_60x40_50', 'methanol50', 'nuclear14', 'nd_netgen-2000-3-4-b-a-ns_7', 'sssd20-04persp', 'sssd22-08persp', 'sssd25-04persp', 'sssd25-08persp', 'watercontamination0303', 'smallinvDAXr1b150-165', 'smallinvDAXr2b150-165', 'smallinvDAXr1b200-220', 'smallinvDAXr2b200-220', 'eniplac', 'lop97icx', 'spring', 'stockcycle', 'rocket100', 'rocket200', 'rocket400']
def load(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    return {r['name']: r for r in csv.DictReader(io.StringIO(t), delimiter=';')}
cur = load(CUR)
for snap in ['dl/instancedata.20200219193207.csv', 'dl/instancedata.20240315154357.csv']:
    old = load(snap)
    bad = []
    for n in NAMES:
        if n not in old:
            bad.append((n, 'missing')); continue
        for f in F:
            if f in old[n] and f in cur[n] and old[n][f] != cur[n][f]:
                bad.append((n, f, old[n][f], cur[n][f]))
    print(snap, 'present', sum(n in old for n in NAMES), 'of', len(NAMES), 'differences:', bad)
