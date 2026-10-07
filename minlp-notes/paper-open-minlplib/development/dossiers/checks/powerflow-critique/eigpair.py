# Critic: smallest eigenvalues of A(w) at 50 digits for the 0030p root and the 0039p decisive leaf
import json, sys
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, "/tmp/pfcrit/rev")
import verify_leaves as vl, own_relax as orl, pf_model as pm
def small_eigs(A, k=4):
    with mp.workdps(50):
        Am = mp.matrix([[mp.mpf(a.numerator) / a.denominator for a in row] for row in A])
        ev = sorted(mp.eigsy(Am, eigvals_only=True))
        return [mp.nstr(e, 15) for e in ev[:k]]
# 0030p root
D = json.load(open("/tmp/pfcrit/rev/logs/powerflow0030p.sdpcert.json"))
R = orl.build("powerflow0030p"); M = pm.decode("powerflow0030p")
rows = [R["rows"][r["name"]] for r in M["rows"] if r["kind"] != "angle"]
A = vl.lagrangian(R, rows, dict(R["ybox"]), D["raw"])[2]
print("0030p root, 4 smallest eigenvalues (50 digits):", small_eigs(A))
# 0039p decisive leaf, with and without angle multipliers
D = json.load(open("/tmp/pfcrit/rev/logs/powerflow0039p.bb3t.json"))
R = orl.build("powerflow0039p"); M = pm.decode("powerflow0039p"); ld = vl.leaf_data(R)
lf = D["leaves"][0]; bx = tuple((Fr(a), Fr(c)) for a, c in lf["box"])
rows, ybox, npl = vl.node_rows(R, M, ld, bx)
A = vl.lagrangian(R, rows, ybox, lf["raw"])[2]
print("0039p decisive leaf, stored multipliers:", small_eigs(A))
raw = [list(x) for x in lf["raw"]]
for i, r in enumerate(M["rows"]):
    if r["kind"] == "angle": raw[i] = ["ineq", None, None]
A = vl.lagrangian(R, rows, ybox, raw)[2]
print("0039p decisive leaf, angle multipliers zeroed:", small_eigs(A))
amax = max(max(abs(x[1] or 0), abs(x[2] or 0)) for i, x in enumerate(lf["raw"]) if M["rows"][i]["kind"] == "angle")
print("largest stored angle multiplier on decisive leaf:", amax)
