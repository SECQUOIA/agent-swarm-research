"""Check the lukvle10 dual shown in open-instances-summary.md line 26 against the verifier's bound.

The verifier (reviews/open-instances-verification/v_lukvle10_bnb.py, lines 298-312) certifies
    bound = sum_g count_g * (LB_g - 1e-18) + (LB_tail - 1e-18) + sum_{j<994} lam_j,
with lam = the stored KKT multipliers, lam[30:961] set to lam[495], and LB strings as stored in
logs/lukvle10_bnb.json. This script
  (1) evaluates that expression exactly in rationals (no stored sum_lam string is used), and
  (2) replays the verifier's own 64-bit interval evaluation in the same order and takes lo(bound).
Reads only; writes nothing."""
import json, os
from fractions import Fraction as F
import numpy as np
import mpmath
from mpmath import iv, mp

V = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "open-instances-verification", "logs")
d = json.load(open(os.path.join(V, "lukvle10_bnb.json")))
lam = np.load(os.path.join(V, "lukvle10_lam_kkt.npy")).copy()
M = 994
LC = lam[495]
lam[30:961] = LC
assert float(LC) == d["LC"] and d["n_groups"] == len(d["groups"])
assert sum(g["count"] for g in d["groups"]) == 497

# (1) exact rational value of the certified expression
eps = F("1e-18")
T = sum(g["count"] * (F(g["LB"]) - eps) for g in d["groups"]) + (F(d["tail"]["LB"]) - eps)
S = sum(F(float(lam[j])) for j in range(M))
E = T + S

# (2) the verifier's own 64-bit interval evaluation, same operation order
iv.prec = 64; mp.prec = 64
tot = iv.mpf(0)
for g in d["groups"]:
    tot += g["count"] * (iv.mpf(g["LB"]) - iv.mpf("1e-18"))
tot += iv.mpf(d["tail"]["LB"]) - iv.mpf("1e-18")
s = iv.mpf(0)
for j in range(M):
    s += iv.mpf(float(lam[j]))
bound = tot + s
sg, man, ex, _ = bound._mpi_[0]  # exact binary value of lo(bound)
lo64 = (-1) ** sg * F(int(man)) * F(2) ** int(ex)
assert mpmath.nstr(mp.make_mpf(s._mpi_[0]), 20) == d["sum_lam"]
assert mpmath.nstr(mp.make_mpf(bound._mpi_[0]), 16) == d["dual_bound"]
assert lo64 <= E

mp.prec = 200
f = lambda q: mpmath.nstr(mpmath.mpf(q.numerator) / q.denominator, 24)
g = lambda q: mpmath.nstr(mpmath.mpf(q.numerator) / q.denominator, 4)
print("sum_lam exact            =", f(S), " stored string", d["sum_lam"])
print("certified value, exact   =", f(E))
print("verifier lo(bound), 64b  =", f(lo64), " (verifier prints", d["dual_bound"] + ")")
for label, shown in (("old display", "352.2380254050785"), ("new display", "352.2380254050784")):
    x = F(shown)
    print(label, shown, ": minus exact =", g(x - E), "; minus lo64 =", g(x - lo64), "; valid:", x <= lo64)
p5 = F("352.2380254064961")
print("gap cell: p5 - new display =", g(p5 - F("352.2380254050784")))
