"""Critic's independent check of dossier Theorem 3 (lnts exact optimum).

Different arithmetic from the dossier: mpmath iv at 130 digits (outward rounding),
own c_j from the recursion (not the closed form), own root search by bisection,
own bracket. Also: the 3-equation Newton system without the symmetry ansatz,
tightness of Proposition 2 at (mu*, nu*), and comparison with the stored
Krawczyk h-boxes of the independently proved primal points.
"""
import json
from fractions import Fraction as Fr
import mpmath
from mpmath import mp, iv, mpf

mp.dps = 140
iv.dps = 130


def wc(N):
    # build c_j by simulating the recursion on unit impulses (exact rationals)
    w = [Fr(1, 2)] + [Fr(1)] * (N - 1) + [Fr(1, 2)]
    c = []
    for j in range(N + 1):
        s = [Fr(0)] * (N + 1)
        s[j] = Fr(1)
        vy, py = Fr(0), Fr(0)
        for i in range(N):
            vy_new = vy + Fr(1, 2) * (s[i] + s[i + 1])
            py = py + Fr(1, 2) * (vy + vy_new)
            vy = vy_new
        c.append(py)  # py_N / (a h^2) for sin = e_j
    return w, c


def g_mp(nu, w, c, N):
    C = D = mpf(0)
    for wj, cj in zip(w, c):
        r = mpf(cj.numerator) / cj.denominator / (mpf(wj.numerator) / wj.denominator) - mpf(N) / 2
        t = nu * r
        s = mp.sqrt(1 + t * t)
        C += mpf(wj.numerator) / wj.denominator / s
        D += mpf(cj.numerator) / cj.denominator * t / s
    return D - mpf(20) / 81 * C * C, C


def g_iv(nu_str, w, c, N):
    nu = iv.mpf(nu_str)
    C = D = iv.mpf(0)
    for wj, cj in zip(w, c):
        W = iv.mpf(wj.numerator) / wj.denominator
        Cc = iv.mpf(cj.numerator) / cj.denominator
        r = Cc / W - iv.mpf(N) / 2
        t = nu * r
        s = iv.sqrt(1 + t * t)
        C += W / s
        D += Cc * t / s
    return D - iv.mpf(20) / 81 * C * C, C


def main(N):
    w, c = wc(N)
    # bisection for the root in mp
    lo, hi = mpf('1e-6'), mpf(1)
    assert g_mp(lo, w, c, N)[0] < 0 < g_mp(hi, w, c, N)[0]
    for _ in range(460):
        m = (lo + hi) / 2
        if g_mp(m, w, c, N)[0] < 0:
            lo = m
        else:
            hi = m
    nu = (lo + hi) / 2
    # bracket with asymmetric offsets (different from the dossier's)
    a = mpmath.nstr(nu - mpf('3e-66'), 100, strip_zeros=False)
    b = mpmath.nstr(nu + mpf('7e-66'), 100, strip_zeros=False)
    ga, Ca = g_iv(a, w, c, N)
    gb, Cb = g_iv(b, w, c, N)
    ok = mp.make_mpf(ga._mpi_[1]) < 0 and mp.make_mpf(gb._mpi_[0]) > 0
    obj_lo = iv.mpf(9 * N) / (20 * iv.mpf(mp.make_mpf(Ca._mpi_[1])))
    obj_hi = iv.mpf(9 * N) / (20 * iv.mpf(mp.make_mpf(Cb._mpi_[0])))
    olo, ohi = mp.make_mpf(obj_lo._mpi_[0]), mp.make_mpf(obj_hi._mpi_[1])
    # free Newton on (mu, nu, h) without symmetry ansatz
    def F(mu, nu_, h):
        s1 = s2 = s3 = mpf(0)
        for wj, cj in zip(w, c):
            W = mpf(wj.numerator) / wj.denominator
            Cc = mpf(cj.numerator) / cj.denominator
            t = mu + nu_ * Cc / W
            r = mp.sqrt(1 + t * t)
            s1 += W / r
            s2 += W * t / r
            s3 += Cc * t / r
        return [s1 - mpf(45) / (100 * h), s2, s3 - mpf(5) / (100 * h * h)]
    mp.dps = 80
    sol = mpmath.findroot(F, [mpf(-1.41), mpf(2.82) / N, mpf('0.5546') / N], tol=mpf(10) ** -70)
    mp.dps = 140
    mu_f, nu_f, h_f = sol
    sym = mu_f + nu_f * N / 2
    # Prop 2 tightness at (mu*, nu*, h*): S - nu B - A
    hstar = mpf(9) / (20 * g_mp(nu, w, c, N)[1])
    S = sum(mpf(wj.numerator) / wj.denominator * mp.sqrt(1 + (nu * (mpf(cj.numerator) / cj.denominator / (mpf(wj.numerator) / wj.denominator) - mpf(N) / 2)) ** 2) for wj, cj in zip(w, c))
    tight = S - nu * mpf(5) / (100 * hstar ** 2) - mpf(45) / (100 * hstar)
    # stored primal h-box
    pt = json.load(open(f'lnts{N}_point.json'))
    hkey = [k for k in pt['unknowns_box'] if k not in ('x1', 'x%d' % (N + 1))][0]
    hb = pt['unknowns_box'][hkey]
    hc, hr = Fr(hb['centre']), Fr(hb['radius'])
    pobj_lo, pobj_hi = N * (hc - hr), N * (hc + hr)
    olo_fr = Fr(mpmath.nstr(olo, 120, strip_zeros=False))  # decimal approx of lower end
    d = json.load(open('lnts_exact_opt.json'))
    dd = [r for r in d if r['N'] == N][0]
    dlo, dhi = Fr(dd['opt_lower']), Fr(dd['opt_upper'])
    out = dict(N=N, sign_change=bool(ok), g_a_upper=mpmath.nstr(mp.make_mpf(ga._mpi_[1]), 5), g_b_lower=mpmath.nstr(mp.make_mpf(gb._mpi_[0]), 5),
               opt_lo=mpmath.nstr(olo, 120), opt_hi=mpmath.nstr(ohi, 120), width=mpmath.nstr(ohi - olo, 5),
               dossier_encl_contains_mine=bool(dlo <= Fr(mpmath.nstr(olo, 60)) and Fr(mpmath.nstr(ohi, 60)) <= dhi + Fr(1, 10**58)),
               free_newton_mu_plus_nuN2=mpmath.nstr(sym, 5), free_newton_nu_minus_root=mpmath.nstr(nu_f - nu, 5),
               free_newton_Nh=mpmath.nstr(N * h_f, 45),
               prop2_residual_at_exact=mpmath.nstr(tight, 5),
               primal_hbox_Nh_lo=float(pobj_lo - olo_fr), primal_hbox_Nh_hi=float(pobj_hi - olo_fr),
               primal_centre_minus_opt=float(N * hc - olo_fr))
    print(json.dumps(out, indent=1))
    return out


if __name__ == '__main__':
    import sys
    res = [main(int(a)) for a in sys.argv[1:]]
    json.dump(res, open('thm3_iv.json', 'w'), indent=1)
