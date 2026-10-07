# Critic: small exact checks (containment, leaf identity values, envelope error, gaps, displays)
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec = 40
D = lambda x: Decimal(x.numerator) / Decimal(x.denominator)
b = Fr(69060773480663, 1250000000000)
assert b == Fr("55.2486187845304") and abs(float(b) - 1/0.0181) < 1e-12
F = lambda p, q, s: s - 2*q/b + (q*q + p*p)/(b*b*s)
pts = {"0039p": Fr(41964029348667, 6250000000000), "0039r": Fr(167856117394623, 25000000000000)}
leaf = {"0039p": [(Fr(3024409,450773), Fr(449605480,66644851)), (Fr(7,5), Fr(83,50)), (Fr(2749,2500), Fr(2809,2500))],
        "0039r": [(Fr(1327418,197845), Fr(5938456,884431)), (Fr(7,5), Fr(713,500)), (Fr(2803,2500), Fr(2809,2500))]}
for k, Pg in pts.items():
    z = (Pg, Fr(7,5), Fr(2809,2500))
    inside = all(lo <= v <= hi for v, (lo, hi) in zip(z, leaf[k]))
    print(k, "x* (Pg,Qg,W_LL) in decisive leaf:", inside, "; W_NN(x*) = F exactly =", D(F(*z)), "; v2 =", D(F(*z)).sqrt())
    print("   leaf box decimals", [[float(a), float(c)] for a, c in leaf[k]])
# root envelope error along Pg at Qg = 1.4, W_LL = 1.1236
p = Fr(6714, 1000); s = Fr(2809, 2500)
print("root Pg-envelope error at Pg=6.714:", float(p*(Fr(52,5)-p)/(b*b*s)))
# gaps and displays
cert = {"0030p": "576.89341229880046984915963178631773750440513386654",
        "0039p": None, "0039r": None}
up = {"0030p": Fr("576.8934134703742598676684"), "0039p": Fr("41869.0515113202038027683845"), "0039r": Fr("41869.0515113209830932768582")}
lo = {"0030p": Fr("576.8934134703742598676683"), "0039p": Fr("41869.0515113202038027683844"), "0039r": Fr("41869.0515113209830932768581")}
disp = {"0030p": Fr("576.8934122988004"), "0039p": Fr("41869.05148485014"), "0039r": Fr("41869.05148327243")}
pdisp = {"0030p": Fr("576.8934134704"), "0039p": Fr("41869.0515113203"), "0039r": Fr("41869.0515113210")}
best = {"0030p": Fr("572.8395847"), "0039p": Fr("41818.27916"), "0039r": Fr("41804.88153")}
p1 = {"0039p": Fr("41869.051511320199159"), "0039r": Fr("41869.051511320800473")}
for k in up:
    g = up[k] - disp[k]
    print(k, "abs gap", "%.10e" % float(g), "rel/dual %.6e" % float(g/disp[k]), "rel/primal %.6e" % float(g/up[k]),
          "primal display >= upper:", pdisp[k] >= up[k], "dual < lower:", disp[k] < lo[k], "improvement %.5f" % float(disp[k]-best[k]))
    if k in p1: print("   enclosure lower - obj(p1) = %.4e" % float(lo[k]-p1[k]))
print("0039r display ...244 - 41869051483272433/1e12 =", float(Fr("41869.05148327244") - Fr(41869051483272433, 10**12)))
print("41869051483272433/1e12 =", D(Fr(41869051483272433, 10**12)))
print("GUROBI 0039p point below dual by", float(Fr("41869.05148485014") - Fr("41869.0502370")))
print("sum vmax2 0030p:", 25*Fr(105,100)**2 + 5*Fr(110,100)**2, " 0039:", 39*Fr(106,100)**2)
print("0.94^2, 1.06^2:", Fr(94,100)**2, Fr(106,100)**2)
