import sys, json
import numpy as np
import period, rbb

D = period.setup(6)
k = json.load(open('logs/bundle_06_w1.json'))
W = rbb.Window(D, 0, 1)
c = W.objective(k['lam'], k['mu'])
lo, hi = W.fbbt(W.lo0, W.hi0)
names = [D['M']['names'][v] for v in W.gv] + [f"aux{j}:{W.auxdef[j][0]}({','.join(D['M']['names'][W.gv[a]] for a in W.auxdef[j][1])})" for j in range(W.naux)]
wid = hi - lo
order = np.argsort(-wid)
print('widest after FBBT:', [(names[j], lo[j], hi[j]) for j in order[:15]])
L = W.relaxation(lo, hi)
x, nu, val = W.node_lp(c, lo, hi, L)
print('LP value', val)
b = W.safe_bound(c, lo, hi, L, nu)
print('safe bound', b)
# contributions
rlo = c.copy()
for (cols, mid, cl, ch, sense, bl, bh), y in zip(L, nu):
    if sense == 'le': y = max(y, 0)
    np.add.at(rlo, cols, y * mid)
contrib = np.minimum(rlo * lo, rlo * hi)
lin = contrib - rlo * x
o = np.argsort(lin)
print('largest losses r_j*(bound - x*):', [(names[j], rlo[j], lo[j], hi[j], x[j]) for j in o[:10]])
