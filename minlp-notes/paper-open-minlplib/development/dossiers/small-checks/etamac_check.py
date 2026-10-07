from fractions import Fraction as Fr
from mpmath import iv, mp
iv.dps = 50; mp.dps = 50
p1, p2, p3, q = Fr(".342222222222222"), Fr(".427777777777778"), Fr(".794444444444445"), Fr(".818181818181818")
s = (p2 + p3) * q
print("p1*q =", float(p1 * q), " s - 1 =", float(s - 1), " s =", s)
print("1/q =", float(1 / q), " -1/q (power-mean exponent) =", float(-1 / q))
for W in ("1015.6000321087411", "2022.06", "2062.83"):
    k = iv.exp((iv.mpf(s.numerator) / s.denominator - 1) * iv.log(iv.mpf(W)))
    print("W =", W, " W^(s-1) upper =", mp.nstr(k.b, 25), " <= 1.000000000000004:", k.b <= iv.mpf("1.000000000000004").a)
# displays
cert = Fr("-15.2946756433680921684870123983")   # verifier l(xh) lower end (dual bound -15.294675643368092168...)
print("display -15.294675643368093 <= certified bound:", Fr("-15.294675643368093") <= Fr("-15.294675643368092168"))
prim_hi = Fr("-15.2946756433680895919829233612845357438291772")
print("primal upper end - certified dual =", float(prim_hi - Fr("-15.294675643368092168")))
print("suggested primal display -15.29467564336808959 >= primal upper end:", Fr("-15.29467564336808959") >= prim_hi)
