"""Exact check of a single-ray corner value: for ray j, q(sbar + t p_j) = q0 + L t + M t^2 with dumped
data converted exactly to rationals; prints the exact smallest root (as float) times the floored rate.
Usage: python3 exact_single_ray_zk.py INST K J   (J = index among corner rays, i.e. after dropping fixed rays)"""
import sys, os, json, gzip, math
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build
inst, k, j = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for l in gzip.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l)
    if rec['inst'] == inst and rec['k'] == k:
        break
Q, b, c, sbar, P, w, width, nq = build(rec)
keep = width > 1e-9; P, w = P[:, keep], w[keep]; wf = np.maximum(w, 1e-9 * w.max())
n = len(sbar); p = P[:, j]
idx = [i for i in range(n)]
Qf = [[F(Q[a, m]) for m in idx] for a in idx]; bf = [F(x) for x in b]; sf = [F(x) for x in sbar]; pf = [F(x) for x in p]
q0 = sum(sf[a] * Qf[a][m] * sf[m] for a in idx for m in idx) + sum(bf[a] * sf[a] for a in idx) + F(c)
L = sum(2 * sf[a] * Qf[a][m] * pf[m] for a in idx for m in idx) + sum(bf[a] * pf[a] for a in idx)
M = sum(pf[a] * Qf[a][m] * pf[m] for a in idx for m in idx)
print('q0 %.17g L %.17g M %.17g' % (q0, L, M))
disc = L * L - 4 * M * q0
if M == 0:
    t = -q0 / L if L < 0 else math.inf
else:
    d = math.sqrt(disc) if disc >= 0 else float('nan')
    roots = [((-float(L) - d) / (2 * float(M))), ((-float(L) + d) / (2 * float(M)))]
    t = min(r for r in roots if r > 0)
print('exact-data root t = %.17g, z = w_j t = %.17g' % (t, wf[j] * t))
tf = F(t)
for f in (F(1) - F(1, 10**9), F(1) + F(1, 10**9)):
    print('  q at t*(%s) = %.6e' % ('1-1e-9' if f < 1 else '1+1e-9', float(q0 + L * tf * f + M * (tf * f) ** 2)))
