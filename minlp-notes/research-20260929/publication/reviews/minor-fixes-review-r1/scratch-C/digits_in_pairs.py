"""Group C: are any >10-digit displayed values (definitions A/B/C of digits_check.py) part of a
screened pair or a display tie in bound-audit/screen.json?"""
import json
from pathlib import Path
BA = Path(__file__).resolve().parents[4] / 'bound-audit'
scr = json.loads((BA / 'screen.json').read_text())
def nz(v): return len(v.lstrip('+-').replace('.', '').strip('0'))
def tr(v): return len(v.lstrip('+-').replace('.', '').lstrip('0'))
defs = {'A': lambda v: '.' in v and v.split('.')[1] != '' and nz(v) > 10, 'B': lambda v: nz(v) > 10, 'C': lambda v: tr(v) > 10}
for k, f in defs.items():
    for lab in ('pairs', 'ties'):
        hits = [(x['name'], x['solver'], x['point'], x['d_listed'], x['p_listed']) for x in scr[lab] if f(x['d_listed']) or f(x['p_listed'])]
        print(k, lab, len(hits), 'instances', sorted({h[0] for h in hits}))
