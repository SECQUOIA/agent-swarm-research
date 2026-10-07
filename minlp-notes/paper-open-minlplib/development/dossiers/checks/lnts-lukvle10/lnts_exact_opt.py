"""Dossier check (own code, no mpmath in the proof part): exact optimum of lntsN.

Claim: opt = N*h*, h* = 45/(100*C(nu*)), where nu* > 0 is a root of
  g(nu) = D(nu) - (20/81) C(nu)^2,
  C(nu) = sum_j w_j / sqrt(1+t_j^2),  D(nu) = sum_j c_j t_j / sqrt(1+t_j^2),
  t_j = nu * r_j,  r_j = c_j/w_j - N/2.
Proof part: integer/Fraction arithmetic with isqrt-based outward enclosures.
mpmath is used only to locate nu* numerically (not trusted).
"""
import sys
import json
from fractions import Fraction as Fr
from math import isqrt

P = 600  # fixed-point bits
S = 1 << P


def weights(N):
    w = [Fr(1, 2)] + [Fr(1)] * (N - 1) + [Fr(1, 2)]
    c = [Fr(0)] * (N + 1)
    for k in range(N + 1):
        for j in range(N + 1):
            W = Fr((1 if j <= k - 1 else 0) + (1 if 1 <= j <= k else 0), 2)
            c[j] += w[k] * W
    return w, c


def recursion_identity(N, w, c):
    # exact rational recursion with arbitrary rational stand-ins for sin, cos
    import random
    rnd = random.Random(7 + N)
    a, h = Fr(100), Fr(rnd.randint(1, 999), 997)
    s = [Fr(rnd.randint(-999, 999), 991) for _ in range(N + 1)]
    k = [Fr(rnd.randint(-999, 999), 983) for _ in range(N + 1)]
    vx, vy, py = [Fr(0)], [Fr(0)], [Fr(0)]
    for i in range(N):
        vx.append(vx[i] + h / 2 * (a * k[i] + a * k[i + 1]))
        vy.append(vy[i] + h / 2 * (a * s[i] + a * s[i + 1]))
        py.append(py[i] + h / 2 * (vy[i] + vy[i + 1]))
    assert vx[N] == a * h * sum(x * y for x, y in zip(w, k))
    assert vy[N] == a * h * sum(x * y for x, y in zip(w, s))
    assert py[N] == a * h * h * sum(x * y for x, y in zip(c, s))


def floorS(q):  # floor(q * S) for Fraction q
    return (q.numerator * S) // q.denominator


def ceilS(q):
    return -((-q.numerator * S) // q.denominator)


def inv_sqrt_1pt2(t):
    """Enclosure [lo, hi] (integers, units 2^-P) of 1/sqrt(1+t^2) for rational t."""
    q = 1 + t * t  # = p/r
    p, r = q.numerator, q.denominator
    # sqrt(q) = sqrt(p*r)/r ; isqrt(p*r*S^2) <= S*sqrt(p*r) < isqrt(...)+1
    m = isqrt(p * r * S * S)
    sq_lo = Fr(m, r * S)
    sq_hi = Fr(m + 1, r * S)
    return floorS(1 / sq_hi), ceilS(1 / sq_lo)


def CD_enclosure(N, w, c, nu):
    """Integer enclosures (units 2^-P for C; units 2^-P for D) of C(nu), D(nu)."""
    half = Fr(N, 2)
    Clo = Chi = Dlo = Dhi = 0
    for wj, cj in zip(w, c):
        r = cj / wj - half
        t = nu * r
        lo, hi = inv_sqrt_1pt2(t)
        # w_j * [lo, hi]
        Clo += floorS(wj * Fr(lo, S)); Chi += ceilS(wj * Fr(hi, S))
        # c_j t_j / sqrt(1+t^2): c_j >= 0; sign of t
        a = cj * t
        if a >= 0:
            Dlo += floorS(a * Fr(lo, S)); Dhi += ceilS(a * Fr(hi, S))
        else:
            Dlo += floorS(a * Fr(hi, S)); Dhi += ceilS(a * Fr(lo, S))
    return Fr(Clo, S), Fr(Chi, S), Fr(Dlo, S), Fr(Dhi, S)


def g_enclosure(N, w, c, nu):
    Clo, Chi, Dlo, Dhi = CD_enclosure(N, w, c, nu)
    k = Fr(20, 81)
    assert Clo > 0
    return Dlo - k * Chi * Chi, Dhi - k * Clo * Clo, (Clo, Chi)


def find_nu_numeric(N, w, c):
    import mpmath as mp
    mp.mp.dps = 120
    wm = [mp.mpf(x.numerator) / x.denominator for x in w]
    cm = [mp.mpf(x.numerator) / x.denominator for x in c]
    half = mp.mpf(N) / 2

    def g(nu):
        C = D = mp.mpf(0)
        for wj, cj in zip(wm, cm):
            t = nu * (cj / wj - half)
            s = mp.sqrt(1 + t * t)
            C += wj / s
            D += cj * t / s
        return D - mp.mpf(20) / 81 * C * C
    nu = mp.findroot(g, mp.mpf('2.82') / N, tol=mp.mpf(10) ** -110)
    return nu


def dec_floor(q, d):
    """decimal string of floor(q * 10^d) / 10^d"""
    n = (q.numerator * 10 ** d) // q.denominator
    s = str(n).rjust(d + 1, '0')
    return s[:-d] + '.' + s[-d:]


def dec_ceil(q, d):
    n = -((-q.numerator * 10 ** d) // q.denominator)
    s = str(n).rjust(d + 1, '0')
    return s[:-d] + '.' + s[-d:]


def main(N):
    w, c = weights(N)
    # closed form of c
    assert c[0] == Fr(N, 2) - Fr(1, 4) and c[N] == Fr(1, 4)
    assert all(c[j] == N - j for j in range(1, N))
    # reflection identity c_{N-j} = N w_j - c_j
    assert all(c[N - j] == N * w[j] - c[j] for j in range(N + 1))
    recursion_identity(N, w, c)
    nu_num = find_nu_numeric(N, w, c)
    import mpmath as mp
    # rational bracket around the numerical root
    den = 10 ** 70
    nu_c = Fr(int(mp.nint(nu_num * den)), den)
    delta = Fr(1, 10 ** 62)
    nu_lo, nu_hi = nu_c - delta, nu_c + delta
    assert nu_lo > 0
    glo_lo, glo_hi, (C_lo_at_lo, C_hi_at_lo) = g_enclosure(N, w, c, nu_lo)
    ghi_lo, ghi_hi, (C_lo_at_hi, C_hi_at_hi) = g_enclosure(N, w, c, nu_hi)
    sign_ok = glo_hi < 0 < ghi_lo
    # N h* = 45 N / (100 C(nu*)), C decreasing in nu >= 0
    obj_lo = Fr(45 * N, 100) / C_hi_at_lo
    obj_hi = Fr(45 * N, 100) / C_lo_at_hi
    # max |theta|: t_0 = nu (N/2 - 1/2) largest |t|
    tmax = nu_hi * (Fr(N, 2) - Fr(1, 2))
    rec = dict(N=N, nu_numeric=mp.nstr(nu_num, 30), mu_numeric=mp.nstr(-nu_num * N / 2, 30),
               g_at_lo_upper=float(glo_hi), g_at_hi_lower=float(ghi_lo), sign_change=sign_ok,
               opt_lower=dec_floor(obj_lo, 40), opt_upper=dec_ceil(obj_hi, 40),
               width=float(obj_hi - obj_lo), tmax_upper=float(tmax))
    # compare with stored primal point objective enclosure and summary/verifier duals
    pt = json.load(open(f'lnts{N}_point.json'))
    oe = pt['objective_enclosure']
    plo, phi = Fr(oe[0]), Fr(oe[1])
    rec['point_obj_enclosure'] = oe
    rec['point_obj_ge_opt_lower'] = phi >= obj_lo  # necessary consistency (point is feasible)
    rec['point_minus_opt_upper_bound'] = float(phi - obj_lo)
    summ = {50: '0.5546687649381', 100: '0.5545954011663', 200: '0.5545770161025', 400: '0.5545724137001'}[N]
    rec['summary_dual_le_opt'] = Fr(summ) <= obj_lo
    rec['opt_minus_summary_dual_upper'] = float(obj_hi - Fr(summ))
    print(json.dumps(rec, indent=1, default=str))
    return rec


if __name__ == '__main__':
    out = [main(int(a)) for a in sys.argv[1:]]
    json.dump(out, open('lnts_exact_opt.json', 'w'), indent=1, default=str)
