"""Float sanity check (not a proof) of the lukvle10 interval code: grid minima vs certified LBs,
and interval point values vs plain float evaluation."""
import numpy as np, json
from scipy.optimize import minimize
import v_lukvle10_bnb as V
from mpmath import iv, mp

lam = np.load('logs/lukvle10_lam_kkt.npy').copy(); x5 = np.load('logs/lukvle10_x5.npy')
LC = lam[495]; lam[30:961] = LC

def f(a, b):
    return (a * a) ** (b * b + 1) + (b * b) ** (a * a + 1)

def pairfun(i):
    L = lambda j: lam[j] if 0 <= j < V.M else 0.0
    ba = -L(2*i) + 3*L(2*i-1) - 2*L(2*i-2); qa = -2*L(2*i-1)
    bb = -L(2*i+1) + 3*L(2*i) - 2*L(2*i-1); qb = -2*L(2*i)
    return lambda a, b: f(a, b) + qa*a*a + ba*a + qb*b*b + bb*b

def step(a, b):
    return (-a + 3*b - 2*b*b + 1) / 2

def tailfun():
    ba = 3*lam[993] - 2*lam[992]; qa = -2*lam[993]; bb = -2*lam[993]
    def F(a, b):
        c = step(a, b); d = step(b, c); e = step(c, d); g = step(d, e)
        return f(a, b) + f(c, d) + f(e, g) + qa*a*a + ba*a + bb*b
    return F

out = {}
res = json.load(open('logs/lukvle10_bnb.json'))
lb = {g['first_pair']: float(g['LB']) for g in res['groups']}
R = {g['first_pair']: g['R'] for g in res['groups']}
cases = [(k, pairfun(k), R[k], lb[k]) for k in sorted(lb)] + [('tail', tailfun(), res['tail']['R'], float(res['tail']['LB']))]
worst = 1e9
for key, F, (Ra, Rb), LB in cases:
    A, B = np.meshgrid(np.linspace(-Ra, Ra, 1201), np.linspace(-Rb, Rb, 1201), indexing='ij')
    with np.errstate(all='ignore'):
        Z = F(A, B)
    k = np.nanargmin(Z); a0, b0 = A.flat[k], B.flat[k]
    r = minimize(lambda z: F(z[0], z[1]), [a0, b0], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-15, maxiter=4000))
    m = min(np.nanmin(Z), r.fun)
    worst = min(worst, m - LB)
    out[str(key)] = dict(grid_min=float(np.nanmin(Z)), local_min=float(r.fun), LB=LB, margin=float(m - LB))
# point consistency: interval point value vs float at p5 pair 16
Pm = V.Pair(*(lambda L: (-L+3*L-2*L, -2*L, -L+3*L-2*L, -2*L))(iv.mpf(float(LC))))
pv = Pm.point(float(x5[32]), float(x5[33]))
out['point_check_mid'] = [float(V.lo(pv)), float(pairfun(16)(x5[32], x5[33]))]
out['min_margin'] = worst
print(json.dumps(out, indent=0)[-1500:])
json.dump(out, open('logs/lukvle10_sanity.json', 'w'), indent=1)
