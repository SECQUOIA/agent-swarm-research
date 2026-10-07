# Analytic existence proof for hvycrash, checked in exact rationals.
# On the feasible set: theta_k - theta_{k-1} = kappa(c_k) / (-cos theta_k),
# kappa(c) = 10*h*(A(c)+1)*D(c), h = 0.00437, A = c/(0.01+0.3c^2), D = 0.0162079 + 0.486237 c^2.
from fractions import Fraction as F
from mpmath import iv, mp
h = F("0.00437")
def kappa(c):
    A = c / (F("0.01") + F("0.3") * c * c)
    D = F("0.0162079") + F("0.486237") * c * c
    return 10 * h * (A + 1) * D, A, D
for c in (F("0.08"), F("0.417")):
    k, A, D = kappa(c)
    print("c =", c, " A =", float(A), " D =", float(D), " kappa =", float(k))
k, A, D = kappa(F("0.08"))
# Claim: with theta_50 = 3 and the backward recursion, every theta_k lies in [2.6, 3].
# Needs: -cos(2.6) >= 0.85 and 50*kappa/0.85 <= 3 - 2.6 = 0.4; also 2.6 > pi/2 and 3 < pi.
iv.dps = 50
print("cos(2.6) in", iv.cos(iv.mpf("2.6")), "; pi/2 =", iv.pi / 2)
# exact Taylor bound for cos(2.6) <= -0.85 without libraries:
# cos x = sum (-1)^n x^(2n)/(2n)!, alternating with decreasing terms once x^2/((2n+1)(2n+2)) < 1;
x = F(26, 10); s = F(0); t = F(1); n = 0
partial = []
while n < 30:
    s += t; partial.append(s)
    t = -t * x * x / ((2 * n + 1) * (2 * n + 2)); n += 1
# terms decrease in absolute value for n >= 2 (x^2 = 6.76 < (2n+1)(2n+2) for n >= 1); partial sums bracket cos x
lo, hi = min(partial[-1], partial[-2]), max(partial[-1], partial[-2])
print("Taylor bracket for cos 2.6:", float(lo), float(hi), " hi <= -0.85:", hi <= F("-0.85"))
print("50*kappa/0.85 =", float(50 * k / F("0.85")), " <= 0.4:", 50 * k / F("0.85") <= F("0.4"))
# pi bounds: 3 < pi (Archimedes 223/71 < pi) and pi/2 < 1.6 < 2.6
print("3 < 223/71:", F(3) < F(223, 71), "; 22/7/2 =", float(F(22, 7) / 2), "< 2.6")
# Construct the point numerically and report theta_0 (illustration only)
mp.dps = 50
th = mp.mpf(3); ths = [th]
kf = mp.mpf(k.numerator) / k.denominator
for _ in range(50):
    th = th - kf / (-mp.cos(th)); ths.append(th)
print("theta_0 =", mp.nstr(ths[-1], 20), " theta_49 =", mp.nstr(ths[1], 20))
