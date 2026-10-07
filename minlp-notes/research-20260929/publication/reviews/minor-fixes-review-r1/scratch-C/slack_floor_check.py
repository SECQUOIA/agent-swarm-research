"""Group C: effect of the 10th-significant-digit slack floor in bound-audit/audit.py shown_slack().
Re-derives the class of every audit pair from bound-audit/results.json with the slack computed
(a) as in audit.py (floor) and (b) without the floor; read-only, does not rerun audit.py."""
import json, math, collections
from fractions import Fraction as F
from pathlib import Path
BA = Path(__file__).resolve().parents[4] / 'bound-audit'

def unit_shown(s):
    t = s.lstrip('+-').lower(); mant, _, ex = t.partition('e')
    dec = len(mant.split('.')[1]) if '.' in mant else 0
    return F(10) ** (-dec + (int(ex) if ex else 0))

def slack(s, floor):
    v = F(s)
    if v == 0:
        return F(5, 10**9)
    u = unit_shown(s)
    if floor:
        e = math.floor(math.log10(abs(float(v))))
        u = max(u, F(10) ** (e - 9))
    return u / 2

def cls(rec, floor):
    c = rec['cls']
    if 'obj_lo' not in rec or not c.startswith(('(i)', '(i-r)')) and 'margin_proved' not in rec:
        return c
    if 'margin_proved' not in rec:
        return c
    sg = 1 if rec['sense'] == 'min' else -1
    d = F(rec['d_listed']); lo, hi = F(str(rec['obj_lo'])), F(str(rec['obj_hi']))
    worst = hi if sg == 1 else lo; best = lo if sg == 1 else hi
    m = sg * (d - worst)
    if m > slack(rec['d_listed'], floor): return '(i) proven invalid'
    if m > 0: return '(i-r) invalid as listed, within rounding of shown digits'
    if sg * (d - best) <= 0: return '(ii) tolerance effect'
    return '(iii) undecided'

rows = json.loads((BA / 'results.json').read_text())
scr = json.loads((BA / 'screen.json').read_text())
print('results rows', len(rows), 'screen pairs', len(scr['pairs']), 'ties', len(scr['ties']))
bind = [r for r in rows if slack(r['d_listed'], True) != slack(r['d_listed'], False)]
print('result rows where the floor changes the slack:', len(bind), [(r['name'], r['solver'], r['d_listed'], r['cls']) for r in bind])
bind_scr = [p for p in scr['pairs'] if slack(p['d_listed'], True) != slack(p['d_listed'], False)]
bind_tie = [p for p in scr['ties'] if slack(p['d_listed'], True) != slack(p['d_listed'], False)]
print('screen pairs where floor binds:', len(bind_scr), ' ties where floor binds:', len(bind_tie),
      sorted(collections.Counter(p['name'] for p in bind_tie).items()))
# reproduce stored classes with the floor; then without it
mism = [(r['name'], r['solver'], r['cls'], cls(r, True)) for r in rows if 'margin_proved' in r and cls(r, True) != r['cls']
        and not r['cls'].startswith('(ii) tolerance effect (proven)')]
print('stored-class reproduction mismatches (floor):', mism)
c_floor = collections.Counter(cls(r, True) if 'margin_proved' in r else r['cls'] for r in rows)
c_nofl = collections.Counter(cls(r, False) if 'margin_proved' in r else r['cls'] for r in rows)
print('classes with floor   :', dict(c_floor))
print('classes without floor:', dict(c_nofl))
print('changed pairs:', [(r['name'], r['solver']) for r in rows if 'margin_proved' in r and cls(r, True) != cls(r, False)])
print('stored classes       :', dict(collections.Counter(r['cls'] for r in rows)))
