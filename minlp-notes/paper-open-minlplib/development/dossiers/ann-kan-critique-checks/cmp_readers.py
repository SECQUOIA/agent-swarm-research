"""Exact comparison of the shared osilx reader with the primal reviewer's independent rosil reader."""
import os, sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
import osilx, rosil
D = os.path.expanduser("~/.cache/minlplib/minlplib/osil")

def bnd(s, default_inf_sign):
    if osilx.isinf(s):
        return None
    return F(s)

def conv_tree(t):
    if t is None: return None
    if t[0] == "num": return ("num", F(t[1]))
    if t[0] == "var": return ("var", t[1], F(t[2]))
    return (t[0],) + tuple(conv_tree(c) for c in t[1:])

def run(name):
    A = osilx.read(os.path.join(D, name + ".osil"))
    B = rosil.load(name)
    issues = []
    assert A["names"] == B["names"]
    n = len(A["names"])
    for j in range(n):
        if A["vt"][j] != B["vtype"][j]: issues.append(("vtype", j))
        la = bnd(A["lb"][j], -1); ua = bnd(A["ub"][j], 1)
        lb, ub = B["lb"][j], B["ub"][j]
        if B["vtype"][j] == "B" and ub is None:  # rosil default ub INF for binaries; osilx default 1
            ub = F(1); issues.append(("binary-ub-default", j)) if False else None
        if la != lb or ua != ub: issues.append(("varbound", A["names"][j], A["lb"][j], A["ub"][j], lb, ub))
    oa, ob = A["obj"], B["obj"]
    if oa["sense"] != ob["sense"] or F(oa["constant"]) != ob["const"]: issues.append(("objhead",))
    if {j: F(a) for j, a in oa["lin"].items()} != ob["lin"]: issues.append(("objlin",))
    if sorted((i, j, F(a)) for i, j, a in oa["quad"]) != sorted(ob["quad"]) or conv_tree(oa["nl"]) != ob["nl"]: issues.append(("objnl",))
    assert len(A["cons"]) == len(B["cons"])
    for r, (ca, cb) in enumerate(zip(A["cons"], B["cons"])):
        if ca["name"] != cb["name"]: issues.append(("name", r))
        la = None if osilx.isinf(ca["lb"]) else F(ca["lb"]); ua = None if osilx.isinf(ca["ub"]) else F(ca["ub"])
        if la != cb["lb"] or ua != cb["ub"]: issues.append(("conbound", ca["name"]))
        if F(ca["constant"]) != cb["const"]: issues.append(("const", ca["name"]))
        lin_a = {j: F(a) for j, a in ca["lin"].items() if F(a) != 0}
        if lin_a != cb["lin"]: issues.append(("lin", ca["name"]))
        if sorted((i, j, F(a)) for i, j, a in ca["quad"]) != sorted(cb["quad"]): issues.append(("quad", ca["name"]))
        if conv_tree(ca["nl"]) != cb["nl"]: issues.append(("nl", ca["name"]))
    nconst = sum(1 for c in A["cons"] if F(c["constant"]) != 0)
    print(f"{name}: vars {n}, rows {len(A['cons'])}, nonzero row constants {nconst}, differences {len(issues)}", issues[:5])

for name in sys.argv[1:]:
    run(name)
