"""R1 checks of the numeric constants in Sections 4 and 6 (growth.tex, appendix-growth.tex).

Uses mpmath at 60 digits for transcendental comparisons and Fractions where
the claim is rational.  Each check prints PASS/FAIL with the computed margin.
"""
from fractions import Fraction as Fr
import math
import mpmath as mp

mp.mp.dps = 60
ok = True


def report(name, cond, info=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  " + info if info else ""))


s1715 = mp.sqrt(mp.mpf(17) / 15)
# Lemma states: per-coordinate radius constant
c73 = 3 + 2 * s1715 + (2 + s1715) / mp.sqrt(2)
report("7.3 radius constant", c73 < mp.mpf("7.3"), f"value={mp.nstr(c73, 12)}")
report("7.3 < 8 (R_ij)", c73 < 8)
# common-mesh variant: |v-y|<=(1+s)rho h, +h, + theta|v-c| <= (2+s)/sqrt8 rho h
c42 = 2 + s1715 + (2 + s1715) / mp.sqrt(8)
report("4.2 radius constant (common mesh)", c42 < mp.mpf("4.2"), f"value={mp.nstr(c42, 12)}")
report("4.2 < 5 used in (G4)", c42 < 5)


def phi(m):
    return mp.mpf(3) / 4 + 8 * mp.log(mp.mpf(5) / 4 + 4 * mp.sqrt(2 * m))


report("phi(1)<16.3", phi(1) < mp.mpf("16.3"), mp.nstr(phi(1), 10))
report("phi(2)<18.6", phi(2) < mp.mpf("18.6"), mp.nstr(phi(2), 10))
bad = [m for m in list(range(1, 5000)) + [10**k for k in range(4, 13)]
       if phi(m) > 10 * mp.log(m + 2, 2)]
report("phi(m)<=10 log2(m+2) for sampled m", not bad, f"bad={bad[:5]}")
# derivative claims
bad = []
for m in [2, 3, 5, 10, 100, 10**4, 10**8]:
    m = mp.mpf(m)
    dphi = mp.diff(phi, m)
    if dphi > 4 / m or 10 / ((m + 2) * mp.log(2)) < mp.mpf("7.2") / m:
        bad.append(m)
report("phi'(m)<=4/m and d/dm 10log2(m+2)>=7.2/m for m>=2", not bad)

# common-mesh variant cap 8 theta^-1 ceil(log2(n+2)):
# theta R/H <= theta + 2*4.2*theta*rho <= 1/4 + 8.4*sqrt(n/8)


def phiv(m, c=mp.mpf("4.2")):
    return mp.mpf(3) / 4 + 8 * mp.log(mp.mpf(5) / 4 + 2 * c * mp.sqrt(mp.mpf(m) / 8))


bad = [m for m in list(range(1, 5000)) + [10**k for k in range(4, 13)]
       if phiv(m) > 8 * math.ceil(math.log2(m + 2))]
report("common-mesh cap 8/theta*ceil(log2(n+2))", not bad, f"phiv(1)={mp.nstr(phiv(1),8)} bad={bad[:5]}")

# ln(1+x) >= 23x/24 on [0,1/12]
xs = [mp.mpf(k) / 12000 for k in range(0, 1001)]
report("ln(1+x)>=23x/24 on [0,1/12]", all(mp.log(1 + x) >= mp.mpf(23) / 24 * x for x in xs))
# (72/23) <= 4 so ceil bound
report("72/23<=4", Fr(72, 23) <= 4)

# mu* and 2^mu* <= 6 sqrt(kappa), mu* <= 3(1+log2 kappa)
bad = []
for k in [mp.mpf(1) + mp.mpf(i) / 7 for i in range(0, 4000)] + [mp.mpf(10) ** e for e in range(1, 30)]:
    mus = max(2, int(mp.ceil(mp.log(8 * k, 4))))
    th = mp.mpf(2) ** (-mus)
    if not (8 * k * th**2 <= 1 and 2**mus <= 6 * mp.sqrt(k) and mus <= 3 * (1 + mp.log(k, 2))):
        bad.append(k)
report("mu*: 8 kbar theta^2<=1, 2^mu*<=6 sqrt(kbar), mu*<=3(1+log2 kbar)", not bad, f"bad={bad[:3]}")
worst = max(2 ** max(2, int(mp.ceil(mp.log(8 * k, 4)))) / mp.sqrt(k)
            for k in [mp.mpf(1) + mp.mpf(i) / 97 for i in range(0, 20000)])
print("     sup 2^mu*/sqrt(kbar) observed:", mp.nstr(worst, 8), "(4*sqrt2 =", mp.nstr(4 * mp.sqrt(2), 8), ")")

# logabsorb: ceil(log2(nP+2))^p <= 2 p^p (n+2)
bad = []
for p in range(1, 41):
    for n in list(range(1, 3000)) + [10**k for k in range(4, 16)]:
        lhs = math.ceil(math.log2(n + 2)) ** p
        if lhs > 2 * p**p * (n + 2):
            bad.append((p, n))
report("eq:logabsorb", not bad, f"bad={bad[:3]}")

# Sum_{mu<=mu*} K_mu^p <= 2 K_{mu*}^p  (K_mu proportional to 2^mu)
bad = [(p, ms) for p in range(1, 20) for ms in range(2, 30)
       if sum(Fr(2) ** (mu * p) for mu in range(2, ms + 1)) > 2 * Fr(2) ** (ms * p)]
report("geometric sum of caps", not bad)

# Theorem approx (a): sum L_i h_iJ^2/2 <= (8/9) eps when (9/16) a_J <= eps
report("a_J/2 <= 8/9 * (9/16) a_J", Fr(1, 2) <= Fr(8, 9) * Fr(9, 16))

# Lemma inv algebra
g = Fr(1)  # gamma normalised, kbar>=1/gamma
for kb in [Fr(1), Fr(3, 2), Fr(10), Fr(1000)]:
    for gam in [1 / kb, Fr(1, 1) / kb * Fr(3, 2) if kb > 1 else 1 / kb]:
        if gam < 1 / kb:
            continue
        a = Fr(1)
        # (iii): gamma Y <= a/4 + gamma/16 (Y + 4 kb a)
        Y = (a / 4 + gam * kb * a / 4) / (gam * Fr(15, 16))
        assert Y == Fr(4, 15) * (1 / gam + kb) * a and Y <= Fr(8, 15) * kb * a
        # (iv)
        D = a / 4 + Fr(1, 2) * (1 / (8 * kb)) * 5 * kb * a
        assert D == Fr(9, 16) * a
        # (v)
        Z = (Fr(13, 16) * a + gam * kb * a / 4) / (gam * Fr(15, 16))
        assert Z == (Fr(13, 15) / gam + Fr(4, 15) * kb) * a and Z <= Fr(17, 15) * kb * a
report("Lemma inv algebra (iii)-(v)", True)

# Appendix localized (G3) 7/8 vs 9/16 and node-exclusion constant 11/8 and 15/22
report("1/4+1/4+7/8 = 11/8", Fr(1, 4) + Fr(1, 4) + Fr(7, 8) == Fr(11, 8))
report("(15/16)/(11/8) = 15/22", Fr(15, 16) / Fr(11, 8) == Fr(15, 22))
report("1/2 < 4/5 < sqrt(15/22)", Fr(1, 4) < Fr(16, 25) < Fr(15, 22))

# Theorem transfer: g tau^2/4 with tau=1/(4nR)
for n in [1, 3, 10]:
    for R in [1, 7, 100]:
        tau = Fr(1, 4 * n * R)
        assert tau**2 / 4 == Fr(1, 64 * n * n * R * R)
report("tau^2/4 = 1/(64 n^2 R^2)", True)
# Lemma snap: phi(s) <= 3/2 |E| tau <= 3/(8R)
report("3/2 n tau = 3/(8R)", all(Fr(3, 2) * n * Fr(1, 4 * n * R) == Fr(3, 8 * R) for n in range(1, 20) for R in range(1, 20)))

# Remark cf: rounding threshold vs snapping threshold (which one is smaller?)
cases = []
for n in [2, 10, 100]:
    for R in [1, 2, 10, 10**3]:
        snap = Fr(1, 64 * n * n * R * R)
        cf = Fr(1, 32 * R**4)
        cases.append((n, R, snap >= cf))
print("     Remark cf: (n, R, snapping threshold g/(64n^2R^2) >= rounding threshold g/(32R^4)):")
print("     ", cases)

# Example polylimits (a): best growth constant
gbest = 1 + 2 * mp.sqrt(2)
print("     Ex polylimits(a): best g =", mp.nstr(gbest, 8), " kappa with best g =", mp.nstr(12 / gbest, 8))

print("ALL PASS" if ok else "SOME FAIL")
