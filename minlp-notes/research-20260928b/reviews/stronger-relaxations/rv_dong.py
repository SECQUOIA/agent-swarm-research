"""Check 9 (revision check): my own implementation of Dong's exact SDP1 root-exactness test
(Theorem 2 of arXiv 1603.04572) at the OPT support S, compared with the stored SDP1 values
(rule: exact iff OPT - SDP1 <= 1e-6 OPT).  Test: with a = X' r_S and A = X'X/lam + I,
SDP1 is exact at S iff min_{t>0} lambda_max(diag(d(t)) - A) <= 0, where d_i = t/a_i^2 on S and
d_l = a_l^2/t off S (Dong's reduction; lambda_max(...) is convex in t).  Feasible t lie in
[max_l a_l^2/A_ll, min_S a_i^2 A_ii]."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    _os.environ[_v] = "1"
import json, os
import numpy as np
from scipy.optimize import minimize_scalar
from rv_common import gen_nested, fval

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bb-complexity', 'sparse-regression',
                 'stronger-relaxations', 'data')


def dong_exact(X, y, lam, S):
    S = list(S)
    _, _, r = fval(X, y, lam, S)
    a = X.T @ r
    p = X.shape[1]
    A = X.T @ X / lam + np.eye(p)
    off = np.setdiff1d(np.arange(p), S)
    if np.any(np.abs(a[S]) < 1e-14):
        return False, np.inf
    lo = np.max(a[off] ** 2 / np.diag(A)[off])
    hi = np.min(a[S] ** 2 * np.diag(A)[S])
    if lo > hi:
        return False, lo / hi

    def f(u):
        t = np.exp(u)
        d = np.empty(p); d[S] = t / a[S] ** 2; d[off] = a[off] ** 2 / t
        return np.linalg.eigvalsh(np.diag(d) - A)[-1]
    res = minimize_scalar(f, bounds=(np.log(lo), np.log(hi)), method='bounded', options=dict(xatol=1e-12))
    val = min(res.fun, f(np.log(lo)), f(np.log(hi)))
    return bool(val <= 1e-9 * np.abs(A).max()), float(val)


out = []
for n, fn, ofn in [(20, 'mech_n20_k3.jsonl', 'opt_mech_n20_k3.jsonl'), (40, 'mech_n40_k3.jsonl', 'opt_mech_n40_k3.jsonl')]:
    opt = {(o['p'], o['seed']): o for o in map(json.loads, open(os.path.join(D, ofn)))}
    for r in map(json.loads, open(os.path.join(D, fn))):
        if r.get('sdp1') is None or (r['p'], r['seed']) not in opt or 'OPT' not in opt[(r['p'], r['seed'])]:
            continue
        o = opt[(r['p'], r['seed'])]
        X, y, lam, S = gen_nested(n, 3, 3200 if n == 40 else 2560, r['p'], r['seed'])
        assert abs(fval(X, y, lam, S)[0] - r['fS']) < 1e-9 * r['fS']
        ex, val = dong_exact(X, y, lam, o['OPT_support'])
        rule = (o['OPT'] - r['sdp1']) / o['OPT'] <= 1e-6
        out.append((n, r['p'], r['seed'], ex, rule, val))
agree = sum(e == ru for *_, e, ru, _v in out)
print('rows', len(out), 'agreement', agree)
for n, p, s, e, ru, v in sorted(out):
    print(n, p, s, 'dong_exact' if e else 'dong_inexact', 'rule_exact' if ru else 'rule_inexact', '%.3e' % v)
