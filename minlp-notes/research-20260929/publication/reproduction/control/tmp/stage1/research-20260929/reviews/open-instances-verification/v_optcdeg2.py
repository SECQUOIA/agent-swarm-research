"""Independent verification of the optcdeg2 dual bound (Lagrangian + exact head block).

Model (checked from the OSIL with exact strings; N = 50000):
  min 2e-4 * sum_{t=0}^{N} y_t^2
  Y_t: y_{t+1} - y_t - 4e-4 v_t = 0
  V_t: v_{t+1} - v_t - 4e-4 u_t + 8e-6 y_t + 8e-5 v_t^2 = 0
  y_0 = 10, v_0 = 0, v_N = 0, v_t >= -1 (1 <= t <= N-1), u_t in [-.2, .2], y free.
Certificate data: the authors' multiplier arrays (mu_t for Y_t, lam_t for V_t);
any multipliers give a valid bound, so only the arithmetic has to be checked.
Everything below is my own code in mpmath interval arithmetic (iv, 100 bits):
  * feasible-state bounds by forward + backward interval propagation;
  * separable Lagrangian terms;
  * head block t < m: reachable intervals over the whole control box,
    interval adjoint, sign check of dJ/du_t, corner trajectory J(-0.2,...).
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import json, sys, time, pickle, os
import numpy as np
import mpmath
from mpmath import iv, mp, mpf
import osilx

P = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
AUTH = _REPO + '/research-20260929/open-instances/'
N = 50000
iv.prec = 100
mp.prec = 100


def layout():
    u = list(range(0, N - 1)) + [50000]
    y = list(range(50001, 50001 + N + 1))
    v = list(range(100002, 100002 + N)) + [49999]
    return u, y, v


def check_structure(I):
    u, y, v = layout()
    n = len(I['names'])
    assert n == 3 * N + 2 and len(I['cons']) == 2 * N
    assert sorted(u + y + v) == list(range(n))
    o = I['obj']
    assert o['sense'] == 'min' and not o['lin'] and o['nl'] is None and o['constant'] == '0'
    assert sorted(o['quad']) == sorted((j, j, '2e-4') for j in y)
    for t in range(N):
        assert (I['lb'][u[t]], I['ub'][u[t]]) == ('-.2', '.2')
    for t in range(N + 1):
        assert (I['lb'][y[t]], I['ub'][y[t]]) == (('10', '10') if t == 0 else ('-INF', 'INF'))
    assert (I['lb'][v[0]], I['ub'][v[0]]) == ('0', '0')
    assert (I['lb'][v[N]], I['ub'][v[N]]) == ('0', '0')
    for t in range(1, N):
        assert (I['lb'][v[t]], I['ub'][v[t]]) == ('-1', 'INF')
    for t in range(N):
        c = I['cons'][t]
        assert (c['lb'], c['ub'], c['nl'], c['quad'], c['constant']) == ('0', '0', None, [], '0')
        assert c['lin'] == {y[t]: '-1', y[t + 1]: '1', v[t]: '-4e-4'}, t
        c = I['cons'][N + t]
        assert (c['lb'], c['ub'], c['nl'], c['constant']) == ('0', '0', None, '0')
        assert c['lin'] == {v[t]: '-1', v[t + 1]: '1', u[t]: '-4e-4', y[t]: '8e-6'}, t
        assert c['quad'] == [(v[t], v[t], '8e-5')], t


# exact decimal constants as intervals
HY = iv.mpf('4e-4')
CU = iv.mpf('4e-4')
CY = iv.mpf('8e-6')
CV = iv.mpf('8e-5')
COBJ = iv.mpf('2e-4')
UB = iv.mpf('0.2')


def ivbox(lo, hi):
    return iv.mpf([lo, hi])


def lo(x):
    return mp.make_mpf(x._mpi_[0])


def hi(x):
    return mp.make_mpf(x._mpi_[1])


def inter(a, b):
    l = max(lo(a), lo(b)); h = min(hi(a), hi(b))
    assert l <= h, 'empty intersection'
    return iv.mpf([l, h])


UBOX = iv.mpf(['-0.2', '0.2'])


def g_img(V):
    """image of v - cv v^2 over V (increasing for v < 1/(2cv) = 6250)"""
    assert hi(V) < 6000
    a = iv.mpf(lo(V)); b = iv.mpf(hi(V))
    ga = a - CV * a * a; gb = b - CV * b * b
    return iv.mpf([lo(ga), hi(gb)])


def g_inv(W):
    """preimage on the branch v < 6250: v = 2w / (1 + sqrt(1 - 4 cv w)), increasing in w"""
    assert hi(W) < 3000
    a = iv.mpf(lo(W)); b = iv.mpf(hi(W))
    fa = 2 * a / (1 + iv.sqrt(1 - 4 * CV * a))
    fb = 2 * b / (1 + iv.sqrt(1 - 4 * CV * b))
    return iv.mpf([lo(fa), hi(fb)])


def state_bounds():
    Y = [None] * (N + 1); V = [None] * (N + 1)
    Y[0] = iv.mpf(10); V[0] = iv.mpf(0)
    for t in range(N):
        Y[t + 1] = Y[t] + HY * V[t]
        Vn = g_img(V[t]) + CU * UBOX - CY * Y[t]
        if t + 1 < N:
            Vn = inter(Vn, iv.mpf([-1, mpmath.inf]))
        else:
            Vn = inter(Vn, iv.mpf(0))
        V[t + 1] = Vn
    V[N] = iv.mpf(0)
    for t in range(N - 1, 0, -1):
        Y[t] = inter(Y[t], Y[t + 1] - HY * V[t])
        W = V[t + 1] - CU * UBOX + CY * Y[t]
        V[t] = inter(V[t], g_inv(W))
    return Y, V


def ymin(c):
    """min over free y of COBJ y^2 + c y  =  -c^2 / (4 COBJ)"""
    return -(c * c) / (4 * COBJ)


def vmin(A, B, Vt):
    """rigorous lower bound of min_{v in Vt} A v^2 + B v"""
    a = iv.mpf(lo(Vt)); b = iv.mpf(hi(Vt))
    fa = A * a * a + B * a
    fb = A * b * b + B * b
    ends = min(lo(fa), lo(fb))
    if lo(A) > 0:
        vs = -B / (2 * A)
        if hi(vs) < lo(Vt) or lo(vs) > hi(Vt):
            return ends
        return min(ends, lo(-(B * B) / (4 * A)))
    if hi(A) < 0:
        return ends
    return lo(A * Vt * Vt + B * Vt)  # A contains 0: natural enclosure (never hit here)


def rest_terms(lam, mu, V, m):
    """sum of separable terms for rows t >= m dualized (m >= 0); head handled separately."""
    L = [iv.mpf(float(x)) for x in lam]
    M = [iv.mpf(float(x)) for x in mu]
    s = iv.mpf(0)
    for t in range(m, N):
        s += -UB * CU * abs(L[t])
    for t in range(m + 1, N):
        s += ymin(M[t - 1] - M[t] + CY * L[t])
        s += vmin(CV * L[t], L[t - 1] - L[t] - HY * M[t], V[t])
    s += ymin(M[N - 1])
    return s


def head(lam, mu, m):
    """exact head block t < m: returns (monotone?, min lower p_v, J_corner interval)"""
    Lm = iv.mpf(float(lam[m])); Mm = iv.mpf(float(mu[m]))
    # reachable intervals over the whole box (no feasibility intersection)
    Yh = [iv.mpf(10)]; Vh = [iv.mpf(0)]
    for k in range(m):
        Yh.append(Yh[k] + HY * Vh[k])
        Vh.append(Vh[k] - CV * Vh[k] * Vh[k] + CU * UBOX - CY * Yh[k])
    # interval adjoint
    py = 2 * COBJ * Yh[m] - Mm + CY * Lm
    pv = -HY * Mm - Lm + 2 * CV * Lm * Vh[m]
    minpv = lo(pv)
    for k in range(m - 1, 0, -1):
        py, pv = 2 * COBJ * Yh[k] + py - CY * pv, HY * py + (1 - 2 * CV * Vh[k]) * pv
        minpv = min(minpv, lo(pv))
    # corner trajectory u = -0.2
    y = iv.mpf(10); v = iv.mpf(0); J = iv.mpf(0)
    for k in range(m):
        J += COBJ * y * y
        y, v = y + HY * v, v - CV * v * v - CU * UB - CY * y
    J += COBJ * y * y + (-Mm + CY * Lm) * y + (-HY * Mm - Lm) * v + CV * Lm * v * v
    vr = (float(min(lo(x) for x in Vh)), float(max(hi(x) for x in Vh)))
    return minpv > 0, minpv, J, vr


def simulate_point(I, u_arr):
    """states from controls by forward recursion in 40 digits, rounded to double; v_N set to 0."""
    uu, yy, vv = layout()
    mp.dps = 40
    x = [mpf(0)] * (3 * N + 2)
    y = mpf(10); v = mpf(0)
    ud = [mpf(float(a)) for a in u_arr]
    for t in range(N):
        x[uu[t]] = ud[t]; x[yy[t]] = y; x[vv[t]] = v
        yn = mpf(float(y + mpf('4e-4') * v))
        vn = v + mpf('4e-4') * ud[t] - mpf('8e-6') * y - mpf('8e-5') * v * v
        y, v = yn, (mpf(float(vn)) if t < N - 1 else vn)
    x[yy[N]] = mpf(float(y))
    vN = v
    x[vv[N]] = mpf(0)
    x[vv[0]] = mpf(0); x[yy[0]] = mpf(10)
    return x, vN


def evaluate(I, x):
    mp.dps = 50
    num = mpf
    rv = mpf(0); worst = None
    for i, c in enumerate(I['cons']):
        val = abs(osilx.ev_row(c, x, num, {}))
        if val > rv:
            rv, worst = val, c['name']
    bv = mpf(0)
    for j in range(len(x)):
        l, h = I['lb'][j], I['ub'][j]
        if not osilx.isinf(l):
            bv = max(bv, mpf(l) - x[j])
        if not osilx.isinf(h):
            bv = max(bv, x[j] - mpf(h))
    obj = osilx.ev_row(I['obj'], x, num, {})
    mp.prec = 100
    return obj, rv, bv, worst


def read_sol(I, path):
    idx = {nm: j for j, nm in enumerate(I['names'])}
    x = [mpf(0)] * len(I['names'])
    for line in open(path):
        nm, val = line.split()
        if nm != 'objvar':
            x[idx[nm]] = mpf(val)
    return x


def main():
    t0 = time.time()
    I = osilx.read(P + 'optcdeg2.osil')
    check_structure(I)
    out = {}
    lam = np.load(AUTH + 'logs/optcdeg2_lam.npy')
    mu = np.load(AUTH + 'logs/optcdeg2_mu.npy')
    assert lam.shape == (N,) and mu.shape == (N,)
    out['lam_sign_changes'] = [int(i) for i in np.where(np.diff(np.sign(lam)) != 0)[0]]
    Y, V = state_bounds()
    out['t_state_bounds'] = time.time() - t0
    out['V_hi_max'] = float(max(hi(x) for x in V))
    out['Y_range_end'] = [float(lo(Y[N])), float(hi(Y[N]))]
    # compare with authors' state bounds (information only)
    vb = np.load(AUTH + 'logs/optcdeg2_vbounds.npy')
    out['max_abs_diff_Vbounds_vs_authors'] = float(max(max(abs(float(lo(V[t])) - vb[t, 0]), abs(float(hi(V[t])) - vb[t, 1])) for t in range(N + 1)))
    # full Lagrangian (m = 0)
    J0 = iv.mpf(0) + COBJ * 100 + (-iv.mpf(float(mu[0])) + CY * iv.mpf(float(lam[0]))) * 10
    full = J0 + rest_terms(lam, mu, V, 0)
    out['full_lagrangian'] = [mpmath.nstr(lo(full), 13), mpmath.nstr(hi(full), 13)]
    print(json.dumps(out), flush=True)
    for m in [2800, 3000, 3080, 3090, 3100]:
        mono, minpv, J, vr = head(lam, mu, m)
        r = rest_terms(lam, mu, V, m)
        tot = J + r
        rec = dict(m=m, monotone=bool(mono), min_pv_lower=float(minpv), J_corner=float(lo(J)),
                   rest=float(lo(r)), bound=mpmath.nstr(lo(tot), 13) if mono else None,
                   head_v_range=vr)
        out.setdefault('head', []).append(rec)
        print(json.dumps(rec), flush=True)
    # primal points
    u_arr = np.load(AUTH + 'logs/optcdeg2_primal_u.npy')
    x, vN = simulate_point(I, u_arr)
    o, rv, bv, worst = evaluate(I, x)
    out['authors_primal'] = dict(obj=mpmath.nstr(o, 15), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3),
                                 worst=worst, simulated_vN=mpmath.nstr(vN, 3))
    xs = read_sol(I, AUTH + 'minlplib_sol/optcdeg2.p1.sol')
    o, rv, bv, worst = evaluate(I, xs)
    out['minlplib_p1'] = dict(obj=mpmath.nstr(o, 15), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3), worst=worst)
    out['seconds'] = time.time() - t0
    print(json.dumps(out, indent=1))
    json.dump(out, open('logs/optcdeg2_verify.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
