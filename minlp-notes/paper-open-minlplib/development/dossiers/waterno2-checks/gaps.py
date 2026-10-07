import json, math
from fractions import Fraction as F
d = {6: F(39157472136693483, 140737488355328)}
for T in [9, 12, 18, 24]: d[T] = F(json.load(open(f'cert_{T:02d}_w1_impl.json'))['certified_bound_exact'])
up = lambda x, k: math.ceil(x * 10**k) / 10**k
dn = lambda x, k: math.floor(x * 10**k) / 10**k
for T in [6, 9, 12, 18, 24]:
    p = F(json.load(open(f'waterno2_{T:02d}.exact.json'))['objective'])
    g = p - d[T]
    print(f'T={T} dual {d[T]} (display {dn(d[T],6)}) primal {p} (display {up(p,6)}) abs gap <= {up(g,4)} '
          f'gap/dual {float(100*g/d[T]):.6f}% (<= {up(100*g/d[T],2)}%) gap/primal {float(100*g/p):.6f}%')
# the stored objective of each exact point equals the sum of its (rational) cost coordinates
import osilmini
for T in [6, 9, 12, 18, 24]:
    m = osilmini.read(f'waterno2_{T:02d}.osil'); pt = json.load(open(f'waterno2_{T:02d}.exact.json'))
    names = [v['name'] for v in m['vars']]
    vals = [pt['x'][names[j]] for j in m['obj']]
    ok = all(isinstance(v, str) for v in vals) and sum(c * F(pt['x'][names[j]]) for j, c in m['obj'].items()) == F(pt['objective'])
    print(f'T={T}: {len(vals)} cost coordinates rational and summing exactly to the stored objective: {ok}')
