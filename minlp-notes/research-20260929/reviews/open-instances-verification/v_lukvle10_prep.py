"""lukvle10: structure check, primal evaluation of MINLPLib points, own KKT multipliers.

Model (checked from the OSIL exactly):
  min sum_{i=0}^{499} f(x_{2i}, x_{2i+1}),  f(a,b) = (a^2)^(b^2+1) + (b^2)^(a^2+1)
  c_j = -x_j + 3 x_{j+1} - 2 x_{j+2} - 2 x_{j+1}^2 + 1 = 0,  j = 0..997, all x free.
Lagrangian L = f + sum_j lam_j c_j.  KKT: grad f + J^T lam = 0, solved by least squares at p5.
"""
import os
import json
import numpy as np
import mpmath
from mpmath import mp, mpf
import osilx

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
AUTH = _REPO + '/research-20260929/open-instances/'
n = 1000


def check_structure(I):
    assert len(I['names']) == n and len(I['cons']) == n - 2
    assert all((I['lb'][j], I['ub'][j]) == ('-INF', 'INF') for j in range(n))
    o = I['obj']
    assert not o['lin'] and not o['quad'] and o['constant'] == '0' and o['sense'] == 'min'
    t = o['nl']
    assert t[0] == 'sum' and len(t) == 1 + n
    for i in range(500):
        a, b = 2 * i, 2 * i + 1
        assert t[1 + 2 * i] == ('power', ('square', ('var', a, '1')), ('sum', ('square', ('var', b, '1')), ('num', '1')))
        assert t[2 + 2 * i] == ('power', ('square', ('var', b, '1')), ('sum', ('square', ('var', a, '1')), ('num', '1')))
    for j, c in enumerate(I['cons']):
        assert (c['lb'], c['ub'], c['constant'], c['nl']) == ('-1', '-1', '0', None)
        assert c['lin'] == {j: '-1', j + 1: '3', j + 2: '-2'} and c['quad'] == [(j + 1, j + 1, '-2')]


def fpair(a, b):
    return (a * a) ** (b * b + 1) + (b * b) ** (a * a + 1)


def evaluate(x):
    mp.dps = 50
    obj = sum(fpair(x[2 * i], x[2 * i + 1]) for i in range(500))
    viol = max(abs(-x[j] + 3 * x[j + 1] - 2 * x[j + 2] - 2 * x[j + 1] ** 2 + 1) for j in range(n - 2))
    return obj, viol


def read_sol(I, path):
    idx = {nm: j for j, nm in enumerate(I['names'])}
    x = [mpf(0)] * n
    for line in open(path):
        nm, val = line.split()
        if nm != 'objvar':
            x[idx[nm]] = mpf(val)
    return x


def grad_f(x):
    g = np.zeros(n)
    for i in range(500):
        a, b = x[2 * i], x[2 * i + 1]
        A, B = a * a, b * b
        # d/da [A^(B+1)] = (B+1) A^B 2a ; d/da [B^(A+1)] = B^(A+1) ln(B) 2a
        ga = (B + 1) * A ** B * 2 * a + (B ** (A + 1) * np.log(B) * 2 * a if B > 0 else 0.0)
        gb = (A + 1) * B ** A * 2 * b + (A ** (B + 1) * np.log(A) * 2 * b if A > 0 else 0.0)
        g[2 * i], g[2 * i + 1] = ga, gb
    return g


def kkt_multipliers(x):
    g = grad_f(x)
    Jt = np.zeros((n, n - 2))
    for j in range(n - 2):
        Jt[j, j] = -1.0
        Jt[j + 1, j] = 3 - 4 * x[j + 1]
        Jt[j + 2, j] = -2.0
    lam, *_ = np.linalg.lstsq(Jt, -g, rcond=None)
    res = np.max(np.abs(Jt @ lam + g))
    return lam, res


def main():
    I = osilx.read(P + 'lukvle10.osil')
    check_structure(I)
    out = {}
    for p in ['p1', 'p5']:
        x = read_sol(I, AUTH + f'minlplib_sol/lukvle10.{p}.sol')
        o, v = evaluate(x)
        out[p] = dict(obj=mpmath.nstr(o, 16), viol=mpmath.nstr(v, 3))
    x5 = np.array([float(v) for v in read_sol(I, AUTH + 'minlplib_sol/lukvle10.p5.sol')])
    lam, res = kkt_multipliers(x5)
    out['kkt_residual'] = float(res)
    out['lam_range'] = [float(lam.min()), float(lam.max())]
    out['q_min'] = float((-2 * lam).min())
    out['x5_mid_range'] = [float(x5[40:960].min()), float(x5[40:960].max())]
    out['lam_mid_spread_30_960'] = float(lam[30:961].max() - lam[30:961].min())
    np.save('logs/lukvle10_lam_kkt.npy', lam)
    np.save('logs/lukvle10_x5.npy', x5)
    print(json.dumps(out, indent=1))
    json.dump(out, open('logs/lukvle10_prep.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
