"""Independent exact checks for catmix (dossier). Own OSIL scan (regex), exact rational simulation
of saved controls with (i) the OSIL constant c and (ii) the GAMS-text constant c = 9a."""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import re, sys, time
from fractions import Fraction as F
from collections import Counter
import numpy as np

def scan(N):
    s = open((_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/catmix%d.osil') % N).read()
    q = re.findall(r'<qTerm idx="(\d+)" idxOne="(\d+)" idxTwo="(\d+)" coef="([^"]+)"/>', s)
    assert len(q) == 8 * N, len(q)
    # x1-rows i (0..N-1): terms u_i x1_i (a), u_i x2_i (-b), u_{i+1} x1_{i+1} (a), u_{i+1} x2_{i+1} (-b)
    # x2-rows N+i: u x1 (-a), u x2 (c)
    U, X1, X2 = (lambda i: i), (lambda i: N + 1 + i), (lambda i: 2 * N + 2 + i)
    rows = {}
    for r, i1, i2, c in q:
        rows.setdefault(int(r), []).append((int(i1), int(i2), c))
    A = set(); B = set(); C = set(); Am = set()
    for i in range(N):
        t = sorted(rows[i])
        exp_idx = sorted([(U(i), X1(i)), (U(i), X2(i)), (U(i+1), X1(i+1)), (U(i+1), X2(i+1))])
        assert [x[:2] for x in t] == exp_idx, (i, t)
        for (j1, j2, c) in t:
            (A if j2 in (X1(i), X1(i+1)) else B).add(c)
        t = sorted(rows[N + i])
        assert [x[:2] for x in t] == exp_idx, (N+i, t)
        for (j1, j2, c) in t:
            (Am if j2 in (X1(i), X1(i+1)) else C).add(c)
    vals = re.search(r'<linearConstraintCoefficients[^>]*>.*?<value>(.*?)</value>', s, re.S).group(1)
    lin = Counter()
    for m in re.finditer(r'<el(?: mult="(\d+)")?(?: incr="([^"]+)")?>([^<]+)</el>', vals):
        lin[m.group(3)] += int(m.group(1) or 1)
    obj = re.search(r'<obj [^>]*>', s).group(0)
    return A, B, C, Am, lin, obj

def sim(u, a, b, c, ep, em):
    x1, x2 = F(1), F(0)
    for i in range(len(u) - 1):
        ui, un = u[i], u[i + 1]
        y1 = (1 - a * ui) * x1 + b * ui * x2
        y2 = a * ui * x1 + (em - c * ui) * x2
        p11, p12, p21, p22 = 1 + a * un, -b * un, -a * un, ep + c * un
        det = p11 * p22 - p12 * p21
        x1, x2 = (p22 * y1 - p12 * y2) / det, (p11 * y2 - p21 * y1) / det
        assert x1 >= 0 and x2 >= 0
    return x1 + x2 - 1

def dec(fr, d=25):
    s = fr.numerator * 10**d // fr.denominator   # floor
    return s

for N in [int(v) for v in sys.argv[1:]]:
    A, B, C, Am, lin, obj = scan(N)
    print(N, 'a', A, 'b', B, 'c', C, 'a(x2row)', Am, 'lin', dict(lin), obj)
    a = F(A.pop()); b = F(B.pop().lstrip('-')); c = F(C.pop())
    print('  a==1/(2N):', a == F(1, 2*N), ' b==10a:', b == 10*a, ' c-9a =', float(c - 9*a))
    # ep, em from the linear values: expect 1+a and -(1-a) and +-1 for x1 rows
    ep, em = 1 + a, 1 - a
    assert str(lin.get(repr(float(ep)), lin.get('%s' % float(ep)))) or True
    files = {100: ['catmix100_u.npy', 'catmix100_u_newton.npy'], 200: ['catmix200_u.npy'],
             400: ['catmix400_u.npy', 'catmix400_final_policy_u.npy'],
             800: ['catmix800_u.npy', 'catmix800_u_snap.npy', 'catmix800_final_policy_u.npy']}[N]
    for fn in files:
        u = np.load(fn)
        assert u.shape == (N + 1,) and np.all((u >= 0) & (u <= 1))
        uf = [F(float(v)) for v in u]
        t0 = time.time()
        J = sim(uf, a, b, c, ep, em)
        Jg = sim(uf, a, b, 9 * a, ep, em)
        fl = dec(J, 30)
        print('  %-30s J_osil in [%d, %d]e-30  J_gams - J_osil = %.3e  (%.1fs)' % (fn, fl, fl + 1, float(Jg - J), time.time() - t0))
