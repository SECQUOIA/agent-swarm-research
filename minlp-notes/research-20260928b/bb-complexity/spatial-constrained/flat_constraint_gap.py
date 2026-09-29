"""Constraint-gap schemes: a flat optimal segment and isotropic vs anisotropic gaps.

Problem: minimize f(z) = z_2 subject to g(z) = -z_2 <= 0 on X0 = [LO, HI]^2.
f* = 0, optimal set {z_2 = 0} (a segment, p = 1).  The objective is kept exact
(alpha = 0).  The constraint relaxation is deliberately loosened with an
alphaBB-type margin (Section 5 of the note):
    iso:   -z_2 - beta (a_1(z_1) + a_2(z_2)) <= 0
    aniso: -z_2 - beta a_2(z_2)             <= 0
with a_i(z) = (z_i - l_i)(u_i - z_i).  Node bound: exact closed form (the
relaxed set is convex; the best z_1 is the midpoint, then a quadratic in z_2).
No bound tightening (constraint propagation would remove the loosening).

Reports node counts for widest-side bisection and z_2-only bisection, the
bounds of the three-box certificate split at z_2 = -0.6 and z_2 = 0, and the covering lower bound
of Theorem 5.3:  N_opt >= 2^-2 * ceil(|X0_1| / (2 sqrt(2 eps / beta))).
Usage: python3 flat_constraint_gap.py
"""
import math
import json

LO, HI = -1.2, 1.3
BETA = 1.0


def lb(l1, u1, l2, u2, iso):
    A1 = BETA * (u1 - l1) ** 2 / 4.0 if iso else 0.0
    # beta z^2 - (1 + beta(l2+u2)) z + beta l2 u2 - A1 <= 0
    a = BETA
    b = -(1.0 + BETA * (l2 + u2))
    c = BETA * l2 * u2 - A1
    D = b * b - 4 * a * c
    if D < 0:
        return math.inf
    r1 = (-b - math.sqrt(D)) / (2 * a)
    r2 = (-b + math.sqrt(D)) / (2 * a)
    lo, hi = max(l2, r1), min(u2, r2)
    if lo > hi:
        return math.inf
    return lo


def count(eps, iso, rule, max_nodes=2_000_000):
    stack = [(LO, HI, LO, HI)]
    nodes = 0
    while stack:
        l1, u1, l2, u2 = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None
        if lb(l1, u1, l2, u2, iso) >= -eps:
            continue
        if rule == "widest" and (u1 - l1) > (u2 - l2):
            m = 0.5 * (l1 + u1)
            stack += [(l1, m, l2, u2), (m, u1, l2, u2)]
        else:
            m = 0.5 * (l2 + u2)
            stack += [(l1, u1, l2, m), (l1, u1, m, u2)]
    return nodes


def main():
    for iso in (False, True):
        cert = [lb(LO, HI, LO, -0.6, iso), lb(LO, HI, -0.6, 0.0, iso), lb(LO, HI, 0.0, HI, iso)]
        print(json.dumps({"iso": iso, "three_box_certificate_bounds": cert}))
        for eps in [m * 10.0 ** (-k) for k in range(1, 8) for m in (3.0, 1.0)]:
            row = {"iso": iso, "eps": eps,
                   "widest": count(eps, iso, "widest"),
                   "z2only": count(eps, iso, "z2only")}
            if iso:
                row["cover_LB_leaves"] = math.ceil((HI - LO) / (2 * math.sqrt(2 * eps / BETA))) / 4.0
            print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
