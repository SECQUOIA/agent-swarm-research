"""Exact (rational) check of q along one dumped ray: q(sbar + t p) = q0 + L t + M t^2 with the dumped data
converted exactly to fractions.  Usage: python3 exact_ray_check.py INST K RAY"""
import sys, json, gzip, os
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
n = len(sbar)
Qf = [[F(Q[i, m]) for m in range(n)] for i in range(n)]
bf = [F(x) for x in b]; sf = [F(x) for x in sbar]; pf = [F(x) for x in P[:, j]]; cf = F(c)
q0 = sum(sf[i] * Qf[i][m] * sf[m] for i in range(n) for m in range(n)) + sum(bf[i] * sf[i] for i in range(n)) + cf
L = sum(2 * sf[i] * Qf[i][m] * pf[m] for i in range(n) for m in range(n)) + sum(bf[i] * pf[i] for i in range(n))
M = sum(pf[i] * Qf[i][m] * pf[m] for i in range(n) for m in range(n))
t = [e['t'] for e in rec['perray'] if e['i'] == j][0]
print('q0 %.6e  L %.6e  M %.6e  SCIP t %.6e' % (float(q0), float(L), float(M), t))
tf = F(t)
for tau in (F(1, 4), F(1, 2), F(3, 4), F(99, 100)):
    print('  exact q at tau=%s: %.6e' % (tau, float(q0 + L * tau * tf + M * (tau * tf) ** 2)))
print('  float64 q at tau=1/2:', float((sbar + 0.5 * t * P[:, j]) @ Q @ (sbar + 0.5 * t * P[:, j]) + b @ (sbar + 0.5 * t * P[:, j]) + c))
