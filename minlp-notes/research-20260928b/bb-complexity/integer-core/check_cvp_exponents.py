"""Exponents in Section 3 (random CVP), computed to 12 digits.

R_KL(theta): Kabatiansky-Levenshtein bound, (1/n) log2 A(n, theta) <= R_KL(theta) + o(1)
for spherical codes with minimal angle theta in (0, pi/2):
  R_KL = (1+s)/(2s) log2((1+s)/(2s)) - (1-s)/(2s) log2((1-s)/(2s)),  s = sin(theta).
Sanity: R_KL(60 deg) = 0.4014 (kissing-number exponent).

Reported:
  clique lower exponent  e_w-   = 0.5 log2(4/3)                        (Theorem 3.4)
  class lower exponent   e_k-   = 0.5 log2(3/2)                        (Theorem 3.5)
  clique upper exponent  e_w+   = max_{1<rho<2} min(0.5 log2 rho, R_KL(arccos((2-rho)/rho)))
                                                                        (Proposition 3.6(c))
  class upper exponent   e_k+   = 0.5                                  (Proposition 3.6(b))
  optional refinement of e_k- with KL applied to caps (Remark 3.5a):
      max_{rho in [3/2, 2]} 0.5 log2 rho - R_KL(theta), 2 sin(theta/2) = 1/sqrt(rho-1)
"""
import mpmath as mp

mp.mp.dps = 30


def RKL(theta):
    s = mp.sin(theta)
    if s >= 1:
        return mp.mpf(0)
    a = (1 + s) / (2 * s)
    b = (1 - s) / (2 * s)
    return a * mp.log(a, 2) - b * mp.log(b, 2)


print("R_KL(60 deg) =", mp.nstr(RKL(mp.pi / 3), 6))
ew_minus = mp.log(mp.mpf(4) / 3, 2) / 2
ek_minus = mp.log(mp.mpf(3) / 2, 2) / 2
print("clique lower exponent 0.5 log2(4/3) =", mp.nstr(ew_minus, 12))
print("class  lower exponent 0.5 log2(3/2) =", mp.nstr(ek_minus, 12))


def upper_w(rho):
    theta = mp.acos((2 - rho) / rho)
    return min(mp.log(rho, 2) / 2, RKL(theta))


# the min is increasing then decreasing; locate the crossing
f = lambda rho: mp.log(rho, 2) / 2 - RKL(mp.acos((2 - rho) / rho))
rho_star = mp.findroot(f, 1.44)
print("clique upper exponent: crossing rho* =", mp.nstr(rho_star, 10), " exponent =", mp.nstr(mp.log(rho_star, 2) / 2, 12))
grid = [1 + mp.mpf(i) / 1000 for i in range(1, 1000)]
print("   grid max of min(...) over rho in (1,2):", mp.nstr(max(upper_w(r) for r in grid), 12))


def ref_k(rho):
    a = mp.sqrt(rho - 1)
    x = 1 / (2 * a)
    if x >= 1:
        return mp.log(rho, 2) / 2
    theta = 2 * mp.asin(x)
    if theta >= mp.pi / 2:
        return mp.log(rho, 2) / 2
    return mp.log(rho, 2) / 2 - RKL(theta)


gridk = [mp.mpf(3) / 2 + mp.mpf(i) / 2000 for i in range(0, 1001)]
best = max(gridk, key=ref_k)
print("class lower exponent with KL on caps: max at rho =", mp.nstr(best, 6), " exponent =", mp.nstr(ref_k(best), 8))
print("separation: e_k- - e_w+ =", mp.nstr(ek_minus - mp.log(rho_star, 2) / 2, 8))
