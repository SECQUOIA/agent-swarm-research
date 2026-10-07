"""Print an OSIL model in readable form (uses the verifier's osilx reader)."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys, os
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx
name = sys.argv[1]
I = osilx.read(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
N = I['names']
def s(t):
    op = t[0]
    if op == 'num': return t[1]
    if op == 'var': return (t[2] + '*' if t[2] != '1' else '') + N[t[1]]
    return op + '(' + ', '.join(s(c) for c in t[1:]) + ')'
for j, nm in enumerate(N):
    print(nm, I['vt'][j], I['lb'][j], I['ub'][j])
o = I['obj']
print('OBJ', o['sense'], 'const', o['constant'], {N[j]: v for j, v in o['lin'].items()}, [(N[a], N[b], c) for a, b, c in o['quad']], s(o['nl']) if o['nl'] else None)
for c in I['cons']:
    print(c['name'], c['lb'], c['ub'], 'const', c['constant'], {N[j]: v for j, v in c['lin'].items()}, [(N[a], N[b], cc) for a, b, cc in c['quad']], s(c['nl']) if c['nl'] else None)
