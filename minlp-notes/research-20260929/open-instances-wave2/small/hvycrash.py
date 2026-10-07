"""hvycrash: the objective is constant (-0.2185) on the exactly feasible set,
and the feasible set is nonempty.

1. Structure: every row, bound and the objective are asserted by exact string
   equality against the expected expression trees (osilx keeps decimal strings).
   Stage k = 1..50: th_k = x{k}, c_k = x{50+k}, r_k = x{101+k}, th_0 = x101,
   accumulator s_k = x{202-k} (s_1 = x201, s_50 = x152 = objective).
     acc_k : -s_k + s_{k-1} + 4.37e-3 cos(th_k) / (D_k r_k^2) = 0      (s_0 := 0)
     alg_k : -1/r_k - cos(th_k) / (D_k r_k^3) = 0
     dyn_k : .1 th_{k-1} + 4.37e-3 c_k/((.3 c_k^2 + 1e-2) r_k^2)
             - 4.37e-3 cos(th_k)/(D_k r_k^4) - .1 th_k = 0
   with D_k = .486237 c_k^2 + 1.62079e-2 > 0.
2. Identity (exact): alg_k needs r_k != 0; multiplying by -r_k gives
   cos(th_k)/(D_k r_k^2) = -1, so the accumulator increment is exactly -4.37e-3
   and x152 = -50 * 4.37e-3 = -0.2185 (checked in Fraction arithmetic).
3. Existence: an explicit real feasible point, built backwards:
   c_k = 8e-2, th_50 = 3, r_k = sqrt(-cos th_k / D_k) (alg_k holds identically),
   th_{k-1} solved from the linear row dyn_k (holds identically). Feasibility then
   only needs bounds, verified with mpmath interval arithmetic.
4. 60-digit evaluation of that point and of MINLPLib p1..p3 (via ev.py).
"""
import os
import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402

I = ev.load("hvycrash")
NM = I["names"]
ix = {n: j for j, n in enumerate(NM)}


def V(name, coef="1"):
    return ("var", ix[name], coef)


def Dt(c):
    return ("sum", ("product", V(c, ".486237"), V(c)), ("num", "1.62079e-2"))


# ---------- 1. structure ----------
assert len(NM) == 201 and len(I["cons"]) == 150
for k in range(1, 51):
    assert (I["lb"][ix[f"x{k}"]], I["ub"][ix[f"x{k}"]]) == ("0", "6.2831854")
    assert (I["lb"][ix[f"x{50+k}"]], I["ub"][ix[f"x{50+k}"]]) == ("8e-2", ".417")
    assert (I["lb"][ix[f"x{101+k}"]], I["ub"][ix[f"x{101+k}"]]) == ("-INF", "INF")
    assert (I["lb"][ix[f"x{151+k}"]], I["ub"][ix[f"x{151+k}"]]) == ("-INF", "INF")
assert (I["lb"][ix["x101"]], I["ub"][ix["x101"]]) == ("0", "6.2831854")
assert all(t == "C" for t in I["vt"])
o = I["obj"]
assert o["sense"] == "min" and o["constant"] == "0" and o["lin"] == {ix["x152"]: "1"} and not o["quad"] and o["nl"] is None
for k in range(1, 51):
    th, c, r = f"x{k}", f"x{50+k}", f"x{101+k}"
    thp = "x101" if k == 1 else f"x{k-1}"
    acc, alg, dyn = I["cons"][3 * (k - 1): 3 * k]
    for R in (acc, alg, dyn):
        assert R["lb"] == R["ub"] == "0" and R["constant"] == "0" and not R["quad"]
    A = ("divide", ("product", ("cos", V(th)), ("num", "4.37e-3")), ("product", Dt(c), V(r), V(r)))
    assert acc["nl"] == A
    s_k, s_prev = f"x{202-k}", f"x{203-k}"
    assert acc["lin"] == ({ix[s_k]: "-1"} if k == 1 else {ix[s_k]: "-1", ix[s_prev]: "1"})
    assert alg["lin"] == {}
    assert alg["nl"] == ("sum", ("negate", ("divide", ("num", "1"), V(r))),
                         ("negate", ("divide", ("cos", V(th)), ("product", Dt(c), V(r), V(r), V(r)))))
    assert dyn["lin"] == {ix[thp]: ".1"}
    assert dyn["nl"] == ("sum",
                         ("divide", V(c, "4.37e-3"), ("product", ("sum", ("product", V(c, ".3"), V(c)), ("num", "1e-2")), V(r), V(r))),
                         ("negate", ("divide", ("product", ("cos", V(th)), ("num", "4.37e-3")),
                                     ("product", Dt(c), V(r), V(r), V(r), V(r)))),
                         V(th, "-.1"))
print("structure: all 150 rows, 201 bounds and the objective match the expected pattern exactly")

# ---------- 2. identity ----------
# alg_k * (-r_k):  1 + cos(th)/(D r^2) = 0  (valid since r_k != 0 on the domain of 1/r_k)
# acc_k increment: 4.37e-3 * cos(th)/(D r^2) = 4.37e-3 * (-1)
val = sum(Fraction("4.37e-3") * Fraction(-1) for _ in range(50))
assert val == Fraction("-0.2185")
print("identity: x152 = sum_k 4.37e-3 * (-1) =", val, "= -0.2185 exactly on the feasible set")
# D_k > 0: .486237 c^2 >= 0 and 1.62079e-2 > 0.

# ---------- 3. existence (interval arithmetic) ----------
iv = mp.iv
iv.dps = 50
c_iv = iv.mpf("8e-2")
D_iv = iv.mpf(".486237") * c_iv * c_iv + iv.mpf("1.62079e-2")
g_den = iv.mpf(".3") * c_iv * c_iv + iv.mpf("1e-2")
th = [None] * 51
th[50] = iv.mpf(3)
TWO_PI_UB = iv.mpf("6.2831854")
for k in range(50, 0, -1):
    cs = iv.cos(th[k])
    assert cs.b < 0, (k, cs)                      # cos(th_k) < 0, so r_k is real and nonzero
    r2 = -cs / D_iv                               # r_k^2 = -cos/D
    # dyn_k solved for th_{k-1}: .1 th_{k-1} = .1 th_k - 4.37e-3 c/(g_den r^2) + 4.37e-3 cos/(D r^4)
    rhs = iv.mpf(".1") * th[k] - iv.mpf("4.37e-3") * c_iv / (g_den * r2) + iv.mpf("4.37e-3") * cs / (D_iv * r2 * r2)
    th[k - 1] = rhs / iv.mpf(".1")
for k in range(51):
    assert th[k].a >= 0 and th[k].b <= TWO_PI_UB.a, (k, th[k])
print("existence: backward construction stays in bounds; th_0 in", mp.nstr(th[0], 12), "; th_1 in", mp.nstr(th[1], 12),
      "; all cos(th_k) < 0 for k>=1")

# ---------- 4. high-precision point of the construction ----------
mp.mp.dps = 60
thp = [None] * 51
thp[50] = mp.mpf(3)
cc = mp.mpf("8e-2")
Dp = mp.mpf(".486237") * cc * cc + mp.mpf("1.62079e-2")
gd = mp.mpf(".3") * cc * cc + mp.mpf("1e-2")
rr = [None] * 51
for k in range(50, 0, -1):
    cs = mp.cos(thp[k])
    rr[k] = mp.sqrt(-cs / Dp)
    r2 = rr[k] ** 2
    thp[k - 1] = (mp.mpf(".1") * thp[k] - mp.mpf("4.37e-3") * cc / (gd * r2) + mp.mpf("4.37e-3") * cs / (Dp * r2 * r2)) / mp.mpf(".1")
x = [mp.mpf(0)] * 201
x[ix["x101"]] = thp[0]
s = mp.mpf(0)
for k in range(1, 51):
    x[ix[f"x{k}"]] = thp[k]
    x[ix[f"x{50+k}"]] = cc
    x[ix[f"x{101+k}"]] = rr[k]
    s += mp.mpf("4.37e-3") * mp.cos(thp[k]) / (Dp * rr[k] ** 2)
    x[ix[f"x{202-k}"]] = s
res = ev.evaluate(I, x, dps=60)
print("constructed point (60 digits): obj", mp.nstr(res["obj"], 25), "max row viol", mp.nstr(res["row_viol"], 3),
      "max bound viol", mp.nstr(res["bound_viol"], 3))
with open(os.path.join(ev.HERE, "logs", "hvycrash_point.txt"), "w") as f:
    for j, n in enumerate(NM):
        f.write(f"{n} {mp.nstr(x[j], 50)}\n")

# ---------- 5. MINLPLib points ----------
for tag in ("hvycrash.p1", "hvycrash.p2", "hvycrash.p3"):
    r = ev.eval_sol(tag, dps=50)
    print(f"{tag}: obj {mp.nstr(r['obj'], 18)}  max row viol {mp.nstr(r['row_viol'], 3)} ({r['worst_row']})  bound viol {mp.nstr(r['bound_viol'], 3)}")
# per-stage view of p3: increment ratio cos/(D r^2) (should be -1)
vals = ev.read_sol(os.path.join(ev.HERE, "sol", "hvycrash.p3.sol"))
mp.mp.dps = 50
dev = []
for k in range(1, 51):
    t, c, r = (mp.mpf(vals[f"x{k}"]), mp.mpf(vals[f"x{50+k}"]), mp.mpf(vals[f"x{101+k}"]))
    D = mp.mpf(".486237") * c * c + mp.mpf("1.62079e-2")
    dev.append(abs(mp.cos(t) / (D * r * r) + 1))
print("p3: max_k |cos(th_k)/(D_k r_k^2) + 1| =", mp.nstr(max(dev), 3))
