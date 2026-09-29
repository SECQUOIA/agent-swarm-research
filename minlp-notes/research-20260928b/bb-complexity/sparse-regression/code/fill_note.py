"""Insert generated tables into phase-transition.md (run from data/)."""
import io, sys, contextlib, os, json, numpy as np
sys.path.insert(0, '../code')
import make_tables as mt
from predict_c1 import agreement
def cap(fun, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): fun(*a)
    return buf.getvalue().strip()
fn = '../phase-transition.md'; s = open(fn).read()
t61 = mt.load('c1_p200_k8_t1.5.jsonl') + mt.load('c1_scaleP_*.jsonl')
_seen = set(); _t = []
for r in t61:
    kk = (r['p'], r['n'], r['seed'])
    if kk not in _seen: _seen.add(kk); _t.append(r)
t61 = _t
rep = {
 '{T61}': cap(mt.table_c1, t61, 'Table 6.1 (`k = 8`, `tau0 = 1.5`, 8 seeds).'),
 '{T62}': cap(mt.table_c1, [r for r in mt.load('c1_gamma_half.jsonl') if not (os.path.exists('c1_gamma_half_full.jsonl') and r['n'] <= 180)] + mt.load('c1_gamma_half_full.jsonl'), 'Table 6.2 (`p = 400`, `k = 20`, `tau0 = 1.5`, 6 seeds).'),
 '{T63}': cap(mt.table_c1, mt.load('c1_sqrtn_k5.jsonl'), 'Table 6.3 (`lam = sqrt n`, `k = 5`, `alpha = 3`, 8 seeds).'),
 '{T64}': cap(mt.table_hard, mt.load('hard_k3-8.jsonl') + mt.load('hard_noise_k9-10.jsonl'), 'Table 6.4.'),
 '{T65}': cap(mt.table_hard, mt.load('hard_planted_lowalpha.jsonl'), 'Table 6.5 (planted, `b = 1`, `p = 10k`, 4 seeds).'),
 '{T66}': cap(mt.table_rule, mt.load('rule_p100_k6.jsonl') + mt.load('rule_p200_k8.jsonl'), 'Table 6.6.'),
}
agr, tot = agreement(t61)
rep['{H38}'] = '%d of %d' % (agr, tot)
s = s.replace('agrees with the exact C1 outcome in 219 of 256 instances of Section 6.1', 'agrees with the exact C1 outcome in %d of %d instances of Table 6.1' % (agr, tot))
for k, v in rep.items(): s = s.replace(k, v)
open(fn, 'w').write(s)
print('filled', {k: len(v) for k, v in rep.items()})
