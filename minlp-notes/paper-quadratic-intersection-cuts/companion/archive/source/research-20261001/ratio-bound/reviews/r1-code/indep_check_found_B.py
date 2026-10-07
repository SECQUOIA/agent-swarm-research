"""Reviewer: independent membership check of the best (B) sets reported for the near-tangent families
(logs/tangent_family_eta*.log), in the normalized frame, at rho = (D z_B / z_K) / sqrt(k) * (1 - 1e-6).
A point s lies in B_X iff some s - tau e_w, 0 <= tau <= q(s), lies in C_X = {sym(X M) >= 0}; the minimum
eigenvalue is concave in tau, so it is maximized by golden section."""
import json, numpy as np
def M(s): return np.array([[s[2], s[0]], [s[1], 1.0]])
def lmin(X, s):
    A = X @ M(s); S = (A + A.T) / 2
    return np.linalg.eigvalsh(S)[0]
def best_lower(X, s):
    qq = s[2] - s[0]*s[1]
    f = lambda t: lmin(X, (s[0], s[1], s[2] - t))
    a, b = 0.0, qq; g = (np.sqrt(5) - 1) / 2
    for _ in range(200):
        m1, m2 = b - g*(b - a), a + g*(b - a)
        if f(m1) >= f(m2): b = m2
        else: a = m1
    return max(f(0.0), f(qq), f(0.5*(a + b)))
ok = True
for fn in ['tangent_family_eta0.001_k4.log', 'tangent_family_eta0.01_k4.log', 'tangent_family_eta0.001_k2.25.log', 'tangent_family_eta0.001_k1.96_L30.log']:
    for line in open('../../logs/' + fn):
        d = json.loads(line)
        eta, k, L = d['eta'], d['k'], d['L']
        X = np.array(d['XB'])
        rho = d['D_times']['zB_found'] / np.sqrt(k) * (1 - 1e-6)
        sk = np.sqrt(k)
        pts = {'sbar': (0, 0, 1.0), 'P1': (rho, -rho, 1 - 2*rho*(1 - eta)), 'P2': (rho, -k*rho, 1 - 2*sk*rho*(1 - eta)),
               'P3': (rho, rho, 1 + rho*L)}
        vals = {n: best_lower(X, p) for n, p in pts.items()}
        good = all(v >= -1e-9 for v in vals.values()) and np.linalg.det(X) > 0
        # sbar interior of B_X: some lowered point of sbar strictly inside C_X ... checked as lmin > 0 for tau in (0, q)
        interior = best_lower(X, (0, 0, 1.0)) > 1e-12  # tiny but positive margins: sbar is within ~1e-9 of the boundary
        ok &= good and interior
        print('%s L=%g rho=%.6f D z_B=%.5f  minlam: %s  sbar-interior %s -> %s' % (fn, L, rho, d['D_times']['zB_found'],
              ' '.join('%s %.2e' % kv for kv in vals.items()), interior, 'OK' if good and interior else 'FAIL'))
print('ALL OK' if ok else 'SOME FAIL')
