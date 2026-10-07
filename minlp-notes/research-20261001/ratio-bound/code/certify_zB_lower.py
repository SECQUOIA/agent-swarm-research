"""Exact lower-bound certificate for family (B) on the Theorem B family (Theorem B2(2) of the note).

Normalized frame of sbar = (0, 0, eps): P1 = (rho, -rho, 1), P2 = (rho, -2 rho, 1), P3 = (rho, rho, 1 + rho/sqrt(eps))
are the vertices of T_r, r = rho sqrt(eps) / z_K.  For one explicit rational X (found by the heuristic (B)
search, zB_extended.py) this script checks in exact arithmetic:
  (i)   sym(X) is positive definite, so sbar = (0, 0, 1) lies in the interior of C_X (hence of B_X) and det X > 0;
  (ii)  sym(X M(P_i - tau_i e_w)) is PSD for explicit rational tau_i in [0, q(P_i)], i = 1, 2, so P1, P2 lie in B_X;
  (iii) sym(X M(rho, rho, h0)) is PSD for an explicit rational h0, so (rho, rho, h) lies in B_X for every
        h >= h0 (upward closure); P3 qualifies when 1 + rho/sqrt(eps) >= h0.
Conclusion: for every eps <= (rho/(h0 - 1))^2, z_B / z_K >= rho sqrt(eps) / z_K(eps).
usage: python3 certify_zB_lower.py"""
from fractions import Fraction as Fr
import numpy as np

X0 = np.array([[1.0, -1.678587], [0.007315, 0.698332]])     # zB_extended.log (eps = 1e-5, 1e-6, 1e-8)
RHO = Fr(273, 2)                                            # 136.5


def M(s):
    x, y, w = s
    return [[w, x], [y, Fr(1)]]


def symXN(X, N):
    a = X[0][0] * N[0][0] + X[0][1] * N[1][0]
    b = X[0][0] * N[0][1] + X[0][1] * N[1][1]
    c = X[1][0] * N[0][0] + X[1][1] * N[1][0]
    d = X[1][0] * N[0][1] + X[1][1] * N[1][1]
    return a, (b + c) / 2, d


def psd(S):
    a, b, d = S
    return a >= 0 and d >= 0 and a * d - b * b >= 0


def pd(S):
    a, b, d = S
    return a > 0 and a * d - b * b > 0


def lmin(S):
    a, b, d = (float(t) for t in S)
    return 0.5 * (a + d) - np.sqrt(0.25 * (a - d) ** 2 + b * b)


def best_param(f, lo, hi, n=4000):
    """grid + golden refinement of a concave function on [lo, hi] (floats); returns the argmax"""
    xs = np.linspace(lo, hi, n)
    k = int(np.argmax([f(x) for x in xs]))
    a, b = xs[max(k - 1, 0)], xs[min(k + 1, n - 1)]
    g = (np.sqrt(5) - 1) / 2
    for _ in range(200):
        m1, m2 = b - g * (b - a), a + g * (b - a)
        if f(m1) >= f(m2):
            b = m2
        else:
            a = m1
    return 0.5 * (a + b)


def main():
    X = [[Fr(X0[i, j]).limit_denominator(10 ** 6) for j in range(2)] for i in range(2)]
    E = [[Fr(1), Fr(0)], [Fr(0), Fr(0)]]
    rho = RHO
    checks = {}
    checks['sym(X) positive definite (sbar interior, det X > 0)'] = pd(symXN(X, [[1, 0], [0, 1]]))
    detX = X[0][0] * X[1][1] - X[0][1] * X[1][0]
    taus = []
    for name, P in (('P1', (rho, -rho, Fr(1))), ('P2', (rho, -2 * rho, Fr(1)))):
        q = P[2] - P[0] * P[1]
        f = lambda t: lmin(symXN(X, M((P[0], P[1], P[2] - Fr(t)))))
        t = Fr(best_param(f, 0.0, float(q))).limit_denominator(10 ** 4)
        S = symXN(X, M((P[0], P[1], P[2] - t)))
        checks['%s - tau e_w in C_X with tau = %s in [0, q] (q = %s)' % (name, t, q)] = (0 <= t <= q) and psd(S)
        taus.append(t)
    fh = lambda h: lmin(symXN(X, M((rho, rho, Fr(h)))))
    h0 = Fr(best_param(fh, float(rho * rho), float(rho * rho) + 1e5)).limit_denominator(10)
    checks['(rho, rho, h0) in C_X with h0 = %s' % h0] = psd(symXN(X, M((rho, rho, h0))))
    eps0 = (rho / (h0 - 1)) ** 2
    print('X =', [[str(t) for t in r] for r in X], ' det X =', detX)
    print('rho =', rho, ' tau1, tau2 =', [str(t) for t in taus], ' h0 =', h0)
    print('valid for eps <= (rho/(h0 - 1))^2 =', eps0, '= %.4e' % float(eps0))
    for k, v in checks.items():
        print(k, ':', 'PASS' if v else 'FAIL')
    print('ALL PASS' if all(checks.values()) else 'SOME FAIL')


if __name__ == '__main__':
    main()
