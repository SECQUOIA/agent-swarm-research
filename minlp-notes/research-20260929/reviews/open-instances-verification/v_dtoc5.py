"""Independent verification of the dtoc5 dual bound and primal value.

Model (checked below from the OSIL, exact strings):
  min sum_{t<T} 2e-5 (u_t^2 + y_t^2),  T = 49999, y_0 = 1 (fixed), all else free
  -2e-5 u_t + y_t - y_{t+1} + 8e-5 y_t^2 = 0,  t = 0..T-1.
Own primal: damped Newton on the reduced problem in y (tridiagonal Hessian).
Multipliers lam_t = -2 u_t with lam_{T-1} = 0 forced.  Dual function
  d(lam) = h(1-4lam_0) - lam_0 - (h/4) sum lam_t^2
           - sum_{t=1}^{T-1} (lam_{t-1}-lam_t)^2 / (4h(1-4lam_t))
evaluated in mpmath interval arithmetic with h = 1/50000 exactly.
"""
import os
import json
import numpy as np
from scipy.linalg import solve_banded
import mpmath
from mpmath import mp, iv, mpf
import osilx

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
AUTH = _REPO + '/research-20260929/open-instances/'
T = 49999


def check_structure(I):
    n = len(I['names'])
    assert n == 2 * T + 1 and len(I['cons']) == T
    o = I['obj']
    assert o['sense'] == 'min' and not o['lin'] and o['nl'] is None and o['constant'] == '0'
    assert sorted(o['quad']) == [(j, j, '2e-5') for j in range(2 * T)]  # u_0..u_{T-1}, y_0..y_{T-1}
    for j in range(n):
        assert I['vt'][j] == 'C'
        assert (I['lb'][j], I['ub'][j]) == (('1', '1') if j == T else ('-INF', 'INF')), j
    for t, c in enumerate(I['cons']):
        assert c['lb'] == '0' and c['ub'] == '0' and c['constant'] == '0' and c['nl'] is None
        assert c['lin'] == {t: '-2e-5', T + t: '1', T + t + 1: '-1'}, t
        assert c['quad'] == [(T + t, T + t, '8e-5')], t


def newton_primal():
    h = 2e-5
    y = np.ones(T + 1)
    y[1:] = np.exp(-np.arange(1, T + 1) * h * 1.0)  # rough start

    def J(y):
        r = y[:-1] + 4 * h * y[:-1] ** 2 - y[1:]
        return np.sum(r * r) / h + h * np.sum(y[:-1] ** 2)

    for it in range(100):
        r = y[:-1] + 4 * h * y[:-1] ** 2 - y[1:]
        d = 1 + 8 * h * y[:-1]
        g = np.zeros(T + 1)
        g[:-1] += 2 * r * d / h + 2 * h * y[:-1]
        g[1:] += -2 * r / h
        Hd = np.zeros(T + 1)
        Hd[:-1] += 2 * d * d / h + 16 * r + 2 * h
        Hd[1:] += 2 / h
        Ho = -2 * d / h  # (k, k+1)
        # restrict to y_1..y_T
        gg = g[1:]
        ab = np.zeros((3, T))
        ab[0, 1:] = Ho[1:]      # super diagonal
        ab[1, :] = Hd[1:]
        ab[2, :-1] = Ho[1:]     # sub diagonal
        step = solve_banded((1, 1), ab, -gg)
        f0 = J(y)
        a = 1.0
        while True:
            yn = y.copy(); yn[1:] += a * step
            if J(yn) <= f0 + 1e-4 * a * gg.dot(step) or a < 1e-12:
                break
            a *= 0.5
        y = yn
        if np.max(np.abs(gg)) < 1e-13 and a == 1.0:
            break
    return y, it


def refine_mp(y, steps=3, dps=40):
    """Newton steps on the reduced problem in mpmath (Thomas algorithm)."""
    mp.dps = dps
    H = mpf(1) / 50000
    Y = [mpf(1)] + [mpf(float(v)) for v in y[1:]]
    for s in range(steps):
        r = [Y[t] + 4 * H * Y[t] ** 2 - Y[t + 1] for t in range(T)]
        d = [1 + 8 * H * Y[t] for t in range(T)]
        g = [mpf(0)] * (T + 1); Hd = [mpf(0)] * (T + 1)
        for t in range(T):
            g[t] += 2 * r[t] * d[t] / H + 2 * H * Y[t]
            g[t + 1] += -2 * r[t] / H
            Hd[t] += 2 * d[t] ** 2 / H + 16 * r[t] + 2 * H
            Hd[t + 1] += 2 / H
        Ho = [-2 * d[t] / H for t in range(T)]
        # solve on unknowns k = 1..T: diag Hd[k], off (k,k+1) Ho[k]
        n = T
        a = [Hd[k] for k in range(1, T + 1)]
        b = [Ho[k] for k in range(1, T)]
        rhs = [-g[k] for k in range(1, T + 1)]
        cp = [mpf(0)] * n; dp = [mpf(0)] * n
        cp[0] = b[0] / a[0]; dp[0] = rhs[0] / a[0]
        for i in range(1, n):
            m = a[i] - b[i - 1] * cp[i - 1]
            cp[i] = b[i] / m if i < n - 1 else mpf(0)
            dp[i] = (rhs[i] - b[i - 1] * dp[i - 1]) / m
        xs = [mpf(0)] * n
        xs[-1] = dp[-1]
        for i in range(n - 2, -1, -1):
            xs[i] = dp[i] - cp[i] * xs[i + 1]
        gmax = max(abs(v) for v in g[1:])
        smax = max(abs(v) for v in xs)
        print('mp newton step', s, 'max|grad|', mpmath.nstr(gmax, 3), 'max|step|', mpmath.nstr(smax, 3))
        for k in range(1, T + 1):
            Y[k] += xs[k - 1]
    r = [Y[t] + 4 * H * Y[t] ** 2 - Y[t + 1] for t in range(T)]
    u = [rt / H for rt in r]
    return Y, u


def dual_bound(lam, dps=30):
    iv.dps = dps
    h = iv.mpf(1) / 50000
    L = [iv.mpf(float(v)) for v in lam]
    d = h * (1 - 4 * L[0]) - L[0]
    s1 = iv.mpf(0)
    for v in L:
        s1 += v * v
    d -= h / 4 * s1
    s2 = iv.mpf(0)
    for t in range(1, T):
        diff = L[t - 1] - L[t]
        s2 += diff * diff / (4 * h * (1 - 4 * L[t]))
    d -= s2
    return d


def evaluate(I, x):
    mp.dps = 50
    num = mpf
    rv = mpf(0)
    for c in I['cons']:
        v = osilx.ev_row(c, x, num, {})
        rv = max(rv, abs(v))
    obj = osilx.ev_row(I['obj'], x, num, {})
    bv = abs(x[T] - 1)
    return obj, rv, bv


def point_from_y(y):
    h = 2e-5
    yd = [float(v) for v in y]
    yd[0] = 1.0
    x = [mpf(0)] * (2 * T + 1)
    mp.dps = 50
    H = mpf(1) / 50000
    for t in range(T):
        u = (mpf(yd[t]) + 4 * H * mpf(yd[t]) ** 2 - mpf(yd[t + 1])) / H
        x[t] = mpf(float(u))
    for t in range(T + 1):
        x[T + t] = mpf(yd[t])
    return x


def main():
    I = osilx.read(P + 'dtoc5.osil')
    check_structure(I)
    y, its = newton_primal()
    Y, U = refine_mp(y)
    y = np.array([float(v) for v in Y])
    u = np.array([float(v) for v in U])
    lam = np.array([float(-2 * v) for v in U])
    lam[-1] = 0.0
    out = dict(newton_iters=its, u_min=float(u.min()), u_max=float(u.max()), lam_max=float(lam.max()),
               y_min=float(y.min()), y_max=float(y.max()), u_last=float(u[-1]))
    assert lam.max() < 0.25
    d = dual_bound(lam)
    out['dual_bound'] = [mpmath.nstr(d.a, 17), mpmath.nstr(d.b, 17)]
    x = point_from_y(y)
    o, rv, bv = evaluate(I, x)
    out['own_primal'] = dict(obj=mpmath.nstr(o, 17), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3))
    ya = np.load(AUTH + 'logs/dtoc5_y.npy')
    out['authors_y_len'] = int(len(ya))
    xa = point_from_y(ya)
    o, rv, bv = evaluate(I, xa)
    out['authors_primal_from_y'] = dict(obj=mpmath.nstr(o, 17), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3))
    out['max_abs_y_diff_vs_authors'] = float(np.max(np.abs(ya - y)))
    print(json.dumps(out, indent=1))
    json.dump(out, open('logs/dtoc5_verify.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
