from fractions import Fraction as Fr
from mpmath import iv, mp
iv.dps = 60; mp.dps = 60
data = {
 "ex6_2_7": dict(lam=["-0.23993666802341555716", "-0.54068374800661316808", "-0.021609146907096643708"],
                 b=["0.4", "0.1", "0.5"], tau="6e-15", phases=3, R="5e-14"),
 "ex6_2_5": dict(lam=["-0.92114611232187116319", "-2.2777893037791928146", "-0.40139310690864392314"],
                 b=["40.30707", "5.14979", "54.54314"], tau="1e-17", phases=2, R="0"),
}
for name, d in data.items():
    lb = sum(Fr(l) * Fr(b) for l, b in zip(d["lam"], d["b"]))
    tmax = sum(Fr(b) for b in d["b"])
    term = d["phases"] * min(Fr(0), tmax * (-Fr(d["tau"])))
    bound = iv.mpf(lb.numerator) / lb.denominator + iv.mpf(term.numerator) / term.denominator \
        - 3 * iv.mpf(d["R"]) / iv.e
    print(name, "lam.b =", mp.nstr(mp.mpf(lb.numerator) / lb.denominator, 30), " tmax =", tmax)
    print("   bound lower end =", mp.nstr(bound.a, 30))
# ideal phase of ex6_2_5: min over simplex of sum y ln y - sum y (lam - c) = -ln sum exp(lam - c)
lam = [iv.mpf(s) for s in data["ex6_2_5"]["lam"]]; c = iv.mpf(".156969560191053")
m = -iv.log(sum(iv.exp(l - c) for l in lam))
print("ex6_2_5 ideal-phase tangent-plane minimum in", m)
# ex6_2_7 R_p: t ln t coefficient of the n3 terms in the OSIL objective
print("ex6_2_7 R_3 =", Fr("8.73945638067505") + Fr("1.868") - Fr("10.607456380675"))
print("summary displays:")
for nm, disp, cert in (("ex6_2_7", "-0.16084761546364905", "-0.1608476154636490434421757163"),
                       ("ex6_2_5", "-70.75207783344770759", "-70.7520778334477075803539469")):
    print("  ", nm, "display <= certified:", Fr(disp) <= Fr(cert))
# primal enclosures (verifier) and gap displays
for nm, prim, dual, shown in (("ex6_2_7", "-0.16084761546360086152", "-0.16084761546364904344", "4.9e-14"),
                              ("ex6_2_5", "-70.75207783344770558", "-70.7520778334477075803539469", "2.1e-15")):
    print("  ", nm, "primal(20 digits) - certified dual =", float(Fr(prim) - Fr(dual)), "<=", shown)
