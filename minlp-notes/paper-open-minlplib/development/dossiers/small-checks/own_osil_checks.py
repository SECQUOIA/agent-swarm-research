import json, sys
from fractions import Fraction as Fr
from mpmath import mp, iv
import osil_own as O
mp.dps = 60; iv.dps = 60
MPF = dict(exp=mp.exp, log=mp.log, cos=mp.cos, sqrt=mp.sqrt)
IVF = dict(exp=iv.exp, log=iv.log, cos=iv.cos, sqrt=iv.sqrt)
mpn = lambda s: mp.mpf(s); ivn = lambda s: iv.mpf(s)
# ---- hvycrash: analytic point c_k = 0.08, theta_50 = 3 (independent construction and parser) ----
m = O.read("hvycrash.osil")
nm = {n: i for i, n in enumerate(m["names"])}
print("hvycrash vars", len(m["names"]), "rows", len(m["cons"]), "obj lin", m["olin"], "sense", m["sense"])
h = Fr("0.00437"); c = Fr("0.08")
Dc = Fr("0.0162079") + Fr("0.486237") * c * c; A = c / (Fr("0.01") + Fr("0.3") * c * c)
kap = 10 * h * (A + 1) * Dc
th = {50: iv.mpf(3)}
for k in range(50, 0, -1):
    th[k - 1] = th[k] - iv.mpf(kap.numerator) / kap.denominator / (-iv.cos(th[k]))
x = [None] * len(m["names"])
for k in range(1, 51):
    x[nm["x%d" % k]] = th[k]; x[nm["x%d" % (50 + k)]] = iv.mpf("0.08")
    x[nm["x%d" % (101 + k)]] = iv.sqrt(-iv.cos(th[k]) / (iv.mpf(Dc.numerator) / Dc.denominator))
    x[nm["x%d" % (202 - k)]] = -iv.mpf(k) * iv.mpf("0.00437")
x[nm["x101"]] = th[0]
assert all(v is not None for v in x)
viol = mp.mpf(0)
for i, cn in enumerate(m["cons"]):
    v = O.row(m, i, x, ivn, IVF)
    assert cn["lb"] == cn["ub"]
    viol = max(viol, abs(mp.mpf(v.a) - mp.mpf(cn["lb"])), abs(mp.mpf(v.b) - mp.mpf(cn["lb"])))
bnd_ok = all((m["lb"][j] == "-INF" or x[j].a >= mp.mpf(m["lb"][j])) and (m["ub"][j] == "INF" or x[j].b <= mp.mpf(m["ub"][j])) for j in range(len(x)))
print("hvycrash analytic point: max |row - rhs| over interval enclosures", mp.nstr(viol, 3), "(rows hold as identities; this is enclosure width)")
print("  bounds hold on enclosures:", bnd_ok, " theta_0 in", mp.nstr(th[0].a, 15), " objective", O.objective(m, x, ivn, IVF))
# ---- Gibbs: objective at the verifier's exact primal points ----
for name in ("ex6_2_7", "ex6_2_5"):
    mm = O.read(name + ".osil")
    d = json.load(open(name + "_bound.json"))
    pt = [Fr(s) for s in d["own_primal_point"]]
    X = [iv.mpf(p.numerator) / p.denominator for p in pt]
    f = O.objective(mm, X, ivn, IVF)
    rows = [O.row(mm, i, X, ivn, IVF) for i in range(len(mm["cons"]))]
    print(name, "objective at verifier point:", mp.nstr(f.a, 25), mp.nstr(f.b, 25), "| rows:", [mp.nstr(r.a, 12) for r in rows],
          "rhs", [cn["lb"] for cn in mm["cons"]])
    # exact row check in rationals
    for i, cn in enumerate(mm["cons"]):
        assert sum(Fr(cf) * pt[j] for j, cf in mm["lin"][i].items()) == Fr(cn["lb"]) == Fr(cn["ub"])
    assert all(Fr(mm["lb"][j]) <= pt[j] <= Fr(mm["ub"][j]) for j in range(9))
    print("   rows exact and bounds hold (Fractions)")
# ---- etamac at MINLPLib p1 and pindyck at stored point ----
def readsol(path):
    d = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and p[0].startswith("x"): d[p[0]] = p[1]
    return d
me = O.read("etamac.osil"); s = readsol("etamac.p1.sol")
xe = [mp.mpf(s.get(n, "0")) for n in me["names"]]
print("etamac p1 objective (own parser):", mp.nstr(O.objective(me, xe, mpn, MPF), 16))
mpd = O.read("pindyck.osil"); s = readsol("pindyck_primal.txt")
xp = [mp.mpf(s.get(n, "0")) for n in mpd["names"]]
res = max(abs(O.row(mpd, i, xp, mpn, MPF) - mp.mpf(cn["lb"])) for i, cn in enumerate(mpd["cons"]))
print("pindyck stored point objective (own parser):", mp.nstr(O.objective(mpd, xp, mpn, MPF), 30), " max row residual", mp.nstr(res, 3))
