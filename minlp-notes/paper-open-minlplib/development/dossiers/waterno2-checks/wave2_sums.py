import json, math
from fractions import Fraction as F
import osilmini
for T in [6, 9, 12, 18, 24]:
    d = json.load(open(f'cert_{T:02d}_w1_impl.json'))
    mult = json.load(open(f'mult_{T:02d}_w1_impl.json'))
    m = osilmini.read(f'waterno2_{T:02d}.osil')
    hor = [i for i, c in enumerate(m['cons']) if i not in m['nonlin'] and c['lb'] is not None and c['lb'] > 0
           and c['ub'] is None and all(v == 1 for v in m['rows'][i].values()) and len(m['rows'][i]) == T]
    c = m['cons'][hor[0]]['lb']
    mu = F(float(d['mu']))
    assert mu >= 0
    assert all(r['status'] == 'certified' for r in d['results'])
    assert len(d['results']) == T
    # multipliers in cert equal those in mult file?
    same = [[float(x) for x in r] for r in d['lam']] == [[float(x) for x in r] for r in mult['lam']] and float(d['mu']) == float(mult['mu'])
    tot = mu * c + sum(F(r['bound']) for r in d['results'])
    ok = tot == F(d['certified_bound_exact'])
    down9 = F(math.floor(tot * 10**9), 10**9)
    print(T, 'mu*c =', float(mu * c), 'sum =', tot, '~', float(tot), 'matches stored exact:', ok,
          'rounded down 9dp:', down9 == F(d['certified_bound_rounded_down']), 'mult file same:', same)
