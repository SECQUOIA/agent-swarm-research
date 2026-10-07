"""Fresh exact checks for the catmix dossier (written 2026-10-04, independent of earlier scripts).
Reads OSIL with xml.etree, extracts a, b, c, ep, em as exact Fractions from the decimal strings,
asserts the row pattern, then simulates saved binary64 controls exactly (Fractions) with
(i) the OSIL c and (ii) c = 9a (GAMS text), and reports floor/ceil of J at 1e-30."""
import sys, time
import xml.etree.ElementTree as ET
from fractions import Fraction as F
import numpy as np

def strip(t): return t.split('}')[-1]

def read(N):
    root = ET.parse('catmix%d.osil' % N).getroot()
    ns = {}
    q = {}
    for el in root.iter():
        if strip(el.tag) == 'qTerm':
            r = int(el.get('idx')); q.setdefault(r, []).append((int(el.get('idxOne')), int(el.get('idxTwo')), el.get('coef')))
        if strip(el.tag) == 'obj':
            obj = dict(el.attrib); objc = [(int(c.get('idx')), c.text) for c in el if strip(c.tag) == 'coef']
        if strip(el.tag) == 'var':
            ns.setdefault('vars', []).append(dict(el.attrib))
        if strip(el.tag) == 'con':
            ns.setdefault('cons', []).append(dict(el.attrib))
    V = ns['vars']; C = ns['cons']
    assert len(V) == 3 * N + 3 and len(C) == 2 * N
    U, X1, X2 = (lambda i: i), (lambda i: N + 1 + i), (lambda i: 2 * N + 2 + i)
    for j, v in enumerate(V):
        lb, ub = v.get('lb', '0'), v.get('ub', 'INF')
        if j <= N: assert F(lb) == 0 and F(ub) == 1, (j, v)
        elif j == X1(0): assert F(lb) == 1 and F(ub) == 1
        elif j == X2(0): assert F(lb) == 0 and F(ub) == 0
        else: assert lb == '-INF' and ub == 'INF', (j, v)
        assert v.get('type', 'C') == 'C'
    for c in C: assert F(c['lb']) == 0 and F(c['ub']) == 0
    assert obj.get('maxOrMin') == 'min' and F(obj.get('constant')) == -1
    assert sorted(objc) == sorted([(X1(N), '1'), (X2(N), '1')]), objc
    A = {t[2] for i in range(N) for t in q[i] if t[1] in (X1(i), X1(i + 1))}
    B = {t[2] for i in range(N) for t in q[i] if t[1] in (X2(i), X2(i + 1))}
    Am = {t[2] for i in range(N) for t in q[N + i] if t[1] in (X1(i), X1(i + 1))}
    Cc = {t[2] for i in range(N) for t in q[N + i] if t[1] in (X2(i), X2(i + 1))}
    for i in range(N):
        assert sorted((t[0], t[1]) for t in q[i]) == sorted([(U(i), X1(i)), (U(i), X2(i)), (U(i + 1), X1(i + 1)), (U(i + 1), X2(i + 1))])
        assert sorted((t[0], t[1]) for t in q[N + i]) == sorted([(U(i), X1(i)), (U(i), X2(i)), (U(i + 1), X1(i + 1)), (U(i + 1), X2(i + 1))])
    assert len(A) == len(B) == len(Am) == len(Cc) == 1, (A, B, Am, Cc)
    a, b, am, c = F(A.pop()), -F(B.pop()), -F(Am.pop()), F(Cc.pop())
    assert a == am == F(1, 2 * N) and b == 10 * a
    return a, b, c

def sim(u, a, b, c):
    ep, em = 1 + a, 1 - a
    x1, x2 = F(1), F(0)
    for i in range(len(u) - 1):
        ui, un = u[i], u[i + 1]
        y1 = (1 - a * ui) * x1 + b * ui * x2
        y2 = a * ui * x1 + (em - c * ui) * x2
        p11, p12, p21, p22 = 1 + a * un, -b * un, -a * un, ep + c * un
        det = p11 * p22 - p12 * p21
        assert det > 0
        x1, x2 = (p22 * y1 - p12 * y2) / det, (p11 * y2 - p21 * y1) / det
        assert x1 >= 0 and x2 >= 0
    return x1 + x2 - 1

def fl30(x): return x.numerator * 10**30 // x.denominator

files = {100: ['catmix100_u.npy', 'catmix100_u_newton.npy'], 200: ['catmix200_u.npy'],
         400: ['catmix400_u.npy', 'catmix400_final_policy_u.npy'],
         800: ['catmix800_u.npy', 'catmix800_u_snap.npy', 'catmix800_final_policy_u.npy']}
for N in [int(v) for v in sys.argv[1:]]:
    a, b, c = read(N)
    print('N=%d a=%s b=%s c=%s  c-9a=%s (>0: %s)' % (N, a, b, c, c - 9 * a, c - 9 * a > 0), flush=True)
    for fn in files[N]:
        u = np.load(fn)
        assert u.shape == (N + 1,) and np.all((u >= 0) & (u <= 1))
        uf = [F(float(v)) for v in u]
        t0 = time.time()
        J = sim(uf, a, b, c)
        Jg = sim(uf, a, b, 9 * a)
        s = fl30(J); sg = fl30(Jg)
        print('  %-30s J_osil in [%de-30, %de-30]  J_9a - J_osil = %.4e  float(J)=%r  (%.1fs)' % (fn, s, s + 1, float(Jg - J), float(J), time.time() - t0), flush=True)
