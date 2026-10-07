"""Reviewer: exact rational check that the first box-search attempts that hit MAXDEPTH (rho = 6/5 for
tan:1/100:4, rho = 1 and 19/20 for tan:1/1000:9/4) were at values where a valid (B) set exists, i.e. the
statements 'z_B/z_K <= rho/z_K' are false there (for the stated L), so no method could certify them.
Uses the best (B) sets X reported in logs/tangent_family_eta*.log, rounded to rationals; lowering
parameters tau found in floating point, then rationalized; all PSD/PD tests exact."""
import json
import numpy as np
from fractions import Fraction as Fr

def symXM(X, s):
    x, y, w = s
    M = ((w, x), (y, Fr(1)))
    a = X[0][0]*M[0][0] + X[0][1]*M[1][0]; b = X[0][0]*M[0][1] + X[0][1]*M[1][1]
    c = X[1][0]*M[0][0] + X[1][1]*M[1][0]; d = X[1][0]*M[0][1] + X[1][1]*M[1][1]
    return a, (b + c)/2, d

def lmin_f(S):
    a, b, d = (float(t) for t in S)
    return 0.5*(a + d) - np.sqrt(0.25*(a - d)**2 + b*b)

def best_tau(X, s):
    qq = s[2] - s[0]*s[1]
    f = lambda t: lmin_f(symXM(X, (s[0], s[1], s[2] - Fr(t))))
    a, b = 0.0, float(qq); g = (np.sqrt(5) - 1)/2
    for _ in range(150):
        m1, m2 = b - g*(b - a), a + g*(b - a)
        if f(m1) >= f(m2): b = m2
        else: a = m1
    cands = [Fr(0), qq, Fr(0.5*(a + b)).limit_denominator(10**9)]
    return max(cands, key=lambda t: lmin_f(symXM(X, (s[0], s[1], s[2] - t))))

def psd(S, strict):
    a, b, d = S
    return (a > 0 and a*d - b*b > 0) if strict else (a >= 0 and d >= 0 and a*d - b*b >= 0)

cases = [('tangent_family_eta0.01_k4.log', Fr(1, 100), Fr(4), Fr(2), Fr(6, 5)),
         ('tangent_family_eta0.001_k2.25.log', Fr(1, 1000), Fr(9, 4), Fr(3, 2), Fr(1)),
         ('tangent_family_eta0.001_k2.25.log', Fr(1, 1000), Fr(9, 4), Fr(3, 2), Fr(19, 20))]
allok = True
for fn, eta, k, sk, rho in cases:
    for line in open('../../logs/' + fn):
        d = json.loads(line)
        L = Fr(d['L']).limit_denominator(10**6)
        X = [[Fr(v).limit_denominator(10**8) for v in row] for row in d['XB']]
        detX = X[0][0]*X[1][1] - X[0][1]*X[1][0]
        pts = {'sbar': (Fr(0), Fr(0), Fr(1)), 'P1': (rho, -rho, 1 - 2*rho*(1 - eta)),
               'P2': (rho, -k*rho, 1 - 2*sk*rho*(1 - eta)), 'P3': (rho, rho, 1 + rho*L)}
        ok = detX > 0
        res = []
        for n, s in pts.items():
            t = best_tau(X, s)
            qq = s[2] - s[0]*s[1]
            S = symXM(X, (s[0], s[1], s[2] - t))
            strict = (n == 'sbar')
            good = (0 <= t <= qq) and psd(S, strict) and (not strict or t < qq)
            ok &= good
            res.append('%s tau=%.4g %s' % (n, float(t), 'ok' if good else 'FAIL'))
        allok &= ok
        print('%s rho=%s L=%s: %s -> %s' % (fn, rho, L, '; '.join(res), 'VALID SET' if ok else 'not shown'))
print('ALL VALID' if allok else 'SOME NOT SHOWN')
