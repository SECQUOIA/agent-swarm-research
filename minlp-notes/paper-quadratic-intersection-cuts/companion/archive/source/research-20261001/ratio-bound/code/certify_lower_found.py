"""Exact lower-bound certificates for family (B) from the best sets found by the heuristic searches
(revision after review round 1; generalizes certify_zB_lower.py, which is kept unchanged).

For a family ('B' = Theorem B family; 'tan:ETA:K' = near-tangent family of Theorem B3), a target rho and a
matrix X copied from a log (taken as the exact decimal printed there), the script checks in exact rational
arithmetic:
  (i)   sym(X) is positive definite: sbar = (0, 0, 1) lies in int C_X, hence in int B_X, and det X > 0,
        so B_X = cl(C_X + R_+ e_w) is a family-(B) set;
  (ii)  sym(X M(P_1)) and sym(X M(P_2)) are PSD: P_1, P_2 lie in C_X (no lowering is used);
  (iii) sym(X M(rho, rho, h0)) is PSD for a rational h0: (rho, rho, h) lies in B_X for every h >= h0.
Then B_X contains sbar, P_1, P_2 and P_3 = (rho, rho, h3) whenever h3 >= h0, hence (convexity) the simplex T_r,
and its single-cut bound is at least r z_K:
  'B'         : P_3 = (rho, rho, 1 + rho/sqrt(eps)), r = rho sqrt(eps)/z_0; valid for eps <= (rho/(h0 - 1))^2;
                so z_B/z_K >= rho sqrt(eps)/z_0, i.e. D z_B/z_K >= sqrt(2) rho  (D = z_0 sqrt(2/eps)).
  'tan:ETA:K' : P_3 = (rho, rho, 1 + rho L), r = rho/z_K; valid for L >= L0 = (h0 - 1)/rho;
                so z_B/z_K >= rho/z_K, i.e. D z_B/z_K >= sqrt(K) rho  (D = sqrt(K) z_K).
Since (i)-(iii) are closed under shrinking rho for the simplex (T_r' is contained in T_r for r' <= r), the
same X also gives valid sets at every smaller rho (with the same h0 bound on the height of P_3).
h0 is chosen by a floating-point golden-section search for the largest smallest eigenvalue in (iii) and
then rounded; only the exact checks matter.
usage: python3 certify_lower_found.py"""
from fractions import Fraction as Fr
import numpy as np

# family, target rho, X (exact decimals as printed in the log), source log
CASES = [
    ('B', Fr(1367, 10), [['1', '-1.678587'], ['0.007315', '0.698332']], 'logs/zB_extended.log'),
    ('tan:1/1000:4', Fr(9844, 10000), [['1.00000003', '-2.11841757'], ['1.01581925', '0.30393078']],
     'logs/tangent_family_eta0.001_k4.log'),
    ('tan:1/100:4', Fr(12234, 10000), [['1.0', '-2.08684938'], ['0.81738698', '0.4028837']],
     'logs/tangent_family_eta0.01_k4.log'),
    ('tan:1/1000:9/4', Fr(10414, 10000), [['1.0', '-2.43916573'], ['0.96020732', '0.5468295']],
     'logs/tangent_family_eta0.001_k2.25.log'),
    ('tan:1/1000:49/25', Fr(10772, 10000), [['1.0', '-2.51367434'], ['0.9282616', '0.62838339']],
     'logs/tangent_family_eta0.001_k1.96_L30.log'),
]


def sqrt_frac(k):
    s = Fr(int(round(k.numerator ** 0.5)), int(round(k.denominator ** 0.5)))
    assert s * s == k
    return s


def pts(spec, rho):
    """exact P_1, P_2 in the normalized frame; same formulas as certify_zB.family_points_exact"""
    r = Fr(rho)
    if spec == 'B':
        return (r, -r, Fr(1)), (r, -2 * r, Fr(1))
    _, eta, k = spec.split(':')
    eta, k = Fr(eta), Fr(k)
    sk = sqrt_frac(k)
    return (r, -r, 1 - 2 * r * (1 - eta)), (r, -k * r, 1 - 2 * sk * r * (1 - eta))


def symXN(X, N):
    a = X[0][0] * N[0][0] + X[0][1] * N[1][0]
    b = X[0][0] * N[0][1] + X[0][1] * N[1][1]
    c = X[1][0] * N[0][0] + X[1][1] * N[1][0]
    d = X[1][0] * N[0][1] + X[1][1] * N[1][1]
    return a, (b + c) / 2, d


def Mq(s):
    return [[s[2], s[0]], [s[1], Fr(1)]]


def psd(S):
    a, b, d = S
    return a >= 0 and d >= 0 and a * d - b * b >= 0


def pd(S):
    a, b, d = S
    return a > 0 and a * d - b * b > 0


def lmin(S):
    a, b, d = (float(t) for t in S)
    return 0.5 * (a + d) - np.sqrt(0.25 * (a - d) ** 2 + b * b)


def golden(f, a, b, it=200):
    g = (np.sqrt(5) - 1) / 2
    for _ in range(it):
        m1, m2 = b - g * (b - a), a + g * (b - a)
        if f(m1) >= f(m2):
            b = m2
        else:
            a = m1
    return 0.5 * (a + b)


def main():
    allok = True
    for spec, rho, Xs, src in CASES:
        X = [[Fr(v) for v in row] for row in Xs]
        p1, p2 = pts(spec, rho)
        rf = float(rho)
        # best height: lmin(sym(X M(rho, rho, h))) is concave in h; search on [rho^2, rho^2 + span]
        span = 1e5 if spec == 'B' else 100.0
        f = lambda h: lmin(symXN(X, Mq((rho, rho, Fr(h)))))
        hs = np.linspace(rf * rf, rf * rf + span, 20001)
        kk = int(np.argmax([f(h) for h in hs]))
        hbest = golden(f, hs[max(kk - 1, 0)], hs[min(kk + 1, len(hs) - 1)])
        h0 = Fr(hbest).limit_denominator(10 ** 6)
        S0 = symXN(X, [[Fr(1), Fr(0)], [Fr(0), Fr(1)]])
        checks = [
            ('sym(X) positive definite (sbar in int B_X, det X > 0)', pd(S0)),
            ('sym(X M(P_1)) PSD', psd(symXN(X, Mq(p1)))),
            ('sym(X M(P_2)) PSD', psd(symXN(X, Mq(p2)))),
            ('sym(X M(rho, rho, h0)) PSD', psd(symXN(X, Mq((rho, rho, h0))))),
        ]
        ok = all(v for _, v in checks)
        allok &= ok
        print('=== family %s, rho = %s = %.6f, X from %s' % (spec, rho, rf, src))
        print('X =', Xs, ' det sym(X) = %.3e, float smallest eigenvalues: sbar %.2e, P1 %.2e, P2 %.2e, line %.2e'
              % (float(S0[0] * S0[2] - S0[1] ** 2), lmin(S0), lmin(symXN(X, Mq(p1))), lmin(symXN(X, Mq(p2))),
                 lmin(symXN(X, Mq((rho, rho, h0))))))
        print('h0 = %s = %.6f' % (h0, float(h0)))
        for name, v in checks:
            print('  %s: %s' % (name, 'PASS' if v else 'FAIL'))
        if spec == 'B':
            eps0 = (rho / (h0 - 1)) ** 2
            print('  conclusion: for every eps <= (rho/(h0-1))^2 = %s = %.4e: z_B/z_K >= (%s) sqrt(eps)/z_0,'
                  ' i.e. D z_B/z_K >= sqrt(2) rho = %.4f' % (eps0, float(eps0), rho, 2 ** 0.5 * rf))
            print('  also: rho_max(H) >= %s for H = h0 - 1 = %.6g (X contains P_1, P_2, (rho, rho, h0) in C_X itself)'
                  % (rho, float(h0 - 1)))
        else:
            sk = sqrt_frac(Fr(spec.split(':')[2]))
            L0 = (h0 - 1) / rho
            print('  conclusion: for every L >= L0 = (h0-1)/rho = %.4f: z_B/z_K >= %s/z_K,'
                  ' i.e. D z_B/z_K >= sqrt(K) rho = %s = %.4f' % (float(L0), rho, sk * rho, float(sk * rho)))
        print('RESULT:', 'PASS' if ok else 'FAIL', flush=True)
    print('ALL PASS' if allok else 'SOME FAIL')


if __name__ == '__main__':
    main()
