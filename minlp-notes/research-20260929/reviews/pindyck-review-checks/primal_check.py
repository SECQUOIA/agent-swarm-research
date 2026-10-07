"""Primal re-evaluation and rigorous enclosure of J(p*), grad J(p*) (reviewer's own code).

1. Build the full 116-vector from the decimal prices p* (logs/pindyck_primal.txt, x1..x16)
   by the exact recursion at 60 digits; evaluate all 96 OSIL rows, all bounds and the
   objective from the OSIL expression trees (own_osil.py).
2. Rigorous: mpmath.iv (50 digits) forward mode; each s_t is enclosed by an interval Newton
   step N(X) = m - f(m)/f'(X) with N(X) inside X (unique root, contained in N(X)).
Writes logs/primal_check.txt and logs/primal_enclosure.txt (J and gradient end points).
"""
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_model as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "..", "open-instances-wave2", "small", "logs", "pindyck_primal.txt")
out = open(os.path.join(HERE, "logs", "primal_check.txt"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s)
    out.write(s + "\n")


vals = dict(line.split() for line in open(PRIM))
pstr = [vals[f"x{t}"] for t in range(1, 17)]
say("p* =", pstr)

# ---- 1. full point at 60 digits, OSIL rows ----
with mp.workdps(60):
    x = M.states([mp.mpf(s) for s in pstr])
    rw, bw = M.rows_resid(x)
    f = M.objective(x)
    say("60-digit recursion point: max row residual", mp.nstr(rw, 3), " max bound violation", mp.nstr(bw, 3))
    say("objective (min form) =", mp.nstr(f, 40))
    say("min d_t =", mp.nstr(min(x[M.D[t]] for t in range(1, 17)), 8),
        " min R_t =", mp.nstr(min(x[M.R[t]] for t in range(1, 17)), 8),
        " min td_t =", mp.nstr(min(x[M.TD[t]] for t in range(1, 17)), 8))
    # the stored 30-digit point from the author's primal file (states rounded)
    xs = [mp.mpf(vals[n]) for n in M.I["names"]]
    rw2, bw2 = M.rows_resid(xs)
    say("stored point in pindyck_primal.txt: max row residual", mp.nstr(rw2, 3), " bound violation", mp.nstr(bw2, 3),
        " objective", mp.nstr(M.objective(xs), 30))

# ---- 2. rigorous interval enclosure ----
iv = mp.iv
iv.dps = 50
mp.mp.dps = 60


def raw2fr(r):
    sgn, man, ex, _ = r
    q = Fr(man) * (Fr(2) ** ex)
    return -q if sgn else q


def ivends(x):
    """exact Fraction end points of an mpmath iv interval"""
    a, b = x._mpi_
    return raw2fr(a), raw2fr(b)


K = -iv.mpf(M.KAPSTR) * iv.log(iv.mpf("1.02"))
n = 16
p = [iv.mpf(s) for s in pstr]
for t in range(n):   # iv.mpf(str) must enclose the decimal exactly
    lo_, hi_ = ivends(p[t])
    assert lo_ <= Fr(pstr[t]) <= hi_


def zeros():
    return [iv.mpf(0)] * n


td_v, td_g = iv.mpf(18), zeros()
s_v, s_g = iv.mpf("6.5"), zeros()
cs_v, cs_g = iv.mpf(0), zeros()
R_v, R_g = iv.mpf(500), zeros()
J_v, J_g = iv.mpf(0), zeros()
dmin, Rmin = [], []
for t in range(n):
    e = [iv.mpf(1) if k == t else iv.mpf(0) for k in range(n)]
    td_v = iv.mpf(".87") * td_v - iv.mpf(".13") * p[t] + iv.mpf(M.CT[t])
    td_g = [iv.mpf(".87") * g - iv.mpf(".13") * ek for g, ek in zip(td_g, e)]
    a_v, a_g = iv.mpf(".75") * s_v, [iv.mpf(".75") * g for g in s_g]
    E = iv.exp(-K * cs_v)
    lin = iv.mpf("1.1") + iv.mpf(".1") * p[t]
    b_v = lin * E
    b_g = [iv.mpf(".1") * ek * E - lin * K * E * cg for ek, cg in zip(e, cs_g)]
    # interval Newton for f(y) = y - a - b exp(-K y)
    with mp.workdps(60):
        y = mp.mpf((a_v + b_v).mid)
        am, bm = mp.mpf(a_v.mid), mp.mpf(b_v.mid)
        Km = mp.mpf(K.mid)
        for _ in range(100):
            y = y - (y - am - bm * mp.exp(-Km * y)) / (1 + Km * bm * mp.exp(-Km * y))
    Xb = iv.mpf([y - mp.mpf(10) ** -35, y + mp.mpf(10) ** -35])
    m = iv.mpf(y)
    fm = m - a_v - b_v * iv.exp(-K * m)
    fp = 1 + K * b_v * iv.exp(-K * Xb)
    assert fp.a > 0
    N = m - fm / fp
    assert Xb.a < N.a and N.b < Xb.b, "interval Newton failed"
    s_v = N
    phi = iv.exp(-K * s_v)
    den = 1 + K * b_v * phi
    s_g = [(ag + phi * bg) / den for ag, bg in zip(a_g, b_g)]
    cs_v, cs_g = cs_v + s_v, [u + w for u, w in zip(cs_g, s_g)]
    d_v, d_g = td_v - s_v, [u - w for u, w in zip(td_g, s_g)]
    R_v, R_g = R_v - d_v, [u - w for u, w in zip(R_g, d_g)]
    q_v = p[t] - 250 / R_v
    q_g = [ek + 250 * rg / (R_v * R_v) for ek, rg in zip(e, R_g)]
    dl = iv.mpf(M.DELTA[t])
    J_v = J_v + dl * d_v * q_v
    J_g = [jg + dl * (dg * q_v + d_v * qg) for jg, dg, qg in zip(J_g, d_g, q_g)]
    dmin.append(d_v.a)
    Rmin.append(R_v.a)


Jlo, Jhi = ivends(J_v)
G = [ivends(g) for g in J_g]
gabs = [max(abs(a), abs(b)) for a, b in G]
say("interval run (iv.dps = 50): min d_t lower end %.10f, min R_t lower end %.6f"
    % (min(float(ivends(d)[0]) for d in dmin), min(float(ivends(r)[0]) for r in Rmin)))
say("J(p*) in [%s, %s], width %.2e" % (mp.nstr(mp.mpf(Jlo.numerator) / Jlo.denominator, 40),
                                       mp.nstr(mp.mpf(Jhi.numerator) / Jhi.denominator, 40), float(Jhi - Jlo)))
gmax = max(gabs)
sumsq = sum(g * g for g in gabs)
g2 = Fr(float(sumsq) ** 0.5 * (1 + 1e-9))
assert g2 * g2 >= sumsq
say("max_t |dJ/dp_t(p*)| <= %.6e   ||grad J(p*)||_2 <= %.6e" % (float(gmax) * (1 + 1e-12), float(g2)))
say("componentwise |grad| upper ends:", ["%.3e" % float(g) for g in gabs])
say("2 ||grad||_2 / mu with mu = 0.001:  %.6e" % float(2 * g2 / Fr(1, 1000)))
with open(os.path.join(HERE, "logs", "primal_enclosure.txt"), "w") as fo:
    fo.write("J %s/%s %s/%s\n" % (Jlo.numerator, Jlo.denominator, Jhi.numerator, Jhi.denominator))
    for t, (a, b) in enumerate(G):
        fo.write("g%d %s/%s %s/%s\n" % (t + 1, a.numerator, a.denominator, b.numerator, b.denominator))
claim = Fr("-1170.486285436088562087577")
say("claim 'objective(p*) <= -1170.486285436088562087577':", "holds" if -Jlo <= claim else
    "fails: objective in [%.30e, %.30e] exceeds the claim by up to %.3e" % (float(-Jhi), float(-Jlo), float(-Jlo - claim)))
out.close()
