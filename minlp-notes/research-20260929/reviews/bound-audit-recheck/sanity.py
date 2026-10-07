"""Negative controls for the exact checks used in this recheck (own code).

Each control perturbs a certified point by a tiny exact amount and confirms that the exact checker
(qosil.Model.violations) reports the expected row, bound or integrality violation.
"""
import os
from fractions import Fraction as F

import emfl_bounds
import qosil
import sssd_exact

HERE = os.path.dirname(os.path.abspath(__file__))
TINY = F(1, 10 ** 30)


def expect(M, x, label, kind_name):
    v = M.violations(x)
    hit = [(k, nm) for _, k, nm in v]
    ok = any(k == kind_name[0] and nm == kind_name[1] for k, nm in hit)
    print(f"  {label}: {len(v)} violation(s) {hit[:3]} -> {'caught' if ok else 'NOT CAUGHT'}")
    assert ok


# sssd22-08persp p4
M = qosil.Model(os.path.join(HERE, "data", "sssd22-08persp.osil"))
xs, _, _ = qosil.read_sol(os.path.join(HERE, "data", "sssd22-08persp.p4.sol"), M)
xs = [v if v is not None else F(0) for v in xs]
x, _, U, Qv = sssd_exact.build(M, xs)
assert not M.violations(x)
print("sssd22-08persp.p4 constructed point: 0 violations (positive control)")
q = next(j for j in Qv if x[j] > 0)
row = next(M.cname[i] for i in range(M.m) if any(q in (a, b) for a, b, c in M.Q[i])
           and any(x[v] > 0 and v in U for a, b, c in M.Q[i] for v in (a, b)))  # the row whose binary is 1
y = list(x); y[q] -= TINY
expect(M, y, f"queue variable {M.name[q]} lowered by 1e-30", ("row ub", row))
u = next(j for j in U if x[j] > 0)
y = list(x); y[u] += TINY
load = next(M.cname[i] for i in range(M.m) if u in M.A[i] and M.clb[i] == M.cub[i])
expect(M, y, f"utilization {M.name[u]} raised by 1e-30", ("row lb", load))
b = next(j for j in range(M.n) if M.type[j] == "B" and x[j] == 1)
y = list(x); y[b] = F(1, 2)
expect(M, y, f"binary {M.name[b]} set to 1/2", ("int", M.name[b]))

# smallinvDAXr2b200-220 p2: objvar just below x'Qx
M = qosil.Model(os.path.join(HERE, "data", "smallinvDAXr2b200-220.osil"))
xs, _, _ = qosil.read_sol(os.path.join(HERE, "data", "smallinvDAXr2b200-220.p2.sol"), M)
x = [v if v is not None else F(0) for v in xs]
ov = M.index["objvar"]
x[ov] = F(0); x[ov] = M.row(0, x)
assert not M.violations(x)
print("smallinvDAXr2b200-220.p2 with objvar := x'Qx: 0 violations (positive control)")
y = list(x); y[ov] -= TINY
expect(M, y, "objvar lowered by 1e-30", ("row ub", "e1"))

# emfl050_5_5: point from a rational z, one t lowered
M = qosil.Model(os.path.join(HERE, "data", "emfl050_5_5.osil"))
cones, base, defn = emfl_bounds.structure(M)
x = [F(0)] * M.n
for k, j in enumerate(base):
    x[j] = F(k + 1, 97)
for w, (coef, ew) in defn.items():
    x[w] = ew + sum((v * x[j] for j, v in coef.items()), F(0))
for _, t, ws in cones:
    x[t] = emfl_bounds.sqrt_up(sum((x[w] * x[w] for w in ws), F(0)))
assert not M.violations(x)
print("emfl050_5_5 point from an arbitrary rational z >= 0: 0 violations (positive control)")
i, t, ws = next(c for c in cones if any(x[w] != 0 for w in c[2]))
s2 = sum((x[w] * x[w] for w in ws), F(0))
y = list(x); y[t] = s2 / emfl_bounds.sqrt_up(s2) * (1 - TINY)  # strictly below sqrt(s2)
expect(M, y, f"t variable {M.name[t]} set just below |w|", ("row lb", M.cname[i]))
y = list(x); y[base[0]] = -TINY
expect(M, y, f"base variable {M.name[base[0]]} set to -1e-30", ("lb", M.name[base[0]]))

# emfl050_3_3 dual certificate: the exact check must reject small perturbations
print("emfl050_3_3 dual certificate:")
LB, UB, C = emfl_bounds.main("emfl050_3_3", [])
Y, act, groups, Ar, E, c, nb = C["Y"], C["act"], C["groups"], C["Ar"], C["E"], C["c"], C["nb"]
print("  certified:", emfl_bounds.check_cert(Y, act, groups, Ar, E, c, nb)[:2], "(positive control)")
k = max(act, key=lambda k: sum((Y[p] * Y[p] for p in groups[k]), F(0)) / c[k] ** 2)
Z = list(Y)
for p in groups[k]:
    Z[p] *= 1 + F(1, 10 ** 12)
r = emfl_bounds.check_cert(Z, act, groups, Ar, E, c, nb)
print(f"  cone {k} scaled by 1 + 1e-12: norm ok = {r[0]}, g ok = {r[1]} -> {'caught' if not r[0] else 'NOT CAUGHT'}")
assert not r[0]
g = [F(0)] * nb
for p, yp in enumerate(Y):
    for j, v in Ar[p].items():
        g[j] += v * yp
j0 = min(range(nb), key=lambda j: g[j])
p0 = next(p for p in range(len(Y)) if list(Ar[p]) == [j0])
Z = list(Y)
Z[p0] -= (g[j0] + F(1, 10 ** 20)) / Ar[p0][j0]
r = emfl_bounds.check_cert(Z, act, groups, Ar, E, c, nb)
print(f"  g_{j0} pushed to -1e-20: g ok = {r[1]} -> {'caught' if not r[1] else 'NOT CAUGHT'}")
assert not r[1]
