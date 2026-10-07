"""Review r2: independent check of Theorem B2(2) and Theorem B3(5) of ../../note.md.

Does not import the stream's code.  For each case the matrix X is parsed from the stream's log (the exact decimal
printed there), and the theorem's test points are built from the formulas in the note:
  Theorem B family (normalized frame): sbar = (0,0,1), P1 = (rho,-rho,1), P2 = (rho,-2rho,1),
      P3 = (rho, rho, 1 + rho/sqrt(eps)), r = rho sqrt(eps)/z0, D = z0 sqrt(2/eps).
  Near-tangent family: sbar = (0,0,1), P1 = (rho,-rho,1-2rho(1-eta)), P2 = (rho,-k rho,1-2 sqrt(k) rho(1-eta)),
      P3 = (rho, rho, 1 + rho L), r = rho/z_K, D = sqrt(k) z_K.
Exact checks (Fractions): sym(X) positive definite; sym(X M(P1)), sym(X M(P2)) PSD; the set of heights h with
sym(X M(rho,rho,h)) PSD is an interval [h_lo, h_hi] (det is a concave quadratic in h); we check that the note's h0
lies in it exactly, and compute h_lo to 40 digits to see the slack.  Then we recompute the note's derived numbers
(eps_1, L_0, the constants sqrt(k) rho) exactly.
Float cross-check: for several L (or eps) we compute the actual step lengths of B_X = cl(C_X + R_+ e_w) along the
three rays by bisection with an independent membership test (lowering parameter optimized by golden section),
and compare D * min step / z_K with the certified constant.
"""
import json
import re
from fractions import Fraction as Fr
import mpmath as mp
import numpy as np

mp.mp.dps = 40
LOGS = '../../logs/'


def parse_B():
    for line in open(LOGS + 'zB_extended.log'):
        m = re.search(r'X = (\[\[.*\]\])', line)
        if m:
            return m.group(1)


def parse_tan(fname):
    for line in open(LOGS + fname):
        if line.startswith('{'):
            d = json.loads(line)
            # keep the literal text of XB as printed
            m = re.search(r'"XB": (\[\[[^\]]*\], \[[^\]]*\]\])', line)
            return m.group(1)


def to_frac(txt):
    rows = re.findall(r'\[([^\[\]]*)\]', txt)
    return [[Fr(v.strip()) for v in r.split(',')] for r in rows]


def symXM(X, s):
    x, y, w = s
    M = [[w, x], [y, Fr(1)]]
    A = [[sum(X[i][k] * M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return A[0][0], (A[0][1] + A[1][0]) / 2, A[1][1]


def psd(S):
    a, b, d = S
    return a >= 0 and d >= 0 and a * d - b * b >= 0


def pd(S):
    a, b, d = S
    return a > 0 and d > 0 and a * d - b * b > 0


def line_interval(X, rho):
    """coefficients of det sym(X M(rho,rho,h)) = c2 h^2 + c1 h + c0, and float roots"""
    h = [Fr(0), Fr(1), Fr(2)]
    vals = []
    for hv in h:
        a, b, d = symXM(X, (rho, rho, hv))
        vals.append(a * d - b * b)
    c0 = vals[0]
    c2 = (vals[2] - 2 * vals[1] + vals[0]) / 2
    c1 = vals[1] - c0 - c2
    disc = mp.mpf(c1.numerator) / c1.denominator
    C2 = mp.mpf(c2.numerator) / c2.denominator
    C0 = mp.mpf(c0.numerator) / c0.denominator
    D = disc ** 2 - 4 * C2 * C0
    r1 = (-disc + mp.sqrt(D)) / (2 * C2)
    r2 = (-disc - mp.sqrt(D)) / (2 * C2)
    return c2, sorted([r1, r2])


# --- float membership in B_X and step lengths (independent of the exact part)
def lmin(X, s):
    x, y, w = s
    M = np.array([[w, x], [y, 1.0]])
    S = X @ M
    S = 0.5 * (S + S.T)
    return np.linalg.eigvalsh(S)[0]


def in_BX(X, s, tol=0.0):
    q = s[2] - s[0] * s[1]
    if q < 0:
        return False
    f = lambda t: lmin(X, (s[0], s[1], s[2] - t))
    a, b = 0.0, q
    g = (5 ** 0.5 - 1) / 2
    for _ in range(100):
        m1, m2 = b - g * (b - a), a + g * (b - a)
        if f(m1) >= f(m2):
            b = m2
        else:
            a = m1
    best = max(f(0.0), f(q), f(0.5 * (a + b)))
    return best >= -tol


def step(X, sbar, p, smax=1e9):
    lo, hi = 0.0, 1.0
    while in_BX(X, sbar + hi * p, 1e-12) and hi < smax:
        lo, hi = hi, 2 * hi
    if hi >= smax:
        return np.inf
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if in_BX(X, sbar + m * p, 1e-12):
            lo = m
        else:
            hi = m
    return lo


CASES = [
    # name, X text, rho, h0, claimed constant D z_B/z_K, family params
    ('B', parse_B(), Fr(1367, 10), Fr(5417132036, 169459), None),
    ('tan eta=1/1000 k=4', parse_tan('tangent_family_eta0.001_k4.log'), Fr(2461, 2500), Fr(1240951, 370546),
     (Fr(1, 1000), Fr(4), Fr(2), Fr(2461, 1250), Fr(197, 100))),
    ('tan eta=1/100 k=4', parse_tan('tangent_family_eta0.01_k4.log'), Fr(6117, 5000), Fr(4011447, 862162),
     (Fr(1, 100), Fr(4), Fr(2), Fr(6117, 2500), Fr(5, 2))),
    ('tan eta=1/1000 k=9/4', parse_tan('tangent_family_eta0.001_k2.25.log'), Fr(5207, 5000), Fr(4025363, 954377),
     (Fr(1, 1000), Fr(9, 4), Fr(3, 2), Fr(15621, 10000), Fr(1575, 1000))),
    ('tan eta=1/1000 k=49/25', parse_tan('tangent_family_eta0.001_k1.96_L30.log'), Fr(2693, 2500),
     Fr(412614, 89749), (Fr(1, 1000), Fr(49, 25), Fr(7, 5), Fr(18851, 12500), Fr(154, 100))),
]

allok = True
for name, Xtxt, rho, h0, fam in CASES:
    X = to_frac(Xtxt)
    print('=== %s: X = %s (parsed from log), rho = %s' % (name, Xtxt, rho))
    if fam is None:
        P1, P2 = (rho, -rho, Fr(1)), (rho, -2 * rho, Fr(1))
    else:
        eta, k, sk, const, upper = fam
        assert sk * sk == k
        P1 = (rho, -rho, 1 - 2 * rho * (1 - eta))
        P2 = (rho, -k * rho, 1 - 2 * sk * rho * (1 - eta))
    S0 = symXM(X, (Fr(0), Fr(0), Fr(1)))
    c2, (hlo, hhi) = line_interval(X, rho)
    a3, b3, d3 = symXM(X, (rho, rho, h0))
    checks = {
        'sym(X) PD': pd(S0),
        'sym(X M(P1)) PSD': psd(symXM(X, P1)),
        'sym(X M(P2)) PSD': psd(symXM(X, P2)),
        'sym(X M(rho,rho,h0)) PSD (exact)': psd((a3, b3, d3)),
        '(2,2) entry rho x21 + x22 > 0 (so the line condition can hold)': X[1][0] * rho + X[1][1] > 0,
    }
    for kk, v in checks.items():
        print('  %-62s %s' % (kk, 'PASS' if v else 'FAIL'))
        allok &= v
    print('  PSD heights on the line: [%s, %s]; note h0 = %.10f; slack h0 - h_lo = %.3e'
          % (mp.nstr(hlo, 15), mp.nstr(hhi, 15), float(h0), float(mp.mpf(h0.numerator) / h0.denominator - hlo)))
    if fam is None:
        eps1 = (rho / (h0 - 1)) ** 2
        note_eps1 = Fr(53661932375105209, 2934348356061848092900)
        ok = eps1 == note_eps1
        print('  eps_1 = (rho/(h0-1))^2 = %.6e; equals the note\'s fraction: %s' % (float(eps1), ok))
        print('  best possible eps bound from this X: (rho/(h_lo-1))^2 = %s' % mp.nstr((rho.numerator / mp.mpf(rho.denominator) / (hlo - 1)) ** 2, 8))
        print('  D z_B/z_K >= sqrt(2) rho = %.5f (note: 193.32); upper 137 sqrt(2) = %.4f (note: < 193.8)'
              % (2 ** 0.5 * float(rho), 137 * 2 ** 0.5))
        allok &= ok
        # float step check at eps = eps_1 and 1e-6, 1e-8
        for eps in [float(eps1) * (1 - 1e-9), 1e-6, 1e-8]:
            z0 = (1 + (1 + 4 * eps) ** 0.5) / 2
            # normalized-frame scaled rays: p~_j = z0 p_j mapped by (x/sqrt(eps), y/sqrt(eps), w/eps)
            se = eps ** 0.5
            rays = [np.array([z0 / se, -z0 / se, 0.0]), np.array([z0 / se, -2 * z0 / se, 0.0]),
                    np.array([z0 / se, z0 / se, z0 / eps])]
            Xf = np.array([[float(v) for v in r] for r in X])
            st = [step(Xf, np.array([0.0, 0.0, 1.0]), p) for p in rays]
            r = min(st)
            print('  float: eps = %.4e: steps %s; min step * z0/sqrt(eps) = %.5f (certified >= %s)'
                  % (eps, ['%.6g' % s for s in st], r * z0 / se, float(rho)))
            allok &= r * z0 / se >= float(rho) * (1 - 1e-7)
    else:
        L0 = (h0 - 1) / rho
        print('  L0 = (h0-1)/rho = %.4f; best possible from this X: (h_lo-1)/rho = %s'
              % (float(L0), mp.nstr((hlo - 1) / (mp.mpf(rho.numerator) / rho.denominator), 6)))
        ok1 = sk * rho == const
        ok2 = 1 + rho * Fr(34, 10) >= h0
        print('  sqrt(k) rho = %s = %.4f equals the note\'s constant: %s; L = 3.4 >= L0: %s'
              % (sk * rho, float(sk * rho), ok1, ok2))
        print('  gap to the box upper bound %.4f: %.3f%%' % (float(upper), 100 * float(upper / const - 1)))
        allok &= ok1 and ok2
        Xf = np.array([[float(v) for v in r] for r in X])
        for L in [3.4, 10.0, 1000.0]:
            # z_K cancels: the steps along p~_j = z_K p_j times D = sqrt(k) z_K equal sqrt(k) times the steps along p_j
            zK = 1.0
            rays = [zK * np.array([1.0, -1.0, -2 * (1 - float(eta))]),
                    zK * np.array([1.0, -float(k), -2 * float(sk) * (1 - float(eta))]),
                    zK * np.array([1.0, 1.0, L])]
            st = [step(Xf, np.array([0.0, 0.0, 1.0]), p) for p in rays]
            Dv = float(sk) * zK
            print('  float: L = %g: steps %s; D * min step = %.5f (certified >= %.4f)'
                  % (L, ['%.6g' % s for s in st], Dv * min(st), float(const)))
            allok &= Dv * min(st) >= float(const) * (1 - 1e-7)
print('ALL PASS' if allok else 'SOME FAIL')
