# Critic: replay the stored 0030p multipliers on the 0039 reviewer's own rows (own_osil/own_relax),
# using the reviewer's exact Lagrangian and its Cholesky + exact residual + Gershgorin PSD bound,
# and additionally an exact LDL^T (own code) on A.
import json, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/pfcrit/rev")
import verify_leaves as vl
import own_relax as orl
import pf_model as pm
name = "powerflow0030p"
D = json.load(open("/tmp/pfcrit/rev/logs/powerflow0030p.sdpcert.json"))
R = orl.build(name)
M = pm.decode(name)
order = [r["name"] for r in M["rows"] if r["kind"] != "angle"]
assert len(order) == len(D["raw"]) == 332, (len(order), len(D["raw"]))
rows = [R["rows"][nm] for nm in order]
const, inner, A, clipped = vl.lagrangian(R, rows, dict(R["ybox"]), D["raw"])
t = time.time()
shift, lam, eps = vl.psd_shift(A)
vm2 = sum(R["vmax2"])
bound = const + inner + min(Fr(0), shift) * vm2
# own exact LDL^T (no pivoting; fails loudly on a non-positive pivot)
n = len(A); Mx = [row[:] for row in A]; minpiv = None
for k in range(n):
    d = Mx[k][k]
    assert d > 0, ("pivot", k, d)
    minpiv = d if minpiv is None else min(minpiv, d)
    for i in range(k + 1, n):
        if Mx[i][k] != 0:
            f = Mx[i][k] / d
            for j in range(k + 1, n):
                if Mx[k][j] != 0:
                    Mx[i][j] -= f * Mx[k][j]
ex = const + inner
st = Fr(D["bound_exact"])
print(f"{name}: own rows {len(rows)} (order from pf_model names), sum vmax2 {vm2}, clipped {clipped}")
print(f"  lam_min(A) {lam:.6e}; Gershgorin shift {float(shift):.3e}; bound (Gershgorin) {float(bound)!r}")
print(f"  exact LDL^T: {n} positive pivots, min {float(minpiv):.4e}; eps=0 bound const+inner == stored bound_exact: {ex == st}")
from decimal import Decimal, getcontext; getcontext().prec = 40
print(f"  const+inner = {Decimal(ex.numerator)/Decimal(ex.denominator)}")
