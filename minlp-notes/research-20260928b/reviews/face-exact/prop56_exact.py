"""Reviewer's exact rational replay of Proposition 5.6 (min-score strong branching, Couenne point).

Scout instance f = 2|x-a| - (x-a)(y-b), a = 1/3 (b irrelevant as long as L > |c| max|y-b|).
Exact straddling-box bound (checked in floats against a vertex enumeration in kink_rules.py, part [1]):
    LB = -w_y (a-l_x)(u_x-a)/w_x,  xhat = a,  yhat at relative position rho = (a-l_x)/w_x (c < 0).
Non-straddling boxes have LB >= 0 (Theorem 4.4); for the min score only the straddling child matters.
Rule: point R(1/4, 1/5) for both variables; choose the variable maximising min(child LBs);
ties -> x.  Counts processed nodes (all generated nodes), pruning iff LB >= -eps, all in Fractions.
"""
from fractions import Fraction as Fr

a = Fr(1, 3)
al, be = Fr(1, 4), Fr(1, 5)


def straddle(b):
    return b[0] < a < b[1]


def lb(b):
    if not straddle(b):
        return Fr(0)
    lx, ux, ly, uy = b
    return -(uy - ly) * (a - lx) * (ux - a) / (ux - lx)


def point(l, u, xh):
    w = u - l
    p = al * xh + (1 - al) * (l + u) / 2
    return min(max(p, l + be * w), u - be * w)


def decide(b):
    lx, ux, ly, uy = b
    rho = (a - lx) / (ux - lx)
    yh = ly + rho * (uy - ly)
    px, py = point(lx, ux, a), point(ly, uy, yh)
    cx = ((lx, px, ly, uy), (px, ux, ly, uy))
    cy = ((lx, ux, ly, py), (lx, ux, py, uy))
    sx, sy = min(lb(c) for c in cx), min(lb(c) for c in cy)
    return ("x", cx, sx, sy) if sx >= sy else ("y", cy, sx, sy)


def count(eps, trace=False):
    stack = [(Fr(0), Fr(1), Fr(0), Fr(1))]
    n = 0
    shown = 0
    while stack:
        b = stack.pop()
        n += 1
        if lb(b) >= -eps:
            continue
        var, ch, sx, sy = decide(b)
        if trace and shown < 6 and b[2] == 0 and b[3] == 1:
            print(f"    x-range [{b[0]}, {b[1]}], rho = {(a - b[0]) / (b[1] - b[0])}: min child LB "
                  f"x {float(sx):.6f}, y {float(sy):.6f} -> {var}")
            shown += 1
        stack.extend(ch)
    return n


if __name__ == "__main__":
    print("[path] straddling boxes with full y-range:")
    count(Fr(1, 10**3), trace=True)
    lx, ux = Fr(49, 192), Fr(539, 1536)
    D = (a - lx) * (ux - a) / (ux - lx)
    print(f"[column] D = {D} = {float(D):.6f}; 2D = {float(2 * D):.5f}")
    for k in (2, 3, 4, 5, 6):
        eps = Fr(1, 10**k)
        n = count(eps)
        print(f"    eps=1e-{k}: nodes = {n}; bound 2D/eps - 1 = {float(2 * D / eps - 1):.1f}; ok = {n >= 2 * D / eps - 1}")
