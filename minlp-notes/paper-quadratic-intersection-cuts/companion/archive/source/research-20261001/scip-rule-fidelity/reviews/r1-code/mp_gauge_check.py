"""High-precision (mpmath, 60 digits) evaluation of the SCIP-set gauge G along one ray, with the
eigendecomposition recomputed in high precision from the dumped data (reviewer's Set formulas).
Usage: python3 mp_gauge_check.py INST K RAY T1 [T2 ...]"""
import sys, os, json, gzip
import mpmath as mp
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build
mp.mp.dps = 60
inst, k, j = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); ts = [mp.mpf(x) for x in sys.argv[4:]]
for l in gzip.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l)
    if rec['inst'] == inst and rec['k'] == k:
        break
Q, b, c, sbar, P, w, width, nq = build(rec)
Qq = mp.matrix([[mp.mpf(Q[a, m]) for m in range(nq)] for a in range(nq)])
th, V = mp.eigsy(Qq)
th = [th[i] for i in range(nq)]
beta = [sum(V[a, i] * mp.mpf(b[a]) for a in range(nq)) for i in range(nq)]
EPS = mp.mpf('1e-9')
ip = [i for i in range(nq) if th[i] > EPS]; im = [i for i in range(nq) if th[i] < -EPS]; i0 = [i for i in range(nq) if abs(th[i]) <= EPS]
kap = mp.mpf(c) - sum(beta[i] ** 2 / th[i] for i in ip + im) / 4
if abs(kap) <= EPS: kap = mp.mpf(0)
case4 = bool(rec['case4'])
def xyw(s):
    psi = [sum(V[a, i] * s[a] for a in range(nq)) for i in range(nq)]
    x = [mp.sqrt(th[i]) * (psi[i] + beta[i] / (2 * th[i])) for i in ip]
    y = [mp.sqrt(-th[i]) * (psi[i] + beta[i] / (2 * th[i])) for i in im]
    wv = sum(beta[i] * psi[i] for i in i0) + sum(mp.mpf(b[a]) * s[a] for a in range(nq, len(s)))
    return x, y, wv
sb = [mp.mpf(v) for v in sbar]; p = [mp.mpf(v) for v in P[:, j]]
x0, y0, w0 = xyw(sb)
r = mp.sqrt(1 + kap ** 2)
if case4:
    lam = x0 + [(w0 + kap + r) / (2 * mp.sqrt(r))]
elif kap > 0:
    lam = x0 + [mp.sqrt(kap)]
else:
    lam = list(x0)
nl = mp.sqrt(sum(v ** 2 for v in lam)); lam = [v / nl for v in lam]
def G(t):
    s = [sb[a] + t * p[a] for a in range(len(sb))]
    x, y, wv = xyw(s)
    if not case4:
        if kap == 0: return mp.sqrt(sum(v ** 2 for v in y)) - sum(lam[i] * x[i] for i in range(len(x)))
        if kap > 0: return mp.sqrt(sum(v ** 2 for v in y)) - sum(lam[i] * x[i] for i in range(len(x))) - lam[-1] * mp.sqrt(kap)
        return mp.sqrt(sum(v ** 2 for v in y) - kap) - sum(lam[i] * x[i] for i in range(len(x)))
    xh = x + [(wv + kap + r) / (2 * mp.sqrt(r))]; yh = y + [(wv + kap - r) / (2 * mp.sqrt(r))]
    le = lam[-1]; ny = mp.sqrt(sum(v ** 2 for v in yh)); ye = yh[-1]
    phi = ny if ye <= le * ny else mp.sqrt(max((1 - le ** 2) * (ny ** 2 - ye ** 2), 0)) + le * ye
    return phi - sum(lam[i] * xh[i] for i in range(len(xh)))
t_scip = [e['t'] for e in rec['perray'] if e['i'] == j]
print(inst, k, 'ray', j, 'case4', case4, 'kappa', mp.nstr(kap, 8), 'SCIP t', t_scip, 'G(0) =', mp.nstr(G(0), 8))
for t in ts:
    print('  G(%s) = %s' % (mp.nstr(t, 6), mp.nstr(G(t), 10)))
