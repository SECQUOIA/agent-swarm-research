"""Reviewer check of Proposition 4 and of the solver branching-point rules.

Instance f(y) = 2|y - a| on [0,1], alpha = 1, incumbent 0.  For a node [l,u]
containing a in its interior the unique relaxation minimizer is a and the node
is invalid iff (a-l)(u-a) > eps; other nodes are pruned (note, Prop. 4 steps
2-3, re-derived by the reviewer).  So the tree only depends on where the rule
splits nodes that contain a.

Part 1: table of p-bar and kappa (mpmath, 40 digits) and chain simulation with
        p-bar computed to 60 digits (mpmath) or exactly (Fractions).
Part 2: SCIP 10 rule as implemented in src/scip/branch.c (master, fetched
        2026-09-28): LP value x, midpull 0.75 scaled by the local/global width
        ratio r when r < 0.5, then clamp 0.2.  Couenne default "mid-point":
        0.25 x + 0.75 mid, clamped to [l + 0.05 w, u - 0.05 w].
        These rules are simulated in exact rationals for several kink
        positions a, including a = 1/6 (the note's SCIP instance).
"""
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60


def tree(a, eps, split, cap=10 ** 5):
    nodes, stack = 0, [(Fr(0), Fr(1)) if isinstance(a, Fr) else (mp.mpf(0), mp.mpf(1))]
    while stack:
        l, u = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if not (l < a < u) or (a - l) * (u - a) <= eps:
            continue
        s = split(l, u, a)
        assert l < s < u
        stack += [(l, s), (s, u)]
    return nodes


def mixrule(lam, theta):
    def split(l, u, x):
        w = u - l
        s = lam * x + (1 - lam) * (l + u) / 2
        return min(max(s, l + theta * w), u - theta * w)
    return split


def scip_rule(l, u, x):
    midpull = Fr(3, 4)
    r = (u - l) / 1                      # global domain [0,1]
    if r < Fr(1, 2):
        midpull *= r
    b = midpull * (l + u) / 2 + (1 - midpull) * x
    w = u - l
    return min(max(b, l + Fr(1, 5) * w), u - Fr(1, 5) * w)


def couenne_rule(l, u, x):
    b = Fr(1, 4) * x + Fr(3, 4) * (l + u) / 2
    w = u - l
    if (b - l) / w < Fr(1, 20):
        b = l + w / 20
    elif (u - b) / w < Fr(1, 20):
        b = u - w / 20
    return b


def M(v):
    return mp.mpf(v.numerator) / v.denominator if isinstance(v, Fr) else mp.mpf(str(v))


def pbar(lam, theta):
    lam, theta = M(lam), M(theta)
    h = lambda p: min(max(lam * p + (1 - lam) / 2, theta), 1 - theta) - p / (1 - p)
    lo, hi = mp.mpf(0), mp.mpf('0.5')
    assert h(lo) > 0 and h(hi) < 0
    for _ in range(220):
        mid = (lo + hi) / 2
        if h(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def part1():
    print("Part 1: p-bar, kappa and chains for R_{lambda,theta}")
    table = [("SCIP per Speakman-Lee", 1, 0.2), ("Couenne (0.25,0.2)", 0.25, 0.2), ("Couenne actual (0.25,0.05)", 0.25, 0.05),
             ("scout mix", 0.8, 0.02), ("exact example", Fr(2, 3), Fr(1, 5)), ("bisection", 0, 0.2),
             ("SCIP root-level (0.25,0.2)", 0.25, 0.2), ("tiny clamp", 1, 0.001), ("tiny mixing", 0.999, 0)]
    for name, lam, theta in table:
        p = pbar(lam, theta)
        kappa = p / (1 - p)
        Ts = []
        for k in (4, 8, 16, 32):
            eps = mp.mpf(10) ** (-k)
            T = tree(p, eps, mixrule(M(lam), M(theta)))
            K = int(mp.ceil(mp.log(p * (1 - p) / eps) / (2 * mp.log(1 / kappa))))
            assert T >= 2 * K + 1, (name, k, T, K)
            Ts.append((k, T, 2 * K + 1))
        print(f"  {name:28s} lam={float(lam):.3f} theta={float(theta):.3f} p-bar={mp.nstr(p, 6)} kappa={mp.nstr(kappa, 6)}  "
              + "  ".join(f"eps=1e-{k}: T={T} (>= {b})" for k, T, b in Ts))
    # exact rational cases
    for lam, theta, p in ((Fr(1), Fr(1, 5), Fr(1, 6)), (Fr(2, 3), Fr(1, 5), Fr(1, 4)), (Fr(0), Fr(1, 5), Fr(1, 3))):
        kappa = p / (1 - p)
        assert mixrule(lam, theta)(Fr(0), Fr(1), p) == kappa
        T = [tree(p, Fr(1, 10 ** k), mixrule(lam, theta)) for k in (4, 8, 16, 32)]
        print(f"  exact lam={lam} theta={theta} p-bar={p}: T at eps=1e-4,1e-8,1e-16,1e-32: {T}; pure minimizer: "
              f"{[tree(p, Fr(1, 10 ** k), mixrule(Fr(1), Fr(0))) for k in (4, 32)]}")


def part2():
    print("Part 2: actual solver rules (exact rationals), T at eps = 1e-4, 1e-8, 1e-16, 1e-32, 1e-64")
    for name, rule in (("SCIP 10 default", scip_rule), ("Couenne default", couenne_rule),
                       ("pure minimizer", mixrule(Fr(1), Fr(0)))):
        for a in (Fr(1, 6), Fr(1, 3), Fr(1, 7), Fr(2, 5), Fr(3, 10), Fr(123, 1000), Fr(1, 2)):
            T = [tree(a, Fr(1, 10 ** k), rule) for k in (4, 8, 16, 32, 64)]
            print(f"  {name:16s} a={str(a):9s} T={T}")


if __name__ == "__main__":
    part1()
    part2()
    print("all assertions passed")
