"""Re-evaluate the constructed sssd and smallinvDAX points with the previous verifier's separate
exact evaluator (reviews/bound-audit-verification/osil.py): rows, bounds, integrality, objective."""
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "bound-audit-verification"))
import osil
import qosil
import sssd_exact


def other_check(path, x):
    B = osil.parse(path)
    bad = 0
    for j in range(B.n):
        bad += (B.lb[j] is not None and x[j] < B.lb[j]) + (B.ub[j] is not None and x[j] > B.ub[j])
        bad += B.vtype[j] in ("B", "I") and x[j].denominator != 1
    for i in range(B.m):
        v = osil.row_exact(B, i, x)
        bad += (B.clb[i] is not None and v < B.clb[i]) + (B.cub[i] is not None and v > B.cub[i])
    return bad, osil.obj_exact(B, x)


for tag in ["sssd20-04persp.p3", "sssd22-08persp.p4", "sssd22-08persp.p3", "sssd25-04persp.p3",
            "sssd25-08persp.p4", "sssd25-08persp.p3", "smallinvDAXr2b150-165.p2", "smallinvDAXr2b200-220.p2"]:
    name, pt = tag.rsplit(".", 1)
    path = os.path.join(HERE, "data", name + ".osil")
    M = qosil.Model(path)
    xs, _, _ = qosil.read_sol(os.path.join(HERE, "data", f"{name}.{pt}.sol"), M)
    xs = [v if v is not None else F(0) for v in xs]
    if name.startswith("sssd"):
        x = sssd_exact.build(M, xs)[0]
    else:
        x = list(xs)
        ov = M.index["objvar"]
        x[ov] = F(0)
        x[ov] = M.row(0, x)
    bad, f = other_check(path, x)
    same = f == M.objective(x)
    print(f"{tag}: violations by the other evaluator: {bad}; objective {sssd_exact.fmt(f, 12)}; equal to own value: {same}")
    assert bad == 0 and same
