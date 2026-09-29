"""1D check: alphaBB branch-and-bound with node-wise OBBT on the same relaxation.

OBBT on [l,u] replaces the box by the interval {y : phi_B(y) <= f* - eps}
(phi_B = f - alpha q_B is convex), repeated up to 20 rounds per node while it
shrinks the box by at least 1%.  Every discarded end piece is itself a valid
box for the same scheme, so leaves = pruned nodes + discarded pieces form a
box certificate and must satisfy the integral lower bound.  Uncertified
floating-point illustration (scout scratch).
"""
import numpy as np
import sbb_toy as S


def sublevel(P, l, u, c):
    """Interval {y in [l,u] : phi(y) <= c} for convex phi, or None."""
    a = P.alpha
    phi = lambda z: P.f(np.array([z])) - a * (z - l) * (u - z)
    dphi = lambda z: P.grad(np.array([z]))[0] - a * (u + l - 2 * z)
    lb, y = S.lb_1d(phi, dphi, l, u)
    if lb > c:
        return None
    y = y[0]
    if phi(y) > c:              # bound below c but no certified point: keep whole box
        return l, u

    def root(lo, hi, inside_hi):   # phi(inside end) <= c
        for _ in range(100):
            m = 0.5 * (lo + hi)
            if (phi(m) <= c) == inside_hi:
                hi = m
            else:
                lo = m
        return lo, hi
    left = l if phi(l) <= c else root(l, y, True)[0]
    right = u if phi(u) <= c else root(y, u, False)[1]
    return left, right


def run(P, eps, obbt=True):
    stack = [(P.lo[0], P.hi[0])]
    relax = leaves = 0
    while stack:
        l, u = stack.pop()
        for _ in range(20 if obbt else 1):
            relax += 1
            iv = sublevel(P, l, u, P.fstar - eps)
            if iv is None:
                leaves += 1
                l = None
                break
            if not obbt:
                break
            nl, nu = iv
            leaves += (nl > l) + (nu < u)
            shrink = (nu - nl) < 0.99 * (u - l)
            l, u = nl, nu
            if not shrink:
                break
        if l is None:
            continue
        m = 0.5 * (l + u)
        stack += [(l, m), (m, u)]
    return relax, leaves


if __name__ == "__main__":
    for key in ("nondeg1", "quartic1", "sharp1"):
        P = S.PROBLEMS[key]()
        print("==", P.name)
        for k in range(2, 9):
            eps = 10.0 ** -k
            r0, l0 = run(P, eps, obbt=False)
            r1, l1 = run(P, eps, obbt=True)
            print({"eps": eps, "plain_relax": r0, "plain_leaves": l0,
                   "obbt_relax": r1, "obbt_leaves": l1,
                   "opt_leaves": S.opt_cover_1d(P, eps),
                   "int_lb": round(S.integral_lb(P, eps, pts=[S.A1]), 2)}, flush=True)
