# Independent recomputation of the pricing050 Lagrangian upper bound (own OSIL parser, own 1-D B&B).
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr
from mpmath import iv, mp
import time
ns = {"o": "os.optimizationservices.org"}
root = ET.parse("pricing050.osil").getroot()
q = lambda tag: "{os.optimizationservices.org}" + tag
vars_ = root.find(".//o:variables", ns).findall("o:var", ns)
n = len(vars_)
lb = [v.get("lb", "0") for v in vars_]; ub = [v.get("ub", "INF") for v in vars_]
assert all(l == "0" for l in lb) and all(u == "10" for u in ub)
obj = root.find(".//o:objectives/o:obj", ns)
assert obj.get("maxOrMin") == "max" and obj.get("constant") in (None, "0")
cobj = [Fr(0)] * n
for c in obj.findall("o:coef", ns):
    cobj[int(c.get("idx"))] = -Fr(c.text)           # min form: minimize c.x
assert all(v >= 0 for v in cobj)
cons = root.find(".//o:constraints", ns).findall("o:con", ns)
rhs = [c.get("ub") for c in cons]; assert all(c.get("lb") is None for c in cons)
print("rows:", [c.get("name") for c in cons], "rhs:", rhs)
lin = root.find(".//o:linearConstraintCoefficients", ns)
assert lin is None or int(lin.get("numberOfValues", "0")) == 0
terms = {}  # (row, j) -> (a, g, p)
for nl in root.find(".//o:nonlinearExpressions", ns).findall("o:nl", ns):
    i = int(nl.get("idx")); s = list(nl)[0]; assert s.tag == q("sum")
    for prod in s:
        assert prod.tag == q("product") and len(prod) == 2
        e, v = prod
        assert e.tag == q("exp") and v.tag == q("variable")
        j = int(v.get("idx")); a = v.get("coef")
        arg = e[0]
        if arg.tag == q("variable"):
            assert int(arg.get("idx")) == j; g, p = arg.get("coef"), 1
        else:
            assert arg.tag == q("product") and len(arg) == 2
            base, num = arg
            assert num.tag == q("number")
            g = num.get("value")
            if base.tag == q("square"):
                assert int(base[0].get("idx")) == j and base[0].get("coef") in (None, "1"); p = 2
            else:
                assert base.tag == q("power") and int(base[0].get("idx")) == j and base[1].get("value") == "3"; p = 3
        assert (i, j) not in terms and Fr(a) < 0 and Fr(g) < 0
        terms[(i, j)] = (a, g, p)
print("terms:", len(terms), "distinct g:", sorted({t[1] for t in terms.values()}))
mu = {3: "3.0489011208166370021", 4: "2.1677509642745686136"}   # e5, e6 (verifier/author multipliers)
assert [cons[i].get("name") for i in mu] == ["e5", "e6"]
iv.dps = 50; mp.dps = 50
MU = {i: iv.mpf(v) for i, v in mu.items()}
T = {k: (iv.mpf(a), iv.mpf(g), p) for k, (a, g, p) in terms.items() if k[0] in mu}
C = [iv.mpf(c.numerator) / c.denominator for c in cobj]
def pw(X, p):
    r = X
    for _ in range(p - 1): r = r * X
    return r
def Fv(j, X):
    s = C[j] * X
    for i in mu:
        if (i, j) in T:
            a, g, p = T[(i, j)]
            s = s + MU[i] * a * X * iv.exp(g * pw(X, p))
    return s
def F1(j, X):
    s = C[j]
    for i in mu:
        if (i, j) in T:
            a, g, p = T[(i, j)]
            u = g * pw(X, p)
            s = s + MU[i] * a * iv.exp(u) * (1 + p * u)
    return s
def certify(j, tol=mp.mpf("1e-25")):
    U = min(Fv(j, iv.mpf(0)).b, Fv(j, iv.mpf(10)).b)
    stack = [(mp.mpf(0), mp.mpf(10))]
    lbs = []; nb = 0
    while stack:
        lo, hi = stack.pop(); nb += 1
        X = iv.mpf([lo, hi]); d1 = F1(j, X)
        if d1.a >= 0:
            lbs.append(Fv(j, iv.mpf(lo)).a); continue
        if d1.b <= 0:
            lbs.append(Fv(j, iv.mpf(hi)).a); continue
        c = (lo + hi) / 2
        Fc = Fv(j, iv.mpf(c)); U = min(U, Fc.b)
        lbv = max(Fv(j, X).a, (Fc + d1 * (X - c)).a)
        if lbv >= U - tol:
            lbs.append(lbv); continue
        assert hi - lo > mp.mpf("1e-40")
        stack += [(lo, c), (c, hi)]
    return min(lbs), U, nb
t0 = time.time()
tot_lb = iv.mpf(0); tot_U = mp.mpf(0); nbt = 0
for j in range(n):
    l, U, nb = certify(j)
    tot_lb = tot_lb + iv.mpf(l); tot_U += U; nbt += nb
muR = sum(MU[i] * iv.mpf(rhs[i]) for i in mu)
UB = muR - tot_lb
print("boxes:", nbt, "time %.1f s" % (time.time() - t0))
print("sum min F_j >=", mp.nstr(tot_lb.a, 30), "; sum of point upper values", mp.nstr(tot_U, 30))
print("upper bound (max form) <=", mp.nstr(UB.b, 30))
disp = mp.mpf("-1813.8290784519730577")
print("display -1813.8290784519730577 minus certified UB =", mp.nstr(disp - UB.b, 5), " (must be >= 0)")

# ---- rigorous check of the author's saved primal point (logs/pricing050_primal.txt, copied) ----
pts = {}
for line in open("pricing050_primal.txt"):
    k, v = line.split(); pts[k] = v
names = [v.get("name") for v in vars_]
xs = [Fr(pts[nm]) for nm in names]
assert all(Fr(0) <= v <= 10 for v in xs)
allT = {k: (iv.mpf(a), iv.mpf(g), p) for k, (a, g, p) in terms.items()}
X = [iv.mpf(v.numerator) / v.denominator for v in xs]
slack = []
for i in range(5):
    s = iv.mpf(0)
    for j in range(n):
        if (i, j) in allT:
            a, g, p = allT[(i, j)]
            s = s + a * X[j] * iv.exp(g * pw(X[j], p))
    slack.append(iv.mpf(rhs[i]) - s)
print("row slacks (rhs - row), lower ends:", [mp.nstr(sl.a, 4) for sl in slack])
assert all(sl.a > 0 for sl in slack)
objmax = -sum(cobj[j] * xs[j] for j in range(n))
print("author primal objective (max form, exact):", mp.nstr(mp.mpf(objmax.numerator) / objmax.denominator, 25))
print("gap UB - primal <=", mp.nstr(UB.b - mp.mpf(objmax.numerator) / objmax.denominator, 5))
