"""Proposition 4 checks: clamped and mixed relaxation-minimizer rules on sharp 1D instances.

Instance: f(y) = sigma |y - a| on [0,1], exact alphaBB with alpha = 1, sigma = 2,
incumbent f* = 0, tolerance eps.  For every node [l,u] the relaxation minimizer
is a if a in [l,u] (sigma >= alpha * width), with value eps - (a-l)(u-a) (in m units);
nodes not containing a in their interior are pruned.  N_opt = 2 ([0,a], [a,1]).
Rule R(lam, theta): split at clip(lam*y + (1-lam)*mid, l + theta*w, u - theta*w).
The instance is a = p-bar, the root in (0,1/2) of clip(lam p + (1-lam)/2, theta, 1-theta) = p/(1-p);
along the chain the relative position of a alternates p-bar, 1-p-bar and widths shrink by
kappa = p-bar/(1-p-bar).
Exact rational arithmetic where the data are rational.
"""
from fractions import Fraction as Fr
import math


def tree(a, eps, lam, theta):
    nodes, stack = 0, [(Fr(0) if isinstance(a, Fr) else 0.0, Fr(1) if isinstance(a, Fr) else 1.0)]
    while stack:
        l, u = stack.pop()
        nodes += 1
        if not (l < a < u):
            continue                      # pruned (a not interior): value >= eps > 0
        if eps - (a - l) * (u - a) >= 0:
            continue                      # pruned at the kink
        w = u - l
        s = lam * a + (1 - lam) * (l + u) / 2
        s = min(max(s, l + theta * w), u - theta * w)
        stack += [(l, s), (s, u)]
    return nodes


def part_a():
    print("(a) lam = 1 (clamped minimizer), fixed instance a = theta/(1+theta), kappa = theta")
    for theta in (Fr(1, 5), Fr(1, 50)):
        a = theta / (1 + theta)
        for k in (4, 8, 12, 16):
            eps = Fr(1, 10 ** k)
            K = sum(1 for j in range(400) if a * (1 - a) * theta ** (2 * j) > eps)
            T = tree(a, eps, Fr(1), theta)
            T0 = tree(a, eps, Fr(1), Fr(0))
            print(f"   theta={theta} a={a} eps=1e-{k:<2d} T_clamp={T:3d} (chain prediction >= {2*K+1})   T_unclamped={T0}")
            assert T >= 2 * K + 1 and T0 == 3


def part_b():
    print("(b) mixed rule, a = p*(lam) solving lam p^2 + 1.5 (1-lam) p - (1-lam)/2 = 0; kappa = p*/(1-p*)")
    cases = [(Fr(2, 3), Fr(1, 5), Fr(1, 4))]            # exact: p* = 1/4, kappa = 1/3
    for lam in (0.25, 0.8):
        p = (-1.5 * (1 - lam) + math.sqrt(2.25 * (1 - lam) ** 2 + 2 * lam * (1 - lam))) / (2 * lam)
        cases.append((lam, 0.2 if lam == 0.25 else 0.02, p))
    for lam, theta, p in cases:
        kappa = p / (1 - p)
        for k in (4, 8, 12, 16):
            eps = Fr(1, 10 ** k) if isinstance(p, Fr) else 10.0 ** (-k)
            T = tree(p, eps, lam, theta)
            # chain nodes: width kappa^j, a at relative position p or 1-p: invalid iff p(1-p) kappa^(2j) > eps
            K = sum(1 for j in range(400) if p * (1 - p) * kappa ** (2 * j) > eps)
            print(f"   lam={float(lam):.3f} theta={float(theta):.2f} p*={float(p):.4f} kappa={float(kappa):.4f} "
                  f"eps=1e-{k:<2d} T={T:3d} (chain prediction >= {2*K+1})")
            assert T >= 2 * K + 1


if __name__ == "__main__":
    part_a()
    part_b()
    print("all assertions passed")
