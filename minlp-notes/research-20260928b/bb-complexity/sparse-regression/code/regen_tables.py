"""Regenerate Tables 6.1-6.3 of phase-transition.md in place (run from data/), using exact C1
decisions (capped runs replaced by redecide_c1.py results)."""
import io, sys, contextlib, os, json
sys.path.insert(0, '../code')
import make_tables as mt
def cap(fun, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): fun(*a)
    return buf.getvalue().strip()
def dedup(rows):
    seen, out = set(), []
    for r in rows:
        kk = (r['p'], r['k'], r['n'], r['seed'])
        if kk not in seen: seen.add(kk); out.append(r)
    return out
t61 = dedup(mt.load('c1_p200_k8_t1.5.jsonl') + mt.load('c1_scaleP_*.jsonl'))
t62 = [r for r in mt.load('c1_gamma_half.jsonl') if r['n'] > 180] + mt.load('c1_gamma_half_full.jsonl')
t63 = mt.load('c1_sqrtn_k5.jsonl')
new = {'Table 6.1': cap(mt.table_c1, t61, 'Table 6.1 (`k = 8`, `tau0 = 1.5`, 8 seeds).'),
       'Table 6.2': cap(mt.table_c1, t62, 'Table 6.2 (`p = 400`, `k = 20`, `tau0 = 1.5`, 6 seeds).'),
       'Table 6.3': cap(mt.table_c1, t63, 'Table 6.3 (`lam = sqrt n`, `k = 5`, `alpha = 3`, 8 seeds).')}
fn = '../phase-transition.md'; lines = open(fn).read().split('\n')
out = []; i = 0
while i < len(lines):
    L = lines[i]; key = next((k for k in new if L.startswith(k + ' (')), None)
    if key is None: out.append(L); i += 1; continue
    out.extend(new[key].split('\n'))
    i += 1
    while i < len(lines) and lines[i].strip() == '': i += 1          # blank after caption
    while i < len(lines) and lines[i].startswith('|'): i += 1         # old table rows
print('replaced', [k for k in new])
open(fn, 'w').write('\n'.join(out))
