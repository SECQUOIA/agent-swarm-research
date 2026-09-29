"""SCIP-10-style branching point on sharp 1D instances (exact rationals).

Rule (as reported by the coordinator for SCIP 10.0.2 defaults): with root width W0,
    mu = midpull                      if w/W0 >= reldomtrig
       = midpull * (w/W0)             otherwise,
    s  = mu * mid + (1 - mu) * y      (y = relaxation minimizer),
    s  = clip(s, l + clamp*w, u - clamp*w),
midpull = 3/4, reldomtrig = 1/2, clamp = 1/5.  Variants: clamp 0 (vanishing midpull only),
and the pure minimizer rule.  Instance f(y) = 2 alpha |y - a| on [0,1] (alpha = 1), exact:
a node [l,u] with a in its interior has relaxation minimizer a and is pruned iff eps >= (a-l)(u-a);
other nodes are pruned.  N_opt = 2.
Usage: python3 scip_rule_check.py
"""
from fractions import Fraction as Fr
import math
import random


def make_rule(midpull, trig, clamp):
    def rule(l, u, y):
        w = u - l
        mu = midpull if w >= trig else midpull * w          # W0 = 1
        s = mu * (l + u) / 2 + (1 - mu) * y
        return min(max(s, l + clamp * w), u - clamp * w)
    return rule


def chain(a, eps, rule, maxlen=10 ** 6):
    """Nodes on the path of nodes containing a; returns (tree size, list of (l,u))."""
    nodes, stack, path = 0, [(Fr(0), Fr(1))], []
    while stack:
        l, u = stack.pop()
        nodes += 1
        if not (l < a < u) or eps >= (a - l) * (u - a):
            continue
        path.append((l, u))
        s = rule(l, u, a)
        if s == a:
            nodes += 2          # both children pruned (a at an endpoint)
            continue
        stack += [(l, s), (s, u)]
    return nodes, path


if __name__ == "__main__":
    scip = make_rule(Fr(3, 4), Fr(1, 2), Fr(1, 5))
    noclamp = make_rule(Fr(3, 4), Fr(1, 2), Fr(0))
    pure = make_rule(Fr(0), Fr(1, 2), Fr(0))
    a = Fr(3, 238)
    print("instance a = 3/238; SCIP-default chain (first nodes, relative position of a):")
    _, path = chain(a, Fr(1, 10 ** 12), scip)
    for (l, u) in path[:6]:
        print(f"   [{l}, {u}]  width {float(u-l):.6g}  rel. position {(a-l)/(u-l)}")
    for k in (4, 8, 12, 16, 24, 32):
        eps = Fr(1, 10 ** k)
        T = {name: chain(a, eps, r)[0] for name, r in (("scip", scip), ("scip_noclamp", noclamp), ("pure_min", pure))}
        K = sum(1 for j in range(2, 400) if Fr(5, 36) * (Fr(9, 119) / 5 ** (j - 2)) ** 2 > eps) + 2
        print(f"eps=1e-{k:<2d} nodes {T}; predicted SCIP chain >= {K} invalid nodes -> T >= {2*K+1}")
        assert T["scip"] >= 2 * K + 1 and T["pure_min"] == 3
    # random rational a: SCIP-default and no-clamp variants
    random.seed(1)
    print("random a (20 draws), max/mean nodes at eps = 1e-8, 1e-16, 1e-32:")
    for k in (8, 16, 32):
        eps = Fr(1, 10 ** k)
        res = {"scip": [], "scip_noclamp": []}
        for _ in range(20):
            a = Fr(random.randint(1, 10 ** 9 - 1), 10 ** 9)
            res["scip"].append(chain(a, eps, scip)[0])
            res["scip_noclamp"].append(chain(a, eps, noclamp)[0])
        print(f"   eps=1e-{k}: " + ", ".join(f"{n}: max {max(v)} mean {sum(v)/len(v):.1f}" for n, v in res.items()))
